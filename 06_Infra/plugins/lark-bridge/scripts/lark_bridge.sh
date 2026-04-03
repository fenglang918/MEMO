#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOTSTRAP_SCRIPT="${SCRIPT_DIR}/bootstrap_lark_cli.sh"
DOCTOR_SCRIPT="${SCRIPT_DIR}/doctor_lark.sh"

usage() {
  cat <<'EOF'
Usage:
  bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh <subcommand> [args]

Subcommands:
  bootstrap
  doctor
  docs-search
  docs-fetch
  chats-list
  chat-search
  messages-list
  messages-search
  mail-list
  calendar-agenda
  contact-search

Examples:
  bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh doctor
  bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh docs-search --query "AgenQA" --format pretty
  bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh chats-list --format table
  bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh calendar-agenda --format pretty
EOF
}

require_lark_cli() {
  if ! command -v lark-cli >/dev/null 2>&1; then
    printf 'Missing lark-cli. Run:\n  bash 06_Infra/plugins/lark-bridge/scripts/bootstrap_lark_cli.sh\n' >&2
    exit 127
  fi
}

has_mailbox_arg() {
  local prev=""
  for arg in "$@"; do
    if [[ "${prev}" == "--mailbox" ]]; then
      return 0
    fi
    prev="${arg}"
    case "${arg}" in
      --mailbox=*) return 0 ;;
    esac
  done
  return 1
}

ensure_scopes() {
  local label="$1"
  local scopes="$2"
  require_lark_cli

  if lark-cli auth check --scope "${scopes}" >/dev/null 2>&1; then
    return
  fi

  cat <<EOF >&2
Missing required scope(s) for ${label}.
Run:
  lark-cli auth login --scope "${scopes}"
EOF
  exit 2
}

ensure_mailbox_profile() {
  if has_mailbox_arg "$@"; then
    return
  fi

  local profile_output
  profile_output="$(lark-cli mail user_mailboxes profile --as user --params '{"user_mailbox_id":"me"}' --format json 2>&1 || true)"
  if grep -q 'primary_email_address' <<<"${profile_output}"; then
    return
  fi

  if grep -q 'user does not have email' <<<"${profile_output}"; then
    cat <<'EOF' >&2
mail-list requires a Feishu mailbox for the current user, but the current user does not have email provisioned.
If you do have a mailbox, pass it explicitly with:
  --mailbox your.name@example.com
EOF
    exit 3
  fi

  cat <<'EOF' >&2
Unable to resolve the current user's mailbox profile.
Run:
  lark-cli mail user_mailboxes profile --as user --params '{"user_mailbox_id":"me"}' --format json
EOF
  exit 3
}

main() {
  local subcommand="${1:-}"
  if [[ -z "${subcommand}" ]]; then
    usage
    exit 1
  fi
  shift || true

  case "${subcommand}" in
    bootstrap)
      exec "${BOOTSTRAP_SCRIPT}" "$@"
      ;;
    doctor)
      exec "${DOCTOR_SCRIPT}" "$@"
      ;;
    docs-search)
      ensure_scopes "docs-search" "search:docs:read docx:document:readonly"
      exec lark-cli docs +search --as user "$@"
      ;;
    docs-fetch)
      ensure_scopes "docs-fetch" "docx:document:readonly"
      exec lark-cli docs +fetch --as user "$@"
      ;;
    chats-list)
      ensure_scopes "chats-list" "im:chat:read"
      exec lark-cli im chats list --as user "$@"
      ;;
    chat-search)
      ensure_scopes "chat-search" "im:chat:read"
      exec lark-cli im +chat-search --as user "$@"
      ;;
    messages-list)
      ensure_scopes "messages-list" "im:message:readonly"
      exec lark-cli im +chat-messages-list --as user "$@"
      ;;
    messages-search)
      ensure_scopes "messages-search" "im:message:readonly search:message"
      exec lark-cli im +messages-search --as user "$@"
      ;;
    mail-list)
      ensure_scopes "mail-list" "mail:user_mailbox:readonly mail:user_mailbox.message.address:read mail:user_mailbox.message.subject:read mail:user_mailbox.message.body:read"
      ensure_mailbox_profile "$@"
      exec lark-cli mail +triage --as user "$@"
      ;;
    calendar-agenda)
      ensure_scopes "calendar-agenda" "calendar:calendar:read calendar:calendar.event:read"
      exec lark-cli calendar +agenda --as user "$@"
      ;;
    contact-search)
      ensure_scopes "contact-search" "contact:user:search"
      exec lark-cli contact +search-user --as user "$@"
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      printf 'Unknown subcommand: %s\n\n' "${subcommand}" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
