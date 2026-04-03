# Master Schedule

这个目录是跨项目的时间中枢：只放“时间决策信息”，不复制项目细节。

## 文件说明

- `calendar.md`：按月关键节点总览（手工维护）
- `milestones.md`：跨项目里程碑清单（手工维护）
- `weekly.md`：本周推进视图（手工维护）
- `inbox.md`：临时时间项收集（待归档）
- `auto-timeline.md`：自动抽取视图（脚本生成）
- `calendar-page-data.js`：月视图页面的数据源（由脚本生成）
- `calendar.ics`：Apple Calendar 可导入文件（由脚本生成）
- `decision-principles-time-value-and-autonomy.md`：旧链接兼容指针

## 维护规则

1. 每条节点都尽量附来源链接（指向原项目文件、Inbox 条目或相关原则）。
2. `calendar.md` 只保留真正需要盯的节点，避免过载。
3. 自动抽取仅作辅助，最终以手工看板为准。

## 最短闭环

1. 在 `calendar.md` 放入你真正承诺要推进的节点
2. 用 `weekly.md` 做本周收敛
3. 运行脚本刷新 `auto-timeline.md` 或 `calendar-page-data.js`
4. 如需 Apple Calendar，同步到本机日历

## Local Skills / Agent 入口

- `AGENTS.md`
  - 模块级工作规则与读写顺序
- `../../.agents/skills/master-schedule-sync/SKILL.md`
  - repo-level 日程同步入口

## 页面与导出

月视图页面的数据来源是 `calendar.md`：

```bash
python3 06_Infra/plugins/master-schedule/scripts/build_month_calendar_feed.py \
  --calendar 08_Operations/00_Master-Schedule/calendar.md \
  --output 08_Operations/00_Master-Schedule/calendar-page-data.js
```

Apple Calendar 可导入文件：

```bash
python3 06_Infra/plugins/master-schedule/scripts/build_apple_calendar_ics.py \
  --calendar 08_Operations/00_Master-Schedule/calendar.md \
  --output 08_Operations/00_Master-Schedule/calendar.ics
```

## Apple Calendar 直接同步

```bash
python3 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.py \
  --calendar 08_Operations/00_Master-Schedule/calendar.md \
  --routing-mode by-type \
  --work-calendar "Work" \
  --personal-calendar "Personal" \
  --explore-calendar "Explore" \
  --inbox-calendar "Inbox" \
  --from-date 2026-01-01
```

推荐先 dry-run：

```bash
ME_DRY_RUN=1 bash 06_Infra/plugins/master-schedule/scripts/sync_apple_calendar.sh
```

如需在 `calendar.md` 变更后自动触发同步，可启用：

```bash
bash 06_Infra/plugins/master-schedule/scripts/install_apple_calendar_hooks.sh
git config --local core.hooksPath .githooks
```

## Apple Calendar 反向拉取

把 Apple Calendar 中手工新增的事件回流到 `inbox.md`：

```bash
python3 06_Infra/plugins/master-schedule/scripts/pull_apple_calendar_to_inbox.py \
  --inbox 08_Operations/00_Master-Schedule/inbox.md \
  --calendars "Work,Personal,Explore,Inbox" \
  --from-date 2026-01-01
```

## Inbox -> Calendar -> Project SOP

1. 在 `01_Inbox/` 或 `inbox.md` 里快速收集事项
2. 当它变成明确时间节点时，迁入 `calendar.md`
3. 当它形成持续推进主题时，再建立 `03_Goal-Projects/YYYY/MM/<project>/`
4. 用来源链接把时间节点回链到项目或 Inbox

## 相关入口

- 插件与脚本：`../../06_Infra/plugins/master-schedule/README.md`
- Agent skill：`../../.agents/skills/master-schedule-sync/SKILL.md`
- 时间投入记录：`../01_Time-Tracking/README.md`
- 项目管理入口：`../../03_Goal-Projects/README.md`
