#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gacc_trade_flow import GaccTradeFlowAdapter


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect official GACC Jiangsu/Xuzhou trade-flow evidence")
    parser.add_argument("--output", default=".local/gacc_trade_flow.json")
    args = parser.parse_args()

    payload = GaccTradeFlowAdapter().collect()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    print("period=", payload["period"])
    print("jiangsu_ytd_usd_thousand=", payload["jiangsu_importer_exporter_location"]["total_ytd_usd_thousand"])
    print("xuzhou_location=", json.dumps(payload["xuzhou_importer_exporter_location"], ensure_ascii=False, sort_keys=True))
    print("xuzhou_specific_areas=", json.dumps(payload["xuzhou_specific_areas"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
