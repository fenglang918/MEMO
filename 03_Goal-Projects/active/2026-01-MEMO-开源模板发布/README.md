# MEMO 开源模板（示例项目 / Target）

> 说明：这是一个脱敏后的示例项目，用于演示“如何把一个真实目标落到 TPCD”。请把其中的“我们/作者”理解为占位叙事，而不是具体个人信息。

## 目标（What）

发布一个中英双语的 **MEMO 仓库模板**：把“人生 memory 的管理方式”抽象成可复用的结构与协议（files + conventions + templates + optional scripts）。

## 为什么（Why）

- 人生记录的价值在于“可检索、可复盘、可行动”，但多数工具会绑定平台或导致多份副本漂移。
- 我们无法也不打算提供自动化数据源/产品化 LLM API；开源的意义是提供一套 vendor-neutral 的协议与方法，让用户用自己的信息源和 AI 工具来“编译”记忆。
- 长期目标是：输入随意（聊天/报告/网页/截图），输出稳定（People/Events/Projects/Signals/索引），把碎片沉淀成可迁移的个人记忆资产。

## 关键结果（KRs）

1. 模板仓库作为一个可独立使用的 repo 具备“开箱即用”能力（README/隐私基线/用法/模板/示例），并能在需要时对外发布。
2. 明确“协议化输出”的对象模型与最小字段（先从 people cards / projects 开始）。
3. 给出最小可行的本地工作流（search-first + optional CLI），并有 1–2 个可跑通的示例。

## 约束与边界

- 预算：0（只用本地文件 + Git；AI 工具由用户自选）
- 时间：先做 MVP（可用、可解释、可扩展），再迭代协议细节
- 不可妥协项：不放可直接滥用的明文机密（账号密码、API keys、私钥等）
- 可妥协项：自动化程度、可视化、跨平台集成（都放到后续）

## 本项目的“产出物”在仓库哪里

这不是一个“写一篇文章”的项目，而是一个“把协议与工作流落地成 repo 结构”的项目。核心产出分布在：

- Repo 宣言与使用入口：`README.md`
- 协议层（对象/规则/使用说明）：`00_Protocol/`
- 人脉库（People cards + 设计文档 + 可选 CLI）：`05_Resources/network/`
- PRISM ingest prompt（可复制给任意 AI）：`06_Infra/skills/portable/prism.md`
- 核心 native skill（维护人脉库端到端）：`06_Infra/skills/native/me-network-crm/SKILL.md`
- 双语切换（一键覆盖 README/skills/prompt）：`06_Infra/i18n/switch_language.py`
- AI-native 初始化（建议用 `/init` 生成 AGENTS）：`00_Protocol/AGENTS.md.template`

## 最小闭环 Demo（10 分钟）

目标：证明“输入碎片 → 输出结构化对象 → 可检索/可行动”这条链路是通的。

1) 准备输入：一段聊天/简介页/截图（不一定要先落盘到 `01_Inbox/raw/`）
2) 交给 Agent：按 `06_Infra/skills/portable/prism.md` 输出 Facts/Inferences/Actions/Me-Info
3) 写入对象：
   - 人物卡片：`05_Resources/network/people/<handle>.md`
   - Me 信号（可选）：`04_Assets/profile/signals.md`
4) 自检：
   - `python3 05_Resources/network/_cli/validate_people.py`
   - `rg -n "<关键词>" 05_Resources/network/people`

## 这个示例项目想证明什么（而不是证明什么）

- 证明：**协议优先**（目录/文件名定义要记录什么），执行性内容放 `06_Infra/`
- 证明：**search-first** 可以跑起来；脚本只做加速
- 证明：AI-native 的典型流：截图直接给 Agent → 写回结构化对象（而不是先囤 raw）
- 不证明：需要一个 SaaS/数据库/账号体系才能“做记忆系统”
