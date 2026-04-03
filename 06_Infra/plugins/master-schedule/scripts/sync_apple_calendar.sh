#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root dynamically; allow explicit override via MEMO_HOME/ME_REPO_ROOT.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
ME_REPO_ROOT="${MEMO_HOME:-${ME_REPO_ROOT:-$DEFAULT_REPO_ROOT}}"
CALENDAR_PATH="08_Operations/00_Master-Schedule/calendar.md"
SCRIPT="${ME_REPO_ROOT}/06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.py"

ROUTING_MODE="${ME_ROUTING_MODE:-by-type}"
APPLE_CALENDAR="${ME_APPLE_CALENDAR:-Home}"
INBOX_CALENDAR="${ME_INBOX_CALENDAR:-Inbox}"
WORK_CALENDAR="${ME_WORK_CALENDAR:-Work}"
PERSONAL_CALENDAR="${ME_PERSONAL_CALENDAR:-Personal}"
EXPLORE_CALENDAR="${ME_EXPLORE_CALENDAR:-Explore}"
CALENDAR_ACCOUNT="${ME_CALENDAR_ACCOUNT:-iCloud}"
TITLE_FILTER="${ME_TITLE_FILTER:-${ME_APPLE_TITLE_FILTER:-}}"
FROM_DATE="${ME_FROM_DATE:-$(date +%F)}"
DRY_RUN="${ME_DRY_RUN:-0}"
PREFLIGHT_ONLY="${ME_PREFLIGHT_ONLY:-0}"
REQUIRE_EXISTING="${ME_REQUIRE_EXISTING_CALENDARS:-1}"
AUTO_CREATE_MISSING="${ME_AUTO_CREATE_MISSING_CALENDARS:-0}"

cd "$ME_REPO_ROOT"

PY_ARGS=(
  --calendar "$CALENDAR_PATH"
  --routing-mode "$ROUTING_MODE"
  --from-date "$FROM_DATE"
)

if [[ "$ROUTING_MODE" == "single" ]]; then
  PY_ARGS+=(--apple-calendar "$APPLE_CALENDAR")
elif [[ "$ROUTING_MODE" == "by-project" ]] || [[ "$ROUTING_MODE" == "by-quadrant" ]]; then
  PY_ARGS+=(--inbox-calendar "$INBOX_CALENDAR")
  if [[ "$REQUIRE_EXISTING" == "1" || "$REQUIRE_EXISTING" == "true" ]]; then
    PY_ARGS+=(--require-existing-calendars)
  else
    PY_ARGS+=(--no-require-existing-calendars)
  fi
  if [[ -n "${ME_APPLE_CALENDAR:-}" ]]; then
    echo "[INFO] routing-mode=$ROUTING_MODE, ignore ME_APPLE_CALENDAR=${ME_APPLE_CALENDAR}"
  fi
elif [[ "$ROUTING_MODE" == "by-type" ]]; then
  PY_ARGS+=(
    --inbox-calendar "$INBOX_CALENDAR"
    --work-calendar "$WORK_CALENDAR"
    --personal-calendar "$PERSONAL_CALENDAR"
    --explore-calendar "$EXPLORE_CALENDAR"
  )
  if [[ "$REQUIRE_EXISTING" == "1" || "$REQUIRE_EXISTING" == "true" ]]; then
    PY_ARGS+=(--require-existing-calendars)
  else
    PY_ARGS+=(--no-require-existing-calendars)
  fi
  if [[ -n "${ME_APPLE_CALENDAR:-}" ]]; then
    echo "[INFO] routing-mode=$ROUTING_MODE, ignore ME_APPLE_CALENDAR=${ME_APPLE_CALENDAR}"
  fi
else
  echo "[INFO] routing-mode=$ROUTING_MODE, no extra compatibility flags for Apple calendar binding"
fi

if [[ -n "$CALENDAR_ACCOUNT" ]]; then
  PY_ARGS+=(--calendar-account "$CALENDAR_ACCOUNT")
fi

if [[ "$AUTO_CREATE_MISSING" == "1" || "$AUTO_CREATE_MISSING" == "true" ]]; then
  PY_ARGS+=(--auto-create-missing-calendars)
else
  PY_ARGS+=(--no-auto-create-missing-calendars)
fi

if [[ -n "$TITLE_FILTER" ]]; then
  PY_ARGS+=(--title-contains "$TITLE_FILTER")
fi

if [[ "${DRY_RUN}" == "1" ]]; then
  PY_ARGS+=(--dry-run)
fi

if [[ "${PREFLIGHT_ONLY}" == "1" ]]; then
  PY_ARGS+=(--preflight-only)
fi

python3 "$SCRIPT" "${PY_ARGS[@]}"
