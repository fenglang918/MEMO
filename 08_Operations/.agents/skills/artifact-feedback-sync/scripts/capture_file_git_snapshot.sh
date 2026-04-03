#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  capture_file_git_snapshot.sh --repo-root <repo_root> --file-relpath <file_relpath> [--recorded-at <iso_timestamp>] [--label <label>]

Description:
  Emit markdown-ready git snapshot fields for any file in a git repo.
  Fail-fast if repo_root is not a git repo or file does not exist.
EOF
}

repo_root=""
file_relpath=""
recorded_at=""
label="目标产物"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      repo_root="${2:-}"
      shift 2
      ;;
    --file-relpath)
      file_relpath="${2:-}"
      shift 2
      ;;
    --recorded-at)
      recorded_at="${2:-}"
      shift 2
      ;;
    --label)
      label="${2:-}"
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

if [[ -z "$repo_root" || -z "$file_relpath" ]]; then
  echo "[ERROR] --repo-root and --file-relpath are required." >&2
  usage >&2
  exit 2
fi

if [[ ! -d "$repo_root" ]]; then
  echo "[ERROR] repo_root not found: $repo_root" >&2
  exit 2
fi

if ! git -C "$repo_root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[ERROR] not a git repository: $repo_root" >&2
  exit 2
fi

file_abs="$repo_root/$file_relpath"
if [[ ! -f "$file_abs" ]]; then
  echo "[ERROR] file not found: $file_abs" >&2
  exit 2
fi

if [[ -z "$recorded_at" ]]; then
  recorded_at="$(date -Iseconds)"
fi

branch="$(git -C "$repo_root" branch --show-current)"
head_full="$(git -C "$repo_root" rev-parse HEAD)"
head_short="$(git -C "$repo_root" rev-parse --short HEAD)"
file_blob_hash="$(git -C "$repo_root" hash-object "$file_relpath")"
last_commit_full="$(git -C "$repo_root" log -1 --format='%H' -- "$file_relpath")"
last_commit_date="$(git -C "$repo_root" log -1 --format='%ad' --date=iso -- "$file_relpath")"
last_commit_subject="$(git -C "$repo_root" log -1 --format='%s' -- "$file_relpath")"

cat <<EOF
- 记录时刻：\`$recorded_at\`
- Git 仓库根：\`$repo_root\`
- 分支：\`$branch\`
- 当前 HEAD：
  - short: \`$head_short\`
  - full: \`$head_full\`
- ${label}文件路径（repo 相对）：
  - \`$file_relpath\`
- ${label}文件 blob hash（工作区）：
  - \`$file_blob_hash\`
- 最近一次修改该文件的提交：
  - commit: \`$last_commit_full\`
  - date: \`$last_commit_date\`
  - subject: \`$last_commit_subject\`
EOF
