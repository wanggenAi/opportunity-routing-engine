import json
import tempfile
import unittest
from pathlib import Path

from src.capability_verification_intake import (
    verification_event_from_record,
    verification_events_from_path,
)
from src.capability_verification_store import (
    SQLiteCapabilityVerificationStore,
    VerificationVerdict,
)
from src.live_resource_signals import AvailabilityState, PermissionState


class ReviewedCapabilityVerificationIntakeTests(unittest.TestCase):
    def _record(self, **overrides):
        payload = {
            "verification_id": "verify-1",
            "actor_ref": "actor-a",
            "capability_key": "cap.a",
            "verdict": "CONFIRMED",
            "verified_at": "2026-09-13T22:00:00+08:00",
            "evidence_ref": "field-check:verify-1",
            "evidence_note": "reviewed direct capability check",
            "geography": "Xuzhou",
            "availability": "CONFIRMED",
            "permission": "ALLOWED",
            "related_signal_refs": ["sensor-a::item-1"],
        }
        payload.update(overrides)
        return payload

    def test_confirmed_record_requires_explicit_evidence_and_parses_truth_dimensions(self):
        event = verification_event_from_record(self._record())
        self.assertEqual(event.verdict, VerificationVerdict.CONFIRMED)
        self.assertEqual(event.availability, AvailabilityState.CONFIRMED)
        self.assertEqual(event.permission, PermissionState.ALLOWED)
        self.assertEqual(event.evidence_ref, "field-check:verify-1")
        self.assertEqual(event.related_signal_refs, ("sensor-a::item-1",))

    def test_transaction_truth_fields_are_rejected(self):
        for field in (
            "counterparty_consented",
            "payer_committed",
            "transaction_ready",
            "access_approved",
            "safety_approved",
        ):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "transaction truth fields"):
                    verification_event_from_record(self._record(**{field: True}))

    def test_unknown_fields_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown verification fields"):
            verification_event_from_record(self._record(score=100))

    def test_evidence_ref_note_and_timezone_are_required(self):
        with self.assertRaisesRegex(ValueError, "missing:evidence_ref"):
            verification_event_from_record(self._record(evidence_ref=""))
        with self.assertRaisesRegex(ValueError, "missing:evidence_note"):
            verification_event_from_record(self._record(evidence_note=""))
        with self.assertRaisesRegex(ValueError, "verified_at_must_be_timezone_aware"):
            verification_event_from_record(
                self._record(verified_at="2026-09-13T22:00:00")
            )

    def test_rejected_record_cannot_carry_availability_or_permission_promotion(self):
        with self.assertRaisesRegex(ValueError, "rejected_capability_must_not_set_availability"):
            verification_event_from_record(
                self._record(
                    verdict="REJECTED",
                    availability="CONFIRMED",
                    permission="UNKNOWN",
                )
            )
        with self.assertRaisesRegex(ValueError, "rejected_capability_must_not_set_permission"):
            verification_event_from_record(
                self._record(
                    verdict="REJECTED",
                    availability="UNKNOWN",
                    permission="RESTRICTED",
                )
            )

    def test_jsonl_intake_registers_confirmation_and_rejection_history(self):
        confirmed = self._record()
        rejected = self._record(
            verification_id="verify-2",
            verdict="REJECTED",
            verified_at="2026-09-13T23:00:00+08:00",
            evidence_ref="field-check:verify-2",
            evidence_note="later direct check rejected capability",
            availability="UNKNOWN",
            permission="UNKNOWN",
        )
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "verification.jsonl"
            input_path.write_text(
                json.dumps(confirmed) + "\n" + json.dumps(rejected) + "\n",
                encoding="utf-8",
            )
            events = tuple(verification_events_from_path(input_path))
            self.assertEqual(
                tuple(event.verification_id for event in events),
                ("verify-1", "verify-2"),
            )
            with SQLiteCapabilityVerificationStore(Path(tmp) / "verification.db") as store:
                for event in events:
                    store.append(event)
                stored = store.events()
                self.assertEqual(len(stored), 2)
                self.assertEqual(stored[-1].verdict, VerificationVerdict.REJECTED)


if __name__ == "__main__":
    unittest.main()
