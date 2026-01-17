# Network (Personal CRM) / Network（人脉库）

Goal: treat “people” as a searchable, actionable resource. One person = one Markdown card.

目标：把“人”当作可检索、可行动的资源来维护；一人一张 Markdown 卡片。

## Files / 文件

- `people/`: person cards
- `people/_template.md`: template
- `requirements-architecture.md`: design rationale
- `/_cli/network.py` (optional): lightweight query script

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
