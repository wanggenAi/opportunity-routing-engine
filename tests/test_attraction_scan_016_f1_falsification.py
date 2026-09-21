import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "research_runs" / "attraction_scan_016_f1_falsification.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan016_f1_is_demoted_fail_closed():
    result=load(RESULT)
    assert result["formation_id"]=="ATTRACTION_SCAN_016-F1"
    assert result["verdict"]=="DEMOTED_UNPROVEN_TWO_RAIL_9610_CALLABILITY_AND_PLATFORM_OWNED_VALUE_LAYER"
    assert result["commercial_candidate"] is False
    assert result["retain_for_active_validation"] is False
    assert result["first_external_value_flow"]=="NOT_PROVEN"

def test_physical_availability_does_not_satisfy_callable_rail_gate():
    result=load(RESULT)
    proven={x["gate"]:x["status"] for x in result["proven"]}
    kills={x["kill"]:x["status"] for x in result["decisive_kills"]}
    assert proven["LEGAL_AND_PHYSICAL_CHOICE_SET"]=="PASS"
    assert proven["GENERIC_REVERSE_LOGISTICS_API_EXISTENCE"]=="PASS"
    assert kills["TWO_INDEPENDENT_THIRD_PARTY_CALLABLE_9610_RAILS"]=="NOT_PROVEN_NONCOMPENSATORY_FAIL"
    assert kills["NON_CONSULTING_OPERATOR_ECONOMICS"]=="NOT_PROVEN_NONCOMPENSATORY_FAIL"

def test_state_removes_scan016_from_active_validation():
    state=load(STATE)
    retained={x["formation_id"] for x in state["retained_research_formations"]}
    resolved={x["formation_id"]:x["verdict"] for x in state["resolved_research_formations"]}
    active_validation={x["formation_id"] for x in state["parallel_workstreams"]["validation"]}
    assert retained=={"ATTRACTION_SCAN_015-F1"}
    assert "ATTRACTION_SCAN_016-F1" not in active_validation
    assert resolved["ATTRACTION_SCAN_016-F1"]=="DEMOTED_UNPROVEN_TWO_RAIL_9610_CALLABILITY_AND_PLATFORM_OWNED_VALUE_LAYER"
    assert state["active_commercial_candidates"]==[]
    assert state["first_external_value_flow"]=="NOT_PROVEN"
    assert state["next_scan_id"]=="ATTRACTION_SCAN_032"
