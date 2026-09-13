import unittest
from datetime import datetime, timedelta, timezone

from src.live_resource_signals import (
    AvailabilityState,
    ExplicitCapability,
    ObservedFact,
    PermissionState,
    SignalObservation,
)
from src.live_signal_ledger import (
    SignalLedger,
    TransitionKind,
    observe_signal,
    semantic_fingerprint,
)


T0 = datetime(2026, 9, 13, 8, 0, tzinfo=timezone.utc)


def make_signal(*, observed_at=T0, raw_text="v1", availability=AvailabilityState.ADVERTISED, geography="Xuzhou"):
    return SignalObservation(
        signal_id="item-1",
        source_id="sensor-a",
        observed_at=observed_at,
        actor_ref="resource-node-1",
        geography=geography,
        raw_text=raw_text,
        facts=(ObservedFact("offers_paid_offline_tasks", True, "public offer"),),
        explicit_capabilities=(ExplicitCapability("task.local_errand", "public offer"),),
        availability=availability,
        permission=PermissionState.UNKNOWN,
    )


class LiveSignalLedgerTests(unittest.TestCase):
    def test_first_seen_then_reobserved(self):
        first, transition = observe_signal(None, make_signal())
        self.assertEqual(transition.kind, TransitionKind.FIRST_SEEN)
        second, transition = observe_signal(first, make_signal(observed_at=T0 + timedelta(days=1)))
        self.assertEqual(transition.kind, TransitionKind.REOBSERVED)
        self.assertEqual(second.seen_count, 2)
        self.assertEqual(second.revision_count, 0)

    def test_raw_text_cosmetic_change_is_not_semantic_change(self):
        first, _ = observe_signal(None, make_signal(raw_text="page wording A"))
        second, transition = observe_signal(
            first,
            make_signal(observed_at=T0 + timedelta(hours=1), raw_text="page wording B"),
        )
        self.assertEqual(transition.kind, TransitionKind.REOBSERVED)
        self.assertEqual(first.current_fingerprint, second.current_fingerprint)

    def test_availability_change_is_semantic_revision(self):
        first, _ = observe_signal(None, make_signal())
        second, transition = observe_signal(
            first,
            make_signal(
                observed_at=T0 + timedelta(hours=2),
                availability=AvailabilityState.CONFIRMED,
            ),
        )
        self.assertEqual(transition.kind, TransitionKind.CHANGED)
        self.assertIn("availability", transition.changed_dimensions)
        self.assertEqual(second.revision_count, 1)
        self.assertEqual(len(second.previous_fingerprints), 1)

    def test_out_of_order_signal_cannot_roll_back_latest_state(self):
        first, _ = observe_signal(None, make_signal(observed_at=T0 + timedelta(days=2)))
        same, transition = observe_signal(first, make_signal(observed_at=T0))
        self.assertEqual(transition.kind, TransitionKind.OUT_OF_ORDER)
        self.assertEqual(same, first)

    def test_stale_does_not_mean_disappeared(self):
        ledger = SignalLedger()
        ledger.ingest(make_signal())
        stale = ledger.stale_entries(T0 + timedelta(days=31), timedelta(days=30))
        self.assertEqual(len(stale), 1)
        self.assertEqual(stale[0].signal_id, "item-1")

    def test_semantic_fingerprint_is_deterministic(self):
        self.assertEqual(semantic_fingerprint(make_signal()), semantic_fingerprint(make_signal()))

    def test_stable_signal_id_cannot_switch_actor(self):
        first, _ = observe_signal(None, make_signal())
        conflicting = SignalObservation(
            **{**make_signal(observed_at=T0 + timedelta(hours=1)).__dict__, "actor_ref": "another-resource"}
        )
        with self.assertRaisesRegex(ValueError, "actor identity changed"):
            observe_signal(first, conflicting)


if __name__ == "__main__":
    unittest.main()
