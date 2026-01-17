# MEMO

**Making Ephemeral Memories Objects**

An AI-native personal operating system protocol.

让转瞬即逝的记忆成为实体。

> **我们选择记录什么，说明我们珍惜什么。**
> *What we choose to record reveals what we choose to value.*

---

## 这是什么

**MEMO** 是一个 **AI 原生的个人操作系统协议**——一套用于将转瞬即逝的记忆与经验，转化为可结构化、可版本化、可长期演化对象的方法论。

这个仓库是该协议的 **可分享模板**（中英双语），从私有 "Me repo" 中提炼而来。

**特点**：Markdown-first · Git 版本化 · 全文检索优先 · 低维护成本

---

## 为什么需要 MEMO

### 第一层：记录人生记忆本身的意义

人生不是由事件堆叠而成，而是由 **被记住、被反复回看的片段** 塑造的。

> **记忆不是存档，记忆是选择，记忆是对"什么重要"的持续确认。**

通过把人生中的想法、关系、决定、反思转化为 **Objects**，你能够：

- 反复回看自己是如何走到今天的
- 理解当下的决定从何而来
- 在时间中建立连续的「自我感」

这不是记录生活，而是 **构建一个可回溯、可复盘的人生模型**。

### 第二层：在 AI Memory 时代，MEMO 作为「协议」的意义

日记工具很多，AI 产品也都有自己的 Memory 功能。真正的问题是：

> **谁拥有记忆？记忆是否可控？是否可迁移？是否可组合？**

现状是 **数据封建割据**：ChatGPT Memory 只给 GPT 用，Claude Project 只给 Claude 用，你的人生碎片被锁在不同的「围墙花园」里。

#### MEMO 的立场：Protocol First, Agent Agnostic

> **MEMO 不做你人生的「应用」，MEMO 做你人生的「文件系统」。**

应用会死、会涨价、会倒闭。文件系统是永恒的。

| 维度 | 传统工具 / AI Memory | **MEMO 协议** |
|------|----------------------|---------------|
| **所有权** | 平台拥有 | ✅ 你完全拥有（本地 Git） |
| **格式** | 私有格式 | ✅ 纯 Markdown（永不过时） |
| **模型绑定** | 锁定单一 AI | ✅ 随时 export 给任意 AI |
| **管理方式** | 只能用官方 App | ✅ 任意 Code Agent 管理 |
| **来源整合** | 单一来源 | ✅ 整合任意人生碎片 |

**核心架构**：把 **数据存储（Storage）** 和 **智能处理（Intelligence）** 彻底分家。

```
任意人生碎片 → MEMO（本地 Git） → 任意 AI / Code Agent
         ↑                              ↓
    你完全控制所有权              模型只是可替换的 CPU
```

今天 DeepSeek 便宜好用，让它整理；明天 GPT-6 出来，不需要迁移数据，直接接进来读你的 Git 仓库。

#### Code Agent 是「园丁」而非「助理」

普通 Chat Agent 只会 **Append（追加）**：聊完存下来，记忆是线性堆叠的流水账。

Code Agent 能做 **Refactor（重构）**：

- 遍历你的 Git 仓库
- 把散落在不同日期的「创业想法」碎片
- 自动提取、合并成一篇 `03_Goal-Projects/active/<project>/README.md`
- 提交一个 PR 给你

人生记忆不应该只是 Log，而应该是 **可演化的 Knowledge Graph**。

#### RAG for Life：对抗记忆美化与遗忘

当你面临「要不要离职读博」这个决策时：

- **普通日记**：自己翻两年前的日记，看当时为什么工作
- **MEMO**：AI 自动调出你过去相关的项目对象（例如 `03_Goal-Projects/active/<project>/README.md`），对比多段认知笔记与互动记录，生成一份可复盘的分析与行动清单

这不仅是搜索，是 **诚实地面对过去的自己**。

### 一句话总结

> **MEMO 的意义，不是帮你记住人生，而是让你拥有、迁移、复用、推理自己的人生记忆。**

**你在记录的同时，也在不断复盘；你在复盘的同时，也在塑造未来的自己。**

---

## 核心理念

### 记忆是选择，不是存储

大多数系统解决的是「存储」问题——能不能记下来、存得多、搜得到。

**MEMO 关注的是另一个问题**：

> 什么值得被转化为一个长期存在的对象？

如果一条内容无法被对象化，它就不属于 MEMO。

### ME + MO

完整的个人记录，必须同时包含「自我」与「连接」：

| 维度 | 含义 |
|------|------|
| **ME** | 内在状态、偏好、目标、身份锚点 |
| **MO** | Others（他人）、Mode（交互模式）、Model（使用的模型） |

人是社会性动物，**自我是通过与世界的连接被塑造的**。

---

## 目录结构

