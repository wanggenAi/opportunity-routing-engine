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
        action_gate_callability=3,
        a_population_replenishment=3,
        b_population_replenishment=3,
        recurring_connection_pressure=3,
        recurring_missing_edge=3,
        recurring_event_source=3,
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
        action_gate_evidence=ev("action-gate"),
        a_population_replenishment_evidence=ev("a-replenishment"),
        b_population_replenishment_evidence=ev("b-replenishment"),
        recurring_connection_pressure_evidence=ev("connection-pressure"),
        recurring_missing_edge_evidence=ev("missing-edge"),
        recurring_event_source_evidence=ev("event-source"),
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


def test_uncallable_action_gate_kills_high_attraction():
    p = profile(
        action_gate_callability=1,
        action_gate_evidence=ev("requires-case-by-case-incumbent-permission"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
    assert discovery_attention_allowed(p) is False


def test_stable_callable_action_gate_can_survive_with_other_hard_floors():
    p = profile(
        action_gate_callability=2,
        action_gate_evidence=ev("standard-self-service-transaction-rail"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.HIGH_ATTRACTION_BEACON


def test_native_transaction_api_is_strong_action_gate_evidence():
    p = profile(
        action_gate_callability=3,
        action_gate_evidence=ev("native-api-order-booking-settlement"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.HIGH_ATTRACTION_BEACON


def test_generic_agent_substitutability_requires_evidence():
    p = profile(generic_agent_substitutable=True)
    assert attraction_beacon_state(p) is AttractionBeaconState.UNASSESSED
    assert discovery_attention_allowed(p) is False


def test_generic_agent_substitutability_kills_high_attraction():
    p = profile(
        generic_agent_substitutable=True,
        generic_agent_substitution_evidence=ev(
            "general-agent-plus-official-rail-reproduces-same-route"
        ),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
    assert discovery_attention_allowed(p) is False


def test_missing_regenerative_field_kills_high_attraction():
    p = profile(
        recurring_missing_edge=1,
        recurring_missing_edge_evidence=ev("market-already-closes-the-edge"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
    assert discovery_attention_allowed(p) is False


def test_single_transaction_seed_is_not_a_discovery_ontology():
    p = profile(explicit_transaction_seeded=True)
    assert attraction_beacon_state(p) is AttractionBeaconState.LOW_ATTRACTION
    assert discovery_attention_allowed(p) is False


def test_transaction_observation_can_survive_only_after_independent_field_evidence():
    p = profile(
        explicit_transaction_seeded=True,
        independent_regenerative_field_evidence=ev("independent-replenishing-field"),
    )
    assert attraction_beacon_state(p) is AttractionBeaconState.HIGH_ATTRACTION_BEACON
    assert discovery_attention_allowed(p) is True
