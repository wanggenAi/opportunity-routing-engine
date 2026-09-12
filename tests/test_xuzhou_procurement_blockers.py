import unittest

from src.xuzhou_procurement_blockers import extract_explicit_constraints


class XuzhouProcurementBlockerTests(unittest.TestCase):
    def test_specific_qualification_is_observed_capability_constraint(self):
        text = """
二、申请人的资格要求：
（三）本项目的特定资格要求：
投标人具备市政公用工程施工总承包贰级（含）及以上资质（须提供资质证书）。
三、获取招标文件
"""
        result = extract_explicit_constraints(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "CAPABILITY_GAP")
        self.assertEqual(result[0][1], "EXPLICIT_SPECIFIC_QUALIFICATION_REQUIREMENT")
        self.assertIn("市政公用工程施工总承包贰级", result[0][2])

    def test_no_specific_requirement_does_not_manufacture_blocker(self):
        text = """
（三）本项目的特定资格要求：无
三、获取招标文件
"""
        self.assertEqual(extract_explicit_constraints(text), [])

    def test_no_subcontract_rule_is_observed_coordination_constraint(self):
        text = "成交后不得转包或分包，但电气设备的预防性试验可以委托第三方完成。"
        result = extract_explicit_constraints(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "COORDINATION_GAP")
        self.assertEqual(result[0][1], "EXPLICIT_NO_SUBCONTRACT_OR_TRANSFER_RULE")
        self.assertIn("不得转包或分包", result[0][2])

    def test_generic_qualification_section_is_not_enough(self):
        text = "申请人的资格要求：满足政府采购法第二十二条规定。"
        self.assertEqual(extract_explicit_constraints(text), [])


if __name__ == "__main__":
    unittest.main()
