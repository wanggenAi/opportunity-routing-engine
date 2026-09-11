# Resource Underuse Sensor 001 — Xuzhou Public Assets

Date: `2026-09-11`

Status: `LIVE SOURCE VERIFIED / UNDERUSE EVIDENCE PARTIAL`

## Question

Can official public property-rights listings provide machine-readable evidence for the **surplus/resource side** of the Resource Imbalance Engine without confusing resource existence, underuse and transaction friction?

## Live pipeline result

GitHub Actions run:

`https://github.com/wanggenAi/opportunity-routing-engine/actions/runs/34550874710`

Current Xuzhou property-rights list sample:

```text
discovered: 12
parsed: 12
errors: 0
explicit underuse: 0
relistings: 3
```

Interpretation:

- the current list/detail path is machine-readable;
- all 12 public listings establish `resource_state=DISCOVERED` only;
- 3 listings contain explicit second/third/repeated-listing evidence, so allocation friction is observable;
- none of the 12 current-detail texts met the strict explicit `闲置/空置` parser gate;
- therefore this live sample contains **zero `underuse=OBSERVED` resource signals**;
- the system correctly preserves that zero instead of promoting relisting into underuse.

## Why `relisting != underuse`

A second/third listing can prove that an offered resource failed to clear under previous conditions.

It may indicate:
- PRICE_GAP;
- INFORMATION_GAP;
- poor packaging/granularity;
- weak demand access;
- timing/geography mismatch;
- restrictive transaction conditions;
- or another blocker.

But without additional evidence it does not prove that the asset was operationally idle before or during the listing period.

Therefore V1 records:

```text
public listing       → DISCOVERED resource
explicit 闲置/空置  → OBSERVED underuse
relisting            → observed allocation friction only
```

## Official corroboration outside the current top-page sample

The Jiangsu public-resource platform statically mirrors Xuzhou-origin property-rights notices and demonstrates that stronger underuse evidence really exists in this source family.

### A. Large vacant factory space

Official mirror:

`https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260820/a61e3535-95f2-4711-bfac-7ce438d7ce89.html`

Observed facts in the official notice:
- project: 江苏徐州睢宁县沙集物流园一期4#厂房招租项目;
- lease area: `10515.20㎡`;
- status: `空置`;
- rent floor: `893792.00元/年`;
- owner: 江苏宁通投资发展集团有限公司.

This is valid evidence of a **discovered + observed-underuse physical-space resource**. It is not yet evidence that the Opportunity Routing Engine has optioned the property or has a profitable reuse route.

### B. Small vacant office space

Official mirror:

`https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260819/0c110ff9-10dc-46c1-9b44-bfedfcc3a9f6.html`

Observed facts:
- 睢宁县维景大厦 B座10F（B1008）部分房产;
- lease area: `17.80㎡`;
- status: `空置`;
- rent floor: `4628.00元/年`.

This demonstrates that the source can expose resource granularity from very small to very large spaces.

### C. Idle machinery + failed allocation / repricing

First listing official mirror:

`https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260204/8b2cbee7-32e8-40b4-9001-f8bd47d5c6db.html`

Third listing official mirror:

`https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260309/43e2d63b-3284-442c-b89f-7458d7083c06.html`

Observed facts:
- same batch of raw materials, machinery and electronic equipment;
- notice explicitly states assets are `处于闲置状态`;
- first listing floor: `112185.25元`;
- third listing floor: `90870.06元`;
- third-listing floor is approximately `19.0%` below the first-listing floor.

This is substantially stronger than a generic second-hand listing because it combines:

```text
RESOURCE EXISTS
+
EXPLICIT UNDERUSE
+
REPEATED FAILURE TO CLEAR
+
OBSERVED PRICE ADJUSTMENT
```

Even this combination is **not yet a business opportunity**. The system still needs a compatible need/payer and a defensible blocker/route.

## Current engineering decision

Keep the Xuzhou local listing adapter as a daily live sensor.

Do not require every daily sample to contain explicit underuse. A source-health workflow should remain green when the source is healthy but the current sample legitimately contains no qualifying resource.

Next source-side improvement:
1. retain current Xuzhou local discovery;
2. add a bounded official Jiangsu-mirror/Xuzhou-origin history path so explicit vacant/idle resource evidence can be collected across a longer window;
3. transform only caller-classified assets into `ResourceSignal` records;
4. never infer CapabilityUnit identity from free-form titles;
5. keep relisting/friction evidence separate from underuse state;
6. only then compare against paid NeedSignals.

## Commercial truth

> `闲置资产存在` 不是项目；`重复挂牌` 也不是项目。真正有价值的是：某种真实需求正在付钱，同时某种兼容资源明确闲置，而且我们能证明阻塞点并用更低交易成本建立新的交换路径。
