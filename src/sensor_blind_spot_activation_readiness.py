"""Fail-closed activation readiness for evidence-channel blind spots.

This layer answers a narrower question than sensor discovery or source liveness:
can a currently non-observed source legitimately enter an automated producer trial
*now*? Accessibility, public visibility, registration, or an official API surface do
not by themselves grant automation permission.

The model consumes the latest sensor evidence-channel coverage artifact so it only
assesses channels that are still blind in the current production state. It never
activates a source, changes a registry, buys access, reverse engineers endpoints, or
promotes evidence into commercial truth.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from typing import Any

from src.sensor_portfolio import OperationalSource
from src.sensor_registry import SensorCandidate, assess_sensor_candidate


SCHEMA_VERSION = "sensor-blind-spot-activation-readiness.v1"

_EXPLICIT_AUTOMATION_TOKENS = {
    "BOUNDED_PUBLIC_FETCH",
    "PUBLIC_ENDPOINT",
    "FREE_PUBLIC_ENDPOINT",
    "PUBLIC_JSON_API",
}


def _tokens(value: str) -> set[str]:
    return {part.strip().upper() for part in value.split(";") if part.strip()}


def _operational_readiness(source: OperationalSource) -> dict[str, Any]:
    access = source.access_mode.strip().upper()
    status = source.status.strip().upper()
    rules = _tokens(source.automation_allowed)
    blockers: list[str] = []
    constraints: list[str] = []

    if source.is_production_live:
        state = "ALREADY_PRODUCTION"
        producer_trial_allowed = False
        blockers.append("ALREADY_PRODUCTION_NOT_A_BLIND_SPOT_TRIAL")
    else:
        if source.is_disabled_or_retired or "DISABLED" in status:
            blockers.append("SOURCE_DISABLED_OR_RETIRED")
        if source.is_manual_surface or "MANUAL" in access or "LOGIN_MANUAL" in access:
            blockers.append("MANUAL_OR_LOGIN_BOUND_ACCESS")
        if source.automation_allowed.strip().upper() == "UNKNOWN":
            blockers.append("AUTOMATION_PERMISSION_UNKNOWN")
        if "TERMS_DEPENDENT" in rules:
            blockers.append("TERMS_REVIEW_REQUIRED")
        if "REVIEW_REQUIRED" in status:
            blockers.append("ACTIVATION_REVIEW_REQUIRED")
        if "PAID" in status or "DO_NOT_PURCHASE_PLAN" in rules:
            blockers.append("PAID_PATH_DISABLED")
        if "NO_REVERSE_ENGINEERED_ENDPOINTS" in rules:
            constraints.append("REVERSE_ENGINEERED_ENDPOINTS_FORBIDDEN")
        if "NO_PRIVATE_API" in rules:
            constraints.append("PRIVATE_API_FORBIDDEN")
        if "NO_PAID_DATA" in rules or "NO_PAID_CREDITS" in rules:
            constraints.append("PAID_DATA_OR_CREDITS_FORBIDDEN")
        if "ONLY_IF_OFFICIAL_SCOPE_HAS_ZERO_INCREMENTAL_USAGE_FEE" in rules:
            blockers.append("ZERO_INCREMENTAL_FEE_SCOPE_NOT_PROVEN")
        authorized_surface = any(token in access for token in ("AUTHORIZED", "OAUTH", "OPENAPI"))
        if authorized_surface:
            blockers.append("AUTHORIZED_SCOPE_NOT_PROVEN_FOR_PRODUCER")

        explicit_automation = bool(rules & _EXPLICIT_AUTOMATION_TOKENS)
        producer_trial_allowed = explicit_automation and not blockers
        if producer_trial_allowed:
            state = "PRODUCER_TRIAL_READY"
        elif authorized_surface and not source.is_disabled_or_retired:
            state = "PERMISSION_VALIDATION_CANDIDATE"
        elif source.is_manual_surface:
            state = "MANUAL_ONLY_BLOCKED"
        elif source.is_disabled_or_retired:
            state = "DISABLED"
        else:
            state = "NOT_READY"

    return {
        "source_id": source.source_id,
        "source_kind": "OPERATIONAL",
        "name": source.name,
        "registry_status": source.status,
        "access_mode": source.access_mode,
        "automation_allowed": source.automation_allowed,
        "readiness_state": state,
        "producer_trial_allowed": producer_trial_allowed,
        "blockers": sorted(set(blockers)),
        "constraints": sorted(set(constraints)),
        "permission_validation_candidate": state == "PERMISSION_VALIDATION_CANDIDATE",
    }


def _candidate_readiness(candidate: SensorCandidate) -> dict[str, Any]:
    assessment = assess_sensor_candidate(candidate)
    blockers = sorted(
        set(assessment["qualification_blockers"]) | set(assessment["activation_blockers"])
    )
    ready = bool(assessment["automation_ready"])
    return {
        "source_id": candidate.source_id,
        "source_kind": "CANDIDATE",
        "name": candidate.name,
        "lifecycle_state": candidate.lifecycle_state,
        "collection_mode": candidate.collection_mode,
        "effective_state": assessment["effective_state"],
        "china_relevant": assessment["china_relevant"],
        "producer_trial_allowed": ready,
        "readiness_state": "PRODUCER_TRIAL_READY" if ready else "DISCOVERY_OR_QUALIFICATION_BLOCKED",
        "blockers": blockers,
        "constraints": [],
        "permission_validation_candidate": False,
    }


def reconcile_blind_spot_activation_readiness(
    operational_sources: Iterable[OperationalSource],
    candidates: Iterable[SensorCandidate],
    evidence_channel_coverage: Mapping[str, Any],
) -> dict[str, Any]:
    """Assess only the latest production evidence-channel blind spots.

    A source is producer-trial-ready only when the current registry/candidate contract
    explicitly supports automation and no blocker remains. We do not infer permission
    from a public page or from the existence of an official developer portal.
    """

    if evidence_channel_coverage.get("schema_version") != "sensor-evidence-channel-coverage.v1":
        raise ValueError("unsupported evidence channel coverage schema")

    channel_rows = evidence_channel_coverage.get("channels")
    if not isinstance(channel_rows, list):
        raise ValueError("evidence channel coverage channels must be a list")
    declared_blind = evidence_channel_coverage.get("blind_spot_channel_ids")
    if not isinstance(declared_blind, list) or not all(isinstance(x, str) for x in declared_blind):
        raise ValueError("blind_spot_channel_ids must be a list of strings")
    blind_ids = set(declared_blind)
    actual_blind = {
        row.get("channel_id")
        for row in channel_rows
        if isinstance(row, Mapping) and row.get("blind_spot") is True
    }
    if blind_ids != actual_blind:
        raise ValueError("blind spot summary diverges from channel rows")

    operational = tuple(operational_sources)
    candidate_items = tuple(candidates)
    op_by_id = {item.source_id: item for item in operational}
    cand_by_id = {item.source_id: item for item in candidate_items}
    if len(op_by_id) != len(operational) or len(cand_by_id) != len(candidate_items):
        raise ValueError("duplicate source ids in registries")

    channels: list[dict[str, Any]] = []
    all_ready: set[str] = set()
    all_permission_validation: set[str] = set()
    blocker_counts: Counter[str] = Counter()

    for row in sorted(
        (x for x in channel_rows if isinstance(x, Mapping) and x.get("channel_id") in blind_ids),
        key=lambda x: str(x.get("channel_id")),
    ):
        channel_id = str(row.get("channel_id"))
        op_ids = row.get("registered_operational_source_ids", [])
        cand_ids = row.get("candidate_source_ids", [])
        if not isinstance(op_ids, list) or not isinstance(cand_ids, list):
            raise ValueError(f"invalid source lists for blind channel {channel_id}")
        unknown_op = sorted(set(op_ids) - set(op_by_id))
        unknown_cand = sorted(set(cand_ids) - set(cand_by_id))
        if unknown_op or unknown_cand:
            raise ValueError(f"blind channel {channel_id} references unknown sources")

        assessments = [_operational_readiness(op_by_id[source_id]) for source_id in op_ids]
        assessments.extend(_candidate_readiness(cand_by_id[source_id]) for source_id in cand_ids)
        ready = sorted(item["source_id"] for item in assessments if item["producer_trial_allowed"])
        permission_validation = sorted(
            item["source_id"] for item in assessments if item["permission_validation_candidate"]
        )
        all_ready.update(ready)
        all_permission_validation.update(permission_validation)
        for item in assessments:
            blocker_counts.update(item["blockers"])

        if ready:
            state = "PRODUCER_TRIAL_READY"
        elif permission_validation:
            state = "PERMISSION_VALIDATION_REQUIRED"
        else:
            state = "NO_SAFE_AUTOMATED_PATH_CURRENTLY_PROVEN"

        channels.append(
            {
                "channel_id": channel_id,
                "readiness_state": state,
                "producer_trial_ready_source_ids": ready,
                "permission_validation_candidate_source_ids": permission_validation,
                "source_assessments": sorted(assessments, key=lambda x: (x["source_kind"], x["source_id"])),
            }
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "blind_spot_channel_count": len(channels),
        "blind_spot_channel_ids": sorted(blind_ids),
        "producer_trial_ready_source_count": len(all_ready),
        "producer_trial_ready_source_ids": sorted(all_ready),
        "permission_validation_candidate_count": len(all_permission_validation),
        "permission_validation_candidate_source_ids": sorted(all_permission_validation),
        "safe_activation_conclusion": (
            "PRODUCER_TRIAL_AVAILABLE" if all_ready else "NO_SAFE_AUTOMATED_PRODUCER_TRIAL_CURRENTLY_PROVEN"
        ),
        "blocker_counts": dict(sorted(blocker_counts.items())),
        "channels": channels,
        "upstream_evidence_channel_state": {
            "channel_count": evidence_channel_coverage.get("channel_count"),
            "observed_channel_count": evidence_channel_coverage.get("observed_channel_count"),
            "blind_spot_channel_count": evidence_channel_coverage.get("blind_spot_channel_count"),
            "observed_channel_ids": evidence_channel_coverage.get("observed_channel_ids"),
        },
        "truth_boundaries": [
            "PUBLIC_ACCESS_NE_AUTOMATION_PERMISSION",
            "OFFICIAL_API_SURFACE_NE_AUTHORIZED_SCOPE",
            "MANUAL_VISIBILITY_NE_PRODUCTION_SENSOR",
            "TERMS_REVIEW_REQUIRED_NE_PERMISSION_GRANTED",
            "CANDIDATE_DISCOVERY_NE_PRODUCER_READINESS",
            "GLOBAL_SOURCE_NE_CHINA_PRIMARY_EVIDENCE",
            "ZERO_INCREMENTAL_FEE_NOT_PROVEN_NE_FREE_TO_RUN",
            "NO_REVERSE_ENGINEERED_ENDPOINTS",
            "NO_PAID_DATA_OR_CREDITS",
            "READINESS_NE_SOURCE_ACTIVATION",
            "UNKNOWN_NE_PASS",
        ],
    }


GOVERNING_INVARIANTS = (
    "ASSESS_ONLY_CURRENT_BLIND_CHANNELS",
    "AUTOMATION_PERMISSION_MUST_BE_EXPLICIT",
    "OFFICIAL_DEVELOPER_SURFACE_NE_GRANTED_SCOPE",
    "MANUAL_SOURCE_NE_AUTOMATED_SENSOR",
    "BLOCKED_SOURCE_MUST_REMAIN_VISIBLE",
    "PRODUCER_TRIAL_READY_NE_PRODUCTION_LIVE",
    "UNKNOWN_NE_PASS",
)
