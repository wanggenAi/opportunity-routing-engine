#!/usr/bin/env python3
"""Probe the Jiangsu-government local-dynamics shell for its real list-loader route.

This is a bounded diagnostic tool, not a search-engine fallback. It fetches one
official column shell and records only structural clues needed to identify the
site's own public list endpoint.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.html_ingest import PublicHtmlClient, html_to_document
from src.network_ingest import write_json_atomic
from src.xuzhou_macro_mirror import COLUMN_URL, HOST, SOURCE_ID


URLISH_RE = re.compile(
    r'''(?P<quote>["'])(?P<url>(?:https?:)?//[^"']+|/[^"']*(?:module|jpage|dataproxy|ajax|column|col33718|212860)[^"']*)(?P=quote)''',
    re.I,
)
IFRAME_RE = re.compile(r'<iframe\b[^>]*?\bsrc=["\']([^"\']+)["\']', re.I)
SCRIPT_RE = re.compile(r'<script\b[^>]*?\bsrc=["\']([^"\']+)["\']', re.I)
FORM_RE = re.compile(r'<form\b[^>]*?\baction=["\']([^"\']+)["\']', re.I)


def _snippets(html: str, needle: str, radius: int = 220, limit: int = 8) -> list[str]:
    lower = html.lower()
    target = needle.lower()
    found: list[str] = []
    start = 0
    while len(found) < limit:
        pos = lower.find(target, start)
        if pos < 0:
            break
        left = max(0, pos - radius)
        right = min(len(html), pos + len(needle) + radius)
        snippet = re.sub(r"\s+", " ", html[left:right]).strip()
        if snippet not in found:
            found.append(snippet)
        start = pos + len(needle)
    return found


def _absolute(base: str, values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        value = value.strip()
        if not value:
            continue
        url = urljoin(base, value)
        if url not in result:
            result.append(url)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    client = PublicHtmlClient(
        source_id=SOURCE_ID,
        allowed_hosts={HOST},
        timeout_seconds=30,
        retries=2,
        max_response_bytes=5_000_000,
    )
    env = client.fetch(COLUMN_URL, request_name="js-gov.local-dynamics.shell-probe")
    html = env.html
    doc = html_to_document(html, base_url=env.url)

    iframe_srcs = _absolute(env.url, IFRAME_RE.findall(html))
    script_srcs = _absolute(env.url, SCRIPT_RE.findall(html))
    form_actions = _absolute(env.url, FORM_RE.findall(html))
    url_hints: list[str] = []
    for match in URLISH_RE.finditer(html):
        raw = match.group("url")
        url = urljoin(env.url, raw)
        if url not in url_hints:
            url_hints.append(url)

    needles = [
        "33718",
        "212860",
        "dataproxy",
        "jpage",
        "/module/",
        "ajax",
        "iframe",
        "pageNum",
        "uid",
        "columnid",
        "col33718",
    ]
    payload = {
        "source_id": SOURCE_ID,
        "shell_url": env.url,
        "shell_provenance": env.metadata(),
        "html_size_chars": len(html),
        "parsed_link_count": len(doc.get("links", [])),
        "parsed_links": doc.get("links", [])[:20],
        "iframe_srcs": iframe_srcs,
        "script_srcs": script_srcs,
        "form_actions": form_actions,
        "url_hints": url_hints[:100],
        "snippets": {needle: _snippets(html, needle) for needle in needles},
    }
    write_json_atomic(args.output, payload)
    print(f"wrote {args.output}")
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
