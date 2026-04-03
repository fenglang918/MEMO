# 04_Assets

`04_Assets/` 是公开模板里的稳定存量层：放 **已经拥有、已经形成、或已经可稳定调用** 的内部存量，而不是仍待调用和转化的外部资源。

和 [`../05_Resources/`](../05_Resources/) 的区别：

- `04_Assets/` 更像已经入账、已经相对稳定的存量
- `05_Resources/` 更像仍需调用、维护和转化的外部杠杆

## 当前模板保留的资产域

- [`profile/`](./profile/)
  - 公开画像、结构化 Me、时间线、values、signals
- [`appearance/`](./appearance/)
  - 外观 / 形象相关材料（可选）
- [`skills/`](./skills/)
  - 技能画像与证据化能力（可选）
- [`exports/`](./exports/)
  - 可发布导出物，例如简历、主页、作品集（可选）

## 为什么模板只保留这几块

私有真源仓里的 `04_Assets/` 可能还包含：

- finance
- publication
- repositories
- writing
- virtual-assets

但公开模板不需要默认把这些高私密或强个人化资产都带上。

模板更适合先保留最通用的 4 类：

1. `profile`：谁是你、你怎么介绍自己
2. `appearance`：你的对外形象材料
3. `skills`：你有哪些稳定能力与证据
4. `exports`：哪些内容已经变成可分享产物

## 使用顺序

1. 先看 `profile/*.example.md`，理解结构
2. 再填写 `profile/*.md` 模板
3. 需要对外投递或公开时，再进入 [`exports/`](./exports/)
4. 需要补能力资产时，再维护 [`skills/README.md`](./skills/README.md)

## 典型导流

上游通常来自：

- `01_Inbox/`
- `03_Goal-Projects/`
- `05_Resources/`
- 对话、复盘、项目交付物

常见进入资产层的条件：

- 已经形成稳定事实
- 已经成为长期可复用存量
- 已经进入对外交付或正式成果状态
