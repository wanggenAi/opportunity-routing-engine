"""Extract explicit failed-package evidence from Xuzhou procurement result pages.

A failed/void package is a CHANGE / FRICTION observation. It is deliberately not a
provider signal, paid-need signal, payer identity, or proof that a later tender is an
exact package-level rebid.

Only source-explicit text ending in ``此采购包已作废`` is admitted. Missing supplier
rows, missing packages, or title similarity alone never manufacture failure evidence.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.xuzhou_structured_metadata import structured_value, titled_span_fields

XZ_GGZY_HOST = "ggzy.zwb.xz.gov.cn"
_RESULT_DETAIL_RE = re.compile(
    r"/jyxx/003004/003004006/(20\d{6})/[0-9a-fA-F-]+\.html(?:\?.*)?$"
)
_PACKAGE_TOKEN_RE = re.compile(r"采购包\s*([一二三四五六七八九十\d]+)")
_VOID_MARKER = "此采购包已作废"


@dataclass(frozen=True)
class ProcurementPackageFailure:
    source_id: str
    title: str
    url: str
    publication_date: str | None
    project_id: str | None
    project_name: str | None
    buyer_actor: str | None
    package_name: str
    outcome_state: str
    outcome_text: str
    provenance: dict[str, Any]


def _text(value: object) -> str | None:
    text = normalize_whitespace(str(value or ""))
    return text or None


def _first(pattern: str, text: str, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    return _text(match.group(1)) if match else None


def _date_from_url(url: str) -> str | None:
    match = re.search(r"/(20\d{6})/", url)
    if not match:
        return None
    raw = match.group(1)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def _publication_date(text: str, url: str) -> str | None:
    value = _first(
        r"信息发布时间[：:\s]*([0-9]{4}[-年][0-9]{1,2}[-月][0-9]{1,2}日?)",
        text,
    )
    if value:
        parts = re.findall(r"\d+", value)
        if len(parts) >= 3:
            return f"{int(parts[0]):04d}-{int(parts[1]):02d}-{int(parts[2]):02d}"
    return _date_from_url(url)


def _best_title(text: str, html_title: str, fallback: str | None) -> str:
    for line in text.splitlines()[:35]:
        line = normalize_whitespace(line)
        if len(line) <= 240 and any(
            marker in line
            for marker in ("中标结果公告", "中标公告", "成交结果公告", "成交公告")
        ):
            return line
    return fallback or html_title


def extract_explicit_void_packages(text: str) -> list[tuple[str, str]]:
    """Return package labels whose own text segment explicitly says it was voided.

    The segment boundary is the next ``采购包X`` token. This prevents a void marker
    belonging to package 2 from being attributed to package 1 merely because both
    occur on the same result page.
    """

    normalized = normalize_whitespace(text)
    matches = list(_PACKAGE_TOKEN_RE.finditer(normalized))
    result: list[tuple[str, str]] = []
    seen: set[str] = set()
    for index, match in enumerate(matches):
        package_name = f"采购包{match.group(1)}"
        end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        segment = normalized[match.start() : end]
        marker_index = segment.find(_VOID_MARKER)
        if marker_index < 0 or package_name in seen:
            continue
        evidence_text = normalize_whitespace(
            segment[: marker_index + len(_VOID_MARKER)]
        )
        seen.add(package_name)
        result.append((package_name, evidence_text))
    return result


class XuzhouProcurementFailureAdapter:
    """Fetch official result pages and retain explicit failed-package evidence."""

    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id="XZ_GGZY_PROCUREMENT_FAILURE",
            allowed_hosts={XZ_GGZY_HOST},
            timeout_seconds=30,
            retries=2,
        )

    def fetch_failures(
        self,
        url: str,
        *,
        fallback_title: str | None = None,
    ) -> list[ProcurementPackageFailure]:
        if not _RESULT_DETAIL_RE.search(url):
            raise ValueError("URL is not a Xuzhou government-procurement result notice")
        envelope = self.client.fetch(
            url,
            request_name="xz_ggzy.procurement_failures.detail",
        )
        doc = html_to_document(envelope.html, base_url=url)
        text = doc["text"]
        failures = extract_explicit_void_packages(text)
        if not failures:
            return []

        fields = titled_span_fields(envelope.html)
        title = _best_title(text, doc["title"], fallback_title)
        project_id = (
            structured_value(fields, "项目编号")
            or _first(r"项目编号[：:\s]*([^\n]+)", text)
        )
        project_name = (
            structured_value(fields, "项目名称")
            or _first(r"项目名称[：:\s]*([^\n]+)", text)
        )
        buyer_actor = (
            structured_value(fields, "采购人单位名称", "采购人名称")
            or _first(
                r"采购人信息[\s\S]{0,800}?单位名称[：:\s]*([^\n]+)",
                text,
            )
        )
        publication_date = _publication_date(text, url)
        return [
            ProcurementPackageFailure(
                source_id="XZ_GGZY_PROCUREMENT_FAILURE",
                title=title,
                url=url,
                publication_date=publication_date,
                project_id=project_id,
                project_name=project_name,
                buyer_actor=buyer_actor,
                package_name=package_name,
                outcome_state="EXPLICIT_PACKAGE_VOID",
                outcome_text=outcome_text,
                provenance=envelope.metadata(),
            )
            for package_name, outcome_text in failures
        ]

    def collect_from_result_payloads(
        self,
        payloads: Iterable[Mapping[str, Any]],
    ) -> dict[str, Any]:
        """Inspect only already-proven result URLs, avoiding broad duplicate crawling."""

        candidates: list[tuple[str, str | None]] = []
        seen_urls: set[str] = set()
        for payload in payloads:
            for award in payload.get("awards", []) or []:
                url = str(award.get("url") or "").strip()
                if not url or url in seen_urls:
                    continue
                if not _RESULT_DETAIL_RE.search(url):
                    continue
                seen_urls.add(url)
                candidates.append((url, _text(award.get("title"))))

        failures: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        seen_failures: set[tuple[str | None, str]] = set()
        for url, title in candidates:
            try:
                parsed = self.fetch_failures(url, fallback_title=title)
            except Exception as exc:
                errors.append({"url": url, "error": str(exc)})
                continue
            for failure in parsed:
                identity = (failure.project_id, failure.package_name)
                if identity in seen_failures:
                    continue
                seen_failures.add(identity)
                failures.append(asdict(failure))

        failures.sort(
            key=lambda item: (
                str(item.get("publication_date") or ""),
                str(item.get("project_id") or ""),
                str(item.get("package_name") or ""),
            )
        )
        return {
            "source_id": "XZ_GGZY_PROCUREMENT_FAILURE",
            "result_url_count": len(candidates),
            "failed_package_count": len(failures),
            "error_count": len(errors),
            "failures": failures,
            "errors": errors,
            "truth_notes": [
                "Only source-explicit '此采购包已作废' text creates failure evidence.",
                "A failed package is CHANGE/FRICTION evidence, not provider evidence and not PAID need evidence.",
                "Missing supplier rows or missing package rows never imply failure.",
                "Package failure does not by itself prove why the market failed to clear.",
            ],
        }
