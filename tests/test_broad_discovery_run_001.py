import json
import unittest
from pathlib import Path

from src.research_control_plane import (
    assess_research_coverage,
    build_research_plan,
    evidence_from_dict,
    mission_from_dict,
)


RUN_DIR = Path("data/research_runs/BROAD_DISCOVERY_RUN_001_2026-09-14")
MISSION = Path("data/research_missions/china_primary_broad_discovery.json")
FORBIDDEN_EVIDENCE_FIELDS = {
    "opportunity",
    "opportunity_score",
    "commercial_score",
    "payer",
    "paid_need",
    "route_testable",
    "business_promotion",
    "regenerative_loop_confirmed",
}


class BroadDiscoveryRun001Tests(unittest.TestCase):
    def _load(self):
        mission = mission_from_dict(json.loads(MISSION.read_text(encoding="utf-8")))
        plan = build_research_plan(mission)
        payload = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        records = [evidence_from_dict(item) for item in payload["evidence"]]
        return mission, plan, payload, records

    def test_run_reaches_broad_coverage_without_commercial_promotion(self):
        mission, plan, payload, records = self._load()
        self.assertEqual(payload["mission_id"], mission.mission_id)
        self.assertEqual(len(records), 30)
        self.assertEqual(len({item.evidence_id for item in records}), 30)

        assessment = assess_research_coverage(mission, plan, records)
        self.assertEqual(assessment.state, "BROAD_DISCOVERY_READY")
        self.assertTrue(assessment.broad_discovery_use_authorized)
        self.assertEqual(assessment.evidence_count, 30)
        self.assertGreaterEqual(assessment.independent_host_count, mission.min_independent_hosts)
        self.assertGreaterEqual(assessment.source_family_count, mission.min_source_families)
        self.assertEqual(assessment.blockers, ())
        for lane, weight in mission.lane_weights.items():
            if weight > 0:
                self.assertGreater(assessment.lane_counts.get(lane, 0), 0)

    def test_research_evidence_cannot_smuggle_business_truth(self):
        payload = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        for item in payload["evidence"]:
            self.assertFalse(FORBIDDEN_EVIDENCE_FIELDS & set(item))

    def test_global_auxiliary_records_have_domestic_corroboration(self):
        mission, plan, _, records = self._load()
        query_lane = {q["query_id"]: q["lane"] for q in plan["queries"]}
        global_records = [item for item in records if query_lane[item.query_id] == "GLOBAL_AUXILIARY"]
        self.assertGreater(len(global_records), 0)
        self.assertTrue(all(item.domestic_corroboration_ref for item in global_records))

    def test_dynamic_vocabulary_is_next_run_input_not_taxonomy(self):
        payload = json.loads((RUN_DIR / "dynamic_terms.json").read_text(encoding="utf-8"))
        self.assertEqual(payload["semantics"], "NEXT_RUN_RESEARCH_VOCABULARY_NOT_ONTOLOGY")
        self.assertGreaterEqual(len(payload["dynamic_terms"]), 8)
        self.assertIn("DYNAMIC_TERM_NE_TAXONOMY", payload["truth_boundaries"])
        expanded = build_research_plan(
            mission_from_dict(json.loads(MISSION.read_text(encoding="utf-8"))),
            dynamic_terms=payload["dynamic_terms"],
        )
        self.assertTrue(any(q["seed_id"].startswith("dynamic-") for q in expanded["queries"]))


if __name__ == "__main__":
    unittest.main()
