import unittest

from src.xuzhou_hrss_capability_demand import (
    discover_job_table_attachment,
    discover_recent_recruitment_articles,
    extract_capability_demand,
)


class XuzhouHrssCapabilityDemandTests(unittest.TestCase):
    def test_discovery_keeps_only_official_recruitment_articles_and_sorts_by_date(self):
        doc = {
            "links": [
                {
                    "text": "徐州市2026年事业单位统一公开招聘人员公告",
                    "url": "https://hrss.xz.gov.cn/001/001004/20260320/9545437c-677a-4dac-bcc9-476e7e0773d1.html",
                },
                {
                    "text": "2026年公开招聘高层次人才公告",
                    "url": "https://hrss.xz.gov.cn/001/001004/20260810/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html",
                },
                {
                    "text": "招聘转载",
                    "url": "https://evil.example/001/001004/20260901/aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.html",
                },
                {
                    "text": "职称评审通知",
                    "url": "https://hrss.xz.gov.cn/001/001004/20260901/ffffffff-bbbb-cccc-dddd-eeeeeeeeeeee.html",
                },
            ]
        }
        items = discover_recent_recruitment_articles(doc)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["publication_date_from_url"], "2026-08-10")
        self.assertEqual(items[1]["publication_date_from_url"], "2026-03-20")

    def test_job_table_attachment_requires_official_xls_and_semantic_name(self):
        doc = {
            "links": [
                {"text": "招聘岗位表.xls", "url": "https://hrss.xz.gov.cn/files/jobs.xls"},
                {"text": "报名表.xls", "url": "https://hrss.xz.gov.cn/files/form.xls"},
                {"text": "岗位表.xls", "url": "https://evil.example/jobs.xls"},
            ]
        }
        self.assertEqual(
            discover_job_table_attachment(doc),
            "https://hrss.xz.gov.cn/files/jobs.xls",
        )

    def test_multiple_job_table_attachments_fail_closed(self):
        doc = {
            "links": [
                {"text": "岗位表一.xls", "url": "https://hrss.xz.gov.cn/files/a.xls"},
                {"text": "岗位表二.xls", "url": "https://hrss.xz.gov.cn/files/b.xls"},
            ]
        }
        with self.assertRaisesRegex(ValueError, "multiple official HRSS job-table"):
            discover_job_table_attachment(doc)

    def test_extracts_explicit_demand_without_inventing_surplus(self):
        workbook = [
            {
                "sheet_index": 0,
                "sheet_name": "招聘岗位表",
                "rows": [
                    ["徐州市2026年公开招聘岗位表"],
                    ["招聘单位", "岗位代码", "岗位名称", "招聘人数", "学历", "学位", "专业", "职称要求", "工作经历"],
                    ["甲单位", "A01", "数据管理", 2, "本科及以上", "学士及以上", "计算机科学与技术", None, "2年以上"],
                    ["乙单位", "B02", "财务管理", 1, "本科", "学士", "会计学", "中级", None],
                ],
            }
        ]
        result = extract_capability_demand(workbook)
        self.assertEqual(result["demand_unit_count"], 2)
        self.assertEqual(result["total_requested_headcount"], 3)
        first = result["demand_units"][0]
        self.assertEqual(first["position"], "数据管理")
        self.assertEqual(first["hiring_count"], 2)
        self.assertEqual(first["major_requirement"], "计算机科学与技术")
        self.assertEqual(first["evidence_state"], "EXPLICIT_CAPABILITY_DEMAND")
        self.assertNotIn("availability", first)
        self.assertNotIn("willingness", first)
        self.assertNotIn("surplus", first)

    def test_projected_or_missing_hiring_count_never_becomes_zero(self):
        workbook = [
            {
                "sheet_index": 0,
                "sheet_name": "岗位表",
                "rows": [
                    ["单位名称", "岗位名称", "招聘人数", "专业要求"],
                    ["甲单位", "工程师", None, "机械工程"],
                    ["乙单位", "分析员", "若干", "经济学"],
                    ["丙单位", "审计", 1, "审计学"],
                ],
            }
        ]
        result = extract_capability_demand(workbook)
        self.assertEqual(result["demand_unit_count"], 1)
        self.assertEqual(result["total_requested_headcount"], 1)
        self.assertEqual(result["demand_units"][0]["employer"], "丙单位")

    def test_ambiguous_structured_sheets_fail_closed(self):
        rows = [
            ["招聘单位", "岗位名称", "招聘人数", "专业"],
            ["甲单位", "工程师", 1, "机械工程"],
        ]
        workbook = [
            {"sheet_index": 0, "sheet_name": "一", "rows": rows},
            {"sheet_index": 1, "sheet_name": "二", "rows": rows},
        ]
        with self.assertRaisesRegex(ValueError, "expected one structured recruitment sheet"):
            extract_capability_demand(workbook)


if __name__ == "__main__":
    unittest.main()
