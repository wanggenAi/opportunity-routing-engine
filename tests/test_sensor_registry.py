import unittest
from pathlib import Path

from src.sensor_registry import (
    SensorCandidate,
    assess_sensor_candidate,
    load_sensor_candidates,
    sensor_candidate_from_dict,
)


ROOT = Path(__file__).resolve().parents[1]


class SensorRegistryTests(unittest.TestCase):
    def test_global_seed_sources_are_discovered_not_silently_activated(self):
        candidates = load_sensor_candidates(ROOT / "data" / "sensor_candidates.json")
        self.assertEqual(len(candidates), 4)
        for candidate in candidates:
            result = assess_sensor_candidate(candidate)
            self.assertEqual(candidate.lifecycle_state, "DISCOVERED")
            self.assertFalse(result["qualified"])
            self.assertFalse(result["automation_ready"])
            self.assertEqual(result["effective_state"], "DISCOVERED")
            self.assertIn(
                "CHINA_RELEVANCE_NOT_EVIDENCED",
                result["qualification_blockers"],
            )
            self.assertIn(
                "UNIQUE_SIGNAL_VALUE_UNASSESSED",
                result["qualification_blockers"],
            )

    def test_foreign_source_can_qualify_for_china_research_without_becoming_active(self):
        candidate = SensorCandidate(
            source_id="FUTURE_GLOBAL_FORUM",
            name="Future global forum",
            base_url="https://example.com",
            origin_geography="GLOBAL",
            relevance_geographies=("CN",),
            observable_dimensions=("PERCEPTION", "BEHAVIOR"),
            collection_mode="PUBLIC_MANUAL",
            provenance_refs=("source-identity",),
            china_relevance_evidence_refs=("china-topic-sample",),
            unique_signal_value="China-related early behavior discussion",
        )
        result = assess_sensor_candidate(candidate)
        self.assertTrue(result["qualified"])
        self.assertFalse(result["automation_ready"])
        self.assertEqual(result["effective_state"], "QUALIFIED")
        self.assertIn("MANUAL_ONLY_NOT_AUTOMATED", result["activation_blockers"])

    def test_authorized_source_requires_activation_evidence(self):
        candidate = SensorCandidate(
            source_id="AUTHORIZED_SOURCE",
            name="Authorized source",
            base_url="https://example.com",
            origin_geography="CN",
            relevance_geographies=("CN",),
            observable_dimensions=("BEHAVIOR",),
            collection_mode="AUTHORIZED_API",
            provenance_refs=("source-identity",),
            unique_signal_value="Direct behavior observations",
        )
        result = assess_sensor_candidate(candidate)
        self.assertTrue(result["qualified"])
        self.assertFalse(result["automation_ready"])
        self.assertIn(
            "ACTIVATION_PERMISSION_EVIDENCE_MISSING",
            result["activation_blockers"],
        )

    def test_authorized_source_with_evidence_can_be_activation_ready(self):
        candidate = SensorCandidate(
            source_id="AUTHORIZED_SOURCE",
            name="Authorized source",
            base_url="https://example.com",
            origin_geography="CN",
            relevance_geographies=("CN",),
            observable_dimensions=("BEHAVIOR", "FLOW"),
            collection_mode="AUTHORIZED_API",
            provenance_refs=("source-identity",),
            activation_evidence_refs=("api-authorization",),
            unique_signal_value="Direct behavior and flow evidence",
            lifecycle_state="QUALIFIED",
        )
        result = assess_sensor_candidate(candidate)
        self.assertTrue(result["automation_ready"])
        self.assertEqual(result["effective_state"], "ACTIVE_READY")

    def test_new_platform_name_does_not_require_code_change(self):
        candidate = sensor_candidate_from_dict(
            {
                "source_id": "PLATFORM_NOT_YET_INVENTED",
                "name": "A future platform",
                "base_url": "https://future.example",
                "origin_geography": "CN",
                "relevance_geographies": ["CN-JS-XZ"],
                "observable_dimensions": ["MOTIVE", "BEHAVIOR", "FRICTION"],
                "collection_mode": "PUBLIC_MANUAL",
                "provenance_refs": ["discovery-record"],
                "unique_signal_value": "Previously unseen local behavior signal"
            }
        )
        self.assertEqual(candidate.source_id, "PLATFORM_NOT_YET_INVENTED")
        self.assertEqual(candidate.observable_dimensions[-1], "FRICTION")

    def test_unknown_semantic_dimension_fails_closed(self):
        with self.assertRaises(ValueError):
            SensorCandidate(
                source_id="BAD",
                name="Bad source",
                base_url="https://example.com",
                origin_geography="CN",
                relevance_geographies=("CN",),
                observable_dimensions=("FIXED_MARKET_CATEGORY",),
                collection_mode="PUBLIC_MANUAL",
                provenance_refs=("ref",),
            )

    def test_loader_rejects_unknown_fields(self):
        with self.assertRaises(ValueError):
            sensor_candidate_from_dict(
                {
                    "source_id": "BAD",
                    "name": "Bad",
                    "base_url": "https://example.com",
                    "origin_geography": "CN",
                    "relevance_geographies": ["CN"],
                    "observable_dimensions": ["BEHAVIOR"],
                    "collection_mode": "PUBLIC_MANUAL",
                    "provenance_refs": ["ref"],
                    "market_taxonomy": "hard-coded"
                }
            )


if __name__ == "__main__":
    unittest.main()
