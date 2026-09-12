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
            backing_leverage="formal institution provides legitimate entry context",
            counterparty_reason_to_engage="a real commercialization or project route is relevant to the institution's mandate",
            counterparty_visible_surplus="the institution can realize an authorized technology-transfer / funded-validation outcome",
            surplus_realization_mechanism="an enterprise-side opportunity is routed through the institution into an authorized pilot or transfer process",
            institutional_cover_or_referral="formal technology-transfer center route",
            status_trust_friction="counterpart protects scarce time, reputation and institutional boundaries",
            operator_credibility_assets="evidenced professional history, technical literacy, systems analysis and mature communication",
            missing_credibility="",
            operator_commitment="absorb initial research/coordination cost and keep the first ask bounded",
            counterparty_commitment_requested="confirm whether the opportunity belongs in the formal channel and nominate the correct next contact",
            founder_identity_dependency="low after institutional route and economic structure are accepted",
            first_value_packet="optional supporting notes; not the reason to engage",
            counterparty_downside="time and reputation risk if the opportunity is vague or commercially empty",
            cultural_context_notes="local status/face sensitivity is an operator-supplied field prior to validate, not a universal stereotype",
            evidence=(AccessEvidence("official-window", "institution publishes a formal external cooperation route"),),
        )
        payload.update(overrides)
        return AccessFeasibility(**payload)

    def test_legitimate_window_and_visible_surplus_can_be_ready(self):
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
            backing_leverage="none",
            counterparty_reason_to_engage="",
            counterparty_visible_surplus="",
        )
        self.assertEqual(access_state(record), AccessState.ACCESS_BLOCKED)
        errors = validate_access(record)
        self.assertIn("missing:counterparty_reason_to_engage", errors)
        self.assertIn("missing:counterparty_visible_surplus", errors)

    def test_ppt_or_analysis_is_not_counterparty_surplus(self):
        for weak in ("ppt", "analysis", "分析", "认知"):
            record = self._record(counterparty_visible_surplus=weak)
            self.assertIn("non_economic_or_non_concrete_surplus", validate_access(record))

    def test_first_value_packet_is_not_a_hard_gate(self):
        record = self._record(first_value_packet="")
        self.assertNotIn("missing:first_value_packet", validate_access(record))

    def test_access_blocked_does_not_mutate_value_truth(self):
        record = self._record(legitimate_entry_path="")
        self.assertEqual(access_state(record), AccessState.ACCESS_BLOCKED)
        self.assertEqual(record.candidate_id, "LV-XZ-TEST")

    def test_vague_social_ask_is_rejected(self):
        record = self._record(counterparty_commitment_requested="合作")
        self.assertIn("unbounded_counterparty_ask", validate_access(record))

    def test_local_culture_is_context_not_universal_truth(self):
        record = self._record()
        self.assertIn("field prior", record.cultural_context_notes.lower())


if __name__ == "__main__":
    unittest.main()
