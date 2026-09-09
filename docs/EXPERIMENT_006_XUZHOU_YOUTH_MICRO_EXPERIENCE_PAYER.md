# EXPERIMENT 006 — Xuzhou Youth Micro-Experience Payer Structure

Status: `SECONDARY / MULTI-SIDED ORCHESTRATION SANDBOX`

Date opened: 2026-09-10

Strategic kernel: `docs/RESOURCE_ORCHESTRATION_KERNEL.md`.

Canonical issue: GitHub Issue #5 was originally titled `EXP-005`; the repository already contained `EXPERIMENT_005_ASEAN_SME_AI_MICROFLOWS.md`, so the youth experiment remains **EXP-006**.

## Objective

Determine whether one small youth offline experience can form a viable multi-sided transaction and, if tested further, whether its execution capabilities can be **delegated rather than performed by the operator**.

Payer candidates:
1. participant;
2. venue / merchant;
3. blended participant + venue.

This remains a `PAYER_SHIFT + TIME_GAP + COORDINATION_GAP` test.

It is no longer the system's default first-priority experiment because the first strategic milestone is delegated orchestration (`EXP-008`), and this format has low ticket size plus several coordination functions.

## First format remains locked

> **10-person beginner coffee-flavor micro-experience + guided low-pressure interaction**

Do not silently switch format to manufacture success.

## Capability decomposition — NEW

If EXP-006 is executed, treat the event as a capability network:

```text
C1 merchant / venue BD
C2 venue + coffee capability
C3 participant recruitment
C4 booking / collection
C5 host / facilitation
C6 attendance / evidence
C7 settlement / feedback
```

The operator is **not** required to personally perform C1, C3 or C5.

Each recurring capability should define:
- input;
- required output;
- acceptance;
- payout;
- deadline;
- replacement rule.

Use `docs/templates/CAPABILITY_UNIT_TEMPLATE.md`.

## Example delegated transaction design

Possible structure, to be tested rather than assumed:

```text
Merchant-BD provider
  → payout for authorized venue commitment / qualified meeting

Participant recruiter
  → payout per valid deposit and/or attendance

Venue / barista
  → capability/resource contribution under explicit terms

Host
  → fixed accepted-event payout

Orchestrator
  → event transaction architecture, task interfaces, economics, acceptance and learning
```

A person's willingness to “help” is not a capability contract. Essential execution should have explicit incentives.

## Existing payer evidence

Local reporting remains useful:
- youth-night-school / youth-shop programs routed youth traffic into venues;
- one cafe reported about 30% revenue growth;
- later reporting described higher unit price/repeat in the space-reuse pattern;
- public/free youth activities remain a material substitute.

The strongest anchor `空山半闲咖啡` also received public/youth-program support, so it remains a mechanism case rather than independent payer proof.

Merchant controls remain required before generalizing venue willingness to pay.

## Participant payer test

Original test remains:
- exact price around `RMB49` for the locked format;
- same date / venue / offer;
- PASS only when >=6 qualified participants place real refundable deposits.

But participant acquisition should preferably be tested as a delegated capability rather than requiring the operator to stand in public places recruiting people personally.

Example capability unit:

```text
Input: exact event/date/venue/qualification rule
Output: qualified participant deposits
Payout: RMB X per valid deposit or accepted attendance
No payout: fake/friendly/unqualified booking
```

## Venue payer test

Original gate remains:
- >=1 qualified venue;
- authorized `RMB200+` cash / minimum-guaranteed economic commitment or equivalent guaranteed structure.

Merchant outreach may be delegated to a BD capability provider.

Example:

```text
Input: approved venue profile + exact event offer
Output: owner/authorized manager commitment under defined conditions
Payout: per qualified attended decision meeting and/or successful authorized commitment
```

Free space remains `RESOURCE / CAPABILITY` evidence, not venue-payer PASS.

## Strategic PASS

EXP-006 becomes strategically interesting if:
- one payer arm reaches real commitment;
- merchant/venue acquisition is delegated or routable;
- participant acquisition is delegated or routable;
- event delivery/hosting is delegated;
- event completes safely;
- settlement and payouts are recorded;
- operator shadow labor is recorded;
- normalized orchestration economics are at least plausibly sustainable.

A completed event that depends on the operator personally recruiting, selling and hosting may provide demand evidence but is weak evidence for the target system.

## Economic truth

Record:

```text
participant inflow
+ venue/sponsor inflow
- recruiter payout
- merchant-BD payout
- host payout
- venue/resource cost
- booking / refund / support costs
- other execution cost
= cash contribution margin

cash contribution margin
- operator shadow labor
= normalized orchestration margin
```

At this ticket size, coordination cost is a serious risk and must not be hidden.

## Stop / downgrade

Downgrade if:
- no payer commits;
- free/public alternatives solve the same outcome sufficiently;
- participant/venue acquisition cannot be delegated economically;
- recruiting/hosting/support payouts destroy margin;
- the operator must personally drive recurring execution;
- no repeat payer behavior appears.

## Relationship to EXP-008

EXP-006 may provide an `O2/L4` proof only if acquisition and delivery are materially delegated.

It is **not preferred for the first O2 proof** because low ticket size and multi-party coordination create harder normalized economics than bounded digital work.

## Existing execution materials

Historical/usable research remains:
- `docs/research/EXP_006_XUZHOU_PAYER_TARGETS_V1_2026-09-10.md`
- `docs/results/EXP_006_XUZHOU_FIELD_PACK_2026-09-10.md`
- `docs/results/EXP_006_FIELD_CARD_2026-09-10.md`
- `data/exp_006_field_log_template.csv`

Those files describe the prior direct field approach. Under the new kernel, they are inputs for **delegated BD/recruitment capability providers**, not instructions that the operator personally must do the work.

## Build rule

No community/app/event platform before repeat transactions and routable acquisition economics exist.

## Governing question

> **Can the event work as a priced network of capabilities, rather than because the operator personally sells, recruits and executes it?**
