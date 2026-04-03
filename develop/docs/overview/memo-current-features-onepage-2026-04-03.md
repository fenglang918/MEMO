# MEMO Template 当前 Features（一页式）

日期：2026-04-03  
用途：快速说明公开模板版 MEMO 现在默认“能做什么”  
口径：只基于 `pre-publish/repo` 当前真实存在的目录、脚本、skills 与示例，不把私有仓专属能力或理想化方向当成已交付 feature

## 先说结论

**MEMO Template 当前最清楚的能力，不是“一个统一前台 App”，而是一套由 Markdown 真源骨架 + Agent 工作流 + 少量脚本组成的可执行模板。**

它现在已经有：

- 稳定的对象化目录骨架
- 可复用的项目 / 人脉 / 日程工作流
- 少量可直接运行的脚本闭环
- 一组可被 Agent 消费的本地 skills

它现在还没有：

- 单一统一前台
- 私有仓那类更强的外部 bridge 全量默认接入
- 把所有实验能力打磨到同一成熟度

---

## 状态标记

- `stable`：已经是模板默认骨架的一部分，真源和示例都在仓库内
- `usable`：已经能用，但更像工具层 / 进阶工作流，不是每个模板使用者都会默认启用
- `experimental`：明确存在，但当前不是默认依赖或日常推荐入口

---

## Feature Map

| Feature | 状态 | 当前能做什么 | 典型输入 → 输出 | 真源 / 入口 |
| --------------------- | -------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| 对象化知识底座 | `stable` | 把长期信息按对象归位，而不是堆成无结构日志 | `Inbox/想法/对话/截图` → 归位到 `Projects / Resources / Assets / Principles` | `README.md`、`00_Protocol/README.md` |
| TPCD 项目工作流 | `stable` | 用 `Target / Plan / Cognition / Decision` 组织复杂项目和决策 | 一个长期目标/复杂问题 → 项目目录 + 认知演进 + ADR | `03_Goal-Projects/README.md` |
| Personal CRM | `stable` | 给人建立长期卡片、标签、互动记录与跟进线索 | “刚认识某人”“帮我找某类人” → 人物卡 / 检索 / 跟进线索 | `05_Resources/network/index.md` |
| Master Schedule | `stable` | 在 Markdown 中维护主日程，并生成月视图 / ICS / Apple Calendar 同步链路 | `calendar.md / inbox.md` → 月视图数据 / ICS / 日历同步 | `08_Operations/00_Master-Schedule/README.md`、`06_Infra/plugins/master-schedule/` |
| 结构化 Profile / Assets | `stable` | 管理 profile、timeline、values、resume 等稳定存量 | 内部资料更新 → profile / export / 公开材料骨架 | `04_Assets/README.md`、`04_Assets/profile/` |
| Inbox Routing / Archiving | `stable` | 把临时输入从 `01_Inbox/` 导流到稳定域，并保留 raw source、结构化输出与回链 | `截图 / 资料包 / 转录 / 临时文件夹` → `Projects / Assets / Resources` 中的稳定记录 | `01_Inbox/README.md`、`.agents/skills/inbox-folder-archiver/` |
| Agent Skills 工作流 | `usable` | 把常见仓库动作封成 skill，减少每次重写 prompt 与手工步骤 | “归档 Inbox”“同步主日程”“维护 pins” → 由 skill 驱动的标准流程 | `.agents/skills/` |
| Lark Bridge | `usable` | 通过本机 `lark-cli` 从同一工作区查询 docs / chats / messages / mail / calendar / contacts | 本机已登录 Lark CLI → read-first 查询结果 | `06_Infra/plugins/lark-bridge/` |
| Cloud Sync Mount | `usable` | 通过本地云盘客户端，把 `sync-dir/` 配成跨设备同步入口 | 本地大文件 / 临时资料包 → 云盘同步目录 | `06_Infra/plugins/Google-Drive/` |
| Offline Audio Transcribe Plugin | `usable` | 把本地音频离线转成 transcript 并写入 `01_Inbox/` | `mp3 / m4a / wav` → `transcript.md / transcript.txt / segments.v1.jsonl` | `plugins/memo-audio-transcribe/`、`.agents/plugins/marketplace.json` |
| i18n 语言切换 | `usable` | 提供模板内容的 zh / en 语言包与切换脚本 | 默认中文或英文语料 → 对应 langpack 版本 | `06_Infra/i18n/` |
| 示例清理 | `usable` | 把模板里的内置示例项目和示例数据清理掉，保留骨架 | 模板仓初始化 → 更空的结构骨架 | `06_Infra/cleanup_examples.py` |
| Repo concept indexing | `experimental` | 提供 concept → evidence 索引实验与 link-check 思路 | 明确要求刷新实验 → 索引产物 / 校验报告 | `06_Infra/indexing/` |

