import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "data" / "research_runs" / "attraction_scan_015_f1_gate_b_preflight.json"
SKILL_PATH = ROOT / "experiments" / "scan015_f1_gate_b_skill" / "SKILL.md"


def load_state():
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def test_gate_b_preflight_is_not_promoted_or_published():
    state = load_state()
    assert state["status"] == "PREPARED_NOT_PUBLISHED"
    assert state["gate_b"] == "NOT_RUN"
    assert state["experiment"]["published"] is False
    assert state["first_external_value_flow"] == "NOT_PROVEN"


def test_gate_b_preflight_cannot_execute_transactions_or_collect_identity():
    state = load_state()
    assert state["experiment"]["transaction_execution"] is False
    assert state["experiment"]["real_platform_quotes"] is False
    assert state["experiment"]["collects_personal_data"] is False


def test_founder_distribution_cannot_count_as_inbound_proof():
    state = load_state()
    assert state["experiment"]["founder_distribution_allowed_as_gate_evidence"] is False
    assert state["experiment"]["paid_acquisition_allowed_as_gate_evidence"] is False
    assert state["experiment"]["synthetic_prompts_allowed_as_gate_evidence"] is False


def test_discovery_infrastructure_does_not_imply_seller_intent():
    state = load_state()
    assert state["surfaces"]["qianwen_ai_skills_hub"]["discovery_infrastructure"] == "PASS"
    assert state["surfaces"]["qianwen_ai_skills_hub"]["qualified_used_device_seller_intent"] == "NOT_PROVEN"
    assert state["surfaces"]["onekey_mcp"]["end_user_seller_intent"] == "NOT_PROVEN"


def test_skill_is_fail_closed_on_sensitive_data_and_live_routing():
    skill = SKILL_PATH.read_text(encoding="utf-8")
    for prohibited in [
        "Never ask for or retain:",
        "mobile;",
        "exact address;",
        "payment account;",
        "IMEI;",
        "serial number;",
        "Do not fabricate:",
        "live quotes;",
        "platform rankings;",
        "This is an experiment artifact. It is not a live recycling router.",
    ]:
        assert prohibited in skill
