import json
import unittest
from pathlib import Path

from src.research_control_plane import build_research_plan, mission_from_dict
from src.research_execution_capture import (
    bind_capture_to_plan,
    bind_captures_to_plan,
    capture_from_dict,
)


MISSION = Path("data/research_missions/attraction_field_broad_reality.json")


class ResearchExecutionCaptureTests(unittest.TestCase):
    def _plan(self):
        mission = mission_from_dict(json.loads(MISSION.read_text(encoding="utf-8")))
        return build_research_plan(mission)

    def _capture(self, **overrides):
        payload = {
            "evidence_id": "ev-001",
            "mission_id": "ATTRACTION_FIELD_BROAD_REALITY_V1",
            "lane": "CHINA_CORE",
            "seed_id": "formation-diversity-no-mechanism-inheritance",
            "source_url": "https://www.stats.gov.cn/example",
            "source_family": "official_statistics",
            "origin_geography": "CN",
            "relevance_geography": "CN",
            "provenance_ref": "web:turn-example",
            "collected_via": "INTERACTIVE_AGENT_WEB",
            "contradiction": False,
        }
        payload.update(overrides)
        return capture_from_dict(payload)

    def test_lane_seed_pair_resolves_exact_query_id(self):
        plan = self._plan()
        capture = self._capture()
        evidence = bind_capture_to_plan(plan, capture)
        expected = next(
            item for item in plan["queries"]
            if item["lane"] == "CHINA_CORE" and item["seed_id"] == "formation-diversity-no-mechanism-inheritance"
        )
        self.assertEqual(evidence["query_id"], expected["query_id"])
        self.assertEqual(evidence["source_url"], capture.source_url)

    def test_unknown_seed_or_wrong_lane_fails_closed(self):
        plan = self._plan()
        with self.assertRaisesRegex(ValueError, "exactly one research query task"):
            bind_capture_to_plan(plan, self._capture(seed_id="not-in-plan"))
        # Pick a seed that is genuinely present in the China lane but not allocated
        # to GLOBAL_AUXILIARY. This keeps the test about lane/plan binding rather than
        # coupling it to any historical bootstrap seed name.
        china_seeds = {
            item["seed_id"] for item in plan["queries"] if item["lane"] == "CHINA_CORE"
        }
        global_seeds = {
            item["seed_id"] for item in plan["queries"] if item["lane"] == "GLOBAL_AUXILIARY"
        }
        china_only_seed = next(seed_id for seed_id in china_seeds if seed_id not in global_seeds)
        with self.assertRaisesRegex(ValueError, "exactly one research query task"):
            bind_capture_to_plan(
                plan,
                self._capture(lane="GLOBAL_AUXILIARY", seed_id=china_only_seed),
            )

    def test_capture_mission_mismatch_fails_closed(self):
        plan = self._plan()
        with self.assertRaisesRegex(ValueError, "mission_id"):
            bind_capture_to_plan(plan, self._capture(mission_id="OTHER"))

    def test_duplicate_evidence_id_fails_closed(self):
        plan = self._plan()
        capture = self._capture()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            bind_captures_to_plan(plan, (capture, capture))

    def test_commercial_truth_fields_are_rejected(self):
        base = self._capture().as_dict()
        base["opportunity_score"] = 99
        with self.assertRaisesRegex(ValueError, "commercial/canonical truth"):
            capture_from_dict(base)

    def test_foreign_origin_is_allowed_but_china_relevance_is_required(self):
        plan = self._plan()
        foreign = self._capture(
            lane="GLOBAL_AUXILIARY",
            seed_id="formation-diversity-no-mechanism-inheritance",
            origin_geography="GLOBAL",
            relevance_geography="CN",
            domestic_corroboration_ref="domestic-001",
        )
        evidence = bind_capture_to_plan(plan, foreign)
        self.assertEqual(evidence["origin_geography"], "GLOBAL")
        self.assertEqual(evidence["relevance_geography"], "CN")

        with self.assertRaisesRegex(ValueError, "China relevance"):
            bind_capture_to_plan(
                plan,
                self._capture(relevance_geography="SG"),
            )

    def test_batch_payload_is_research_evidence_only(self):
        payload = bind_captures_to_plan(self._plan(), (self._capture(),))
        self.assertEqual(payload["evidence_count"], 1)
        self.assertEqual(payload["capture_schema_version"], "research-executor-capture.v1")
        rendered = json.dumps(payload, ensure_ascii=False)
        self.assertNotIn("opportunity_score", rendered)
        self.assertNotIn('"payer"', rendered)


if __name__ == "__main__":
    unittest.main()
