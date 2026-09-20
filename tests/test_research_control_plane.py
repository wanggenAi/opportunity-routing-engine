import json
import unittest
from pathlib import Path

from src.research_control_plane import (
    ResearchEvidenceRecord,
    ResearchMission,
    ResearchSeed,
    assess_research_coverage,
    build_research_plan,
    empty_coverage_assessment,
    mission_from_dict,
)


class ResearchControlPlaneTests(unittest.TestCase):
    def _mission(self):
        payload = json.loads(
            Path("data/research_missions/attraction_field_broad_reality.json").read_text(
                encoding="utf-8"
            )
        )
        return mission_from_dict(payload)

    def test_clean_slate_plan_has_bounded_unique_multi_lane_budget(self):
        mission = self._mission()
        plan = build_research_plan(mission)
        self.assertEqual(plan["query_count"], 60)
        self.assertEqual(
            plan["lane_query_budget"],
            {
                "CHINA_CORE": 21,
                "JIANGSU_ZOOM": 9,
                "XUZHOU_ZOOM": 9,
                "GLOBAL_AUXILIARY": 9,
                "CONTRADICTION_SEARCH": 6,
                "SOURCE_DISCOVERY": 6,
            },
        )
        query_ids = [q["query_id"] for q in plan["queries"]]
        query_texts = [q["query"] for q in plan["queries"]]
        self.assertEqual(len(set(query_ids)), 60)
        self.assertEqual(len(set(query_texts)), 60)
        self.assertTrue(all(q["target_geography"].startswith("CN") for q in plan["queries"]))
        self.assertEqual(plan["mission"]["cross_border_mode"], "EXCEPTION_ONLY")
        self.assertFalse(plan["executor_contract"]["login_or_access_control_bypass_allowed"])
        self.assertFalse(plan["executor_contract"]["captcha_or_antibot_bypass_allowed"])
        self.assertFalse(plan["executor_contract"]["source_discovery_implies_activation"])
        self.assertFalse(plan["executor_contract"]["foreign_signal_implies_china_fact"])
        self.assertEqual(plan["mission"]["attention_mode"], "ATTRACTION_FIRST")
        self.assertEqual(plan["executor_contract"]["attention_mode"], "ATTRACTION_FIRST")
        self.assertIn(
            "STATE_DEPENDENT_VALUE_JUMP",
            plan["executor_contract"]["attraction_signal_contract"],
        )
        self.assertIn(
            "DECISION_WINDOW_STILL_MOVABLE",
            plan["executor_contract"]["attraction_signal_contract"],
        )
        self.assertIn(
            "A_SIDE_DISCOVERABILITY",
            plan["executor_contract"]["attraction_signal_contract"],
        )
        self.assertIn(
            "B_SIDE_DISCOVERABILITY",
            plan["executor_contract"]["attraction_signal_contract"],
        )
        self.assertIn(
            "MATCH_RESOLVABILITY_WITHOUT_RECURRING_EXPERT_LABOR",
            plan["executor_contract"]["attraction_signal_contract"],
        )

    def test_dynamic_terms_are_prioritized_without_changing_ontology(self):
        mission = self._mission()
        plan = build_research_plan(
            mission,
            dynamic_terms=["宠物独居陪伴行为新变化", "AI代理授权摩擦"],
        )
        self.assertEqual(plan["dynamic_term_count"], 2)
        queries = [item["query"] for item in plan["queries"]]
        self.assertTrue(any("宠物独居陪伴行为新变化" in value for value in queries))
        self.assertTrue(any("AI代理授权摩擦" in value for value in queries))
        self.assertEqual(len({item["query_id"] for item in plan["queries"]}), 60)
        self.assertEqual(plan["schema_version"], "research-control-plane.v1")

    def test_query_budget_fails_closed_when_seed_space_would_duplicate_tasks(self):
        mission = ResearchMission(
            mission_id="tiny",
            as_of_date="2026-09-14",
            primary_geography="CN",
            zoom_geographies=("CN-JS",),
            objective_primitives=("CHANGE",),
            seeds=(ResearchSeed("one", "单一主题", "zh-CN", ("CHANGE",)),),
            lane_weights={
                "CHINA_CORE": 1,
                "JIANGSU_ZOOM": 0,
                "XUZHOU_ZOOM": 0,
                "GLOBAL_AUXILIARY": 0,
                "CONTRADICTION_SEARCH": 0,
                "SOURCE_DISCOVERY": 0,
            },
            max_query_count=2,
        )
        with self.assertRaisesRegex(ValueError, "duplicate query slots"):
            build_research_plan(mission)

    def test_unexecuted_plan_is_explicit_calibration_only(self):
        mission = self._mission()
        plan = build_research_plan(mission)
        coverage = empty_coverage_assessment(mission, plan)
        self.assertEqual(coverage["state"], "CALIBRATION_ONLY")
        self.assertFalse(coverage["broad_discovery_use_authorized"])
        self.assertIn("NO_RESEARCH_EVIDENCE_EXECUTED", coverage["blockers"])
        self.assertTrue(any("ObservedPatterns" in note for note in coverage["truth_notes"]))

    def test_diverse_multi_lane_evidence_can_reach_broad_discovery_ready(self):
        mission = self._mission()
        plan = build_research_plan(mission)
        by_lane = {}
        for query in plan["queries"]:
            by_lane.setdefault(query["lane"], query["query_id"])

        lanes = [
            "CHINA_CORE",
            "JIANGSU_ZOOM",
            "XUZHOU_ZOOM",
            "GLOBAL_AUXILIARY",
            "CONTRADICTION_SEARCH",
            "SOURCE_DISCOVERY",
        ]
        evidence = []
        for index in range(12):
            lane = lanes[index % len(lanes)]
            evidence.append(
                ResearchEvidenceRecord(
                    evidence_id=f"ev-{index}",
                    query_id=by_lane[lane],
                    source_url=f"https://source{index}.example.test/item",
                    source_family=f"family-{index % 6}",
                    origin_geography="GLOBAL" if lane == "GLOBAL_AUXILIARY" else "CN",
                    relevance_geography="CN",
                    provenance_ref=f"prov-{index}",
                    collected_via="INTERACTIVE_AGENT_WEB",
                    domestic_corroboration_ref=("domestic-corroboration" if lane == "GLOBAL_AUXILIARY" else None),
                    contradiction=lane == "CONTRADICTION_SEARCH",
                )
            )

        coverage = assess_research_coverage(mission, plan, evidence)
        self.assertEqual(coverage.state, "BROAD_DISCOVERY_READY")
        self.assertTrue(coverage.broad_discovery_use_authorized)
        self.assertEqual(coverage.independent_host_count, 12)
        self.assertEqual(coverage.source_family_count, 6)
        self.assertEqual(coverage.blockers, ())

    def test_source_concentration_keeps_scope_partial(self):
        mission = self._mission()
        plan = build_research_plan(mission)
        china_query = next(q["query_id"] for q in plan["queries"] if q["lane"] == "CHINA_CORE")
        evidence = [
            ResearchEvidenceRecord(
                evidence_id=f"ev-{index}",
                query_id=china_query,
                source_url=f"https://one.example.test/item/{index}",
                source_family="social",
                origin_geography="CN",
                relevance_geography="CN",
                provenance_ref=f"prov-{index}",
                collected_via="INTERACTIVE_AGENT_WEB",
            )
            for index in range(20)
        ]
        coverage = assess_research_coverage(mission, plan, evidence)
        self.assertEqual(coverage.state, "PARTIAL_DISCOVERY")
        self.assertFalse(coverage.broad_discovery_use_authorized)
        self.assertIn("SINGLE_HOST_OVERCONCENTRATION", coverage.blockers)
        self.assertIn("INSUFFICIENT_SOURCE_FAMILY_DIVERSITY", coverage.blockers)

    def test_evidence_cannot_reference_query_outside_plan(self):
        mission = self._mission()
        plan = build_research_plan(mission)
        evidence = [
            ResearchEvidenceRecord(
                evidence_id="ev-x",
                query_id="unknown-query",
                source_url="https://example.test/item",
                source_family="official",
                origin_geography="CN",
                relevance_geography="CN",
                provenance_ref="prov-x",
                collected_via="DIRECT_PUBLIC_SOURCE",
            )
        ]
        with self.assertRaisesRegex(ValueError, "unknown query ids"):
            assess_research_coverage(mission, plan, evidence)


if __name__ == "__main__":
    unittest.main()
