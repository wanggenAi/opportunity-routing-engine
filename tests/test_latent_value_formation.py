import unittest

from src.latent_value_discovery import CandidateClass, validate_candidate
from src.latent_value_formation import (
    ComplementaryWorldNode,
    ContradictionEvidence,
    FormationEvidenceKind,
    FormationEvidenceRef,
    FormationState,
    LatentValueFormationHypothesis,
    formation_state,
    to_latent_value_candidate,
    validate_formation,
)
from src.psychology_tracker import PsychologySnapshot


class LatentValueFormationTests(unittest.TestCase):
    def _psychology_snapshot(
        self,
        primitive="MOTIVE",
        actor_segment="NEW_RETIREES",
        *,
        behavior_corroborated=True,
        money_corroborated=False,
    ):
        supporting = [f"psych:{primitive.lower()}:1"]
        behavior_refs = ()
        money_refs = ()
        if behavior_corroborated:
            behavior_refs = ("psych:behavior:observed",)
            supporting.extend(behavior_refs)
        if money_corroborated:
            money_refs = ("psych:money:observed",)
            supporting.extend(money_refs)
        return PsychologySnapshot(
            geography="CN",
            actor_segment=actor_segment,
            psychology_dimension="POST_RETIREMENT_SELF_DIRECTED_LIFE_REORIENTATION",
            window_days=90,
            signal_count=4,
            source_class_count=2,
            salience_index=62.0,
            momentum="RISING",
            confidence="MEDIUM",
            behavior_corroboration=0.5 if behavior_corroborated else 0.0,
            money_corroboration=0.3 if money_corroborated else 0.0,
            representative_share=None,
            representative_sample_size=None,
            semantic_primitive=primitive,
            supporting_evidence_refs=tuple(supporting),
            behavior_evidence_refs=behavior_refs,
            money_evidence_refs=money_refs,
            representative_evidence_refs=(),
        )

    def _hypothesis(self, **overrides):
        evidence = (
            FormationEvidenceRef(
                "stats:endowment",
                "new retirees have observable time and pension/savings endowments",
                FormationEvidenceKind.OBJECTIVE_ENDOWMENT,
            ),
            FormationEvidenceRef(
                "survey:state",
                "retirement changes daily schedule and work-role structure",
                FormationEvidenceKind.ORIGIN_STATE,
            ),
            FormationEvidenceRef(
                "policy:retirement",
                "a cohort is entering retirement transition",
                FormationEvidenceKind.ORIGIN_CHANGE,
            ),
            FormationEvidenceRef(
                "research:underuse",
                "professional experience and time are not fully converted into bounded new-life or productive uses",
                FormationEvidenceKind.UNDERUSE_MISALIGNMENT,
            ),
            FormationEvidenceRef(
                "behavior:learning-travel",
                "observed learning, travel, social and continued-contribution behavior follows the transition",
                FormationEvidenceKind.OBSERVED_BEHAVIOR,
            ),
            FormationEvidenceRef(
                "labor:youth",
                "younger digital-capability group has execution capacity and weak access to trusted paid work",
                FormationEvidenceKind.COMPLEMENTARY_NODE,
            ),
            FormationEvidenceRef(
                "field:informal-crossgen",
                "synthetic test evidence: repeated informal cross-generation help already approximates the proposed relationship",
                FormationEvidenceKind.CONNECTION_PRESSURE,
            ),
            FormationEvidenceRef(
                "field:trust-packaging",
                "trust, packaging, role definition and acceptance prevent direct exchange",
                FormationEvidenceKind.STRANDING_BARRIER,
            ),
        )
        payload = dict(
            candidate_id="LVF-RETIREMENT-001",
            actor_segment="NEW_RETIREES",
            geography="CN",
            objective_endowments=(
                "discretionary time",
                "pension/savings for some segments",
                "professional and life experience",
            ),
            observed_state="work-defined daily structure is being replaced by self-directed time",
            observed_change="retirement transition changes time, identity, social and spending context",
            underused_or_misaligned_value="time, experience and purchasing power are not fully converted into valued post-retirement outcomes",
            resource_psychology_disequilibrium="objective time/experience endowments rise while actors seek autonomy, relevance and modern-life connection without a trusted route",
            observed_behavior="learning, travel, interest groups, digital-tool adoption and selective continued work appear as adaptation behaviors",
            latent_outcome_hypothesis="a bounded way to turn post-retirement time/experience into chosen modern-life or productive outcomes",
            complementary_nodes=(
                ComplementaryWorldNode(
                    node_id="YOUNG_DIGITAL_EXECUTION_POOL",
                    node_type="GROUP",
                    observed_state="digital/AI execution capacity exists while trusted paid access is weak",
                    contribution_hypothesis="provide bounded digital execution under explicit acceptance and trust rules",
                    controller_or_owner="participants themselves",
                    evidence_refs=("labor:youth",),
                ),
                ComplementaryWorldNode(
                    node_id="TRUSTED_COMMUNITY_CHANNEL",
                    node_type="CHANNEL / TRUST RELATIONSHIP",
                    observed_state="community or institutional channels can lower stranger-to-stranger trust cost",
                    contribution_hypothesis="provide legitimate discovery, trust and bounded participation rails",
                    controller_or_owner="channel operator",
                    evidence_refs=("field:trust-packaging",),
                ),
            ),
            counterfactual_exchange_design="package a chosen outcome into bounded roles where retirees contribute money/time/experience, external digital executors provide defined work, and a trusted channel governs identity, scope, acceptance and settlement",
            why_exchange_does_not_already_happen="resources are not packaged into callable units and trust, discovery, acceptance and incentive interfaces are missing",
            incremental_value_for_origin_actor="more useful and self-directed post-retirement outcomes without returning to full-time employment",
            incremental_value_for_complementary_nodes="paid utilization, portfolio evidence and trusted access for external execution nodes",
            orchestrator_value_capture_hypothesis="fee only if the orchestrator materially reduces search, packaging, trust, coordination and acceptance cost",
            cheapest_decisive_validation="test one narrowly defined outcome with a small segment and real opt-in behavior before claiming demand",
            kill_conditions="no repeated behavior, no participant surplus, no willingness to make a real commitment, or trust/coordination cost consumes the value",
            psychology_snapshots=(self._psychology_snapshot(),),
            evidence=evidence,
            contradictions=(),
        )
        payload.update(overrides)
        return LatentValueFormationHypothesis(**payload)

    def test_complete_connection_evidenced_formation_can_be_validation_ready(self):
        hypothesis = self._hypothesis()
        self.assertEqual(validate_formation(hypothesis), [])
        self.assertEqual(formation_state(hypothesis), FormationState.VALIDATION_READY)

        candidate = to_latent_value_candidate(hypothesis)
        self.assertEqual(candidate.candidate_class(), CandidateClass.LATENT_VALUE_ACTIVATION)
        self.assertEqual(candidate.source_mode, "LATENT_VALUE_DISCOVERY")
        self.assertEqual(validate_candidate(candidate), [])

    def test_complementarity_and_exchange_design_without_connection_pressure_cannot_promote(self):
        hypothesis = self._hypothesis(
            evidence=tuple(
                item
                for item in self._hypothesis().evidence
                if item.kind is not FormationEvidenceKind.CONNECTION_PRESSURE
            )
        )
        errors = validate_formation(hypothesis)
        self.assertIn("missing:evidence_kind:CONNECTION_PRESSURE", errors)
        self.assertEqual(
            formation_state(hypothesis), FormationState.COMPLEMENTARITY_HYPOTHESIS
        )
        with self.assertRaisesRegex(ValueError, "VALIDATION_READY"):
            to_latent_value_candidate(hypothesis)

    def test_psychology_alone_cannot_manufacture_latent_value(self):
        hypothesis = self._hypothesis(
            objective_endowments=(),
            evidence=(
                FormationEvidenceRef(
                    "social:posts",
                    "retirement discussion is salient",
                    FormationEvidenceKind.GENERAL_CONTEXT,
                ),
            ),
        )
        errors = validate_formation(hypothesis)
        self.assertIn("missing:objective_endowments", errors)
        self.assertIn("missing:evidence_kind:OBJECTIVE_ENDOWMENT", errors)
        self.assertEqual(formation_state(hypothesis), FormationState.OBSERVED_TRANSITION)
        with self.assertRaisesRegex(ValueError, "VALIDATION_READY"):
            to_latent_value_candidate(hypothesis)

    def test_psychology_signal_is_not_paid_demand(self):
        hypothesis = self._hypothesis()
        candidate = to_latent_value_candidate(hypothesis)
        self.assertEqual(candidate.source_mode, "LATENT_VALUE_DISCOVERY")
        self.assertNotEqual(candidate.source_mode, "EXPLICIT_DEMAND")
        self.assertNotIn("payer", candidate.__dataclass_fields__)
        self.assertNotIn("payment_evidence", candidate.__dataclass_fields__)

    def test_behavior_corroboration_is_required_before_validation_ready(self):
        snapshot = self._psychology_snapshot(behavior_corroborated=False)
        hypothesis = self._hypothesis(psychology_snapshots=(snapshot,))
        self.assertIn(
            "missing:psychology_behavior_corroboration",
            validate_formation(hypothesis),
        )
        self.assertEqual(
            formation_state(hypothesis),
            FormationState.RESOURCE_PSYCHOLOGY_MISALIGNMENT_HYPOTHESIS,
        )

    def test_heterogeneous_nonhuman_nodes_are_first_class(self):
        hypothesis = self._hypothesis(
            complementary_nodes=(
                ComplementaryWorldNode(
                    node_id="IDLE_WEEKDAY_SPACE",
                    node_type="SPACE / PHYSICAL ASSET",
                    observed_state="measured weekday space is underused",
                    contribution_hypothesis="host a bounded activity if permission and economics clear",
                    controller_or_owner="venue operator",
                    evidence_refs=("space:utilization",),
                ),
                ComplementaryWorldNode(
                    node_id="BOOKING_SOFTWARE",
                    node_type="SOFTWARE / API",
                    observed_state="booking and payment capability exists",
                    contribution_hypothesis="reduce scheduling and settlement coordination",
                    controller_or_owner="software provider",
                    evidence_refs=("software:capability",),
                ),
            )
        )
        self.assertEqual(validate_formation(hypothesis), [])
        candidate = to_latent_value_candidate(hypothesis)
        self.assertIn("SPACE / PHYSICAL ASSET", candidate.complementary_actor_hypothesis)
        self.assertIn("SOFTWARE / API", candidate.complementary_actor_hypothesis)

    def test_material_contradiction_blocks_validation_promotion(self):
        hypothesis = self._hypothesis(
            contradictions=(
                ContradictionEvidence(
                    "counter:behavior",
                    "bounded evidence shows the proposed outcome is already solved cheaply",
                    material=True,
                    resolved=False,
                ),
            )
        )
        self.assertIn("unresolved_material_contradiction", validate_formation(hypothesis))
        self.assertEqual(
            formation_state(hypothesis), FormationState.COMPLEMENTARITY_HYPOTHESIS
        )

    def test_resolved_contradiction_is_preserved_but_does_not_block(self):
        hypothesis = self._hypothesis(
            contradictions=(
                ContradictionEvidence(
                    "counter:segment",
                    "one adjacent segment behaves differently",
                    material=True,
                    resolved=True,
                ),
            )
        )
        self.assertEqual(validate_formation(hypothesis), [])
        self.assertEqual(formation_state(hypothesis), FormationState.VALIDATION_READY)

    def test_psychology_must_refer_to_same_actor_segment(self):
        hypothesis = self._hypothesis(
            psychology_snapshots=(
                self._psychology_snapshot(actor_segment="UNEMPLOYED_GRADUATES"),
            )
        )
        errors = validate_formation(hypothesis)
        self.assertIn("missing:psychology_evidence", errors)
        self.assertIn(
            "psychology_actor_segment_mismatch:UNEMPLOYED_GRADUATES", errors
        )
        self.assertEqual(formation_state(hypothesis), FormationState.OBSERVED_TRANSITION)

    def test_money_evidence_is_not_required_to_form_hypothesis(self):
        hypothesis = self._hypothesis()
        self.assertEqual(
            hypothesis.psychology_snapshots[0].money_evidence_refs,
            (),
        )
        self.assertEqual(formation_state(hypothesis), FormationState.VALIDATION_READY)
        candidate = to_latent_value_candidate(hypothesis)
        self.assertEqual(candidate.candidate_class(), CandidateClass.LATENT_VALUE_ACTIVATION)


if __name__ == "__main__":
    unittest.main()
