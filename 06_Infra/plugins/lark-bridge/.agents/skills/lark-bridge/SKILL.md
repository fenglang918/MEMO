---
name: lark-bridge
description: Query local Lark/Feishu data from MEMO through the repo's read-first `lark-bridge` plugin. Use when the user wants to inspect docs, chats, messages, mail, calendars, or contacts via the locally configured `lark-cli`.
---

# Lark Bridge

Use this skill for Lark/Feishu queries that should go through the MEMO-local
plugin wrapper instead of scattered raw `lark-cli` commands.

## Workflow

1. Run doctor first:
   ```bash
   bash 06_Infra/plugins/lark-bridge/scripts/doctor_lark.sh
   ```
2. If dependencies or global Lark skills are missing, bootstrap:
   ```bash
   bash 06_Infra/plugins/lark-bridge/scripts/bootstrap_lark_cli.sh
   ```
3. If doctor or a wrapper reports missing scopes, use the exact printed command:
   ```bash
   lark-cli auth login --scope "<space separated scopes>"
   ```
4. For read queries, prefer the wrapper:
   ```bash
   bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh <subcommand> [args]
   ```

## Preferred entrypoints

- docs:
  - `docs-search`
  - `docs-fetch`
- chats:
  - `chats-list`
  - `chat-search`
- messages:
  - `messages-list`
  - `messages-search`
- mail:
  - `mail-list`
- calendar:
  - `calendar-agenda`
- contacts:
  - `contact-search`

## Safety rules

- Default to read-only workflows.
- Do not write Feishu/Lark objects unless the user explicitly asks.
- Do not persist auth tokens, app secrets, or copied sensitive content into repo
  files unless the user explicitly asks for archival.
- When a query needs broader access, stop at the missing-scope hint and have the
  user complete the browser authorization flow.
- `mail-list` also depends on the current user having a Feishu mailbox. If the
  wrapper says the mailbox is unavailable, treat that as an environment
  limitation instead of a scope problem.
