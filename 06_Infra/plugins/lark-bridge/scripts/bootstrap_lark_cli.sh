#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCTOR_SCRIPT="${SCRIPT_DIR}/doctor_lark.sh"
LARK_SKILL_DIR="${HOME}/.agents/skills/lark-shared"

info() {
  printf '[lark-bootstrap] %s\n' "$1"
}

warn() {
  printf '[lark-bootstrap] WARN: %s\n' "$1" >&2
}

fail() {
  printf '[lark-bootstrap] ERROR: %s\n' "$1" >&2
  exit 1
}

ensure_node() {
  if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    info "node/npm already available: $(node -v) / $(npm -v)"
    return
  fi

  if ! command -v brew >/dev/null 2>&1; then
    fail "Homebrew not found. Install Homebrew first, or install node/npm manually."
  fi

  info "Installing node via Homebrew..."
  brew install node
  info "node/npm ready: $(node -v) / $(npm -v)"
}

ensure_lark_cli() {
  if command -v lark-cli >/dev/null 2>&1; then
    info "lark-cli already installed: $(lark-cli --version)"
    return
  fi

  info "Installing @larksuite/cli globally..."
  npm install -g @larksuite/cli
  info "lark-cli ready: $(lark-cli --version)"
}

ensure_lark_skills() {
  if [[ -f "${LARK_SKILL_DIR}/SKILL.md" ]]; then
    info "Global Lark skills already installed: ${LARK_SKILL_DIR}"
    return
  fi

  info "Installing Lark skills globally..."
  npx --yes skills add larksuite/cli -y -g
}

print_next_steps() {
  local status_output="$1"

  if grep -q 'not configured' <<<"${status_output}"; then
    cat <<'EOF'

Next step: configure the app in a browser.
Run this command in the background, copy the URL it prints, then open it:

  lark-cli config init --new

After configuration completes, log in with:

  lark-cli auth login --recommend
EOF
    return
  fi

  if grep -q 'No user logged in' <<<"${status_output}"; then
    cat <<'EOF'

Next step: log in with your user identity.
Run this command in the background, copy the URL it prints, then open it:

  lark-cli auth login --recommend
EOF
    return
  fi

  cat <<'EOF'

Bootstrap completed. Run the doctor for a full capability/scope check:

  bash 06_Infra/plugins/lark-bridge/scripts/doctor_lark.sh
EOF
}

main() {
  ensure_node
  ensure_lark_cli
  ensure_lark_skills

  if [[ -x "${DOCTOR_SCRIPT}" ]]; then
    "${DOCTOR_SCRIPT}" || true
  fi

  local status_output
  status_output="$(lark-cli auth status 2>&1 || true)"
  print_next_steps "${status_output}"
}

main "$@"
