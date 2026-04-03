# lark-bridge

MEMO's local Lark/Feishu CLI bridge plugin.

It does not store primary knowledge in this repo. Instead, it bridges the local
`lark-cli` runtime into MEMO so agents and humans can query docs, chats,
messages, mail, calendars, and contacts from the same workspace.

## Scope

`lark-bridge` is a read-first infrastructure plugin:

- default: read-only workflows
- v1 domains: docs, chats, messages, mail, calendar, contact
- write actions: intentionally excluded from default wrappers and skill flow

This plugin assumes:

- macOS + zsh
- Homebrew available for bootstrap
- Node/npm available or installable
- `@larksuite/cli` installed globally
- OAuth login state stored locally on the machine

## Safety boundaries

- Do not commit tokens, app secrets, or CLI cache/state to the repo.
- Do not dump sensitive message/doc content into repo files unless the user
  explicitly asks for archival.
- Default wrapper commands are read-only.
- For missing scopes, the scripts print exact `lark-cli auth login --scope ...`
  commands instead of silently escalating permissions.

## Layout

```text
06_Infra/plugins/lark-bridge/
├── README.md
├── scripts/
│   ├── bootstrap_lark_cli.sh
│   ├── doctor_lark.sh
│   └── lark_bridge.sh
└── .agents/skills/lark-bridge/
    └── SKILL.md
```

## Agent Entry

- `.agents/skills/lark-bridge/SKILL.md`
  - 插件级 read-first workflow 入口
  - 适合在同一工作区里查询 docs / chats / messages / mail / calendar / contacts
  - 默认不把写侧操作当成这条 skill 的主路径

## Bootstrap

Run bootstrap when setting up a new machine or when `lark-cli` is missing:

```bash
bash 06_Infra/plugins/lark-bridge/scripts/bootstrap_lark_cli.sh
```

Bootstrap behavior:

- installs `node` via Homebrew if missing
- installs `@larksuite/cli` globally if missing
- installs Lark skills globally via `skills`
- runs a doctor check
- prints the next exact auth/config command if local login is incomplete

It does not silently finish browser-based authorization for you.

## Doctor

Use doctor before queries or when something fails:

```bash
bash 06_Infra/plugins/lark-bridge/scripts/doctor_lark.sh
```

Doctor checks:

- `brew`, `node`, `npm`, `lark-cli`
- Lark skills installation
- `lark-cli` version
- auth state / identity / token validity
- v1 read-scope coverage

Troubleshooting order:

1. `doctor`
2. `bootstrap`
3. `lark-cli auth status`
4. `lark-cli auth login --scope "..."`

## Wrapper interface

Stable wrapper entry:

```bash
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh <subcommand> [args]
```

Supported subcommands:

- `bootstrap`
- `doctor`
- `docs-search`
- `docs-fetch`
- `chats-list`
- `chat-search`
- `messages-list`
- `messages-search`
- `mail-list`
- `calendar-agenda`
- `contact-search`

All data commands default to `--as user` and transparently forward the remaining
arguments to `lark-cli`.

## Examples

```bash
# Search docs/wiki/spreadsheets
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh docs-search \
  --query "AgenQA" --format pretty

# Fetch a doc by URL or token
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh docs-fetch \
  --doc "https://my.feishu.cn/wiki/SAeAwiQPLi0VDCkAA6ocYM6lnah" --format pretty

# List current chats
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh chats-list \
  --params '{"page_size":20,"sort_type":"ByActiveTimeDesc"}' --format table

# Search chats by name/member
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh chat-search \
  --query "Innovator" --format pretty

# List messages in a chat
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh messages-list \
  --chat-id "oc_xxx" --page-size 20 --format pretty

# Search messages across chats
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh messages-search \
  --query "AgenQA" --format pretty

# List mail summaries
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh mail-list \
  --max 10

# Show today's agenda
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh calendar-agenda \
  --format pretty

# Search contacts
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh contact-search \
  --query "冯亮" --format pretty
```

## Recommended auth scopes for v1

The wrappers check and hint exact scopes before calling the API.

- docs search: `search:docs:read docx:document:readonly`
- docs fetch: `docx:document:readonly`
- chats: `im:chat:read`
- messages list: `im:message:readonly`
- messages search: `im:message:readonly search:message`
- mail: `mail:user_mailbox:readonly mail:user_mailbox.message.address:read mail:user_mailbox.message.subject:read mail:user_mailbox.message.body:read`
- calendar: `calendar:calendar:read calendar:calendar.event:read`
- contact: `contact:user:search`

If a scope is missing, the wrapper prints the exact `auth login --scope` command
to run next.

Mail has one extra environment requirement: the current user must actually have
a Feishu mailbox. If the mailbox is not provisioned, `mail-list` fails early
with a readable hint instead of surfacing the raw API error.
