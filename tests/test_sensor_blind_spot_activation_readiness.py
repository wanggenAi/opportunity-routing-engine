import unittest
from pathlib import Path

from src.sensor_blind_spot_activation_readiness import (
    reconcile_blind_spot_activation_readiness,
)
from src.sensor_portfolio import OperationalSource, load_operational_sources
from src.sensor_registry import load_sensor_candidates


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


def douyin_permission_probe():
    return {
        "schema_version": "douyin-openapi-permission-probe.v1",
        "source_id": "DOUYIN_OPENAPI",
        "intended_scope": "video.search",
        "signal_fit": "KEYWORD_VIDEO_AND_COMMENT_DISCOVERY_SUPPORTED_BY_OFFICIAL_DOCS",
        "permission_class": "SPECIAL_PERMISSION",
        "permission_default_state": "DEFAULT_OFF",
        "permission_application_route": "MANAGEMENT_CENTER_APPLICATION",
        "application_approval_status": "NOT_ESTABLISHED",
        "intended_scope_free_quota_amount_status": "NOT_ESTABLISHED_FROM_PUBLIC_DOCS",
        "zero_incremental_fee_condition": "NOT_ESTABLISHED",
        "paid_extension_status": "PAID_EXTENSION_EXISTS_AFTER_FREE_QUOTA",
        "producer_trial_allowed": False,
        "blockers": [
            "VIDEO_SEARCH_SPECIAL_PERMISSION_DEFAULT_OFF",
            "APPLICATION_APPROVAL_NOT_ESTABLISHED",
            "VIDEO_SEARCH_FREE_QUOTA_NOT_PUBLICLY_ESTABLISHED",
            "ZERO_INCREMENTAL_FEE_CONDITION_NOT_ESTABLISHED",
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
        baidu = next(x for x in search["source_assessments"] if x["source_id"] == "BAIDU_INDEX")
        self.assertEqual(search["readiness_state"], "NO_SAFE_AUTOMATED_PATH_CURRENTLY_PROVEN")
        self.assertFalse(baidu["producer_trial_allowed"])
        self.assertIn("MANUAL_OR_LOGIN_BOUND_ACCESS", baidu["blockers"])
        self.assertIn("REVERSE_ENGINEERED_ENDPOINTS_FORBIDDEN", baidu["constraints"])

    def test_douyin_without_bound_probe_remains_permission_validation_candidate(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational, candidates, current_blind_coverage()
        )
        social = next(x for x in result["channels"] if x["channel_id"] == "SOCIAL_PUBLIC_DISCOURSE")
        self.assertEqual(social["readiness_state"], "PERMISSION_VALIDATION_REQUIRED")
        douyin = next(x for x in social["source_assessments"] if x["source_id"] == "DOUYIN_OPENAPI")
        self.assertEqual(douyin["readiness_state"], "PERMISSION_VALIDATION_CANDIDATE")
        self.assertFalse(douyin["external_approval_required"])

    def test_bound_official_probe_converges_douyin_to_external_approval_required(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational,
            candidates,
            current_blind_coverage(),
            permission_probes={"DOUYIN_OPENAPI": douyin_permission_probe()},
        )
        self.assertEqual(result["producer_trial_ready_source_count"], 0)
        self.assertEqual(result["external_approval_required_source_ids"], ["DOUYIN_OPENAPI"])
        self.assertEqual(
            result["safe_activation_conclusion"],
            "BLOCKED_ON_EXTERNAL_APPROVAL_AND_EFFECTIVE_QUOTA_EVIDENCE",
        )
        social = next(x for x in result["channels"] if x["channel_id"] == "SOCIAL_PUBLIC_DISCOURSE")
        self.assertEqual(social["readiness_state"], "EXTERNAL_APPROVAL_REQUIRED")
        self.assertEqual(social["external_approval_required_source_ids"], ["DOUYIN_OPENAPI"])
        douyin = next(x for x in social["source_assessments"] if x["source_id"] == "DOUYIN_OPENAPI")
        self.assertEqual(douyin["readiness_state"], "EXTERNAL_APPROVAL_REQUIRED")
        self.assertTrue(douyin["external_approval_required"])
        self.assertFalse(douyin["producer_trial_allowed"])
        self.assertEqual(
            set(douyin["next_required_evidence"]),
            {
                "VIDEO_SEARCH_APPLICATION_APPROVED_FOR_THIS_APP",
                "VIDEO_SEARCH_EFFECTIVE_FREE_QUOTA_FOR_THIS_APP_SCOPE",
                "INTENDED_COLLECTION_CADENCE_FITS_ZERO_INCREMENTAL_FEE",
            },
        )
        self.assertEqual(douyin["official_permission_probe"]["intended_scope"], "video.search")
        self.assertIn("APPLICATION_APPROVAL_NOT_ESTABLISHED", douyin["blockers"])
        self.assertIn("VIDEO_SEARCH_FREE_QUOTA_NOT_PUBLICLY_ESTABLISHED", douyin["blockers"])

    def test_invalid_permission_probe_fails_closed(self):
        operational, candidates = self._actual()
        probe = douyin_permission_probe()
        probe["application_approval_status"] = "APPROVED"
        with self.assertRaisesRegex(ValueError, "approval"):
            reconcile_blind_spot_activation_readiness(
                operational,
                candidates,
                current_blind_coverage(),
                permission_probes={"DOUYIN_OPENAPI": probe},
            )

    def test_global_social_candidates_remain_unqualified(self):
        operational, candidates = self._actual()
        result = reconcile_blind_spot_activation_readiness(
            operational, candidates, current_blind_coverage()
        )
        social = next(x for x in result["channels"] if x["channel_id"] == "SOCIAL_PUBLIC_DISCOURSE")
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
            "channels": [{
                "channel_id": "TEST_BLIND",
                "blind_spot": True,
                "registered_operational_source_ids": ["SAFE_TEST"],
                "candidate_source_ids": [],
            }],
        }
        result = reconcile_blind_spot_activation_readiness((source,), (), coverage)
        self.assertEqual(result["producer_trial_ready_source_ids"], ["SAFE_TEST"])
        self.assertEqual(result["safe_activation_conclusion"], "PRODUCER_TRIAL_AVAILABLE")
        row = result["channels"][0]["source_assessments"][0]
        self.assertTrue(row["producer_trial_allowed"])

    def test_blind_spot_summary_mismatch_fails_closed(self):
        operational, candidates = self._actual()
        coverage = current_blind_coverage()
        coverage["blind_spot_channel_ids"] = ["SEARCH_INTENT"]
        with self.assertRaisesRegex(ValueError, "diverges"):
            reconcile_blind_spot_activation_readiness(operational, candidates, coverage)


if __name__ == "__main__":
    unittest.main()
