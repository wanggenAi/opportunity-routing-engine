#!/usr/bin/env python3
"""Collect bounded public QuestMobile research evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.questmobile_public_research import QuestMobilePublicResearchCollector


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-limit", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    payload = QuestMobilePublicResearchCollector().collect(report_limit=args.report_limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "source_id": payload["source_id"],
        "report_count": payload["report_count"],
        "text_finding_count": payload["text_finding_count"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
