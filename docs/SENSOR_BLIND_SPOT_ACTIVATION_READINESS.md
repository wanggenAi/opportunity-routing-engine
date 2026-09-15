# Sensor Blind-Spot Activation Readiness

This layer converts current evidence-channel blind spots into an auditable source-activation queue without pretending that public visibility or an official developer portal grants automation permission.

The chain is:

`latest evidence-channel coverage -> blind channels -> registered/candidate source assessment -> official permission evidence -> producer-trial readiness`

It is deliberately downstream of both `sensor-evidence-channel-coverage-021` and source-specific permission probes. Only channels that remain blind in the latest production artifact are assessed.

## Readiness meanings

- `PRODUCER_TRIAL_READY`: registry/candidate evidence explicitly supports automation and no current blocker remains. This still does **not** make the source production-live.
- `PERMISSION_VALIDATION_REQUIRED`: an official authorized/API surface exists, but current public evidence has not yet narrowed the blocker far enough.
- `EXTERNAL_APPROVAL_REQUIRED`: current official public documentation proves the relevant scope and application path, but account/application approval and effective scope quota/cost are external facts that are still missing. This is not producer-ready.
- `MANUAL_ONLY_BLOCKED`: current access is manual/login-bound and therefore does not count as an automated path.
- `DISABLED`: the registered path is disabled/retired.
- `DISCOVERY_OR_QUALIFICATION_BLOCKED`: a dynamic candidate still lacks qualification and/or activation evidence.
- `NO_SAFE_AUTOMATED_PATH_CURRENTLY_PROVEN`: no source in that blind channel currently qualifies for a producer trial.

## Current production truth

After QuestMobile moved `REPRESENTATIVE_RESEARCH` into observed production, two blind channels remain:

- `SEARCH_INTENT`
- `SOCIAL_PUBLIC_DISCOURSE`

`BAIDU_INDEX` remains manual/login-bound, and the registry explicitly forbids reverse-engineered endpoints.

For social evidence, public Weibo/Xiaohongshu/Douyin/Zhihu surfaces remain manual/terms-dependent. The Reddit/X/Instagram/Telegram dynamic candidates remain unqualified because China relevance, unique signal value and collection mode are not established.

`DOUYIN_OPENAPI` is different. The live official-document probe proves that `video.search` can provide keyword-video/comment discovery, but it also proves that the scope is a special permission, default-off and applied for in the management center. Public documentation does not establish that this repository/user's application has been approved, does not publish the effective free quota for `video.search`, and does not prove that the intended collection cadence fits within zero incremental cost.

The expected readiness result is therefore:

- producer-trial-ready sources: **0**;
- `DOUYIN_OPENAPI`: `EXTERNAL_APPROVAL_REQUIRED`;
- overall conclusion: `BLOCKED_ON_EXTERNAL_APPROVAL_AND_EFFECTIVE_QUOTA_EVIDENCE`.

The only evidence that can advance this source is:

1. `VIDEO_SEARCH_APPLICATION_APPROVED_FOR_THIS_APP`;
2. `VIDEO_SEARCH_EFFECTIVE_FREE_QUOTA_FOR_THIS_APP_SCOPE`;
3. `INTENDED_COLLECTION_CADENCE_FITS_ZERO_INCREMENTAL_FEE`.

The durable artifact records the exact evidence-channel coverage run and Douyin permission-probe run it consumed.

## Truth boundaries

- Public access is not automation permission.
- An official API surface is not granted API scope.
- Official public documentation is not account/application approval.
- Manual visibility is not a production sensor.
- Terms review required is not permission granted.
- Candidate discovery is not producer readiness.
- Global-source relevance to China must be evidenced before it can be China-primary evidence.
- An unproven zero-incremental-fee condition is not free-to-run permission.
- Reverse-engineered endpoints remain forbidden where the registry says so.
- Paid data / paid credits are not silently introduced.
- External approval required is not producer-ready.
- Producer-trial readiness is not source activation or production coverage.
- `UNKNOWN != PASS`.
