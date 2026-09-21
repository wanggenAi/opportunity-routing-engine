import unittest

from src.jev_research_advisory import build_continuation_directive


def _row(route: str, *, status: str = "SUCCESS", formation_id: str = "F1") -> dict:
    return {
        "formation_id": formation_id,
        "status": status,
        "effective_research_route": route,
        "state_fingerprint": "abc123",
        "decisions": {"attention_priority": {"choice": "HIGH"}},
    }


class JevContinuationDirectiveTests(unittest.TestCase):
    def test_all_closed_advances_without_asking_user_to_continue(self):
        payload = {
            "contract": "OPPORTUNITY_JEV_RESEARCH_ADVISORY_V2",
            "execution_status": "SUCCESS",
            "input_scan_id": "ATTRACTION_SCAN_035",
            "input_scan_path": "data/research_runs/attraction_scan_035.json",
            "rows": [_row("NO_FURTHER_RESEARCH")],
        }
        directive = build_continuation_directive(payload)
        self.assertEqual(directive["next_action"], "ADVANCE_TO_NEXT_SCAN")
        self.assertTrue(directive["autonomous_continuation_allowed"])
        self.assertFalse(directive["human_intervention_required"])
        self.assertFalse(directive["automatic_research_execution_by_jev"])
        self.assertFalse(directive["commercial_promotion_authority"])
        self.assertFalse(directive["external_side_effects_allowed"])

    def test_open_research_routes_become_agent_execution_queue(self):
        payload = {
            "contract": "OPPORTUNITY_JEV_RESEARCH_ADVISORY_V2",
            "execution_status": "SUCCESS",
            "rows": [
                _row("EXACT_INCUMBENT_PREFLIGHT", formation_id="F1"),
                _row("CAUSAL_DESCENT", formation_id="F2"),
                _row("NO_FURTHER_RESEARCH", formation_id="F3"),
            ],
        }
        directive = build_continuation_directive(payload)
        self.assertEqual(directive["next_action"], "EXECUTE_RESEARCH_QUEUE")
        self.assertTrue(directive["autonomous_continuation_allowed"])
        self.assertEqual(
            [item["action"] for item in directive["dispatch_items"]],
            [
                "RUN_EXACT_INCUMBENT_PREFLIGHT",
                "RUN_CAUSAL_DESCENT",
                "DROP_FROM_CURRENT_RESEARCH_QUEUE",
            ],
        )

    def test_human_review_or_failed_execution_stops_autonomous_loop(self):
        for payload in (
            {
                "contract": "OPPORTUNITY_JEV_RESEARCH_ADVISORY_V2",
                "execution_status": "SUCCESS",
                "rows": [_row("HUMAN_REVIEW")],
            },
            {
                "contract": "OPPORTUNITY_JEV_RESEARCH_ADVISORY_V2",
                "execution_status": "FAILED",
                "rows": [],
            },
        ):
            with self.subTest(payload=payload):
                directive = build_continuation_directive(payload)
                self.assertEqual(directive["next_action"], "STOP_FOR_HUMAN_REVIEW")
                self.assertFalse(directive["autonomous_continuation_allowed"])
                self.assertTrue(directive["human_intervention_required"])


if __name__ == "__main__":
    unittest.main()
