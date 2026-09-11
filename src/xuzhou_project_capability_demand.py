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

# Bare role words occur frequently in experience descriptions and statutory
# certificate names. Candidate headings therefore need either explicit
# qualification wording or a numbered requirement immediately after the role.
_ROLE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "PROJECT_MANAGER",
        re.compile(
            r"(?:[aA][.．、]\s*)?项目经理(?:（项目负责人）|\(项目负责人\))?"
            r"(?:资格(?:条件|要求)?|条件|要求|应满足的要求|(?=\s*[（(]?\d+[）)]?))"
        ),
    ),
    (
        "PROJECT_TECHNICAL_LEAD",
        re.compile(
            r"(?:[bB][.．、]\s*)?项目总工"
            r"(?:（项目技术负责人）|\(项目技术负责人\)|（技术负责人）|\(技术负责人\))?"
            r"(?:资格(?:条件|要求)?|条件|要求|(?=\s*[（(]?\d+[）)]?))"
        ),
    ),
    (
        "PROJECT_LEAD",
        re.compile(
            r"(?:拟派|拟投入)?项目负责人(?:资格(?:条件|要求)?|条件|要求|应满足的要求)"
        ),
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


def _bounded_excerpt(
    text: str,
    start: int,
    *,
    next_role_start: int | None = None,
    max_chars: int = 1800,
) -> str:
    end = min(len(text), start + max_chars)
    if next_role_start is not None and start < next_role_start < end:
        end = next_role_start
    tail = text[start:end]
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
    # Parenthetical aliases are the same person-role, not a second role. Normalize
    # them before testing whether a line really summarizes multiple distinct roles.
    normalized = line
    for alias, canonical in (
        ("项目经理（项目负责人）", "项目经理"),
        ("项目经理(项目负责人)", "项目经理"),
        ("项目总工（项目技术负责人）", "项目总工"),
        ("项目总工(项目技术负责人)", "项目总工"),
        ("项目总工（技术负责人）", "项目总工"),
        ("项目总工(技术负责人)", "项目总工"),
    ):
        normalized = normalized.replace(alias, canonical)
    markers = ("项目经理", "项目总工", "项目负责人")
    return sum(marker in normalized for marker in markers) >= 2


def _qualification_scope(excerpt: str) -> str:
    """Keep credential parsing inside the role's own qualification clause.

    Shared employment/social-insurance notes and later explanatory notes are kept
    in the raw excerpt for audit, but must not leak another role's credentials into
    this role's structured fields.
    """

    cut = len(excerpt)
    for marker in (" 注：", " 注:", " 拟投入", " 拟派"):
        pos = excerpt.find(marker, 40)
        if pos >= 0:
            cut = min(cut, pos)
    return excerpt[:cut]


def _find_first(patterns: tuple[str, ...], text: str) -> str | None:
    """Return the earliest matched evidence, not the first pattern that matches."""
    matches: list[re.Match[str]] = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            matches.append(match)
    if not matches:
        return None
    match = min(matches, key=lambda item: item.start())
    return normalize_whitespace(match.group(0))


def _structure_requirement(role: str, excerpt: str, full_text: str) -> CapabilityRequirement:
    local = _qualification_scope(excerpt)
    constructor_license = _find_first(
        (
            r"(?:公路工程(?:专业)?|机电工程(?:专业)?)?"
            r"(?:一级|二级)(?:及以上)?(?:建造师注册证书|注册建造师(?:资格|证书)?)",
        ),
        local,
    )
    professional_title = _find_first(
        (
            r"(?:公路工程相关专业)?副高级(?:或以上|及以上)?专业技术职称",
            r"(?:公路工程相关专业)?高级工程师(?:或以上|及以上)?(?:技术职称)?",
            r"(?:公路工程相关专业)?中级(?:及以上)?技术职称",
            r"(?:公路工程相关专业)?工程师(?:或以上|及以上)?技术职称",
            r"高级(?:及以上)?技术职称",
        ),
        local,
    )
    testing_certificate = _find_first(
        (
            r"《公路工程试验检测工程师证书》",
            r"《公路水运工程试验检测师证书》",
            r"公路工程试验检测工程师或试验检测师证书",
            r"公路水运工程试验检测师证书",
            r"公路工程试验检测工程师证书",
        ),
        local,
    )
    prior_experience = bool(
        re.search(r"(?:至少|不少于).{0,60}(?:承担过|担任过|完成过)", excerpt)
        or re.search(r"(?:承担过|担任过|完成过).{0,100}(?:项目经理|项目总工|项目负责人)", excerpt)
        or re.search(r"(?:业绩要求.{0,160}?(?:完成过|承担过)|完成过以下类似业绩)", excerpt)
    )
    # Employment/social-insurance ties may be stated once for several roles, so
    # those transaction constraints remain event-level corroboration.
    bidder_employee_required = bool(
        re.search(r"(?:拟投入|拟派).{0,60}(?:应为|须为|必须为)投标人本单位人员", full_text)
        or re.search(r"(?:拟投入|拟派).{0,60}必须为申请人自有人员", full_text)
    )
    social_insurance_required = bidder_employee_required and bool(
        re.search(r"(?:社保|社会保险).{0,100}(?:证明|缴费|明细)", full_text)
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


def _role_candidates(text: str) -> list[tuple[int, str]]:
    found: list[tuple[int, str]] = []
    for role, pattern in _ROLE_PATTERNS:
        for match in pattern.finditer(text):
            found.append((match.start(), role))
    found.sort(key=lambda item: item[0])
    return found


def extract_project_capability_requirements(text: str) -> list[CapabilityRequirement]:
    """Extract explicit generic role requirements; never infer supply or shortage."""
    found = _role_candidates(text)
    result: list[CapabilityRequirement] = []
    seen_roles: set[str] = set()

    for index, (start, role) in enumerate(found):
        if role in seen_roles:
            continue
        heading = _heading_line(text, start)
        if _multi_role_summary_heading(heading):
            continue

        next_role_start = found[index + 1][0] if index + 1 < len(found) else None
        next_role = found[index + 1][1] if index + 1 < len(found) else None
        # Some notices use “拟派项目负责人应满足的要求” only as an umbrella,
        # immediately followed by a concrete project-manager subsection. It is
        # not a third personnel role.
        if (
            role == "PROJECT_LEAD"
            and next_role in {"PROJECT_MANAGER", "PROJECT_TECHNICAL_LEAD"}
            and next_role_start is not None
            and next_role_start - start < 250
        ):
            continue

        excerpt = _bounded_excerpt(
            text,
            start,
            next_role_start=next_role_start,
        )
        if not any(
            token in excerpt
            for token in (
                "职称",
                "建造师",
                "检测师",
                "检测工程师",
                "承担过",
                "担任过",
                "完成过",
                "本单位人员",
                "自有人员",
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
