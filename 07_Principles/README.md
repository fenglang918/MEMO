# Principles (Cross-Project)

本模块用于沉淀 **跨项目的高优先级原则**（上游约束），目标是让你在协作与决策时可快速检索并裁决，而不是临场重新推理一遍。

边界：

- 不属于 `00_Protocol/`：协议层只放 schema、定义、结构与使用约定，不放具体原则正文。
- 不等同于单个项目的 `decisions/`：项目 ADR 记录项目语境下的分叉决策；可以回链本模块作为前置约束。
- 不放可直接滥用的明文机密。

## Tags

命名空间：

- `#area/...`
- `#scene/...`
- `#trigger/...`
- `#scope/...`
- `#status/...`

常见示例：

- `#area/time`
- `#area/collab`
- `#area/knowledge-management`
- `#scene/async-collab`
- `#scene/decision-making`
- `#scene/learning`
- `#trigger/context-switch`
- `#trigger/hidden-cost`
- `#trigger/reading-notes`
- `#status/active`

## Search

- `rg -n "#scene/async-collab" 07_Principles`
- `rg -n "#scene/decision-making" 07_Principles`
- `rg -n "#trigger/context-switch" 07_Principles`
- `rg -n "#area/time.*#scene/decision-making|#scene/decision-making.*#area/time" 07_Principles`

## Index

- [`005-ai-assisted-delivery-attitude.md`](./005-ai-assisted-delivery-attitude.md)
  - AI-Assisted Delivery Boundaries and Attitude: 对外关键交付默认不能直接发送 raw AI text。`#area/writing #area/collab #scene/collab-tooling #trigger/urgent-ping #status/active`
- [`004-project-first-knowledge-accumulation.md`](./004-project-first-knowledge-accumulation.md)
  - Project-First Knowledge Accumulation：先在项目语境里消费知识，再抽象成资产。`#area/knowledge-management #scene/learning #trigger/reading-notes #status/active`
- [`003-reading-materials-as-resources.md`](./003-reading-materials-as-resources.md)
  - Reading Materials as Resources：阅读材料先进入 `05_Resources/`，不要直接制造项目执行噪音。`#area/research #area/time #scene/information-intake #trigger/context-switch #status/active`
- [`002-certainty-vs-probability-budget.md`](./002-certainty-vs-probability-budget.md)
  - Certainty vs. Probability Budget：确定性基建与高波动尝试应预算隔离。`#area/finance #area/time #scene/decision-making #trigger/hidden-cost #status/active`
- [`000-time-value-and-autonomy.md`](./000-time-value-and-autonomy.md)
  - Time Value and Autonomy：默认避免把自己变成长期维护者。`#area/time #area/collab #scene/async-collab #scene/time-budget #trigger/context-switch #status/active`

## Docs

- 模板：[`_template.md`](./_template.md)
- 模块说明：[`AGENTS.md`](./AGENTS.md)
