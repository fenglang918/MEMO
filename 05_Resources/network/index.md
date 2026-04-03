# Network (Personal CRM) / Network（人脉库）

Goal: treat “people” as a searchable, actionable resource. One person = one Markdown card.

目标：把“人”当作可检索、可行动的资源来维护；一人一张 Markdown 卡片。

## Files / 文件

- `people/`: person cards
- `people/_template.md`: template
- `AGENTS.md`: module instructions
- `requirements-architecture.md`: design rationale
- `/_cli/network.py` (optional): lightweight query script
- `../../.agents/skills/me-network-crm/SKILL.md`: agent workflow entry

## Naming / 命名

- Prefer stable ASCII handles for filenames: `people/<handle>.md`
- Put real names / aliases inside the file for search recall.

## Tags / 标签

Recommended prefixes:

- Domain: `#domain/...` (e.g. `#domain/ml`)
- Resource: `#resource/...` (e.g. `#resource/intro`)
- Role: `#role/...` (e.g. `#role/researcher`)
- City: `#city/...` (e.g. `#city/sg`)
- Relationship: `#rel/...` (e.g. `#rel/mentor`)
- Status: `#status/...` (e.g. `#status/active`)

## Retrieval / 检索

- `rg -n "#resource/intro" 05_Resources/network/people`
- `python3 05_Resources/network/_cli/network.py --tag '#resource/intro' --json` (optional)

## Agent Entry / Agent 入口

- `../../.agents/skills/me-network-crm/SKILL.md`
  - 默认 CRM workflow 入口
  - 适合录入联系人、更新 card、按标签检索、处理外部资料 ingest

## Recommended Reading Order / 推荐阅读顺序

1. `index.md`
2. `people/_template.md`
3. `AGENTS.md`
4. `requirements-architecture.md`
5. `../../.agents/skills/me-network-crm/SKILL.md`
