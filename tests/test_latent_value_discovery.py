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
            evidence=(
                EvidenceRef("origin", "person-bound knowledge observed", EvidenceKind.ORIGIN_STATE),
                EvidenceRef("complement", "counterparty state observed", EvidenceKind.COMPLEMENTARY_STATE),
                EvidenceRef("barrier", "packaging or rights barrier observed", EvidenceKind.STRANDING_BARRIER),
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

    def test_one_generic_source_cannot_make_story_validation_ready(self):
        candidate = self._candidate(
            evidence=(EvidenceRef("macro", "industry is changing"),),
        )
        errors = validate_candidate(candidate)
        self.assertIn("missing:evidence_kind:ORIGIN_STATE", errors)
        self.assertIn("missing:evidence_kind:COMPLEMENTARY_STATE", errors)
        self.assertIn("missing:evidence_kind:STRANDING_BARRIER", errors)
        self.assertEqual(discovery_state(candidate), DiscoveryState.COMPLEMENTARITY_HYPOTHESIS)

    def test_explicit_demand_execution_is_not_core_latent_value_discovery(self):
        candidate = self._candidate(source_mode="EXPLICIT_DEMAND")
        self.assertEqual(candidate.candidate_class(), CandidateClass.EXPLICIT_DEMAND_EXECUTION)
        self.assertIn(
            "explicit_demand_execution_is_not_core_latent_value_discovery",
            validate_candidate(candidate),
        )
        self.assertEqual(discovery_state(candidate), DiscoveryState.COMPLEMENTARITY_HYPOTHESIS)

    def test_missing_hidden_value_fails_closed(self):
        candidate = self._candidate(hidden_or_underrecognized_value="")
        self.assertIn("missing:hidden_or_underrecognized_value", validate_candidate(candidate))
        self.assertEqual(discovery_state(candidate), DiscoveryState.OBSERVED_PATTERN)

    def test_missing_transformation_mechanism_cannot_be_validation_ready(self):
        candidate = self._candidate(transformation_mechanism="")
        self.assertIn("missing:transformation_mechanism", validate_candidate(candidate))
        self.assertEqual(discovery_state(candidate), DiscoveryState.LATENT_VALUE_HYPOTHESIS)

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
