---
name: master-schedule-sync
description: Sync MEMO master schedule with Apple Calendar using the existing scripts for push (`calendar.md -> Apple`), pull (manual Apple events -> `inbox.md`), or one-shot bidirectional flow. Use when the user asks to sync/update Apple Calendar events, pull phone/manual events back, or run the full schedule calendar linkage.
---

# Master Schedule Sync

Use the existing master-schedule scripts as the single entrypoint for calendar synchronization.

## Workflow

1. Ensure repo root is current working directory.
2. Default to bidirectional sync (`both`): push first, then pull.
3. Use `push-only` when the user requests publishing `calendar.md` changes only.
4. Use `pull-only` when the user requests importing manual Apple events only.
5. Report the summary lines from the scripts, including route mode and imported/skipped counts.

## Commands

Bidirectional one-shot:

```bash
bash 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar_bidirectional.sh
```

Push only (`calendar.md -> Apple`):

```bash
ME_BIDIR_MODE=push-only \
ME_ROUTING_MODE=by-type \
ME_WORK_CALENDAR=Work \
ME_PERSONAL_CALENDAR=Personal \
ME_EXPLORE_CALENDAR=Explore \
ME_INBOX_CALENDAR=Inbox \
bash 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar_bidirectional.sh
```

Pull only (manual Apple events -> `inbox.md`):

```bash
ME_BIDIR_MODE=pull-only \
ME_PULL_CALENDARS="Work,Personal,Explore,Inbox" \
bash 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar_bidirectional.sh
```

## Guardrails

- Use only these scripts:
  - `06_Infra/plugins/master-schedule/scripts/sync_apple_calendar_bidirectional.sh`
  - `06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.sh`
  - `06_Infra/plugins/master-schedule/scripts/pull_apple_calendar_to_inbox.sh`
- Do not reimplement synchronization logic in ad-hoc commands.
- Keep routing default as `by-type` unless the user explicitly changes it.
- Preserve de-dup behavior in pull flow (`APPLE_PULL_ID`).

## References

- `06_Infra/plugins/master-schedule/README.md`
- `08_Operations/00_Master-Schedule/README.md`
