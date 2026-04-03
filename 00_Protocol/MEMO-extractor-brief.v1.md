# MEMO Extractor Brief v1

> 目的：让没有仓库权限的外部提问器只负责生成高质量请求；由有仓库权限的 Agent 负责检索、引用、回链与整理。

## 1. 这个模板仓库是什么

- 这是一个可分发的 MEMO 模板仓库，不是某个单一项目 repo
- 核心对象按目录语义组织：Inbox / Desires / Goal-Projects / Assets / Resources / Principles / Operations
- 项目主域位于 `03_Goal-Projects/`，推荐结构：
  - `YYYY/MM/<project>/`
  - `evergreen/<project>/`
- 模板当前最重要的默认工作流：
  - TPCD 项目工作流
  - Personal CRM
  - Master Schedule
  - 本地 `.agents/skills/`

参考：

- 仓库总览：[`../README.md`](../README.md)
- 内容契约：[`schemas/repo-contents-contract.v1.md`](schemas/repo-contents-contract.v1.md)
- 联邦导航：[`schemas/protocol-federation-map.v1.md`](schemas/protocol-federation-map.v1.md)

## 2. 角色分工

### A. 外部 extractor（无仓库权限）

- 不做仓库检索
- 不编造路径
- 不声称“仓库里已经有结论”
- 只产出高质量任务请求包

### B. 内部 agent（有仓库权限）

- 先读目标域入口，再做最小化检索
- 给关键结论附仓库内路径
- 区分事实 / 推断 / 假设 / 不确定点
- 未命中时明确写“未检索到现成文档”

## 3. 外部 extractor 的任务请求包（6 槽位）

1. 目标域：优先查哪个域
2. 时间窗：是否限定日期范围
3. 对象类型：`timeline / cognition / decision / raw / README`
4. 证据粒度：原话优先还是摘要优先
5. 输出结构：希望按什么框架输出
6. 缺失处理：未命中是否显式说明

## 4. 内部 agent 的执行顺序

1. 先读目标目录的 `README.md` / `index.md` / `AGENTS.md`
2. 必要时再看 [`schemas/protocol-federation-map.v1.md`](schemas/protocol-federation-map.v1.md) 与 [`schemas/repo-contents-contract.v1.md`](schemas/repo-contents-contract.v1.md)
3. 再打开命中的真源文档与具体证据
4. 输出时附相对路径，未命中要明说

执行入口模板：

- [`AGENTS.md.template`](AGENTS.md.template)

## 5. 推荐输出骨架

1. Timeline
2. Statements / Evidence
3. Structure / Constraints
4. Decision Factors
5. Missing Evidence

## 6. 可直接复制给外部 extractor 的 Prompt

```text
你是“外部提问器”，没有 MEMO 仓库读写权限。
你的任务不是检索仓库，而是生成一个交给“有仓库权限的 Agent”执行的任务请求包。

请输出：
1) 目标域
2) 时间窗
3) 对象类型
4) 证据粒度
5) 输出结构
6) 缺失处理

要求：
- 不要声称你已经检索仓库；
- 不要编造文件路径；
- 用明确、可执行、可验证的中文写给内部 Agent。
```

## 7. 治理

- 本文是外部提问入口摘要，不替代各目录真源
- 任何规则变更，先改真源，再更新本 brief
- 若模板结构发生显著变化，建议新开版本文件
