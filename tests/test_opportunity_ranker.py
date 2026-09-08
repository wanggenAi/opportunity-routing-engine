import unittest

from src.opportunity_ranker import SCORE_MAXIMA, evaluate


def full_scores():
    return dict(SCORE_MAXIMA)


class OpportunityRankerTests(unittest.TestCase):
    def test_unknown_gate_never_becomes_test_now(self):
        result = evaluate(
            full_scores(),
            {"G0": "PASS", "G1": "UNKNOWN", "G2": "PASS", "G3": "PASS"},
        )
        self.assertEqual(result.final_score, 100)
        self.assertEqual(result.band, "A")
        self.assertFalse(result.gate_ready)
        self.assertEqual(result.decision, "INVESTIGATE")

    def test_fail_gate_blocks_even_perfect_score(self):
        result = evaluate(
            full_scores(),
            {"G0": "PASS", "G1": "PASS", "G2": "FAIL", "G3": "PASS"},
        )
        self.assertTrue(result.hard_blocked)
        self.assertEqual(result.decision, "REJECT_OR_REDESIGN")

    def test_conditional_g3_can_be_ready(self):
        result = evaluate(
            full_scores(),
            {"G0": "PASS", "G1": "PASS", "G2": "PASS", "G3": "CONDITIONAL"},
            penalty_points=10,
        )
        self.assertTrue(result.gate_ready)
        self.assertEqual(result.final_score, 90)
        self.assertEqual(result.decision, "TEST_NOW")

    def test_penalty_floor_is_zero(self):
        result = evaluate(
            {key: 0 for key in SCORE_MAXIMA},
            {"G0": "PASS", "G1": "PASS", "G2": "PASS", "G3": "PASS"},
            penalty_points=50,
        )
        self.assertEqual(result.final_score, 0)
        self.assertEqual(result.decision, "REJECT_OR_DORMANT")

    def test_rejects_out_of_range_score(self):
        scores = full_scores()
        scores["pain_severity"] = 11
        with self.assertRaises(ValueError):
            evaluate(
                scores,
                {"G0": "PASS", "G1": "PASS", "G2": "PASS", "G3": "PASS"},
            )


if __name__ == "__main__":
    unittest.main()
