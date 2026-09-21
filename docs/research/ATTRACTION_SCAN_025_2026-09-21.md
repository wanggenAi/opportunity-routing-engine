# ATTRACTION_SCAN_025 — platform-owned consumer-flow micro-edge falsification

Date: 2026-09-21  
Epoch: `ATTRACTION_FIELD_V1`  
Status: COMPLETE  
Commercial promotions: **0**  
Retained research formations: **0**  
First external value flow: **NOT_PROVEN**

## Search rule

Scan 025 continued the high-energy micro-edge method after Scan 024, but explicitly excluded AI gateways,
quota plans, used-device recycling, 9610 returns and recent policy/compliance verticals.

The scan tested current consumer flows where people are actively spending, complaining, switching or paying
for reduced uncertainty:

- instant retail;
- e-commerce aftersales;
- home repair;
- pet medical services;
- collectibles / anime goods;
- shared bicycles.

The result is intentionally **zero retention**.

## Main finding

The repeated pattern is:

```text
HIGH USER PAIN
+ MACHINE-READABLE ORDER STATE
!=
UNOWNED THIRD-PARTY CONTROL EDGE

WHEN THE PLATFORM OWNS:
ORDER + BILLING + REFUND + INVENTORY + FULFILLMENT
THE THIRD PARTY OFTEN OWNS ONLY ADVICE
```

That is not enough for this project.

## 1. Instant retail stockout / aftersales — platform owns the executable loop

JD's current instant-retail APIs expose store/SKU stock state, stockout state, order adjustment, order
tracking and aftersales/refund workflows. Douyin's open platform similarly exposes instant-retail order and
aftersales APIs.

Sources:
- https://opendj.jd.com/staticnew/widgets/api/MQStoreSkuStockVendibility.html
- https://opendj.jd.com/api/getApiDetail/200/10812f9fc7ee4564b552f19270a7e92e.htm
- https://opendj.jd.com/staticnew/widgets/doc/waimai.html
- https://op.jinritemai.com/docs/api/84/7277

A third party can build merchant software around these APIs, but the platform still owns the customer order,
refund and adjustment rights. That is a software-feature surface, not an unowned transaction-control layer.

Verdict: **demoted**.

## 2. Home repair price/diagnosis guard — platform protection + human diagnosis

JD already offers paid out-of-warranty diagnosis/repair, service-order progress, fee references and
overcharge compensation. When the exact repair is not in the published table, the final diagnosis and quote
still depend on the on-site engineer, model, fault, parts and installation conditions.

Sources:
- https://help.jd.com/user/issue/321-4508.html
- https://help.jd.com/user/issue/938-4284.html
- https://help.jd.com/user/issue/942-4005.html

The remaining high-value uncertainty is therefore not a clean machine state. A third party would either
duplicate platform protection or reintroduce recurring expert diagnosis.

Verdict: **demoted**.

## 3. Pet clinic price/trust choice — exact proprietary-data incumbent

Pet medical spending is high and price opacity is real, but the strongest decision edge is already occupied.

Ant Insurance's "真选医院" uses more than **5 million pet-insurance claims** and 28 dimensions to evaluate
hospitals, including treatment experience, capability and cost. It publishes hospital treatment-cost
information and updates the evaluation dynamically.

Source:
- https://m.thepaper.cn/newsDetail_forward_33583801

RuiPai and Tmall are also moving standardized pet services online with transparent pricing, booking and
offline fulfillment:
- https://finance.sina.com.cn/tech/roll/2026-08-19/doc-ininukpm9826078.shtml

The winning asset here is proprietary claims/clinical transaction data, not a public-web comparison layer.
The medical result remains professional human delivery.

Verdict: **demoted**.

## 4. Collectibles / anime goods — platform internalizes authentication, custody and price data

The pain is real: authenticity, non-delivery, logistics and resale-price uncertainty create strong user
motion. But Xianyu's current "鱼鲤购" already combines:

- platform authentication;
- official warehouse fulfillment;
- full-process video evidence;
- seller pricing;
- historical transaction data.

Sources:
- https://finance.sina.com.cn/tob/2026-01-12/doc-inhfzcnv8501423.shtml
- https://www.donews.com/news/detail/4/6486735.html

A thin third party cannot recreate the most valuable parts—physical custody, authentication rights,
warehouse evidence and transaction data—without becoming another marketplace/fulfillment operator.

Verdict: **demoted**.

## 5. Shared-bike overcharge — real leakage, platform-owned billing rights

Black Cat's August 2026 data reported more than 7,000 shared-bike/e-bike complaints, with overcharging making
up roughly three quarters.

Source:
- https://finance.sina.com.cn/heimao/2026-09-14/doc-inirupew9524253.shtml

This is a high-frequency leak, but generally low-value per incident. The operator controls geofence, ride
record, billing and refund state. Without operator cooperation, a third-party layer can only organize evidence
or draft a complaint.

That output is generic-agent substitutable and has weak value capture.

Verdict: **demoted**.

## 6. Generic e-commerce refund/evidence assistant — no action right

Black Cat's 2026 618 report recorded 189,096 complaints across major e-commerce platforms, prominently
including poor customer service, rejected refund requests and fake shipping.

Source:
- https://finance.sina.com.cn/heimao/2026-06-29/doc-inifacma7030733.shtml

But major platforms already expose structured return/refund state machines and merchant/ISV APIs. For example,
Taobao documents unified return/refund APIs and automatic timing rules.

Source:
- https://developer.alibaba.com/docs/doc.htm?articleId=102594&docType=1

The consumer-side third party cannot adjudicate or move platform funds. If it only summarizes evidence or
writes complaints, it again collapses into generic AI assistance.

Verdict: **demoted**.

## Why zero retention is the correct outcome

No tested formation survived all of these floors simultaneously:

- meaningful current voluntary energy;
- an unowned control edge;
- machine-resolvable state;
- executable action rights;
- no recurring expert/human delivery;
- non-generic operator asset;
- plausible independent economics.

The consumer flows are hot. The control loops are not free.

## Next search boundary

Scan 026 should move away from dominant consumer transaction platforms and test **active business spending /
operational loss flows where no single marketplace owns the full action loop**.

This is not a return to "B2B = opportunity" or "routing = opportunity." The question is narrower:

```text
IS MONEY / OPERATIONAL LOSS ALREADY MOVING?
IS THE DECISIVE STATE MACHINE-READABLE?
IS THE ACTION LOOP OUTSIDE ONE DOMINANT TRANSACTION PLATFORM?
IS THERE A REUSABLE CONTROL ASSET WITHOUT RECURRING HUMAN DELIVERY?
```

Scan 026 must not inherit the specific Scan 025 verticals.
