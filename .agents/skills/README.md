# MEMO Template Skills Map

这个目录是公开模板版 MEMO 的 skills 总入口。

模板当前的本地 skill 可以按 3 层理解：

1. 仓库级 skills：`/.agents/skills/`
2. 模块级 skills：`<module>/.agents/skills/`
3. 插件级 skills：`06_Infra/plugins/*/.agents/skills/` 或 `plugins/*/skills/`

## 仓库级

- `inbox-folder-archiver`
- `master-schedule-sync`
- `me-network-crm`
- `prism`
- `repo-indexing-memory`

## 模块级

- `08_Operations/.agents/skills/artifact-feedback-sync`
- `08_Operations/.agents/skills/meeting-transcript-refiner`

## 插件级

- `06_Infra/plugins/lark-bridge/.agents/skills/lark-bridge`
- `plugins/memo-audio-transcribe/skills/memo-audio-transcribe`

## 为什么模板的 skill 清单和私有仓不完全一样

- 公开模板优先考虑“起步就能跑的默认入口”
- 私有仓优先考虑“真源绑定在哪个模块”

所以模板里会刻意把某些能力提升成 repo-level 默认 skill，例如：

- `me-network-crm`
- `prism`

而私有仓里，这两者不一定都属于 repo root 下的本地真源 skill。

## 额外说明

- `plugins/*/skills/` 属于插件层，不等于 `.agents/skills/` 那一路径的发现机制
- `memo-audio-transcribe` 是 plugin layer，不是模板根级 `.agents/skills/` 目录中的 skill

## 经典 workflows

- `Inbox -> Stable Domain`
- `Task Intake -> Calendar -> Project`
- `Calendar -> Apple -> Back to Inbox`
- `Artifact -> Feedback -> Git Snapshot`
- `Transcript -> Polished Doc -> Minutes`
