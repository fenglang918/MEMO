#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
STATE_FILE="${SCRIPT_DIR}/.watch_calendar_changes_state"

CALENDAR_PATH="${1:-08_Operations/00_Master-Schedule/calendar.md}"
SYNC_SCRIPT="${SCRIPT_DIR}/sync_apple_calendar.sh"

FILE_PATH="${REPO_ROOT}/${CALENDAR_PATH}"
if [[ ! -f "${FILE_PATH}" ]]; then
  echo "Calendar file not found: ${FILE_PATH}" >&2
  exit 1
fi

if ! command -v fswatch >/dev/null 2>&1; then
  echo "Required tool not found: fswatch. Install with `brew install fswatch`." >&2
  exit 1
fi

echo "[ME_APPLE_WATCH] monitoring: ${FILE_PATH}"
echo "[ME_APPLE_WATCH] sync: ${SYNC_SCRIPT}"

get_mtime() {
  stat -f %m "$1"
}

last_mtime="$(get_mtime "${FILE_PATH}")"
echo "${last_mtime}" >"${STATE_FILE}"

while true; do
  fswatch -1 "${FILE_PATH}"
  current_mtime="$(get_mtime "${FILE_PATH}")"
  if [[ "${current_mtime}" != "${last_mtime}" ]]; then
    last_mtime="${current_mtime}"
    echo "[ME_APPLE_WATCH] changed, trigger sync"
    bash "${SYNC_SCRIPT}"
    echo "${current_mtime}" >"${STATE_FILE}"
  fi
done
