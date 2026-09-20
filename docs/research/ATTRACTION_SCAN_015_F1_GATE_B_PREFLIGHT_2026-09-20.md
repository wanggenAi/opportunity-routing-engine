# ATTRACTION_SCAN_015-F1 — Gate B Inbound Discovery Preflight

Date: 2026-09-20  
Formation: `ATTRACTION_SCAN_015-F1 — USED-DEVICE REALIZED-PAYOUT_ROUTER`  
Status: `PREPARED_NOT_PUBLISHED / GATE_B_NOT_RUN`

## Purpose

Gate B asks whether high-intent used-device sellers can **self-reveal** through a
scalable Agent/Skill discovery surface without recurring founder acquisition.

This is not a traffic experiment yet. It is a fail-closed preflight.

The experiment must distinguish:

```text
SKILL / MCP DISCOVERY INFRASTRUCTURE EXISTS
!=
USED-DEVICE SELLER INTENT NATURALLY FLOWS THROUGH THAT SURFACE
```

and:

```text
FOUNDER DISTRIBUTED LINK CLICK
!=
SELF-REVEALING INBOUND INTENT
```

## Current discovery surfaces

### 1. Qianwen AI Platform Skills Hub

Current official documentation says:
- the Skill market is an open Skill-sharing community;
- all users can browse and install Skills;
- all users can publish after the required account/identity workflow;
- Skills can be searched by keyword and category;
- published Skills can be attached to supported Agent clients.

Sources:
- https://platform.qianwenai.com/docs/agent-infra/skills/custom
- https://platform.qianwenai.com/docs/agent-infra/skills/publish
- https://www.qianwenai.com/hub/skills/qianwen-find-skills

Truth:

`PUBLIC_SKILL_DISCOVERY_INFRASTRUCTURE = PASS`.

Boundary:

The dominant install/use surface is Agent clients such as Qoder / Claude Code and
other Skill-capable clients. This proves discoverability of a capability to Agent
users, not that ordinary used-device sellers naturally arrive with sell/recycle
intent.

`USED_DEVICE_SELLER_INTENT_ON_SKILLS_HUB = NOT_PROVEN`.

### 2. Qianwen App / third-party Agent surface

Current public evidence shows:
- Qianwen App has an Agent plaza and life-service functionality;
- Qianwen announced opening third-party Agent/Skill participation to enterprises;
- official brands are already being integrated into the consumer-facing App.

Sources:
- https://apps.apple.com/cn/app/id6466733523
- https://www.thepaper.cn/newsDetail_forward_33299006
- https://www.stcn.com/article/detail/3941333.html

Truth:

`CONSUMER_AGENT_SURFACE = CURRENTLY_REAL`.

Boundary:

Current public evidence does not prove:
- open self-service publishing for this formation;
- ranking/search placement for a small independent operator;
- organic invocation volume for used-device recycling intent;
- whether enterprise qualification or commercial review would be required for this
  specific service.

`FOUNDER_FREE_CONSUMER_INBOUND = NOT_PROVEN`.

### 3. OneKey MCP / Qianwen MCP store

Current official documentation proves:
- MCP providers can publish OneKey MCP services into Agent platforms;
- MCP market services are visible to platform users;
- services can be mounted into Agents and called automatically;
- OneKey MCP provider publication requires provider onboarding and can be invite-only
  in the current commercial path.

Sources:
- https://help.aliyun.com/zh/marketplace/released-the-bailian-mcp-service-product/
- https://platform.qianwenai.com/docs/agent-infra/mcp/official-services
- https://platform.qianwenai.com/docs/agent-infra/mcp/external-invocation

Truth:

`MCP_CALLABILITY_AND_MARKET_DISCOVERY = PASS`.

Boundary:

This is primarily a developer / Agent-builder distribution surface. It does not by
itself prove end-user seller intent.

`MCP_MARKETPLACE != A_SIDE_SELLER_FLOW`.

## Gate-B preflight verdict

