#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root dynamically; allow explicit override via MEMO_HOME/ME_REPO_ROOT.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
ME_REPO_ROOT="${MEMO_HOME:-${ME_REPO_ROOT:-$DEFAULT_REPO_ROOT}}"
SCRIPT="${ME_REPO_ROOT}/06_Infra/plugins/master-schedule/scripts/pull_apple_calendar_to_inbox.py"
INBOX_PATH="${ME_INBOX_PATH:-08_Operations/00_Master-Schedule/inbox.md}"
FROM_DATE="${ME_FROM_DATE:-$(date +%F)}"
TO_DATE="${ME_TO_DATE:-}"
CALENDARS="${ME_PULL_CALENDARS:-Work,Personal,Explore,Inbox}"
DRY_RUN="${ME_DRY_RUN:-0}"
VERBOSE="${ME_VERBOSE:-0}"

cd "$ME_REPO_ROOT"

PY_ARGS=(
  --inbox "$INBOX_PATH"
  --from-date "$FROM_DATE"
  --calendars "$CALENDARS"
)

if [[ -n "$TO_DATE" ]]; then
  PY_ARGS+=(--to-date "$TO_DATE")
fi

if [[ "$DRY_RUN" == "1" || "$DRY_RUN" == "true" ]]; then
  PY_ARGS+=(--dry-run)
fi

if [[ "$VERBOSE" == "1" || "$VERBOSE" == "true" ]]; then
  PY_ARGS+=(--verbose)
fi

python3 "$SCRIPT" "${PY_ARGS[@]}"
