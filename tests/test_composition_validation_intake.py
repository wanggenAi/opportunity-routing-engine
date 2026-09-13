import json
import tempfile
import unittest
from pathlib import Path

from src.access_feasibility import AccessState
from src.composition_validation_intake import (
    validation_event_from_record,
    validation_events_from_path,
)
from src.composition_validation_store import ValidationDimension


class CompositionValidationIntakeTests(unittest.TestCase):
    def _base(self):
        return {
            "validation_id": "v-1",
            "composition_run_id": 7,
            "hypothesis_index": 0,
            "dimension": "PAYER_CLARITY",
            "value": "PASS",
            "observed_at": "2026-09-13T20:00:00+08:00",
            "evidence_ref": "field:payer-review",
            "evidence_note": "payer identity and role reviewed",
            "subject_ref": "payer-a",
            "details": {"reviewed": True},
        }

    def _access_record(self):
        return {
            "candidate_id": "candidate-a",
            "target_actor": "institution-a",
            "route_kind": "PUBLIC_INSTITUTIONAL_WINDOW",
            "legitimate_entry_path": "formal public cooperation window",
            "backing_leverage": "formal route gives legitimate entry context",
            "counterparty_reason_to_engage": "bounded pilot can reduce a measured operating cost",
            "counterparty_visible_surplus": "lower verified operating cost if pilot succeeds",
            "surplus_realization_mechanism": "accepted pilot output reduces repeated manual cost",
            "institutional_cover_or_referral": "formal institution route",
            "status_trust_friction": "counterparty protects time and authority boundaries",
            "operator_credibility_assets": "relevant delivery history",
            "missing_credibility": "",
            "operator_commitment": "absorb initial coordination cost",
            "counterparty_commitment_requested": "confirm fit and nominate bounded next step",
            "founder_identity_dependency": "low after formal route acceptance",
            "evidence": [
                {
                    "source_id": "official-window",
                    "claim": "formal cooperation route is published",
                }
            ],
        }

    def test_generic_record_parses_one_explicit_dimension(self):
        event = validation_event_from_record(self._base())
        self.assertEqual(event.dimension, ValidationDimension.PAYER_CLARITY)
        self.assertEqual(event.value, "PASS")
        self.assertEqual(event.composition_run_id, 7)

    def test_unknown_and_derived_gate_fields_are_rejected(self):
        for key in ("transaction_ready", "G2", "G6"):
            record = self._base()
            record[key] = True
            with self.assertRaisesRegex(ValueError, "derived gate fields are not accepted"):
                validation_event_from_record(record)
        record = self._base()
        record["magic"] = "PASS"
        with self.assertRaisesRegex(ValueError, "unknown validation fields"):
            validation_event_from_record(record)

    def test_operator_access_cannot_be_hand_written(self):
        record = self._base()
        record["dimension"] = "OPERATOR_ACCESS"
        record["value"] = "VALIDATION_ACCESS_READY"
        record["access_record"] = self._access_record()
        with self.assertRaisesRegex(ValueError, "cannot be supplied directly"):
            validation_event_from_record(record)

    def test_operator_access_is_derived_from_canonical_access_record(self):
        record = {
            "validation_id": "access-1",
            "composition_run_id": 7,
            "hypothesis_index": 0,
            "dimension": "OPERATOR_ACCESS",
            "observed_at": "2026-09-13T20:00:00+08:00",
            "evidence_ref": "field:access-review",
            "evidence_note": "canonical access feasibility review",
            "access_record": self._access_record(),
        }
        event = validation_event_from_record(record)
        self.assertEqual(event.dimension, ValidationDimension.OPERATOR_ACCESS)
        self.assertEqual(event.value, AccessState.VALIDATION_ACCESS_READY.value)
        self.assertEqual(event.subject_ref, "institution-a")

    def test_incomplete_access_record_is_rejected_by_reviewed_schema(self):
        access = self._access_record()
        access["legitimate_entry_path"] = ""
        record = {
            "validation_id": "access-2",
            "composition_run_id": 7,
            "hypothesis_index": 0,
            "dimension": "OPERATOR_ACCESS",
            "observed_at": "2026-09-13T20:00:00+08:00",
            "evidence_ref": "field:access-review",
            "evidence_note": "entry path not established",
            "access_record": access,
        }
        with self.assertRaisesRegex(ValueError, "missing:legitimate_entry_path"):
            validation_event_from_record(record)

    def test_non_access_record_cannot_smuggle_access_record(self):
        record = self._base()
        record["access_record"] = self._access_record()
        with self.assertRaisesRegex(ValueError, "only valid for OPERATOR_ACCESS"):
            validation_event_from_record(record)

    def test_unknown_is_not_accepted_as_an_asserted_event(self):
        record = self._base()
        record["value"] = "UNKNOWN"
        with self.assertRaisesRegex(ValueError, "validation_event_must_not_assert_unknown"):
            validation_event_from_record(record)

    def test_json_and_jsonl_paths_are_supported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = self._base()
            second = self._base()
            second["validation_id"] = "v-2"
            second["dimension"] = "ACTOR_ROLE_CLARITY"

            json_path = root / "events.json"
            json_path.write_text(json.dumps([first, second]), encoding="utf-8")
            self.assertEqual(
                [event.validation_id for event in validation_events_from_path(json_path)],
                ["v-1", "v-2"],
            )

            jsonl_path = root / "events.jsonl"
            jsonl_path.write_text(
                json.dumps(first) + "\n" + json.dumps(second) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                [event.validation_id for event in validation_events_from_path(jsonl_path)],
                ["v-1", "v-2"],
            )


if __name__ == "__main__":
    unittest.main()
