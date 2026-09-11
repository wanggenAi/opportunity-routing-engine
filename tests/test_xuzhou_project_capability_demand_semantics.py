import unittest

from src.xuzhou_project_capability_demand import extract_project_capability_requirements


class XuzhouProjectCapabilityDemandSemanticIsolationTests(unittest.TestCase):
    def test_technical_lead_does_not_inherit_manager_constructor_note(self):
        text = """
        3.2.1项目经理资格条件：
        ①持有有效的公路工程专业二级及以上建造师注册证书；
        ②2021年1月1日至今至少担任过1个公路工程项目的项目经理。
        3.2.2项目总工资格条件：
        ①具有公路工程相关专业中级及以上技术职称；
        ②2021年1月1日至今至少担任过1个公路工程项目的项目总工。
        拟投入的项目经理、项目总工应为投标人本单位人员，并提供社保缴费明细。
        如投标人拟投入的项目经理为一级建造师，其一级建造师注册证书应满足电子证书要求。
        3.3其他要求
        """
        by_role = {item.role: item for item in extract_project_capability_requirements(text)}
        self.assertIn("PROJECT_MANAGER", by_role)
        self.assertIn("PROJECT_TECHNICAL_LEAD", by_role)
        self.assertIn("二级", by_role["PROJECT_MANAGER"].constructor_license)
        self.assertIsNone(by_role["PROJECT_TECHNICAL_LEAD"].constructor_license)
        self.assertIn("中级", by_role["PROJECT_TECHNICAL_LEAD"].professional_title)

    def test_project_lead_umbrella_followed_by_manager_is_not_counted(self):
        text = """
        拟派项目负责人应满足的要求：
        3.3.1项目经理（项目负责人）资格：
        （1）拟投入本项目的项目经理应具有机电工程专业二级注册建造师资格；
        （2）2021年1月1日以来至少完成过一项公路机电工程施工项目的项目经理。
        3.3.2项目总工（技术负责人）资格：
        （1）需具有中级及以上技术职称；
        （2）2021年1月1日以来至少完成过一项公路机电工程施工项目的项目总工。
        拟投入项目经理、项目总工应为投标人本单位人员，并提供社保缴费明细。
        """
        roles = [item.role for item in extract_project_capability_requirements(text)]
        self.assertEqual(roles.count("PROJECT_LEAD"), 0)
        self.assertEqual(roles.count("PROJECT_MANAGER"), 1)
        self.assertEqual(roles.count("PROJECT_TECHNICAL_LEAD"), 1)


if __name__ == "__main__":
    unittest.main()
