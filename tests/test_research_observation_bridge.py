import json
import tempfile
import unittest
from pathlib import Path

from src.observation_store import SQLiteObservationStore
from src.observed_patterns import summarize_observed_patterns
from src.research_observation_bridge import (
    build_reviewed_research_observations,
    summarize_reviewed_research_observations,
)


RUN_DIR = Path("data/research_runs/BROAD_DISCOVERY_RUN_001_2026-09-14")


class ResearchObservationBridgeTests(unittest.TestCase):
    def _build(self):
        evidence = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        reviewed = json.loads((RUN_DIR / "reviewed_observations.json").read_text(encoding="utf-8"))
        return build_reviewed_research_observations(evidence, reviewed)

    def test_reviewed_run_builds_seven_truth_bounded_observations(self):
        envelopes = self._build()
        self.assertEqual(len(envelopes), 7)
        self.assertEqual(len({item.observation_id for item in envelopes}), 7)
        self.assertTrue(all("NOT_FULL_PAGE" in item.sampling_boundary for item in envelopes))
        self.assertTrue(all(len(item.raw_payload_hash) == 64 for item in envelopes))
        summary = summarize_reviewed_research_observations(envelopes)
        self.assertEqual(summary["business_promotion"], "NOT_PROMOTED")
        self.assertNotIn("opportunity_score", summary)

    def test_secondary_media_claims_remain_reported(self):
        envelopes = {item.observation_id: item for item in self._build()}
        ltc = envelopes["bd001-obs-xz-primary-medical-ltc-20260119"]
        self.assertEqual({claim.epistemic_status for claim in ltc.claims}, {"REPORTED"})
        ai_cs = envelopes["bd001-obs-ai-customer-service-friction-h1-2026"]
        self.assertEqual({claim.epistemic_status for claim in ai_cs.claims}, {"REPORTED"})

    def test_first_party_xuzhou_metro_keeps_resource_permission_unknown(self):
        envelopes = {item.observation_id: item for item in self._build()}
        metro = envelopes["bd001-obs-xz-metro-idle-space-20260619"]
        self.assertIn("RESOURCE_MARKET_AVAILABILITY_UNKNOWN", metro.unknown_fields)
        self.assertIn("OPERATOR_PERMISSION_UNKNOWN", metro.unknown_fields)
        self.assertEqual(metro.actor_ids, ("actor:xuzhou-metro-group",))
        self.assertEqual(
            {claim.primitive for claim in metro.claims},
            {"RESOURCE", "BEHAVIOR", "FRICTION"},
        )

    def test_research_observations_persist_without_manufacturing_recurrence(self):
        envelopes = self._build()
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteObservationStore(Path(tmp) / "observations.sqlite") as store:
                transitions = [store.ingest(item) for item in envelopes]
                current = tuple(store.iter_current())
            self.assertEqual({item.kind for item in transitions}, {"FIRST_SEEN"})
            self.assertEqual(len(current), 7)

        patterns = summarize_observed_patterns(
            envelopes,
            research_scope_state="BROAD_DISCOVERY_READY",
        )
        self.assertEqual(patterns["research_scope_state"], "BROAD_DISCOVERY_READY")
        self.assertTrue(patterns["broad_discovery_use_authorized"])
        self.assertEqual(patterns["observed_pattern_count"], 0)
        self.assertGreater(patterns["unbound_pattern_count"], 0)
        self.assertEqual(patterns["business_promotion"], "NOT_PROMOTED")

    def test_unknown_research_evidence_id_fails_closed(self):
        evidence = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        reviewed = json.loads((RUN_DIR / "reviewed_observations.json").read_text(encoding="utf-8"))
        reviewed["records"][0]["research_evidence_id"] = "missing"
        with self.assertRaisesRegex(ValueError, "unknown research evidence id"):
            build_reviewed_research_observations(evidence, reviewed)

    def test_commercial_truth_field_is_rejected(self):
        evidence = json.loads((RUN_DIR / "evidence.json").read_text(encoding="utf-8"))
        reviewed = json.loads((RUN_DIR / "reviewed_observations.json").read_text(encoding="utf-8"))
        reviewed["records"][0]["payer"] = "invented"
        with self.assertRaisesRegex(ValueError, "commercial truth leaked"):
            build_reviewed_research_observations(evidence, reviewed)


if __name__ == "__main__":
    unittest.main()
