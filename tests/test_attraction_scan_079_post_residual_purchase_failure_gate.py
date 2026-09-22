import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_079.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text())


def test_scan079_requires_paid_layer_then_buyer_authored_post_purchase_failure_without_mechanism_inheritance():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_079"
    assert scan["status"] == "COMPLETE"
    assert scan["inherited_mechanism_as_requirement"] is False
    assert len(scan["examined_formations"]) == 3
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == []
    for formation in scan["examined_formations"]:
        assert formation["evidence_summary"]
        assert formation["buyer_authored_post_live_or_platform_residual_evidence"]
        assert formation["actual_non_incumbent_recurring_payment_evidence"]
        assert formation["buyer_authored_post_residual_purchase_failure_evidence"]
        assert formation["pre_residual_same_outcome_causal_chain"]
        assert formation["post_residual_same_outcome_causal_chain"]
        assert formation["non_incumbent_residual_provider_preflight"]
        assert formation["exact_incumbent_preflight"]
        assert formation["founder_independence_check"]
        assert formation["data_action_rights_check"]
        assert formation["normalized_margin_check"]
        assert formation["machine_delegatability_check"]
        assert formation["generic_agent_substitutability_check"]
        assert formation["verdict"].startswith("DEMOTED_")


def test_scan079_contains_one_strong_post_purchase_failure_and_one_negative_control():
    scan = load(SCAN)
    formations = {f["formation_id"]: f for f in scan["examined_formations"]}
    assert formations["ATTRACTION_SCAN_079-F1"]["post_residual_same_outcome_causal_chain"].startswith("PASS_STRONG_")
    assert formations["ATTRACTION_SCAN_079-F2"]["post_residual_same_outcome_causal_chain"].startswith("PARTIAL_PASS_")
    assert formations["ATTRACTION_SCAN_079-F3"]["post_residual_same_outcome_causal_chain"].startswith("FAIL_")
    learnings = " ".join(scan["scan_learnings"])
    assert "POST_RESIDUAL_PURCHASE_FAILURE_EVIDENCE_IS_DISCOVERABLE" in learnings
    assert "SCAN079_ZERO_RETENTION" in learnings


def test_scan079_enforces_no_repeat_and_does_not_inherit_old_primary_signals():
    scan = load(SCAN)
    excluded = {item["observation"]: item["excluded_reason"] for item in scan["excluded_observations"]}
    assert "RICHMOND_POLICE_VERITONE_REDACT_POST_PURCHASE_CAPACITY_FAILURE" in excluded
    assert "ASPEN_AUDIOEYE_POST_DEPLOYMENT_ACCESSIBILITY_RESIDUAL" in excluded
    assert all("EXCLUDE_NO_REPEAT" in reason for reason in excluded.values())


def test_scan079_runs_second_independent_pass_before_deriving_provider_switch_or_router_ontology():
    scan = load(SCAN)
    assert scan["next_scan_id"] == "ATTRACTION_SCAN_080"
    boundary = scan["next_search_boundary"]
    assert "SECOND_INDEPENDENT" in boundary
    assert "POST_RESIDUAL_PURCHASE_EVIDENCE" in boundary
    assert "NO_MECHANISM_INHERITANCE" in boundary
    assert "ROUTER" not in boundary
    assert "PROVIDER_SWITCH" not in boundary
    assert "MULTI_PROVIDER" not in boundary


def test_scan079_updates_reset_state_without_promoting_commercial_candidate():
    scan = load(SCAN)
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_079"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_080"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    assert state["parallel_workstreams"]["discovery"]["next_scan_id"] == "ATTRACTION_SCAN_080"
    assert state["parallel_workstreams"]["discovery"]["search_boundary"] == scan["next_search_boundary"]
