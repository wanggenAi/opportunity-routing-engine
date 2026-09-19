import copy
import tempfile
import unittest
from pathlib import Path

from src.observation_store import SQLiteObservationStore
from src.observed_patterns import summarize_observed_patterns
from src.research_observation_bridge import build_reviewed_research_observations, summarize_reviewed_research_observations


def _fixtures():
    evidence = {
        "evidence": [
            {
                "evidence_id": "ev-official",
                "source_url": "https://example.test/official",
                "source_family": "OFFICIAL",
                "origin_geography": "CN",
                "relevance_geography": "CN",
            },
            {
                "evidence_id": "ev-community",
                "source_url": "https://example.test/community",
                "source_family": "PUBLIC_COMMUNITY",
                "origin_geography": "CN",
                "relevance_geography": "CN",
            },
        ]
    }
    reviewed = {
        "schema_version": "reviewed-research-observations.v1",
        "semantics": "REVIEWED_SOURCE_CAPTURE_NOT_FULL_PAGE",
        "retrieved_at": "2026-09-19T12:00:00+08:00",
        "records": [
            {
                "observation_id": "obs-official",
                "research_evidence_id": "ev-official",
                "source_origin_geography": "CN",
                "relevance_geographies": ["CN"],
                "sampling_boundary": "SYNTHETIC_TEST_NOT_FULL_PAGE",
                "captured_payload": {"fixture": "official"},
                "actor_ids": ["actor:synthetic-a"],
                "evidence_excerpt": "Synthetic observation for bridge behavior only.",
                "source_id": "SYNTHETIC_OFFICIAL",
                "source_record_id": "record-a",
                "source_tier": "TEST",
                "observed_at": "2026-09-18T10:00:00+08:00",
                "unknown_fields": ["PERMISSION_UNKNOWN"],
                "claims": [
                    {
                        "claim_id": "claim-a",
                        "primitive": "BEHAVIOR",
                        "concept": "SYNTHETIC_WORKAROUND",
                        "epistemic_status": "OBSERVED",
                        "actor_id": "actor:synthetic-a",
                        "geography": "CN",
                    }
                ],
            },
            {
                "observation_id": "obs-community",
                "research_evidence_id": "ev-community",
                "source_origin_geography": "CN",
                "relevance_geographies": ["CN"],
                "sampling_boundary": "SYNTHETIC_TEST_NOT_FULL_PAGE",
                "captured_payload": {"fixture": "community"},
                "actor_ids": ["actor:synthetic-b"],
                "evidence_excerpt": "Synthetic community report for bridge behavior only.",
                "source_id": "SYNTHETIC_COMMUNITY",
                "source_record_id": "record-b",
                "source_tier": "TEST",
                "observed_at": "2026-09-19T10:00:00+08:00",
                "unknown_fields": [],
                "claims": [
                    {
                        "claim_id": "claim-b",
                        "primitive": "PERCEPTION",
                        "concept": "SYNTHETIC_REPORTED_SIGNAL",
                        "epistemic_status": "REPORTED",
                        "actor_id": "actor:synthetic-b",
                        "geography": "CN",
                    }
                ],
            },
        ],
    }
    return evidence, reviewed


class ResearchObservationBridgeTests(unittest.TestCase):
    def _build(self):
        evidence, reviewed = _fixtures()
        return build_reviewed_research_observations(evidence, reviewed)

    def test_reviewed_fixture_builds_truth_bounded_observations(self):
        envelopes = self._build()
        self.assertEqual(len(envelopes), 2)
        self.assertTrue(all("NOT_FULL_PAGE" in item.sampling_boundary for item in envelopes))
        self.assertTrue(all(len(item.raw_payload_hash) == 64 for item in envelopes))
        summary = summarize_reviewed_research_observations(envelopes)
        self.assertEqual(summary["business_promotion"], "NOT_PROMOTED")
        self.assertNotIn("opportunity_score", summary)

    def test_public_community_claim_remains_reported(self):
        envelopes = {item.observation_id: item for item in self._build()}
        self.assertEqual({claim.epistemic_status for claim in envelopes["obs-community"].claims}, {"REPORTED"})

    def test_unknown_fields_survive_without_manufacturing_permission(self):
        envelopes = {item.observation_id: item for item in self._build()}
        self.assertIn("PERMISSION_UNKNOWN", envelopes["obs-official"].unknown_fields)

    def test_research_observations_persist_without_manufacturing_recurrence(self):
        envelopes = self._build()
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "observations.sqlite") as store:
                transitions = [store.ingest(item) for item in envelopes]
                current = tuple(store.iter_current())
            self.assertEqual({item.kind for item in transitions}, {"FIRST_SEEN"})
            self.assertEqual(len(current), 2)
        patterns = summarize_observed_patterns(envelopes, research_scope_state="BROAD_DISCOVERY_READY")
        self.assertEqual(patterns["observed_pattern_count"], 0)
        self.assertGreater(patterns["unbound_pattern_count"], 0)
        self.assertEqual(patterns["business_promotion"], "NOT_PROMOTED")

    def test_unknown_research_evidence_id_fails_closed(self):
        evidence, reviewed = _fixtures()
        reviewed = copy.deepcopy(reviewed)
        reviewed["records"][0]["research_evidence_id"] = "missing"
        with self.assertRaisesRegex(ValueError, "unknown research evidence id"):
            build_reviewed_research_observations(evidence, reviewed)

    def test_commercial_truth_field_is_rejected(self):
        evidence, reviewed = _fixtures()
        reviewed = copy.deepcopy(reviewed)
        reviewed["records"][0]["payer"] = "invented"
        with self.assertRaisesRegex(ValueError, "commercial truth leaked"):
            build_reviewed_research_observations(evidence, reviewed)


if __name__ == "__main__":
    unittest.main()
