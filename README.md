# MEMO

**Making Ephemeral Memories Objects**

An AI-native personal operating system template.

让转瞬即逝的记忆成为实体。

这个仓库是 MEMO 的 **公开模板源骨架**：保留当前已经稳定下来的目录语义、Agent workflows、脱敏示例、少量脚本闭环，以及可选插件扩展点。

如果你只看一眼就想知道它现在是什么，最准确的说法是：

**MEMO Template 不是单一 App，而是一套用 Markdown + Git 持有长期对象、用 Agent 与少量脚本辅助维护的个人记录协议模板。**

## 你可以用它做什么

用这套模板，你可以比较自然地把个人长期信息整理成一组稳定对象，而不是把一切都堆在一个笔记本里。

- 把临时输入导流到稳定位置，例如项目、资产、资源或日程
- 用项目对象承接目标、计划、认知、决策与执行痕迹
- 维护个人 CRM、阅读队列、结构化 profile 与运行面看板
- 让 Codex、Claude Code 这类 code agent 直接在本地仓库上工作
- 在 Markdown 真源之上叠加少量 skills、plugins 和脚本闭环

例如：

- 你把一堆会议记录、邮件摘录、网页片段先丢进 [`01_Inbox/`](./01_Inbox/)，再让 Agent 帮你归档到项目、资源或资产目录
- 你在 [`03_Goal-Projects/`](./03_Goal-Projects/) 里维护一个真实项目，把目标、计划、认知、决策和执行痕迹放在同一个对象下面
- 你在 [`05_Resources/network/`](./05_Resources/network/) 里维护联系人卡片和互动记录，而不是把人脉信息散落在聊天记录里
- 你在 [`08_Operations/00_Master-Schedule/`](./08_Operations/00_Master-Schedule/) 里维护主日程，再通过插件同步到 Apple Calendar
- 你让 Agent 直接读 README、AGENTS 和局部 skill，帮你解释仓库结构、整理材料、更新项目或刷新某条 workflow

## 它给用户带来什么价值

- **更容易长期积累**
  - 信息按对象归位，后续检索、引用、迁移和发布都更稳定
- **更容易让 Agent 真正帮你干活**
  - Agent 不只是“聊天”，而是可以围绕目录结构、真源文档和局部 workflow 直接执行
- **更容易从私人仓过渡到公开模板**
  - 私有真源、预发布模板和公开仓可以形成清楚的分层

## 快速开始

1. clone 或使用模板创建仓库
2. 推荐直接用 Codex、Claude Code 或同类 code agent 打开仓库，把它当作“可执行的个人记录协议模板”来探索
3. 先让 Agent 读 [`README.md`](./README.md)、[`00_Protocol/README.md`](./00_Protocol/README.md) 和 [`00_Protocol/AGENTS.md.template`](./00_Protocol/AGENTS.md.template)
4. 再读你最关心的内容域入口：
   - [`03_Goal-Projects/README.md`](./03_Goal-Projects/README.md)
   - [`05_Resources/network/index.md`](./05_Resources/network/index.md)
   - [`08_Operations/README.md`](./08_Operations/README.md)
5. 用 [`00_Protocol/AGENTS.md.template`](./00_Protocol/AGENTS.md.template) 生成你的仓库级 `AGENTS.md`
6. 可以先让 Agent 试跑一条简单 workflow，例如：

```text
阅读 README、00_Protocol/README.md、03_Goal-Projects/README.md，
然后解释这个仓库的顶层结构，并告诉我一个项目应该放在哪里。
```

7. 如需清掉示例数据，运行：

```bash
python3 06_Infra/cleanup_examples.py
```

如果你想要更空的起始骨架，也可以在检查完影响后使用：

```bash
python3 06_Infra/cleanup_examples.py --apply
```

## 当前最成熟的能力

模板当前最值得讲的 `stable` features 有 6 个：

1. 对象化目录骨架
2. TPCD 项目工作流
3. Personal CRM
4. Master Schedule
5. 结构化 Profile / Assets
6. Inbox Routing / Archiving

对应真源入口分别是：

- [`00_Protocol/README.md`](./00_Protocol/README.md)
- [`03_Goal-Projects/README.md`](./03_Goal-Projects/README.md)
- [`05_Resources/network/index.md`](./05_Resources/network/index.md)
- [`08_Operations/00_Master-Schedule/README.md`](./08_Operations/00_Master-Schedule/README.md)
- [`04_Assets/README.md`](./04_Assets/README.md)
- [`01_Inbox/README.md`](./01_Inbox/README.md)

## 顶层结构

```text
.
├── 00_Protocol/             # 全局契约、usage、privacy、schema
├── 01_Inbox/                # 输入缓冲层
├── 02_Desires/              # 上游驱动层
├── 03_Goal-Projects/        # 核心项目对象层（TPCD）
├── 04_Assets/               # 稳定存量层
├── 05_Resources/            # 外部杠杆层
├── 06_Infra/                # 脚本、插件、i18n、可选实验
├── 07_Principles/           # 跨项目裁决层
├── 08_Operations/           # 运行面、主看板、留痕
├── .agents/skills/          # 仓库级默认 skills
├── .agents/plugins/         # 本地插件市场配置
├── plugins/                 # 可选 Codex 本地插件
└── develop/                 # 模板自身的开发工作区
```