```text
DISCOVERY_INFRASTRUCTURE              = PASS
PUBLIC_SKILL_PUBLICATION_PATH         = PASS
CONSUMER_AGENT_SURFACE                = PASS_CURRENT_PUBLIC_EVIDENCE
USED_DEVICE_SELLER_INTENT_FLOW        = NOT_PROVEN
FOUNDER_FREE_ORGANIC_INVOCATION       = NOT_PROVEN
TRANSACTION_EXECUTION                 = BLOCKED_BY_GATE_A
PERSONAL_DATA_COLLECTION              = DISALLOWED
GATE_B                                = NOT_RUN
```

This is a **negative correction** to any earlier assumption that Skill/MCP existence
already proves inbound demand.

## Minimal experiment unit

A publishable experiment, only after the release gate is satisfied, must be a narrow
capability with the promise:

> Compare expected final realized payout, not just the prettiest displayed estimate.

The first version must **not**:
- fetch unauthorized live prices;
- rank real recycling rails using fabricated data;
- create recycling orders;
- collect name, phone, exact address, payment account, IMEI or serial number;
- claim that cross-platform outcome history already exists;
- advertise guaranteed highest payout.

It may only:
- recognize sell/recycle intent;
- collect non-identifying device attributes;
- explain estimate-vs-realized-payout risk;
- state when live routing is unavailable;
- record anonymous experiment telemetry if the host platform and user consent permit.

## Non-identifying input envelope

Allowed:
- device category;
- model/configuration bucket;
- storage bucket;
- coarse condition flags;
- coarse region if needed;
- desired time-to-cash;
- whether the user prioritizes expected payout, speed or downside certainty.

Disallowed:
- name;
- mobile;
- exact address;
- payment account;
- IMEI;
- serial number;
- identity document;
- raw order credentials.

## Measurement design

The only positive Gate-B evidence is **self-revealing high-intent discovery**.

Count separately:

1. `organic_market_search_install` — user found the capability through platform
   search/recommendation without founder-provided direct link;
2. `organic_agent_invocation` — user invoked through Agent routing/search without
   founder solicitation;
3. `qualified_sell_intent` — user expresses a current intent to sell/recycle a real
   device;
4. `routing_value_request` — user explicitly asks which route is likely to deliver a
   better actual final outcome, not merely a generic recycling explanation.

Do not count as demand proof:
- founder tests;
- friends/family;
- direct links sent by the founder;
- paid ads;
- cold DMs;
- developer-only installs with no sell intent;
- GitHub stars/views;
- generic curiosity;
- synthetic prompts.

## Promotion / kill rule

Gate B cannot pass from raw traffic.

Required evidence shape:

```text
PLATFORM-NATIVE DISCOVERY
→ UNSOLICITED QUALIFIED SELL INTENT
→ USER ASKS FOR ROUTING VALUE
→ REPEATS WITHOUT FOUNDER DISTRIBUTION
```

If publication is available but qualified intent only appears after manual promotion:

`GATE_B_FAIL_RECURRING_ACQUISITION`.

If Agent users install the Skill but do not bring real current sell/recycle intent:

`GATE_B_FAIL_WRONG_DISTRIBUTION_SURFACE`.

If qualified seller intent appears organically but Gate A rights remain unproven:

`DEMAND_SIGNAL_ONLY / NO TRANSACTION EXECUTION`.

## Release gate

This preflight package may exist on GitHub now.

Public publication of the experiment remains blocked until:
1. Gate A has sufficient written rights clarity for the intended public promise; or
2. the published artifact is explicitly limited to non-transactional education and
   cannot imply live cross-rail routing.

Real order execution remains blocked until Gate A passes.

## Current conclusion

The infrastructure is no longer the central unknown.

The central Gate-B unknown is:

> **Will a real used-device seller naturally ask an Agent ecosystem for
> expected-final-payout routing, without the founder first manufacturing that traffic?**

Until measured:

`GATE_B = NOT_RUN`.
