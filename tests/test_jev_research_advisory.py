import json
import unittest
from pathlib import Path

from src.jev_research_advisory import (
    CONTRACT,
    JevResearchConfig,
    build_research_states,
    evaluate_research_advisory,
    render_advisory_markdown,
)
from tools.run_jev_research_advisory import resolve_scan_path


ROOT = Path(__file__).resolve().parents[1]


class FakeProvider:
    def evaluate(self, state, *, model, timeout_seconds):
        return {
            "model": "jev-test",
            "usage": {"requests": 1},
            "decisions": {
                "needs_exact_incumbent_preflight": {
                    "type": "noul",
                    "answer": True,
                    "probability": 0.9,
                    "confidence": 0.8,
                },
                "needs_deeper_causal_research": {
                    "type": "noul",
                    "answer": True,
                    "probability": 0.8,
                    "confidence": 0.6,
                },
                # Intentionally disagree with a closed DEMOTED engine verdict.
                "research_route": {
                    "type": "choice",
                    "choice": "CAUSAL_DESCENT",
                    "confidence": 0.81,
                    "probabilities": {
                        "NO_FURTHER_RESEARCH": 0.05,
                        "EXACT_INCUMBENT_PREFLIGHT": 0.10,
                        "CAUSAL_DESCENT": 0.81,
                        "HUMAN_REVIEW": 0.04,
                    },
                },
                "attention_priority": {
                    "type": "choice",
                    "choice": "HIGH",
                    "confidence": 0.75,
                },
                "evidence_state": {
                    "type": "choice",
                    "choice": "INSUFFICIENT",
                    "confidence": 0.72,
                },
            },
        }


