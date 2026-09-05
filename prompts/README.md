# Prompts

Versioned prompts used for research, extraction, verification, scoring, matching, and outreach drafting belong here.

## Rules

- Prompts are production logic and must be versioned.
- Keep extraction prompts separate from judgment prompts.
- Require structured outputs for machine-consumed prompts.
- Require `UNKNOWN` when evidence is insufficient.
- Never instruct a model to infer private contact information or invent missing commercial facts.
- Store evaluation examples before changing a prompt that affects qualification/scoring.

## Planned prompt families

- `extract_opportunity_*`
- `verify_buyer_*`
- `classify_contactability_*`
- `score_opportunity_*`
- `match_supplier_*`
- `draft_outreach_*`
- `classify_reply_*`

No production prompt has been approved yet.
