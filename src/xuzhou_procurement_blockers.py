"""Observed transaction blockers from first-party Xuzhou procurement notices.

Only explicit source text may become a blocker. The adapter re-fetches the exact
notice URL, revalidates project identity, binds capability through the canonical
exact allowlist, and emits only bounded transaction access/routing constraints.

Current Xuzhou procurement pages may carry the full article body inside embedded
markup that the generic HTML document parser intentionally skips with ``script``.
This adapter therefore uses a bounded raw-HTML-to-plain-text fallback only when the
normal document text does not expose the two approved blocker markers. The same
first-party response and provenance are retained either way.

An observed constraint does not prove that a particular provider fails it.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.live_imbalance_ledger import classify_procurement_event
from src.regional_adapters import (
    XZ_GGZY_HOST,
    _plain_html_fragment,
    _structured_value,
    _titled_span_fields,
)


_SPECIFIC_QUAL_RE = re.compile(
    r"(?:\(三\)|（三）)?\s*本项目的特定资格要求[：:\s]*"
    r"(?P<body>.*?)"
    r"(?=\s*(?:(?:三、|三\.)\s*获取招标文件|四、|四\. |$))",
    re.S,
)
_NO_SUBCONTRACT_RE = re.compile(r"成交后不得转包或分包(?:，但[^。；\n]{0,180})?")
_APPROVED_MARKERS = ("本项目的特定资格要求", "成交后不得转包或分包")


@dataclass(frozen=True)
class ProcurementBlockerEvidence:
    signal_id: str
    project_id: str
    capability_key: str
    geography: str
    blocker_type: str
    evidence_state: str
    description: str
    blocker_basis: str
    extraction_path: str
    source_ids: tuple[str, ...]
    url: str
    provenance: dict[str, Any]


def _bounded(value: str, limit: int = 700) -> str:
    value = normalize_whitespace(value)
    return value[:limit].rstrip()


def _blocker_evidence_text(html: str, *, base_url: str) -> tuple[str, str]:
    """Return the narrowest trustworthy text surface that exposes blocker markers.

    The generic parser remains preferred. Xuzhou's current procurement publication
    template can embed the article markup in a script/template payload, which the
    generic parser correctly excludes. If neither approved marker is visible there,
    strip tags from the exact same fetched HTML and use that plain text only when an
    approved marker becomes visible. This does not execute JavaScript, fetch a second
    source, decode arbitrary blobs, or infer blockers from semantic similarity.
    """

    document_text = html_to_document(html, base_url=base_url)["text"]
    if any(marker in document_text for marker in _APPROVED_MARKERS):
        return document_text, "DOCUMENT_TEXT"

    raw_plain_text = _plain_html_fragment(html)
    if any(marker in raw_plain_text for marker in _APPROVED_MARKERS):
        return raw_plain_text, "RAW_HTML_PLAIN_FALLBACK"
    return document_text, "DOCUMENT_TEXT"


def extract_explicit_constraints(text: str) -> list[tuple[str, str, str]]:
    """Return (blocker_type, basis, description) for explicit constraints only."""

    result: list[tuple[str, str, str]] = []
    match = _SPECIFIC_QUAL_RE.search(text)
    if match:
        body = _bounded(match.group("body"))
        if body and not re.fullmatch(r"(?:无|无。|不适用)", body):
            result.append(
                (
                    "CAPABILITY_GAP",
                    "EXPLICIT_SPECIFIC_QUALIFICATION_REQUIREMENT",
                    f"官方采购公告存在特定资格准入要求：{body}",
                )
            )

    subcontract = _NO_SUBCONTRACT_RE.search(text)
    if subcontract:
        excerpt = _bounded(subcontract.group(0), 260)
        result.append(
            (
                "COORDINATION_GAP",
                "EXPLICIT_NO_SUBCONTRACT_OR_TRANSFER_RULE",
                f"官方采购公告明确限制成交后的资源路由：{excerpt}",
            )
        )
    return result


class XuzhouProcurementBlockerAdapter:
    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id="XZ_GGZY_PROCUREMENT_BLOCKER",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def collect(self, procurement_payload: Mapping[str, Any]) -> dict[str, Any]:
        blockers: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        queried = 0
        for event in list(procurement_payload.get("events", []) or []):
            classification = classify_procurement_event(event)
            if classification.capability_key is None:
                continue
            project_id = str(event.get("project_id") or "").strip()
            url = str(event.get("url") or "").strip()
            if not project_id or not url:
                continue
            queried += 1
            envelope = self.client.fetch(
                url,
                request_name="xz_ggzy.procurement_blocker.detail",
            )
            fields = _titled_span_fields(envelope.html)
            parsed_project_id = _structured_value(fields, "项目编号")
            document_text = html_to_document(envelope.html, base_url=url)["text"]
            if not parsed_project_id:
                match = re.search(r"项目编号[：:\s]*([^\n]+)", document_text)
                parsed_project_id = normalize_whitespace(match.group(1)) if match else None
            if parsed_project_id != project_id:
                rejected.append(
                    {
                        "project_id": project_id,
                        "parsed_project_id": parsed_project_id,
                        "url": url,
                        "reason": "NO_EXACT_PROJECT_ID_MATCH",
                    }
                )
                continue

            evidence_text, extraction_path = _blocker_evidence_text(
                envelope.html,
                base_url=url,
            )
            for blocker_type, basis, description in extract_explicit_constraints(evidence_text):
                evidence = ProcurementBlockerEvidence(
                    signal_id=f"LIVE_BLOCKER::XZ_GGZY::{project_id}::{basis}",
                    project_id=project_id,
                    capability_key=classification.capability_key,
                    geography="Xuzhou",
                    blocker_type=blocker_type,
                    evidence_state="OBSERVED",
                    description=description,
                    blocker_basis=basis,
                    extraction_path=extraction_path,
                    source_ids=("XZ_GGZY", url),
                    url=url,
                    provenance=envelope.metadata(),
                )
                blockers.append(asdict(evidence))

        return {
            "source_id": "XZ_GGZY_PROCUREMENT_BLOCKER",
            "query_strategy": "EXACT_PROJECT_ID_REVALIDATION_PLUS_EXPLICIT_TEXT_ONLY",
            "queried_event_count": queried,
            "blocker_count": len(blockers),
            "blockers": blockers,
            "rejected": rejected,
            "truth_note": (
                "Observed blocker means an explicit transaction access/routing constraint exists; "
                "it does not prove a particular provider fails that constraint and does not prove "
                "paid demand, payer identity, resource underuse, availability or control."
            ),
        }
