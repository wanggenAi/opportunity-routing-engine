import json
import tempfile
import unittest
from pathlib import Path

from src.requirement_bundle_intake import (
    requirement_spec_from_record,
    requirement_specs_from_path,
)
from src.requirement_bundle_registry import SQLiteRequirementBundleRegistry


class ReviewedRequirementBundleIntakeTests(unittest.TestCase):
    def _record(self, **overrides):
        payload = {
            "bundle_id": "opp-1-capabilities",
            "version": 1,
            "required_capabilities": ["presence.local_execution", "mobility.local"],
            "geography": "Xuzhou",
            "source_ref": "opportunity:opp-1",
            "rationale": "reviewed decomposition of the bounded outcome",
            "active": True,
        }
        payload.update(overrides)
        return payload

    def test_reviewed_record_parses_without_demand_promotion(self):
        spec = requirement_spec_from_record(self._record())
        self.assertEqual(spec.bundle_id, "opp-1-capabilities")
        self.assertEqual(spec.version, 1)
        self.assertEqual(
            tuple(spec.required_capabilities),
            ("presence.local_execution", "mobility.local"),
        )
        self.assertEqual(spec.source_ref, "opportunity:opp-1")
        self.assertTrue(spec.active)

    def test_truth_promotion_fields_are_rejected(self):
        for field in (
            "demand_confirmed",
            "payer_committed",
            "transaction_ready",
            "consent_confirmed",
            "access_confirmed",
        ):
            with self.subTest(field=field):
                record = self._record(**{field: True})
                with self.assertRaisesRegex(ValueError, "truth promotion fields"):
                    requirement_spec_from_record(record)

    def test_unknown_fields_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown requirement fields"):
            requirement_spec_from_record(self._record(score=99))

    def test_source_ref_and_rationale_are_required(self):
        with self.assertRaisesRegex(ValueError, "missing:source_ref"):
            requirement_spec_from_record(self._record(source_ref=""))
        with self.assertRaisesRegex(ValueError, "missing:rationale"):
            requirement_spec_from_record(self._record(rationale=""))

    def test_version_and_active_types_are_strict(self):
        with self.assertRaisesRegex(ValueError, "version must be an integer"):
            requirement_spec_from_record(self._record(version=True))
        with self.assertRaisesRegex(ValueError, "active must be a boolean"):
            requirement_spec_from_record(self._record(active="true"))

    def test_json_and_jsonl_paths_parse_deterministically(self):
        first = self._record()
        second = self._record(
            version=2,
            required_capabilities=[
                "presence.local_execution",
                "mobility.local",
                "evidence.capture.photo_video",
            ],
            rationale="reviewed decomposition version 2",
        )
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "requirements.json"
            json_path.write_text(json.dumps([first, second]), encoding="utf-8")
            specs = tuple(requirement_specs_from_path(json_path))
            self.assertEqual(tuple(spec.version for spec in specs), (1, 2))

            jsonl_path = Path(tmp) / "requirements.jsonl"
            jsonl_path.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            specs = tuple(requirement_specs_from_path(jsonl_path))
            self.assertEqual(tuple(spec.version for spec in specs), (1, 2))

    def test_reviewed_intake_registers_versions_and_active_selection(self):
        first = self._record(active=True)
        second = self._record(
            version=2,
            required_capabilities=[
                "presence.local_execution",
                "mobility.local",
                "evidence.capture.photo_video",
            ],
            rationale="reviewed decomposition version 2",
            active=True,
        )
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "requirements.jsonl"
            input_path.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            with SQLiteRequirementBundleRegistry(Path(tmp) / "requirements.db") as registry:
                for spec in requirement_specs_from_path(input_path):
                    registry.register(spec)
                versions = registry.versions("opp-1-capabilities")
                self.assertEqual(tuple(item.version for item in versions), (1, 2))
                self.assertFalse(versions[0].active)
                self.assertTrue(versions[1].active)
                self.assertEqual(registry.active("opp-1-capabilities").version, 2)

    def test_reimport_same_reviewed_version_is_idempotent(self):
        spec = requirement_spec_from_record(self._record())
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteRequirementBundleRegistry(Path(tmp) / "requirements.db") as registry:
                registry.register(spec)
                registry.register(spec)
                self.assertEqual(len(registry.versions("opp-1-capabilities")), 1)


if __name__ == "__main__":
    unittest.main()
