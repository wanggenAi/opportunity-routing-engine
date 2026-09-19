import unittest

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

    def test_surface_story_without_evidenced_structural_friction_fails_closed(self):
        candidate = self._candidate(structural_friction_truth_state="INFERRED")
        errors = validate_candidate(candidate)
        self.assertIn("structural_friction_not_evidenced", errors)
        self.assertEqual(
            discovery_state(candidate),
            DiscoveryState.STRUCTURAL_FRICTION_HYPOTHESIS,
        )

    def test_structural_friction_needs_alternative_explanations(self):
        candidate = self._candidate(alternative_explanations=())
        errors = validate_candidate(candidate)
        self.assertIn("missing:alternative_explanations", errors)
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
