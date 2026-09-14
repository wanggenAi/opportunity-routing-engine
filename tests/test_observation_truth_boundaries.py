import unittest
from pathlib import Path

from src.emergent_taxonomy import assess_emergent_concept
from src.semantic_kernel import SemanticObservation


ROOT = Path(__file__).resolve().parents[1]


class ObservationTruthBoundaryTests(unittest.TestCase):
    def test_inferred_claims_cannot_self_promote_emergent_taxonomy(self):
        concept = "inferred.only.friction"
        observations = tuple(
            SemanticObservation(
                observation_id=f"inferred-{index}",
                primitive="FRICTION",
                concept=concept,
                source_id=f"source-{index}",
                observed_at=f"2026-09-{index:02d}T10:00:00+08:00",
                evidence_refs=(f"ref-{index}",),
                actor_id=f"actor-{index}",
                geography="CN",
                epistemic_status="INFERRED",
            )
            for index in range(1, 5)
        )
        result = assess_emergent_concept(concept, observations)
        self.assertEqual(result.state, "RESIDUAL")
        self.assertEqual(result.observation_count, 0)

    def test_actor_autonomy_is_canonical_observation_truth(self):
        doctrine = (ROOT / "docs/OBSERVATION_FABRIC.md").read_text(encoding="utf-8")
        for invariant in (
            "ACTOR_AUTONOMY",
            "NO_COERCIVE_ROUTING",
            "NO_MORAL_PERSONALITY_SCORING",
            "OBSERVATION_NE_JUDGMENT",
            "RECOMMENDATION_NE_CONSENT",
            "VALUE_FROM_FRICTION_REDUCTION",
            "NO_ARTIFICIAL_DEPENDENCY",
        ):
            self.assertIn(invariant, doctrine)
        self.assertIn("Actor rejection is valid evidence", doctrine)
        self.assertIn("not automatically a bad outcome", doctrine)


if __name__ == "__main__":
    unittest.main()
