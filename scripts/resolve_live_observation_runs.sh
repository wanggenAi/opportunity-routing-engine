#!/usr/bin/env bash
set -euo pipefail

: "${GH_TOKEN:?GH_TOKEN is required}"
: "${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"
: "${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}"

resolve_upstream_run() {
  local workflow="$1"
  local run_json database_id status conclusion

  run_json="$(gh run list \
    --repo "$GITHUB_REPOSITORY" \
    --workflow "$workflow" \
    --branch main \
    --limit 1 \
    --json databaseId,status,conclusion \
    --jq '.[0] // empty')"

  if [[ -z "$run_json" || "$run_json" == "null" ]]; then
    echo "No main-branch run exists for upstream workflow $workflow" >&2
    return 1
  fi

  database_id="$(jq -r '.databaseId // empty' <<<"$run_json")"
  status="$(jq -r '.status // empty' <<<"$run_json")"
  conclusion="$(jq -r '.conclusion // empty' <<<"$run_json")"
  if [[ -z "$database_id" || "$status" != "completed" || "$conclusion" != "success" ]]; then
    echo "Latest main-branch run for $workflow is not completed/success (id=${database_id:-unknown}, status=${status:-unknown}, conclusion=${conclusion:-unknown}); refusing to fall back to an older successful artifact" >&2
    return 1
  fi

  echo "$database_id"
}

resolve_previous_live_run() {
  gh run list \
    --repo "$GITHUB_REPOSITORY" \
    --workflow observation-fabric-live.yml \
    --branch main \
    --status success \
    --limit 1 \
    --json databaseId \
    --jq '.[0].databaseId // empty'
}

jiangsu_run_id="$(resolve_upstream_run jiangsu-money-flow-live.yml)"
regional_run_id="$(resolve_upstream_run regional-data-live.yml)"
resource_run_id="$(resolve_upstream_run resource-underuse-live.yml)"
previous_live_run_id="$(resolve_previous_live_run || true)"

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
