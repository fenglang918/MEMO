# Inbox / 临时收集

`01_Inbox/` 是模板里的输入缓冲层，用来承接尚未归位的现实输入。

建议入口：

- 结构化讨论流转：[`discussion/README.md`](discussion/README.md)
- 任务盘点与临时收口：[`任务梳理.md`](任务梳理.md)
- 导流与归档：[`../.agents/skills/inbox-folder-archiver/SKILL.md`](../.agents/skills/inbox-folder-archiver/SKILL.md)

当前这里允许混杂：

- 截图、SRT、图片、配置片段等原始输入
- 尚未归档到 `03_Goal-Projects/` / `04_Assets/` / `05_Resources/` 的半成品材料
- 模板化保留时，也可放在 `raw/` 与 `processed/` 这类中间态目录

原则上：

- 先落地
- 先记录事实
- 再决定是否对象化和归档

## AI Native（重点）

在 MEMO 的工作方式里，你不一定需要先把“截图 / 聊天记录”手工落盘成一套固定 raw 结构。

更常见的流程是：**直接把截图、对话上下文或文件交给 Code Agent**，让它端到端完成整理、提炼与对象化，然后只把结构化结果写入仓库。

当你确实想保留原始材料作为证据 / 回溯时，再把文件放入 `01_Inbox/` 并在后续完成归档。

## 常见导流方向

如果一个 Inbox 输入已经足够清楚，通常会被导流到下面几类稳定域：

- `03_Goal-Projects/`
  - 活跃项目、决策过程、交付过程材料
- `04_Assets/`
  - 稳定个人事实、长期拥有记录、结构化 profile / exports
- `05_Resources/`
  - 可复用资源、参考材料、案例、联系人、工具信息

如果还不够清楚：

- 可以继续留在 `01_Inbox/`
- 或先只抽任务进入 `08_Operations/00_Master-Schedule/inbox.md`

## 典型流程

### 1. Raw Input -> Stable Domain

适用于：

- 资料包、截图集合、转录结果、临时收集文件夹

对应 skill：

- `../.agents/skills/inbox-folder-archiver/`

### 2. Raw Input -> Task / Calendar

适用于：

- 输入里主要是待办、时间节点、后续动作

下一跳：

- `../08_Operations/00_Master-Schedule/inbox.md`
- `../08_Operations/00_Master-Schedule/calendar.md`
- `../08_Operations/00_Master-Schedule/AGENTS.md`
- `../.agents/skills/master-schedule-sync/SKILL.md`

### 3. Raw Input -> Discussion Buffer

适用于：

- 还不适合直接对象化，但值得保留讨论上下文的内容

下一跳：

- `discussion/README.md`

## 模板骨架说明

- `raw/`
  - 放需要保留回溯证据的原始材料
- `processed/`
  - 放已经处理过、但尚未完全导流到稳定域的中间态

公开模板保留这两个目录，是为了给“想先保留文件”的用户一个最小骨架；并不表示所有 AI-native workflow 都必须先落这里。
