---
name: me-network-crm
description: Record (录入), update, and query your personal network/contact data in a MEMO repo under `05_Resources/network/`, including ingesting external info sources (screenshots/chats/profiles) via PRISM-style decomposition, time-aware life-stage inference (`阶段锚点`), and relative-to-Me deltas (age / graduation). Use when asked to add/update a person card from any raw context, extract facts/inferences/actions, compute relative stage/age differences, or search for matching people via tags/keywords using CLI.
---

# Me Network CRM

## Files and conventions (source of truth)

- Entry guide: `05_Resources/network/index.md`
- Requirements/architecture: `05_Resources/network/requirements-architecture.md`
- Person card template: `05_Resources/network/people/_template.md`
- CLI query tool (agent-friendly): `05_Resources/network/_cli/network.py`
- CLI validator: `05_Resources/network/_cli/validate_people.py`
- PRISM (portable ingest skill): `06_Infra/skills/portable/prism.md`
- External source ingest notes (this skill): `06_Infra/skills/native/me-network-crm/references/external-source-ingest.md`
- Fields/tags reference (this skill): `06_Infra/skills/native/me-network-crm/references/fields-and-tags.md`

## Workflow

### A) Add / ingest a new contact (录入)

1) Choose a stable `Handle/ID` (ASCII, stable over time). Prefer `primary-handle` to make `Ctrl+P`/Quick Open easier.
2) Create `05_Resources/network/people/<handle>.md` from `05_Resources/network/people/_template.md`.
3) Fill the minimum fields for retrieval + action:
   - `Handle/ID`, `关键词`, `Tags`, `状态`, `最后联系`, `下次跟进` (or explicitly `暂无`)
   - Optional but useful for long-lived accuracy: `阶段锚点` (e.g. `2026-01-13（本科大三）`)
   - Optional for relative calculations: `出生日期` and/or `预计毕业`
4) Convert raw context into searchable tokens:
   - Put “domain + resource + scenario” into `关键词`
   - Add tags using the copy-paste list in `05_Resources/network/index.md` and only add new tags when necessary (then update the list)
5) If the user provided a long summary, keep it in sections, but avoid sensitive PII and avoid storing raw passwords/keys.

### B) Update an existing contact

1) Locate the card by tags/keywords/name:
   - `python3 05_Resources/network/_cli/network.py <keywords>`
   - `python3 05_Resources/network/_cli/network.py --tag '#resource/intro' <keywords> --json`
2) Append one line to `互动记录（流水）` for the new event/outcome.
3) Update `最后联系` and set/adjust `下次跟进` date + action.
4) Adjust `状态` if needed (`#status/active|warmup|dormant|archived`).

### C) Find people for a problem (检索匹配)

1) Translate the ask into tags + 2–5 keywords (domain + resource + scenario).
2) Query:
   - `python3 05_Resources/network/_cli/network.py --tag '#domain/ml' --tag '#resource/intro' <keywords> --json`
   - Time-aware stage inference (if cards have `阶段锚点`): `python3 05_Resources/network/_cli/network.py --as-of 2026-09-01 --json`
   - Relative to you (age / graduation deltas): `python3 05_Resources/network/_cli/network.py --relative-to-me --json`
     - Uses `04_Assets/profile/Me.md` by default (machine-readable fields); override via `--me-path`, `--me-birth-date`, `--me-stage-anchor`, `--me-expected-graduation`
     - Needs contact `出生日期` and/or `预计毕业` (otherwise部分字段为空；`预计毕业`可由`阶段锚点`对本科/硕士做粗略推算)
3) Return top candidates with:
   - Why they match (tags/keywords)
   - Suggested outreach angle (1–2 sentences)
   - Next action (update `下次跟进` in their cards if you’re taking action now)

## Validation (optional but recommended)

Run:

- Preferred: `python3 05_Resources/network/_cli/validate_people.py`
- Legacy (this skill copy): `python3 06_Infra/skills/native/me-network-crm/scripts/validate_people.py`

Fix any missing required fields or malformed tags/dates it reports.

If `python3` in your environment hangs (e.g. conda shim issues), retry with `/usr/bin/python3`.

### D) Ingest external info sources (截图/聊天/简介页) with PRISM

Goal: turn “mixed raw context” into **Facts / Inferences / Actions / Me-Info**, then write it into `05_Resources/network/people/<handle>.md` (append-only logs; update top fields as needed). If the user is sending a long timeline of chat screenshots, treat **each screenshot as one ingest batch** and keep the cumulative person card as the running log.

1) Identify the source type(s) and extraction constraints:
   - Chat screenshot / chat text
   - Profile page / bio / homepage
   - Email / long-form note
   - Mixed multi-source bundle (dedupe across sources)
   - If content is missing or ambiguous, ask up to 3 minimal questions (name, relationship+strength, last contact date).
2) Extract and normalize raw signals into searchable tokens (don’t over-interpret):
   - Pull explicit facts (names, school/company, stage, location, constraints, preferences)
   - Keep uncertain items as “to confirm”
3) Run PRISM decomposition (follow the canonical prompt; keep Facts vs Inferences separated):
   - Facts: only what is explicitly stated
   - Inferences: cautious, with basis
   - Actions: 1–3 dated follow-ups (date + purpose + tone)
   - Me-Info: any “about me” signals in the content; prefer stable preference/boundary/strategy, but keep time-stamped notes even if they are small (the user wants complete records)
4) Store results:
   - Update the card’s top bullets (`关键词/Tags/最后联系/下次跟进/阶段锚点/预计毕业/出生日期` as applicable)
   - Append one `## Prism（...）` block (date-stamped) near the bottom; avoid sensitive secrets (passwords/keys)
   - If you extract stable “about me” signals (preferences/boundaries/strategy), sync them into `04_Assets/profile/signals.md` (create if missing; short, reusable bullets; time-stamped when possible)
