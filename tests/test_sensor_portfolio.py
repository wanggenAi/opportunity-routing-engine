import unittest
from pathlib import Path

from src.sensor_portfolio import OperationalSource, load_operational_sources, reconcile_sensor_portfolio
from src.sensor_registry import SensorCandidate, load_sensor_candidates


ROOT = Path(__file__).resolve().parents[1]


class SensorPortfolioTests(unittest.TestCase):
    def _operational(self, *, source_id="SYNTHETIC", status="ACTIVE_LIVE_TEST", access_mode="PUBLIC_JSON_API"):
        return OperationalSource(
            source_id=source_id,
            name="Synthetic operational source",
            source_tier="A",
            owner="Synthetic owner",
            base_url="https://example.test",
            geography="China",
            indicator_scope="synthetic signal",
            access_mode=access_mode,
            refresh_cadence="DAILY",
            automation_allowed="SYNTHETIC_ONLY",
            status=status,
        )

    def _candidate(self, *, source_id="SYNTHETIC", lifecycle_state="DISCOVERED"):
        return SensorCandidate(
            source_id=source_id,
            name="Synthetic candidate",
            base_url="https://example.test",
            origin_geography="CN",
            relevance_geographies=("CN",),
            observable_dimensions=("CHANGE", "BEHAVIOR"),
            collection_mode="PUBLIC_ALLOWED_AUTOMATION",
            provenance_refs=("evidence:discovery",),
            activation_evidence_refs=("evidence:automation-permission",),
            unique_signal_value="Adds a synthetic signal for testing.",
            lifecycle_state=lifecycle_state,
        )

    def test_active_ready_candidate_does_not_count_as_production_until_explicit_active_state(self):
        result = reconcile_sensor_portfolio((), (self._candidate(),))
        self.assertEqual(result["candidate_sources"][0]["effective_state"], "ACTIVE_READY")
        self.assertTrue(result["candidate_sources"][0]["automation_ready"])
        self.assertFalse(result["candidate_sources"][0]["production_coverage"])
        self.assertEqual(result["candidate_production_live_count"], 0)
        self.assertEqual(result["production_coverage_count"], 0)

    def test_explicit_active_and_automation_ready_candidate_can_count_as_production(self):
        result = reconcile_sensor_portfolio(
            (), (self._candidate(lifecycle_state="ACTIVE"),)
        )
        self.assertTrue(result["candidate_sources"][0]["production_coverage"])
        self.assertEqual(result["candidate_production_live_count"], 1)
        self.assertEqual(result["production_coverage_count"], 1)

    def test_overlap_state_mismatch_stays_visible(self):
        result = reconcile_sensor_portfolio(
            (self._operational(),),
            (self._candidate(lifecycle_state="DISCOVERED"),),
        )
        self.assertEqual(result["overlap_count"], 1)
        self.assertEqual(result["registry_mismatch_count"], 1)
        mismatch = result["registry_mismatches"][0]
        self.assertTrue(mismatch["operational_registry_production_live"])
        self.assertFalse(mismatch["candidate_registry_production_live"])
        self.assertEqual(mismatch["state"], "REGISTRY_STATE_MISMATCH")

    def test_manual_registered_source_never_counts_as_production_live(self):
        manual = self._operational(
            status="ACTIVE",
            access_mode="HTML/MANUAL",
        )
        result = reconcile_sensor_portfolio((manual,), ())
        self.assertEqual(result["registered_manual_count"], 1)
        self.assertEqual(result["operational_production_live_count"], 0)
        self.assertEqual(result["production_coverage_count"], 0)
        self.assertEqual(result["operational_sources"][0]["operational_class"], "REGISTERED_MANUAL")

    def test_real_registry_distinguishes_live_manual_and_candidate_surfaces(self):
        operational = load_operational_sources(ROOT / "data/source_registry.csv")
        candidates = load_sensor_candidates(ROOT / "data/sensor_candidates.json")
        result = reconcile_sensor_portfolio(operational, candidates)

        self.assertEqual(result["candidate_registry_count"], 4)
        self.assertEqual(result["candidate_production_live_count"], 0)
        self.assertEqual(result["candidate_not_production_count"], 4)
        self.assertEqual(result["registry_mismatch_count"], 0)
        self.assertEqual(result["overlap_count"], 0)
        self.assertGreater(result["operational_production_live_count"], 0)
        self.assertEqual(
            result["production_coverage_count"],
            result["operational_production_live_count"],
        )

        production = set(result["production_coverage_source_ids"])
        manual = set(result["registered_manual_source_ids"])
        candidate_only = set(result["candidate_only_source_ids"])
        operational_only = set(result["operational_only_source_ids"])

        self.assertIn("CN_NBS", production)
        self.assertIn("JS_STATS", production)
        self.assertIn("XZ_GGZY", production)
        self.assertIn("BAIDU_INDEX", manual)
        self.assertIn("WEIBO_PUBLIC", manual)
        self.assertIn("XHS_PUBLIC", manual)
        self.assertIn("DOUYIN_PUBLIC", manual)
        self.assertIn("ZHIHU_PUBLIC", manual)
        self.assertFalse({"BAIDU_INDEX", "WEIBO_PUBLIC", "XHS_PUBLIC", "DOUYIN_PUBLIC", "ZHIHU_PUBLIC"} & production)
        self.assertEqual(
            candidate_only,
            {
                "REDDIT_CHINA_AUX_CANDIDATE",
                "X_CHINA_AUX_CANDIDATE",
                "INSTAGRAM_CHINA_AUX_CANDIDATE",
                "TELEGRAM_CHINA_AUX_CANDIDATE",
            },
        )
        self.assertIn("XHS_PUBLIC", operational_only)
        self.assertIn("UNREGISTERED", "UNREGISTERED")  # keep no implicit source synthesis in test fixtures
        self.assertIn("DISCOVERED_SOURCE_NE_PRODUCTION_COVERAGE", result["truth_boundaries"])
        self.assertIn("MANUAL_SURFACE_NE_AUTOMATED_LIVE_SENSOR", result["truth_boundaries"])


if __name__ == "__main__":
    unittest.main()
