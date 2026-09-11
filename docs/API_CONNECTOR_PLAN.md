# API Connector Plan

## Purpose

The discovery engine needs two broad families of machine inputs:

1. **Macro / money / resource evidence** — official statistics, procurement, transactions, employment, prices, assets.
2. **Behavior / psychology evidence** — search interest, public content, trend velocity, topic salience, interaction patterns, local-life signals.

Behavior/social/search evidence never promotes a commercial opportunity by itself. It must be corroborated by behavior and money/resource evidence.

## Zero-paid-data MVP policy — LOCKED

During the current MVP, a connector may enter production only when its intended use has **zero incremental data/API usage fee**.

- do not buy API credits, subscriptions or data packages;
- do not activate a connector merely because credentials exist;
- do not replace a paid/open-API limitation with undocumented browser/XHR endpoints;
- paid sources may remain documented for future review, but their state is `DISABLED_PAID_MVP`;
- if pricing or scope cost is unclear, state is `FREE_ONLY_REVIEW_REQUIRED`, not ACTIVE.

This policy is about the current MVP cost boundary, not a claim that paid data is never valuable.

## Authorization / transport classes

### PUBLIC_API_HTTPS
Anonymous official HTTPS endpoint. Example: the current National Bureau of Statistics JSON endpoints. This is the preferred machine source.

### PUBLIC_API_HTTP_OFFICIAL
An official HTTPS documentation/catalog page explicitly publishes an API endpoint that is still plain HTTP. This is allowed only as a **source-specific exact host/path exception**. It must not weaken the repository-wide HTTPS client.

Rules:
- exact documented host/path only;
- redirect may remain on the same host/path and move to HTTPS;
- provenance must record the final URL and body hash;
- if the final transport remains HTTP, evidence is marked `PLAINTEXT_HTTP` and `corroboration_required=true`;
- plain-HTTP evidence cannot by itself promote a money-flow conclusion.

Current example: MOFCOM public open-data JSON endpoint.

### OFFICIAL_AUTHORIZED_API
An official developer application receives `client_key`, `client_secret`, OAuth/access tokens or equivalent. Acceptable only when the exact intended scopes are authorized **and zero incremental usage fee is verified for MVP**.

Secrets live only in server-side secret stores such as GitHub Actions Secrets. Never commit or log them.

### OFFICIAL_CONNECTOR
Provider-supported CLI/agent connector. It is still subject to the zero-paid-data policy. Being official does not make a paid connector eligible for MVP.

### LOGIN_MANUAL_NO_OPEN_API
The product can be used after login but the provider exposes no suitable open API. Authorized/manual free research may be used; reverse-engineered internal browser endpoints are not production connectors.

### PRIVATE_INTERNAL
Undocumented browser/XHR endpoints, session cookies, signed internal APIs or anti-bot flows that are not an authorized developer contract. These are not production connectors.

## Connector states

- `ACTIVE_LIVE` — bounded live probe succeeded and the source is eligible under the free-only policy.
- `UNCONFIGURED_AUTH` — otherwise-eligible official connector/API lacks credentials/session.
- `PERMISSION_REQUIRED` — credentials exist but desired scope still requires approval.
- `AUTHENTICATED_NOT_PROBED` — auth prerequisites exist but no bounded live probe has succeeded.
- `FREE_ONLY_REVIEW_REQUIRED` — official access may exist, but zero incremental usage fee for our exact scope is not yet proven.
- `DISABLED_PAID_MVP` — intended use requires paid plan/credits and is disabled for current MVP.
- `NO_OPEN_API` — provider exposes no open API for this product.
- `MANUAL_AUTHORIZED_ONLY` — authenticated/manual research only; not automated as API.
- `ERROR` — a previously eligible/configured connector failed its bounded probe.

`credential_present != ACTIVE_LIVE`, `HTTP 200 != valid data`, and `missing != zero`.

## Current connectors

### National Bureau of Statistics

Public HTTPS JSON source. Already live. It remains the reference pattern for higher-trust anonymous structured data.

### MOFCOM public open-data platform

The public-service open-data catalog exposes fully open datasets and documents JSON API paths. For the initial social-financing dataset, the currently published request path uses `http://opendata.mofcom.gov.cn/front/data/jsonData?...` even though the dataset-detail page is HTTPS.

Therefore:
- use a dedicated exact-endpoint client;
- never enable generic HTTP in `JsonHttpClient`;
- preserve raw payload/hash;
- mark final HTTP transport lower-trust and require independent corroboration before money-flow promotion;
- dataset-specific field semantics/freshness are validated separately after live payload inspection.

### Douyin OpenAPI

Official developer API, but current state is `FREE_ONLY_REVIEW_REQUIRED`. Even if `DOUYIN_CLIENT_KEY` and `DOUYIN_CLIENT_SECRET` exist, the connector does not advance until the exact scopes used by the tracker are verified to have zero incremental usage fee.

### Weibo CLI

Official Agent-oriented connector, but the intended production use requires a paid plan/credits. It is therefore `DISABLED_PAID_MVP`. Existing local login does not change this state and no plan should be purchased for current MVP.

### Baidu Index

Official help currently exposes no suitable open API. Use only authorized/manual free views. Do not substitute reverse-engineered browser calls.

### QuestMobile / public social platforms

Use only free public reports/views permitted by the provider. Paid databases, credits and private APIs are outside the current MVP.

## Security and truth rules

1. Secret values never enter source, CSV, docs, issues, artifacts or ordinary logs.
2. Code may record credential names/presence only, never values.
3. OAuth access/refresh tokens are secrets.
4. API transport success does not prove freshness or business meaning.
5. API error/status=0 never becomes a numeric zero observation.
6. Social/search signal is not a population-share estimate.
7. Paid/unverified-cost connectors do not silently activate.
8. A platform login does not authorize extraction beyond its documented/contracted interfaces.
9. Plain HTTP official evidence is explicitly lower-trust and must be corroborated.

## Psychology Tracker usage

Eligible behavioral connectors should emit aggregate signals such as topic/concept, geography, legitimate audience slice, salience, momentum, interaction intensity, observation period and provenance. The tracker is for aggregate psychology/behavior shifts, not personal psychographic profiling.
