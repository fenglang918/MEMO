# Protocol Federation Map v1

## 1. 目的

本文件定义模板仓库中的“协议联邦”模型：

- 各目录维护自己的局部真源
- `00_Protocol` 负责跨域导航与总结
- Agent / 可选工具先用这里定位，再下钻真源

## 2. 角色分工

1. 局部协议（真源层）
   每个域的 `README.md` / `index.md` / 局部 `AGENTS.md` 负责该域的细节与边界。

2. `00_Protocol`（总结层）
   负责跨域接口、消费顺序、引用规则，不复制真源正文。

3. 消费层（执行层）
   - Agent：按仓库级 `AGENTS.md` 检索与回链
   - 可选工具：若未来引入自研或外部 search / indexing 服务，也应按本层导航下钻真源

## 3. 局部协议真源清单

| 域 | 真源入口 | 在 `00_Protocol` 的摘要关注点 |
|---|---|---|
| Inbox | [`../../01_Inbox/README.md`](../../01_Inbox/README.md) | 临时收集、清理、归档入口 |
| Desires | [`../../02_Desires/README.md`](../../02_Desires/README.md) | 上游驱动与长期偏好 |
| Goal-Projects | [`../../03_Goal-Projects/README.md`](../../03_Goal-Projects/README.md) | TPCD 与 `YYYY/MM/` 目录约定 |
| Assets / Profile | [`../../04_Assets/profile/README.md`](../../04_Assets/profile/README.md) | 稳定个人资料、signals 与 exports 骨架 |
| Network | [`../../05_Resources/network/index.md`](../../05_Resources/network/index.md) | 人脉卡片、tags、检索方式 |
| Infra | [`../../06_Infra/README.md`](../../06_Infra/README.md) | scripts、plugins、i18n、实验层 |
| Principles | [`../../07_Principles/README.md`](../../07_Principles/README.md) | 跨项目裁决原则 |
| Operations | [`../../08_Operations/README.md`](../../08_Operations/README.md) | 日程、时间追踪、环境运维 |
| Develop | [`../../develop/README.md`](../../develop/README.md) | 模板自身迭代与开发记录 |

说明：

- 若某域新增或迁移真源，需要同步更新本表
- 本表是导航层，不替代各域正文

## 4. 给 Agent 的快速消费顺序

1. 读 [`../README.md`](../README.md)
2. 读 [`repo-contents-contract.v1.md`](repo-contents-contract.v1.md)
3. 按任务命中的域跳转本文件第 3 节
4. 输出时优先链接真源与具体证据路径

## 5. 给可选工具的支持接口

`00_Protocol` 向未来候选工具提供：

- 目录语义
- 对象语义
- 真源入口

历史草案：

- [`indexing-contract.v1.md`](indexing-contract.v1.md)

## 6. 治理规则

1. 先改真源，再改总结层
2. 总结层新增链接必须校验可达
3. 若未来工具暴露问题，优先回到对应真源修订
