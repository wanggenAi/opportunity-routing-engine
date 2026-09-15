#!/usr/bin/env python3
"""Build/update the durable live Observation Fabric from existing sensor artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.gacc_trade_observation_adapter import gacc_trade_flow_observations
from src.live_observation_adapters import (
    jiangsu_money_flow_observations,
    xuzhou_procurement_observations,
    xuzhou_resource_underuse_observations,
)
from src.live_observation_pipeline import ingest_live_observations, summarize_live_store
from src.observation_store import SQLiteObservationStore
from src.official_macro_observation_adapters import (
    nbs_macro_watchlist_observations,
    pbc_jiangsu_credit_observations,
)
from src.pbc_observation_adapter import pbc_money_flow_observations
from src.questmobile_research_observation_adapter import (
    questmobile_public_research_observations,
)
from src.xuzhou_financing_demand_observation_adapter import (
    xuzhou_financing_demand_observations,
)


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def build(
    *,
    jiangsu_path: Path,
    procurement_path: Path,
    resource_paths: list[Path],
    nbs_path: Path,
    pbc_jiangsu_path: Path,
    pbc_money_flow_path: Path,
    xuzhou_financing_demand_path: Path,
    gacc_trade_flow_path: Path,
    questmobile_public_research_path: Path,
    store_path: Path,
    output_path: Path,
    current_jsonl_path: Path,
    upstream_manifest_path: Path | None = None,
) -> dict:
    if not resource_paths:
        raise ValueError("at least one resource-underuse artifact is required")

    envelopes = []
    envelopes.extend(jiangsu_money_flow_observations(_load_json(jiangsu_path)))
    envelopes.extend(xuzhou_procurement_observations(_load_json(procurement_path)))
    for path in resource_paths:
        envelopes.extend(xuzhou_resource_underuse_observations(_load_json(path)))
    envelopes.extend(nbs_macro_watchlist_observations(_load_json(nbs_path)))
    envelopes.extend(pbc_jiangsu_credit_observations(_load_json(pbc_jiangsu_path)))
    envelopes.extend(pbc_money_flow_observations(_load_json(pbc_money_flow_path)))
    envelopes.extend(
        xuzhou_financing_demand_observations(_load_json(xuzhou_financing_demand_path))
    )
    envelopes.extend(gacc_trade_flow_observations(_load_json(gacc_trade_flow_path)))
    envelopes.extend(
        questmobile_public_research_observations(
            _load_json(questmobile_public_research_path)
        )
    )
    if not envelopes:
        raise ValueError("live adapters produced no observations")

    manifest = _load_json(upstream_manifest_path) if upstream_manifest_path else None
    store_path.parent.mkdir(parents=True, exist_ok=True)
    with SQLiteObservationStore(store_path) as store:
        transitions = ingest_live_observations(store, envelopes)
        assessment = summarize_live_store(
            store,
            input_observation_count=len(envelopes),
            transition_counts=transitions,
            upstream_manifest=manifest,
        )
        current_envelopes = tuple(store.iter_current())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(assessment, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    current_jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with current_jsonl_path.open("w", encoding="utf-8") as handle:
        for envelope in current_envelopes:
            handle.write(json.dumps(envelope.as_dict(), ensure_ascii=False, sort_keys=True) + "\n")
    return assessment


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--jiangsu-money-flow", type=Path, required=True)
    parser.add_argument("--xuzhou-procurement", type=Path, required=True)
    parser.add_argument("--resource-underuse", type=Path, action="append", default=[])
    parser.add_argument("--nbs-macro-watchlist", type=Path, required=True)
    parser.add_argument("--pbc-jiangsu-credit", type=Path, required=True)
    parser.add_argument("--pbc-money-flow", type=Path, required=True)
    parser.add_argument("--xuzhou-financing-demand", type=Path, required=True)
    parser.add_argument("--gacc-trade-flow", type=Path, required=True)
    parser.add_argument("--questmobile-public-research", type=Path, required=True)
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--current-jsonl", type=Path, required=True)
    parser.add_argument("--upstream-manifest", type=Path)
    args = parser.parse_args()
    assessment = build(
        jiangsu_path=args.jiangsu_money_flow,
        procurement_path=args.xuzhou_procurement,
        resource_paths=args.resource_underuse,
        nbs_path=args.nbs_macro_watchlist,
        pbc_jiangsu_path=args.pbc_jiangsu_credit,
        pbc_money_flow_path=args.pbc_money_flow,
        xuzhou_financing_demand_path=args.xuzhou_financing_demand,
        gacc_trade_flow_path=args.gacc_trade_flow,
        questmobile_public_research_path=args.questmobile_public_research,
        store_path=args.store,
        output_path=args.output,
        current_jsonl_path=args.current_jsonl,
        upstream_manifest_path=args.upstream_manifest,
    )
    print(json.dumps(assessment, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
