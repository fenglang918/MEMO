#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root dynamically; allow explicit override via MEMO_HOME/ME_REPO_ROOT.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
ME_REPO_ROOT="${MEMO_HOME:-${ME_REPO_ROOT:-$DEFAULT_REPO_ROOT}}"
PUSH_SCRIPT="${ME_REPO_ROOT}/06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.sh"
PULL_SCRIPT="${ME_REPO_ROOT}/06_Infra/plugins/master-schedule/scripts/pull_apple_calendar_to_inbox.sh"
MODE="${ME_BIDIR_MODE:-both}"

cd "$ME_REPO_ROOT"

if [[ "$MODE" != "both" && "$MODE" != "push-only" && "$MODE" != "pull-only" ]]; then
  echo "[ERROR] invalid ME_BIDIR_MODE=$MODE (expected: both|push-only|pull-only)"
  exit 2
fi

if [[ "$MODE" == "both" || "$MODE" == "push-only" ]]; then
  echo "[STEP] push: calendar.md -> Apple Calendar"
  bash "$PUSH_SCRIPT"
fi

if [[ "$MODE" == "both" || "$MODE" == "pull-only" ]]; then
  echo "[STEP] pull: Apple Calendar manual events -> inbox.md"
  bash "$PULL_SCRIPT"
fi

echo "[OK] bidirectional sync finished (mode=$MODE)"
