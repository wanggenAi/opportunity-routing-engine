# QuestMobile Public Research Evidence

This producer ingests a bounded set of **publicly accessible QuestMobile research-report pages**. It improves the `REPRESENTATIVE_RESEARCH` sensor evidence channel without buying a database, bypassing login, reverse-engineering private endpoints, or converting research narrative into commercial truth.

## Collection scope

The collector starts from the public research index:

`https://www.questmobile.com.cn/research/report-list`

It follows only canonical detail URLs on `www.questmobile.com.cn` matching `/research/report/<numeric-id>/`, with a configurable hard limit of 1–10 reports. Production currently requests the latest five public report links exposed by the index; fewer may be collected when fewer governed links are currently visible.

For every detail page the producer binds:

- numeric report ID;
- exact public report title;
- publication date anchored after that title;
- exact source authority `QuestMobile研究院`;
- optional public industry/category text;
- canonical source URL;
- fetched-at timestamp and full-page SHA-256;
- exact source-native textual findings whose normalized text contains `QuestMobile数据显示` or `QuestAuto数据显示`;
- SHA-256 of every retained finding excerpt.

The producer never OCRs charts/images. A report whose useful evidence is image-only remains `NO_TEXT_FINDING`; missing text is not treated as zero.

## Observation Fabric ingress

After real PR and main GitHub Actions runs proved the public producer and validator end-to-end, `QM` is governed as `ACTIVE_LIVE_PUBLIC_REPORTS`.

`src/questmobile_research_observation_adapter.py` converts only text-supported reports into source-neutral Observation envelopes. Every source-native finding becomes:

- primitive: `EVIDENCE`;
- concept: `PUBLIC_RESEARCH_FINDING_EXCERPT`;
- epistemic state: `OBSERVED`;
- geography: `CN` only;
- evidence: exact public excerpt + report page URL + report page SHA-256.

The adapter deliberately does not parse report percentages or prose into hard market facts. `representativeness_status`, current-local-reality status and paid-demand status remain explicitly not established. Image-only reports are not promoted into empty observations.

Stable observation identity is based on report identity/URL rather than page hash, so a later public-page correction becomes a durable revision instead of a new logical report.

## Production contract

`scripts/validate_questmobile_public_research.py` independently verifies report counts, unique IDs/URLs, canonical host/path, publication dates, exact source authority, page provenance hashes, finding counts, attribution-to-excerpt binding and recomputed excerpt hashes.

`.github/workflows/questmobile-public-research-live.yml` runs the full repository tests, performs a real public collection, validates the artifact and uploads `questmobile-public-research-evidence`.

The live Observation Fabric resolves the latest completed/successful main QuestMobile producer run and refuses to fall back to an older successful artifact if the latest producer run fails.

## Truth boundaries

- Public report page only; no login or paid database.
- No OCR or image-metric extraction in this producer.
- `NO_TEXT_FINDING != 0`.
- A research report is not current Jiangsu/Xuzhou reality.
- A panel/sample result is not a census fact.
- An observed research channel does not prove representative population coverage.
- A research finding is not paid demand, payer identity, payment or opportunity truth.
- Exact excerpt and page provenance are required.
- `UNKNOWN != PASS`.