## 经典 workflows

模板当前最清楚的 5 条 classic workflows 是：

### 1. Inbox -> Stable Domain

- 上游：[`01_Inbox/`](./01_Inbox/)
- 入口 skill：[`inbox-folder-archiver`](./.agents/skills/inbox-folder-archiver/SKILL.md)
- 下游：[`03_Goal-Projects/`](./03_Goal-Projects/) / [`04_Assets/`](./04_Assets/) / [`05_Resources/`](./05_Resources/)

### 2. Task Intake -> Calendar -> Project

- 入口：[`08_Operations/00_Master-Schedule/`](./08_Operations/00_Master-Schedule/)
- 相关 skill：[`master-schedule-sync`](./.agents/skills/master-schedule-sync/SKILL.md)

### 3. Calendar -> Apple -> Back to Inbox

- 真源：[`08_Operations/00_Master-Schedule/calendar.md`](./08_Operations/00_Master-Schedule/calendar.md)
- 实现：[`06_Infra/plugins/master-schedule/`](./06_Infra/plugins/master-schedule/)

### 4. Network Input -> People Card / CRM Update

- 真源：[`05_Resources/network/index.md`](./05_Resources/network/index.md)
- 入口 skill：[`me-network-crm`](./.agents/skills/me-network-crm/SKILL.md)

### 5. Transcript -> Polished Doc -> Minutes

- 入口：[`08_Operations/.agents/skills/meeting-transcript-refiner`](./08_Operations/.agents/skills/meeting-transcript-refiner/SKILL.md)
- 可选插件：[`plugins/memo-audio-transcribe/`](./plugins/memo-audio-transcribe/)

## 这是什么，以及它怎么设计

MEMO Template 解决的不是“再给你一个笔记本”，而是：

- 如何把长期信息按对象归位
- 如何让 Agent 在本地仓库上稳定工作
- 如何把目录结构、文档真源、skills、少量脚本闭环接起来

它当前的核心立场是：

- **Protocol first**
  - 先定义对象和边界，再谈工具
- **Markdown source of truth**
  - Markdown / Git 持有长期真源
- **Agent-assisted, not agent-only**
  - Agent 是执行层，不替代真源结构
- **Search before summary**
  - 先看目录、README、AGENTS、局部真源，再总结

## 如果你想先看总览

- [`develop/docs/overview/memo-global-architecture-onepage-2026-03-12.md`](./develop/docs/overview/memo-global-architecture-onepage-2026-03-12.md)
  - 一页式全局架构图
- [`develop/docs/overview/memo-current-features-onepage-2026-04-03.md`](./develop/docs/overview/memo-current-features-onepage-2026-04-03.md)
  - 当前默认 features 与成熟度
- [`develop/docs/overview/memo-skills-map-2026-04-03.md`](./develop/docs/overview/memo-skills-map-2026-04-03.md)
  - skills 与经典 workflows 总览

## Skills 与可选扩展

仓库默认保留一组可被 Agent 直接消费的 skills：

- [`inbox-folder-archiver`](./.agents/skills/inbox-folder-archiver/SKILL.md)
- [`master-schedule-sync`](./.agents/skills/master-schedule-sync/SKILL.md)
- [`me-network-crm`](./.agents/skills/me-network-crm/SKILL.md)
- [`prism`](./.agents/skills/prism/SKILL.md)
- [`repo-indexing-memory`](./.agents/skills/repo-indexing-memory/SKILL.md)

模板也保留了几类 **可选扩展面**：

- 仓库内插件：
  - [`06_Infra/plugins/master-schedule/`](./06_Infra/plugins/master-schedule/)
  - [`06_Infra/plugins/lark-bridge/`](./06_Infra/plugins/lark-bridge/)
  - [`06_Infra/plugins/Google-Drive/`](./06_Infra/plugins/Google-Drive/)
- Codex 本地插件：
  - [`plugins/memo-audio-transcribe/`](./plugins/memo-audio-transcribe/)
  - [`.agents/plugins/marketplace.json`](./.agents/plugins/marketplace.json)

这些扩展的口径是：

- `master-schedule`：模板默认内置的运行面闭环
- `lark-bridge`：可选的 read-first Lark / Feishu bridge
- `Google-Drive`：可配置的本地云盘挂载 / 同步入口
- `memo-audio-transcribe`：可选的本地离线音频转写插件

## 模板边界

这个仓库是 **公开模板**，不是私有真源仓的完整镜像。

它保留的是：

- 当前稳定下来的结构语义
- 默认可复用的 workflows
- 脱敏示例
- 模板层的 skills / plugins / 脚本闭环

它不默认包含：

- 私有真源仓里的真实 profile / finance / network 数据
- 强依赖个人环境的专属 bridge 和上下文
- 尚未稳定的内部讨论材料

## 更适合什么，不适合什么

更适合：

- 需要长期、可迁移、可检索的个人记录结构
- 希望让 Code Agent 在本地仓库上工作
- 想把对象结构和工具能力分开维护

不适合：

- 只想要一个被动记事本
- 希望完全零结构、什么都往里堆
- 把仓库当作明文机密保险箱

## License

MIT
