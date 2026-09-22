import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_093.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan093_resets_to_broad_current_reality_not_paid_stack_ontology():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_093"
    assert scan["status"] == "COMPLETE"
    assert scan["discovery_source_reset"] is True
    assert scan["inherited_mechanism_as_requirement"] is False
    assert "BROAD_CURRENT_REALITY_SOURCE_RESET" in scan["search_mode"]
    assert "WITHOUT_STARTING_FROM_EXISTING_PAID_PRODUCTS" in scan["search_mode"]
    assert "NO_JOB_GIG_RFQ_OR_PROCUREMENT_FEED_AS_DISCOVERY_ONTOLOGY" in scan["search_mode"]


def test_scan093_is_formation_diverse_and_promotes_nothing():
    scan = load(SCAN)
    assert len(scan["examined_formations"]) == 3
    titles = {f["title"] for f in scan["examined_formations"]}
    assert any("TLS_CERTIFICATE" in title for title in titles)
    assert any("A2L_HVAC" in title for title in titles)
    assert any("ECOMMERCE_ACCESSIBILITY" in title for title in titles)
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    assert scan["high_attraction_beacons"] == []


def test_scan093_binds_state_change_endowment_contradiction_before_control_preflight():
    scan = load(SCAN)
    for formation in scan["examined_formations"]:
        assert formation["observed_actor_state_change_evidence"]
        assert formation["objective_endowment_or_underuse_evidence"]
        assert formation["observed_behavior_or_workaround_evidence"]
        assert formation["contradiction_or_partial_flow_evidence"]
        assert formation["exact_incumbent_and_control_surface_preflight"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan093_preserves_hard_operator_and_execution_floors():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    tls = formations["ATTRACTION_SCAN_093-F1"]
    hvac = formations["ATTRACTION_SCAN_093-F2"]
    eaa = formations["ATTRACTION_SCAN_093-F3"]
    assert tls["machine_delegatability_check"].startswith("PASS_")
    assert "MATURE_CLM" in tls["normalized_margin_check"]
    assert hvac["machine_delegatability_check"].startswith("PARTIAL_")
    assert "PHYSICAL" in hvac["founder_independence_check"]
    assert eaa["machine_delegatability_check"].startswith("PARTIAL_")
    assert "HUMAN" in eaa["founder_independence_check"]


def test_scan093_requires_second_independent_broad_reality_pass_before_new_signal():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_094"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT_BROAD_CURRENT_REALITY_SOURCE_RESET" in boundary
    assert "EXCLUDE_SCAN060_TO_093_FORMATIONS_AND_PRIMARY_SIGNALS" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert scan["drift_audit"]["response"].startswith(
        "RUN_ONE_SECOND_INDEPENDENT_BROAD_CURRENT_REALITY"
    )


def test_scan093_updates_reset_state_without_commercial_promotion():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_093"
    assert state["last_resolved_formation_id"] == "ATTRACTION_SCAN_093-F3"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_094"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_094"
    assert (
        state["parallel_workstreams"]["discovery"]["search_boundary"]
        == scan["next_search_boundary"]
    )
