#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

resolve_run() {
  local workflow="$1"
  gh run list \
    --repo "$GITHUB_REPOSITORY" \
    --workflow "$workflow" \
    --branch main \
    --status success \
    --limit 1 \
    --json databaseId \
    --jq '.[0].databaseId // empty'
}

jiangsu_run_id="$(resolve_run jiangsu-money-flow-live.yml)"
regional_run_id="$(resolve_run regional-data-live.yml)"
resource_run_id="$(resolve_run resource-underuse-live.yml)"
previous_live_run_id="$(resolve_run observation-fabric-live.yml || true)"

for pair in \
  "jiangsu_run_id:$jiangsu_run_id" \
  "regional_run_id:$regional_run_id" \
  "resource_run_id:$resource_run_id"; do
  name="${pair%%:*}"
  value="${pair#*:}"
  if [[ -z "$value" ]]; then
    echo "No successful upstream run resolved for $name" >&2
    exit 1
  fi
done

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
    --json databaseId,headSha,createdAt,updatedAt,url,conclusion,event \
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
