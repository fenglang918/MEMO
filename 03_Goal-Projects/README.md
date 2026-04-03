# Projects

这里把一个“目标 / 项目”视为四个层级，统称 **TPCD**：

- **Target**：目标与边界，写在 `README.md`
- **Plan**：执行路径与阶段，写在 `PLAN.md`
- **Cognition**：认知演进、复盘、假设与反例，写在 `cognition/`
- **Decision**：关键取舍与理由，写在 `decisions/`

## 推荐目录结构

```text
03_Goal-Projects/
├── _docs/                     # 概念与使用说明
├── _TEMPLATE/                 # 新项目模板
├── evergreen/                 # 常驻项目
└── YYYY/
    └── MM/
        └── <project>/
            ├── README.md
            ├── PLAN.md
            ├── cognition/
            └── decisions/
```

## 目录约定

- 时间归档项目：放在 `YYYY/MM/`
- 不适合按月份归档的长期事项：放在 `evergreen/`
- 不再使用 `active/` 作为主入口

## 为什么要这样组织

这套结构的目的，不是把项目拆成更多目录，而是避免三种常见混乱：

- 目标、执行、理解和决策混写在一页里
- 长期项目只剩日志，回看时看不出“为什么这样做”
- 关键取舍只存在于聊天或脑内，没有被固化

TPCD 的价值在于：

- `README.md` 保留目标函数
- `PLAN.md` 保留推进路径
- `cognition/` 保留理解是怎么变化的
- `decisions/` 保留关键岔路口为什么这么选

## 入口

- 模板：[`_TEMPLATE/`](./_TEMPLATE/)
- 概念说明：[`_docs/concepts.md`](./_docs/concepts.md)
- 常驻项目说明：[`evergreen/README.md`](./evergreen/README.md)

## 示例（脱敏）

- [`2026/01/MEMO-开源模板发布/`](./2026/01/MEMO-开源模板发布/)
- [`2026/01/phd-vs-job/`](./2026/01/phd-vs-job/)

## 与其他顶层目录的关系

- 如果重点是“我要达成什么目标”，优先放这里
- 如果重点是“跨项目都适用的裁决规则”，优先放 [`../07_Principles/`](../07_Principles/)
- 如果重点是“已经拥有的稳定资料或导出物”，优先放 [`../04_Assets/`](../04_Assets/)
- 如果重点是“项目运行中的主日程与执行留痕”，优先放 [`../08_Operations/`](../08_Operations/)
