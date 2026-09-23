import json
from pathlib import Path

from src.ground_truth_routing_economics import (
    EconomicsDecision,
    TaskEconomicsEvidence,
    evaluate_task_economics,
    ground_truth_economics_boundaries,
)
from src.jev_research_advisory import build_research_states
from tools.run_jev_research_advisory import resolve_scan_path

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "data" / "research_runs" / "attraction_scan_126.json"
ECON = ROOT / "data" / "research_runs" / "scan126_ground_truth_economics.json"
STATE = ROOT / "data" / "commercial_reset_state.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_scan126_is_canonical_and_live_jev_auto_resolution_uses_it():
    state = load(STATE)
    path = resolve_scan_path("auto", state, research_dir=ROOT / "data" / "research_runs")
    assert state["last_completed_scan_id"] == "ATTRACTION_SCAN_126"
    assert path == SCAN


def test_scan126_exposes_exactly_one_open_formation_to_jev():
    scan = load(SCAN)
    state = load(STATE)
    states = build_research_states(scan=scan, commercial_state=state)
    assert scan["status"] == "COMPLETE"
    assert scan["zero_primary_admissions"] is False
    assert scan["active_commercial_candidate_promotions"] == []
    assert scan["retained_research_formations"] == ["ATTRACTION_SCAN_126-F1"]
    assert len(states) == 1
    row = states[0]
    assert row["formation"]["formation_id"] == "ATTRACTION_SCAN_126-F1"
    assert row["authoritative_engine_context"]["existing_closure_authoritative"] is False
    assert row["authoritative_engine_context"]["already_retained_for_research"] is True


def test_four_dollar_site_visit_is_below_executor_floor_even_before_travel():
    ev = TaskEconomicsEvidence(
        buyer_budget_cny=26.804,
        executor_payout_min_cny=30,
        executor_payout_max_cny=80,
        marketplace_fee_rate_max=0.15,
        same_scope_cost_binding=True,
        subcontract_path_authorized=True,
        access_and_privacy_resolved=True,
        travel_cost_max_cny=0,
        qa_rework_cost_max_cny=0,
    )
    assert evaluate_task_economics(ev) is EconomicsDecision.REJECT_PRICE_BELOW_EXECUTOR_FLOOR


def test_hypothetical_same_scope_hundred_dollar_task_has_headroom_but_not_normalized_without_travel_qa_bounds():
    ev = TaskEconomicsEvidence(
        buyer_budget_cny=670.1,
        executor_payout_min_cny=80,
        executor_payout_max_cny=200,
        marketplace_fee_rate_max=0.15,
        same_scope_cost_binding=True,
        subcontract_path_authorized=True,
        access_and_privacy_resolved=True,
    )
    low, high = ev.raw_headroom_range()
    assert round(low, 3) == 369.585
    assert round(high, 3) == 489.585
    assert evaluate_task_economics(ev) is EconomicsDecision.POSITIVE_HEADROOM_NOT_NORMALIZED


def test_retail_shop_signal_has_positive_raw_headroom_but_not_ready_by_itself():
    econ = load(ECON)
    retail = next(x for x in econ["task_classes"] if x["task_class"] == "RETAIL_SHELF_OR_SHOP_PHOTO_EVIDENCE")
    assert retail["raw_headroom_cny_at_high_payout"] > 0
    assert retail["travel_cost_bound"] is False
    assert retail["qa_rework_cost_bound"] is False
    assert retail["verdict"] == "POSITIVE_HEADROOM_NOT_NORMALIZED"


def test_factory_qc_cannot_borrow_generic_crowd_cost_as_same_scope():
    ev = TaskEconomicsEvidence(
        buyer_budget_cny=1340.2,
        executor_payout_min_cny=80,
        executor_payout_max_cny=200,
        marketplace_fee_rate_max=0.15,
        same_scope_cost_binding=False,
        specialist_required=True,
        subcontract_path_authorized=True,
        access_and_privacy_resolved=True,
    )
    assert evaluate_task_economics(ev) is EconomicsDecision.REJECT_SPECIALIST_SCOPE


def test_authorization_and_access_are_hard_gates():
    base = dict(
        buyer_budget_cny=670.1,
        executor_payout_min_cny=80,
        executor_payout_max_cny=200,
        marketplace_fee_rate_max=0.15,
        same_scope_cost_binding=True,
        travel_cost_max_cny=50,
        qa_rework_cost_max_cny=50,
    )
    assert evaluate_task_economics(
        TaskEconomicsEvidence(**base, subcontract_path_authorized=False, access_and_privacy_resolved=True)
    ) is EconomicsDecision.BLOCKED_SUBCONTRACT_AUTHORIZATION
    assert evaluate_task_economics(
        TaskEconomicsEvidence(**base, subcontract_path_authorized=True, access_and_privacy_resolved=False)
    ) is EconomicsDecision.BLOCKED_ACCESS_OR_PRIVACY


def test_ready_state_requires_positive_fully_bounded_worst_case_headroom():
    ev = TaskEconomicsEvidence(
        buyer_budget_cny=670.1,
        executor_payout_min_cny=80,
        executor_payout_max_cny=200,
        marketplace_fee_rate_max=0.15,
        same_scope_cost_binding=True,
        subcontract_path_authorized=True,
        access_and_privacy_resolved=True,
        travel_cost_max_cny=100,
        qa_rework_cost_max_cny=80,
    )
    assert round(ev.normalized_worst_case_headroom(), 3) == 189.585
    assert evaluate_task_economics(ev) is EconomicsDecision.BOUNDED_BOOTSTRAP_ECONOMICS_READY


def test_truth_boundaries_are_explicit():
    boundaries = ground_truth_economics_boundaries()
    assert "RAW_SPREAD_NE_NORMALIZED_MARGIN" in boundaries
    assert "SAME_SCOPE_COST_BINDING_REQUIRED" in boundaries
    assert "SUBCONTRACT_PATH_MUST_BE_AUTHORIZED" in boundaries
    assert "TRAVEL_QA_REWORK_MUST_BE_BOUNDED_FOR_READY_STATE" in boundaries


def test_observed_hundred_dollar_audit_remains_scope_unbound():
    econ = load(ECON)
    audit = next(x for x in econ["task_classes"] if x["task_class"] == "PREDEFINED_NONTECHNICAL_SITE_AUDIT")
    assert audit["same_scope_cost_binding"] is False
    assert audit["verdict"] == "SCOPE_NOT_COMPARABLE_YET"
