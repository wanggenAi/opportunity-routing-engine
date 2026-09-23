from datetime import date

from src.attraction_discovery import AttractionDiscoveryProfile, AttractionEvidence
from src.success_pattern_calibration import (
    CalibrationState,
    LaunchUrgencyPolicy,
    PrecedentEvidenceClass,
    SearchDirection,
    SuccessPrecedent,
    calibrate_search_direction,
    deadline_response,
    high_attraction_experiment_allowed,
    independently_supported_mechanisms,
    precedent_cycle_is_broad_enough,
)


def ev(name: str):
    return (AttractionEvidence(source_id=name, claim=f"evidence for {name}"),)


def profile(**overrides):
    values = dict(
        signal_id="S-CAL",
        reality_pattern="both sides already moving around a narrow missing edge",
        a_actor="A",
        b_actor="B",
        candidate_bridge="machine-resolvable bridge",
        a_voluntary_motion=3,
        b_voluntary_motion=3,
        state_dependent_value_jump=3,
        decision_window=3,
        bridge_compression=3,
        activation_ease=2,
        self_propulsion=2,
        operator_control=3,
        a_discoverability=3,
        b_discoverability=3,
        match_resolvability=3,
        action_gate_callability=3,
        a_motion_evidence=ev("a"),
        b_motion_evidence=ev("b"),
        value_jump_evidence=ev("value"),
        decision_window_evidence=ev("window"),
        bridge_compression_evidence=ev("bridge"),
        activation_evidence=ev("activation"),
        self_propulsion_evidence=ev("self"),
        operator_control_evidence=ev("operator"),
        a_discoverability_evidence=ev("a-discovery"),
        b_discoverability_evidence=ev("b-discovery"),
        match_resolvability_evidence=ev("match"),
        action_gate_evidence=ev("action"),
    )
    values.update(overrides)
    return AttractionDiscoveryProfile(**values)


def precedent(i: int, *, negative=False, source_class=None):
    return SuccessPrecedent(
        precedent_id=f"P{i}",
        source_url=f"https://example.com/{i}",
        evidence_class=source_class
        or (
            PrecedentEvidenceClass.OFFICIAL
            if i % 2
            else PrecedentEvidenceClass.FOUNDER_INTERVIEW
        ),
        observed_result="real usage or revenue",
        mechanisms=frozenset(
            {"SELF_SERVICE_ACTIVATION", "MACHINE_NATIVE_DELIVERY", f"M{i % 3}"}
        ),
        transfer_claim="learn the mechanism, not the vertical",
        anti_copy_warning="do not copy the product or treat success as candidate proof",
        negative_control=negative,
    )


def policy():
    return LaunchUrgencyPolicy(
        decision_deadline=date(2026, 9, 30),
        minimum_precedents_per_cycle=8,
        minimum_source_classes=3,
        minimum_independent_support_per_mechanism=2,
    )


def broad_precedents():
    items = [precedent(i) for i in range(1, 8)]
    items.append(
        precedent(
            8,
            source_class=PrecedentEvidenceClass.CREDIBLE_SECONDARY,
        )
    )
    return items


def test_precedent_cycle_requires_real_breadth_not_one_famous_story():
    assert precedent_cycle_is_broad_enough(broad_precedents(), policy()) is True
    assert precedent_cycle_is_broad_enough(broad_precedents()[:4], policy()) is False


def test_repeated_mechanisms_become_search_priors_not_candidate_proof():
    supported = independently_supported_mechanisms(broad_precedents())
    assert "SELF_SERVICE_ACTIVATION" in supported
    assert "MACHINE_NATIVE_DELIVERY" in supported


def test_success_precedent_cannot_rescue_low_attraction_direction():
    direction = SearchDirection(
        direction_id="D1",
        attraction_profile=profile(founder_sales_required_per_transaction=True),
        mechanisms=frozenset({"SELF_SERVICE_ACTIVATION", "MACHINE_NATIVE_DELIVERY"}),
    )
    assert (
        calibrate_search_direction(direction, broad_precedents(), policy())
        is CalibrationState.LOW_ATTRACTION_REJECT
    )


def test_high_attraction_direction_can_use_independent_success_patterns_as_prior():
    direction = SearchDirection(
        direction_id="D2",
        attraction_profile=profile(),
        mechanisms=frozenset({"SELF_SERVICE_ACTIVATION", "MACHINE_NATIVE_DELIVERY"}),
    )
    assert (
        calibrate_search_direction(direction, broad_precedents(), policy())
        is CalibrationState.CALIBRATED_HIGH_ATTRACTION_SEARCH_DIRECTION
    )


def test_negative_control_does_not_create_positive_mechanism_support():
    items = broad_precedents()
    negative = SuccessPrecedent(
        precedent_id="NEG",
        source_url="https://example.com/neg",
        evidence_class=PrecedentEvidenceClass.COMMUNITY_SELF_REPORT,
        observed_result="revenue mainly from cold outreach and lifetime deals",
        mechanisms=frozenset({"COLD_OUTREACH_DEPENDENCE"}),
        transfer_claim="financial success can still violate our model",
        anti_copy_warning="do not use revenue alone as attraction evidence",
        negative_control=True,
    )
    supported = independently_supported_mechanisms([*items, negative])
    assert "COLD_OUTREACH_DEPENDENCE" not in supported


def test_fast_experiment_is_forbidden_when_attraction_is_weak():
    assert (
        high_attraction_experiment_allowed(
            profile(founder_delivery_required=True),
            decisive_unknown="will the rail grant outcome-data rights?",
            reversible=True,
            founder_manufactured_demand=False,
        )
        is False
    )


def test_high_attraction_experiment_must_not_manufacture_demand():
    assert (
        high_attraction_experiment_allowed(
            profile(),
            decisive_unknown="will organic actors invoke this route?",
            reversible=True,
            founder_manufactured_demand=True,
        )
        is False
    )
    assert (
        high_attraction_experiment_allowed(
            profile(),
            decisive_unknown="will organic actors invoke this route?",
            reversible=True,
            founder_manufactured_demand=False,
        )
        is True
    )


def test_deadline_expands_search_instead_of_relaxing_gates():
    p = policy()
    assert deadline_response(
        p, as_of=date(2026, 9, 29), retained_high_attraction_formations=0
    ) == "CONTINUE_CALIBRATED_HIGH_BREADTH_SEARCH"
    assert deadline_response(
        p, as_of=date(2026, 10, 1), retained_high_attraction_formations=0
    ) == "EXPAND_SOURCE_UNIVERSE_AND_MECHANISM_DIVERSITY_DO_NOT_RELAX_GATES"
