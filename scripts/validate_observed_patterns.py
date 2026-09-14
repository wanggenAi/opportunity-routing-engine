#!/usr/bin/env python3
"""Fail-closed validator for production ObservedPattern artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.observation_store import SQLiteObservationStore
from src.observed_patterns import (
    BUSINESS_PROMOTION,
    ORDERING_BASIS,
    PATTERN_SCHEMA_VERSION,
    PATTERN_STATES,
    RESEARCH_SCOPE_STATES,
)


FORBIDDEN_PATTERN_KEYS = {
    "commercial_score",
    "opportunity_score",
    "payer",
    "paid_need",
    "payment_confirmed",
    "availability_confirmed",
    "permission_allowed",
    "route_testable",
    "opportunity_confirmed",
    "regenerative_loop_confirmed",
}


def _load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", type=Path, required=True)
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--expected-source-run-id", type=int)
    args = parser.parse_args()

    data = _load(args.patterns)
    if data.get("schema_version") != PATTERN_SCHEMA_VERSION:
        raise SystemExit("unexpected observed-pattern schema version")
    if data.get("ordering_basis") != ORDERING_BASIS:
        raise SystemExit("pattern ordering drifted into non-evidence ranking")
    if data.get("business_promotion") != BUSINESS_PROMOTION:
        raise SystemExit("pattern artifact attempted business promotion")
    if data.get("pattern_gate_semantics") != "OPERATIONAL_EVIDENCE_THRESHOLD_NOT_COMMERCIAL_TRUTH":
        raise SystemExit("pattern gate semantics are missing or drifted")
    if args.expected_source_run_id is not None and data.get("source_observation_run_id") != args.expected_source_run_id:
        raise SystemExit("pattern artifact does not point to the requested Observation Fabric run")

    scope_state = data.get("research_scope_state")
    if scope_state not in RESEARCH_SCOPE_STATES:
        raise SystemExit("pattern artifact lacks a valid research scope state")
    expected_authorization = scope_state == "BROAD_DISCOVERY_READY"
    if data.get("broad_discovery_use_authorized") is not expected_authorization:
        raise SystemExit("pattern broad-discovery authorization drifted from scope state")

    if args.coverage is None:
        if scope_state != "CALIBRATION_ONLY":
            raise SystemExit("pattern run without research coverage evidence must remain CALIBRATION_ONLY")
    else:
        coverage = _load(args.coverage)
        if coverage.get("state") != scope_state:
            raise SystemExit("pattern scope state diverges from research coverage artifact")
        if coverage.get("broad_discovery_use_authorized") is not expected_authorization:
            raise SystemExit("research coverage authorization mismatch")

    with SQLiteObservationStore(args.store) as store:
        current = tuple(store.iter_current())

    if data.get("input_current_observation_count") != len(current):
        raise SystemExit("pattern artifact input count diverges from current Observation Fabric state")

    current_observations = {
        f"{envelope.source_id}::{envelope.observation_id}": envelope
        for envelope in current
    }
    current_claims = {
        f"{envelope.source_id}::{envelope.observation_id}::{claim.claim_id}": claim
        for envelope in current
        for claim in envelope.claims
    }

    patterns = data.get("patterns")
    if not isinstance(patterns, list):
        raise SystemExit("patterns must be an array")
    if data.get("pattern_count") != len(patterns):
        raise SystemExit("pattern_count does not match patterns array")

    observed_count = 0
    unbound_count = 0
    pattern_ids: set[str] = set()
    exact_keys: set[tuple[str, str, str]] = set()
    gate = data.get("pattern_gate", {})
    for required in ("min_observations", "min_actors", "min_periods", "min_sources"):
        value = gate.get(required)
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise SystemExit(f"invalid pattern gate: {required}")

    for item in patterns:
        if not isinstance(item, dict):
            raise SystemExit("pattern record must be an object")
        forbidden = FORBIDDEN_PATTERN_KEYS & set(item)
        if forbidden:
            raise SystemExit(f"downstream commercial truth leaked into pattern record: {sorted(forbidden)}")
        if item.get("schema_version") != PATTERN_SCHEMA_VERSION:
            raise SystemExit("pattern record schema version drifted")
        if item.get("business_promotion") != BUSINESS_PROMOTION:
            raise SystemExit("individual pattern attempted business promotion")
        state = item.get("state")
        if state not in PATTERN_STATES:
            raise SystemExit(f"unsupported pattern state: {state}")

        pattern_id = item.get("pattern_id")
        if not isinstance(pattern_id, str) or not pattern_id or pattern_id in pattern_ids:
            raise SystemExit("pattern_id is missing or duplicated")
        pattern_ids.add(pattern_id)
        exact_key = (item.get("primitive"), item.get("concept"), item.get("geography"))
        if any(not isinstance(part, str) or not part for part in exact_key) or exact_key in exact_keys:
            raise SystemExit("exact pattern key is invalid or duplicated")
        exact_keys.add(exact_key)

        observation_refs = item.get("supporting_observation_refs")
        claim_refs = item.get("supporting_claim_refs")
        actor_ids = item.get("supporting_actor_ids")
        source_ids = item.get("supporting_source_ids")
        periods = item.get("supporting_periods")
        for name, value in (
            ("supporting_observation_refs", observation_refs),
            ("supporting_claim_refs", claim_refs),
            ("supporting_actor_ids", actor_ids),
            ("supporting_source_ids", source_ids),
            ("supporting_periods", periods),
        ):
            if not isinstance(value, list) or len(value) != len(set(value)):
                raise SystemExit(f"{name} must be a unique array")

        if item.get("observation_count") != len(observation_refs):
            raise SystemExit("observation_count does not match support identities")
        if item.get("actor_count") != len(actor_ids):
            raise SystemExit("actor_count does not match support actors")
        if item.get("source_count") != len(source_ids):
            raise SystemExit("source_count does not match support sources")
        if item.get("period_count") != len(periods):
            raise SystemExit("period_count does not match support periods")
        if set(observation_refs) - set(current_observations):
            raise SystemExit("pattern references non-current observation identity")
        if set(claim_refs) - set(current_claims):
            raise SystemExit("pattern references non-current semantic claim")
        if any(current_claims[ref].epistemic_status != "OBSERVED" for ref in claim_refs):
            raise SystemExit("non-OBSERVED claim entered pattern support")

        missing = item.get("missing_pattern_evidence")
        if not isinstance(missing, list):
            raise SystemExit("missing_pattern_evidence must be an array")
        if state == "OBSERVED_PATTERN":
            observed_count += 1
            if missing:
                raise SystemExit("OBSERVED_PATTERN still has missing gate evidence")
            if item["observation_count"] < gate["min_observations"]:
                raise SystemExit("OBSERVED_PATTERN lacks recurrence count")
            if item["actor_count"] < gate["min_actors"]:
                raise SystemExit("OBSERVED_PATTERN lacks actor diversity")
            if item["period_count"] < gate["min_periods"]:
                raise SystemExit("OBSERVED_PATTERN lacks time persistence")
            if item["source_count"] < gate["min_sources"]:
                raise SystemExit("OBSERVED_PATTERN lacks required source diversity")
        else:
            unbound_count += 1
            if not missing:
                raise SystemExit("UNBOUND pattern must identify missing evidence")

        downstream_unknowns = item.get("downstream_unknowns")
        required_unknowns = {
            "LATENT_VALUE_NOT_ESTABLISHED",
            "COMPLEMENTARY_ACTOR_NOT_ESTABLISHED",
            "TRANSFORMATION_MECHANISM_NOT_ESTABLISHED",
            "REGENERATING_EVENT_FLOW_NOT_ESTABLISHED",
            "PAYER_NOT_ESTABLISHED",
            "REPEAT_MONETIZATION_NOT_ESTABLISHED",
            "COMPOUNDING_NOT_ESTABLISHED",
        }
        if not isinstance(downstream_unknowns, list) or not required_unknowns.issubset(downstream_unknowns):
            raise SystemExit("pattern record lost downstream unknown boundaries")

    if data.get("observed_pattern_count") != observed_count:
        raise SystemExit("observed_pattern_count mismatch")
    if data.get("unbound_pattern_count") != unbound_count:
        raise SystemExit("unbound_pattern_count mismatch")

    print(json.dumps({
        "validated": True,
        "research_scope_state": scope_state,
        "broad_discovery_use_authorized": expected_authorization,
        "input_current_observation_count": len(current),
        "pattern_count": len(patterns),
        "observed_pattern_count": observed_count,
        "unbound_pattern_count": unbound_count,
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
