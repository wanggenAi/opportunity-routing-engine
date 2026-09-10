import unittest

from src.opportunity_ranker import SCORE_MAXIMA, evaluate


def full_scores():
    return dict(SCORE_MAXIMA)


def gates(**overrides):
    base = {
        "G0": "PASS",
        "G1": "PASS",
        "G2": "PASS",
        "G3": "PASS",
        "G4": "PASS",
        "G5": "PASS",
    }
    base.update(overrides)
    return base


class OpportunityRankerTests(unittest.TestCase):
    def test_unknown_payer_gate_never_becomes_test_now(self):
        result = evaluate(full_scores(), gates(G1="UNKNOWN"))
        self.assertEqual(result.final_score, 100)
        self.assertEqual(result.band, "A")
        self.assertFalse(result.transaction_ready)
        self.assertEqual(result.decision, "INVESTIGATE")

    def test_fail_transaction_gate_blocks_even_perfect_score(self):
        result = evaluate(full_scores(), gates(G2="FAIL"))
        self.assertTrue(result.hard_blocked)
        self.assertEqual(result.decision, "REJECT_OR_REDESIGN")

    def test_conditional_g3_can_be_transaction_ready(self):
        result = evaluate(full_scores(), gates(G3="CONDITIONAL"), penalty_points=10)
        self.assertTrue(result.transaction_ready)
        self.assertTrue(result.scale_ready)
        self.assertEqual(result.final_score, 90)
        self.assertEqual(result.decision, "TEST_NOW")

    def test_unknown_orchestration_gate_can_be_explicit_test_target(self):
        result = evaluate(full_scores(), gates(G5="UNKNOWN"))
        self.assertTrue(result.transaction_ready)
        self.assertFalse(result.scale_ready)
        self.assertEqual(result.decision, "TEST_NOW")
        self.assertIn("resolve", result.reason)

    def test_failed_delegatability_blocks_strategic_fit(self):
        result = evaluate(full_scores(), gates(G4="FAIL"))
        self.assertTrue(result.transaction_ready)
        self.assertTrue(result.strategic_blocked)
        self.assertEqual(result.decision, "REDESIGN_STRATEGIC_FIT")

    def test_penalty_floor_is_zero(self):
        result = evaluate(
            {key: 0 for key in SCORE_MAXIMA},
            gates(),
            penalty_points=50,
        )
        self.assertEqual(result.final_score, 0)
        self.assertEqual(result.decision, "REJECT_OR_DORMANT")

    def test_rejects_out_of_range_score(self):
        scores = full_scores()
        scores["pain_severity"] = 11
        with self.assertRaises(ValueError):
            evaluate(scores, gates())

    def test_requires_all_six_gates(self):
        with self.assertRaises(ValueError):
            evaluate(
                full_scores(),
                {"G0": "PASS", "G1": "PASS", "G2": "PASS", "G3": "PASS"},
            )


if __name__ == "__main__":
    unittest.main()
