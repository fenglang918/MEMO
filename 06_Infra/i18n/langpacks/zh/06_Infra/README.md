# 06_Infra

这里是可选的基础设施区，用于放脚本、插件、语言切换与其他低依赖工具；`indexing/` 仅作为实验候选保留。

## 当前入口

- 生效 skills：`../.agents/skills/`
- plugins：`06_Infra/plugins/`
- 可选 indexing：`06_Infra/indexing/`
- i18n：`06_Infra/i18n/`
- utilities：`06_Infra/cleanup_examples.py`

## 推荐先看

- `06_Infra/plugins/master-schedule/`
- `06_Infra/i18n/`

## 常用命令

```bash
python3 06_Infra/i18n/switch_language.py --lang en
python3 06_Infra/i18n/switch_language.py --lang zh
python3 06_Infra/cleanup_examples.py
```
