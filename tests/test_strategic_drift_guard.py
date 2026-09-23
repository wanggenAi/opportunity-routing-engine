import json
from pathlib import Path

from src.strategic_drift_guard import (
    ENFORCEMENT_START_SCAN,
    STATE_CHANGE_ENFORCEMENT_START_SCAN,
    strategic_drift_errors,
    strategic_drift_guard_passes,
)


ROOT = Path(__file__).resolve().parents[1]


def evidenced(ref: str):
    return {"state": "EVIDENCED", "evidence_refs": [ref]}


def compliant_scan(scan_id: str = "ATTRACTION_SCAN_142"):
    return {
        "scan_id": scan_id,
        "drift_audit": {
            "regenerative_field_revalidated": True,
            "explicit_transaction_seed_not_ontology": True,
            "next_search_boundary_rederived_from_broad_reality": True,
        },
        "high_attraction_beacons": [
            {
                "formation_id": f"{scan_id}-F1",
                "regenerative_field_gate": {
                    "seed_kind": "BROAD_REALITY_PATTERN",
                    "actor_a_replenishment": evidenced("A-POP"),
                    "actor_b_replenishment": evidenced("B-POP"),
                    "recurring_connection_pressure": evidenced("PRESSURE"),
                    "recurring_missing_edge": evidenced("EDGE"),
                    "recurring_event_source": evidenced("EVENT"),
                    "independent_field_evidence_refs": ["FIELD-1"],
                },
            }
        ],
    }


def test_compliant_regenerative_scan_passes():
    scan = compliant_scan()
    assert strategic_drift_guard_passes(scan)
    assert strategic_drift_errors(scan) == []


def test_single_asset_listing_cannot_define_high_attraction_without_independent_field():
    scan = compliant_scan()
    gate = scan["high_attraction_beacons"][0]["regenerative_field_gate"]
    gate["seed_kind"] = "ASSET_LISTING"
    gate["independent_field_evidence_refs"] = []

    errors = strategic_drift_errors(scan)
    assert any(
        "explicit_transaction_seed_without_independent_field_evidence" in error
        for error in errors
    )


def test_missing_recurring_missing_edge_fails_closed():
    scan = compliant_scan()
    gate = scan["high_attraction_beacons"][0]["regenerative_field_gate"]
    gate["recurring_missing_edge"] = {
        "state": "UNKNOWN",
        "evidence_refs": [],
    }

    errors = strategic_drift_errors(scan)
    assert any("dimension_not_evidenced:recurring_missing_edge" in error for error in errors)
    assert any("missing_evidence_refs:recurring_missing_edge" in error for error in errors)


def test_scan140_style_asset_lane_would_fail_if_repeated_after_enforcement_boundary():
    legacy = json.loads(
        (ROOT / "data/research_runs/attraction_scan_140.json").read_text(encoding="utf-8")
    )
    legacy["scan_id"] = f"ATTRACTION_SCAN_{ENFORCEMENT_START_SCAN:03d}"

    errors = strategic_drift_errors(legacy)
    assert "drift_audit_not_true:regenerative_field_revalidated" in errors
    assert any("missing_regenerative_field_gate" in error for error in errors)



def state_change_gate(owner_state: str = "UNOWNED_OPEN"):
    return {
        "event_trace": evidenced("EVENT-TRACE"),
        "affected_actor_population": evidenced("AFFECTED-ACTORS"),
        "counterparty_population": evidenced("COUNTERPARTIES"),
        "decisive_action_gate": {
            **evidenced("ACTION-GATE"),
            "owner_state": owner_state,
        },
    }


def scan157_compliant(owner_state: str = "UNOWNED_OPEN"):
    scan = compliant_scan(f"ATTRACTION_SCAN_{STATE_CHANGE_ENFORCEMENT_START_SCAN}")
    scan["drift_audit"].update(
        {
            "prior_domain_deduplication_checked": True,
            "state_change_first_search": True,
            "decisive_action_gate_owner_checked": True,
        }
    )
    scan["high_attraction_beacons"][0]["state_change_gate"] = state_change_gate(
        owner_state
    )
    return scan


def test_scan157_requires_state_change_search_audit_flags():
    scan = compliant_scan(f"ATTRACTION_SCAN_{STATE_CHANGE_ENFORCEMENT_START_SCAN}")
    errors = strategic_drift_errors(scan)
    assert "drift_audit_not_true:prior_domain_deduplication_checked" in errors
    assert "drift_audit_not_true:state_change_first_search" in errors
    assert "drift_audit_not_true:decisive_action_gate_owner_checked" in errors


def test_scan157_high_attraction_rejects_incumbent_owned_decisive_gate():
    scan = scan157_compliant("INCUMBENT_OWNED")
    errors = strategic_drift_errors(scan)
    assert any(
        "decisive_action_gate_not_operator_ownable:INCUMBENT_OWNED" in error
        for error in errors
    )


def test_scan157_high_attraction_accepts_evidenced_unowned_open_gate():
    scan = scan157_compliant("UNOWNED_OPEN")
    assert strategic_drift_errors(scan) == []


def test_every_future_persisted_scan_is_strategically_guarded():
    for path in sorted((ROOT / "data/research_runs").glob("attraction_scan_*.json")):
        suffix = path.stem.removeprefix("attraction_scan_")
        if not suffix.isdigit() or int(suffix) < ENFORCEMENT_START_SCAN:
            continue
        scan = json.loads(path.read_text(encoding="utf-8"))
        assert strategic_drift_errors(scan) == [], (
            f"{path.name} violates strategic anti-drift guard: "
            f"{strategic_drift_errors(scan)}"
        )
