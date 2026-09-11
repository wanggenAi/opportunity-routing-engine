# API Connector Plan

## Purpose

The discovery engine needs two broad families of machine inputs:

1. **Macro / money / resource evidence** — official statistics, procurement, transactions, employment, prices, assets.
2. **Behavior / psychology evidence** — search interest, public content, trend velocity, topic salience, interaction patterns, local-life signals.

The second family is useful for the Consumer Psychology & Behavior Tracker, but it never promotes a commercial opportunity by itself.  Social/search evidence must still be corroborated by behavior and money-flow evidence.

## Authorization classes

### PUBLIC_API
Anonymous official endpoint. Example: current National Bureau of Statistics JSON endpoints.

### OFFICIAL_AUTHORIZED_API
A developer account/application receives official credentials such as `client_key`, `client_secret`, `access_token`, or OAuth grants.  This is acceptable for production automation when the requested scope is approved.

Secrets must be stored server-side.  For GitHub Actions, use repository/environment Secrets.  Never commit credentials or paste their values into logs/artifacts.

### OFFICIAL_CONNECTOR
The platform supplies a supported command-line/agent connector rather than requiring us to reproduce HTTP auth.  Weibo CLI is currently handled this way.  Binary installation alone is not proof of auth; `whoami`/equivalent must pass before a connector becomes `ACTIVE_LIVE`.

### LOGIN_MANUAL_NO_OPEN_API
The product can be used after login but the provider does not expose an open API.  Baidu Index currently belongs here according to its official help.  Do not replace this with reverse-engineered internal browser endpoints.

### PRIVATE_INTERNAL
Undocumented browser/XHR endpoints, session cookies, signed internal APIs or anti-bot flows that are not an authorized developer contract.  These are **not** production connectors merely because a logged-in browser can call them.

## Connector states

- `ACTIVE_LIVE` — authenticated/authorized and a bounded live probe has succeeded.
- `UNCONFIGURED_AUTH` — official connector/API exists but credentials/session have not been configured.
- `PERMISSION_REQUIRED` — credentials exist but the desired API scope still requires approval.
- `AUTHENTICATED_NOT_PROBED` — credential prerequisites exist, but no successful bounded probe has yet proven access.
- `NO_OPEN_API` — provider explicitly exposes no open API for this product.
- `MANUAL_AUTHORIZED_ONLY` — authenticated manual/browser research may be used under provider terms but not automated as API.
- `ERROR` — a previously configured connector failed its bounded probe.

`UNCONFIGURED_AUTH != ERROR` and `AUTHENTICATED_NOT_PROBED != ACTIVE_LIVE`.

## Current connectors

### Douyin OpenAPI

Official docs require an approved developer application with `ClientKey` and `ClientSecret`.  OAuth can produce user `access_token`; a `client_token` is available for approved APIs that do not require user authorization.  Individual scopes may still require separate platform approval.

Repository secret contract:

- `DOUYIN_CLIENT_KEY`
- `DOUYIN_CLIENT_SECRET`

The presence of these secrets only advances the connector to `AUTHENTICATED_NOT_PROBED`.  A real API probe and scope check are required before `ACTIVE_LIVE`.

### Weibo CLI

Weibo currently exposes an official Agent-oriented CLI with search, hot trends, statistics and structured output.  We prefer the official connector over inventing private REST endpoints.  Authentication is performed through the CLI's supported auth flow; successful `weibo auth whoami` (or equivalent official check) is required before live use.

### Baidu Index

Official Baidu Index help currently states that it does **not** provide an open API.  Therefore the source remains login/manual (or separately contracted/authorized data service if Baidu explicitly grants one).  Internal browser calls are not treated as an API contract.

## Security rules

1. Secret values never enter source files, CSV, docs, issue comments, artifacts or normal logs.
2. Code may record only credential **names/presence**, never values.
3. OAuth refresh/access tokens are treated as secrets.
4. Connector artifacts store only sanitized status and evidence metadata.
5. Scope denial is kept as `PERMISSION_REQUIRED`, never converted into zero demand or missing behavior.
6. A platform login does not authorize automated extraction beyond the platform's documented/contracted interfaces.

## Psychology Tracker usage

Authorized behavioral connectors should emit normalized aggregate signals such as:

- topic / keyword / concept
- geography
- audience slice when legitimately available
- signal salience
- momentum / change rate
- interaction intensity
- observation period
- provenance

They must **not** become a personal-profile database.  The tracker is designed for aggregate psychology/behavior shifts, not identification of individual users.
