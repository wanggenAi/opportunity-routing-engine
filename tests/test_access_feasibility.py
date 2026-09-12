import unittest

from src.access_feasibility import (
    AccessEvidence,
    AccessFeasibility,
    AccessRouteKind,
    AccessState,
    OperatorCapabilityEnvelope,
    OperatorFitState,
    access_state,
    operator_fit_state,
    validate_access,
)


class AccessFeasibilityTests(unittest.TestCase):
    def _record(self, **overrides):
        payload = dict(
            candidate_id="LV-XZ-TEST",
            target_actor="high-trust expert or institution",
            route_kind=AccessRouteKind.PUBLIC_INSTITUTIONAL_WINDOW,
            legitimate_entry_path="formal public technology-transfer window",
            counterparty_reason_to_engage="operator brings a bounded evidence-backed problem packet relevant to the institution's mandate",
            first_value_packet="one-page problem/asset map with evidence, unknowns and a reversible validation request",
            institutional_cover_or_referral="formal technology-transfer center route",
            status_trust_friction="counterpart protects scarce time, reputation and institutional boundaries",
            operator_credibility_assets="evidenced professional history, technical literacy, systems analysis and mature communication",
            missing_credibility="",
            operator_commitment="prepare the evidence packet and absorb initial research/coordination cost",
            counterparty_commitment_requested="confirm whether the packet belongs in the formal channel and nominate the correct next contact",
            founder_identity_dependency="low after institutional route and packet are accepted",
            cultural_context_notes="local status/face sensitivity is a hypothesis to test, not a stereotype",
            evidence=(AccessEvidence("official-window", "institution publishes a formal external cooperation route"),),
        )
        payload.update(overrides)
        return AccessFeasibility(**payload)

    def test_legitimate_window_and_bounded_value_packet_can_be_ready(self):
        record = self._record()
        self.assertEqual(validate_access(record), [])
        self.assertEqual(access_state(record), AccessState.VALIDATION_ACCESS_READY)

    def test_multi_year_real_work_history_counts_as_contextual_credibility(self):
        profile = OperatorCapabilityEnvelope(
            professional_years=8,
            proven_domains=("enterprise IT", "systems delivery"),
            accepted_delivery_contexts=("multi-company project work",),
            education_training=("engineering degree",),
            cross_context_experience=("cross-city", "international study"),
            communication_trust_assets=("mature stakeholder communication",),
            local_knowledge=("home-city context",),
        )
        self.assertEqual(
            operator_fit_state(profile),
            OperatorFitState.STRONG_CONTEXTUAL_CREDIBILITY,
        )

    def test_operator_history_is_credibility_but_not_entitlement(self):
        record = self._record(
            route_kind=AccessRouteKind.DIRECT_COLD,
            institutional_cover_or_referral="",
            first_value_packet="",
            counterparty_reason_to_engage="",
        )
        self.assertEqual(access_state(record), AccessState.ACCESS_BLOCKED)
        errors = validate_access(record)
        self.assertIn("missing:counterparty_reason_to_engage", errors)
        self.assertIn("missing:first_value_packet", errors)

    def test_access_blocked_does_not_mutate_value_truth(self):
        record = self._record(legitimate_entry_path="")
        self.assertEqual(access_state(record), AccessState.ACCESS_BLOCKED)
        self.assertEqual(record.candidate_id, "LV-XZ-TEST")

    def test_vague_social_ask_is_rejected(self):
        record = self._record(counterparty_commitment_requested="合作")
        self.assertIn("unbounded_counterparty_ask", validate_access(record))

    def test_local_culture_is_context_not_universal_truth(self):
        record = self._record()
        self.assertIn("hypothesis", record.cultural_context_notes.lower())


if __name__ == "__main__":
    unittest.main()
