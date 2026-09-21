"""Shadow-only Jev research advisory for the opportunity-routing engine.

Jev may help sequence research. It may not create commercial truth, reverse an
existing demotion, promote a formation, mutate commercial state, or turn model
confidence into evidence.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Protocol

CONTRACT = "OPPORTUNITY_JEV_RESEARCH_ADVISORY_V1"
STATE_SCHEMA_VERSION = "OPPORTUNITY_JEV_RESEARCH_STATE_V1"
QUESTION_SET_VERSION = "OPPORTUNITY_JEV_RESEARCH_ROUTING_V1"

ALLOWED_ROUTES = {
    "NO_FURTHER_RESEARCH",
    "EXACT_INCUMBENT_PREFLIGHT",
    "CAUSAL_DESCENT",
    "HUMAN_REVIEW",
}
ALLOWED_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}
ALLOWED_EVIDENCE_STATES = {
    "ADEQUATE_FOR_CURRENT_RESEARCH_STAGE",
    "INSUFFICIENT",
    "CONFLICTED",
    "STALE_OR_LINEAGE_UNCLEAR",
}

QUESTION_SPECS: dict[str, dict[str, Any]] = {
    "needs_exact_incumbent_preflight": {
        "type": "noul",
        "instructions": (
            "Given only the supplied bounded research record, is an exact current "
            "incumbent/control-loop preflight still needed before expensive research? "
            "Judge research sequencing only. Do not infer commercial truth, reverse an "
            "existing engine demotion, or recommend promotion."
        ),
    },
    "needs_deeper_causal_research": {
        "type": "noul",
        "instructions": (
            "If the authoritative existing closure does not already end this research "
            "path, would deeper causal research materially help resolve the remaining "
            "uncertainty? Judge research sequencing only and do not invent evidence."
        ),
    },
    "research_route": {
        "type": "choice",
        "instructions": (
            "Choose the most appropriate next research route from the supplied record. "
            "Existing engine verdicts and hard-floor closures remain authoritative. "
            "This is advisory research routing only, never commercial promotion."
        ),
        "criteria": {
            "NO_FURTHER_RESEARCH": (
                "The supplied authoritative record already closes or demotes this path, "
                "so no extra research is justified from the current evidence."
            ),
            "EXACT_INCUMBENT_PREFLIGHT": (
                "Before deeper work, verify whether an exact current incumbent, native "
                "control surface, or platform-owned loop already absorbs the proposed edge."
            ),
            "CAUSAL_DESCENT": (
                "After required preflight, deeper falsifiable causal research is the next "
                "useful step for a still-open formation."
            ),
            "HUMAN_REVIEW": (
                "The record is materially conflicting, ambiguous, or high-stakes enough "
                "that a human should inspect it before further automated research."
            ),
        },
    },
    "attention_priority": {
        "type": "choice",
        "instructions": (
            "How much research attention should this record receive relative to other "
            "research work? This is research priority, not business attractiveness."
        ),
        "criteria": {
            "LOW": "Routine or no further research attention is appropriate.",
            "MEDIUM": "Meaningful uncertainty remains but is not unusually urgent.",
            "HIGH": "A material unresolved research question justifies prompt attention.",
        },
    },
    "evidence_state": {
        "type": "choice",
        "instructions": (
            "Which label best describes the evidence state shown? Judge only supplied "
            "evidence and lineage. Model confidence is not evidence."
        ),
        "criteria": {
            "ADEQUATE_FOR_CURRENT_RESEARCH_STAGE": (
                "The supplied evidence is adequate for the current research-stage conclusion."
            ),
            "INSUFFICIENT": "Important research questions remain unresolved by the supplied evidence.",
            "CONFLICTED": "Material supplied evidence conflicts and needs reconciliation.",
            "STALE_OR_LINEAGE_UNCLEAR": "Freshness, provenance, or lineage is too unclear to rely on.",
        },
    },
}


class JevProvider(Protocol):
    def evaluate(
        self,
        state: Mapping[str, Any],
        *,
        model: str,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        """Return normalized provider output for one compact state."""


@dataclass(frozen=True)
class JevResearchConfig:
    enabled: bool = False
    shadow_mode: bool = True
    model: str = "jev-latest"
    timeout_seconds: float = 3.0
    max_retries: int = 1

    @classmethod
    def from_env(cls) -> "JevResearchConfig":
        return cls(
            enabled=_env_bool("JEV_ENABLED", False),
            shadow_mode=_env_bool("JEV_SHADOW_MODE", True),
            model=(os.getenv("JEV_MODEL") or "jev-latest").strip() or "jev-latest",
            timeout_seconds=_env_float("JEV_TIMEOUT_SECONDS", 3.0, minimum=0.1),
            max_retries=_env_int("JEV_MAX_RETRIES", 1, minimum=0, maximum=5),
        )


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: float, *, minimum: float) -> float:
    try:
        value = float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return max(minimum, value)


def _env_int(name: str, default: int, *, minimum: int, maximum: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default
    return min(maximum, max(minimum, value))


def _compact_text(value: Any, limit: int = 900) -> str:
    text = str(value or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _safe_dump(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        dumped = model_dump()
        return dict(dumped) if isinstance(dumped, Mapping) else {}
    dict_method = getattr(value, "dict", None)
    if callable(dict_method):
        dumped = dict_method()
        return dict(dumped) if isinstance(dumped, Mapping) else {}
    raw = getattr(value, "__dict__", None)
    return dict(raw) if isinstance(raw, Mapping) else {}


def _choice_payload(answer: Any) -> dict[str, Any]:
    raw = _safe_dump(answer)
    choice = getattr(answer, "choice", raw.get("choice"))
    confidence = getattr(answer, "confidence", raw.get("confidence"))
    probabilities = getattr(answer, "probabilities", raw.get("probabilities"))
    result: dict[str, Any] = {"type": "choice", "choice": str(choice or "")}
    if isinstance(confidence, (int, float)):
        result["confidence"] = round(float(confidence), 6)
    if isinstance(probabilities, Mapping):
        result["probabilities"] = {
            str(key): round(float(value), 6)
            for key, value in probabilities.items()
            if isinstance(value, (int, float))
        }
    return result


def _noul_payload(answer: Any) -> dict[str, Any]:
    raw = _safe_dump(answer)
    probability = getattr(answer, "noul", raw.get("noul"))
    try:
        value = float(probability)
    except (TypeError, ValueError):
        value = 0.5
    value = min(1.0, max(0.0, value))
    return {
        "type": "noul",
        "probability": round(value, 6),
        "answer": value >= 0.5,
        "confidence": round(abs(value - 0.5) * 2.0, 6),
        "confidence_kind": "derived_from_binary_probability",
    }


def build_research_states(
    *,
    scan: Mapping[str, Any],
    commercial_state: Mapping[str, Any] | None = None,
    max_entities: int = 12,
) -> list[dict[str, Any]]:
    """Build compact Jev inputs while preserving authoritative engine conclusions."""

    max_entities = max(1, min(int(max_entities), 100))
    commercial = dict(commercial_state or {})
    examined = scan.get("examined_formations")
    rows = examined if isinstance(examined, list) else []
    active_promotions = {
        str(item)
        for item in (scan.get("active_commercial_candidate_promotions") or [])
    }
    retained = {
        str(item)
        for item in (scan.get("retained_research_formations") or [])
    }

    states: list[dict[str, Any]] = []
    for raw in rows[:max_entities]:
        if not isinstance(raw, Mapping):
            continue
        title = str(raw.get("title") or "").strip()
        if not title:
            continue
        verdict = str(raw.get("verdict") or "UNKNOWN").strip() or "UNKNOWN"
        is_closed = verdict.startswith(("DEMOTED_", "REJECTED_", "CLOSED_"))
        states.append(
            {
                "state_schema_version": STATE_SCHEMA_VERSION,
                "scan_context": {
                    "scan_id": str(scan.get("scan_id") or ""),
                    "as_of_date": str(scan.get("as_of_date") or ""),
                    "status": str(scan.get("status") or ""),
                    "search_mode": _compact_text(scan.get("search_mode"), 1200),
                    "next_scan_id": str(scan.get("next_scan_id") or commercial.get("next_scan_id") or ""),
                    "next_search_boundary": _compact_text(
                        scan.get("next_search_boundary")
                        or commercial.get("current_research_action"),
                        1200,
                    ),
                    "first_external_value_flow": str(
                        scan.get("first_external_value_flow")
                        or commercial.get("first_external_value_flow")
                        or "UNKNOWN"
                    ),
                },
                "formation": {
                    "title": title,
                    "chinese_title": str(raw.get("chinese_title") or ""),
                    "evidence_class": str(raw.get("evidence_class") or ""),
                    "evidence_summary": _compact_text(raw.get("evidence_summary"), 1400),
                },
                "authoritative_engine_context": {
                    "existing_verdict": verdict,
                    "existing_closure_authoritative": is_closed,
                    "already_commercially_promoted": title in active_promotions,
                    "already_retained_for_research": title in retained,
                    "active_commercial_candidate_count": len(
                        commercial.get("active_commercial_candidates") or []
                    ),
                    "current_validation_formation": str(
                        (commercial.get("current_validation_state") or {}).get("formation_id")
                        if isinstance(commercial.get("current_validation_state"), Mapping)
                        else ""
                    ),
                },
                "guardrails": {
                    "jev_authority": "SHADOW_RESEARCH_ADVISORY_ONLY",
                    "commercial_promotion_authority": False,
                    "mutates_commercial_state": False,
                    "may_reverse_existing_demotions": False,
                    "may_create_active_candidate": False,
                    "llm_confidence_is_commercial_evidence": False,
                    "unknown_is_pass": False,
                },
            }
        )
    return states


class TypeSafeJevProvider:
    """Thin optional dependency boundary around typesafe-sdk."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def evaluate(
        self,
        state: Mapping[str, Any],
        *,
        model: str,
        timeout_seconds: float,
    ) -> dict[str, Any]:
        try:
            from typesafe_sdk import Choice, Noul, TypeSafeClient
        except ImportError as exc:
            raise RuntimeError(
                "typesafe-sdk is required for live Jev evaluation; install typesafe-sdk==0.7.0"
            ) from exc

        questions: dict[str, Any] = {}
        for question_id, spec in QUESTION_SPECS.items():
            if spec["type"] == "noul":
                questions[question_id] = Noul(instructions=spec["instructions"])
            else:
                questions[question_id] = Choice(
                    instructions=spec["instructions"],
                    criteria=dict(spec["criteria"]),
                )

        with TypeSafeClient(
            api_key=self.api_key,
            model=model,
            timeout=timeout_seconds,
        ) as client:
            response = client.system_one(state=dict(state), questions=questions)

        answers = getattr(response, "answers", None)
        choices = getattr(response, "choices", None)
        nouls = getattr(response, "nouls", None)
        decisions: dict[str, dict[str, Any]] = {}
        for question_id, spec in QUESTION_SPECS.items():
            answer: Any = None
            if isinstance(answers, Mapping):
                answer = answers.get(question_id)
            if answer is None and spec["type"] == "choice" and isinstance(choices, Mapping):
                answer = choices.get(question_id)
            if answer is None and spec["type"] == "noul" and isinstance(nouls, Mapping):
                answer = nouls.get(question_id)
            if answer is None:
                raise ValueError(f"Jev response missing answer for {question_id}")
            decisions[question_id] = (
                _noul_payload(answer)
                if spec["type"] == "noul"
                else _choice_payload(answer)
            )

        return {
            "model": str(getattr(response, "model", model) or model),
            "decisions": decisions,
            "usage": _safe_dump(getattr(response, "usage", None)),
        }


