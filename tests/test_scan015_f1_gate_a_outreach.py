import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "research_runs" / "attraction_scan_015_f1_gate_a_outreach.json"


def load_state():
    return json.loads(STATE.read_text(encoding="utf-8"))


def test_wave1_is_sent_but_rights_are_still_unknown():
    state = load_state()
    assert state["status"] == "WAVE1_SENT_WAITING_RESPONSE"
    assert state["wave1"]["targets"]["AIHUISHOU"]["draft_ready"] is True
    assert state["wave1"]["targets"]["AIHUISHOU"]["sent"] is True
    assert state["wave1"]["targets"]["XIAOZHI_BEARHOME"]["draft_ready"] is True
    assert state["wave1"]["targets"]["XIAOZHI_BEARHOME"]["sent"] is True


def test_preparation_and_sending_cannot_promote_rights():
    state = load_state()
    assert state["rights_confirmed_rails"] == 0
    assert state["provider_responses"] == 0
    assert state["gate_a"] == "PARTIAL_PASS_RIGHTS_UNKNOWN"
    assert state["evidence_rules"]["draft_ready_does_not_mean_sent"] is True
    assert state["evidence_rules"]["sent_does_not_mean_permission"] is True
    assert state["evidence_rules"]["vague_commercial_reply_does_not_mean_pass"] is True


def test_two_written_rails_are_still_required():
    state = load_state()
    assert state["evidence_rules"]["two_compatible_written_rails_required"] is True
    assert state["external_action_requires_explicit_user_authorization"] is False


def test_suhuanji_contact_is_not_fabricated():
    state = load_state()
    target = state["wave1"]["targets"]["SUHUANJI"]
    assert target["official_contact"] == "UNRESOLVED"
    assert target["draft_ready"] is False
    assert target["sent"] is False


def test_sent_messages_do_not_imply_permission():
    state = load_state()
    assert state["external_action_truth"]["emails_sent"] is True
    assert state["external_action_truth"]["responses_received"] == 0
    assert state["external_action_truth"]["rights_confirmed_rails"] == 0
    assert state["external_action_truth"]["gate_a"] == "PARTIAL_PASS_RIGHTS_UNKNOWN"
