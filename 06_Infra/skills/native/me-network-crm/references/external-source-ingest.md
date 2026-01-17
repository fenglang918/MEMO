# External Source Ingest (PRISM) — Notes

Use this when the user provides “external info sources” (截图/聊天/简介页/邮件/群聊等) and wants you to extract + organize + store into `05_Resources/network/people/`.

## Source types → extraction focus

- Chat (text / screenshot)
  - Pull: explicit facts, constraints, preferences, asks/requests, commitments, boundaries, dates
  - Don’t: interpret “已读不回/没点赞” as rejection (at most: “可能的互动规则”，标注不确定)
- Profile/bio/homepage
  - Pull: identity, org/role, location/timezone, research interests, contact channels, public links
  - Tag: `#role/... #domain/... #city/...`
- Email / long-form note
  - Pull: decisions, timelines, open loops, promised follow-ups, concrete deliverables
- Mixed bundle
  - Dedupe: unify the same fact across sources; keep “source-of-truth” notes in the Prism Facts section when useful

## PRISM output contract (what must be produced)

- Facts: only explicitly stated items; ok to quote short phrases
- Inferences: cautious language + basis (“依据：…”) + mark uncertainty
- Actions: 1–3 next steps, each with `YYYY-MM-DD`, purpose, and tone
- Me-Info: any “about me” signals; prefer stable preference/boundary/strategy, but keep time-stamped notes even if they are small (the user wants complete records)

Canonical prompt (in this repo): `06_Infra/skills/portable/prism.md`

## Storage rules

- Update top bullets for retrieval: `关键词/Tags/状态/最后联系/下次跟进` (+ optional `阶段锚点/出生日期/预计毕业`)
- Append a dated block: `## Prism（...，YYYY-MM-DD）` with Facts/Inferences/Actions/Me-Info
- If you extract stable “about me” signals, sync them into `04_Assets/profile/signals.md` (short, reusable bullets; create if missing; append-only)
- Never store directly abusable secrets (passwords/API keys/private keys)
