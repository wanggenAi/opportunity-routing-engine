# Xuzhou Actor-First Opportunity Scan V2 — 2026-09-10

Status: `EVIDENCE-BACKED RESEARCH / FIELD VALIDATION REQUIRED`

This scan continues `XUZHOU_ACTOR_FIRST_SCAN_V1_2026-09-08.md`.

It does **not** treat every friction as a business. The purpose is to widen the actor surface, identify structurally different transaction gaps, record negative evidence, and then retain only the few candidates that deserve real-world commitment tests.

## 1. What changed from V1

V1 contained 12 candidate opportunities. V2 expands the working problem pool to **38 distinct friction records** across consumers, households, students, workers, merchants, institutions, asset owners and enterprises.

The scan now explicitly uses the canonical gap ontology in `docs/THESIS_TRANSACTION_GAPS.md`:

```text
DEMAND_GAP
CAPABILITY_GAP
PRICE_GAP
TRUST_GAP
INFORMATION_GAP
GEOGRAPHY_GAP
TIME_GAP
COORDINATION_GAP
PAYER_SHIFT
TECHNOLOGY_SHIFT
```

Important V2 corrections:

1. **Free/public provision is both demand evidence and competition.** It cannot be counted as direct private willingness to pay.
2. **Outcome-linked sponsors are a first-class payer hypothesis.** A venue that earns more from traffic or a training institution whose funding improves with employment outcomes may have stronger payer economics than the beneficiary.
3. **Trust penalties must actually be applied.** A high-trust idea cannot keep a high final score while home-access / vulnerable-person risk remains unresolved.
4. **A real paid incumbent proves payment but may destroy the opportunity.** Existing transaction volume is not enough if the orchestrator adds no distinct value.
5. **The unit of discovery is a friction + role map + transaction mechanism, not an industry label.**

## 2. Evidence legend

This memo uses a compact public-evidence label. It is not the field commitment scale.

- `STRONG` — actual price, purchase/service use, procurement, repeated paid category, outcome-linked budget, or costly repeated market behavior is observable.
- `MEDIUM` — repeated behavior / utilization / explicit economic incentive exists, but payment for the proposed transaction is not proven.
- `WEAK` — plausible structural signal with incomplete Xuzhou-specific payment behavior.

Field evidence must still use `docs/FIELD_VALIDATION_PLAYBOOK_XUZHOU.md` Level 0–5.

## 3. Friction pool — 38 records

### Cluster A — Youth experience, social connection and space utilization

| ID | Need actor / resource owner | Friction | Primary gap | Payment / behavior evidence | Payer hypothesis | Evidence | Disposition |
|---|---|---|---|---|---|---|---|
| XZF-001 | young worker / student | Wants low-pressure novelty / interest activity but public social events do not prove willingness to pay for a private recurring format | DEMAND_GAP | repeated youth-night-school / social participation; direct private event payment still unknown | participant | MEDIUM | PROMOTE only through deposit test |
| XZF-002 | cafe / youth shop | Needs qualified foot traffic during weaker periods | PAYER_SHIFT | a Xuzhou cafe reported ~30% revenue growth after youth-night-school activity | venue / merchant | STRONG on merchant benefit, payment unproven | PROMOTE sponsor test |
| XZF-003 | cafe / studio / small venue | Physical space is underused at some times even though fixed cost is already paid | TIME_GAP | local space-reuse case later reported ~20% higher customer unit price and ~15% higher repeat rate | venue + participant | STRONG on outcome | PROMOTE as part of EXP-006 |
| XZF-004 | maker / hobby instructor / student host | Can teach or host a narrow activity but lacks predictable paid group formation | CAPABILITY_GAP | night-school formats repeatedly route instructors/shops to groups | participant / venue | MEDIUM | INVESTIGATE inside event test, not standalone marketplace |
| XZF-005 | youth shop owner | Customer shortage / weak operating capability despite a viable physical product/service | COORDINATION_GAP | local youth-shop programs explicitly target customer shortage; event/space reuse has measurable revenue effects | merchant | MEDIUM-STRONG | Fold into EXP-006 / merchant acquisition, do not sell generic marketing |
| XZF-006 | young adult | Wants a quiet paid place to study or prepare for exams when home/library is unsuitable | DEMAND_GAP | Xuzhou has 20+ paid study rooms; observed prices include RMB 9.9/day, RMB 319/month and RMB 999/half-year; peak seats require advance booking | user | STRONG | Payment proven but incumbent strong |
| XZF-007 | paid study-room operator | Peak demand is strong but the market shows price competition / homogeneity | PRICE_GAP | local reporting explicitly notes price wars and differentiation attempts | user | STRONG market, weak orchestration value | WATCH; do not build seat directory |
| XZF-008 | new graduate / newly arrived youth | Needs short-term landing, housing and social integration | DEMAND_GAP | city is building youth talent communities and short-term stations | youth / government / employer | MEDIUM | Public provision is strong substitute |
| XZF-009 | youth housing seeker | Information about low-cost youth housing / policy is fragmented | INFORMATION_GAP | youth services increasingly integrated into official channels / talent code | user | MEDIUM | REJECT generic housing-info product; official infrastructure is stronger |
| XZF-010 | parent + child / young family | Wants low-cost cultural / maker experiences during holidays | DEMAND_GAP | city runs large sets of spring/holiday activities and discounts | parent / public sponsor | MEDIUM | WATCH; public supply can suppress private pay |

