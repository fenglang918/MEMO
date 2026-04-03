# Module Instructions: 07_Principles

## 目录定位

- 本目录只放跨项目、可复用、可裁决的高优先级原则正文。
- 不在这里放 `00_Protocol/` 层的 schema、定义或结构文档。
- 不在这里放单个项目语境下的 ADR；项目决策应写在 `03_Goal-Projects/*/decisions/`，并回链本目录原则。

## 读写顺序

- 先看 `README.md`：获取 tags、检索方式和原则索引。
- 新增原则时，先复制 `_template.md`，再补全最小可裁决字段。
- 修改已有原则时，优先保持“可检索 + 可裁决 + 可引用”的密度，而不是把它写成长篇散文。

## 新增与修改约束

- 原则正文文件命名使用递增编号 + 简短 slug，例如 `005-example-principle.md`。
- 每条原则至少包含：`Keywords`、`Tags`、`Trigger signals`、`Decision rule`、`Context`、`Examples`。
- 若只是某项目下的本地化解释，不要在这里重写原则正文，改为在项目 ADR 中引用本目录。
- tags 先复用 `README.md` 中已有枚举；确需新增时，先更新 `README.md` 再落到正文，避免孤儿 tag。
- 不记录可直接滥用的明文机密。
- 面向公开模板时，原则正文应优先选择跨人群可复用的表达，避免混入明显私人病史、身份或关系锚点。
