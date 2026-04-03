# MEMO Template 全局架构压缩图（一页式）

日期：2026-04-03  
用途：快速说明公开模板版 MEMO 的当前结构  
口径：基于 `memo-publishing/pre-publish/repo/` 当前真实目录与默认脚手架，不把私有仓专属 bridge / 插件当成模板默认能力

## 一句话总述

**MEMO Template 不是单一 App，而是一套用 Markdown + Git 持有长期对象、用 Agent 与少量脚本驱动维护的个人记录协议模板。**

---

## 全局架构图

```text
                           00_Protocol
                     (全局契约 / 消费地图)
                                  |
                                  v
  02_Desires  --->  07_Principles  --->  01_Inbox
  (驱动层)          (裁决层)             (输入缓冲层)
                                  |
                                  v
                          03_Goal-Projects
                           (核心对象层)
                           /          \
                          v            v
                   05_Resources     04_Assets
                   (外部杠杆层)     (稳定存量层)
                          \            /
                           \          /
                            v        v
                            08_Operations
                       (运行面 / 主看板 / 留痕)
                                  ^
                                  |
                             06_Infra
                  (脚本 / 插件 / i18n / 可选实验层)

          人类 / Agent 前台：编辑器 + Code Agent + `.agents/skills/`
```

---

## 每层一句话

| 层 | 目录 | 一句话角色 |
| ------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| 全局契约层 | [00_Protocol](../../../00_Protocol/README.md) | 给整个模板和 agent 用的结构契约、消费地图与入口说明。 |
| 驱动层 | [02_Desires](../../../02_Desires/README.md) | 保留长期行动背后的偏好、欲望与驱动。 |
| 裁决层 | [07_Principles](../../../07_Principles/README.md) | 为跨项目重复出现的高频取舍提供默认裁决规则。 |
| 输入缓冲层 | [01_Inbox](../../../01_Inbox/README.md) | 承接尚未归位的现实输入，让材料先落地、再分流。 |
| 核心项目对象层 | [03_Goal-Projects](../../../03_Goal-Projects/README.md) | 用 TPCD 组织长期目标、项目与高机会成本决策。 |
| 外部杠杆层 | [05_Resources](../../../05_Resources/README.md) | 维护可调用的外部资源，如 network、工具与资料。 |
| 稳定存量层 | [04_Assets](../../../04_Assets/README.md) | 沉淀 profile、exports、resume 等稳定存量。 |
| 运行面 | [08_Operations](../../../08_Operations/README.md) | 承担主日程、时间追踪、运行留痕与日常运转。 |
| 基础设施层 | [06_Infra](../../../06_Infra/README.md) | 提供脚本、插件、i18n 和可选实验能力。 |
| 模板开发区 | [develop](../../../develop/README.md) | 放模板自身演进说明、架构文档和开发记录。 |

---

## 最关键的三点

### 1. 模板中心不是协议说明，而是对象层

- 真正“活着”的核心仍然是：
  - [03_Goal-Projects](../../../03_Goal-Projects/README.md)
  - [05_Resources/network](../../../05_Resources/network/index.md)
  - [04_Assets](../../../04_Assets/README.md)
  - [08_Operations](../../../08_Operations/README.md)
- [00_Protocol](../../../00_Protocol/README.md) 很重要，但更像全局约定层，不是日常主工作区。

### 2. 模板核心不是“记笔记”，而是“对象化”

- 项目被组织成长期工作对象
- 人物被组织成可检索的人脉对象
- 自我资料与成果被组织成稳定存量对象
- 时间与执行被组织成运行面对象

一句话：**MEMO Template 试图给“长期对象如何被维护”提供一个可复用骨架。**

### 3. 模板已经不是纯静态目录，而是带少量执行闭环的协议脚手架

- [03_Goal-Projects](../../../03_Goal-Projects/README.md) 提供 TPCD 工作流
- [05_Resources/network](../../../05_Resources/network/index.md) 提供 Personal CRM 骨架
- [08_Operations/00_Master-Schedule](../../../08_Operations/00_Master-Schedule/README.md) + [06_Infra/plugins/master-schedule](../../../06_Infra/plugins/master-schedule/README.md) 提供主日程闭环
- [04_Assets/profile](../../../04_Assets/profile/README.md) 提供 profile / values / timeline 骨架
- [`.agents/skills/`](../../../.agents/skills/) 提供模板内置 Agent 工作流入口

但这里的“执行闭环”仍然是：

- Markdown 真源
- Agent / script 辅助
- 少量派生产物

它不是完整统一前台产品。

---

## 面向首次阅读者的 30 秒说明版

可以直接这样说：

> MEMO Template 本质上不是普通笔记模板，而是一套个人记录协议。最上游是 `Desires`、`Principles` 和 `Inbox`，分别管驱动力、裁决规则和未定型输入；中间最核心的是 `Goal-Projects`、`Resources`、`Assets`，分别管项目对象、外部杠杆和稳定存量；底下由 `Operations` 和 `master-schedule` 提供实际运行与留痕。`00_Protocol` 不负责日常执行，而是给整个模板和 agent 用的结构契约。

---

## 当前不应被误讲的点

- 这不是一个已经产品化完成的统一前台
- 这不是私有真源仓的完整能力集合
- 私有仓里的 bridge、专属插件和敏感上下文，不属于公开模板默认能力
