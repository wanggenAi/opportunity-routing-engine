import json
import tempfile
import unittest
from pathlib import Path

from src.sensor_evidence_channel_coverage import (
    EvidenceChannelDefinition,
    load_evidence_channel_registry,
    reconcile_sensor_evidence_channel_coverage,
)
from src.sensor_portfolio import load_operational_sources
from src.sensor_registry import load_sensor_candidates


ROOT = Path(__file__).resolve().parents[1]
PRODUCTION_IDS = {
    "CN_CUSTOMS",
    "CN_NBS",
    "CN_PBOC",
    "CN_PBOC_JS",
    "EJY365_XZ_LINKED",
    "JS_STATS",
    "QM",
    "XZ_GGZY",
    "XZ_GOV_FINANCE_DEMAND",
}


def live_coverage(*, observed=None, supported=None, production=None):
    production_ids = set(PRODUCTION_IDS if production is None else production)
    supported_ids = set(production_ids if supported is None else supported)
    observed_ids = set(supported_ids if observed is None else observed)
    return {
        "schema_version": "live-observation-coverage.v1",
        "production_live_registry_count": len(production_ids),
        "adapter_supported_production_count": len(supported_ids),
        "observed_production_count": len(observed_ids),
        "production_live_source_ids": sorted(production_ids),
        "adapter_supported_production_source_ids": sorted(supported_ids),
        "observed_production_source_ids": sorted(observed_ids),
        "adapter_supported_not_observed_source_ids": sorted(supported_ids - observed_ids),
        "no_unified_adapter_source_ids": sorted(production_ids - supported_ids),
    }


class SensorEvidenceChannelCoverageTests(unittest.TestCase):
    def _actual(self):
        operational = load_operational_sources(ROOT / "data/source_registry.csv")
        candidates = load_sensor_candidates(ROOT / "data/sensor_candidates.json")
        channels = load_evidence_channel_registry(ROOT / "data/evidence_channel_registry.json")
        return operational, candidates, channels

    def test_current_registry_exposes_four_observed_channels_and_two_blind_spots(self):
        operational, candidates, channels = self._actual()
        result = reconcile_sensor_evidence_channel_coverage(
            operational, candidates, live_coverage(), channels
        )
        self.assertEqual(result["channel_count"], 6)
        self.assertEqual(result["production_live_channel_count"], 4)
        self.assertEqual(result["observed_channel_count"], 4)
        self.assertEqual(result["blind_spot_channel_count"], 2)
        self.assertEqual(
            set(result["observed_channel_ids"]),
            {
                "OFFICIAL_STRUCTURAL_BASELINE",
                "HARD_BEHAVIOR_MONEY",
                "LOCAL_REALITY",
                "REPRESENTATIVE_RESEARCH",
            },
        )
        self.assertEqual(
            set(result["blind_spot_channel_ids"]),
            {"SEARCH_INTENT", "SOCIAL_PUBLIC_DISCOURSE"},
        )
        self.assertEqual(result["unmapped_operational_source_ids"], [])
        self.assertEqual(result["unmapped_candidate_source_ids"], [])
        self.assertEqual(set(result["mapped_observed_production_source_ids"]), PRODUCTION_IDS)

    def test_representative_research_is_observed_only_because_qm_is_live_and_observed(self):
        operational, candidates, channels = self._actual()
        result = reconcile_sensor_evidence_channel_coverage(
            operational, candidates, live_coverage(), channels
        )
        row = next(
            item for item in result["channels"] if item["channel_id"] == "REPRESENTATIVE_RESEARCH"
        )
        self.assertEqual(row["coverage_state"], "OBSERVED_PRODUCTION")
        self.assertFalse(row["blind_spot"])
        self.assertEqual(row["production_live_source_ids"], ["QM"])
        self.assertEqual(row["observed_production_source_ids"], ["QM"])
        self.assertEqual(row["registered_nonlive_source_ids"], [])

    def test_registered_manual_search_surface_is_not_observed_coverage(self):
        operational, candidates, channels = self._actual()
        result = reconcile_sensor_evidence_channel_coverage(
            operational, candidates, live_coverage(), channels
        )
        row = next(item for item in result["channels"] if item["channel_id"] == "SEARCH_INTENT")
        self.assertEqual(row["coverage_state"], "REGISTERED_NONLIVE_ONLY")
        self.assertTrue(row["blind_spot"])
        self.assertEqual(row["production_live_source_ids"], [])
        self.assertEqual(row["observed_production_source_ids"], [])
        self.assertEqual(row["manual_surface_source_ids"], ["BAIDU_INDEX"])

    def test_social_candidates_and_manual_surfaces_do_not_promote_the_channel(self):
        operational, candidates, channels = self._actual()
        result = reconcile_sensor_evidence_channel_coverage(
            operational, candidates, live_coverage(), channels
        )
        row = next(
            item for item in result["channels"] if item["channel_id"] == "SOCIAL_PUBLIC_DISCOURSE"
        )
        self.assertEqual(row["coverage_state"], "REGISTERED_NONLIVE_ONLY")
        self.assertTrue(row["blind_spot"])
        self.assertEqual(row["production_live_source_ids"], [])
        self.assertEqual(row["observed_production_source_ids"], [])
        self.assertEqual(row["candidate_automation_ready_source_ids"], [])
        self.assertEqual(len(row["candidate_source_ids"]), 4)

    def test_one_observed_source_ne_channel_completeness(self):
        operational, candidates, channels = self._actual()
        result = reconcile_sensor_evidence_channel_coverage(
            operational, candidates, live_coverage(), channels
        )
        self.assertIn(
            "ONE_OBSERVED_SOURCE_NE_CHANNEL_COMPLETENESS",
            result["truth_boundaries"],
        )
        self.assertIn(
            "OBSERVED_CHANNEL_NE_REPRESENTATIVE_POPULATION_COVERAGE",
            result["truth_boundaries"],
        )

    def test_unknown_bound_source_fails_closed(self):
        operational, candidates, _ = self._actual()
        channels = (
            EvidenceChannelDefinition(
                channel_id="UNKNOWN_TEST",
                description="synthetic",
                semantic_dimensions=("STATE",),
                operational_source_ids=("DOES_NOT_EXIST",),
                candidate_source_ids=(),
            ),
        )
        with self.assertRaisesRegex(ValueError, "unknown sources"):
            reconcile_sensor_evidence_channel_coverage(
                operational, candidates, live_coverage(), channels
            )

    def test_stale_live_coverage_cannot_disagree_with_operational_registry(self):
        operational, candidates, channels = self._actual()
        stale = set(PRODUCTION_IDS)
        stale.remove("QM")
        with self.assertRaisesRegex(ValueError, "diverges from operational registry"):
            reconcile_sensor_evidence_channel_coverage(
                operational,
                candidates,
                live_coverage(production=stale),
                channels,
            )

    def test_registry_is_dynamic_data_but_semantic_dimensions_remain_kernel_bound(self):
        payload = {
            "schema_version": "sensor-evidence-channel-registry.v1",
            "channels": [
                {
                    "channel_id": "DYNAMIC_TEST",
                    "description": "synthetic",
                    "semantic_dimensions": ["NOT_A_KERNEL_PRIMITIVE"],
                    "operational_source_ids": ["CN_NBS"],
                    "candidate_source_ids": [],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "channels.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown semantic dimensions"):
                load_evidence_channel_registry(path)


if __name__ == "__main__":
    unittest.main()
