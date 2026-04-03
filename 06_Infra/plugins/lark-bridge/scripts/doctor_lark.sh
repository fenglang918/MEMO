#!/usr/bin/env bash

set -euo pipefail

LARK_SKILL_DIR="${HOME}/.agents/skills/lark-shared"

status_json=""
missing_any=0

print_line() {
  printf '[lark-doctor] %s\n' "$1"
}

check_binary() {
  local name="$1"
  if command -v "${name}" >/dev/null 2>&1; then
    print_line "${name}: OK ($(command -v "${name}"))"
  else
    print_line "${name}: MISSING"
    missing_any=1
  fi
}

python_json_field() {
  local field="$1"
  STATUS_JSON="${status_json}" python3 - "$field" <<'PY' 2>/dev/null || true
import json
import os
import sys

field = sys.argv[1]
try:
    data = json.loads(os.environ["STATUS_JSON"])
except Exception:
    sys.exit(0)

value = data.get(field)
if value is None:
    sys.exit(0)
print(value)
PY
}

print_scope_hints() {
  local key="$1"
  local scopes
  local label
  scopes="$(scope_for "${key}")"
  label="$(scope_description_for "${key}")"
  print_line "missing scope group for ${label}"
  printf '  run: lark-cli auth login --scope "%s"\n' "${scopes}"
}

check_scope_group() {
  local key="$1"
  local scopes
  scopes="$(scope_for "${key}")"
  if lark-cli auth check --scope "${scopes}" >/dev/null 2>&1; then
    print_line "scopes $(scope_description_for "${key}"): OK"
  else
    missing_any=1
    print_scope_hints "${key}"
  fi
}

scope_for() {
  case "$1" in
    docs_search) printf '%s\n' 'search:docs:read docx:document:readonly' ;;
    docs_fetch) printf '%s\n' 'docx:document:readonly' ;;
    chats) printf '%s\n' 'im:chat:read' ;;
    messages_list) printf '%s\n' 'im:message:readonly' ;;
    messages_search) printf '%s\n' 'im:message:readonly search:message' ;;
    mail) printf '%s\n' 'mail:user_mailbox:readonly mail:user_mailbox.message.address:read mail:user_mailbox.message.subject:read mail:user_mailbox.message.body:read' ;;
    calendar) printf '%s\n' 'calendar:calendar:read calendar:calendar.event:read' ;;
    contact) printf '%s\n' 'contact:user:search' ;;
    *) return 1 ;;
  esac
}

scope_description_for() {
  case "$1" in
    docs_search) printf '%s\n' 'docs-search' ;;
    docs_fetch) printf '%s\n' 'docs-fetch' ;;
    chats) printf '%s\n' 'chats-list/chat-search' ;;
    messages_list) printf '%s\n' 'messages-list' ;;
    messages_search) printf '%s\n' 'messages-search' ;;
    mail) printf '%s\n' 'mail-list' ;;
    calendar) printf '%s\n' 'calendar-agenda' ;;
    contact) printf '%s\n' 'contact-search' ;;
    *) return 1 ;;
  esac
}

main() {
  print_line "Checking local prerequisites..."
  check_binary brew
  check_binary node
  check_binary npm
  check_binary lark-cli

  if command -v node >/dev/null 2>&1; then
    print_line "node version: $(node -v)"
  fi
  if command -v npm >/dev/null 2>&1; then
    print_line "npm version: $(npm -v)"
  fi

  if [[ -f "${LARK_SKILL_DIR}/SKILL.md" ]]; then
    print_line "global lark skills: OK (${LARK_SKILL_DIR})"
  else
    print_line "global lark skills: MISSING (${LARK_SKILL_DIR})"
    print_line "hint: run bash 06_Infra/plugins/lark-bridge/scripts/bootstrap_lark_cli.sh"
    missing_any=1
  fi

  if ! command -v lark-cli >/dev/null 2>&1; then
    exit "${missing_any}"
  fi

  print_line "lark-cli version: $(lark-cli --version)"

  status_json="$(lark-cli auth status 2>&1 || true)"
  local identity token_status user_name
  identity="$(python_json_field identity)"
  token_status="$(python_json_field tokenStatus)"
  user_name="$(python_json_field userName)"

  if grep -q 'not configured' <<<"${status_json}"; then
    print_line "auth status: NOT CONFIGURED"
    print_line "run: lark-cli config init --new"
    missing_any=1
    exit "${missing_any}"
  fi

  if grep -q 'No user logged in' <<<"${status_json}"; then
    print_line "auth status: APP CONFIGURED, USER NOT LOGGED IN"
    print_line "run: lark-cli auth login --recommend"
    missing_any=1
    exit "${missing_any}"
  fi

  print_line "auth identity: ${identity:-unknown}"
  print_line "token status: ${token_status:-unknown}"
  if [[ -n "${user_name}" ]]; then
    print_line "user: ${user_name}"
  fi

  if [[ "${token_status}" != "valid" ]]; then
    print_line "token is not valid; refresh login first."
    print_line "run: lark-cli auth login --recommend"
    missing_any=1
    exit "${missing_any}"
  fi

  print_line "Checking v1 read scopes..."
  check_scope_group docs_search
  check_scope_group docs_fetch
  check_scope_group chats
  check_scope_group messages_list
  check_scope_group messages_search
  check_scope_group mail
  check_scope_group calendar
  check_scope_group contact

  local mail_profile
  mail_profile="$(lark-cli mail user_mailboxes profile --as user --params '{"user_mailbox_id":"me"}' --format json 2>&1 || true)"
  if grep -q 'primary_email_address' <<<"${mail_profile}"; then
    print_line "mail profile: OK"
  else
    missing_any=1
    print_line "mail profile: UNAVAILABLE"
    if grep -q 'user does not have email' <<<"${mail_profile}"; then
      print_line "hint: current user does not have a Feishu mailbox; mail-list cannot work until mailbox is provisioned."
    else
      print_line "hint: run lark-cli mail user_mailboxes profile --as user --params '{\"user_mailbox_id\":\"me\"}' --format json"
    fi
  fi

  if [[ "${missing_any}" -eq 0 ]]; then
    print_line "doctor result: OK"
  else
    print_line "doctor result: ACTION NEEDED"
  fi

  exit "${missing_any}"
}

main "$@"
