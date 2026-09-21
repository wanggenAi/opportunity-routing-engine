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
    build_research_states,
    evaluate_research_advisory,
    render_advisory_markdown,
)


def _load_object(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scan-json",
        type=Path,
        default=Path("data/research_runs/attraction_scan_035.json"),
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

    scan = _load_object(args.scan_json)
    commercial_state = _load_object(args.commercial_state_json)
    states = build_research_states(
        scan=scan,
        commercial_state=commercial_state,
        max_entities=args.max_entities,
    )
    payload = evaluate_research_advisory(
        states=states,
        config=JevResearchConfig.from_env(),
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "jev_research_advisory.json"
    md_path = args.output_dir / "jev_research_advisory.md"
    state_path = args.output_dir / "jev_research_states.json"

    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_advisory_markdown(payload), encoding="utf-8")
    state_path.write_text(
        json.dumps(states, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "execution_status": payload.get("execution_status"),
                "entity_count": payload.get("entity_count"),
                "summary": payload.get("summary"),
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
