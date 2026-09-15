import unittest

from scripts.validate_live_observation_fabric import (
    upstream_run_ids,
    validate_upstream_monotonicity,
)


def assessment(
    jiangsu: int,
    regional: int,
    resource: int,
    nbs: int,
    pbc_jiangsu: int,
    pbc: int,
    xuzhou_financing: int,
    gacc: int,
    questmobile: int,
) -> dict:
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
                "nbs_macro": {
                    "databaseId": nbs,
                    "status": "completed",
                    "conclusion": "success",
                },
                "pbc_jiangsu_credit": {
                    "databaseId": pbc_jiangsu,
                    "status": "completed",
                    "conclusion": "success",
                },
                "pbc_money_flow": {
                    "databaseId": pbc,
                    "status": "completed",
                    "conclusion": "success",
                },
                "xuzhou_financing_demand": {
                    "databaseId": xuzhou_financing,
                    "status": "completed",
                    "conclusion": "success",
                },
                "gacc_trade_flow": {
                    "databaseId": gacc,
                    "status": "completed",
                    "conclusion": "success",
                },
                "questmobile_public_research": {
                    "databaseId": questmobile,
                    "status": "completed",
                    "conclusion": "success",
                },
            }
        }
    }


class LiveObservationRunLineageTests(unittest.TestCase):
    def test_same_or_newer_upstream_runs_are_allowed(self):
        previous = assessment(100, 200, 300, 400, 500, 600, 700, 800, 900)
        current = assessment(100, 201, 305, 400, 501, 601, 702, 801, 902)
        validate_upstream_monotonicity(current, previous)
        self.assertEqual(
            upstream_run_ids(current),
            {
                "jiangsu_money_flow": 100,
                "regional_data": 201,
                "resource_underuse": 305,
                "nbs_macro": 400,
                "pbc_jiangsu_credit": 501,
                "pbc_money_flow": 601,
                "xuzhou_financing_demand": 702,
                "gacc_trade_flow": 801,
                "questmobile_public_research": 902,
            },
        )

    def test_any_upstream_run_regression_fails_closed(self):
        previous = assessment(100, 200, 300, 400, 500, 600, 700, 800, 900)
        current = assessment(101, 200, 301, 400, 501, 601, 701, 801, 899)
        with self.assertRaisesRegex(SystemExit, "questmobile_public_research:900->899"):
            validate_upstream_monotonicity(current, previous)

    def test_incomplete_or_non_successful_run_metadata_fails_closed(self):
        data = assessment(100, 200, 300, 400, 500, 600, 700, 800, 900)
        data["upstream_manifest"]["upstream_runs"]["questmobile_public_research"]["status"] = "in_progress"
        with self.assertRaisesRegex(SystemExit, "not completed"):
            upstream_run_ids(data)


if __name__ == "__main__":
    unittest.main()
