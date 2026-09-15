# GACC row-level evidence contract

`CN_CUSTOMS` is an official but currently plaintext-HTTP GACC source. Its live producer therefore remains corroboration-gated and must preserve two distinct evidence layers before any parsed trade value can enter the unified Observation Fabric.

1. The GACC table payload provenance proves which official page was parsed.
2. `gacc-source-row-evidence.v1` binds every serialized Jiangsu/Xuzhou row to the exact normalized source cells from the same immutable payload SHA-256.

The row-evidence enrichment performs a second, tightly scoped fetch of the already-selected GACC table page. The second payload SHA-256 must equal the first parser fetch exactly. If the page changed, the source row is missing, or the row identity is ambiguous, the collection fails closed instead of emitting partially bound evidence.

The Jiangsu Government HTTPS corroborator remains a separate dataset-acceptance gate. It corroborates period, Jiangsu identity, and import/export direction only. It does not independently confirm the USD value of a GACC row and must never be treated as row-level value corroboration.

Truth boundaries remain explicit:

- whole-page hash != row-level lineage;
- corroboration gate != row-level value confirmation;
- importer/exporter location != domestic origin/destination;
- Xuzhou specific customs area != whole Xuzhou;
- derived table-8 total != source cell;
- missing != zero;
- trade flow != payment, paid need, blocker, or opportunity.