### Cluster B — Skills, graduates, flexible work and capability monetization

| ID | Need actor / resource owner | Friction | Primary gap | Payment / behavior evidence | Payer hypothesis | Evidence | Disposition |
|---|---|---|---|---|---|---|---|
| XZF-011 | 2026 graduate / unemployed youth | Has education or new skill but lacks first accepted paid proof / portfolio | CAPABILITY_GAP | Xuzhou received a first 15,800-person list of unemployed graduates / registered unemployed youth for targeted support | project buyer / training institution / employer | MEDIUM | PROMOTE narrowed outcome test |
| XZF-012 | skills-night-school learner | Training completion does not guarantee market-accepted output or income | CAPABILITY_GAP | 2026 training catalogue covers hundreds of skills and subsidized programs | buyer / sponsor | MEDIUM | Combine with XZF-011 |
| XZF-013 | training institution | Funding / future program competitiveness depends partly on learner employment outcomes | PAYER_SHIFT | Xuzhou policy: classes with >50% stable employment can receive up to 20% additional subsidy tilt | training institution / public program | STRONG economic incentive; proposed purchase unproven | PROMOTE payer discovery |
| XZF-014 | employer / merchant / OPC founder | Needs a small outcome but not necessarily another full-time employee | PRICE_GAP | firms already pay salaries for digital/content/data capability; local SME digitization and OPC activity are expanding | business / founder | MEDIUM | Continue EXP-003, demand format still unproven |
| XZF-015 | OPC / one-person founder | Has idea/domain ability but lacks one missing function for a bounded task | CAPABILITY_GAP | Xuzhou has multiple OPC communities, free workspaces and light-asset startup support | founder | MEDIUM-LOW payment evidence | FIELD PROBE; possible payer source for micro-projects |
| XZF-016 | flexible worker | Has fragmented available hours that conventional employment cannot fully monetize | TIME_GAP | city actively supports flexible employment and skill upgrading | task buyer | MEDIUM | Do not build generic gig platform |
| XZF-017 | job seeker | Needs vacancy matching / guidance | INFORMATION_GAP | government already offers free `1131` support including targeted job recommendations, guidance and training | government | STRONG substitute | REJECT generic job-matching entrant |
| XZF-018 | student / freelancer | Buyer distrusts unproven capability, deadline reliability and quality | TRUST_GAP | current project thesis requires portfolio, acceptance criteria and QA; direct Xuzhou transaction evidence still missing | project buyer | MEDIUM | Test only inside real bounded project |

### Cluster C — Pet and household trust markets

| ID | Need actor / resource owner | Friction | Primary gap | Payment / behavior evidence | Payer hypothesis | Evidence | Disposition |
|---|---|---|---|---|---|---|---|
| XZF-019 | pet owner leaving home | Needs feeding/walking during travel or work absence | DEMAND_GAP | paid home pet-feeding is an established service category; observed market pricing and holiday demand spikes exist | pet owner | STRONG category, local conversion unproven | Keep EXP-004 interviews |
| XZF-020 | pet owner | Does not trust a stranger with home access, keys, pet safety and private space | TRUST_GAP | service investigations document deposits, contracts, entry video, privacy and liability concerns | pet owner | STRONG friction | Valuable only if trust controls can be bounded |
| XZF-021 | pet owner / sitter | Holiday demand and provider availability are temporally mismatched | TIME_GAP | holiday demand can rise several-fold and schedules fill early in reported markets | pet owner | STRONG category, Xuzhou peak unknown | Investigate seasonality, not a standalone business |
| XZF-022 | pet-care provider | Travel between low-ticket visits can destroy provider economics | GEOGRAPHY_GAP | per-visit pricing is low relative to travel time; providers price by radius/distance | pet owner | STRONG mechanism | Critical stop condition for EXP-004 |
| XZF-023 | household buying cleaning/service | Already pays for service but worries about price and quality consistency | TRUST_GAP | Jiangsu survey: 22.7% report using household services; daily cleaning is the dominant use case | household | STRONG provincial payment | WATCH narrow standardized outputs only |
| XZF-024 | household / service worker | Small home tasks are difficult to scope and quality-check; support cost may exceed ticket | COORDINATION_GAP | household-service use is real but proposed microtask transaction has no direct evidence yet | household | WEAK-MEDIUM | Do not promote until a repeat task class is identified |

