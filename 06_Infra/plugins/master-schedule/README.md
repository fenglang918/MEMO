# master-schedule

为 MEMO 提供“跨项目总日程”能力：从各项目 Markdown 中抽取时间节点，生成统一时间线、月视图和 Apple Calendar 同步链路。

## 目录

- 脚本：`scripts/extract_timeline.py`
- 脚本：`scripts/build_month_calendar_feed.py`
- 脚本：`scripts/build_apple_calendar_ics.py`
- 脚本：`scripts/time_tracking.py`
- Agent 入口：`../../../.agents/skills/master-schedule-sync/`
- 主日程工作区：`../../../08_Operations/00_Master-Schedule/`
- 时间投入记录：`../../../08_Operations/01_Time-Tracking/`
- Git hooks：`../../../.githooks/`

## Agent Entry / Agent 入口

- `../../../.agents/skills/master-schedule-sync/SKILL.md`
  - 模板默认的日程同步入口
- `../../../08_Operations/00_Master-Schedule/AGENTS.md`
  - 主日程模块的工作规则

## 使用方式

1. 手工维护主看板：
   - `08_Operations/00_Master-Schedule/calendar.md`
   - `08_Operations/00_Master-Schedule/milestones.md`
2. 自动抽取项目中的日期节点：

```bash
python3 06_Infra/plugins/master-schedule/scripts/extract_timeline.py
```

默认输出：

- `08_Operations/00_Master-Schedule/auto-timeline.md`

## 时间投入记录

```bash
python3 06_Infra/plugins/master-schedule/scripts/time_tracking.py add \
  --entry "2026-03-03 09:30-11:00 MEMO 模板文档收口"

python3 06_Infra/plugins/master-schedule/scripts/time_tracking.py report
```

## 月视图页面

- 页面模板：`web/calendar-page.html`
- 页面样式：`web/calendar-page.css`
- 页面逻辑：`web/calendar-page.js`
- 数据源：`08_Operations/00_Master-Schedule/calendar-page-data.js`

刷新数据：

```bash
python3 06_Infra/plugins/master-schedule/scripts/build_month_calendar_feed.py \
  --calendar 08_Operations/00_Master-Schedule/calendar.md \
  --output 08_Operations/00_Master-Schedule/calendar-page-data.js
```

说明：

- `web/` 目录只放静态页面资源。
- 如果你要把页面发布到某个静态站点或个人网站，需要把 `web/` 下文件和生成出来的 `calendar-page-data.js` 放到同一个对外目录。

## Apple Calendar

生成 `.ics`：

```bash
python3 06_Infra/plugins/master-schedule/scripts/build_apple_calendar_ics.py \
  --calendar 08_Operations/00_Master-Schedule/calendar.md \
  --output 08_Operations/00_Master-Schedule/calendar.ics
```

直接同步到本机 Apple Calendar：

```bash
ME_ROUTING_MODE=by-type \
ME_WORK_CALENDAR=Work \
ME_PERSONAL_CALENDAR=Personal \
ME_EXPLORE_CALENDAR=Explore \
ME_INBOX_CALENDAR=Inbox \
ME_DRY_RUN=1 \
bash 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.sh
```

反向拉取手动事件：

```bash
ME_FROM_DATE=2026-01-01 \
ME_PULL_CALENDARS="Work,Personal,Explore,Inbox" \
bash 06_Infra/plugins/master-schedule/scripts/pull_apple_calendar_to_inbox.sh
```

双向一键联动：

```bash
bash 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar_bidirectional.sh
```

## Hooks

启用 git hooks：

```bash
bash 06_Infra/plugins/master-schedule/scripts/install_apple_calendar_hooks.sh
git config --local core.hooksPath .githooks
```

作用：

- `calendar.md` 在 commit / merge 后发生变化时，自动触发 Apple Calendar 同步脚本
- 默认可以通过 `ME_APPLE_SKIP_HOOK=1` 临时跳过

## 状态与留痕

- 受管日历状态：`state/apple-managed-calendars.txt`
- 运维留痕示例：`operations-log.md`

`operations-log.md` 是模板化记录样式，不包含任何私有部署路径；如果你在自己的环境里上线或回滚页面，可以按同样格式继续写。
