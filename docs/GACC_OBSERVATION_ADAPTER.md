# Governed GACC Observation ingress

`CN_CUSTOMS` is the final production-live source connected to the source-neutral Observation Fabric. This integration does not promote a trade-flow row into demand, payment, resource surplus, blocker, route, or opportunity truth.

## Acceptance gate

The adapter accepts an artifact only when all of the following remain true:

- the source is `CN_CUSTOMS` and the evidence kind is `CUSTOMS_TRADE_FLOW`;
- transport is explicitly `PLAINTEXT_HTTP` and corroboration remains required;
- the artifact has `gacc-source-row-evidence.v1` for every serialized row;
- row cells, row hash, table identity, source URL and table payload SHA all validate;
- the independent Jiangsu Government HTTPS source corroborates the same period, Jiangsu identity and import/export direction;
- corroboration basis remains `PERIOD_IDENTITY_DIRECTION_ONLY` and monetary comparison remains `UNAVAILABLE_CROSS_CURRENCY`.

The HTTPS corroborator is an acceptance gate, not monetary evidence for a GACC row. Each semantic trade claim cites the exact GACC source row only.

## Geography and scope

The current live artifact contains:

- the Jiangsu importer/exporter-location row from GACC table 8;
- Xuzhou CBZ from GACC table 11;
- Xuzhou BLC from GACC table 11;
- no Xuzhou whole-city importer/exporter-location row.

Therefore the Fabric preserves the whole-city gap as UNKNOWN. A Xuzhou specific customs area is not a Xuzhou city aggregate, and importer/exporter location is not domestic origin/destination.

## Claim semantics

Trade amounts are `FLOW` claims. Reported year-over-year rates are separate `CHANGE` claims. Table-8 total trade is derived export plus import, so it is verified for internal consistency but intentionally not emitted as a source-native claim. Table-11 totals are explicit source cells and may be emitted with `total_basis=EXPLICIT_GACC`.

Observation identity is stable on period + table + row identity. Payload and row hashes remain evidence fingerprints, so a later official correction becomes a durable revision rather than a second current identity.

## Coverage meaning

Once production ingestion succeeds, 8/8 live-source coverage means all eight sources marked production-live in `data/source_registry.csv` have governed adapter support and appear in the latest unified Fabric. It does **not** mean complete geographic, behavioral, industry, or evidence-channel coverage.
