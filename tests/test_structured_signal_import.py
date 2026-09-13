import json
import tempfile
import unittest
from pathlib import Path

from src.live_resource_signals import AvailabilityState, PermissionState
from src.live_signal_ledger import TransitionKind
from src.live_signal_store import SQLiteSignalLedgerStore
from src.structured_signal_import import load_records, signal_from_record


class StructuredSignalImportTests(unittest.TestCase):
    def _record(self, **overrides):
        payload = {
            "signal_id": "manual-1",
            "source_id": "reviewed-public-observation",
            "observed_at": "2026-09-13T08:00:00+00:00",
            "actor_ref": "resource-node-1",
            "geography": "Xuzhou",
            "raw_text": "offers local paid errand help",
            "source_url": "https://example.com/public-item-1",
            "availability": "ADVERTISED",
            "permission": "UNKNOWN",
            "facts": [
                {"key": "offers_paid_offline_tasks", "value": True, "evidence_text": "offers local paid errand help"}
            ],
            "explicit_capabilities": [
                {"capability_key": "task.local_errand", "evidence_text": "explicitly offers local errand help"}
            ],
        }
        payload.update(overrides)
        return payload

    def test_reviewed_record_becomes_neutral_signal(self):
        signal = signal_from_record(self._record())
        self.assertEqual(signal.signal_id, "manual-1")
        self.assertEqual(signal.availability, AvailabilityState.ADVERTISED)
        self.assertEqual(signal.permission, PermissionState.UNKNOWN)
        self.assertEqual(signal.explicit_capabilities[0].capability_key, "task.local_errand")

    def test_structured_import_cannot_create_confirmed_availability(self):
        with self.assertRaisesRegex(ValueError, "intake_cannot_confirm_availability"):
            signal_from_record(self._record(availability="CONFIRMED"))

    def test_structured_import_cannot_create_permission(self):
        with self.assertRaisesRegex(ValueError, "intake_cannot_create_permission"):
            signal_from_record(self._record(permission="ALLOWED"))

    def test_explicit_capability_requires_evidence_text(self):
        record = self._record(explicit_capabilities=[{"capability_key": "task.local_errand"}])
        with self.assertRaisesRegex(ValueError, "evidence_text"):
            signal_from_record(record)

    def test_jsonl_and_json_array_loaders_are_deterministic(self):
        record = self._record()
        with tempfile.TemporaryDirectory() as tmp:
            jsonl = Path(tmp) / "signals.jsonl"
            jsonl.write_text(json.dumps(record) + "\n\n", encoding="utf-8")
            self.assertEqual(load_records(jsonl), (record,))

            json_path = Path(tmp) / "signals.json"
            json_path.write_text(json.dumps([record]), encoding="utf-8")
            self.assertEqual(load_records(json_path), (record,))

    def test_imported_signal_uses_same_durable_transition_semantics(self):
        first = signal_from_record(self._record())
        changed_record = self._record(
            observed_at="2026-09-13T09:00:00+00:00",
            facts=[
                {"key": "offers_paid_offline_tasks", "value": True, "evidence_text": "offers local paid errand help"},
                {"key": "local_mobility_observed", "value": True, "evidence_text": "states local travel is accepted"},
            ],
        )
        changed = signal_from_record(changed_record)

        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "signals.db"
            with SQLiteSignalLedgerStore(db) as store:
                self.assertEqual(store.ingest(first).kind, TransitionKind.FIRST_SEEN)
                transition = store.ingest(changed)
                self.assertEqual(transition.kind, TransitionKind.CHANGED)
                self.assertIn("facts", transition.changed_dimensions)


if __name__ == "__main__":
    unittest.main()
