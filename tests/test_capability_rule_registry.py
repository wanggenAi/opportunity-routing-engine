import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.capability_rule_registry import CapabilityRuleRegistry
from src.live_resource_signals import (
    AvailabilityState,
    EvidenceStatus,
    ObservedFact,
    PermissionState,
    SignalObservation,
)


NOW = datetime(2026, 9, 13, 8, 0, tzinfo=timezone.utc)


class CapabilityRuleRegistryTests(unittest.TestCase):
    def _signal(self):
        return SignalObservation(
            signal_id="sig-1",
            source_id="sensor-1",
            observed_at=NOW,
            actor_ref="actor-1",
            geography="Xuzhou",
            facts=(
                ObservedFact("offers_paid_offline_tasks", True, "public offer"),
                ObservedFact("local_mobility_observed", True, "local travel task"),
            ),
            availability=AvailabilityState.ADVERTISED,
            permission=PermissionState.UNKNOWN,
        )

    def _payload(self):
        return {
            "schema_version": 1,
            "rules": [
                {
                    "rule_id": "r-presence",
                    "capability_key": "presence.local_execution",
                    "rationale": "offline work supports a local-presence hypothesis",
                    "conditions": [
                        {"key": "offers_paid_offline_tasks", "expected_value": True}
                    ],
                },
                {
                    "rule_id": "r-new-open-ended",
                    "capability_key": "future.capability.not_predeclared",
                    "rationale": "open namespace remains extensible",
                    "conditions": [
                        {"key": "local_mobility_observed", "expected_value": True}
                    ],
                },
            ],
        }

    def test_registry_infers_only_hypothesis_capabilities(self):
        registry = CapabilityRuleRegistry.from_mapping(self._payload())
        claims = registry.infer(self._signal())
        by_key = {claim.capability_key: claim for claim in claims}

        self.assertEqual(by_key["presence.local_execution"].evidence_status, EvidenceStatus.INFERRED)
        self.assertEqual(by_key["future.capability.not_predeclared"].evidence_status, EvidenceStatus.INFERRED)
        self.assertEqual(by_key["presence.local_execution"].inference_rule_id, "r-presence")

    def test_missing_fact_does_not_infer_capability(self):
        payload = self._payload()
        payload["rules"] = [
            {
                "rule_id": "r-camera",
                "capability_key": "capture.mobile_photo_video",
                "rationale": "requires explicit device/capture evidence",
                "conditions": [
                    {"key": "smartphone_available", "expected_value": True}
                ],
            }
        ]
        registry = CapabilityRuleRegistry.from_mapping(payload)
        self.assertEqual(registry.infer(self._signal()), [])

    def test_duplicate_rule_id_is_rejected(self):
        payload = self._payload()
        payload["rules"].append(dict(payload["rules"][0]))
        with self.assertRaises(ValueError):
            CapabilityRuleRegistry.from_mapping(payload)

    def test_schema_mismatch_is_rejected(self):
        payload = self._payload()
        payload["schema_version"] = 2
        with self.assertRaises(ValueError):
            CapabilityRuleRegistry.from_mapping(payload)

    def test_json_registry_round_trip_loads_reviewable_rule_data(self):
        payload = self._payload()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "rules.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            registry = CapabilityRuleRegistry.load_json(path)
        self.assertEqual(registry.as_mapping(), payload)


if __name__ == "__main__":
    unittest.main()
