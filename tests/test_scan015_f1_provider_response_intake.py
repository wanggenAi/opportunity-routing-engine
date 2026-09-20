import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "research_runs" / "attraction_scan_015_f1_provider_response_intake.json"


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def test_no_response_is_not_fail():
    state = load_state()
    for provider in ("AIHUISHOU", "XIAOZHI_BEARHOME"):
        p = state["providers"][provider]
        assert p["outreach_sent"] is True
        assert p["response_received"] is False
        assert p["classification"] == "NO_RESPONSE_YET"
        assert "FAIL" not in p["dimensions"].values()


def test_two_compatible_written_rails_are_required():
    state = load_state()
    assert state["gate_rule"]["required_compatible_written_rails"] == 2
    assert state["compatible_written_rails"] == 0
    assert state["gate_a"] == "PARTIAL_PASS_RIGHTS_UNKNOWN"


def test_raw_evidence_must_remain_separate_from_classification():
    state = load_state()
    assert "RAW_PROVIDER_TEXT_MUST_BE_PRESERVED_SEPARATELY_FROM_INTERPRETATION" in state["truth_rules"]
    for provider in state["providers"].values():
        assert "evidence" in provider
        assert "dimensions" in provider


def test_suhuanji_remains_contact_unresolved():
    state = load_state()
    p = state["providers"]["SUHUANJI"]
    assert p["outreach_sent"] is False
    assert p["classification"] == "CONTACT_UNRESOLVED"
