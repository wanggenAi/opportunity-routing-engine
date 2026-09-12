"""Fail-closed package-scope helpers for procurement lifecycle promotion.

A project_id is necessary but not always sufficient transaction identity. Multi-package
procurements may publish package-specific awards, contracts, and settlements. A
package-specific or package-unresolved settlement must never promote a project-level
NeedSignal unless the canonical Need itself is package-scoped. V1 therefore blocks
that promotion rather than aggregating or guessing package semantics.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

_PACKAGE_RE = re.compile(r"采购包\s*([0-9]+)")
_WHOLE_PROJECT_LABELS = {"项目整体", "全部采购包", "所有采购包", "全项目", "整体项目"}


def _text(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None


def _unique(values: Iterable[object]) -> list[str]:
    result: list[str] = []
    for value in values:
        text = _text(value)
        if text and text not in result:
            result.append(text)
    return result


def _normalize_package_name(value: object) -> str | None:
    text = _text(value)
    if not text:
        return None
    match = _PACKAGE_RE.fullmatch(text)
    if match:
        return f"采购包{int(match.group(1))}"
    return text


def discover_tender_package_names(tender: Mapping[str, Any]) -> list[str]:
    """Return only package identities explicitly present in the tender artifact."""

    explicit = tender.get("package_names")
    values: list[object] = []
    if isinstance(explicit, (list, tuple)):
        values.extend(explicit)
    elif explicit is not None:
        values.append(explicit)

    package_name = tender.get("package_name")
    if package_name is not None:
        values.append(package_name)

    for field in ("budget_raw", "budget_breakdown_raw"):
        raw = _text(tender.get(field))
        if not raw:
            continue
        values.extend(f"采购包{int(number)}" for number in _PACKAGE_RE.findall(raw))

    normalized = [_normalize_package_name(value) for value in values]
    return _unique(value for value in normalized if value)


def settlement_package_names(items: Iterable[Mapping[str, Any]]) -> list[str]:
    return _unique(
        value
        for item in items
        for value in [_normalize_package_name(item.get("package_name"))]
        if value
    )


def package_scope(tender_package_names: Iterable[str]) -> str:
    names = _unique(tender_package_names)
    if len(names) > 1:
        return "MULTI_PACKAGE_PROJECT"
    return "SINGLE_PACKAGE_OR_UNSPECIFIED"


def package_scoped_settlement_blocks_project_need(
    tender_package_names: Iterable[str],
    settlement_items: Iterable[Mapping[str, Any]],
) -> bool:
    """Return True when settlement scope cannot safely promote a project Need.

    For an explicitly multi-package tender, missing package identity is UNKNOWN, not
    evidence of a whole-project settlement. Promotion is allowed only when every
    settlement item explicitly declares a whole-project scope label. Package-specific
    settlements remain package-scoped even if multiple packages are present.
    """

    names = _unique(tender_package_names)
    if len(names) <= 1:
        return False

    items = list(settlement_items)
    if not items:
        return False

    for item in items:
        name = _normalize_package_name(item.get("package_name"))
        if name not in _WHOLE_PROJECT_LABELS:
            return True
    return False
