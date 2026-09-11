"""Adapter for the 2026 National Bureau of Statistics '国家数据' release API.

The NBS site migrated away from the legacy easyquery interface. This adapter uses
only the current public release endpoints under:
https://data.stats.gov.cn/dg/website/publicrelease/web/external/

Truth rule: an advertised period is not necessarily a populated period. Empty values
remain unavailable and are never converted into zero or evidence.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any, Iterable

from src.network_ingest import JsonHttpClient


NBS_BASE_URL = "https://data.stats.gov.cn"
NBS_API_PREFIX = "/dg/website/publicrelease/web/external"
MISSING_VALUE_MARKERS = {"", "--", "—", "…", "...", "null", "none", "nan"}


@dataclass(frozen=True)
class PageSpec:
    name: str
    code: int
    frequency: str
    route: str
    has_area: bool = False


PAGE_SPECS = {
    "monthData": PageSpec("monthData", 1, "month", "monthData"),
    "quarterData": PageSpec("quarterData", 2, "quarter", "quarterData"),
    "yearData": PageSpec("yearData", 3, "year", "yearData"),
    "fsMonthData": PageSpec("fsMonthData", 4, "month", "fsMonthData", True),
    "fsQuarterData": PageSpec("fsQuarterData", 5, "quarter", "fsQuarterData", True),
    "fsYearData": PageSpec("fsYearData", 6, "year", "fsYearData", True),
    "mainMonthData": PageSpec("mainMonthData", 7, "month", "mainMonthData", True),
    "mainYearData": PageSpec("mainYearData", 8, "year", "mainYearData", True),
}


def is_populated_value(value: Any) -> bool:
    """Return True only when a source value is materially present.

    Numeric zero is valid. Empty strings and common NBS missing markers are not.
    """

    if value is None:
        return False
    if isinstance(value, (int, float)):
        return True
    return str(value).strip().lower() not in MISSING_VALUE_MARKERS


def normalize_period_token(token: str, frequency: str) -> str:
    token = token.strip().upper()
    if frequency == "month":
        if token.endswith("MM"):
            return token
        digits = "".join(ch for ch in token if ch.isdigit())
        if len(digits) != 6:
            raise ValueError("month period must be YYYYMM")
        return f"{digits}MM"
    if frequency == "year":
        if token.endswith("YY"):
            return token
        digits = "".join(ch for ch in token if ch.isdigit())
        if len(digits) != 4:
            raise ValueError("year period must be YYYY")
        return f"{digits}YY"
    if frequency == "quarter":
        if token.endswith("SS"):
            return token
        if len(token) == 6 and token[:4].isdigit() and token[4] == "Q" and token[5] in "1234":
            return f"{token[:4]}0{token[5]}SS"
        digits = "".join(ch for ch in token if ch.isdigit())
        if len(digits) == 6:
            return f"{digits}SS"
        raise ValueError("quarter period must be YYYYQ1..YYYYQ4 or YYYY0Q")
    raise ValueError(f"unsupported frequency: {frequency}")


def normalize_periods(periods: Iterable[str] | None, frequency: str) -> list[str] | str:
    if periods is None:
        return ""
    result: list[str] = []
    for item in periods:
        text = str(item).strip()
        if not text:
            continue
        if "-" in text:
            start, end = text.split("-", 1)
            result.append(
                f"{normalize_period_token(start, frequency)}-{normalize_period_token(end, frequency)}"
            )
        else:
            result.append(normalize_period_token(text, frequency))
    return result if result else ""


class NBSAdapter:
    def __init__(self, client: JsonHttpClient | None = None) -> None:
        self.client = client or JsonHttpClient(
            source_id="CN_NBS",
            allowed_hosts={"data.stats.gov.cn"},
            timeout_seconds=30,
            retries=2,
            retry_backoff_seconds=1.0,
        )
        self._root_ids: dict[str, str] = {}

    @staticmethod
    def _spec(page: str) -> PageSpec:
        try:
            return PAGE_SPECS[page]
        except KeyError as exc:
            raise ValueError(f"unknown NBS page: {page}") from exc

    @staticmethod
    def _url(path: str) -> str:
        return f"{NBS_BASE_URL}{NBS_API_PREFIX}{path}"

    def _headers(self, page: str) -> dict[str, str]:
        spec = self._spec(page)
        return {
            "Origin": NBS_BASE_URL,
            "Referer": f"{NBS_BASE_URL}/dg/website/page.html#/pc/national/{spec.route}",
            "X-Requested-With": "XMLHttpRequest",
        }

    def root_nodes(self, page: str) -> list[dict[str, Any]]:
        spec = self._spec(page)
        envelope = self.client.request_json(
            "GET",
            self._url("/new/queryIndexTreeAsync"),
            request_name=f"nbs.root.{page}",
            params={"pid": "", "code": spec.code},
            headers=self._headers(page),
        )
        nodes = envelope.payload.get("data", [])
        if not isinstance(nodes, list):
            raise ValueError("NBS root response data must be a list")
        return nodes

    def root_id(self, page: str) -> str:
        if page in self._root_ids:
            return self._root_ids[page]
        roots = self.root_nodes(page)
        if not roots or not roots[0].get("_id"):
            raise ValueError(f"NBS returned no root id for {page}")
        root_id = str(roots[0]["_id"])
        self._root_ids[page] = root_id
        return root_id

    def tree(self, page: str, *, pid: str) -> list[dict[str, Any]]:
        spec = self._spec(page)
        envelope = self.client.request_json(
            "GET",
            self._url("/new/queryIndexTreeAsync"),
            request_name=f"nbs.tree.{page}",
            params={"pid": pid, "code": spec.code},
            headers=self._headers(page),
        )
        nodes = envelope.payload.get("data", [])
        if not isinstance(nodes, list):
            raise ValueError("NBS tree response data must be a list")
        return nodes

    def indicators(self, page: str, *, cid: str, dt: str = "") -> list[dict[str, Any]]:
        envelope = self.client.request_json(
            "GET",
            self._url("/new/queryIndicatorsByCid"),
            request_name=f"nbs.indicators.{page}.{cid}",
            params={"cid": cid, "dt": dt, "name": ""},
            headers=self._headers(page),
        )
        items = envelope.payload.get("data", {}).get("list", [])
        if not isinstance(items, list):
            raise ValueError("NBS indicator list must be a list")
        return [
            {
                "indicator_id": str(item.get("_id", "")),
                "label": str(item.get("i_showname", "")).strip(),
                "unit": str(item.get("du_name", item.get("du", ""))),
                "catalog_id": str(item.get("catalogid", cid)),
                "raw": item,
            }
            for item in items
        ]

    def dates(self, page: str, *, cid: str) -> dict[str, Any]:
        envelope = self.client.request_json(
            "GET",
            self._url("/new/queryDtByCid"),
            request_name=f"nbs.dates.{page}.{cid}",
            params={"cid": cid, "rootId": self.root_id(page)},
            headers=self._headers(page),
        )
        if not isinstance(envelope.payload, dict):
            raise ValueError("NBS dates response must be an object")
        return envelope.payload

    def discover_catalogs(
        self,
        page: str,
        *,
        keywords: Iterable[str],
        max_depth: int = 8,
        max_nodes: int = 600,
        limit_per_keyword: int = 5,
    ) -> dict[str, list[dict[str, Any]]]:
        """Breadth-first catalog discovery with explicit network/request bounds."""

        wanted = [k.strip() for k in keywords if k.strip()]
        if not wanted:
            raise ValueError("at least one keyword is required")
        if max_depth < 0 or max_nodes <= 0 or limit_per_keyword <= 0:
            raise ValueError("discovery bounds must be positive")

        roots = self.root_nodes(page)
        queue: deque[tuple[dict[str, Any], int, list[str]]] = deque(
            (node, 0, [str(node.get("name", ""))]) for node in roots
        )
        results = {keyword: [] for keyword in wanted}
        visited = 0

        while queue and visited < max_nodes:
            node, depth, path = queue.popleft()
            visited += 1
            name = str(node.get("name", ""))
            is_leaf = bool(node.get("isLeaf"))
            for keyword in wanted:
                if keyword in name and len(results[keyword]) < limit_per_keyword:
                    results[keyword].append(
                        {
                            "cid": str(node.get("_id", "")),
                            "name": name,
                            "is_leaf": is_leaf,
                            "path": path,
                            "depth": depth,
                        }
                    )

            if depth >= max_depth or is_leaf:
                continue
            node_id = str(node.get("_id", ""))
            if not node_id:
                continue
            for child in self.tree(page, pid=node_id):
                queue.append((child, depth + 1, path + [str(child.get("name", ""))]))

            if all(len(results[keyword]) >= limit_per_keyword for keyword in wanted):
                break

        return results

    def fetch_values(
        self,
        page: str,
        *,
        cid: str,
        indicator_ids: Iterable[str],
        periods: Iterable[str] | None = None,
        areas: Iterable[dict[str, str]] | None = None,
        show_type: int = 1,
    ) -> dict[str, Any]:
        spec = self._spec(page)
        ids = [str(item).strip() for item in indicator_ids if str(item).strip()]
        if not ids:
            raise ValueError("indicator_ids must not be empty")
        area_values = list(areas) if areas is not None else [
            {"text": "全国", "value": "000000000000"}
        ]
        payload = {
            "cid": cid,
            "indicatorIds": ids,
            "daCatalogId": "",
            "das": area_values,
            "showType": show_type,
            "dts": normalize_periods(periods, spec.frequency),
            "rootId": self.root_id(page),
        }
        envelope = self.client.request_json(
            "POST",
            self._url("/stream/esData"),
            request_name=f"nbs.values.{page}.{cid}",
            json_body=payload,
            headers=self._headers(page),
        )
        raw = envelope.payload
        records: list[dict[str, Any]] = []
        for period in raw.get("data", []) if isinstance(raw, dict) else []:
            for item in period.get("values", []):
                value = item.get("value")
                area_code = str(item.get("areaCode") or item.get("da") or "")
                area_name = str(item.get("area") or item.get("da_name") or "")
                records.append(
                    {
                        "source_id": "CN_NBS",
                        "page": page,
                        "frequency": spec.frequency,
                        "cid": cid,
                        "period_code": str(period.get("code", "")),
                        "period_name": str(period.get("name", "")),
                        "indicator_id": str(item.get("_id", "")),
                        "indicator_label": str(item.get("i_showname", "")).strip(),
                        "unit": str(item.get("du_name", "")),
                        "area_name": area_name,
                        "area_code": area_code,
                        "value": value,
                        "value_present": is_populated_value(value),
                    }
                )
        populated = [record for record in records if record["value_present"]]
        populated_periods = sorted(
            {record["period_code"] for record in populated if record["period_code"]},
            reverse=True,
        )
        return {
            "request": envelope.metadata(),
            "payload": payload,
            "observed_row_count": len(records),
            "populated_row_count": len(populated),
            "populated_periods": populated_periods,
            "latest_populated_period": populated_periods[0] if populated_periods else None,
            "records": records,
            "raw": raw,
        }

    def probe(self, pages: Iterable[str]) -> dict[str, Any]:
        result: dict[str, Any] = {"source_id": "CN_NBS", "pages": {}}
        for page in pages:
            roots = self.root_nodes(page)
            if not roots:
                result["pages"][page] = {"root": None, "children": []}
                continue
            root = roots[0]
            root_id = str(root.get("_id", ""))
            self._root_ids[page] = root_id
            children = self.tree(page, pid=root_id) if root_id else []
            result["pages"][page] = {
                "root": {
                    "id": root_id,
                    "name": root.get("name", ""),
                    "is_leaf": bool(root.get("isLeaf")),
                },
                "children": [
                    {
                        "id": str(child.get("_id", "")),
                        "name": child.get("name", ""),
                        "is_leaf": bool(child.get("isLeaf")),
                    }
                    for child in children
                ],
            }
        return result
