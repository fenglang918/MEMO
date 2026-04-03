# MEMO Template Skills Map

日期：2026-04-03  
用途：把公开模板当前已保留的 skills 和 classic workflows 压成一页图

## 结论

公开模板里的 skills 不是零散附赠物，而是几条经典 workflow 的可执行入口。

模板当前最值得讲清楚的 workflow 有 5 条：

1. Inbox -> Stable Domain
2. Task Intake -> Calendar -> Project
3. Calendar -> Apple -> Back to Inbox
4. Artifact -> Feedback -> Git Snapshot
5. Transcript -> Polished Doc -> Minutes

## Skill Layers

| 层级 | 路径 | 适合放什么 | 代表 skill |
| --- | --- | --- | --- |
| 仓库级 | `.agents/skills/` | 跨模块、模板默认 workflow | `inbox-folder-archiver` `master-schedule-sync` `me-network-crm` `prism` |
| 模块级 | `<module>/.agents/skills/` | 强绑定某个内容域的工作流 | `artifact-feedback-sync` `meeting-transcript-refiner` |
| 插件级 | `06_Infra/plugins/*/.agents/skills/` 或 `plugins/*/skills/` | bridge、插件能力、外部系统接入 | `lark-bridge` `memo-audio-transcribe` |

## 当前口径说明

公开模板里的 skill 清单，不要求和私有真源仓 1:1 一致。

模板会故意把一部分高频 workflow 提升成 repo-level 默认入口，例如：

- `me-network-crm`
- `prism`

目的不是声称“私有仓也是这么组织的”，而是降低模板用户的起步摩擦。

同时需要区分：

- `.agents/skills/`
  - 模板默认 skills
- `plugins/*/skills/`
  - 插件层 skills，例如 `memo-audio-transcribe`

## Classic Workflows

### 1. Inbox -> Stable Domain

- 入口 skill：`inbox-folder-archiver`
- 上游真源：`01_Inbox/`
- 下游稳定域：`03_Goal-Projects/` / `04_Assets/` / `05_Resources/`

### 2. Task Intake -> Calendar -> Project

- 入口：`08_Operations/00_Master-Schedule/`
- 相关 skill：`master-schedule-sync`

### 3. Calendar -> Apple -> Back to Inbox

- 真源：`08_Operations/00_Master-Schedule/calendar.md`
- 入口 skill：`master-schedule-sync`

### 4. Artifact -> Feedback -> Git Snapshot

- 入口 skill：`08_Operations/.agents/skills/artifact-feedback-sync`

### 5. Transcript -> Polished Doc -> Minutes

- 入口 skill：`08_Operations/.agents/skills/meeting-transcript-refiner`
