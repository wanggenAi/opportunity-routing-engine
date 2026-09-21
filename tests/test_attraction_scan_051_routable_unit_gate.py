import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_051.json"
STATE = ROOT / "data" / "commercial_reset_state.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_scan051_retains_exactly_one_research_beacon_without_promotion():
    scan = load(SCAN)
    assert scan["scan_id"] == "ATTRACTION_SCAN_051"
    assert len(scan["examined_formations"]) == 6
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_051-F1"]
    assert len(scan["high_attraction_beacons"]) == 1
    assert scan["first_external_value_flow"] == "NOT_PROVEN"

def test_scan051_f1_has_routable_accepted_audio_unit_and_required_unknowns():
    scan = load(SCAN)
    f1 = scan["high_attraction_beacons"][0]
    assert f1["formation_id"] == "ATTRACTION_SCAN_051-F1"
    assert f1["acceptance_unit"] == "QA_APPROVED_AUDIO_HOUR_OR_BATCH"
    assert "NATIVE_LANGUAGE_ANNOTATOR" in f1["replaceable_execution_unit"]
    unknowns = " ".join(f1["primary_unknowns"])
    for token in ["DEMAND", "SUPPLY", "QA", "MARGIN", "CONFIDENTIALITY", "MANAGED_SERVICES"]:
        assert token in unknowns

def test_scan051_does_not_promote_on_incumbent_leakage_alone():
    scan = load(SCAN)
    f1 = scan["high_attraction_beacons"][0]
    assert f1["commercial_candidate"] is False
    assert "Incumbent presence is strong" in f1["incumbent_preflight"]
    assert scan["examined_formations"][0]["verdict"] == "RETAINED_FOR_CHEAP_FALSIFICATION"

def test_scan051_demotes_five_mature_or_expert_unit_flows():
    scan = load(SCAN)
    demoted = [row for row in scan["examined_formations"] if row.get("formation_id") != "ATTRACTION_SCAN_051-F1"]
    assert len(demoted) == 5
    assert all(row["verdict"].startswith("DEMOTED_") for row in demoted)

def test_state_retains_scan015_and_scan051_f1_only():
    state = load(STATE)
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_051"
    assert state["next_scan_id"] == "ATTRACTION_SCAN_052"
    assert state["active_commercial_candidates"] == []
    assert state["first_external_value_flow"] == "NOT_PROVEN"
    retained = {item["formation_id"] for item in state["retained_research_formations"]}
    assert retained == {"ATTRACTION_SCAN_015-F1", "ATTRACTION_SCAN_051-F1"}
