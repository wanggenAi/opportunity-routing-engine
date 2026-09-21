import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCAN=ROOT/"data"/"research_runs"/"attraction_scan_056.json"
STATE=ROOT/"data"/"commercial_reset_state.json"
def load(p): return json.loads(p.read_text())
def test_scan056_closes_six_external_trigger_loops():
    s=load(SCAN)
    assert s["scan_id"]=="ATTRACTION_SCAN_056"
    assert s["status"]=="COMPLETE"
    assert s["active_commercial_candidate_promotions"]==[]
    assert s["retained_research_formations"]==[]
    assert len(s["examined_formations"])==6
    assert all(x["verdict"].startswith("DEMOTED_") for x in s["examined_formations"])
def test_scan056_external_signals_are_already_integrated_by_vertical_controls():
    s=load(SCAN)
    v={x["formation_id"]:x["verdict"] for x in s["examined_formations"]}
    assert "FX_TO_PRICE_AUTOMATION" in v["ATTRACTION_SCAN_056-F1"]
    assert "WEATHER_TO_AD_ACTION_AUTOMATION" in v["ATTRACTION_SCAN_056-F2"]
    assert "INDEX_DRIVEN_ENTERPRISE_PRICING" in v["ATTRACTION_SCAN_056-F3"]
    assert "COMPETITOR_SIGNAL_REPRICING" in v["ATTRACTION_SCAN_056-F4"]
    assert "DYNAMIC_TARIFF_CHARGING" in v["ATTRACTION_SCAN_056-F5"]
    assert "EVENT_INTELLIGENCE_TO_PARKING_PRICING" in v["ATTRACTION_SCAN_056-F6"]
def test_scan056_advances_to_noncommoditized_external_trigger_boundary():
    s=load(SCAN)
    assert s["next_scan_id"]=="ATTRACTION_SCAN_057"
    b=s["next_search_boundary"]
    assert "EXTERNAL_TRIGGER_NOT_ALREADY_COMMODITIZED_BY_ACTION_CATEGORY" in b
    assert "MACHINE_VERIFIABLE_TRIGGER" in b
    assert "REUSABLE_CROSS_CUSTOMER_MAPPING" in b
    assert "NO_RECURRING_EXPERT_INTERPRETATION" in b
def test_state_advances_after_scan056():
    st=load(STATE)
    assert st["last_completed_scan_id"]=="ATTRACTION_SCAN_056"
    assert st["next_scan_id"]=="ATTRACTION_SCAN_057"
    assert st["active_commercial_candidates"]==[]
    assert st["first_external_value_flow"]=="NOT_PROVEN"
    assert {x["formation_id"] for x in st["retained_research_formations"]}=={"ATTRACTION_SCAN_015-F1"}
