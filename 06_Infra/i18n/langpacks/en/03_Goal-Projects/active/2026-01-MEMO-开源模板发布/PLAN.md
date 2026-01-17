# Open-sourcing the MEMO Template (Example Project / Plan)

> Note: Sanitized example project. Public template keeps only reusable frames.

## Strategy

- Define stable outputs first (objects / minimal fields / retrieval rules); let inputs stay open. “Compile” fragments into durable memory assets.
- Keep search-first (`rg`) as default; scripts only accelerate, never lock-in.
- Make privacy/release explicit: never commit abusable secrets; examples are fictional/sanitized; do a pre-release safety check.

## Milestones

### Phase 1: positioning & protocol (2026-01)

- [x] Clarify positioning: memory protocol / reference workflow (not a product, not a data source, not an LLM API)
- [x] Define outputs: People / Projects / Decisions / Signals (minimal and usable)
- [x] Provide end-to-end workflow (chat/screenshot → PRISM → cards/signals)

### Phase 2: publishable template repo (2026-01 ~ 2026-02)

- [ ] Add release docs: LICENSE / CONTRIBUTING / release notes
- [x] Provide sanitized examples and runnable walkthroughs
- [x] Add guidance for exporting a public subtree (optional: subtree / filter-repo)
- [x] Organize protocol / workflows / skills / prompts / demos into a learnable structure
- [ ] Optional: stateless web playground (no DB, no auth, BYOK) to demonstrate “fragments → structured Markdown”
- [x] Decision: dual-track (GitHub protocol repo + stateless web playground) → `decisions/001-dual-track-repo-and-web-playground.md`
- [ ] Web cost strategy: BYOK by default; optional limited free quota; fallback guidance when quota exhausted

## Key assets (current snapshot)

- PRISM ingest prompt: `06_Infra/skills/portable/prism.md`
- Core native skill: `06_Infra/skills/native/me-network-crm/SKILL.md`
- People cards + design doc + CLI: `05_Resources/network/`
- Me profile + signals: `04_Assets/profile/`
- Language switch (langpacks + apply): `06_Infra/i18n/`
- Example projects (TPCD): `03_Goal-Projects/active/`

## Risks & mitigations

- Risk: users mistake it for an “automation product” → mitigate: README non-goals + boundaries
- Risk: example leaks privacy → mitigate: privacy baseline + fictional/sanitized examples + `.gitignore` guardrails
- Risk: protocol becomes too heavy → mitigate: minimal required fields; optional extensions
- Risk: web demo drifts into SaaS burden → mitigate: stateless by design; no storage; BYOK default

