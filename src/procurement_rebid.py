"""Build strict program-level rebid signals from explicit failed-package evidence.

A rebid signal is a CHANGE / FRICTION observation. It does not promote canonical
need state, identify a payer, prove payment, infer exact package mapping, or select a
commercial winner.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Iterable, Mapping

from src.live_imbalance_ledger import classify_procurement_event


def _text(value: object) -> str | None:
    text = " ".join(str(value or "").split())
    return text or None


def _iso_date(value: object) -> date | None:
    text = _text(value)
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _source_refs(*items: Mapping[str, Any]) -> list[str]:
    refs: list[str] = []
    for item in items:
        for key in ("source_id", "url"):
            text = _text(item.get(key))
            if text and text not in refs:
                refs.append(text)
    return refs


def _failure_groups(failures: Iterable[Mapping[str, Any]]) -> dict[tuple[str, str, str], list[Mapping[str, Any]]]:
    grouped: dict[tuple[str, str, str], list[Mapping[str, Any]]] = {}
    for failure in failures:
        if failure.get("outcome_state") != "EXPLICIT_PACKAGE_VOID":
            continue
        project_id = _text(failure.get("project_id"))
        project_name = _text(failure.get("project_name"))
        buyer_actor = _text(failure.get("buyer_actor"))
        if not project_id or not project_name or not buyer_actor:
            continue
        key = (project_id, project_name, buyer_actor)
        grouped.setdefault(key, []).append(failure)
    return grouped


def build_procurement_rebid_signals(
    tender_payload: Mapping[str, Any] | None,
    failure_payload: Mapping[str, Any] | None,
    *,
    geography: str = "Xuzhou",
    max_days_after_failure: int = 45,
) -> dict[str, Any]:
    """Link a later tender to an earlier explicit package failure conservatively.

    Required program-level lineage:
    - prior result has at least one explicit failed package;
    - later tender has a different exact project ID;
    - normalized project name is exactly equal;
    - prior buyer identity is explicitly present in the later tender title;
    - both artifacts classify to the same exact canonical capability;
    - later publication date is after the failure result and within the bounded window.

    This deliberately stops at program-level lineage. Exact old-package -> new-package
    mapping requires package-scope evidence and is not inferred here.
    """

    if not isinstance(max_days_after_failure, int) or max_days_after_failure < 1:
        raise ValueError("max_days_after_failure must be a positive integer")

    tenders = [
        item for item in (tender_payload or {}).get("events", []) or []
        if isinstance(item, Mapping)
    ]
    failures = [
        item for item in (failure_payload or {}).get("failures", []) or []
        if isinstance(item, Mapping)
    ]
    grouped_failures = _failure_groups(failures)

    signals: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    for tender in tenders:
        current_project_id = _text(tender.get("project_id"))
        current_project_name = _text(tender.get("project_name"))
        current_title = _text(tender.get("title")) or ""
        current_date = _iso_date(tender.get("publication_date"))
        current_classification = classify_procurement_event(tender)
        if (
            not current_project_id
            or not current_project_name
            or current_date is None
            or current_classification.capability_key is None
        ):
            continue

        for (prior_project_id, prior_project_name, buyer_actor), group in grouped_failures.items():
            if prior_project_id == current_project_id:
                continue
            if prior_project_name != current_project_name:
                continue
            if buyer_actor not in current_title:
                rejected.append(
                    {
                        "current_project_id": current_project_id,
                        "prior_project_id": prior_project_id,
                        "reason": "BUYER_ACTOR_NOT_EXPLICIT_IN_CURRENT_TENDER_TITLE",
                    }
                )
                continue

            prior_dates = [_iso_date(item.get("publication_date")) for item in group]
            prior_dates = [item for item in prior_dates if item is not None]
            if not prior_dates:
                continue
            prior_date = max(prior_dates)
            days_after = (current_date - prior_date).days
            if days_after <= 0 or days_after > max_days_after_failure:
                continue

            failure_probe = {
                "project_name": prior_project_name,
                "title": _text(group[0].get("title")),
            }
            prior_classification = classify_procurement_event(failure_probe)
            if (
                prior_classification.capability_key is None
                or prior_classification.capability_key != current_classification.capability_key
            ):
                continue

            identity = (prior_project_id, current_project_id)
            if identity in seen:
                continue
            seen.add(identity)

            failed_packages = sorted(
                {
                    package
                    for package in (_text(item.get("package_name")) for item in group)
                    if package
                }
            )
            source_refs = _source_refs(tender, *group)
            signals.append(
                {
                    "signal_id": f"REBID::{prior_project_id}::{current_project_id}",
                    "change_type": "EXPLICIT_FAILED_PACKAGE_FOLLOWED_BY_SAME_PROGRAM_TENDER",
                    "evidence_state": "OBSERVED_SEQUENCE",
                    "capability_key": current_classification.capability_key,
                    "geography": geography,
                    "actor": buyer_actor,
                    "prior_project_id": prior_project_id,
                    "current_project_id": current_project_id,
                    "project_name": current_project_name,
                    "failed_packages": failed_packages,
                    "failed_package_count": len(failed_packages),
                    "failure_publication_date": prior_date.isoformat(),
                    "current_tender_publication_date": current_date.isoformat(),
                    "days_after_failure": days_after,
                    "current_budget_rmb": _text(tender.get("budget_rmb")),
                    "current_need_signal_id": (
                        f"LIVE_NEED::{_text(tender.get('source_id')) or 'XZ_GGZY'}::{current_project_id}"
                    ),
                    "package_mapping_state": "PROGRAM_LEVEL_ONLY_EXACT_PACKAGE_MAPPING_UNRESOLVED",
                    "source_refs": source_refs,
                }
            )

    signals.sort(
        key=lambda item: (
            int(item["days_after_failure"]),
            str(item["capability_key"]),
            str(item["current_project_id"]),
        )
    )
    return {
        "signal_kind": "PROCUREMENT_REBID_CHANGE_FRICTION",
        "geography": geography,
        "max_days_after_failure": max_days_after_failure,
        "tender_count": len(tenders),
        "failed_package_evidence_count": len(failures),
        "signal_count": len(signals),
        "signals": signals,
        "rejected": rejected,
        "truth_notes": [
            "A rebid signal proves an observed program-level sequence: explicit failed package followed by a later same-name, same-buyer, same-capability tender.",
            "Program-level rebid evidence does not prove exact old-package to new-package mapping.",
            "Rebid evidence is CHANGE/FRICTION evidence only; it is not PAID need, payer identity, provider underuse, or transaction success.",
            "Exact project-name equality and explicit buyer-title identity are required; fuzzy title or LLM similarity is forbidden.",
        ],
    }
