# 核心概念说明

## TPCD

在这个模板里，一个项目目录默认拆成四层：

| 缩写 | 含义 | 典型文件 |
|---|---|---|
| `T` | Target | `README.md` |
| `P` | Plan | `PLAN.md` |
| `C` | Cognition | `cognition/*.md` |
| `D` | Decision | `decisions/*.md` |

这样做的目的，是把“目标、执行、理解、取舍”放在同一个项目目录里，减少上下文断裂。

## ADR

ADR 原意是 Architecture Decision Record。这里借用成“重要决策记录”。

每条 ADR 至少回答四件事：

1. 为什么现在要做决策
2. 有哪些备选项
3. 最后选了什么
4. 为什么这样选

推荐命名：

- `decisions/001-xxx.md`
- `decisions/002-xxx.md`

如果旧决策被推翻，不删除原文件，而是新增一条 ADR 记录推翻原因和新结论。

## Cognition

`cognition/` 不是最终承诺，而是“理解如何演进”的记录区。

适合放：

- 假设
- 证据
- 反例
- 复盘
- 下一步待验证问题

它和 ADR 的区别在于：

- Cognition 是思考演进
- ADR 是某次取舍的固化结果

## 常见错误

- 把所有内容都写进 `PLAN.md`
- 用 README 记流水账
- 口头做了重要决策，却没有留下 ADR
- 把认知变化埋在聊天里，回头无法复盘

## 关联

- [`../README.md`](../README.md)
- [`../../07_Principles/README.md`](../../07_Principles/README.md)
