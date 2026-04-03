# MEMO

**Making Ephemeral Memories Objects**

An AI-native personal operating system protocol.

This repository is the **public template product** of MEMO: it keeps i18n, sanitized examples, `USAGE.md`, and agent workflows, while backporting the newer protocol, directory semantics, and skills from the private working repo; `06_Infra/indexing/` is kept only as an optional experiment.

## What This Is

MEMO is not a single app. It is a protocol for organizing long-lived personal records:

- Markdown and Git hold the data
- directory semantics define object boundaries
- agents and scripts operate on top of the repo

Core stance:

- **Protocol first**
- **Agent agnostic**
- **Search before summary**

## Layout

```text
.
├── 00_Protocol/             # contracts / federation / usage / privacy
├── 01_Inbox/                # temporary intake
├── 02_Desires/              # upstream drivers
├── 03_Goal-Projects/        # TPCD + YYYY/MM/
├── 04_Assets/               # stable personal assets
├── 05_Resources/            # callable external resources
├── 06_Infra/                # indexing / i18n / utilities
├── 07_Principles/           # cross-project principles
├── 08_Operations/           # schedule / time-tracking / setup
├── .agents/skills/          # agent skill packages
└── develop/                 # template development workspace
```

## Project Shape

`03_Goal-Projects/` now has two main entry styles:

- `YYYY/MM/<project>/`
- `evergreen/<project>/`

Each project follows **TPCD**:

- `README.md` = Target
- `PLAN.md` = Plan
- `cognition/` = Cognition
- `decisions/` = Decision

## Quick Start

1. Use the repo as a template or clone it locally.
2. Start by reading the target directory's `README.md` / `index.md` / `AGENTS.md`.
3. Optionally clean built-in examples with `cleanup_examples.py`.
4. Generate your own repo-level `AGENTS.md` from `00_Protocol/AGENTS.md.template`.
5. Only if you want to revisit the old indexing experiment, run the script in `06_Infra/indexing/`.

```bash
python3 06_Infra/cleanup_examples.py
```

## Agent Entry Points

- Protocol: `00_Protocol/`
- Skills: `.agents/skills/`
- Optional indexing experiment: `06_Infra/indexing/`

Recommended lookup order:

```text
repo structure / file naming
  -> matching domain README / index / AGENTS
  -> 00_Protocol summary docs only when needed
```

## Language Packs and Examples

This template keeps:

- `06_Infra/i18n/` for zh/en langpacks
- sanitized example projects / people cards / principles
- `08_Operations/` schedule and time-tracking scaffolding
- `06_Infra/plugins/master-schedule/` scripts for calendar sync and reports
- `00_Protocol/USAGE.md` as the onboarding page

If you want a cleaner skeleton:

- `python3 06_Infra/cleanup_examples.py`
- `python3 06_Infra/cleanup_examples.py --apply`

## Fit

Good fit:

- long-lived, portable, searchable personal records
- local-first workflows with code agents
- separating content structure from tooling

Not a fit:

- passive note dumping
- no-structure, everything-goes logs
- storing directly abusable plaintext secrets

## License

MIT