```text
.
├── 00_Protocol/             # 协议层：schemas + usage/privacy + templates
├── 01_Inbox/                # Ephemeral 区：临时捕获，每周清理
├── 02_Desires/              # 上游驱动：欲望/偏好/价值观/非目标
├── 03_Goal-Projects/        # 目标与项目：Target / Plan / Cognition / Decision（行动）
├── 04_Assets/               # Assets（资产）：你"拥有"的、已确权的存量（ME）
├── 05_Resources/            # Resources（资源）：可调用的外部杠杆（MO）
└── 06_Infra/                # 基础设施（可选）：脚本/一键工具等
```

> 说明：仓库结构会持续迭代；当本文档与实际目录不一致时，以仓库当前目录结构为准。

### Assets vs Resources

| 维度 | **Assets（资产）** | **Resources（资源）** |
|------|---------------------|------------------------|
| **问题** | What I **HAVE** | What I can **USE** |
| **特点** | 稳定，"秀肌肉"用的 | 需维护，可能过期 |
| **示例** | 简历、作品集、技能 | 人脉、API Key、场地 |

**转化公式**：`Resource + Action = Asset`

### Projects 结构

每个项目遵循 **Target / Plan / Cognition / Decision** 四象限：

```text
03_Goal-Projects/active/项目名/
├── README.md                # Target（目标是什么、为什么）
├── PLAN.md                  # Plan（执行计划）
├── cognition/               # 思考过程、认知笔记
└── decisions/               # ADR 式决策记录
```

---

## 快速开始

1. **Fork / Clone / Use as template**
2. （可选）如果你希望从“空骨架”开始：`python3 06_Infra/cleanup_examples.py --apply`（归档可恢复）
3. 推荐用 Code Agent 的 `/init` 在仓库根目录生成 `AGENTS.md`（AI-native 工作方式）
4. 先用 `rg`（ripgrep）全文检索跑起来，痛点明确再加工具
5. 从 `01_Inbox/` 开始，每周将碎片对象化或删除

```bash
# 搜索示例
rg -n "关键词" 05_Resources/network/people
rg -n "#resource/intro" 05_Resources/network/people
```

### AI Native（推荐）

- 使用 `/init` 生成的 `AGENTS.md` 来约束 Agent 的工作方式（目录边界、命名约定、安全底线、常用自检）。
- 推荐以 `00_Protocol/AGENTS.md.template` 作为起点：它强调 `00_Protocol/` 只定义“协议/对象/规则”，可执行的 skills 与脚本应放在 `06_Infra/`。

### 多语言（可选）

可以用 `06_Infra/i18n/` 一键切换 README / prompts / skills /（部分模板与示例）的文档语言：

- 列出语言：`python3 06_Infra/i18n/switch_language.py --list`
- 切到中文：`python3 06_Infra/i18n/switch_language.py --lang zh --apply --backup`
- 切到英文：`python3 06_Infra/i18n/switch_language.py --lang en --apply --backup`

### 清理示例（可选）

本仓库默认包含少量**脱敏示例**（例如：people card / projects / desires / profile），用于演示写法与结构。你可以一键归档清理，之后随时恢复：

- 预览（dry-run）：`python3 06_Infra/cleanup_examples.py`
- 执行清理（归档可恢复）：`python3 06_Infra/cleanup_examples.py --apply`
- 查看归档：`python3 06_Infra/cleanup_examples.py --list-archives`
- 恢复归档：`python3 06_Infra/cleanup_examples.py --restore <timestamp> --apply`（必要时加 `--force`）

---

## 这不是什么

MEMO **明确不做**：

- ❌ 被动的笔记堆积系统
- ❌ 什么都收的日志仓库
- ❌ 社交网络
- ❌ 纯情绪宣泄型日记
- ❌ 效率追踪生产力工具

---

## 哲学立场

用 Git、Markdown、版本控制等理性工具，去维护记忆、关系与人生片段。

> **愿意为重要之物建立系统，本身就是一种温柔的理性。**
> 因为足够在意，才不愿意让它们随意流失。

---

## 核心工作流

| 工作流 | 入口文件 | 用途/节奏 |
|--------|----------|-----------|
| 上游驱动（Desires） | [`02_Desires/README.md`](02_Desires/README.md) | 每月/每季度复查“我在乎什么” |
| 碎片输入（Inbox） | [`01_Inbox/README.md`](01_Inbox/README.md) | 每周清理：对象化或删除 |
| 人脉管理（Personal CRM） | [`05_Resources/network/index.md`](05_Resources/network/index.md) | 需要找人/做引荐时 |
| 项目管理（TPCD） | [`03_Goal-Projects/README.md`](03_Goal-Projects/README.md) | 每个目标一个项目目录 |
| 使用说明 | [`00_Protocol/USAGE.md`](00_Protocol/USAGE.md) | 上手与约定入口 |
| 隐私基线 | [`00_Protocol/PRIVACY.md`](00_Protocol/PRIVACY.md) | 发布前必读 |

---

## License

MIT

---

<p align="center">
  <strong>MEMO</strong><br/>
  <em>Making Ephemeral Memories Objects</em>
</p>
