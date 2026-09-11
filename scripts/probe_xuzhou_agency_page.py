#!/usr/bin/env python3
"""Bounded diagnostics for the public Xuzhou agency-list page.

This is intentionally a source-structure probe, not a bypass. It fetches one public
HTML page and reports only bounded structural hints needed to maintain the adapter.
"""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.xuzhou_agency_resource_feed import XZ_AGENCY_LIST, XZ_GGZY_HOST


def _bounded_unique(values, limit=40):
    result = []
    seen = set()
    for value in values:
        value = normalize_whitespace(unescape(value))
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
        if len(result) >= limit:
            break
    return result


def _snippets(html: str, token: str, limit: int = 5, radius: int = 350):
    result = []
    lowered = html.lower()
    needle = token.lower()
    start = 0
    while len(result) < limit:
        idx = lowered.find(needle, start)
        if idx < 0:
            break
        fragment = html[max(0, idx - radius) : idx + len(token) + radius]
        fragment = re.sub(r"\s+", " ", fragment)
        result.append(fragment[:900])
        start = idx + len(token)
    return result


def main():
    client = PublicHtmlClient(
        source_id="XZ_GGZY_AGENCY_PROBE",
        allowed_hosts={XZ_GGZY_HOST},
        timeout_seconds=30,
        retries=2,
    )
    envelope = client.fetch(XZ_AGENCY_LIST, request_name="xz_ggzy.agency_assets.probe")
    html = envelope.html
    doc = html_to_document(html, base_url=XZ_AGENCY_LIST)

    attr_values = re.findall(
        r"(?:href|src|action|data-url|data-href)\s*=\s*[\"']([^\"']+)[\"']",
        html,
        flags=re.I,
    )
    script_srcs = re.findall(r"<script\b[^>]*src=[\"']([^\"']+)[\"']", html, flags=re.I)
    guid_values = re.findall(r"[0-9a-fA-F]{8}-[0-9a-fA-F-]{27,36}", html)
    gr_codes = re.findall(r"GR20\d{2}JS\d+(?:-\d+)?", html, flags=re.I)

    interesting_attrs = [
        urljoin(XZ_AGENCY_LIST, value)
        for value in attr_values
        if any(
            token in value.lower()
            for token in ("trade", "jyxx", "003010", "api", "list", "query", "page")
        )
    ]

    payload = {
        "provenance": envelope.metadata(),
        "html_length": len(html),
        "parsed_link_count": len(doc["links"]),
        "guid_token_count": html.lower().count("biaoduanguid"),
        "guid_like_count": len(guid_values),
        "guid_like_samples": _bounded_unique(guid_values, 15),
        "gr_code_count": len(gr_codes),
        "gr_code_samples": _bounded_unique(gr_codes, 20),
        "tradeinfo_token_count": html.lower().count("tradeinfo"),
        "ajax_token_count": html.lower().count("ajax"),
        "etrading_token_count": html.count("e交易"),
        "script_srcs": _bounded_unique([urljoin(XZ_AGENCY_LIST, item) for item in script_srcs], 40),
        "interesting_attrs": _bounded_unique(interesting_attrs, 50),
        "snippets": {
            token: _snippets(html, token)
            for token in (
                "BiaoDuanGuid",
                "tradeInfo",
                "e交易",
                "ajax",
                "listqtxx",
                "GR2026JS",
            )
        },
    }
    output = ROOT / ".local" / "xz_agency_page_probe.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2)[:20000])
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
