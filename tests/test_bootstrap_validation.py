from src.attraction_discovery import AttractionDiscoveryProfile, AttractionEvidence
from src.bootstrap_validation import (
    BootstrapDecision,
    BoundedBootstrapPlan,
    bounded_manual_bootstrap_allowed,
)


def ev(name: str):
    return (AttractionEvidence(source_id=name, claim=f"evidence for {name}"),)


def high_profile(**overrides):
    values = dict(
        signal_id="SCAN126-GROUND-TRUTH",
        reality_pattern="remote overseas principals repeatedly pay for bounded physical evidence in China",
        a_actor="remote overseas buyer or team with a time-sensitive China decision",
        b_actor="replaceable China-local executor capable of bounded permitted observation",
        candidate_bridge="standardized dispatch plus evidence acceptance layer",
        a_voluntary_motion=3,
        b_voluntary_motion=3,
        state_dependent_value_jump=3,
        decision_window=3,
        bridge_compression=2,
        activation_ease=2,
        self_propulsion=2,
        operator_control=2,
        a_discoverability=3,
        b_discoverability=3,
        match_resolvability=2,
        action_gate_callability=2,
        a_motion_evidence=ev("public-paid-demand"),
        b_motion_evidence=ev("public-executor-supply"),
        value_jump_evidence=ev("pre-payment-or-shipment-decision"),
        decision_window_evidence=ev("decision-before-deposit-shipment-trip"),
        bridge_compression_evidence=ev("location-checklist-evidence-bundle"),
        activation_evidence=ev("fixed-scope-prepaid-task"),
        self_propulsion_evidence=ev("repeating-import-audit-and-field-work-events"),
        operator_control_evidence=ev("scope-dispatch-acceptance-settlement"),
        a_discoverability_evidence=ev("reddit-upwork-public-intent"),
        b_discoverability_evidence=ev("local-platform-and-field-network"),
        match_resolvability_evidence=ev("city-task-type-deadline"),
        action_gate_evidence=ev("platform-escrow-or-prepaid-fixed-scope"),
    )
    values.update(overrides)
    return AttractionDiscoveryProfile(**values)


def plan(**overrides):
    values = dict(
        formation_id="ATTRACTION_SCAN_126-F1",
        decisive_unknown="can the operator route paid China-local evidence tasks with repeatable margin and replaceable executors?",
        external_demand_evidence_count=6,
        external_payment_signal_count=4,
        local_executor_supply_evidence_count=3,
        buyer_prepayment_or_platform_escrow_available=True,
        standardized_task_brief=True,
        standardized_acceptance_evidence=True,
        executor_replaceability_path=True,
        founder_manual_transaction_cap=3,
        founder_manual_day_cap=14,
        founder_free_labor_excluded_from_unit_economics=True,
    )
    values.update(overrides)
    return BoundedBootstrapPlan(**values)


def test_high_attraction_target_state_can_use_tiny_manual_bootstrap():
    assert (
        bounded_manual_bootstrap_allowed(high_profile(), plan())
        is BootstrapDecision.BOUNDED_VALIDATION_ALLOWED
    )


def test_low_attraction_project_cannot_hide_behind_bootstrap_language():
    profile = high_profile(
        b_voluntary_motion=1,
        b_motion_evidence=ev("weak-supply-push"),
    )
    assert bounded_manual_bootstrap_allowed(profile, plan()) is BootstrapDecision.FORBIDDEN


def test_bootstrap_cannot_become_open_ended_manual_operations():
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(founder_manual_transaction_cap=4)
        )
        is BootstrapDecision.FORBIDDEN
    )
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(founder_manual_day_cap=30)
        )
        is BootstrapDecision.FORBIDDEN
    )


def test_founder_manufactured_demand_is_forbidden():
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(founder_manufactured_demand=True)
        )
        is BootstrapDecision.FORBIDDEN
    )


def test_buyer_money_signal_and_pre_execution_payment_are_required():
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(external_payment_signal_count=0)
        )
        is BootstrapDecision.FORBIDDEN
    )
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(buyer_prepayment_or_platform_escrow_available=False)
        )
        is BootstrapDecision.FORBIDDEN
    )


def test_local_executor_must_be_replaceable_and_evidenced():
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(local_executor_supply_evidence_count=1)
        )
        is BootstrapDecision.FORBIDDEN
    )
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(executor_replaceability_path=False)
        )
        is BootstrapDecision.FORBIDDEN
    )


def test_free_founder_labor_cannot_make_bad_economics_look_good():
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(founder_free_labor_excluded_from_unit_economics=False)
        )
        is BootstrapDecision.FORBIDDEN
    )


def test_specialist_certification_and_permanent_founder_work_are_not_generic_bootstrap():
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(), plan(specialist_certification_required=True)
        )
        is BootstrapDecision.FORBIDDEN
    )
    assert (
        bounded_manual_bootstrap_allowed(
            high_profile(),
            plan(target_state_founder_search_required_per_transaction=True),
        )
        is BootstrapDecision.FORBIDDEN
    )
