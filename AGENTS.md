# AGENTS.md

Instructions for AI agents, coding assistants, and human contributors working in this repository.

## Prime directive

The commercial objective is to determine whether AI + software + local Xuzhou execution can repeatedly turn fragmented overseas demand signals into qualified, reachable buyer opportunities and supplier matches that progress toward real transactions.

Do not optimize for code volume. Optimize for truthful evidence and measurable commercial progress.

## Source of truth

Before changing business logic, read:

1. `docs/FORMAL_TRUTH.md`
2. `docs/EXPERIMENT_001.md`
3. `docs/ARCHITECTURE.md`

When evidence changes a major assumption, update `docs/FORMAL_TRUTH.md` in the same change.

## Non-negotiable rules

- Never fabricate buyer, supplier, contact, import, RFQ, pricing, MOQ, certification, or transaction data.
- `UNKNOWN` / missing is never equivalent to pass.
- Keep evidence provenance and timestamps wherever practical.
- Do not build prohibited scraping or bypass platform access controls.
- Prefer official APIs, feeds, exports, saved searches, licensed data, and public business information.
- Do not impersonate buyers or suppliers.
- No binding quotation or commercial commitment without supplier authorization.
- Never commit secrets, credentials, paid-database exports that cannot legally be stored, personal/private contact data, or sensitive credentials.
- Keep raw sensitive/paid data outside Git unless storage rights are explicit.

## Development approach

1. Define measurable experiment.
2. Collect real observations.
3. Store reproducible, non-sensitive evidence or references.
4. Analyze failure modes.
5. Only then automate the repeated bottleneck.

## Code principles

- Small modules, explicit schemas, deterministic validation where possible.
- AI classifications must expose evidence/input and be reviewable.
- Separate source ingestion from verification and scoring.
- Preserve original source identifiers/URLs when permitted.
- Tests should protect truth gates, deduplication, scoring boundaries, and lifecycle transitions.

## Opportunity lifecycle safety

A record cannot become `QUALIFIED` merely because an LLM says it looks good. Required deterministic gates (including contactability when applicable) must pass.

## Communication

Prefer written buyer outreach during initial validation. Telephone outreach is not required for the first experiments.
