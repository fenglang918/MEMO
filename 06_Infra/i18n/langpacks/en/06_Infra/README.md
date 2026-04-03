# 06_Infra

This is the optional infrastructure area for scripts, plugins, language switching, and other low-dependency tooling. `indexing/` is kept only as an experimental candidate.

## Current Entry Points

- active skills: `../.agents/skills/`
- plugins: `06_Infra/plugins/`
- optional indexing: `06_Infra/indexing/`
- i18n: `06_Infra/i18n/`
- utilities: `06_Infra/cleanup_examples.py`

## Recommended First Look

- `06_Infra/plugins/master-schedule/`
- `06_Infra/i18n/`

## Common Commands

```bash
python3 06_Infra/i18n/switch_language.py --lang en
python3 06_Infra/i18n/switch_language.py --lang zh
python3 06_Infra/cleanup_examples.py
```
