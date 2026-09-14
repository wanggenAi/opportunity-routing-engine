#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

resolve_latest_source_run() {
  local workflow="$1"
  local snapshot
  snapshot="$(gh run list \
    --repo "$GITHUB_REPOSITORY" \
    --workflow "$workflow" \
    --branch main \
    --limit 1 \
    --json databaseId,status,conclusion,createdAt,updatedAt)"

  local run_id status conclusion
  run_id="$(jq -r '.[0].databaseId // empty' <<<"$snapshot")"
  status="$(jq -r '.[0].status // empty' <<<"$snapshot")"
  conclusion="$(jq -r '.[0].conclusion // empty' <<<"$snapshot")"
  if [[ -z "$run_id" ]]; then
    echo "No upstream run exists for $workflow" >&2
    return 1
  fi
  if [[ "$status" != "completed" || "$conclusion" != "success" ]]; then
    echo "Latest upstream run for $workflow is not completed+success: id=$run_id status=$status conclusion=$conclusion" >&2
    return 1
  fi
  printf '%s\n' "$run_id"
}

resolve_previous_live_success() {
  gh run list \
    --repo "$GITHUB_REPOSITORY" \
    --workflow observation-fabric-live.yml \
    --branch main \
    --status success \
    --limit 1 \
    --json databaseId \
    --jq '.[0].databaseId // empty'
}

jiangsu_run_id="$(resolve_latest_source_run jiangsu-money-flow-live.yml)"
regional_run_id="$(resolve_latest_source_run regional-data-live.yml)"
resource_run_id="$(resolve_latest_source_run resource-underuse-live.yml)"
previous_live_run_id="$(resolve_previous_live_success || true)"

{
  echo "jiangsu_run_id=$jiangsu_run_id"
  echo "regional_run_id=$regional_run_id"
  echo "resource_run_id=$resource_run_id"
  echo "previous_live_run_id=$previous_live_run_id"
} >> "$GITHUB_OUTPUT"

mkdir -p .local
for spec in \
  "jiangsu:$jiangsu_run_id" \
  "regional:$regional_run_id" \
  "resource:$resource_run_id"; do
  key="${spec%%:*}"
  run_id="${spec#*:}"
  gh run view "$run_id" \
    --repo "$GITHUB_REPOSITORY" \
    --json databaseId,headSha,createdAt,updatedAt,url,status,conclusion,event \
    > ".local/${key}_run.json"
done

jq -n \
  --slurpfile jiangsu .local/jiangsu_run.json \
  --slurpfile regional .local/regional_run.json \
  --slurpfile resource .local/resource_run.json \
  --arg previous_live_run_id "$previous_live_run_id" \
  '{
    resolved_at_utc: (now | todateiso8601),
    upstream_runs: {
      jiangsu_money_flow: $jiangsu[0],
      regional_data: $regional[0],
      resource_underuse: $resource[0]
    },
    previous_live_run_id: (if $previous_live_run_id == "" then null else ($previous_live_run_id | tonumber) end),
    bootstrap: ($previous_live_run_id == "")
  }' > .local/live_observation_upstream_manifest.json
