import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.structure_validation_planning import (
    build_structure_field_packets,
    build_structure_validation_queue,
)


PROFILE_PATH = Path("data/research_runs/ELDERCARE_STRUCTURE_VALIDATION_PLAN_006_2026-09-14/profile.json")


class EldercareStructureValidationPlan006Tests(unittest.TestCase):
    def _artifact(self):
        return {
            "candidate_id": "STRUCTURE-ELDERCARE-CAPACITY-ORCHESTRATION-001",
            "candidate_concept": "ELDERCARE_CAPACITY_ORCHESTRATION",
            "commercial_structure_state": "STRUCTURE_VALIDATION_READY",
            "missing_dimensions": ["COMPOUNDING"],
            "business_promotion": "NOT_PROMOTED",
        }

    def _profile(self):
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    def test_eldercare_profile_is_process_level_and_excludes_personal_health_data(self):
        profile = self._profile()
        self.assertEqual(profile["case_unit"], "DEIDENTIFIED_INSTITUTION_OR_PROCESS_EPISODE")
        self.assertIn("NO_PERSONAL_HEALTH_DATA", profile["privacy_constraints"])
        self.assertIn("NO_BENEFICIARY_IDENTITY", profile["privacy_constraints"])
        prohibited = set(profile["prohibited_fields"])
        for field in ("beneficiary_name", "national_id", "phone_number", "home_address", "diagnosis", "medical_record", "raw_health_data"):
            self.assertIn(field, prohibited)
        required = set(profile["local_case_required_fields"])
        self.assertTrue(required.isdisjoint(prohibited))

    def test_eldercare_plan_targets_only_local_corroboration_and_compounding(self):
        queue = build_structure_validation_queue(self._artifact(), profile=self._profile())
        self.assertEqual(queue["validation_profile"]["profile_id"], "ELDERCARE_INSTITUTION_PROCESS_COMPOUNDING_V1")
        self.assertEqual(queue["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(queue["source_missing_dimensions"], ["COMPOUNDING"])
        self.assertEqual(
            {task["target_gate"] for task in queue["tasks"]},
            {"LOCAL_CASE_PANEL", "LOCAL_PAID_MANDATE", "COMPOUNDING"},
        )
        compounding = next(task for task in queue["tasks"] if task["target_gate"] == "COMPOUNDING")
        self.assertEqual(compounding["task_role"], "CORE_MISSING_DIMENSION")
        self.assertEqual(compounding["depends_on"], ["VALIDATE_STRUCTURE::STRUCTURE-ELDERCARE-CAPACITY-ORCHESTRATION-001::LOCAL_CASE_PANEL"])
        self.assertIn("assessment_minutes", compounding["capture_contract"]["predeclared_metrics"])
        self.assertIn("reused_prior_outcome_refs", compounding["capture_contract"]["required_reuse_fields"])
        self.assertIn("NO_PERSONAL_HEALTH_DATA", compounding["capture_contract"]["privacy_constraints"])

    def test_packets_preserve_privacy_and_remain_noncanonical(self):
        packets = build_structure_field_packets(
            build_structure_validation_queue(self._artifact(), profile=self._profile())
        )
        self.assertEqual(packets["packet_count"], 3)
        self.assertEqual(packets["business_promotion"], "NOT_PROMOTED")
        for packet in packets["packets"]:
            self.assertEqual(packet["case_unit"], "DEIDENTIFIED_INSTITUTION_OR_PROCESS_EPISODE")
            self.assertIn("NO_PERSONAL_HEALTH_DATA", packet["privacy_constraints"])
            self.assertNotIn("evidence_state", packet)
            self.assertNotIn("payer_confirmed", packet)
            self.assertNotIn("route_testable", packet)

    def test_cli_materializes_profile_without_truth_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            artifact_path = tmp_path / "artifact.json"
            queue_path = tmp_path / "queue.json"
            packets_path = tmp_path / "packets.json"
            artifact_path.write_text(json.dumps(self._artifact()), encoding="utf-8")
            subprocess.run(
                [
                    sys.executable,
                    "scripts/build_structure_validation_plan.py",
                    "--commercial-structure",
                    str(artifact_path),
                    "--profile",
                    str(PROFILE_PATH),
                    "--queue-output",
                    str(queue_path),
                    "--packets-output",
                    str(packets_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            packets = json.loads(packets_path.read_text(encoding="utf-8"))
        self.assertEqual(queue["validation_profile"]["profile_id"], "ELDERCARE_INSTITUTION_PROCESS_COMPOUNDING_V1")
        self.assertEqual(queue["business_promotion"], "NOT_PROMOTED")
        self.assertEqual(packets["business_promotion"], "NOT_PROMOTED")


if __name__ == "__main__":
    unittest.main()
