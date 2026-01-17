# Open-sourcing the MEMO Template (Example Project / Target)

> Note: This is a sanitized example project used to demonstrate how a real goal lands into TPCD.

## Target (What)

Publish a bilingual **MEMO template repo**: extract a reusable protocol for managing life memory (files + conventions + templates + optional scripts).

## Why

- The value of life records is **searchable, reviewable, actionable**; many tools lock you in or drift into duplicated copies.
- We do not ship a hosted data source or a productized LLM API. The value is a **vendor-neutral protocol**: users “compile” their own fragments with their own AI tools.
- Long-term direction: inputs can be messy (chat / screenshots / links), outputs are stable objects (People / Projects / Signals / indexes).

## Key Results (KRs)

1. The repo is “ready to use” (README / privacy baseline / usage / templates / examples) and can be published when needed.
2. Define the minimal object model + fields (start with people cards and projects).
3. Provide a minimal local workflow (search-first + optional CLI) with 1–2 runnable examples.

## Constraints

- Budget: 0 (local files + Git; user chooses their AI tool)
- Time: MVP first (usable, explainable, extensible), then iterate
- Non-negotiable: never store directly abusable secrets (passwords, API keys, private keys)
- Negotiable: automation level, visualization, integrations

## Where the deliverables live in the repo

This project is not “one doc”; it’s “a repo structure that encodes protocol + workflows”:

- Root manifesto / entry: `README.md`
- Protocol (objects / rules / usage): `00_Protocol/`
- Personal CRM (people cards + design + optional CLI): `05_Resources/network/`
- PRISM ingest prompt (copy into any AI): `06_Infra/skills/portable/prism.md`
- Core native skill (end-to-end CRM maintenance): `06_Infra/skills/native/me-network-crm/SKILL.md`
- Language switch (apply langpacks): `06_Infra/i18n/switch_language.py`
- AI-native init template (for `/init`): `00_Protocol/AGENTS.md.template`

## Minimal end-to-end demo (10 minutes)

Goal: prove the chain “raw fragments → structured objects → searchable/actionable” works.

1) Prepare input: a chat / profile snippet / screenshot (not necessarily saved into `01_Inbox/raw/`)
2) Ask the agent to follow: `06_Infra/skills/portable/prism.md` (Facts/Inferences/Actions/Me-Info)
3) Write objects:
   - Person card: `05_Resources/network/people/<handle>.md`
   - Me signals (optional): `04_Assets/profile/signals.md`
4) Validate:
   - `python3 05_Resources/network/_cli/validate_people.py`
   - `rg -n "<keyword>" 05_Resources/network/people`

## What this example tries to prove (and not prove)

- Proves: **protocol first** (directories/files define “what to record”); executable logic lives in `06_Infra/`
- Proves: **search-first** is enough; scripts only accelerate
- Proves: AI-native ingest: give screenshots directly to the agent → write back objects (raw is optional)
- Not proving: you need SaaS / DB / accounts to build a “memory system”

