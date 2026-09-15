import unittest

from src.live_observation_adapters import xuzhou_procurement_observations


class MissingProcurementProjectNameRegressionTests(unittest.TestCase):
    def _payload(self, project_name=None):
        url = "https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004002/20260914/f06db9cb-f182-4e04-94c9-a68967b5f7ef.html"
        return {
            "source_id": "XZ_GGZY",
            "error_count": 0,
            "events": [
                {
                    "source_id": "XZ_GGZY",
                    "project_id": "JSZC-320321-TZJL-G2026-0002",
                    "project_name": project_name,
                    "title": "丰县应急管理局泡沫消防车车辆采购项目采购公告(二)",
                    "url": url,
                    "publication_date": "2026-09-14",
                    "procurement_method": None,
                    "budget_raw": "预算金额：220.000000万元",
                    "budget_rmb": "2200000.00",
                    "deadline": "2026-10-09 09:30",
                    "contract_term": None,
                    "joint_venture_allowed": "否",
                    "provenance": {
                        "url": url,
                        "payload_sha256": "2" * 64,
                        "fetched_at_utc": "2026-09-14T07:03:35.855729+00:00",
                    },
                }
            ],
        }

    def test_missing_project_name_is_preserved_as_unknown_not_guessed_from_title(self):
        envelope = xuzhou_procurement_observations(self._payload())[0]
        notice = next(
            claim for claim in envelope.claims if claim.concept == "PUBLIC_PROCUREMENT_NOTICE"
        )
        self.assertIsNone(notice.value["project_name"])
        self.assertIn("project_name", envelope.unknown_fields)
        self.assertEqual(envelope.source_record_id, "JSZC-320321-TZJL-G2026-0002")
        self.assertNotEqual(notice.value["project_name"], self._payload()["events"][0]["title"])

    def test_present_project_name_remains_observed_source_value(self):
        expected = "邳州市民政局2026年中秋节慰问面粉采购及配送项目"
        envelope = xuzhou_procurement_observations(self._payload(expected))[0]
        notice = next(
            claim for claim in envelope.claims if claim.concept == "PUBLIC_PROCUREMENT_NOTICE"
        )
        self.assertEqual(notice.value["project_name"], expected)
        self.assertNotIn("project_name", envelope.unknown_fields)

    def test_non_string_project_name_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "must be a string or null"):
            xuzhou_procurement_observations(self._payload(123))


if __name__ == "__main__":
    unittest.main()
