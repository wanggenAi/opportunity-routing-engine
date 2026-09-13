import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.live_resource_signals import AvailabilityState, ExplicitCapability, ObservedFact, PermissionState, SignalObservation
from src.live_signal_intake import signal_from_record, signals_from_path
from src.live_signal_ledger import TransitionKind
from src.live_signal_store import SQLiteSignalLedgerStore


T0 = datetime(2026, 9, 13, 8, 0, tzinfo=timezone.utc)


def make_signal(*, observed_at=T0, availability=AvailabilityState.ADVERTISED):
    return SignalObservation(
        signal_id="item-1",
        source_id="sensor-a",
        observed_at=observed_at,
        actor_ref="resource-node-1",
        geography="Xuzhou",
        facts=(ObservedFact("offers_paid_offline_tasks", True, "public offer"),),
        explicit_capabilities=(ExplicitCapability("task.local_errand", "public offer"),),
        availability=availability,
        permission=PermissionState.UNKNOWN,
    )


class SQLiteSignalLedgerStoreTests(unittest.TestCase):
    def test_store_survives_reopen_and_rebuild_matches_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.db"
            with SQLiteSignalLedgerStore(path) as store:
                self.assertEqual(store.ingest(make_signal()).kind, TransitionKind.FIRST_SEEN)
                self.assertEqual(
                    store.ingest(make_signal(observed_at=T0 + timedelta(hours=1))).kind,
                    TransitionKind.REOBSERVED,
                )
                self.assertEqual(
                    store.ingest(
                        make_signal(
                            observed_at=T0 + timedelta(hours=2),
                            availability=AvailabilityState.CONFIRMED,
                        )
                    ).kind,
                    TransitionKind.CHANGED,
                )

            with SQLiteSignalLedgerStore(path) as reopened:
                current = reopened.get("sensor-a", "item-1")
                rebuilt = reopened.rebuild_entry("sensor-a", "item-1")
                self.assertIsNotNone(current)
                self.assertEqual(current, rebuilt)
                self.assertEqual(current.seen_count, 3)
                self.assertEqual(current.revision_count, 1)
                self.assertEqual(
                    [x.kind for x in reopened.transitions("sensor-a", "item-1")],
                    [TransitionKind.FIRST_SEEN, TransitionKind.REOBSERVED, TransitionKind.CHANGED],
                )

    def test_out_of_order_is_audited_but_does_not_replace_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.db"
            with SQLiteSignalLedgerStore(path) as store:
                store.ingest(make_signal(observed_at=T0 + timedelta(days=2)))
                before = store.get("sensor-a", "item-1")
                transition = store.ingest(make_signal(observed_at=T0))
                after = store.get("sensor-a", "item-1")
                self.assertEqual(transition.kind, TransitionKind.OUT_OF_ORDER)
                self.assertEqual(before, after)
                self.assertEqual(len(store.transitions("sensor-a", "item-1")), 2)


class NeutralSignalIntakeTests(unittest.TestCase):
    def _record(self):
        return {
            "signal_id": "item-1",
            "source_id": "manual-public-observation",
            "observed_at": "2026-09-13T16:00:00+08:00",
            "actor_ref": "resource-node-1",
            "geography": "Xuzhou",
            "source_url": "https://example.invalid/public-item",
            "facts": [
                {"key": "offers_paid_offline_tasks", "value": True, "evidence_text": "public offer"}
            ],
            "explicit_capabilities": [
                {"capability_key": "task.local_errand", "evidence_text": "public offer"}
            ],
            "availability": "ADVERTISED",
            "permission": "UNKNOWN",
        }

    def test_record_parses_without_upgrading_truth(self):
        signal = signal_from_record(self._record())
        self.assertEqual(signal.availability, AvailabilityState.ADVERTISED)
        self.assertEqual(signal.permission, PermissionState.UNKNOWN)
        self.assertEqual(signal.explicit_capabilities[0].capability_key, "task.local_errand")

    def test_invalid_permission_fails_closed(self):
        record = self._record()
        record["permission"] = "ASSUMED_ALLOWED"
        with self.assertRaisesRegex(ValueError, "invalid:permission"):
            signal_from_record(record)

    def test_jsonl_batch_ingests_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "observations.jsonl"
            db_path = Path(tmp) / "signals.db"
            first = self._record()
            second = dict(first)
            second["observed_at"] = "2026-09-13T17:00:00+08:00"
            second["availability"] = "CONFIRMED"
            input_path.write_text(
                json.dumps(first, ensure_ascii=False) + "\n" + json.dumps(second, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            with SQLiteSignalLedgerStore(db_path) as store:
                transitions = [store.ingest(signal) for signal in signals_from_path(input_path)]
                current = store.get("manual-public-observation", "item-1")

            self.assertEqual([x.kind for x in transitions], [TransitionKind.FIRST_SEEN, TransitionKind.CHANGED])
            self.assertEqual(current.current_payload["availability"], "CONFIRMED")


if __name__ == "__main__":
    unittest.main()
