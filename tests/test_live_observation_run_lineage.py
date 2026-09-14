import unittest

from scripts.validate_live_observation_fabric import (
    upstream_run_ids,
    validate_upstream_monotonicity,
)


def assessment(jiangsu: int, regional: int, resource: int) -> dict:
    return {
        "upstream_manifest": {
            "upstream_runs": {
                "jiangsu_money_flow": {
                    "databaseId": jiangsu,
                    "status": "completed",
                    "conclusion": "success",
                },
                "regional_data": {
                    "databaseId": regional,
                    "status": "completed",
                    "conclusion": "success",
                },
                "resource_underuse": {
                    "databaseId": resource,
                    "status": "completed",
                    "conclusion": "success",
                },
            }
        }
    }


class LiveObservationRunLineageTests(unittest.TestCase):
    def test_same_or_newer_upstream_runs_are_allowed(self):
        previous = assessment(100, 200, 300)
        current = assessment(100, 201, 305)
        validate_upstream_monotonicity(current, previous)
        self.assertEqual(
            upstream_run_ids(current),
            {
                "jiangsu_money_flow": 100,
                "regional_data": 201,
                "resource_underuse": 305,
            },
        )

    def test_any_upstream_run_regression_fails_closed(self):
        previous = assessment(100, 200, 300)
        current = assessment(101, 200, 299)
        with self.assertRaisesRegex(SystemExit, "resource_underuse:300->299"):
            validate_upstream_monotonicity(current, previous)

    def test_incomplete_or_non_successful_run_metadata_fails_closed(self):
        data = assessment(100, 200, 300)
        data["upstream_manifest"]["upstream_runs"]["regional_data"]["status"] = "in_progress"
        with self.assertRaisesRegex(SystemExit, "not completed"):
            upstream_run_ids(data)


if __name__ == "__main__":
    unittest.main()
