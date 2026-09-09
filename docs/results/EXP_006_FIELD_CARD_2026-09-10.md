# EXP-006 One-Page Field Card — 2026-09-10

Status: `USE IN FIELD`

## Today resolves only one UNKNOWN

> **Will a real venue commit money for qualified youth traffic around one exact coffee micro-experience?**

Do not discuss apps, platforms, communities or grand business models.

## First route

1. `空山半闲咖啡` — anchor; verify current storefront near the 1818 / Gulou central-commercial area.
2. Control venue #1 — current independent/youth-facing cafe in the same cluster.
3. Control venue #2 — another merchant with a different traffic source / operating structure.
4. Optional: `云玺中心 / 青年发展型街区` operator-level payer comparator.

Do not interview only publicly supported youth-night-school success cases.

## 30-second opening

> 老板您好，不好意思占用您30秒。我不是来卖平台，也不是让您现在办活动。我在徐州做一个很小的商业验证：想确认像咖啡店这种空间，在固定空档时段，如果有人能组织8到10个符合目标客群的年轻新客过来，店里到底愿不愿意为这批有效客流付一点组织成本。您觉得这个事情有没有必要，您来判断。我只问几个真实经营问题。

If the person cannot decide money:

> 这类活动或者获客费用一般是谁能决定？我想直接问能做预算判断的人，避免占用您时间。

## Ask recent behavior first

1. `你们最近四周固定最空的是哪几个时段？`
2. `最近一次为了拉新客真实花钱是什么？平台、达人、折扣还是活动？大概多少钱？`
3. `以前办活动以后，现场消费或者复购有没有实际变化？`
4. `8到10个符合你目标客群的第一次到店用户，对你大概值多少钱？`

## The commercial ask

> 如果我在你们固定的空档时段组织8到10个符合目标客群的年轻新客，做一场60到90分钟、10人以内的咖啡风味体验；**达到约定到场人数以后，你们支付200元组织费**，这个条件您现在能不能接受？

If `NO`, ask exactly:

> 200元不成立，主要是这批客不值200、你们从来不为获客付费、还是需要我先证明消费/复购？

Do not negotiate immediately. First discover the mechanism.

## Classification — choose exactly one

### `VENUE_LEVEL3_PASS`
Authorized decision-maker accepts >=RMB200 monetary commitment, including explicit contingent commitment.

Example:
`满8个合格到场用户，活动完成后付200元。`

### `RESOURCE_ONLY`
Venue offers space / drinks / discount / staff but no monetary commitment.

Useful evidence, **not payer PASS**.

### `PAYER_FAIL`
Authorized decision-maker rejects monetary contribution even after scope / condition is clear.

Record exact reason.

### `REACH_FAIL`
No authorized payer decision-maker reached.

This is an acquisition/access failure, not a market rejection.

## Minimum records before changing direction

Anchor + at least 2 merchant controls.

Do not declare venue-payer success from `空山半闲` alone because that venue has received official youth-program / traffic support.

## If venue payer passes

Lock:
- exact venue;
- exact weak time window;
- exact date;
- exact 200 RMB payment condition;
- coffee/barista capability;
- refund/cancellation boundary.

Then test participants:

> `49元，10人以内，60–90分钟，入门咖啡风味体验+轻互动，满6人成行；现在是否愿意付可退订金占位？`

Participant PASS = >=6 qualified people actually pay deposits for the same event.

## If venue payer does not pass

Do not immediately kill EXP-006.

Finish the required venue sample / controls, then test whether:
- participant direct-pay survives; or
- venue only contributes resource; or
- both sides refuse economic commitment.

## Stop conditions

Stop field interviewing and update GitHub when:
- venue Level 3 PASS occurs; or
- participant Level 3 PASS occurs; or
- sample reaches defined FAIL threshold; or
- a hard legal/safety/transaction issue appears.

## Record immediately

Use `data/exp_006_field_log_template.csv`.

Minimum fields after every conversation:

```text
target:
decision_maker_reached:
weak_time_window:
recent_acquisition_spend:
RMB200_response:
commitment_amount:
commitment_condition:
refusal_reason:
classification:
next_action:
```

**Friendly interest is not the milestone. The milestone is economic commitment.**