class JevResearchAdvisoryTests(unittest.TestCase):
    def setUp(self):
        self.scan = {
            "scan_id": "ATTRACTION_SCAN_TEST",
            "as_of_date": "2026-09-21",
            "status": "COMPLETE",
            "search_mode": "BROAD_CURRENT_REALITY",
            "next_scan_id": "ATTRACTION_SCAN_NEXT",
            "next_search_boundary": "EXACT_INCUMBENT_PREFLIGHT_BEFORE_DEEP_RESEARCH",
            "first_external_value_flow": "NOT_PROVEN",
            "active_commercial_candidate_promotions": [],
            "retained_research_formations": [],
            "examined_formations": [
                {
                    "title": "CLOSED_FORMATION",
                    "chinese_title": "已关闭形成",
                    "evidence_class": "DIRECT_PAYMENT",
                    "verdict": "DEMOTED_EXACT_PAID_INCUMBENT",
                    "evidence_summary": "An exact incumbent already owns the control loop.",
                }
            ],
        }
        self.commercial = {
            "active_commercial_candidates": [],
            "first_external_value_flow": "NOT_PROVEN",
            "next_scan_id": "ATTRACTION_SCAN_NEXT",
            "current_validation_state": {
                "formation_id": "ATTRACTION_SCAN_015-F1",
            },
        }

    def test_state_preserves_authoritative_closure_and_nonpromotion_guardrails(self):
        states = build_research_states(
            scan=self.scan,
            commercial_state=self.commercial,
            max_entities=4,
        )
        self.assertEqual(len(states), 1)
        state = states[0]
        engine = state["authoritative_engine_context"]
        guards = state["guardrails"]

        self.assertEqual(engine["existing_verdict"], "DEMOTED_EXACT_PAID_INCUMBENT")
        self.assertTrue(engine["existing_closure_authoritative"])
        self.assertFalse(guards["commercial_promotion_authority"])
        self.assertFalse(guards["mutates_commercial_state"])
        self.assertFalse(guards["may_reverse_existing_demotions"])
        self.assertFalse(guards["may_create_active_candidate"])
        self.assertFalse(guards["llm_confidence_is_commercial_evidence"])
        self.assertFalse(guards["unknown_is_pass"])

    def test_jev_disagreement_cannot_reverse_engine_demotion(self):
        states = build_research_states(
            scan=self.scan,
            commercial_state=self.commercial,
            max_entities=4,
        )
        payload = evaluate_research_advisory(
            states=states,
            config=JevResearchConfig(enabled=True, shadow_mode=True),
            provider=FakeProvider(),
        )

        self.assertEqual(payload["contract"], CONTRACT)
        self.assertEqual(payload["execution_status"], "SUCCESS")
        self.assertFalse(payload["commercial_promotion_authority"])
        self.assertFalse(payload["mutates_commercial_state"])
        self.assertFalse(payload["may_reverse_existing_demotions"])
        self.assertFalse(payload["may_create_active_candidate"])
        self.assertFalse(payload["automatic_research_dispatch_allowed"])
        self.assertFalse(payload["llm_confidence_is_commercial_evidence"])
        self.assertFalse(payload["unknown_is_pass"])

        row = payload["rows"][0]
        self.assertEqual(row["existing_engine_verdict"], "DEMOTED_EXACT_PAID_INCUMBENT")
        self.assertTrue(row["existing_closure_authoritative"])
        self.assertEqual(
            row["decisions"]["research_route"]["choice"],
            "CAUSAL_DESCENT",
        )
        self.assertEqual(row["model_research_route"], "CAUSAL_DESCENT")
        self.assertEqual(row["effective_research_route"], "NO_FURTHER_RESEARCH")
        self.assertEqual(
            row["effective_route_source"],
            "AUTHORITATIVE_ENGINE_CLOSURE",
        )
        self.assertEqual(
            row["route_alignment"],
            "DISAGREES_WITH_AUTHORITATIVE_CLOSURE",
        )
        self.assertFalse(row["may_reverse_existing_demotions"])
        self.assertFalse(row["may_create_active_candidate"])
        self.assertFalse(row["automatic_research_dispatch_allowed"])
        self.assertEqual(
            payload["summary"]["model_route_counts"],
            {"CAUSAL_DESCENT": 1},
        )
        self.assertEqual(
            payload["summary"]["effective_route_counts"],
            {"NO_FURTHER_RESEARCH": 1},
        )
        self.assertNotIn("commercial_candidate", row)
        self.assertNotIn("promoted", row)

    def test_open_record_keeps_jev_route_advisory_but_never_auto_dispatches(self):
        scan = dict(self.scan)
        scan["examined_formations"] = [
            {
                "title": "OPEN_FORMATION",
                "evidence_class": "REPEATED_WORKAROUND",
                "verdict": "RESEARCH_OPEN",
                "evidence_summary": "A bounded unresolved research path remains.",
            }
        ]
        states = build_research_states(
            scan=scan,
            commercial_state=self.commercial,
        )
        payload = evaluate_research_advisory(
            states=states,
            config=JevResearchConfig(enabled=True, shadow_mode=True),
            provider=FakeProvider(),
        )
        row = payload["rows"][0]
        self.assertFalse(row["existing_closure_authoritative"])
        self.assertEqual(row["model_research_route"], "CAUSAL_DESCENT")
        self.assertEqual(row["effective_research_route"], "CAUSAL_DESCENT")
        self.assertEqual(row["effective_route_source"], "JEV_SHADOW_ADVISORY")
        self.assertEqual(row["route_alignment"], "NO_AUTHORITATIVE_CLOSURE")
        self.assertFalse(row["automatic_research_dispatch_allowed"])

    def test_auto_scan_resolution_follows_commercial_last_completed_scan(self):
        commercial = json.loads(
            (ROOT / "data/commercial_reset_state.json").read_text(encoding="utf-8")
        )
        path = resolve_scan_path(
            "auto",
            commercial,
            research_dir=ROOT / "data/research_runs",
        )
        expected_scan_number = commercial["last_completed_scan_id"].rsplit("_", 1)[-1]
        self.assertEqual(path.name, f"attraction_scan_{expected_scan_number.lower()}.json")

    def test_non_shadow_mode_fails_closed(self):
        states = build_research_states(
            scan=self.scan,
            commercial_state=self.commercial,
        )
        payload = evaluate_research_advisory(
            states=states,
            config=JevResearchConfig(enabled=True, shadow_mode=False),
            provider=FakeProvider(),
        )
        self.assertEqual(payload["execution_status"], "REFUSED_NON_SHADOW")
        self.assertEqual(payload["rows"], [])

    def test_disabled_mode_is_safe_noop(self):
        states = build_research_states(
            scan=self.scan,
            commercial_state=self.commercial,
        )
        payload = evaluate_research_advisory(
            states=states,
            config=JevResearchConfig(enabled=False, shadow_mode=True),
            provider=FakeProvider(),
        )
        self.assertEqual(payload["execution_status"], "SKIPPED_DISABLED")
        self.assertEqual(payload["rows"], [])

    def test_markdown_labels_advisory_boundary(self):
        states = build_research_states(
            scan=self.scan,
            commercial_state=self.commercial,
        )
        payload = evaluate_research_advisory(
            states=states,
            config=JevResearchConfig(enabled=True, shadow_mode=True),
            provider=FakeProvider(),
        )
        rendered = render_advisory_markdown(payload)
        self.assertIn("SHADOW RESEARCH ADVISORY ONLY", rendered)
        self.assertIn("commercial promotion authority: **False**", rendered)
        self.assertIn("may reverse existing demotions: **False**", rendered)
        self.assertIn("LLM confidence is commercial evidence: **False**", rendered)

    def test_scan035_inputs_remain_zero_promotion_truth(self):
        scan = json.loads(
            (ROOT / "data/research_runs/attraction_scan_035.json").read_text(
                encoding="utf-8"
            )
        )
        commercial = json.loads(
            (ROOT / "data/commercial_reset_state.json").read_text(encoding="utf-8")
        )
        states = build_research_states(
            scan=scan,
            commercial_state=commercial,
            max_entities=20,
        )
        self.assertEqual(scan["active_commercial_candidate_promotions"], [])
        self.assertEqual(scan["retained_research_formations"], [])
        self.assertEqual(commercial["active_commercial_candidates"], [])
        self.assertEqual(scan["first_external_value_flow"], "NOT_PROVEN")
        self.assertEqual(len(states), 6)
        self.assertTrue(
            all(
                state["authoritative_engine_context"]["existing_closure_authoritative"]
                for state in states
            )
        )

    def test_workflow_never_grants_contents_write_or_persists_to_main(self):
        workflow = (
            ROOT / ".github/workflows/jev-research-advisory.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("contents: read", workflow)
        self.assertIn("default: 'auto'", workflow)
        self.assertNotIn("contents: write", workflow)
        self.assertNotIn("git push", workflow)
        self.assertNotIn("active_commercial_candidates", workflow)


if __name__ == "__main__":
    unittest.main()