### Cluster D — Value migration, second-hand, repair, tourism and idle assets

| ID | Need actor / resource owner | Friction | Primary gap | Payment / behavior evidence | Payer hypothesis | Evidence | Disposition |
|---|---|---|---|---|---|---|---|
| XZF-025 | second-hand device buyer | Wants lower price but cannot verify hidden condition / repair history | TRUST_GAP | consumers already pay platform inspection/assurance services | buyer | STRONG payment, strong incumbent | WATCH / likely incumbent-dominated |
| XZF-026 | value-conscious household | Would prefer repair to replacement when economics are favorable | PRICE_GAP | value-for-money / trade-in / reuse migration is visible, but one local repeat repair wedge is not proven | user | MEDIUM | SIGNAL; require category-specific transaction evidence |
| XZF-027 | graduating student / mover | Must liquidate low-value items quickly before leaving | TIME_GAP | Xuzhou campuses run graduation flea / reuse activity | seller + buyer | MEDIUM | WATCH / seasonal / logistics margin risk |
| XZF-028 | visitor | Will pay for Hanfu / photography / local experience bundles | DEMAND_GAP | V1 documented paid local experience products; 2026 H1 Xuzhou tourism consumption reached RMB 34.331bn | tourist | STRONG demand, strong incumbents | WATCH; pure routing weak |
| XZF-029 | visitor arriving at peak time | Needs last-minute local plan / activity while capacity and information change quickly | TIME_GAP | tourism and night-economy traffic are high | tourist / merchant | MEDIUM | Pure information REJECT; only transaction-ready inventory could matter |
| XZF-030 | asset-owning organization | Has idle machines/equipment/raw materials that fail to sell promptly | CAPABILITY_GAP | one Xuzhou asset lot reached a third listing with a reduced floor price of RMB 90,870.06 | resource owner / buyer | STRONG friction | Important signal, but public-asset intermediation is regulated |
| XZF-031 | private idle-asset owner | Asset is hard to describe, inspect, lot, price and route to a relevant buyer | INFORMATION_GAP | repeated public listings demonstrate the mechanism; private-market economics not yet proven | seller / buyer | MEDIUM | FIELD PROBE only in lawful private transactions |
| XZF-032 | idle-asset buyer | Needs trustworthy condition evidence and pickup/logistics clarity before buying | TRUST_GAP | public listings explicitly sell assets as-is and require physical verification | buyer | MEDIUM-STRONG | Could be verification service, but liability must be bounded |
| XZF-033 | owner of idle building / room / commercial space | Fixed physical capacity is unused while youth/community uses need space | CAPABILITY_GAP | Xuzhou youth-talent-community plan explicitly encourages reuse of idle buildings / housing stock | institution / operator / user | MEDIUM | DORMANT for operator: capex / policy / asset rights heavy |

### Cluster E — Elderly, caregivers, parents and sponsored services

| ID | Need actor / resource owner | Friction | Primary gap | Payment / behavior evidence | Payer hypothesis | Evidence | Disposition |
|---|---|---|---|---|---|---|---|
| XZF-034 | elderly person | Needs home-based assistance | DEMAND_GAP | Xuzhou/Jiangsu public procurement proves government-paid home elder services | government / family / elder | STRONG payer category | Do not enter broad care directly; regulated/high-trust |
| XZF-035 | adult child | Wants visibility / coordination around an elderly parent's legitimate service providers | TRUST_GAP | care purchasing exists; separate payment for coordination layer not proven | adult child | MEDIUM-LOW | Narrow interview only; no vulnerable-person routing without safeguards |
| XZF-036 | dual-income / flexible-work parent | Holiday child supervision is difficult | DEMAND_GAP | recurring public programs explicitly address the problem | parent / institution | STRONG pain, weak private opportunity | REJECT direct childcare due safety + free substitute |

### Cluster F — SME / AI / cross-regional verticals