def _fingerprint(state: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        state,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:20]


def _error_kind(exc: Exception) -> str:
    text = f"{type(exc).__name__} {exc}".lower()
    return "TIMEOUT" if "timeout" in text else "ERROR"


def _valid_choice(decisions: Mapping[str, Any], key: str, allowed: set[str]) -> bool:
    raw = decisions.get(key)
    return (
        isinstance(raw, Mapping)
        and str(raw.get("choice") or "") in allowed
    )


def _valid_noul(decisions: Mapping[str, Any], key: str) -> bool:
    raw = decisions.get(key)
    return isinstance(raw, Mapping) and isinstance(raw.get("answer"), bool)


def evaluate_research_advisory(
    *,
    states: list[Mapping[str, Any]],
    config: JevResearchConfig,
    provider: JevProvider | None = None,
) -> dict[str, Any]:
    """Evaluate research sequencing without any mutation path to commercial truth."""

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    base: dict[str, Any] = {
        "contract": CONTRACT,
        "generated_at": now,
        "authority": "SHADOW_RESEARCH_ADVISORY_ONLY",
        "commercial_promotion_authority": False,
        "mutates_commercial_state": False,
        "may_reverse_existing_demotions": False,
        "may_create_active_candidate": False,
        "llm_confidence_is_commercial_evidence": False,
        "unknown_is_pass": False,
        "state_schema_version": STATE_SCHEMA_VERSION,
        "question_set_version": QUESTION_SET_VERSION,
        "requested_model": config.model,
        "shadow_mode": config.shadow_mode,
        "entity_count": len(states),
        "rows": [],
    }

    if not config.enabled:
        base["execution_status"] = "SKIPPED_DISABLED"
        base["summary"] = _summary([])
        return base
    if not config.shadow_mode:
        base["execution_status"] = "REFUSED_NON_SHADOW"
        base["summary"] = _summary([])
        return base

    if provider is None:
        api_key = (os.getenv("TYPESAFE_API_KEY") or "").strip()
        if not api_key:
            base["execution_status"] = "SKIPPED_NO_SECRET"
            base["summary"] = _summary([])
            return base
        provider = TypeSafeJevProvider(api_key)

    rows: list[dict[str, Any]] = []
    for state in states:
        formation = state.get("formation") if isinstance(state.get("formation"), Mapping) else {}
        engine = (
            state.get("authoritative_engine_context")
            if isinstance(state.get("authoritative_engine_context"), Mapping)
            else {}
        )
        title = str(formation.get("title") or "")
        started = time.perf_counter()
        result: dict[str, Any] | None = None
        error: Exception | None = None
        attempts = 0

        for attempt in range(config.max_retries + 1):
            attempts = attempt + 1
            try:
                result = provider.evaluate(
                    state,
                    model=config.model,
                    timeout_seconds=config.timeout_seconds,
                )
                error = None
                break
            except Exception as exc:  # provider/network boundary
                error = exc

        latency_ms = round((time.perf_counter() - started) * 1000.0, 3)
        row: dict[str, Any] = {
            "formation_id": title,
            "existing_engine_verdict": str(engine.get("existing_verdict") or "UNKNOWN"),
            "existing_closure_authoritative": engine.get("existing_closure_authoritative") is True,
            "state_fingerprint": _fingerprint(state),
            "attempts": attempts,
            "latency_ms": latency_ms,
            "commercial_promotion_authority": False,
            "mutates_commercial_state": False,
            "may_reverse_existing_demotions": False,
            "may_create_active_candidate": False,
            "llm_confidence_is_commercial_evidence": False,
            "unknown_is_pass": False,
        }

        if error is not None or result is None:
            row.update(
                {
                    "status": "FAILED",
                    "error_kind": _error_kind(error or RuntimeError("missing provider result")),
                    "error": _compact_text(error or "missing provider result", 500),
                }
            )
        else:
            decisions = result.get("decisions")
            decisions_map = decisions if isinstance(decisions, Mapping) else {}
            contract_ok = (
                _valid_noul(decisions_map, "needs_exact_incumbent_preflight")
                and _valid_noul(decisions_map, "needs_deeper_causal_research")
                and _valid_choice(decisions_map, "research_route", ALLOWED_ROUTES)
                and _valid_choice(decisions_map, "attention_priority", ALLOWED_PRIORITIES)
                and _valid_choice(decisions_map, "evidence_state", ALLOWED_EVIDENCE_STATES)
            )
            if not contract_ok:
                row.update(
                    {
                        "status": "FAILED",
                        "error_kind": "INVALID_TYPED_RESPONSE",
                        "error": "Jev response failed the bounded advisory contract",
                    }
                )
            else:
                row.update(
                    {
                        "status": "SUCCESS",
                        "served_model": str(result.get("model") or config.model),
                        "decisions": dict(decisions_map),
                        "usage": dict(result.get("usage") or {}),
                    }
                )
        rows.append(row)

    base["rows"] = rows
    base["summary"] = _summary(rows)
    base["execution_status"] = (
        "SUCCESS"
        if rows and all(row.get("status") == "SUCCESS" for row in rows)
        else "PARTIAL_FAILURE"
        if any(row.get("status") == "SUCCESS" for row in rows)
        else "FAILED"
    )
    return base