---

## 最值得讲清楚的 5 个 Feature

### 1. TPCD 项目工作流

这是模板当前最核心的 feature。

- 它解决的不是待办管理，而是“长期复杂问题怎么留下完整认知链”
- 强项是：
  - `README.md` 管目标
  - `PLAN.md` 管推进
  - `cognition/` 管认知演进
  - `decisions/` 管 ADR

真源：

- `03_Goal-Projects/README.md`

### 2. Personal CRM

这不是联系人列表，而是一个对象化的人脉资源层。

- 每个人有独立卡片
- 可按标签、关系、资源、领域检索
- 可与项目文档互相引用，形成“项目 - 人 - 决策”联动

真源：

- `05_Resources/network/index.md`

### 3. Master Schedule

这是模板里最成熟的“文档层 + 脚本层”闭环 feature。

- Markdown 是真源
- `calendar-page-data.js`、ICS 和 Apple Calendar 同步是派生产物
- 同时保留 `calendar.md`、`weekly.md`、`inbox.md` 三种不同粒度

真源：

- `08_Operations/00_Master-Schedule/calendar.md`
- `08_Operations/00_Master-Schedule/inbox.md`

实现入口：

- `06_Infra/plugins/master-schedule/`
- `.agents/skills/master-schedule-sync/`

### 4. Inbox Routing / Archiving

这是模板运行面的最上游能力之一。

- 原始输入先落到 `01_Inbox/`
- 如果已经足够清楚，就导流到稳定域
- 如果还不够清楚，可以先转成任务、讨论缓冲，或继续保留 raw source
- 它解决的是“怎么不丢东西地把现实输入编译成稳定对象”

真源：

- `01_Inbox/README.md`

实现入口：

- `.agents/skills/inbox-folder-archiver/`

### 5. Agent Skills

模板不是只靠 README 教人手工维护。

当前已经有一批可执行的本地 skill 入口，例如：

- `inbox-folder-archiver`
- `master-schedule-sync`
- `me-network-crm`
- `prism`

这意味着模板已经把部分仓库动作标准化给 Agent 使用，而不只是保留空目录。

### 6. 可选插件扩展

模板现在不只有 skills，也开始保留“可选插件层”。

- `06_Infra/plugins/lark-bridge/` 是仓库内 read-first bridge
- `06_Infra/plugins/Google-Drive/` 是可配置的云盘挂载 / 同步入口
- `plugins/memo-audio-transcribe/` 是 Codex 本地插件示例
- `.agents/plugins/marketplace.json` 提供插件市场入口

这类能力不是所有用户都会默认启用，但它们已经属于模板公开保留的扩展面，而不是只存在于私有仓。

### 7. 示例清理与语言切换

这是模板属性本身的重要 feature。

- `cleanup_examples.py` 负责把内置示例清掉
- `06_Infra/i18n/` 负责中英文模板版本

它们不直接面向“知识对象”，但直接决定这个模板是否真能被别人拿来起步。

---

## 当前不应被误讲成“已成熟产品 feature”的部分

### 1. Indexing

`06_Infra/indexing/` 还在，但当前明确是：

- 历史实验保留
- `experimental`
- 不是默认导航机制

### 2. 统一对话前台

模板默认前提仍然是：

- 仓库真源
- 编辑器
- Agent / scripts

而不是一个已经完成整合的统一产品前台。

### 3. 私有专用桥接能力

公开模板现在已经包含 `lark-bridge` 和本地转录插件示例，但私有真源仓里更强、更多、或依赖私有环境的桥接能力，仍不应被误讲成公开模板默认 feature。

---

## 最适合对外介绍模板的说法

如果只讲当前最硬的 feature，可以压成下面这版：

> MEMO Template 现在最成熟的能力有五个：  
>
> 1. 用 TPCD 管长期项目和决策链；  
> 2. 用 Markdown + Agent 管个人 CRM；  
> 3. 用 Master Schedule 维护主时间看板并生成日历产物；  
> 4. 用本地 skills 把常见仓库动作标准化；  
> 5. 用示例清理和 i18n 机制，把模板变成可分发的起始骨架。  
>
> 它今天已经是一套可执行的个人记录协议模板，但还不是统一前台产品。
