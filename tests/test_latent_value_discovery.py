import unittest

from src.causal_descent import (
    CausalDescentRecord,
    CausalStopReason,
    CausalTruthState,
    LatentOutcomeHypothesis,
    StructuralConstraintHypothesis,
)
from src.latent_value_discovery import (
    CandidateClass,
    DiscoveryState,
    EvidenceKind,
    EvidenceRef,
    LatentValueCandidate,
    discovery_state,
    missing_validation_evidence,
    validate_candidate,
    validate_candidate_record,
)


class LatentValueDiscoveryTests(unittest.TestCase):
    def _causal_descent(self):
        return CausalDescentRecord(
            record_id="CD-FACTORY-KNOWLEDGE-001",
            actor="factory veteran technicians",
            current_state="deep tacit fault-diagnosis knowledge remains person-bound",
            surface_phenomenon=(
                "valuable diagnostic knowledge remains person-bound while access "
                "to it becomes less reliable"
            ),
            surface_evidence_refs=("origin", "structure"),
            outcome_hypotheses=(
                LatentOutcomeHypothesis(
                    outcome_id="OUTCOME-FACTORY-KNOWLEDGE",
                    statement=(
                        "convert bounded tacit diagnostic capability into trusted "
                        "callable outcomes without requiring the original full-time role"
                    ),
                    truth_state=CausalTruthState.EVIDENCED_STRUCTURE,
                    evidence_refs=("origin", "pressure"),
                    falsifiers=(
                        "the knowledge cannot be abstracted beyond the original expert",
                    ),
                ),
                LatentOutcomeHypothesis(
                    outcome_id="OUTCOME-FACTORY-RETENTION",
                    statement=(
                        "keep diagnostic capability inside the original employment "
                        "relationship rather than externalize it as a callable unit"
                    ),
                    truth_state=CausalTruthState.INFERRED,
                    evidence_refs=("origin", "structure"),
                    falsifiers=(
                        "rights-cleared bounded knowledge is repeatedly used outside the original role",
                    ),
                ),
            ),
            selected_outcome_id="OUTCOME-FACTORY-KNOWLEDGE",
            outcome_selection_rationale=(
                "observed choices and sacrifices fit this product-agnostic state "
                "transition better than the nearby alternative explanations"
            ),
            constraint_hypotheses=(
                StructuralConstraintHypothesis(
                    constraint_id="C-PACKAGING",
                    outcome_id="OUTCOME-FACTORY-KNOWLEDGE",
                    depth=1,
                    causal_claim=(
                        "knowledge is not represented as a bounded, rights-cleared, "
                        "evidence-backed and acceptance-ready capability unit"
                    ),
                    mechanism=(
                        "external users cannot cheaply verify rights, scope, reliability "
                        "or acceptance for person-bound diagnostic knowledge"
                    ),
                    truth_state=CausalTruthState.EVIDENCED_STRUCTURE,
                    support_refs=("structure", "barrier"),
                    discriminating_evidence_refs=("pressure",),
                    falsifiers=(
                        "equivalent rights-cleared bounded modules already clear repeatedly",
                    ),
                    intervention_implication=(
                        "make the knowledge rights-cleared, bounded, evidenced and accepted"
                    ),
                ),
                StructuralConstraintHypothesis(
                    constraint_id="C-CONTEXT-SPECIFIC",
                    outcome_id="OUTCOME-FACTORY-KNOWLEDGE",
                    depth=1,
                    causal_claim=(
                        "the apparent stranding may instead be caused by knowledge that "
                        "is too context-specific to transfer"
                    ),
                    mechanism=(
                        "value disappears outside the original machine, team or expert context"
                    ),
                    truth_state=CausalTruthState.INFERRED,
                    support_refs=("origin",),
                    falsifiers=(
                        "the same bounded diagnostic rule works across independent cases",
                    ),
                ),
            ),
            lead_constraint_ids=("C-PACKAGING",),
            outcome_selection_evidence_refs=("origin", "pressure"),
            deeper_search_would_change_decision=False,
            stop_reason=CausalStopReason.INTERVENTION_RELEVANT_BOUNDARY,
            stop_rationale=(
                "the current causal frontier is already specific enough to change "
                "which interface or capability must be tested next"
            ),
        )

    def _candidate(self, **overrides):
        payload = dict(
            candidate_id="LV-001",
            actor="factory veteran technicians",
            observed_state="deep tacit fault-diagnosis knowledge remains person-bound",
            observed_change="retirement and technician turnover increase knowledge-loss risk",
            hidden_or_underrecognized_value="repeatable industrial diagnostic knowledge",
            why_value_is_not_recognized_or_realized="knowledge is treated as personal experience rather than a callable asset",
            complementary_actor_hypothesis="smaller factories with recurring equipment faults",
            complementary_actor_state="downtime and repeated dependence on scarce senior technicians",
            transformation_mechanism="extract, verify and package diagnosis knowledge into bounded callable decision units",
            why_exchange_does_not_already_happen="no trusted packaging, rights, proof, interface or settlement structure exists",
            incremental_value_for_origin_actor="previously stranded experience becomes paid utilization",
            incremental_value_for_complementary_actor="faster fault triage and lower downtime cost",
            orchestrator_value_capture_hypothesis="fee for verified packaging, routing, acceptance and reliability",
            cheapest_decisive_validation="test one rights-cleared fault domain with one expert and one real user",
            kill_conditions="rights cannot be cleared, knowledge cannot be abstracted, or counterpart gets no measurable value",
            surface_phenomenon_or_friction="valuable diagnostic knowledge remains person-bound while access to it becomes less reliable",
            latent_outcome_hypothesis="convert bounded tacit diagnostic capability into trusted callable outcomes without requiring the original full-time role",
            structural_friction_hypothesis="knowledge is not represented as a bounded, rights-cleared, evidence-backed and acceptance-ready capability unit",
            structural_friction_truth_state="EVIDENCED_STRUCTURE",
            alternative_explanations=(
                "the knowledge may be too context-specific to abstract",
                "existing service providers may already package the relevant capability adequately",
            ),
            causal_descent=self._causal_descent(),
            causal_descent_record_id="CD-FACTORY-KNOWLEDGE-001",
            causal_stop_reason="INTERVENTION_RELEVANT_BOUNDARY",
            connection_pressure_hypothesis=(
                "repeated expert dependence and ad-hoc referral behavior show value already "
                "trying to move from person-bound knowledge toward external users"
            ),
            observed_missing_edge=(
                "rights-cleared packaging, trust, proof and acceptance are not available "
                "as a normal interface between the expert knowledge and external users"
            ),
            latent_connection_hypothesis=(
                "rights-cleared tacit diagnostic knowledge can become a callable bounded "
                "capability for external users when proof and acceptance are standardized"
            ),
            evidence=(
                EvidenceRef("origin", "person-bound knowledge observed", EvidenceKind.ORIGIN_STATE),
                EvidenceRef(
                    "structure",
                    "current work packaging cannot make the capability callable under bounded trust and acceptance rules",
                    EvidenceKind.STRUCTURAL_FRICTION,
                ),
                EvidenceRef("complement", "counterparty state observed", EvidenceKind.COMPLEMENTARY_STATE),
                EvidenceRef(
                    "pressure",
                    "repeated workarounds and referrals show actors already trying to cross the boundary",
                    EvidenceKind.CONNECTION_PRESSURE,
                ),
                EvidenceRef(
                    "barrier",
                    "packaging or rights barrier blocks the observed partial flow",
                    EvidenceKind.MISSING_EDGE,
                ),
            ),
        )
        payload.update(overrides)
        return LatentValueCandidate(**payload)

    def test_complete_latent_value_candidate_can_be_validation_ready(self):
        candidate = self._candidate()
        self.assertEqual(candidate.candidate_class(), CandidateClass.LATENT_VALUE_ACTIVATION)
        self.assertEqual(validate_candidate(candidate), [])
        self.assertEqual(missing_validation_evidence(candidate), [])
        self.assertEqual(discovery_state(candidate), DiscoveryState.VALIDATION_READY)

    def test_state_machine_preserves_latent_and_structural_boundaries(self):
        latent_only = self._candidate(
            structural_friction_hypothesis="",
            structural_friction_truth_state="INFERRED",
            causal_descent=None,
            causal_descent_record_id="",
            causal_stop_reason="",
        )
        self.assertEqual(
            discovery_state(latent_only),
            DiscoveryState.LATENT_VALUE_HYPOTHESIS,
        )

        evidenced_structure = self._candidate(
            complementary_actor_hypothesis="",
        )
        self.assertEqual(
            discovery_state(evidenced_structure),
            DiscoveryState.STRUCTURAL_FRICTION_EVIDENCED,
        )

    def test_persistent_mismatch_can_replace_recent_change(self):
        candidate = self._candidate(
            observed_change="",
            persistent_mismatch=(
                "person-bound knowledge remains structurally hard to call over time"
            ),
        )
        self.assertEqual(validate_candidate(candidate), [])
        self.assertEqual(discovery_state(candidate), DiscoveryState.VALIDATION_READY)

    def test_surface_story_without_evidenced_structural_friction_fails_closed(self):
        candidate = self._candidate(structural_friction_truth_state="INFERRED")
        errors = validate_candidate(candidate)
        self.assertIn("structural_friction_not_evidenced", errors)
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS,
        )

    def test_outer_alternative_summary_is_not_a_substitute_for_causal_competition(self):
        candidate = self._candidate(alternative_explanations=())
        self.assertEqual(validate_candidate(candidate), [])
        self.assertEqual(discovery_state(candidate), DiscoveryState.VALIDATION_READY)

        one_story = self._causal_descent()
        one_story = CausalDescentRecord(
            **{
                **one_story.__dict__,
                "constraint_hypotheses": (one_story.constraint_hypotheses[0],),
            }
        )
        candidate = self._candidate(
            alternative_explanations=(),
            causal_descent=one_story,
        )
        errors = validate_candidate(candidate)
        self.assertIn(
            "causal_descent:missing:competing_causal_explanation",
            errors,
        )
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS,
        )

    def test_one_generic_source_cannot_make_story_validation_ready(self):
        candidate = self._candidate(
            evidence=(EvidenceRef("macro", "industry is changing"),),
        )
        errors = validate_candidate(candidate)
        self.assertIn("missing:evidence_kind:ORIGIN_STATE", errors)
        self.assertIn("missing:evidence_kind:COMPLEMENTARY_STATE", errors)
        self.assertIn("missing:evidence_kind:CONNECTION_PRESSURE", errors)
        self.assertIn("missing:evidence_kind:MISSING_EDGE", errors)
        self.assertEqual(discovery_state(candidate), DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS)

    def test_causal_record_id_alone_is_not_causal_evidence(self):
        candidate = self._candidate(causal_descent=None)
        errors = validate_candidate(candidate)
        self.assertIn("missing:causal_descent", errors)
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS,
        )

    def test_denormalized_causal_summary_cannot_drift_from_lineage(self):
        candidate = self._candidate(
            structural_friction_hypothesis="a different convenient story"
        )
        errors = validate_candidate(candidate)
        self.assertIn("structural_friction_projection_mismatch", errors)

    def test_multi_causal_summary_must_match_full_canonical_frontier(self):
        causal = self._causal_descent()
        second = StructuralConstraintHypothesis(
            **{
                **causal.constraint_hypotheses[1].__dict__,
                "truth_state": CausalTruthState.EVIDENCED_STRUCTURE,
                "support_refs": ("origin",),
                "discriminating_evidence_refs": ("pressure",),
                "intervention_implication": (
                    "test transferability separately from packaging and rights"
                ),
            }
        )
        multi = CausalDescentRecord(
            **{
                **causal.__dict__,
                "constraint_hypotheses": (
                    causal.constraint_hypotheses[0],
                    second,
                ),
                "lead_constraint_ids": ("C-PACKAGING", "C-CONTEXT-SPECIFIC"),
                "stop_reason": CausalStopReason.MULTI_CAUSAL_FRONTIER,
            }
        )
        candidate = self._candidate(causal_descent=multi)
        self.assertIn(
            "structural_friction_projection_mismatch",
            validate_candidate(candidate),
        )

    def test_causal_evidence_refs_must_bind_to_candidate_evidence(self):
        causal = self._causal_descent()
        broken_constraint = StructuralConstraintHypothesis(
            **{
                **causal.constraint_hypotheses[0].__dict__,
                "support_refs": ("source:not-in-packet",),
            }
        )
        causal = CausalDescentRecord(
            **{
                **causal.__dict__,
                "constraint_hypotheses": (
                    broken_constraint,
                    causal.constraint_hypotheses[1],
                ),
            }
        )
        candidate = self._candidate(causal_descent=causal)
        errors = validate_candidate(candidate)
        self.assertIn(
            "causal_descent:unbound_evidence_ref:source:not-in-packet",
            errors,
        )
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS,
        )

    def test_legacy_stranding_barrier_normalizes_to_canonical_missing_edge(self):
        candidate = self._candidate(
            evidence=tuple(
                EvidenceRef(item.source_id, item.claim, (
                    EvidenceKind.STRANDING_BARRIER
                    if item.kind is EvidenceKind.MISSING_EDGE
                    else item.kind
                ))
                for item in self._candidate().evidence
            )
        )
        self.assertEqual(missing_validation_evidence(candidate), [])
        self.assertNotIn("missing:evidence_kind:MISSING_EDGE", validate_candidate(candidate))

    def test_connection_truth_is_required_before_exchange_mechanics(self):
        candidate = self._candidate(
            connection_pressure_hypothesis="",
            observed_missing_edge="",
            latent_connection_hypothesis="",
        )
        errors = validate_candidate(candidate)
        self.assertIn("missing:connection_pressure_hypothesis", errors)
        self.assertIn("missing:observed_missing_edge", errors)
        self.assertIn("missing:latent_connection_hypothesis", errors)
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.COMPLEMENTARITY_HYPOTHESIS,
        )

    def test_exchange_mechanics_can_remain_empty_after_connection_is_evidenced(self):
        candidate = self._candidate(
            transformation_mechanism="",
            why_exchange_does_not_already_happen="",
        )
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.LATENT_CONNECTION_EVIDENCED,
        )
        self.assertIn("missing:transformation_mechanism", validate_candidate(candidate))

    def test_explicit_demand_execution_is_not_core_latent_value_discovery(self):
        candidate = self._candidate(source_mode="EXPLICIT_DEMAND")
        self.assertEqual(candidate.candidate_class(), CandidateClass.EXPLICIT_DEMAND_EXECUTION)
        self.assertIn(
            "explicit_demand_execution_is_not_core_latent_value_discovery",
            validate_candidate(candidate),
        )
        self.assertEqual(discovery_state(candidate), DiscoveryState.LATENT_CONNECTION_EVIDENCED)

    def test_missing_hidden_value_fails_closed(self):
        candidate = self._candidate(hidden_or_underrecognized_value="")
        self.assertIn("missing:hidden_or_underrecognized_value", validate_candidate(candidate))
        self.assertEqual(discovery_state(candidate), DiscoveryState.OBSERVED_PATTERN)

    def test_missing_transformation_mechanism_cannot_be_validation_ready(self):
        candidate = self._candidate(transformation_mechanism="")
        self.assertIn("missing:transformation_mechanism", validate_candidate(candidate))
        self.assertEqual(discovery_state(candidate), DiscoveryState.LATENT_CONNECTION_EVIDENCED)

    def test_dict_guard_rejects_old_supply_demand_record_shape(self):
        record = {
            "candidate_id": "OLD-1",
            "actor": "buyer",
            "observed_state": "has task",
            "observed_change": "deadline approaching",
            "source_mode": "EXPLICIT_DEMAND",
            "evidence": ["rfq"],
        }
        errors = validate_candidate_record(record)
        self.assertIn("missing:hidden_or_underrecognized_value", errors)
        self.assertIn("missing:transformation_mechanism", errors)
        self.assertIn("explicit_demand_execution_is_not_core_latent_value_discovery", errors)
        self.assertIn("missing:evidence_kind:ORIGIN_STATE", errors)


if __name__ == "__main__":
    unittest.main()
