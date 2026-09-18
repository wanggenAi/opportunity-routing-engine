# Opportunity Mobilization Scan 006 — Minimum-service-unit kill sweep

Date: 2026-09-18

## Why this scan exists

Scan 005 retained one new watch:

`OMS-006-AI-BUILT-APP-PRODUCTION-READINESS-MICROREVIEW`

but correctly refused to promote it because China payer truth and self-propulsion are still unproven.

This scan does **not** narrow that story again.

Instead it opens five adjacent/highly tempting minimum-service-unit patterns and tries to kill them with incumbent evidence before they consume founder attention.

The rule is simple:

```text
BILATERAL_PULL
+
SMALL TASK UNIT
+
ABUNDANT SUPPLY

does not matter if:

ROUTING + TRUST + ACCEPTANCE + SETTLEMENT
already exist at low friction.
```

---

# 1. Elastic warehouse micro-capacity

## Reality pattern

Demand side:

- merchants and shippers can need temporary overflow space;
- seasonal peaks make long fixed leases inefficient;
- short, flexible storage is economically attractive.

Supply side:

- warehouse operators want higher utilization;
- unused space is perishable capacity.

This looks like a perfect routing problem.

## Counterevidence

It is already substantially routed.

The 全国数智化云仓企业公共服务平台 explicitly:

- aggregates warehouse and fulfillment providers;
- exposes available capacity;
- allows shippers to post requirements;
- matches requirements to warehouse resources;
- frames idle-capacity utilization as a core provider benefit.

Current Xuzhou-facing warehouse providers also explicitly advertise flexible rental and seasonal space adjustment.

## Verdict

`OMS-007-ELASTIC-WAREHOUSE-MICROCAPACITY`

# CLOSED_GENERIC_ROUTE

The generic bridge already exists.

Do not build:

> "Airbnb for warehouse space"

or another cloud-warehouse matching layer.

Only reopen for a **named cargo class in Xuzhou/Jiangsu** that current flexible warehouse/cloud-warehouse providers explicitly refuse, where that refusal creates a measurable cost.

Sources:

- https://www.yuncang.org.cn/
- https://www.yuncang.org.cn/page/index/ids/1.html
- https://www.csjcs.com/news/shangxun/qiye/YmVpamluZy1qaHljenpranl4Z3MxNzg2NTgzNTM3

---

# 2. PLC / industrial-equipment diagnosis and repair microtasks

## Reality pattern

Demand pull is obvious:

```text
machine fails
→ line slows/stops
→ factory wants diagnosis now
```

Supply hunger is also real:

- independent engineers want work;
- service teams want utilization;
- OEMs need wider coverage.

The attractive minimum service unit is:

> one fault diagnosis, one remote session, or one on-site repair order.

## Counterevidence

Again, the generic control plane already exists.

云维保 already provides:

- service-order publishing;
- engineer matching;
- engineer quoting;
- dispatch;
- standardized service records;
- repair-history persistence.

工业速派 explicitly integrates nationwide service stations and professional engineers.

驼驮维保 already markets nationwide repair matching, engineer supply, bidding and tracked service orders.

## Verdict

`OMS-008-INDUSTRIAL-REPAIR-MICROTASK`

# CLOSED_GENERIC_ROUTE

Do not create another:

- industrial repair marketplace;
- PLC expert marketplace;
- engineer dispatch app;
- generic remote-diagnosis matching layer.

Only reopen if a **specific named failure class** repeatedly cannot be routed by existing networks because of a concrete interface, credential, acceptance or time-to-value constraint.

Sources:

- https://www.yweibao.cn/
- https://m.gongkongbpo.com/download/download
- https://www.tuotuo.com.cn/activity-weibao_index.html

---

# 3. Independent used construction-machinery inspection

This one is especially tempting in Xuzhou because the local machinery ecosystem makes both sides reachable.

## Reality pattern

Demand actor:

> buyer who does not trust a remote used machine enough to pay before seeing independent evidence.

Supply actor:

> machinery inspector / experienced equipment expert.

Smallest task:

> inspect one machine and return identity + condition evidence.

The buyer-side pain is real:

- wrong machine;
- hidden damage;
- false condition;
- travel cost;
- export buyer cannot inspect personally.

## Counterevidence

铁甲二手机 already opens paid inspection to the industry and publishes:

- online inspection from RMB 300;
- expert/broker network;
- Chinese/English reports;
- equipment inspection and evaluation.

Mevas sells per-machine independent used-equipment inspection in China.

