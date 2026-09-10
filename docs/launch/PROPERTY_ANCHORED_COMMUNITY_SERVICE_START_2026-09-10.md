# START — Property-Anchored Community Living-Service Orchestration Backend

Date: 2026-09-10
Status: `#1 CYCLE-001 TARGETED VALIDATION`

This is not a property company, home-service company, cleaning company or marketplace app.

Working Chinese name:

> **物业锚定的社区生活服务后台编排**

## 1. Exact system role

```text
RESIDENT / HOUSEHOLD DEMAND
        ↓
PROPERTY / COMMUNITY FRONT DOOR
        ↓
ORCHESTRATION BACKEND
(task definition / provider routing / SLA / acceptance / replacement / settlement)
        ↓
OPTIONED SERVICE PROVIDERS
        ↓
ACCEPTED HOUSEHOLD OUTCOME
        ↓
PAYMENT + SPLIT + PERFORMANCE DATA
        ↺
```

Operator does not perform cleaning/repair and is not required to sell door-to-door to residents.

## 2. Why property is the first demand pump

Current public evidence:
- Xuzhou has 2,237 residential communities;
- 690+ property-service enterprises;
- property firms are actively extending resident convenience/value-added services;
- property fee pressure creates incentive to improve resident satisfaction and develop additional service revenue;
- national cases show property channels can generate repair/renovation/service demand repeatedly.

The market is not proven for this exact backend. The first test exists to resolve G1/G5/G6.

## 3. The hook must exist before property outreach

Do not approach property empty-handed with `I have a platform idea`.

First create an `OPTIONED SUPPLY PACK`.

Target only 2–3 provider categories and obtain conditional commitments. No employment, inventory or guaranteed volume.

### Initial safe categories

A. `HOME_DEEP_CLEANING`
- bounded room/area scope;
- before/after evidence;
- excluded hazardous/specialist work.

B. `APPLIANCE_CLEANING`
- e.g. air-conditioner / washing-machine / range-hood cleaning by competent provider;
- no gas-system modification or unsafe electrical repair.

C. `MOVE_IN_OUT_CLEANING`
- empty/turnover home cleaning;
- fixed scope and acceptance checklist.

Do not start with:
- gas;
- high-voltage/electrical safety work;
- structural repair;
- medical/elder-care personal care;
- childcare;
- home key custody;
- pet home entry;
- anything requiring a regulated qualification unless a qualified provider and correct structure are in place.

## 4. Provider option request

Ask providers for a conditional commitment, not free labor.

Required terms to explore:

```text
service category:
pilot price / pricing rule:
coverage area:
response SLA:
provider identity/business proof:
what is included/excluded:
completion evidence:
rework/complaint rule:
payout event:
capacity per week:
no-volume-guarantee accepted: YES/NO
```

Preferred structure:

> If a qualified order is assigned and the provider accepts it, provider delivers to the agreed checklist; payment is settled after accepted completion. No provider salary, no inventory and no guaranteed order volume before demand proof.

This creates a real `OPTIONED CAPABILITY` without purchasing it upfront.

## 5. Property hook

Only after at least two real provider options exist, approach property.

Do NOT say:
- `我想做一个社区平台`;
- `我这里有一些阿姨/工人`;
- `你帮我发个广告`;
- `我想进小区卖东西`.

Say the economic proposition:

> **我们不是向物业收系统费，也不是让物业自己招人。我已经把几类低风险家庭服务的执行资源、价格边界、服务时效和售后规则先锁成条件方案。物业如果愿意做一个小范围试点，居民有真实订单才产生费用；物业前台只负责把入口给居民，后台的服务商筛选、派单、验收、投诉和替换由我们组织。先跑真实订单，再讨论是否值得长期做。**

The hook is:

```text
PROPERTY UPFRONT COST = 0
+ NO NEW STAFF
+ OPTIONED PROVIDER CAPACITY EXISTS
+ BOUNDED SERVICE MENU
+ ONE BACKEND RESPONSIBILITY POINT
+ PAY ONLY WHEN REAL SERVICE OCCURS
```

If no provider options exist, this hook is not yet real.

## 6. Monetization hypotheses — do not lock prematurely

Test transparent structures:

A. resident price contains orchestration margin;
B. provider pays per accepted order / channel acquisition share;
C. property receives an agreed share or service credit from completed orders;
D. recurring backend operations fee only after transaction volume proves value.

