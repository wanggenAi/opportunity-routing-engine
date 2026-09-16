# Missing Edge Gate

Status: `FIELD PROMOTION RULE / FAIL CLOSED`

A latent-value formation must not be selected for field validation merely because objective resources are underused, psychology/behavior is changing, and complementary nodes can be imagined.

The system must first answer:

1. **What exchange structures already exist for the same actor/outcome?**
2. **What material failure remains despite those structures?**
3. **Why has the market not already solved that failure cheaply enough?**

Canonical sequence:

`FORMATION HYPOTHESIS -> EXISTING EXCHANGE SEARCH -> STRUCTURAL FAILURE EVIDENCE -> MISSING EDGE -> WHY NOT ALREADY SOLVED -> CHEAPEST DECISIVE VALIDATION`

Boundaries:

- `COMPLEMENTARITY != MISSING EDGE`
- `MARKET SIZE != STRUCTURAL FAILURE`
- `COMPETITION != OPPORTUNITY`
- `EXISTING ROUTE != FAILED ROUTE`
- `DIFFERENT PACKAGING != NEW VALUE`
- `WHY NOT ALREADY SOLVED` must be evidence-bound, not a story invented after seeing a crowded market.

If an existing route adequately serves the same actor, outcome, geography, risk and economics, the candidate closes as `MARKET_ALREADY_CLOSED`.

If existing routes are visible but no material failure is observed, the state is `STRUCTURAL_FAILURE_EVIDENCE_REQUIRED`.

Only a candidate with an evidence-backed uncovered edge can become `VALIDATION_READY` under `src/missing_edge_gate.py`.

This gate sits between latent-value formation and field-route promotion. It does not replace downstream payer, permission, resource-control, acceptance, settlement or repeatability gates.
