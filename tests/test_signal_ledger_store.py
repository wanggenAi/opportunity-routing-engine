import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_ledger import SignalLedger, TransitionKind
from src.signal_ledger_store import JsonSignalLedgerStore


NOW = datetime(2026, 9, 13, 8, 0, tzinfo=timezone.utc)


class SignalLedgerStoreTests(unittest.TestCase):
    def _signal(self, when=NOW, *, availability=AvailabilityState.ADVERTISED):
        return SignalObservation(
            signal_id="sig-1",
            source_id="sensor-1",
            observed_at=when,
            actor_ref="actor-1",
            geography="Xuzhou",
            facts=(ObservedFact("offers_paid_offline_tasks", True, "public offer"),),
            explicit_capabilities=(ExplicitCapability("task.local_errand", "explicit offer"),),
            availability=availability,
            permission=PermissionState.UNKNOWN,
        )

    def test_round_trip_preserves_temporal_state_without_creating_new_observation(self):
        ledger = SignalLedger()
        self.assertEqual(ledger.ingest(self._signal()).kind, TransitionKind.FIRST_SEEN)
        self.assertEqual(
            ledger.ingest(self._signal(NOW + timedelta(hours=2))).kind,
            TransitionKind.REOBSERVED,
        )
        self.assertEqual(
            ledger.ingest(
                self._signal(
                    NOW + timedelta(hours=4),
                    availability=AvailabilityState.CONFIRMED,
                )
            ).kind,
            TransitionKind.CHANGED,
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            store = JsonSignalLedgerStore(path)
            store.save(ledger)
            restored = store.load()

        entry = restored.get("sensor-1", "sig-1")
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry.first_seen_at, NOW)
        self.assertEqual(entry.last_seen_at, NOW + timedelta(hours=4))
        self.assertEqual(entry.seen_count, 3)
        self.assertEqual(entry.revision_count, 1)
        self.assertEqual(len(entry.previous_fingerprints), 1)

    def test_missing_file_is_a_valid_empty_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            restored = JsonSignalLedgerStore(Path(tmp) / "missing.json").load()
            self.assertEqual(restored.entries(), ())

    def test_corrupt_json_fails_closed_instead_of_resetting_world(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text("{not-json", encoding="utf-8")
            with self.assertRaises(ValueError):
                JsonSignalLedgerStore(path).load()

    def test_schema_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text(
                json.dumps({"schema_version": 999, "entries": []}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                JsonSignalLedgerStore(path).load()

    def test_duplicate_persisted_identity_is_rejected(self):
        ledger = SignalLedger()
        ledger.ingest(self._signal())
        entry = ledger.entries()[0]
        record = {
            "schema_version": 1,
            "entries": [
                {
                    "source_id": entry.source_id,
                    "signal_id": entry.signal_id,
                    "actor_ref": entry.actor_ref,
                    "first_seen_at": entry.first_seen_at.isoformat(),
                    "last_seen_at": entry.last_seen_at.isoformat(),
                    "seen_count": entry.seen_count,
                    "revision_count": entry.revision_count,
                    "current_fingerprint": entry.current_fingerprint,
                    "current_payload": dict(entry.current_payload),
                    "previous_fingerprints": [],
                }
            ] * 2,
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            with self.assertRaises(ValueError):
                JsonSignalLedgerStore(path).load()


if __name__ == "__main__":
    unittest.main()
