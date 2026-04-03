# Resources

`05_Resources/` 是 MEMO 模板里的外部杠杆层：维护 **可调用、可检索、可后续转化** 的资源，而不是已经入账的稳定资产。

和 `04_Assets/` 的区别：

- `04_Assets/` 更像已经拥有、相对稳定的存量
- `05_Resources/` 更像仍需调用、维护、筛选或转化的外部杠杆

## 当前模板保留的资源域

- [`network/`](./network/)：
  - Personal CRM / 人脉资源库
  - 一人一张卡片，面向检索与行动
- [`reading/`](./reading/)：
  - 尚未转化为项目行动、但值得保留和后续调用的阅读材料

## 为什么模板只保留这两块

私有真源仓里的 `05_Resources/` 可能还包含：

- 工具 / 账号
- 医疗资源
- LLM / infra / server notes
- 研究想法
- 各种专题型资源池

但公开模板不需要一开始就把这些全部带上。

模板更适合先保留两种最通用、最容易被多数人直接复用的资源层：

1. `network`：谁能提供帮助、资源、协作与判断
2. `reading`：哪些材料值得以后调取，但还不该直接塞进项目

## 资源层的典型导流

上游通常来自：

- `01_Inbox/`
- 外部截图 / 聊天 / 简介页 / 文章 / PDF
- 某个项目里的临时参考材料

常见去向：

- 人相关 -> `network/`
- 阅读材料 -> `reading/`
- 如果后来变成稳定个人事实 -> `04_Assets/`
- 如果后来变成项目内认知 / 决策证据 -> `03_Goal-Projects/`

## 推荐阅读顺序

1. 先看 [`network/index.md`](./network/index.md)
2. 再看 [`reading/README.md`](./reading/README.md)
3. 需要理解人脉库设计动机时，再看 [`network/requirements-architecture.md`](./network/requirements-architecture.md)
