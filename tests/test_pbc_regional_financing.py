import io
import unittest
import zipfile

from src.pbc_regional_financing import (
    discover_latest_regional_table,
    discover_xlsx_attachment,
    extract_region_total,
)
from src.xlsx_ingest import XlsxParseError, parse_first_sheet_rows


def _minimal_xlsx() -> bytes:
    workbook = '''<?xml version="1.0" encoding="UTF-8"?>
    <workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <sheets><sheet name="地区社融" sheetId="1" r:id="rId1"/></sheets>
    </workbook>'''
    rels = '''<?xml version="1.0" encoding="UTF-8"?>
    <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
      <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    </Relationships>'''
    shared = '''<?xml version="1.0" encoding="UTF-8"?>
    <sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="4" uniqueCount="4">
      <si><t>地区社会融资规模增量统计表</t></si>
      <si><t>地区</t></si>
      <si><t>地区社会融资规模增量</t></si>
      <si><t>江苏 Jiangsu</t></si>
    </sst>'''
    sheet = '''<?xml version="1.0" encoding="UTF-8"?>
    <worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
      <sheetData>
        <row r="1"><c r="A1" t="s"><v>0</v></c></row>
        <row r="2"><c r="A2" t="s"><v>1</v></c><c r="B2" t="s"><v>2</v></c></row>
        <row r="3"><c r="A3" t="s"><v>3</v></c><c r="B3"><v>28900</v></c><c r="C3"><v>20300</v></c></row>
      </sheetData>
    </worksheet>'''
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", rels)
        zf.writestr("xl/sharedStrings.xml", shared)
        zf.writestr("xl/worksheets/sheet1.xml", sheet)
    return buffer.getvalue()


class PbcRegionalFinancingTests(unittest.TestCase):
    def test_parses_minimal_xlsx_and_extracts_jiangsu_total(self):
        rows = parse_first_sheet_rows(_minimal_xlsx())
        result = extract_region_total(rows, region="江苏")
        self.assertEqual(result["social_financing_flow_100m_cny"], 28900.0)
        self.assertEqual(result["social_financing_flow_trillion_cny"], 2.89)
        self.assertEqual(result["matched_label"], "江苏 Jiangsu")
        self.assertEqual(result["total_column_1based"], 2)

    def test_discovers_latest_regional_table(self):
        doc = {
            "links": [
                {"text": "2026年7月金融统计数据报告", "url": "https://www.pbc.gov.cn/national"},
                {"text": "2026年上半年地区社会融资规模增量统计表", "url": "https://www.pbc.gov.cn/regional"},
            ]
        }
        result = discover_latest_regional_table(doc)
        self.assertEqual(result["title"], "2026年上半年地区社会融资规模增量统计表")

    def test_attachment_must_be_official_xlsx(self):
        doc = {
            "links": [
                {"text": "2026年上半年地区社会融资规模增量统计表.xlsx", "url": "https://www.pbc.gov.cn/file.xlsx"},
            ]
        }
        self.assertEqual(discover_xlsx_attachment(doc), "https://www.pbc.gov.cn/file.xlsx")
        with self.assertRaises(ValueError):
            discover_xlsx_attachment({"links": [{"text": "地区社会融资规模增量统计表.xlsx", "url": "https://evil.example/file.xlsx"}]})

    def test_ambiguous_headers_fail_closed(self):
        rows = [["地区", "金额"], ["江苏", 28900]]
        with self.assertRaises(ValueError):
            extract_region_total(rows, region="江苏")

    def test_invalid_zip_rejected(self):
        with self.assertRaises(XlsxParseError):
            parse_first_sheet_rows(b"not-a-zip")


if __name__ == "__main__":
    unittest.main()
