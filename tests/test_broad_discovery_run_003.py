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


RUN_DIR = Path("data/research_runs/BROAD_DISCOVERY_RUN_003_2026-09-14")
MISSION_PATH = Path("data/research_missions/china_primary_broad_discovery.json")


class BroadDiscoveryRun003Tests(unittest.TestCase):
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
        task_by_query = {item["query_id"]: item for item in plan["queries"]}
        return mission, plan, raw, bound, coverage, task_by_query

    def test_executor_captures_bind_without_manual_query_ids(self):
        _, _, raw, bound, _, _ = self._build()
        self.assertEqual(len(raw["captures"]), 30)
        self.assertTrue(all("query_id" not in item for item in raw["captures"]))
        self.assertEqual(bound["evidence_count"], 30)
        self.assertTrue(all(item["query_id"].startswith("rq-") for item in bound["evidence"]))

    def test_five_new_dynamic_structures_are_in_governed_plan(self):
        _, plan, _, _, _, _ = self._build()
        self.assertEqual(plan["dynamic_term_count"], 5)
        queries = [item["query"] for item in plan["queries"]]
        for term in json.loads((RUN_DIR / "dynamic_terms.json").read_text(encoding="utf-8"))["dynamic_terms"]:
            self.assertTrue(any(term in query for query in queries))

    def test_coverage_is_broad_with_expected_lane_distribution(self):
        _, _, _, _, coverage, _ = self._build()
        self.assertEqual(coverage.state, "BROAD_DISCOVERY_READY")
        self.assertTrue(coverage.broad_discovery_use_authorized)
        self.assertEqual(coverage.blockers, ())
        self.assertEqual(coverage.cautions, ())
        self.assertGreaterEqual(coverage.independent_host_count, 12)
        self.assertGreaterEqual(coverage.source_family_count, 6)
        self.assertEqual(
            dict(coverage.lane_counts),
            {
                "CHINA_CORE": 6,
                "CONTRADICTION_SEARCH": 5,
                "GLOBAL_AUXILIARY": 4,
                "JIANGSU_ZOOM": 5,
                "SOURCE_DISCOVERY": 5,
                "XUZHOU_ZOOM": 5,
            },
        )

    def test_global_auxiliary_is_minor_and_has_domestic_corroboration(self):
        _, _, _, bound, coverage, task_by_query = self._build()
        global_items = [
            item for item in bound["evidence"]
            if task_by_query[item["query_id"]]["lane"] == "GLOBAL_AUXILIARY"
        ]
        self.assertEqual(len(global_items), 4)
        self.assertLessEqual(len(global_items) / coverage.evidence_count, 0.30)
        self.assertTrue(all(item["domestic_corroboration_ref"] for item in global_items))

    def test_counterevidence_covers_all_five_dynamic_structures(self):
        _, _, _, bound, _, task_by_query = self._build()
        contradictions = [
            item for item in bound["evidence"]
            if task_by_query[item["query_id"]]["lane"] == "CONTRADICTION_SEARCH"
        ]
        self.assertEqual(len(contradictions), 5)
        self.assertTrue(all(item["contradiction"] for item in contradictions))
        seed_ids = {task_by_query[item["query_id"]]["seed_id"] for item in contradictions}
        self.assertEqual(seed_ids, {f"dynamic-{i:03d}" for i in range(1, 6)})

    def test_global_origin_outside_auxiliary_is_still_domestically_corroborated(self):
        _, _, _, bound, _, _ = self._build()
        global_origin = [item for item in bound["evidence"] if item["origin_geography"] == "GLOBAL"]
        self.assertGreaterEqual(len(global_origin), 4)
        self.assertTrue(all(item["domestic_corroboration_ref"] for item in global_origin))

    def test_research_batch_cannot_promote_commercial_truth(self):
        _, _, _, bound, coverage, _ = self._build()
        rendered = json.dumps({"bound": bound, "coverage": coverage.as_dict()}, ensure_ascii=False)
        for forbidden_key in (
            '"opportunity_score"',
            '"commercial_score"',
            '"route_testable"',
            '"core_business_candidate"',
            '"business_promotion"',
            '"payer"',
            '"paid_need"',
        ):
            self.assertNotIn(forbidden_key, rendered)


if __name__ == "__main__":
    unittest.main()
