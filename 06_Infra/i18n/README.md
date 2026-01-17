# i18n（Language Packs）

本目录提供一个“语言包（langpack）→ 一键覆盖”的机制，用于在同一套 MEMO 结构下切换文档语言。

设计目标：

- **语言切换是覆盖（apply）**：把 `langpacks/<lang>/` 里的文件覆盖到仓库同路径文件。
- **只覆盖语言相关文档**：默认只收录 README / prompts / skills 等；数据文件不应被语言切换脚本触碰。
- **可扩展**：后续需要双语的文件，把同路径版本放进对应 langpack 即可。
  - 例如：示例项目的 `README.md` / `PLAN.md` / 关键 cognition 也可以纳入（见 `03_Goal-Projects/active/2026-01-MEMO-开源模板发布/`）。

使用：

- 列出可用语言：`python3 06_Infra/i18n/switch_language.py --list`
- Dry-run：`python3 06_Infra/i18n/switch_language.py --lang zh`
- 应用（覆盖）：`python3 06_Infra/i18n/switch_language.py --lang zh --apply`

语言包目录：

- `06_Infra/i18n/langpacks/zh/`
- `06_Infra/i18n/langpacks/en/`
