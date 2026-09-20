from src.attraction_discovery import AttractionDiscoveryProfile, AttractionEvidence
from src.attraction_frontier import (
    dominates,
    non_dominated_layers,
    pareto_frontier,
)


def ev(name: str):
    return (AttractionEvidence(source_id=name, claim=f"evidence for {name}"),)


def profile(signal_id: str, **overrides):
    values = dict(
        signal_id=signal_id,
        reality_pattern=f"pattern {signal_id}",
        a_actor="A",
        b_actor="B",
        candidate_bridge="narrow bridge",
        a_voluntary_motion=2,
        b_voluntary_motion=2,
        state_dependent_value_jump=2,
        decision_window=2,
        bridge_compression=2,
        activation_ease=2,
        self_propulsion=2,
        operator_control=2,
        a_discoverability=2,
        b_discoverability=2,
        match_resolvability=2,
        action_gate_callability=2,
        a_motion_evidence=ev(signal_id + "-a"),
        b_motion_evidence=ev(signal_id + "-b"),
        value_jump_evidence=ev(signal_id + "-value"),
        decision_window_evidence=ev(signal_id + "-decision"),
        bridge_compression_evidence=ev(signal_id + "-bridge"),
        activation_evidence=ev(signal_id + "-activation"),
        self_propulsion_evidence=ev(signal_id + "-self"),
        operator_control_evidence=ev(signal_id + "-operator"),
        a_discoverability_evidence=ev(signal_id + "-a-discoverability"),
        b_discoverability_evidence=ev(signal_id + "-b-discoverability"),
        match_resolvability_evidence=ev(signal_id + "-match"),
        action_gate_evidence=ev(signal_id + "-action"),
    )
    values.update(overrides)
    return AttractionDiscoveryProfile(**values)


def test_dominance_requires_no_worse_everywhere_and_better_somewhere():
    strong = profile("strong", state_dependent_value_jump=3)
    base = profile("base")
    tradeoff = profile("tradeoff", a_voluntary_motion=3, decision_window=2)

    assert dominates(strong, base) is True
    assert dominates(base, strong) is False
    assert dominates(strong, tradeoff) is False


def test_pareto_frontier_keeps_incomparable_high_attraction_structures():
    a = profile("A", a_voluntary_motion=3, state_dependent_value_jump=2)
    b = profile("B", a_voluntary_motion=2, state_dependent_value_jump=3)
    dominated = profile("C")

    assert pareto_frontier([a, b, dominated]) == ("A", "B")


def test_low_attraction_signal_never_enters_frontier_even_if_other_dimensions_are_high():
    valid = profile("valid")
    late = profile(
        "late",
        a_voluntary_motion=3,
        b_voluntary_motion=3,
        state_dependent_value_jump=3,
        decision_window=1,
        bridge_compression=3,
        activation_ease=3,
        self_propulsion=3,
        operator_control=3,
        a_discoverability=3,
        b_discoverability=3,
        match_resolvability=3,
        action_gate_callability=3,
    )

    result = non_dominated_layers([late, valid])
    assert result.frontier_signal_ids == ("valid",)
    assert result.excluded_signal_ids == ("late",)


def test_non_dominated_sort_produces_attention_layers_without_weighted_score():
    top = profile("top", state_dependent_value_jump=3, operator_control=3)
    middle = profile("middle", state_dependent_value_jump=3)
    base = profile("base")

    result = non_dominated_layers([base, top, middle])
    assert result.dominance_layers == (("top",), ("middle",), ("base",))
    assert result.dominated_by["base"] == ("middle", "top")


def test_identical_vectors_are_both_non_dominated():
    x = profile("X")
    y = profile("Y")
    assert pareto_frontier([x, y]) == ("X", "Y")


def test_duplicate_signal_ids_fail_closed():
    x1 = profile("X")
    x2 = profile("X")
    try:
        non_dominated_layers([x1, x2])
    except ValueError as exc:
        assert "duplicate attraction signal ids" in str(exc)
    else:
        raise AssertionError("duplicate ids must fail closed")


def test_action_gate_is_non_compensatory_in_frontier():
    valid = profile("valid")
    blocked = profile(
        "blocked",
        state_dependent_value_jump=3,
        operator_control=3,
        action_gate_callability=1,
        action_gate_evidence=ev("blocked-case-by-case-permission"),
    )
    result = non_dominated_layers([valid, blocked])
    assert result.frontier_signal_ids == ("valid",)
    assert result.excluded_signal_ids == ("blocked",)
