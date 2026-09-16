import unittest

from src.missing_edge_gate import (
    ExistingExchangeRoute,
    FieldAccessProfile,
    FieldAccessState,
    MissingEdgeAssessment,
    MissingEdgeCounterevidence,
    MissingEdgeEvidence,
    MissingEdgeState,
    field_access_state,
    field_validation_allowed,
    missing_edge_state,
    p0_access_priority_allowed,
    p0_field_validation_allowed,
    validate_field_access,
    validate_missing_edge,
)


class MissingEdgeGateTests(unittest.TestCase):
    def _assessment(self, **overrides):
        payload = dict(
            candidate_id="ME-001",
            actor_segment="INDEPENDENT_INDUSTRIAL_SERVICE_ACTORS",
            geography="CN-JS-XZ",
            target_outcome=(
                "turn rights-cleared maintenance/failure traces into reusable industrial-AI "
                "training/evaluation assets without exposing customer or employer secrets"
            ),
            existing_exchange_search_scope=(
                "searched OEM high-quality-dataset projects, expert-data vendors, industrial "
                "dataset platforms and aftermarket digital-service routes"
            ),
            existing_exchange_search_evidence=(
                MissingEdgeEvidence(
                    "official:oem-dataset",
                    "OEM-led engineering-machinery vehicle-network datasets already organize first-party data for AI use",
                ),
                MissingEdgeEvidence(
                    "market:expert-data-vendor",
                    "commercial expert-data vendors already package domain experts for dataset production and evaluation",
                ),
            ),
            existing_routes=(
                ExistingExchangeRoute(
                    route_id="OEM_DATASET_ROUTE",
                    observed_exchange="OEM/platform + first-party telemetry + university support -> high-quality industrial dataset",
                    target_actor_outcome_fit="strong for OEM-owned telemetry, weak for fragmented non-OEM service traces",
                    evidence_refs=("official:oem-dataset",),
                    observed_limitation="does not prove lawful aggregation of independent service-shop repair traces",
                    adequately_solves_target=False,
                ),
                ExistingExchangeRoute(
                    route_id="EXPERT_DATA_VENDOR_ROUTE",
                    observed_exchange="AI buyer + expert network + annotation workflow -> expert-grade training/evaluation data",
                    target_actor_outcome_fit="strong for callable experts, but not proof of access to fragmented field-maintenance records",
                    evidence_refs=("market:expert-data-vendor",),
                    observed_limitation="expert availability alone does not create rights-cleared local failure traces",
                    adequately_solves_target=False,
                ),
            ),
            structural_failure_evidence=(
                MissingEdgeEvidence(
                    "official:manufacturing-ai-gap",
                    "manufacturing AI still reports data barriers, weak interoperability and low data utilization",
                ),
            ),
            missing_edge_hypothesis=(
                "a governed interface for small independent service actors to contribute narrow, "
                "rights-cleared fault/repair traces plus expert adjudication into reusable AI assets"
            ),
            why_market_has_not_already_solved_it=(
                "record ownership, confidentiality, inconsistent schemas, sparse labels and the cost "
                "of expert adjudication make cross-actor aggregation uneconomic without a governance layer"
            ),
            orchestrator_unique_contribution=(
                "define rights boundary, minimum record schema, expert adjudication contract, quality gate, "
                "allowed use and settlement; not merely introduce experts or sell contacts"
            ),
            cheapest_decisive_validation=(
                "inspect record schemas and rights boundaries at 5 independent service/rental actors without copying data, "
                "then test one AI/dataset buyer for incremental value of the exact available fields"
            ),
            kill_conditions=(
                "kill if records do not exist, rights cannot be cleared, existing OEM/platform routes already cover them, "
                "schemas are non-comparable, or no buyer values the resulting evidence"
            ),
            counterevidence=(),
        )
        payload.update(overrides)
        return MissingEdgeAssessment(**payload)

    def _access_profile(self, **overrides):
        payload = dict(
            candidate_id="ME-001",
            actor_segment="NEW_RETIREES_AND_UNIVERSITY_STUDENTS",
            first_probe_description=(
                "observe resource/state-change/behavior patterns through ordinary opt-in conversations "
                "before proposing any product or asking for private records"
            ),
            access_evidence=(
                MissingEdgeEvidence(
                    "official:older-adult-ai-course",
                    "older-adult AI learning programs expose a reachable public learning context",
                ),
                MissingEdgeEvidence(
                    "official:student-opc-camp",
                    "local university entrepreneurship programs expose a reachable student execution context",
                ),
            ),
            reachable_actor_class=True,
            observable_without_proprietary_access=True,
            requires_enterprise_procurement=False,
            requires_proprietary_data=False,
            requires_large_capital=False,
            requires_sensitive_personal_data=False,
            requires_preexisting_contract=False,
            intermediary_required=False,
            notes="P0 access test only; no individual consent is implied by public reachability evidence.",
        )
        payload.update(overrides)
        return FieldAccessProfile(**payload)

    def test_complete_missing_edge_can_be_validation_ready(self):
        assessment = self._assessment()
        self.assertEqual(validate_missing_edge(assessment), [])
        self.assertEqual(missing_edge_state(assessment), MissingEdgeState.VALIDATION_READY)
        self.assertTrue(field_validation_allowed(assessment))

    def test_complementarity_without_exchange_search_cannot_promote(self):
        assessment = self._assessment(
            existing_exchange_search_evidence=(),
            existing_routes=(),
        )
        errors = validate_missing_edge(assessment)
        self.assertIn("missing:existing_exchange_search_evidence", errors)
        self.assertEqual(
            missing_edge_state(assessment),
            MissingEdgeState.EXISTING_EXCHANGE_SEARCH_REQUIRED,
        )
        self.assertFalse(field_validation_allowed(assessment))

    def test_one_search_source_is_not_enough(self):
        assessment = self._assessment(
            existing_exchange_search_evidence=(
                MissingEdgeEvidence("single:source", "one market scan"),
            )
        )
        self.assertIn(
            "insufficient:existing_exchange_search_independence",
            validate_missing_edge(assessment),
        )
        self.assertEqual(
            missing_edge_state(assessment),
            MissingEdgeState.EXISTING_EXCHANGE_SEARCH_REQUIRED,
        )

    def test_adequate_existing_route_closes_candidate(self):
        closed_route = ExistingExchangeRoute(
            route_id="ALREADY_SOLVED",
            observed_exchange="existing route already provides the same actor/outcome interface",
            target_actor_outcome_fit="same actor, same outcome, same geography and acceptable economics",
            evidence_refs=("market:closed",),
            observed_limitation="none material",
            adequately_solves_target=True,
        )
        assessment = self._assessment(existing_routes=(closed_route,))
        self.assertIn("market_already_closed", validate_missing_edge(assessment))
        self.assertEqual(missing_edge_state(assessment), MissingEdgeState.MARKET_ALREADY_CLOSED)
        self.assertFalse(field_validation_allowed(assessment))

    def test_missing_failure_evidence_blocks_story_based_gap(self):
        assessment = self._assessment(structural_failure_evidence=())
        self.assertIn("missing:structural_failure_evidence", validate_missing_edge(assessment))
        self.assertEqual(
            missing_edge_state(assessment),
            MissingEdgeState.STRUCTURAL_FAILURE_EVIDENCE_REQUIRED,
        )

    def test_unresolved_counterevidence_blocks_validation_ready(self):
        assessment = self._assessment(
            counterevidence=(
                MissingEdgeCounterevidence(
                    "counter:existing-platform",
                    "a current platform may already aggregate the same traces with acceptable economics",
                    material=True,
                    resolved=False,
                ),
            )
        )
        self.assertIn("unresolved_material_counterevidence", validate_missing_edge(assessment))
        self.assertEqual(
            missing_edge_state(assessment),
            MissingEdgeState.MISSING_EDGE_HYPOTHESIS,
        )
        self.assertFalse(field_validation_allowed(assessment))

    def test_direct_human_actor_probe_is_p0_accessible(self):
        profile = self._access_profile()
        self.assertEqual(validate_field_access(profile), [])
        self.assertEqual(field_access_state(profile), FieldAccessState.DIRECTLY_TESTABLE)
        self.assertTrue(p0_access_priority_allowed(profile))

    def test_mediated_actor_probe_can_still_be_p0_accessible(self):
        profile = self._access_profile(intermediary_required=True)
        self.assertEqual(field_access_state(profile), FieldAccessState.MEDIATED_TESTABLE)
        self.assertTrue(p0_access_priority_allowed(profile))

    def test_enterprise_procurement_or_proprietary_data_defers_p0(self):
        profile = self._access_profile(
            requires_enterprise_procurement=True,
            requires_proprietary_data=True,
        )
        self.assertEqual(field_access_state(profile), FieldAccessState.HIGH_FRICTION_DEFER)
        self.assertFalse(p0_access_priority_allowed(profile))

    def test_missing_access_evidence_is_fail_closed(self):
        profile = self._access_profile(access_evidence=())
        self.assertIn("missing:field_access_evidence", validate_field_access(profile))
        self.assertEqual(field_access_state(profile), FieldAccessState.ACCESS_EVIDENCE_REQUIRED)
        self.assertFalse(p0_access_priority_allowed(profile))

    def test_combined_p0_gate_requires_same_candidate_and_truth(self):
        assessment = self._assessment()
        profile = self._access_profile()
        self.assertTrue(p0_field_validation_allowed(assessment, profile))
        mismatch = self._access_profile(candidate_id="OTHER")
        self.assertFalse(p0_field_validation_allowed(assessment, mismatch))


if __name__ == "__main__":
    unittest.main()
