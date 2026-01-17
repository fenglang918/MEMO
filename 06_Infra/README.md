# 06_Infra

基础设施区（可选）。用于放置 Agent 可执行技能、脚本与一键工具（例如：清理内置 examples、做一致性检查等），尽量保持无依赖/低依赖。

入口：
- Skills：`06_Infra/skills/`
- i18n（语言切换）：`06_Infra/i18n/`（见 `06_Infra/i18n/switch_language.py`）
- 清理示例（可选，默认归档可恢复）：`python3 06_Infra/cleanup_examples.py --apply`
