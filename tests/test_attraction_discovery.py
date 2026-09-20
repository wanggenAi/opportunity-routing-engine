from src.attraction_discovery import (
    AttractionBeaconState,
    AttractionDiscoveryProfile,
    AttractionEvidence,
    attraction_beacon_state,
    discovery_attention_allowed,
)


def ev(name: str):
    return (AttractionEvidence(source_id=name, claim=f"evidence for {name}"),)


def profile(**overrides):
    values = dict(
        signal_id="S1",
        reality_pattern="two sides already spending effort to reach the same state",
        a_actor="A",
        b_actor="B",
        candidate_bridge="narrow missing edge",
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
        a_motion_evidence=ev("a"),
        b_motion_evidence=ev("b"),
        value_jump_evidence=ev("value"),
        decision_window_evidence=ev("decision"),
        bridge_compression_evidence=ev("bridge"),
        activation_evidence=ev("activation"),
        self_propulsion_evidence=ev("self"),
        operator_control_evidence=ev("operator"),
        a_discoverability_evidence=ev("a-discoverability"),
        b_discoverability_evidence=ev("b-discoverability"),
        match_resolvability_evidence=ev("match-resolvability"),
    )
    values.update(overrides)
    return AttractionDiscoveryProfile(**values)


def test_high_attraction_is_first_class_discovery_beacon():
    p = profile()
    assert attraction_beacon_state(p) is AttractionBeaconState.HIGH_ATTRACTION_BEACON
    assert discovery_attention_allowed(p) is True


def test_real_but_late_locked_friction_is_low_attraction():
    p = profile(
        decision_window=1,
        decision_window_evidence=ev("budget-and-vendor-already-locked"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
    assert discovery_attention_allowed(p) is False


def test_one_dead_side_cannot_be_averaged_away():
    p = profile(
        b_voluntary_motion=1,
        b_motion_evidence=ev("b-only-theoretical-benefit"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION


def test_big_value_story_cannot_override_founder_delivery():
    p = profile(founder_delivery_required=True)
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION


def test_high_explanation_burden_is_not_a_wow_connection():
    p = profile(explanation_burden_high=True)
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION


def test_hidden_supply_kills_high_attraction():
    p = profile(
        a_discoverability=1,
        a_discoverability_evidence=ev("supply-requires-offline-hunting"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
    assert discovery_attention_allowed(p) is False


def test_hidden_demand_kills_high_attraction():
    p = profile(
        b_discoverability=1,
        b_discoverability_evidence=ev("demand-only-visible-through-private-network"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION


def test_recurring_expert_matching_kills_high_attraction():
    p = profile(expert_matching_required_per_transaction=True)
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION


def test_founder_search_is_not_operator_control():
    p = profile(founder_search_required_per_transaction=True)
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION


def test_unresolvable_match_kills_high_attraction_even_with_large_value_jump():
    p = profile(
        match_resolvability=1,
        match_resolvability_evidence=ev("compatibility-requires-case-by-case-engineer"),
        state_dependent_value_jump=3,
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
