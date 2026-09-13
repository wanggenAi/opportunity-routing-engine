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


def make_signal(
    *,
    observed_at=T0,
    availability=AvailabilityState.ADVERTISED,
    raw_text="public offer text",
    source_url="https://example.invalid/item-1",
):
    return SignalObservation(
        signal_id="item-1",
        source_id="sensor-a",
        observed_at=observed_at,
        actor_ref="resource-node-1",
        geography="Xuzhou",
        raw_text=raw_text,
        source_url=source_url,
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

    def test_raw_observations_survive_reopen_with_provenance_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.db"
            original = make_signal(raw_text="exact public wording", source_url="https://example.invalid/source")
            with SQLiteSignalLedgerStore(path) as store:
                store.ingest(original)

            with SQLiteSignalLedgerStore(path) as reopened:
                archived = reopened.observations("sensor-a", "item-1")

            self.assertEqual(len(archived), 1)
            self.assertEqual(archived[0], original)
            self.assertEqual(archived[0].raw_text, "exact public wording")
            self.assertEqual(archived[0].source_url, "https://example.invalid/source")
            self.assertEqual(archived[0].facts[0].evidence_text, "public offer")
            self.assertEqual(archived[0].explicit_capabilities[0].capability_key, "task.local_errand")

    def test_out_of_order_observation_is_archived_even_when_current_state_does_not_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.db"
            newer = make_signal(observed_at=T0 + timedelta(days=2), raw_text="newer")
            older = make_signal(observed_at=T0, raw_text="older")
            with SQLiteSignalLedgerStore(path) as store:
                store.ingest(newer)
                before = store.get("sensor-a", "item-1")
                transition = store.ingest(older)
                after = store.get("sensor-a", "item-1")
                archived = store.observations("sensor-a", "item-1")

            self.assertEqual(transition.kind, TransitionKind.OUT_OF_ORDER)
            self.assertEqual(before, after)
            self.assertEqual([item.raw_text for item in archived], ["newer", "older"])

    def test_exact_duplicate_observation_archive_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.db"
            signal = make_signal()
            with SQLiteSignalLedgerStore(path) as store:
                store.ingest(signal)
                store.ingest(signal)
                archived = store.observations("sensor-a", "item-1")
            self.assertEqual(archived, (signal,))

    def test_non_json_fact_value_fails_before_persisting_evidence(self):
        signal = SignalObservation(
            signal_id="bad-1",
            source_id="sensor-a",
            observed_at=T0,
            actor_ref="resource-node-1",
            facts=(ObservedFact("opaque", object(), "opaque runtime object"),),
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "signals.db"
            with SQLiteSignalLedgerStore(path) as store:
                with self.assertRaisesRegex(ValueError, "JSON-serializable"):
                    store.ingest(signal)
                self.assertIsNone(store.get("sensor-a", "bad-1"))
                self.assertEqual(store.observations("sensor-a", "bad-1"), ())

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

    def test_reviewed_intake_cannot_self_declare_confirmed_availability(self):
        record = self._record()
        record["availability"] = "CONFIRMED"
        with self.assertRaisesRegex(ValueError, "intake_cannot_confirm_availability"):
            signal_from_record(record)

    def test_reviewed_intake_cannot_self_declare_permission(self):
        record = self._record()
        record["permission"] = "ALLOWED"
        with self.assertRaisesRegex(ValueError, "intake_cannot_create_permission"):
            signal_from_record(record)

    def test_jsonl_batch_ingests_end_to_end_without_truth_upgrade(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "observations.jsonl"
            db_path = Path(tmp) / "signals.db"
            first = self._record()
            second = dict(first)
            second["observed_at"] = "2026-09-13T17:00:00+08:00"
            second["facts"] = list(first["facts"]) + [
                {
                    "key": "local_mobility_observed",
                    "value": True,
                    "evidence_text": "public offer includes local travel",
                }
            ]
            input_path.write_text(
                json.dumps(first, ensure_ascii=False) + "\n" + json.dumps(second, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

            with SQLiteSignalLedgerStore(db_path) as store:
                transitions = [store.ingest(signal) for signal in signals_from_path(input_path)]
                current = store.get("manual-public-observation", "item-1")
                archived = store.observations("manual-public-observation", "item-1")

            self.assertEqual([x.kind for x in transitions], [TransitionKind.FIRST_SEEN, TransitionKind.CHANGED])
            self.assertEqual(current.current_payload["availability"], "ADVERTISED")
            self.assertEqual(len(current.current_payload["facts"]), 2)
            self.assertEqual(len(archived), 2)


if __name__ == "__main__":
    unittest.main()
