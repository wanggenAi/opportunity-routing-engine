"""Project-personnel capability-demand evidence from Xuzhou public tenders.

The Xuzhou Public Resources Trading Center publishes public transport/construction
tender notices that contain explicit personnel qualification requirements for
roles such as project manager, technical lead and project lead. These are useful
as transaction-level capability-demand evidence.

Truth boundaries:
- tender qualification != labor shortage;
- required capability != available/surplus capability;
- bidder employee/social-insurance requirements are transaction constraints, not
  proof that a matching independent worker can be routed into the contract;
- a tender notice is not completed hiring or completed payment;
- no named individual/candidate profile is collected;
- no opportunity inference is made.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import urlparse

from src.html_ingest import PublicHtmlClient, html_to_document, normalize_whitespace
from src.regional_adapters import _publication_date


SOURCE_ID = "XZ_GGZY"
HOST = "ggzy.zwb.xz.gov.cn"
LIST_URL = "https://ggzy.zwb.xz.gov.cn/jyxx/003002/003002001/list.html"
_DETAIL_RE = re.compile(
    r"^/jyxx/003002/003002001/(20\d{6})/[0-9a-fA-F-]+\.html$"
)

_ROLE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "PROJECT_MANAGER",
        re.compile(r"(?:项目经理资格(?:要求)?|项目经理条件|项目经理)"),
    ),
    (
        "PROJECT_TECHNICAL_LEAD",
        re.compile(r"(?:项目总工资格(?:要求)?|项目总工(?:（项目技术负责人）|\(项目技术负责人\))?|项目总工)"),
    ),
    (
        "PROJECT_LEAD",
        re.compile(r"(?:拟派项目负责人(?:应满足的要求|资格要求)?|项目负责人(?:条件|资格要求)?|项目负责人)"),
    ),
)

_SECTION_STOP_RE = re.compile(
    r"(?:\n\s*3\.\d+(?:\.\d+)?\s*[^\n]{0,40}(?:要求|条件|其他|信誉|联合体|投标)|"
    r"\n\s*[四五六七八九]、)"
)


@dataclass(frozen=True)
class CapabilityRequirement:
    role: str
    requirement_excerpt: str
    constructor_license: str | None
    professional_title: str | None
    testing_certificate: str | None
    prior_project_experience_required: bool
    bidder_employee_required: bool
    social_insurance_proof_required: bool


@dataclass(frozen=True)
class ProjectCapabilityDemandEvent:
    source_id: str
    evidence_kind: str
    title: str
    url: str
    publication_date: str | None
    capability_requirement_count: int
    requirements: list[dict[str, Any]]
    transaction_constraints: list[str]
    provenance: dict[str, Any]


def _official_detail_date(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != HOST:
        return None
    match = _DETAIL_RE.match(parsed.path)
    if not match:
        return None
    raw = match.group(1)
    return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"


def _best_title(doc_title: str, text: str, fallback: str | None) -> str:
    if fallback:
        return fallback
    for line in text.splitlines()[:35]:
        line = normalize_whitespace(line)
        if 8 <= len(line) <= 180 and "项目" in line:
            return line
    return doc_title


def _bounded_excerpt(text: str, start: int, *, max_chars: int = 1800) -> str:
    tail = text[start : start + max_chars]
    stop = _SECTION_STOP_RE.search(tail[80:])
    if stop:
        tail = tail[: 80 + stop.start()]
    return normalize_whitespace(tail)


def _heading_line(text: str, start: int) -> str:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", start)
    if line_end < 0:
        line_end = len(text)
    return normalize_whitespace(text[line_start:line_end])


def _multi_role_summary_heading(line: str) -> bool:
    markers = ("项目经理", "项目总工", "项目负责人")
    return sum(marker in line for marker in markers) >= 2


def _find_first(patterns: tuple[str, ...], text: str) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return normalize_whitespace(match.group(0))
    return None


def _structure_requirement(role: str, excerpt: str, full_text: str) -> CapabilityRequirement:
    constructor_license = _find_first(
        (
            r"(?:公路工程专业)?一级注册建造师(?:资格)?",
            r"(?:公路工程专业)?二级(?:及以上)?注册建造师(?:资格)?",
            r"(?:公路工程专业)?一级(?:及以上)?注册建造师(?:资格)?",
        ),
        excerpt,
    )
    professional_title = _find_first(
        (
            r"(?:公路工程相关专业)?高级工程师(?:或以上)?(?:技术职称)?",
            r"(?:公路工程相关专业)?中级(?:及以上)?技术职称",
            r"高级(?:及以上)?技术职称",
        ),
        excerpt,
    )
    testing_certificate = _find_first(
        (
            r"《公路工程试验检测工程师证书》",
            r"《公路水运工程试验检测师证书》",
            r"公路水运工程试验检测师证书",
            r"公路工程试验检测工程师证书",
        ),
        excerpt,
    )
    prior_experience = bool(
        re.search(r"(?:至少|不少于).{0,35}(?:承担过|担任过|完成过)", excerpt)
        or re.search(r"(?:承担过|担任过).{0,80}(?:项目经理|项目总工|项目负责人)", excerpt)
    )
    bidder_employee_required = bool(
        re.search(r"(?:拟投入|拟派).{0,40}(?:应为|须为)投标人本单位人员", full_text)
    )
    social_insurance_required = bidder_employee_required and bool(
        re.search(r"(?:社保|社会保险).{0,80}(?:证明|缴费|明细)", full_text)
    )
    return CapabilityRequirement(
        role=role,
        requirement_excerpt=excerpt,
        constructor_license=constructor_license,
        professional_title=professional_title,
        testing_certificate=testing_certificate,
        prior_project_experience_required=prior_experience,
        bidder_employee_required=bidder_employee_required,
        social_insurance_proof_required=social_insurance_required,
    )


def extract_project_capability_requirements(text: str) -> list[CapabilityRequirement]:
    """Extract explicit generic role requirements; never infer supply or shortage."""
    found: list[tuple[int, str]] = []
    for role, pattern in _ROLE_PATTERNS:
        for match in pattern.finditer(text):
            found.append((match.start(), role))
    found.sort(key=lambda item: item[0])

    # Combined headings such as “项目经理资格和项目总工资格要求” are merely
    # section summaries. Taking them as a concrete role block can attribute the
    # manager's license to the technical lead, so they are skipped fail-closed.
    result: list[CapabilityRequirement] = []
    seen_roles: set[str] = set()
    for start, role in found:
        if role in seen_roles:
            continue
        heading = _heading_line(text, start)
        if _multi_role_summary_heading(heading):
            continue
        excerpt = _bounded_excerpt(text, start)
        if not any(
            token in excerpt
            for token in (
                "职称",
                "建造师",
                "检测师",
                "检测工程师",
                "承担过",
                "担任过",
                "本单位人员",
                "社保",
            )
        ):
            continue
        requirement = _structure_requirement(role, excerpt, text)
        result.append(requirement)
        seen_roles.add(role)
    return result


class XuzhouProjectCapabilityDemandAdapter:
    def __init__(self, client: PublicHtmlClient | None = None) -> None:
        self.client = client or PublicHtmlClient(
            source_id=SOURCE_ID,
            allowed_hosts={HOST},
            timeout_seconds=30,
            retries=2,
            max_response_bytes=5_000_000,
        )

    def discover_recent(self, *, limit: int = 15) -> dict[str, Any]:
        if limit <= 0 or limit > 100:
            raise ValueError("limit must be between 1 and 100")
        env = self.client.fetch(LIST_URL, request_name="xz_ggzy.transport_tender.list")
        doc = html_to_document(env.html, base_url=env.url)
        items: list[dict[str, str]] = []
        seen: set[str] = set()
        for link in doc.get("links", []):
            url = str(link.get("url", "")).strip()
            url_date = _official_detail_date(url)
            if url_date is None or url in seen:
                continue
            title = re.sub(r"^\[?新\]?", "", normalize_whitespace(str(link.get("text", "")))).strip()
            if not title:
                continue
            seen.add(url)
            items.append({"title": title, "url": url, "publication_date": url_date})
            if len(items) >= limit:
                break
        return {
            "source_id": SOURCE_ID,
            "evidence_kind": "PROJECT_PERSONNEL_CAPABILITY_DEMAND",
            "list_url": LIST_URL,
            "item_count": len(items),
            "items": items,
            "provenance": env.metadata(),
        }

    def fetch_event(self, url: str, *, fallback_title: str | None = None) -> ProjectCapabilityDemandEvent:
        url_date = _official_detail_date(url)
        if url_date is None:
            raise ValueError("URL is not an official Xuzhou transport tender notice")
        env = self.client.fetch(url, request_name="xz_ggzy.transport_tender.detail")
        doc = html_to_document(env.html, base_url=env.url)
        text = doc["text"]
        page_date = _publication_date(text, url)
        if page_date is not None and page_date != url_date:
            raise ValueError(f"tender publication date conflicts with URL: {page_date} != {url_date}")
        requirements = extract_project_capability_requirements(text)
        constraints: list[str] = []
        if any(item.bidder_employee_required for item in requirements):
            constraints.append("BIDDER_EMPLOYEE_TIE_REQUIRED")
        if any(item.social_insurance_proof_required for item in requirements):
            constraints.append("SOCIAL_INSURANCE_PROOF_REQUIRED")
        return ProjectCapabilityDemandEvent(
            source_id=SOURCE_ID,
            evidence_kind="PROJECT_PERSONNEL_CAPABILITY_DEMAND",
            title=_best_title(doc.get("title", ""), text, fallback_title),
            url=url,
            publication_date=page_date or url_date,
            capability_requirement_count=len(requirements),
            requirements=[asdict(item) for item in requirements],
            transaction_constraints=constraints,
            provenance=env.metadata(),
        )

    def collect_recent_events(self, *, limit: int = 10) -> dict[str, Any]:
        discovery = self.discover_recent(limit=limit)
        events: list[dict[str, Any]] = []
        errors: list[dict[str, str]] = []
        for item in discovery["items"]:
            try:
                event = self.fetch_event(item["url"], fallback_title=item["title"])
                if event.capability_requirement_count > 0:
                    events.append(asdict(event))
            except Exception as exc:
                errors.append({"url": item["url"], "error": str(exc)})
        return {
            "source_id": SOURCE_ID,
            "evidence_kind": "PROJECT_PERSONNEL_CAPABILITY_DEMAND",
            "discovery": discovery,
            "event_count": len(events),
            "error_count": len(errors),
            "requirement_count": sum(e["capability_requirement_count"] for e in events),
            "employment_tie_event_count": sum(
                1 for e in events if "BIDDER_EMPLOYEE_TIE_REQUIRED" in e["transaction_constraints"]
            ),
            "social_insurance_proof_event_count": sum(
                1 for e in events if "SOCIAL_INSURANCE_PROOF_REQUIRED" in e["transaction_constraints"]
            ),
            "events": events,
            "errors": errors,
            "truth_boundaries": [
                "PROJECT_REQUIREMENT_IS_NOT_LABOR_SHORTAGE",
                "DEMAND_IS_NOT_SURPLUS_RESOURCE",
                "BIDDER_EMPLOYEE_TIE_IS_A_TRANSACTION_CONSTRAINT",
                "NO_PERSON_PROFILE",
                "NO_HUMAN_CAPABILITY_UNDERUSE_INFERENCE",
                "NO_OPPORTUNITY_INFERENCE",
            ],
        }