| ID | Need actor / resource owner | Friction | Primary gap | Payment / behavior evidence | Payer hypothesis | Evidence | Disposition |
|---|---|---|---|---|---|---|---|
| XZF-037 | SME / merchant | Repeated small digital/data/content tasks are too irregular for dedicated headcount | PRICE_GAP | related roles are paid through hiring; direct fixed-project purchase remains unproven | SME / merchant | MEDIUM | Continue VERTICAL EXP-003 |
| XZF-038 | SME / trader / remote actor | AI can lower the cost of extraction/research/document workflows, but payer may prefer existing staff/tools | TECHNOLOGY_SHIFT | policy/technology adoption supports investigation; direct payment for proposed microflow remains absent | SME / trader | MEDIUM-LOW | Keep ASEAN/AI work secondary until local payer evidence appears |

## 4. Cluster-level interpretation

### Cluster A — Youth + merchant space is stronger than V1 assumed
The key evidence is no longer only that young people attend activities. Local cases show a measurable **merchant-side economic outcome** from reusing space as experience/social infrastructure.

This makes the payer question testable:

```text
participant wants experience
        ↓
venue has idle/off-peak capacity
        ↓
activity creates qualified traffic
        ↓
participant pays, venue pays, or both
```

The strongest unresolved variable is not demand existence; it is **payer structure and repeat economics**.

### Cluster B — Capability-to-income now has a credible sponsor hypothesis
The previous XZA-001 thesis had a broad and unstable payer.

V2 identifies a more specific third-party incentive:
- learners want income / proof;
- training institutions are evaluated partly by stable-employment outcomes;
- classes above the policy employment threshold may receive additional subsidy support;
- project buyers still need real outputs.

This does not prove training institutions will buy project orchestration, but it creates a falsifiable `PAYER_SHIFT` path that did not exist in V1.

### Cluster C — Pet care remains a good trust laboratory, but not automatically the #1 commercial opportunity
Payment exists and trust friction is real. However, `docs/OPPORTUNITY_SCORECARD.md` explicitly applies a `-20` penalty for unresolved home-access / physical-safety trust risk.

Therefore the previous V1 final score of 79 with no penalty is not canonical while home-entry risk is still unresolved.

EXP-004 remains useful because its purpose is to discover whether a trust layer can remove that penalty economically. It should not be treated as already having done so.

### Cluster D — Idle assets reveal a real transaction failure mechanism
Repeated listing / repricing is unusually useful evidence because it shows an actor taking costly commercial action and failing to complete a transaction quickly.

But public-asset disposal is not an invitation to become an auction intermediary. The lawful opportunity, if any, would need to be found in a private low-regulation version such as:
- buyer-ready asset description;
- condition evidence;
- lot decomposition;
- buyer-category research;
- pickup/logistics readiness.

This remains a field probe, not a promoted business.

### Cluster E — sponsored payer evidence is real, but safety dominates
Elder and child categories clearly demonstrate `BENEFICIARY != PAYER`. They also show why payer clarity alone is not enough. Vulnerability, licensing, safeguarding and public substitutes can dominate the economics.

### Cluster F — enterprise opportunities remain valid but do not dominate
The scan contains only two explicitly SME/AI vertical friction records out of 38. They remain in the portfolio because payment capacity and bounded delivery can be strong, not because the system begins from enterprise budgets.

## 5. Negative controls / explicit rejections

The following should **not** be promoted in current form:

1. generic Xuzhou job-matching platform — government/public infrastructure is extensive and free;
2. generic youth-housing information service — official youth/talent channels increasingly integrate this information and subsidy;
3. generic paid-study-room directory — payment is real but discovery is not the scarce layer;
4. direct childcare marketplace — safety/licensing burden + strong public/free provision;
5. broad eldercare marketplace — vulnerable-person, professional and safety boundaries are too large;
6. pure local tourism content/guide directory — mature discovery/OTA channels already dominate;
7. pure second-hand listing marketplace — strong incumbents and low distinct orchestrator value;
8. broad idle-public-asset brokerage — regulated transaction structure and bypass risk;
9. generic freelancer marketplace — existing labor/gig channels plus bypass risk;
10. broad AI SaaS before a paid repeated microflow exists.

## 6. Current candidate set that deserves deeper scorecard comparison

Only four candidates survive strongly enough for immediate targeted validation:

### C1 — Youth micro-experience payer shift
`XZF-001 + XZF-002 + XZF-003 + XZF-005`

Question:
> For one exact event, will participants deposit, will a venue commit money for qualified traffic, or will a blended structure win?

Canonical experiment: `EXP-006`.

### C2 — Skills-to-income with outcome-linked sponsor
`XZF-011 + XZF-012 + XZF-013 + XZF-018`

Question:
> Will a training institution, project buyer or other outcome-aligned payer commit money to convert trained capability into a bounded accepted project / portfolio outcome?

