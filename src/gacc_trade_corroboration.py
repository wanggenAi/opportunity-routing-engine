"""HTTPS corroboration for the lower-trust GACC English HTTP trade feed.

The GACC English Monthly Bulletin is official but currently exposed to our runner
through plaintext HTTP. This module independently checks a same-period Jiangsu
government HTTPS publication that explicitly attributes the figures to Nanjing
Customs. It corroborates period, geography and import/export direction only.
It does not compare monetary values across currencies.
"""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace


SOURCE_ID = "JS_GOV"
HOST = "jszwb.jiangsu.gov.cn"
CORROBORATION_PERIOD = "2026-07"
CORROBORATION_URL = "https://jszwb.jiangsu.gov.cn/art/2026/8/14/art_71797_11816221.html"

_YTD_RE = re.compile(
    r"前7个月，江苏省外贸进出口(?P<total>\d+(?:\.\d+)?)万亿元.*?"
    r"其中，出口(?P<exports>\d+(?:\.\d+)?)万亿元.*?进口(?P<imports>\d+(?:\.\d+)?)万亿元",
    re.DOTALL,
)
_MONTH_RE = re.compile(
    r"7月份，我省外贸进出口(?P<total>\d+(?:\.\d+)?)亿元.*?"
    r"其中，出口(?P<exports>\d+(?:\.\d+)?)亿元.*?进口(?P<imports>\d+(?:\.\d+)?)亿元",
    re.DOTALL,
)


def _close(total: float, exports: float, imports: float, *, tolerance: float = 0.05) -> bool:
    return abs(total - exports - imports) <= tolerance


class JiangsuTradeCorroborator:
    """Corroborate current GACC Jiangsu trade identity through official HTTPS."""

    def __init__(self, client: Any | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=20,
            retries=1,
            max_response_bytes=5_000_000,
        )

    def corroborate(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = deepcopy(payload)
        period = str(result.get("period") or "")
        result["corroboration_required"] = True

        if period != CORROBORATION_PERIOD:
            result["corroboration_status"] = "PENDING"
            result["corroboration"] = {
                "status": "NO_SAME_PERIOD_HTTPS_CORROBORATION",
                "target_period": period,
                "known_corroboration_period": CORROBORATION_PERIOD,
                "monetary_value_comparison": "UNAVAILABLE_CROSS_CURRENCY",
            }
            return result

        env = self.client.fetch(CORROBORATION_URL, request_name="gacc.jiangsu_https_corroboration")
        doc = html_to_document(env.html, base_url=env.url)
        text = normalize_whitespace(doc.get("text", ""))

        required_phrases = (
            "据南京海关统计",
            "前7个月",
            "江苏省外贸进出口",
            "7月份",
        )
        missing = [phrase for phrase in required_phrases if phrase not in text]
        if missing:
            raise ValueError(f"Jiangsu HTTPS trade corroboration identity drift: missing={missing}")

        ytd = _YTD_RE.search(text)
        month = _MONTH_RE.search(text)
        if ytd is None or month is None:
            raise ValueError("Jiangsu HTTPS trade corroboration metrics could not be parsed")

        ytd_total = float(ytd.group("total"))
        ytd_exports = float(ytd.group("exports"))
        ytd_imports = float(ytd.group("imports"))
        month_total = float(month.group("total"))
        month_exports = float(month.group("exports"))
        month_imports = float(month.group("imports"))

        if not _close(ytd_total, ytd_exports, ytd_imports, tolerance=0.005):
            raise ValueError("Jiangsu HTTPS YTD trade arithmetic is inconsistent")
        if not _close(month_total, month_exports, month_imports, tolerance=0.2):
            raise ValueError("Jiangsu HTTPS monthly trade arithmetic is inconsistent")

        result["corroboration_status"] = "PERIOD_IDENTITY_DIRECTION_CORROBORATED"
        result["corroboration"] = {
            "source_id": SOURCE_ID,
            "source_authority": "JIANGSU_GOVERNMENT_HTTPS_REPOST_CITING_NANJING_CUSTOMS",
            "period": CORROBORATION_PERIOD,
            "geography": "Jiangsu",
            "basis": "PERIOD_IDENTITY_DIRECTION_ONLY",
            "monetary_value_comparison": "UNAVAILABLE_CROSS_CURRENCY",
            "reported_currency": "CNY",
            "reported_ytd": {
                "total_trillion_cny": ytd_total,
                "exports_trillion_cny": ytd_exports,
                "imports_trillion_cny": ytd_imports,
            },
            "reported_month": {
                "total_100m_cny": month_total,
                "exports_100m_cny": month_exports,
                "imports_100m_cny": month_imports,
            },
            "provenance": env.metadata(),
        }
        return result
