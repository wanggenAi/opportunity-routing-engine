# QuestMobile Public Research Evidence

This producer ingests a bounded set of **publicly accessible QuestMobile research-report pages**. It exists to improve the `REPRESENTATIVE_RESEARCH` sensor evidence channel without buying a database, bypassing login, reverse-engineering private endpoints, or converting a research narrative into commercial truth.

## Collection scope

The collector starts from the public research index:

`https://www.questmobile.com.cn/research/report-list`

It follows only canonical detail URLs on `www.questmobile.com.cn` matching `/research/report/<numeric-id>/`, with a configurable hard limit of 1–10 reports. Production currently requests the latest five public reports.

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

## Why findings remain text evidence

QuestMobile reports can contain panel/sample metrics, synthesized interpretation and chart-derived statements. The producer therefore does **not** parse every number into a hard market statistic. It preserves exact source-native excerpts first. A later Observation adapter may record those excerpts as `EVIDENCE`, but cannot silently upgrade them into paid demand, payer identity, payment, current Xuzhou reality, or an opportunity.

## Production contract

`scripts/validate_questmobile_public_research.py` independently verifies report counts, unique IDs/URLs, canonical host/path, publication dates, exact source authority, page provenance hashes, finding counts, attribution-to-excerpt binding and recomputed excerpt hashes.

`.github/workflows/questmobile-public-research-live.yml` runs the full repository tests, performs a real public collection, validates the artifact and uploads `questmobile-public-research-evidence`.

The source registry remains non-production during this producer-only phase. `QM` must not become production-live until a real GitHub Actions run proves that public collection and validation work end-to-end.

## Truth boundaries

- Public report page only; no login or paid database.
- No OCR or image-metric extraction in this producer.
- `NO_TEXT_FINDING != 0`.
- A research report is not current local reality.
- A panel/sample result is not a census fact.
- A research finding is not paid demand, payer identity, payment or opportunity truth.
- Exact excerpt and page provenance are required.
- `UNKNOWN != PASS`.
