import unittest

from src.causal_descent import (
    CausalDescentRecord,
    CausalDescentState,
    CausalStopReason,
    CausalTruthState,
    LatentOutcomeHypothesis,
    StructuralConstraintHypothesis,
    causal_descent_state,
    validate_causal_descent,
    validate_causal_descent_for_promotion,
)


class CausalDescentTests(unittest.TestCase):
    def _record(self, **overrides):
        outcome = LatentOutcomeHypothesis(
            outcome_id="OUTCOME-1",
            statement=(
                "convert bounded time and capability into accepted economic and "
                "developmental outcomes without requiring a full-time employment package"
            ),
            truth_state=CausalTruthState.EVIDENCED_STRUCTURE,
            evidence_refs=("behavior:applications", "behavior:task-seeking"),
            falsifiers=(
                "the segment consistently prefers only formal full-time employment",
            ),
        )
        constraints = (
            StructuralConstraintHypothesis(
                constraint_id="C1",
                outcome_id="OUTCOME-1",
                depth=1,
                causal_claim=(
                    "available work is packaged mainly as whole jobs/projects rather "
                    "than small trusted capability units"
                ),
                mechanism=(
                    "capability cannot become legible, trusted, accepted and settled "
                    "cheaply at a smaller unit of exchange"
                ),
                truth_state=CausalTruthState.EVIDENCED_STRUCTURE,
                support_refs=("market:job-packaging", "behavior:workaround"),
                discriminating_evidence_refs=("comparison:task-vs-job",),
                falsifiers=(
                    "small capability units already clear cheaply with comparable trust",
                ),
                intervention_implication="make capability callable as bounded units",
            ),
            StructuralConstraintHypothesis(
                constraint_id="C2",
                outcome_id="OUTCOME-1",
                depth=1,
                causal_claim=(
                    "the apparent difficulty may instead be caused mainly by insufficient "
                    "skill quality or weak local demand"
                ),
                mechanism="low willingness to pay would persist even if packaging friction disappeared",
                truth_state=CausalTruthState.INFERRED,
                support_refs=("counter:skill-demand",),
                falsifiers=("qualified actors clear bounded paid tasks when trust is supplied",),
            ),
        )
        payload = dict(
            record_id="CD-001",
            actor="UNIVERSITY_STUDENTS",
            current_state="time and basic capability exist but monetization is irregular",
            surface_phenomenon="repeated job/part-time search with poor fit",
            surface_evidence_refs=("behavior:applications",),
            outcome_hypotheses=(outcome,),
            selected_outcome_id="OUTCOME-1",
            outcome_selection_rationale=(
                "observed choices and sacrifices fit this product-agnostic state "
                "transition better than the nearby alternative explanations"
            ),
            constraint_hypotheses=constraints,
            lead_constraint_ids=("C1",),
            stop_reason=CausalStopReason.INTERVENTION_RELEVANT_BOUNDARY,
            stop_rationale=(
                "the current causal frontier is already specific enough to change "
                "which interface or capability must be tested next"
            ),
            decisive_unknown="",
            probe_eligible=False,
        )
        payload.update(overrides)
        return CausalDescentRecord(**payload)

    def test_evidenced_record_reaches_structural_friction_state(self):
        record = self._record()
        self.assertEqual(validate_causal_descent(record), [])
        self.assertEqual(validate_causal_descent_for_promotion(record), [])
        self.assertEqual(
            causal_descent_state(record),
            CausalDescentState.EVIDENCED_STRUCTURAL_FRICTION,
        )

    def test_one_plausible_story_is_not_enough_for_promotion(self):
        record = self._record(
            constraint_hypotheses=(self._record().constraint_hypotheses[0],)
        )
        self.assertIn(
            "missing:competing_causal_explanation",
            validate_causal_descent_for_promotion(record),
        )

    def test_inferred_lead_can_be_decisive_unknown_without_becoming_truth(self):
        inferred = StructuralConstraintHypothesis(
            constraint_id="C1",
            outcome_id="OUTCOME-1",
            depth=1,
            causal_claim="trust/acceptance packaging may be the governing constraint",
            mechanism="actors cannot cheaply verify or accept bounded capability",
            truth_state=CausalTruthState.INFERRED,
            support_refs=("behavior:workaround",),
            falsifiers=("trusted bounded tasks still fail to clear",),
        )
        record = self._record(
            constraint_hypotheses=(
                inferred,
                self._record().constraint_hypotheses[1],
            ),
            lead_constraint_ids=("C1",),
            stop_reason=None,
            probe_eligible=True,
            decisive_unknown="whether trusted bounded task offers clear when exposed",
        )
        self.assertEqual(
            causal_descent_state(record),
            CausalDescentState.DECISIVE_UNKNOWN,
        )
        self.assertIn(
            "causal_descent_not_evidenced",
            validate_causal_descent_for_promotion(record),
        )

    def test_deeper_child_must_really_be_deeper_than_parent(self):
        child = StructuralConstraintHypothesis(
            constraint_id="C3",
            outcome_id="OUTCOME-1",
            depth=1,
            parent_constraint_id="C1",
            causal_claim="a deeper packaging mechanism",
            mechanism="same-depth child is invalid",
        )
        record = self._record(
            constraint_hypotheses=self._record().constraint_hypotheses + (child,)
        )
        self.assertIn(
            "constraint_depth_not_deeper_than_parent:C3",
            validate_causal_descent(record),
        )

    def test_evidenced_claim_requires_falsifier_and_discriminating_evidence(self):
        broken = StructuralConstraintHypothesis(
            constraint_id="C1",
            outcome_id="OUTCOME-1",
            depth=1,
            causal_claim="packaging is the constraint",
            mechanism="capability units are not callable",
            truth_state=CausalTruthState.EVIDENCED_STRUCTURE,
            support_refs=("support:1",),
        )
        record = self._record(
            constraint_hypotheses=(
                broken,
                self._record().constraint_hypotheses[1],
            )
        )
        errors = validate_causal_descent(record)
        self.assertIn("missing:discriminating_evidence:C1", errors)
        self.assertIn("missing:constraint_falsifiers:C1", errors)

    def test_persisted_round_trip_preserves_causal_lineage(self):
        from src.causal_descent import causal_descent_from_mapping

        record = self._record()
        restored = causal_descent_from_mapping(record.as_dict())
        self.assertEqual(restored, record)
        self.assertEqual(validate_causal_descent_for_promotion(restored), [])

    def test_evidence_limit_cannot_promote_even_when_current_frontier_is_supported(self):
        record = self._record(stop_reason=CausalStopReason.EVIDENCE_LIMIT_REACHED)
        self.assertEqual(
            causal_descent_state(record),
            CausalDescentState.CAUSAL_HYPOTHESIS_SET,
        )
        errors = validate_causal_descent_for_promotion(record)
        self.assertIn("causal_evidence_limit_reached", errors)
        self.assertIn("causal_descent_not_evidenced", errors)

    def test_multi_causal_stop_requires_multiple_evidenced_leads(self):
        record = self._record(stop_reason=CausalStopReason.MULTI_CAUSAL_FRONTIER)
        self.assertIn(
            "multi_causal_frontier_requires_multiple_lead_constraints",
            validate_causal_descent(record),
        )
        self.assertEqual(
            causal_descent_state(record),
            CausalDescentState.CAUSAL_HYPOTHESIS_SET,
        )

    def test_selected_outcome_and_stop_reason_require_rationales(self):
        record = self._record(outcome_selection_rationale="")
        self.assertIn(
            "selected_outcome_requires_rationale",
            validate_causal_descent(record),
        )

        record = self._record(stop_rationale="")
        errors = validate_causal_descent(record)
        self.assertIn("stop_reason_requires_rationale", errors)
        self.assertIn(
            "missing:causal_stop_rationale",
            validate_causal_descent_for_promotion(record),
        )

    def test_intervention_stop_requires_actionable_implication(self):
        causal = self._record()
        broken_lead = StructuralConstraintHypothesis(
            **{
                **causal.constraint_hypotheses[0].__dict__,
                "intervention_implication": "",
            }
        )
        record = self._record(
            constraint_hypotheses=(
                broken_lead,
                causal.constraint_hypotheses[1],
            )
        )
        self.assertIn(
            "intervention_boundary_requires_implication:C1",
            validate_causal_descent(record),
        )

    def test_stop_reason_is_part_of_deep_causal_discipline(self):
        record = self._record(stop_reason=None)
        self.assertEqual(
            causal_descent_state(record),
            CausalDescentState.CAUSAL_HYPOTHESIS_SET,
        )
        self.assertIn(
            "missing:causal_stop_reason",
            validate_causal_descent_for_promotion(record),
        )


if __name__ == "__main__":
    unittest.main()
