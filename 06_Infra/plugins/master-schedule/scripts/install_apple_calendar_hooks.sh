#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
HOOKS_DIR="${REPO_ROOT}/.githooks"

if [[ ! -d "${HOOKS_DIR}" ]]; then
  echo "Hooks directory missing: ${HOOKS_DIR}" >&2
  exit 1
fi

git config --local core.hooksPath ".githooks"
echo "[MEMO_HOOKS] core.hooksPath set to .githooks"
echo "[MEMO_HOOKS] Installed post-commit/post-merge hooks for Apple Calendar sync."
