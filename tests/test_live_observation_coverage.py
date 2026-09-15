import unittest
from pathlib import Path

from src.live_observation_coverage import reconcile_live_observation_coverage
from src.sensor_portfolio import OperationalSource, load_operational_sources


ROOT = Path(__file__).resolve().parents[1]


def _assessment(source_counts):
    return {
        "schema_version": "live-observation-fabric.v1",
        "fixture_only": False,
        "live_source_artifacts": True,
        "current_observation_count": sum(source_counts.values()),
        "source_counts": dict(source_counts),
        "upstream_manifest": {"synthetic_test": True},
    }


def _source(source_id, status="ACTIVE_LIVE_TEST"):
    return OperationalSource(
        source_id=source_id,
        name=f"Synthetic {source_id}",
        source_tier="A",
        owner="Synthetic owner",
        base_url="https://example.test",
        geography="China",
        indicator_scope="synthetic",
        access_mode="PUBLIC_JSON_API",
        refresh_cadence="DAILY",
        automation_allowed="SYNTHETIC_ONLY",
        status=status,
    )


class LiveObservationCoverageTests(unittest.TestCase):
    def test_registry_live_without_adapter_remains_explicit_gap(self):
        result = reconcile_live_observation_coverage(
            (_source("LIVE_NO_ADAPTER"),),
            _assessment({}),
            adapter_support={},
        )
        row = result["coverage_rows"][0]
        self.assertEqual(row["coverage_state"], "NO_UNIFIED_ADAPTER")
        self.assertFalse(row["adapter_supported"])
        self.assertFalse(row["observed_in_latest_fabric"])
        self.assertEqual(result["no_unified_adapter_count"], 1)

    def test_adapter_support_without_current_observation_does_not_count_as_observed(self):
        result = reconcile_live_observation_coverage(
            (_source("SUPPORTED"),),
            _assessment({}),
            adapter_support={"SUPPORTED": ("adapter",)},
        )
        self.assertEqual(
            result["coverage_rows"][0]["coverage_state"],
            "ADAPTER_SUPPORTED_NOT_OBSERVED",
        )
        self.assertEqual(result["observed_production_count"], 0)
        self.assertEqual(result["adapter_supported_not_observed_count"], 1)

    def test_observed_without_governed_adapter_support_is_integrity_alert(self):
        result = reconcile_live_observation_coverage(
            (_source("UNDECLARED"),),
            _assessment({"UNDECLARED": 2}),
            adapter_support={},
        )
        row = result["coverage_rows"][0]
        self.assertEqual(row["coverage_state"], "OBSERVED_WITHOUT_GOVERNED_ADAPTER_SUPPORT")
        self.assertEqual(row["integrity_alert"], "OBSERVATION_WITHOUT_GOVERNED_ADAPTER_SUPPORT")
        self.assertEqual(result["observed_without_governed_support_count"], 1)

    def test_nonproduction_observation_is_audited_but_not_production_coverage(self):
        result = reconcile_live_observation_coverage(
            (_source("MANUAL", status="ACTIVE"),),
            _assessment({"MANUAL": 3}),
            adapter_support={"MANUAL": ("adapter",)},
        )
        self.assertEqual(result["production_live_registry_count"], 0)
        self.assertEqual(result["observed_production_count"], 0)
        self.assertEqual(result["observed_nonproduction_source_ids"], ["MANUAL"])

    def test_invalid_fabric_assessment_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "sum"):
            reconcile_live_observation_coverage(
                (_source("SUPPORTED"),),
                {
                    "schema_version": "live-observation-fabric.v1",
                    "fixture_only": False,
                    "live_source_artifacts": True,
                    "current_observation_count": 99,
                    "source_counts": {"SUPPORTED": 1},
                },
                adapter_support={"SUPPORTED": ("adapter",)},
            )

    def test_current_registry_manifest_exposes_three_remaining_adapter_gaps(self):
        operational = load_operational_sources(ROOT / "data/source_registry.csv")
        # This intentionally models the pre-017 Fabric artifact. The two newly
        # governed adapters must show as supported-but-not-yet-observed until the
        # production Fabric actually ingests their artifacts.
        result = reconcile_live_observation_coverage(
            operational,
            _assessment({"JS_STATS": 1, "XZ_GGZY": 24, "EJY365_XZ_LINKED": 29}),
        )
        self.assertEqual(result["production_live_registry_count"], 8)
        self.assertEqual(result["adapter_supported_production_count"], 5)
        self.assertEqual(result["observed_production_count"], 3)
        self.assertEqual(result["adapter_supported_not_observed_count"], 2)
        self.assertEqual(
            set(result["adapter_supported_not_observed_source_ids"]),
            {"CN_NBS", "CN_PBOC_JS"},
        )
        self.assertEqual(result["no_unified_adapter_count"], 3)
        self.assertEqual(
            set(result["no_unified_adapter_source_ids"]),
            {"CN_PBOC", "CN_CUSTOMS", "XZ_GOV_FINANCE_DEMAND"},
        )
        self.assertEqual(
            set(result["observed_production_source_ids"]),
            {"JS_STATS", "XZ_GGZY", "EJY365_XZ_LINKED"},
        )
        self.assertEqual(result["observed_without_governed_support_count"], 0)
        self.assertIn(
            "ACTIVE_LIVE_REGISTRY_NE_OBSERVED_IN_FABRIC",
            result["truth_boundaries"],
        )
        self.assertIn(
            "MISSING_FABRIC_SOURCE_NE_ZERO_WORLD_ACTIVITY",
            result["truth_boundaries"],
        )

    def test_post_ingest_shape_reaches_five_of_eight_without_promoting_remaining_gaps(self):
        operational = load_operational_sources(ROOT / "data/source_registry.csv")
        result = reconcile_live_observation_coverage(
            operational,
            _assessment({
                "CN_NBS": 4,
                "CN_PBOC_JS": 1,
                "JS_STATS": 1,
                "XZ_GGZY": 24,
                "EJY365_XZ_LINKED": 29,
            }),
        )
        self.assertEqual(result["adapter_supported_production_count"], 5)
        self.assertEqual(result["observed_production_count"], 5)
        self.assertEqual(result["adapter_supported_not_observed_count"], 0)
        self.assertEqual(result["no_unified_adapter_count"], 3)
        self.assertEqual(
            set(result["observed_production_source_ids"]),
            {"CN_NBS", "CN_PBOC_JS", "JS_STATS", "XZ_GGZY", "EJY365_XZ_LINKED"},
        )


if __name__ == "__main__":
    unittest.main()