def _summary(rows: list[Mapping[str, Any]]) -> dict[str, Any]:
    successes = [row for row in rows if row.get("status") == "SUCCESS"]
    failures = [row for row in rows if row.get("status") == "FAILED"]
    route_counts: dict[str, int] = {}
    for row in successes:
        decisions = row.get("decisions")
        if not isinstance(decisions, Mapping):
            continue
        route = decisions.get("research_route")
        if isinstance(route, Mapping):
            choice = str(route.get("choice") or "")
            if choice:
                route_counts[choice] = route_counts.get(choice, 0) + 1
    return {
        "evaluated": len(rows),
        "success": len(successes),
        "failed": len(failures),
        "route_counts": dict(sorted(route_counts.items())),
    }


def render_advisory_markdown(payload: Mapping[str, Any]) -> str:
    summary = payload.get("summary") if isinstance(payload.get("summary"), Mapping) else {}
    lines = [
        "# Jev Opportunity Research Advisory",
        "",
        f"- execution: **{payload.get('execution_status') or 'UNKNOWN'}**",
        "- authority: **SHADOW RESEARCH ADVISORY ONLY**",
        "- commercial promotion authority: **False**",
        "- may reverse existing demotions: **False**",
        "- may create active candidate: **False**",
        "- LLM confidence is commercial evidence: **False**",
        "- UNKNOWN != PASS",
        f"- evaluated: **{summary.get('evaluated', 0)}**",
        f"- successful: **{summary.get('success', 0)}**",
        "",
        "## Advisory rows",
        "",
    ]
    rows = payload.get("rows") if isinstance(payload.get("rows"), list) else []
    if not rows:
        lines.append("- No advisory rows available.")
    else:
        for row in rows:
            decisions = row.get("decisions") if isinstance(row.get("decisions"), Mapping) else {}
            route = decisions.get("research_route") if isinstance(decisions, Mapping) else None
            route_choice = route.get("choice") if isinstance(route, Mapping) else "N/A"
            priority = decisions.get("attention_priority") if isinstance(decisions, Mapping) else None
            priority_choice = priority.get("choice") if isinstance(priority, Mapping) else "N/A"
            lines.append(
                "- "
                f"{row.get('formation_id')} | engine={row.get('existing_engine_verdict')} | "
                f"route={route_choice} | priority={priority_choice} | status={row.get('status')}"
            )
    lines.extend(
        [
            "",
            "> This artifact is a research-sequencing second opinion only. Engine evidence, "
            "hard floors, formation validation, leverage gates, and commercial state remain authoritative.",
            "",
        ]
    )
    return "\n".join(lines)
