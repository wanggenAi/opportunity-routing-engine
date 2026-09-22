"""Run the opportunity-routing Jev advisory against a persisted attraction scan."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.jev_research_advisory import (
    JevResearchConfig,
    build_continuation_directive,
    build_research_states,
    evaluate_research_advisory,
    render_advisory_markdown,
)


def _load_object(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def resolve_scan_path(
    requested: str,
    commercial_state: dict,
    *,
    research_dir: Path = Path("data/research_runs"),
) -> Path:
    """Resolve an explicit scan path or the current persisted commercial scan."""

    requested = str(requested or "auto").strip()
    if requested.lower() != "auto":
        path = Path(requested)
        if not path.is_file():
            raise FileNotFoundError(f"scan JSON not found: {path}")
        return path

    scan_id = str(commercial_state.get("last_completed_scan_id") or "").strip()
    if scan_id:
        candidate = research_dir / f"{scan_id.lower()}.json"
        if candidate.is_file():
            return candidate

    candidates: list[tuple[int, Path]] = []
    for path in research_dir.glob("attraction_scan_*.json"):
        suffix = path.stem.removeprefix("attraction_scan_")
        if suffix.isdigit():
            candidates.append((int(suffix), path))
    if not candidates:
        raise FileNotFoundError(
            "no persisted attraction scan found for automatic Jev advisory"
        )
    return max(candidates, key=lambda item: item[0])[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scan-json",
        default="auto",
        help="Persisted attraction scan JSON, or 'auto' to follow commercial state",
    )
    parser.add_argument(
        "--commercial-state-json",
        type=Path,
        default=Path("data/commercial_reset_state.json"),
    )
    parser.add_argument("--max-entities", type=int, default=6)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(".artifacts/jev-research-advisory"),
    )
    parser.add_argument("--require-success", action="store_true")
    args = parser.parse_args()

    commercial_state = _load_object(args.commercial_state_json)
    scan_path = resolve_scan_path(args.scan_json, commercial_state)
    scan = _load_object(scan_path)
    states = build_research_states(
        scan=scan,
        commercial_state=commercial_state,
        max_entities=args.max_entities,
    )
    examined_formations = scan.get("examined_formations")
    authoritative_zero_admission = (
        scan.get("status") == "COMPLETE"
        and scan.get("zero_primary_admissions") is True
        and isinstance(examined_formations, list)
        and len(examined_formations) == 0
    )
    payload = evaluate_research_advisory(
        states=states,
        config=JevResearchConfig.from_env(),
        authoritative_zero_admission=authoritative_zero_admission,
    )
    payload["input_scan_path"] = scan_path.as_posix()
    payload["input_scan_id"] = str(scan.get("scan_id") or "")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "jev_research_advisory.json"
    md_path = args.output_dir / "jev_research_advisory.md"
    state_path = args.output_dir / "jev_research_states.json"
    continuation_path = args.output_dir / "jev_continuation_directive.json"
    continuation = build_continuation_directive(payload)

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_advisory_markdown(payload), encoding="utf-8")
    state_path.write_text(
        json.dumps(states, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    continuation_path.write_text(
        json.dumps(continuation, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "execution_status": payload.get("execution_status"),
                "input_scan_id": payload.get("input_scan_id"),
                "input_scan_path": payload.get("input_scan_path"),
                "entity_count": payload.get("entity_count"),
                "authoritative_zero_admission": payload.get(
                    "authoritative_zero_admission"
                ),
                "summary": payload.get("summary"),
                "continuation_next_action": continuation.get("next_action"),
                "autonomous_continuation_allowed": continuation.get(
                    "autonomous_continuation_allowed"
                ),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )

    if args.require_success and payload.get("execution_status") != "SUCCESS":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
