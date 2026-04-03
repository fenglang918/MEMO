# Operations

本目录放“系统在运行中”的内容，而不是目标本身。

典型用途：

- 日程与时间安排
- 时间追踪与运营记录
- 设备 / 环境配置
- 周期性维护清单

一个简单判断：

- 如果它回答的是“我要做什么目标”，更可能属于 `03_Goal-Projects/`
- 如果它回答的是“这个系统怎么持续运转”，更可能属于 `08_Operations/`

## 模块入口

- [`00_Master-Schedule/`](./00_Master-Schedule/)：跨项目日程中枢；维护 `calendar.md`、`weekly.md`、`milestones.md`
- [`01_Time-Tracking/`](./01_Time-Tracking/)：时间投入记录与周报
- [`Mac-Setup/`](./Mac-Setup/)：设备 / 环境初始化 checklist

## 作为运行面 feature 看，这里有什么

这一层不是“杂项目录”，而是模板里几条已经成型的运行面 workflow 集合：

1. `Inbox Routing / Archiving`
   - 原始输入先进入 `01_Inbox/`
   - 再按内容意图导流到 `03_Goal-Projects/`、`04_Assets/`、`05_Resources/`
   - 对应 skill：`../.agents/skills/inbox-folder-archiver/`

2. `Master Schedule`
   - 真源：`00_Master-Schedule/calendar.md`
   - 配套产物：`auto-timeline.md`、`calendar-page-data.js`、`calendar.ics`
   - 外部联动：Apple Calendar push / pull / bidirectional sync
   - 对应 skill：`../.agents/skills/master-schedule-sync/`

3. `Task Intake -> Calendar -> Project`
   - 原始输入进入 `01_Inbox/`
   - 任务抽取后进入 `00_Master-Schedule/inbox.md` / `calendar.md`
   - 形成持续主题时再升级到 `03_Goal-Projects/`

4. `Artifact Feedback Sync`
   - 给 deliverable 保留 raw dialogue、feedback log、artifact index 和 git snapshot
   - 对应 skill：`./.agents/skills/artifact-feedback-sync/`

5. `Meeting Transcript Refiner`
   - 把 `.srt/.vtt/.txt` 转成完整润色稿和结构化会议纪要
   - 对应 skill：`./.agents/skills/meeting-transcript-refiner/`

## Local Skills / Agent 入口

- [`../.agents/skills/inbox-folder-archiver/SKILL.md`](../.agents/skills/inbox-folder-archiver/SKILL.md)
- [`../.agents/skills/master-schedule-sync/SKILL.md`](../.agents/skills/master-schedule-sync/SKILL.md)
- [`./.agents/skills/artifact-feedback-sync/SKILL.md`](./.agents/skills/artifact-feedback-sync/SKILL.md)
- [`./.agents/skills/meeting-transcript-refiner/SKILL.md`](./.agents/skills/meeting-transcript-refiner/SKILL.md)

## 推荐阅读顺序

1. 先看 [`00_Master-Schedule/README.md`](./00_Master-Schedule/README.md) 了解总日程的手工主看板与脚本链路
2. 再看 [`01_Time-Tracking/README.md`](./01_Time-Tracking/README.md) 了解时间投入记录
3. 最后按需看 [`Mac-Setup/README.md`](./Mac-Setup/README.md)

## 模板内置示例

本模板额外提供一组脱敏示例：

- `00_Master-Schedule/calendar.md`
- `00_Master-Schedule/milestones.md`
- `00_Master-Schedule/inbox.md`
- `00_Master-Schedule/auto-timeline.md`
- `01_Time-Tracking/time_entries.csv`
- `01_Time-Tracking/reports/latest.md`

如果你想从更空的骨架开始，可运行：

```bash
python3 06_Infra/cleanup_examples.py
```

这些示例会被清理，但目录结构与 README 会保留。

## 可选本地 Skills

`08_Operations/.agents/skills/` 里还保留了两类更偏运行面的本地技能：

- `artifact-feedback-sync`
  - 用于给任意 deliverable 保留反馈闭环、双向索引和 git 快照
- `meeting-transcript-refiner`
  - 用于把 `.srt/.vtt/.txt` 转成完整润色稿与结构化会议纪要

它们不是每个模板用户都会默认启用，但属于公开模板保留的可复用运行面工作流。

## 推荐 workflows

如果按“什么时候该来 `08_Operations/`”看，当前最典型的是下面 5 条：

### 1. Inbox -> Stable Domain

适用场景：

- 你刚拿到截图、SRT、录音转写、资料包、临时笔记，还没决定它们应该归到哪里
- 你已经知道这些内容不能永久停留在 `01_Inbox/`

最短路径：

1. 原始材料先进入 `01_Inbox/`
2. 判断它更像：
   - `03_Goal-Projects/`：活跃项目过程材料
   - `04_Assets/`：稳定个人事实或长期拥有记录
   - `05_Resources/`：可复用资源、外部参考、联系人、案例
3. 保留 raw source，并补结构化输出
4. 在目标域更新上游索引

对应 skill：

- `../.agents/skills/inbox-folder-archiver/`

### 2. Task Intake -> Calendar -> Project

适用场景：

- 你手上有一堆零散任务、聊天记录、会议后待办，还没决定它们该归哪
- 你想先把任务收束进时间系统，再决定是否升级成正式项目

最短路径：

1. 原始输入先进入 `01_Inbox/`
2. 时间项收束到 `00_Master-Schedule/inbox.md` 或 `calendar.md`
3. 如果形成持续主题，再升级到 `03_Goal-Projects/`

### 3. Calendar -> Apple -> Back to Inbox

适用场景：

- 你已经在 `calendar.md` 里维护时间节点
- 你想把这些节点同步到 Apple Calendar，或把手动新增事件回拉

主真源：

- `00_Master-Schedule/calendar.md`

对应 skill：

- `../.agents/skills/master-schedule-sync/`

### 4. Artifact -> Feedback -> Git Snapshot

适用场景：

- 某个 proposal、文档、交付物正在被 review
- 你不想让反馈记录、发送版本和最终产物脱节

对应 skill：

- `./.agents/skills/artifact-feedback-sync/`

### 5. Transcript -> Polished Doc -> Minutes

适用场景：

- 你拿到 `.srt`、`.vtt`、`.txt` 转录稿
- 你既想保留完整信息，又想得到可执行会议纪要

对应 skill：

- `./.agents/skills/meeting-transcript-refiner/`
