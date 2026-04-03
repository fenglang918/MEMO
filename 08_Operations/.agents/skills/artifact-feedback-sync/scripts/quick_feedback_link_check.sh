#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  quick_feedback_link_check.sh \
    --project-root <project_root> \
    --artifact-path <path> \
    --raw-dialogue-path <path> \
    --feedback-log-path <path> \
    [--index-path <path>]

Description:
  Validate path existence and bidirectional link keywords across
  artifact, raw-dialogue, feedback-log (and optional INDEX file).
EOF
}

project_root=""
artifact_path=""
raw_dialogue_path=""
feedback_log_path=""
index_path=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-root)
      project_root="${2:-}"
      shift 2
      ;;
    --artifact-path)
      artifact_path="${2:-}"
      shift 2
      ;;
    --raw-dialogue-path)
      raw_dialogue_path="${2:-}"
      shift 2
      ;;
    --feedback-log-path)
      feedback_log_path="${2:-}"
      shift 2
      ;;
    --index-path)
      index_path="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[ERROR] Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$project_root" || -z "$artifact_path" || -z "$raw_dialogue_path" || -z "$feedback_log_path" ]]; then
  echo "[ERROR] missing required arguments." >&2
  usage >&2
  exit 2
fi

if [[ ! -d "$project_root" ]]; then
  echo "[ERROR] project_root not found: $project_root" >&2
  exit 2
fi

fail=0

require_file() {
  local rel="$1"
  local abs="$project_root/$rel"
  if [[ ! -f "$abs" ]]; then
    echo "[FAIL] missing file: $rel"
    fail=1
  else
    echo "[OK] file exists: $rel"
  fi
}

require_contains() {
  local rel="$1"
  local needle="$2"
  local abs="$project_root/$rel"
  if grep -Fq "$needle" "$abs"; then
    echo "[OK] $rel contains: $needle"
  else
    echo "[FAIL] $rel missing: $needle"
    fail=1
  fi
}

require_file "$artifact_path"
require_file "$raw_dialogue_path"
require_file "$feedback_log_path"
if [[ -n "$index_path" ]]; then
  require_file "$index_path"
fi

if [[ $fail -ne 0 ]]; then
  echo "[FAIL] stop due to missing file(s)."
  exit 1
fi

require_contains "$artifact_path" "## 内部索引（仅内部）"
require_contains "$artifact_path" "$raw_dialogue_path"
require_contains "$artifact_path" "$feedback_log_path"

require_contains "$raw_dialogue_path" "$artifact_path"
require_contains "$raw_dialogue_path" "$feedback_log_path"
require_contains "$raw_dialogue_path" "git 快照"

require_contains "$feedback_log_path" "$artifact_path"
require_contains "$feedback_log_path" "$raw_dialogue_path"
require_contains "$feedback_log_path" "## 3) 目标产物 git 快照（记录时刻）"
require_contains "$feedback_log_path" "## 4) 本次反馈时间序（摘要）"

if [[ -n "$index_path" ]]; then
  require_contains "$index_path" "$raw_dialogue_path"
  require_contains "$index_path" "$feedback_log_path"
fi

if [[ $fail -ne 0 ]]; then
  echo "[FAIL] quick feedback link check found issues."
  exit 1
fi

echo "[OK] quick feedback link check passed."
