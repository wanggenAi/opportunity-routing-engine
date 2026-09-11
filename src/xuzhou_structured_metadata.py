"""Structured metadata helpers for Xuzhou public-procurement HTML.

The Xuzhou public-resources site embeds authoritative field identity in titled span
markup even when the surrounding HTML is malformed enough that a generic HTML text
parser cannot expose the article body reliably. These helpers read only those
explicit first-party field labels; they do not infer missing values from prose.
"""

from __future__ import annotations

import re
from html import unescape

from src.html_ingest import normalize_whitespace


def plain_html_fragment(fragment: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize_whitespace(unescape(text))


def titled_span_fields(html: str) -> dict[str, tuple[str, ...]]:
    """Return explicit ``title=`` field labels and unique normalized values.

    Only spans whose own opening tag contains a title attribute are considered. This
    matters because live notices commonly use untitled outer spans around titled
    inner spans. Duplicate equal values collapse; conflicting values are retained so
    callers can fail closed.
    """

    values: dict[str, list[str]] = {}
    for match in re.finditer(
        r"<span\b(?=[^>]*\btitle\s*=)(?P<attrs>[^>]*)>(?P<body>.*?)</span\s*>",
        html,
        flags=re.I | re.S,
    ):
        attrs = match.group("attrs")
        title_match = re.search(
            r"\btitle\s*=\s*(['\"])(?P<title>.*?)\1",
            attrs,
            flags=re.I | re.S,
        )
        if not title_match:
            continue
        label = normalize_whitespace(unescape(title_match.group("title")))
        value = plain_html_fragment(match.group("body"))
        if not label or not value:
            continue
        bucket = values.setdefault(label, [])
        if value not in bucket:
            bucket.append(value)
    return {label: tuple(items) for label, items in values.items()}


def structured_value(
    fields: dict[str, tuple[str, ...]], *labels: str
) -> str | None:
    """Return one exact labeled value, failing closed on conflicting duplicates."""

    for label in labels:
        values = fields.get(label, ())
        if len(values) == 1:
            return values[0]
        if len(values) > 1:
            return None
    return None