Do not invent hidden markups. Exact split must be explicit and economically sustainable.

## 7. Orchestration value test

The model dies if the property can introduce one provider and then bypass the backend with little loss.

Therefore first pilot must test whether backend value is real:
- provider qualification;
- multiple-provider backup;
- fixed service scope;
- response SLA;
- before/after evidence;
- customer acceptance;
- complaint/rework;
- replacement if provider fails;
- consolidated performance history;
- settlement.

If these functions are not valued, G5 fails.

## 8. First transaction template

Example only; do not invent local prices before provider quotes.

```text
resident selects exact service
→ property/front-door sends standardized order
→ backend checks scope
→ provider accepts
→ provider performs service
→ evidence/checklist returned
→ resident/authorized accepter confirms
→ settlement released
→ provider/property/orchestrator shares recorded
→ satisfaction/failure data recorded
```

No software is required. Use a simple form/spreadsheet/WeChat for Cycle 001.

## 9. First validation sequence

### Phase A — Option supply
Target: 5 qualified local providers across 2–3 categories.

PASS:
- >=3 providers accept conditional/order-based cooperation;
- >=2 categories have at least one backup route;
- prices/SLA/acceptance can be written clearly.

FAIL:
- providers require fixed salary/minimum volume upfront;
- quality cannot be standardized enough;
- no economic room after expected acquisition/QA/rework.

### Phase B — Property demand pump
Target: 5 property decision-makers / project managers, not random residents.

Ask:
1. Which resident requests are repeatedly outside the basic property contract?
2. What services do residents repeatedly ask the front desk to recommend?
3. Which ones does property currently refer informally?
4. Has property tried paid/value-added service? What failed?
5. What complaint/liability makes property hesitant?
6. If supplier/SLA/after-sales are externally managed and property pays zero upfront, will it authorize a small pilot?
7. Who is allowed to approve resident communication / service entry / revenue share?

PASS:
- >=3/5 name repeated real resident service requests;
- >=2/5 describe an existing workaround/referral/provider;
- >=1 authorizes a bounded pilot to real residents under exact terms.

### Phase C — Real orders
A property `yes` is not payment proof.

First commercial threshold:
- >=5 real paid resident orders inside one property/community pilot period;
- >=2 service categories OR repeated orders in one category;
- delivery performed by external providers;
- at least one backend acceptance/QA/replacement function actually used;
- economics recorded after all payouts and rework reserve.

### Phase D — Regenerative loop
G6 begins to pass only if:
- same property/community sends new orders without reacquiring the channel;
- recurring task categories become predictable;
- provider performance data improves routing;
- preferably a second provider can replace the first without breaking service.

## 10. Capital rule

Before paid-order proof:

```text
NO office
NO employee payroll
NO inventory
NO marketplace/app build
NO paid mass advertising
NO property system integration
NO fixed supplier retainer
```

Allowed:
- transport/phone/basic print or simple form cost;
- explicitly bounded learning cost;
- success/accepted-order payout.

## 11. Operator-independence rule

The operator may make the first few architecture conversations to learn, but routine roles must be routable:

```text
provider sourcing → CapabilityUnit
property BD → CapabilityUnit
order intake → CapabilityUnit / simple automation
service delivery → provider
QA/evidence → CapabilityUnit
complaint handling → CapabilityUnit
settlement → process/automation
```

Long-run operator role:
- choose service categories;
- design economics;
- approve standards/routes;
- analyze performance;
- resolve exceptions;
- expand demand pumps.

## 12. Stop rules

Kill or redesign if any of these survive a qualified test:
- properties do not receive repeated service requests;
- property will not authorize a channel under zero-upfront terms;
- residents simply use incumbent apps/providers with no unresolved friction;
- provider + complaint/rework + property share leaves no orchestration margin;
- property/provider bypass makes backend unnecessary;
- home-entry trust cost is too high;
- service quality cannot be made verifiable/repeatable.

## 13. Why this is not `a home-service platform`

The experiment is testing a reusable mechanism:

> **Can one trusted local demand pump continuously emit bounded needs into a backend that routes replaceable external capabilities and creates enough governance value to be paid?**

If it works, the same orchestration architecture can later apply to other property/community services or entirely different demand pumps.
