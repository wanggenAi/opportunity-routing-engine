import unittest
from pathlib import Path

from src.sensor_blind_spot_activation_readiness import (
    reconcile_blind_spot_activation_readiness,
)
from src.sensor_portfolio import OperationalSource, load_operational_sources
from src.sensor_registry import SensorCandidate, load_sensor_candidates


ROOT = Path(__file__).resolve().parents[1]


def current_blind_coverage():
    return {
        "schema_version": "sensor-evidence-channel-coverage.v1",
        "channel_count": 6,
        "observed_channel_count": 4,
        "blind_spot_channel_count": 2,
        "observed_channel_ids": [
            "HARD_BEHAVIOR_MONEY",
            "LOCAL_REALITY",
            "OFFICIAL_STRUCTURAL_BASELINE",
            "REPRESENTATIVE_RESEARCH",
        ],
        "blind_spot_channel_ids": ["SEARCH_INTENT", "SOCIAL_PUBLIC_DISCOURSE"],
        "channels": [
            {
                "channel_id": "SEARCH_INTENT",
                "blind_spot": True,
                "registered_operational_source_ids": ["BAIDU_INDEX"],
                "candidate_source_ids": [],
            },
            {
                "channel_id": "SOCIAL_PUBLIC_DISCOURSE",
                "blind_spot": True,
                "registered_operational_source_ids": [
                    "DOUYIN_OPENAPI",
                    "DOUYIN_PUBLIC",
                    "WEIBO_CLI",
                    "WEIBO_PUBLIC",
                    "XHS_PUBLIC",
                    "ZHIHU_PUBLIC",
                ],
                "candidate_source_ids": [
                    "INSTAGRAM_CHINA_AUX_CANDIDATE",
                    "REDDIT_CHINA_AUX_CANDIDATE",
                    "TELEGRAM_CHINA_AUX_CANDIDATE",
                    "X_CHINA_AUX_CANDIDATE",
                ],
            },
            {
                "channel_id": "REPRESENTATIVE_RESEARCH",
                "blind_spot": False,
                "registered_operational_source_ids": ["QM"],
                "candidate_source_ids": [],
            },
        ],
    }


class BlindSpotActivationReadinessTests(unittest.TestCase):
    def _actual(self):
        return (
            load_operational_sources(ROOT / "data/source_registry.csv"),
            load_sensor_candidates(ROOT / "data/sensor_candidates.json"),
        )

    def test_current_blind_spots_have_no_safe_automated_producer_trial(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational, candidates, current_blind_coverage()
        )
        self.assertEqual(result["blind_spot_channel_count"], 2)
        self.assertEqual(
            result["blind_spot_channel_ids"],
            ["SEARCH_INTENT", "SOCIAL_PUBLIC_DISCOURSE"],
        )
        self.assertEqual(result["producer_trial_ready_source_count"], 0)
        self.assertEqual(result["producer_trial_ready_source_ids"], [])
        self.assertEqual(
            result["safe_activation_conclusion"],
            "NO_SAFE_AUTOMATED_PRODUCER_TRIAL_CURRENTLY_PROVEN",
        )

    def test_baidu_index_remains_manual_and_reverse_engineering_is_forbidden(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational, candidates, current_blind_coverage()
        )
        search = next(x for x in result["channels"] if x["channel_id"] == "SEARCH_INTENT")
        self.assertEqual(search["readiness_state"], "NO_SAFE_AUTOMATED_PATH_CURRENTLY_PROVEN")
        baidu = next(x for x in search["source_assessments"] if x["source_id"] == "BAIDU_INDEX")
        self.assertFalse(baidu["producer_trial_allowed"])
        self.assertIn("MANUAL_OR_LOGIN_BOUND_ACCESS", baidu["blockers"])
        self.assertIn("REVERSE_ENGINEERED_ENDPOINTS_FORBIDDEN", baidu["constraints"])

    def test_douyin_openapi_is_permission_validation_candidate_not_producer_ready(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational, candidates, current_blind_coverage()
        )
        social = next(
            x for x in result["channels"] if x["channel_id"] == "SOCIAL_PUBLIC_DISCOURSE"
        )
        self.assertEqual(social["readiness_state"], "PERMISSION_VALIDATION_REQUIRED")
        self.assertEqual(
            social["permission_validation_candidate_source_ids"], ["DOUYIN_OPENAPI"]
        )
        douyin = next(
            x for x in social["source_assessments"] if x["source_id"] == "DOUYIN_OPENAPI"
        )
        self.assertFalse(douyin["producer_trial_allowed"])
        self.assertIn("ACTIVATION_REVIEW_REQUIRED", douyin["blockers"])
        self.assertIn("AUTHORIZED_SCOPE_NOT_PROVEN_FOR_PRODUCER", douyin["blockers"])
        self.assertIn("ZERO_INCREMENTAL_FEE_SCOPE_NOT_PROVEN", douyin["blockers"])

    def test_global_social_candidates_remain_unqualified(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational, candidates, current_blind_coverage()
        )
        social = next(
            x for x in result["channels"] if x["channel_id"] == "SOCIAL_PUBLIC_DISCOURSE"
        )
        candidate_rows = [x for x in social["source_assessments"] if x["source_kind"] == "CANDIDATE"]
        self.assertEqual(len(candidate_rows), 4)
        for row in candidate_rows:
            self.assertFalse(row["producer_trial_allowed"])
            self.assertEqual(row["readiness_state"], "DISCOVERY_OR_QUALIFICATION_BLOCKED")
            self.assertIn("CHINA_RELEVANCE_NOT_EVIDENCED", row["blockers"])
            self.assertIn("COLLECTION_MODE_UNRESOLVED", row["blockers"])

    def test_explicit_allowed_automation_can_reach_trial_ready_without_becoming_production(self):
        source = OperationalSource(
            source_id="SAFE_TEST",
            name="Safe synthetic source",
            source_tier="B",
            owner="Synthetic",
            base_url="https://example.test",
            geography="China",
            indicator_scope="synthetic",
            access_mode="PUBLIC_HTML",
            refresh_cadence="DAILY",
            automation_allowed="BOUNDED_PUBLIC_FETCH;NO_PAID_DATA",
            status="QUALIFIED_NONLIVE",
        )
        coverage = {
            "schema_version": "sensor-evidence-channel-coverage.v1",
            "channel_count": 1,
            "observed_channel_count": 0,
            "blind_spot_channel_count": 1,
            "observed_channel_ids": [],
            "blind_spot_channel_ids": ["TEST_BLIND"],
            "channels": [
                {
                    "channel_id": "TEST_BLIND",
                    "blind_spot": True,
                    "registered_operational_source_ids": ["SAFE_TEST"],
                    "candidate_source_ids": [],
                }
            ],
        }
        result = reconcile_blind_spot_activation_readiness((source,), (), coverage)
        self.assertEqual(result["producer_trial_ready_source_ids"], ["SAFE_TEST"])
        self.assertEqual(result["safe_activation_conclusion"], "PRODUCER_TRIAL_AVAILABLE")
        row = result["channels"][0]["source_assessments"][0]
        self.assertTrue(row["producer_trial_allowed"])
        self.assertEqual(row["registry_status"], "QUALIFIED_NONLIVE")

    def test_blind_spot_summary_mismatch_fails_closed(self):
        operational, candidates = self._actual()
        coverage = current_blind_coverage()
        coverage["blind_spot_channel_ids"] = ["SEARCH_INTENT"]
        with self.assertRaisesRegex(ValueError, "diverges"):
            reconcile_blind_spot_activation_readiness(operational, candidates, coverage)


if __name__ == "__main__":
    unittest.main()