SGS provides remote industrial inspection with expert participation, recorded video and photo evidence.

## Verdict

`OMS-009-USED-HEAVY-EQUIPMENT-INDEPENDENT-INSPECTION`

# CLOSED_GENERIC_ROUTE

The exact transaction unit already exists.

Do not build:

> "local expert verifies the machine for a remote buyer"

as a generic platform thesis.

Only reopen for a named subtype or transaction stage that current inspectors explicitly do not cover and where a buyer still pays a measurable travel/fraud/delay cost.

Sources:

- https://www.tiebaobei.com/introduction.html
- https://mevas.net/used-machinery-inspections-in-china-mandarin-text
- https://www.sgsgroup.com.cn/zh-cn/services/sgs-qiiq-remote-industrial-inspections

---

# 4. Local photo / fact / address verification microtasks

This pattern is almost a textbook Rooter control plane:

```text
REMOTE ENTERPRISE
↓
one local fact needed
↓
task schema
↓
nearby person
↓
photo / location / timestamp / checklist
↓
QA
↓
settlement
```

Demand and supply both move.

But this is not whitespace.

## Counterevidence

有活 publishes a bank-risk-control case in which enterprise-address verification was converted into:

- a network of 1,200 local verifiers;
- coverage across 300 cities;
- standardized task release;
- on-site photo/check-in;
- verification reports.

The same case says the earlier process cost more than RMB 500 per household and averaged five days.

拍拍赚 already operates a national crowd-verification/data-audit network.

Other consumer crowd apps already pay workers for geofenced photo and information-collection tasks.

## Verdict

`OMS-010-FIELD-EVIDENCE-MICROTASK`

# CLOSED_GENERIC_ROUTE

The control plane itself is already real and deployed.

Do not build another generic:

- local-photo marketplace;
- field-data marketplace;
- "someone near the location checks it for you" platform.

Only reopen for a **specialized evidence packet** that generic crowds cannot reliably execute and where a named payer still uses an expensive workaround.

Sources:

- https://www.goldentec.com/yh
- https://lenztechretail.com/Cn/Index/pageView/catid/6.html

---

# 5. Independent acceptance/testing for small outsourced software

This looks structurally attractive for 根哥 because it is digital, standardizable and delegable.

The possible small unit is:

> one bounded acceptance/test pass before final payment.

Demand pull exists because software buyers already use staged payment and acceptance.

Supply is abundant because thousands of QA engineers and developers already take remote work.

But operator fit is not market evidence.

## Counterevidence

猪八戒 already exposes small fixed-price testing transactions.

程序员客栈 already provides:

- thousands of test freelancers;
- project milestones;
- fee escrow;
- staged acceptance;
- developer settlement only after acceptance.

Formal third-party software labs already sell independent acceptance testing where legal/official authority matters.

So the market already spans:

```text
cheap freelance testing
↕
platform escrow / staged acceptance
↕
formal third-party acceptance testing
```

## Verdict

`OMS-011-SMALL-SOFTWARE-ACCEPTANCE-REVIEW`

# CLOSED_GENERIC_ROUTE / SENSOR_ONLY

Do not rescue it by saying:

> "but what about off-platform buyers?"

without real payer evidence.

That would be story-preservation.

Only reopen if one named off-platform buyer recently suffered measurable rework/dispute cost **because all three existing routes were unusable for one bounded acceptance decision**.

Sources:

- https://www.zbj.com/fuwu/ceshifuwuw/
- https://www.proginn.com/b/outsource
- https://www.proginn.com/cat/ceshi
- https://www.cepingshe.com/yanshou/

---

# Portfolio delta

No new P0 candidate is promoted.

Closed in this scan:

1. generic elastic warehouse-capacity routing;
2. generic industrial repair / PLC microtask routing;
3. generic used heavy-equipment inspection;
4. generic local field-evidence crowdsourcing;
5. generic small-software acceptance/testing routing.

Existing watch:

`OMS-006-AI-BUILT-APP-PRODUCTION-READINESS-MICROREVIEW`

remains:

`RETAIN_WATCH / NOT_P0`

No human probe is justified by this scan.

`FIRST_EXTERNAL_VALUE_FLOW = NOT_PROVEN`

# CURRENT BEST NEXT TRUTH

Continue looking for a residual where:

```text
both sides are already moving
+
the task can be standardized
+
resources are callable
+
the incumbent route does NOT already bundle:
routing
trust
acceptance
settlement
```

Do not spend 根哥's time on the five generic routes closed here.
