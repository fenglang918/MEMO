# Apple Calendar Sync Hooks

本目录用于在 `08_Operations/00_Master-Schedule/calendar.md` 变更后，自动触发 Apple Calendar 同步。

- `post-commit`：检测 commit 结果中的 `calendar.md` 变更
- `post-merge`：检测 merge 结果中的 `calendar.md` 变更
- `sync-master-schedule-apple-calendar.sh`：统一检测逻辑并调用 `06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.sh`

启用方式：

```bash
git config --local core.hooksPath .githooks
```

可选环境变量：

- `ME_APPLE_SKIP_HOOK=1`：临时跳过 hooks
- `ME_DRY_RUN=1`：只预览 Apple Calendar 同步结果
- `ME_FROM_DATE=2026-01-01`：设置同步起始日期
- `ME_WORK_CALENDAR` / `ME_PERSONAL_CALENDAR` / `ME_EXPLORE_CALENDAR` / `ME_INBOX_CALENDAR`：覆盖默认日历名
