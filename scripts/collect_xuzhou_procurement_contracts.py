#!/usr/bin/env python3
"""Collect exact-project Xuzhou procurement contract announcements."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.network_ingest import NetworkIngestError, write_json_atomic
from src.xuzhou_procurement_contracts import XuzhouProcurementContractAdapter


def _project_ids_from_value(value: Any) -> list[str]:
    result: list[str] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            project_id = node.get("project_id")
            if project_id is not None:
                text = str(project_id).strip()
                if text and text not in result:
                    result.append(text)
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)

    visit(value)
    return result


def _load_project_ids(paths: list[str]) -> list[str]:
    result: list[str] = []
    for raw_path in paths:
        path = Path(raw_path)
        payload = json.loads(path.read_text(encoding="utf-8"))
        for project_id in _project_ids_from_value(payload):
            if project_id not in result:
                result.append(project_id)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Query the first-party Xuzhou contract archive by exact procurement "
            "project ID and revalidate project identity from each contract body"
        )
    )
    parser.add_argument(
        "--project-id",
        action="append",
        default=[],
        help="Exact project ID to query; may be repeated",
    )
    parser.add_argument(
        "--input-json",
        action="append",
        default=[],
        help=(
            "JSON artifact from which project_id fields are recursively extracted; "
            "may be repeated"
        ),
    )
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--max-records-per-project", type=int, default=100)
    parser.add_argument("--require-contracts", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args()

    project_ids: list[str] = []
    for value in args.project_id:
        text = str(value or "").strip()
        if text and text not in project_ids:
            project_ids.append(text)
    try:
        for project_id in _load_project_ids(args.input_json):
            if project_id not in project_ids:
                project_ids.append(project_id)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"contract project-id input failed: {exc}", file=sys.stderr)
        return 2

    if not project_ids:
        print("no project IDs supplied", file=sys.stderr)
        return 2

    try:
        payload = XuzhouProcurementContractAdapter().collect_projects(
            project_ids,
            page_size=args.page_size,
            max_records_per_project=args.max_records_per_project,
        )
        if args.output:
            write_json_atomic(args.output, payload)
            print(f"wrote {args.output}")
        else:
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        if args.require_contracts and payload["contract_count"] == 0:
            print("no exact-project procurement contracts found", file=sys.stderr)
            return 3
        return 0
    except (NetworkIngestError, ValueError) as exc:
        print(f"procurement contract collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