### C3 — Xuzhou bounded SME micro-project
`XZF-014 + XZF-037`

Question:
> Will a business pay for a fixed accepted result instead of using internal staff / full-time hiring / direct freelancer access?

Canonical experiment: `EXP-003`.

### C4 — Trusted pet-care transaction layer
`XZF-019 + XZF-020 + XZF-021 + XZF-022`

Question:
> Can verification, scope, evidence and exception controls reduce home-access / pet-care risk enough that owner payment covers provider + coordination economics?

Canonical experiment: `EXP-004`.

## 7. Source map

### Youth / experience / merchant space
- S01 Xuzhou night school + youth shop; revenue +30%, 12 linked sites / ~600 attendances: https://www.zgjssw.gov.cn/yaowen/202604/t20260427_8570297.shtml
- S02 Xuzhou commercial-space reuse; customer unit price +20%, repeat rate +15%: https://news.jschina.com.cn/yw/202606/t20260625_s6a3d2258e4b0baeb0111da45.shtml
- S03 Xuzhou youth shops / startup customer shortage: https://news.jschina.com.cn/yw/202601/t20260115_s6968a108e4b05fbb22fe038f.shtml
- S04 Xuzhou paid study rooms, prices and peak booking: https://szb.cnxz.com.cn/xzrb/pad/con/202605/12/content_49840.html
- S05 Xuzhou Youth Card / integrated youth services: https://szb.cnxz.com.cn/xzrb/pad/con/202606/19/content_51558.html

### Skills / employment / OPC
- S06 2026 unemployed-graduate survey, first list 15,800 and `1131` public service: https://szb.cnxz.com.cn/xzrb/pad/con/202607/26/content_53290.html
- S07 2026 Xuzhou subsidized skill catalogue; >50% stable employment gives training institutions up to 20% extra support: https://szb.cnxz.com.cn/dscb/pc/con/202606/30/content_52078.html
- S08 Provincial training rule and outcome-linked support detail: https://jshrss.jiangsu.gov.cn/art/2025/5/13/art_77276_11563528.html
- S09 Xuzhou OPC entry guide / 12 communities: https://szb.cnxz.com.cn/xzrb/pad/con/202608/13/content_54294.html
- S10 Xuzhou OPC support / free workspace and startup support: https://szb.cnxz.com.cn/xzrb/pad/con/202603/27/content_47724.html

### Pet / household
- S11 Paid home pet-feeding: prices, deposits, holiday capacity, privacy/liability risk: https://www.jsjc.gov.cn/yaowen/202602/t20260227_1311217.shtml
- S12 2026 Jiangsu consumption survey including pet / household-service use: https://www.stats.gov.cn/zs/tjwh/tjkw/tjqk/zgxxb/202601/P020260107311898189224.pdf

### Assets / housing / tourism
- S13 Xuzhou idle raw-material/machine/equipment lot, third listing, RMB 90,870.06 floor: https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260309/43e2d63b-3284-442c-b89f-7458d7083c06.html
- S14 Xuzhou July idle electric carts / AC / audio asset disposal: https://jsggzy.jszwfw.gov.cn/jyxx/003006/003006001/20260731/3b2231fb-ac45-4019-bbd4-9ff455c7c236.html
- S15 Xuzhou youth-talent-community plan including reuse of idle buildings / housing stock: https://js.people.com.cn/n2/2026/0821/c360302-41673461.html
- S16 Xuzhou H1 tourism: 36.2981m visits, RMB 34.331bn tourism consumption: https://zgjssw.jschina.com.cn/shixianchuanzhen/xuzhou/202608/t20260823_8589840.shtml
- S17 Xuzhou graduation flea-market / reuse signal: https://www.szcu.edu.cn/2026/0622/c187a91053/page.htm

### Family / elder / child
- S18 Xuzhou home elder-service procurement evidence retained from V1: https://ggzy.zwb.xz.gov.cn/jyxx/003004/003004006/20250212/1c005786-b6e3-4902-960d-399202443b60.html
- S19 Xuzhou holiday childcare signal retained from V1: https://jsnews.jschina.com.cn/xz/a/202608/t20260815_s6a7fdcace4b0eb7bb0f9ee47.shtml

## 8. Research decision

The V2 scan does **not** authorize a platform build.

It authorizes four targeted validation tracks only:

```text
1. EXP-006 youth micro-experience payer commitment
2. skills-to-income sponsor/payer discovery
3. EXP-003 bounded SME micro-project paid validation
4. EXP-004 pet trust-gate interviews / trust resolution
```

The next result memo must score these under the canonical 100-point scorecard and apply penalties consistently.
