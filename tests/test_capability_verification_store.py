import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from src.capability_verification_store import (
    CapabilityVerificationEvent,
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.live_resource_signals import (
    AvailabilityState,
    CapabilityClaim,
    EvidenceStatus,
    PermissionState,
)


NOW = datetime(2026, 9, 13, 13, 0, tzinfo=timezone.utc)


class CapabilityVerificationStoreTests(unittest.TestCase):
    def _event(
        self,
        *,
        verification_id="verify-1",
        verdict=VerificationVerdict.CONFIRMED,
        verified_at=NOW,
        availability=AvailabilityState.UNKNOWN,
        permission=PermissionState.UNKNOWN,
        related_signal_refs=("sensor-a::item-1",),
    ):
        return CapabilityVerificationEvent(
            verification_id=verification_id,
            actor_ref="actor-a",
            capability_key="cap.a",
            verdict=verdict,
            verified_at=verified_at,
            evidence_ref=f"evidence:{verification_id}",
            evidence_note=f"reviewed verification {verification_id}",
            geography="Xuzhou",
            availability=availability,
            permission=permission,
            related_signal_refs=related_signal_refs,
        )

    def _base_claim(self, *, observed_at=NOW - timedelta(hours=1)):
        return CapabilityClaim(
            actor_ref="actor-a",
            capability_key="cap.a",
            evidence_status=EvidenceStatus.OBSERVED,
            source_signal_ids=("sensor-a::item-1",),
            rationale="public observation",
            last_observed_at=observed_at,
            geography="Xuzhou",
            availability=AvailabilityState.ADVERTISED,
            permission=PermissionState.UNKNOWN,
        )

    def test_append_is_durable_idempotent_and_conflicting_id_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "verification.db"
            event = self._event()
            with SQLiteCapabilityVerificationStore(path) as store:
                store.append(event)
                store.append(event)
                self.assertEqual(len(store.events()), 1)

                conflict = CapabilityVerificationEvent(
                    **{
                        **event.__dict__,
                        "evidence_note": "different evidence under same immutable id",
                    }
                )
                with self.assertRaisesRegex(ValueError, "different content"):
                    store.append(conflict)

            with SQLiteCapabilityVerificationStore(path) as reopened:
                stored = reopened.get("verify-1")
                self.assertIsNotNone(stored)
                self.assertEqual(stored.verdict, VerificationVerdict.CONFIRMED)
                self.assertEqual(stored.related_signal_refs, ("sensor-a::item-1",))

    def test_confirmation_does_not_imply_callability(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                store.append(self._event())
                projected = store.project_claims((self._base_claim(),), as_of=NOW)
                confirmed = next(
                    claim for claim in projected if claim.evidence_status is EvidenceStatus.CONFIRMED
                )
                self.assertEqual(
                    confirmed.source_signal_ids,
                    ("verification::verify-1", "sensor-a::item-1"),
                )
                self.assertFalse(confirmed.is_callable(NOW, timedelta(days=30)))

    def test_explicit_availability_permission_and_freshness_can_make_confirmed_claim_callable(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                store.append(
                    self._event(
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                    )
                )
                confirmed = next(
                    claim
                    for claim in store.project_claims((self._base_claim(),), as_of=NOW)
                    if claim.evidence_status is EvidenceStatus.CONFIRMED
                )
                self.assertTrue(confirmed.is_callable(NOW + timedelta(days=1), timedelta(days=30)))
                self.assertFalse(confirmed.is_callable(NOW + timedelta(days=31), timedelta(days=30)))

    def test_rejection_suppresses_older_base_claim_without_rewriting_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                base = self._base_claim(observed_at=NOW - timedelta(days=1))
                store.append(
                    self._event(
                        verification_id="reject-1",
                        verdict=VerificationVerdict.REJECTED,
                        related_signal_refs=("sensor-a::item-1",),
                    )
                )
                projected = store.project_claims((base,), as_of=NOW)
                self.assertEqual(projected, ())
                self.assertEqual(base.evidence_status, EvidenceStatus.OBSERVED)
                self.assertEqual(base.source_signal_ids, ("sensor-a::item-1",))

    def test_newer_observation_reopens_rejected_capability_as_unverified(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                store.append(
                    self._event(
                        verification_id="reject-1",
                        verdict=VerificationVerdict.REJECTED,
                        verified_at=NOW,
                    )
                )
                newer = self._base_claim(observed_at=NOW + timedelta(hours=1))
                projected = store.project_claims(
                    (newer,), as_of=NOW + timedelta(hours=2)
                )
                self.assertEqual(projected, (newer,))
                self.assertEqual(projected[0].evidence_status, EvidenceStatus.OBSERVED)

    def test_latest_verification_event_controls_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                store.append(
                    self._event(
                        verification_id="confirm-1",
                        verified_at=NOW,
                        availability=AvailabilityState.CONFIRMED,
                        permission=PermissionState.ALLOWED,
                    )
                )
                store.append(
                    self._event(
                        verification_id="reject-2",
                        verdict=VerificationVerdict.REJECTED,
                        verified_at=NOW + timedelta(hours=2),
                    )
                )
                before_rejection = store.project_claims(
                    (self._base_claim(),), as_of=NOW + timedelta(hours=1)
                )
                after_rejection = store.project_claims(
                    (self._base_claim(),), as_of=NOW + timedelta(hours=3)
                )
                self.assertTrue(
                    any(claim.evidence_status is EvidenceStatus.CONFIRMED for claim in before_rejection)
                )
                self.assertEqual(after_rejection, ())

    def test_rejected_event_cannot_smuggle_availability_or_permission(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                with self.assertRaisesRegex(ValueError, "rejected_capability_must_not_set_availability"):
                    store.append(
                        self._event(
                            verdict=VerificationVerdict.REJECTED,
                            availability=AvailabilityState.CONFIRMED,
                        )
                    )
                with self.assertRaisesRegex(ValueError, "rejected_capability_must_not_set_permission"):
                    store.append(
                        self._event(
                            verdict=VerificationVerdict.REJECTED,
                            permission=PermissionState.RESTRICTED,
                        )
                    )

    def test_confirmation_does_not_accept_advertised_as_verified_availability(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                with self.assertRaisesRegex(ValueError, "confirmed_availability_advertised"):
                    store.append(
                        self._event(availability=AvailabilityState.ADVERTISED)
                    )

    def test_snapshot_fingerprint_is_time_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                store.append(self._event(verification_id="confirm-1", verified_at=NOW))
                before = store.snapshot_fingerprint(as_of=NOW + timedelta(minutes=1))
                store.append(
                    self._event(
                        verification_id="confirm-2",
                        verified_at=NOW + timedelta(hours=2),
                        availability=AvailabilityState.COMMITTED,
                        permission=PermissionState.ALLOWED,
                    )
                )
                same_past = store.snapshot_fingerprint(as_of=NOW + timedelta(minutes=1))
                future = store.snapshot_fingerprint(as_of=NOW + timedelta(hours=3))
                self.assertEqual(before, same_past)
                self.assertNotEqual(before, future)


if __name__ == "__main__":
    unittest.main()
