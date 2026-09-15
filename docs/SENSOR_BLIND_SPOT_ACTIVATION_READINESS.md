# Sensor Blind-Spot Activation Readiness

This layer converts current evidence-channel blind spots into an auditable source-activation queue without pretending that public visibility or an official developer portal grants automation permission.

The chain is:

`latest evidence-channel coverage -> blind channels -> registered/candidate source assessment -> producer-trial readiness`

It is deliberately downstream of `sensor-evidence-channel-coverage-021`. Only channels that remain blind in the latest production artifact are assessed.

## Readiness meanings

- `PRODUCER_TRIAL_READY`: registry/candidate evidence explicitly supports automation and no current blocker remains. This still does **not** make the source production-live.
- `PERMISSION_VALIDATION_REQUIRED`: an official authorized/API surface exists, but current scope, permission, review, or zero-incremental-fee conditions are not yet proven. It may be researched/validated, but not collected as a production producer.
- `MANUAL_ONLY_BLOCKED`: current access is manual/login-bound and therefore does not count as an automated path.
- `DISABLED`: the registered path is disabled/retired.
- `DISCOVERY_OR_QUALIFICATION_BLOCKED`: a dynamic candidate still lacks qualification and/or activation evidence.
- `NO_SAFE_AUTOMATED_PATH_CURRENTLY_PROVEN`: no source in that blind channel currently qualifies for a producer trial.

## Current expected production truth

After QuestMobile moved `REPRESENTATIVE_RESEARCH` into observed production, two blind channels remain:

- `SEARCH_INTENT`
- `SOCIAL_PUBLIC_DISCOURSE`

The current registry should yield **zero producer-trial-ready sources**.

`BAIDU_INDEX` remains manual/login-bound, and the registry explicitly forbids reverse-engineered endpoints.

For social evidence, public Weibo/Xiaohongshu/Douyin/Zhihu surfaces remain manual/terms-dependent. The Reddit/X/Instagram/Telegram dynamic candidates remain unqualified because China relevance, unique signal value and collection mode are not established.

`DOUYIN_OPENAPI` is intentionally different: it is an official OAuth/OpenAPI surface and therefore may be a **permission-validation candidate**, but it is not producer-ready. The current registry still requires review, proof of authorized scope and proof that the intended scope has zero incremental usage fee.

## Truth boundaries

- Public access is not automation permission.
- An official API surface is not granted API scope.
- Manual visibility is not a production sensor.
- Terms review required is not permission granted.
- Candidate discovery is not producer readiness.
- Global-source relevance to China must be evidenced before it can be China-primary evidence.
- An unproven zero-incremental-fee condition is not free-to-run permission.
- Reverse-engineered endpoints remain forbidden where the registry says so.
- Paid data / paid credits are not silently introduced.
- Producer-trial readiness is not source activation or production coverage.
- `UNKNOWN != PASS`.
