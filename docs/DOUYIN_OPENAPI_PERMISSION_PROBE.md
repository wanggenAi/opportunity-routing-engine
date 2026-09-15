# Douyin OpenAPI Permission Probe

This producer verifies whether the registered `DOUYIN_OPENAPI` path can legitimately advance from permission validation into an automated `SOCIAL_PUBLIC_DISCOURSE` producer trial.

It does **not** call any Douyin API, use a ClientKey/ClientSecret, request user authorization, buy quota, or scrape consumer-facing Douyin pages. It reads only public official documentation from `https://open.douyin.com`.

## Official evidence contract

The probe binds three official public documentation pages:

1. Permission overview: proves `video.search` is the keyword-video-management scope, can obtain keyword-matched Douyin videos and comments, is a **special permission**, is **default off**, and requires a **management-center application**.
2. Free-quota FAQ: proves the platform has daily free quota and documents an example (`video.list=1000/day`), but does not establish the public free-quota amount for the exact `video.search` scope.
3. Payment FAQ: proves paid incremental traffic packages exist on top of free quota.

Every page retains source URL, fetch timestamp, payload SHA-256, normalized official text, an exact evidence excerpt and excerpt SHA-256.

## Current expected decision

The official docs prove that `video.search` has useful signal fit for `SOCIAL_PUBLIC_DISCOURSE`, but they do **not** prove that our application has the special permission or that the intended scope satisfies the project's zero-incremental-fee requirement.

Therefore:

- `producer_trial_allowed = false`
- application approval remains `NOT_ESTABLISHED`
- exact `video.search` free-quota amount remains `NOT_ESTABLISHED_FROM_PUBLIC_DOCS`
- zero incremental fee remains `NOT_ESTABLISHED`

The next legitimate step is application/scope validation in the official management center, not API calls with guessed credentials and not reverse engineering.

## Truth boundaries

- Official scope exists != our application has that scope.
- Default-off permission != permission granted.
- Platform free quota exists != target-scope quota is proven.
- Free quota != permanent zero incremental cost.
- Paid extension availability != permission to buy it.
- Keyword-video/comment discovery != market demand or paid need.
- Permission evidence != source activation.
- `UNKNOWN != PASS`.
