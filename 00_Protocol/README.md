# 00_Protocol（Repo Contents 协议层）

`00_Protocol/` 是公开模板版 MEMO 的 contents 协议层，用来定义：

- 顶层目录分别承载什么语义
- 什么内容算对象、证据、导航入口
- Agent 应如何检索、引用、回链

这里不绑定固定检索实现；无论是人、Agent，还是未来接入的外部工具，都应优先遵循这里定义的结构语义。

## 当前生效协议

- [`schemas/README.md`](schemas/README.md)
  - schema / contract 清单
- [`schemas/repo-contents-contract.v1.md`](schemas/repo-contents-contract.v1.md)
  - 模板当前目录语义与内容对象契约
- [`schemas/protocol-federation-map.v1.md`](schemas/protocol-federation-map.v1.md)
  - 跨域导航层，指向各目录真源入口
- [`MEMO-extractor-brief.v1.md`](MEMO-extractor-brief.v1.md)
  - 给外部提问器或外部协作者的一页入口
- [`USAGE.md`](USAGE.md)
  - 公开模板上手约定
- [`PRIVACY.md`](PRIVACY.md)
  - 公开模板隐私边界
- [`AGENTS.md.template`](AGENTS.md.template)
  - 仓库级 Agent 执行约束模板

## 候选 / 历史草案

- [`schemas/indexing-contract.v1.md`](schemas/indexing-contract.v1.md)
  - 模板内保留的 indexing 实验接口草案；当前不是默认工作流依赖
- [`schemas/profile.schema.md`](schemas/profile.schema.md)
  - profile 字段扩展建议；不是强制主协议

## 协议联邦模型

- 局部规则优先留在各自目录，作为唯一真源
- `00_Protocol` 负责跨域总结、导航与统一消费接口
- 总结层必须回链真源，避免复制出第二份会漂移的“伪真源”

一个简化视图：

```text
局部目录 README / index / AGENTS
        ↓
00_Protocol federation map / contracts
        ↓
Agent / 可选工具下钻真源
```

## 与可选工具的关系

1. `00_Protocol` 先定义内容语义
2. Agent 或未来的可选工具再按该语义消费仓库
3. 若某工具实验暴露噪音或结构漂移，再反向修协议或写作约定

## 关联入口

- 执行入口模板：[`AGENTS.md.template`](AGENTS.md.template)
- 模板总览：[`../README.md`](../README.md)
- 模板开发说明：[`../develop/README.md`](../develop/README.md)
- 当前 overview：[`../develop/docs/overview/`](../develop/docs/overview/)

## 边界

- 这里定义协议，不放执行脚本
- 可执行技能放在 [`../.agents/skills/`](../.agents/skills/)
- 不写入可直接滥用的明文机密
- 私有真源仓的内部材料、私有 bridge、敏感案例，不属于公开模板协议层默认内容
