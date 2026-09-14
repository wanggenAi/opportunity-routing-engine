import json
import unittest
from dataclasses import replace
from pathlib import Path

from src.research_control_plane import (
    assess_research_coverage,
    build_research_plan,
    evidence_from_dict,
    mission_from_dict,
)
from src.research_execution_capture import bind_captures_to_plan, capture_from_dict


RUN_DIR = Path("data/research_runs/BROAD_DISCOVERY_RUN_002_2026-09-14")
MISSION_PATH = Path("data/research_missions/china_primary_broad_discovery.json")


class BroadDiscoveryRun002Tests(unittest.TestCase):
    def _build(self):
        mission = mission_from_dict(json.loads(MISSION_PATH.read_text(encoding="utf-8")))
        mission = replace(mission, as_of_date="2026-09-14")
        dynamic = json.loads((RUN_DIR / "dynamic_terms.json").read_text(encoding="utf-8"))["dynamic_terms"]
        plan = build_research_plan(mission, dynamic_terms=dynamic)
        raw = json.loads((RUN_DIR / "captures.json").read_text(encoding="utf-8"))
        captures = tuple(capture_from_dict(item) for item in raw["captures"])
        bound = bind_captures_to_plan(plan, captures)
        records = tuple(evidence_from_dict(item) for item in bound["evidence"])
        coverage = assess_research_coverage(mission, plan, records)
        return mission, plan, raw, bound, coverage

    def test_executor_captures_have_no_manual_query_ids(self):
        _, _, raw, bound, _ = self._build()
        self.assertEqual(len(raw["captures"]), 30)
        self.assertTrue(all("query_id" not in item for item in raw["captures"]))
        self.assertEqual(bound["evidence_count"], 30)
        self.assertTrue(all(item.get("query_id", "").startswith("rq-") for item in bound["evidence"]))

    def test_dynamic_terms_are_present_in_governed_plan(self):
        _, plan, _, _, _ = self._build()
        self.assertEqual(plan["dynamic_term_count"], 5)
        queries = [item["query"] for item in plan["queries"]]
        for term in json.loads((RUN_DIR / "dynamic_terms.json").read_text(encoding="utf-8"))["dynamic_terms"]:
            self.assertTrue(any(term in query for query in queries))

    def test_coverage_is_broad_and_all_six_lanes_are_executed(self):
        _, _, _, _, coverage = self._build()
        self.assertEqual(coverage.state, "BROAD_DISCOVERY_READY")
        self.assertTrue(coverage.broad_discovery_use_authorized)
        self.assertEqual(coverage.blockers, ())
        self.assertEqual(coverage.cautions, ())
        self.assertGreaterEqual(coverage.independent_host_count, 12)
        self.assertGreaterEqual(coverage.source_family_count, 6)
        self.assertEqual(
            set(coverage.lane_counts),
            {
                "CHINA_CORE",
                "JIANGSU_ZOOM",
                "XUZHOU_ZOOM",
                "GLOBAL_AUXILIARY",
                "CONTRADICTION_SEARCH",
                "SOURCE_DISCOVERY",
            },
        )

    def test_global_auxiliary_is_minor_and_domestically_corroborated(self):
        _, _, _, bound, coverage = self._build()
        self.assertLessEqual(
            coverage.lane_counts["GLOBAL_AUXILIARY"] / coverage.evidence_count,
            0.30,
        )
        global_items = [
            item for item in bound["evidence"]
            if item["query_id"] in {
                evidence["query_id"]
                for evidence in bound["evidence"]
                if evidence["evidence_id"].startswith("global-")
            }
            and item["evidence_id"].startswith("global-")
        ]
        self.assertEqual(len(global_items), 4)
        self.assertTrue(all(item["domestic_corroboration_ref"] for item in global_items))

    def test_contradiction_lane_contains_explicit_counterevidence(self):
        _, _, _, bound, _ = self._build()
        contradictions = [item for item in bound["evidence"] if item["contradiction"]]
        self.assertEqual(len(contradictions), 5)
        ids = {item["evidence_id"] for item in contradictions}
        self.assertIn("contra-prepay-risk-1", ids)
        self.assertIn("contra-consumer-optimism-1", ids)

    def test_research_batch_cannot_promote_commercial_truth(self):
        _, _, _, bound, coverage = self._build()
        rendered = json.dumps(
            {"bound": bound, "coverage": coverage.as_dict()},
            ensure_ascii=False,
        )
        for forbidden_key in (
            '"opportunity_score"',
            '"commercial_score"',
            '"route_testable"',
            '"core_business_candidate"',
            '"business_promotion"',
            '"payer"',
        ):
            self.assertNotIn(forbidden_key, rendered)


if __name__ == "__main__":
    unittest.main()
