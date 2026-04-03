# schemas

本目录存放 `00_Protocol` 的结构化协议文件（schema / contract / field definitions）。

## 当前协议文件

- [`repo-contents-contract.v1.md`](repo-contents-contract.v1.md)
  - 定义顶层目录语义、内容对象边界与引用规则
- [`protocol-federation-map.v1.md`](protocol-federation-map.v1.md)
  - 定义“局部真源 -> 00_Protocol 总结层 -> Agent / 可选工具消费层”的联邦映射
- [`indexing-contract.v1.md`](indexing-contract.v1.md)
  - 历史本地 indexing 实验的接口草案（当前不是默认主协议）
- [`profile.schema.md`](profile.schema.md)
  - profile 可选字段与扩展建议

## 使用约定

1. 新协议文件使用版本后缀，例如 `*.v1.md`
2. 若某候选工具显式依赖协议，再同步更新其实现或计划
3. 内容协议与执行约束分层维护：
   - 内容协议：`00_Protocol/schemas/*`
   - 执行入口模板：[`../AGENTS.md.template`](../AGENTS.md.template)

## 关联

- 模板总入口：[`../README.md`](../README.md)
- 使用约定：[`../USAGE.md`](../USAGE.md)
- 隐私边界：[`../PRIVACY.md`](../PRIVACY.md)
