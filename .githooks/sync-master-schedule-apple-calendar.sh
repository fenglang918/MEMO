#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ "${ME_APPLE_SKIP_HOOK:-0}" == "1" || "${ME_APPLE_SKIP_HOOK:-0}" == "true" || "${ME_APPLE_SKIP_HOOK:-0}" == "yes" ]]; then
  exit 0
fi

if [[ "$#" -lt 2 ]]; then
  exit 0
fi

from_ref="$1"
to_ref="$2"

cd "${REPO_ROOT}"
changed="$(git diff --name-only "${from_ref}" "${to_ref}" -- 08_Operations/00_Master-Schedule/calendar.md || true)"
if [[ -n "${changed}" ]]; then
  bash "${REPO_ROOT}/06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.sh"
fi
