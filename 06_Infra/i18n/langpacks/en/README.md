# MEMO

**Making Ephemeral Memories Objects**

An AI-native personal operating system protocol.

Turn ephemeral memories into durable objects.

> **What we choose to record reveals what we choose to value.**

---

## What this is

**MEMO** is an **AI-native personal operating system protocol**: a way to turn fleeting thoughts, experiences, relationships, decisions, and reflections into **structured, versioned, evolvable objects** stored in a plain Git repo.

This repository is the **shareable template** of that protocol.

**Traits**: Markdown-first · Git versioning · search-first · low maintenance

---

## Why MEMO

Most tools solve “storage”. MEMO focuses on **selection**:

> What is worth becoming a long-lived object?

In the AI-memory era, the real question is ownership and portability:

> Who owns your memory? Can you control it, migrate it, and combine it across models?

### Protocol first, agent agnostic

MEMO is not an “app”; it’s a **file-system-level protocol**.

| Dimension | Typical tools / AI memory | MEMO protocol |
|---|---|---|
| Ownership | platform-owned | you own it (local Git) |
| Format | proprietary | plain Markdown |
| Model lock-in | tied to one AI | any AI / any agent |
| Management | via official app | via any code agent |
| Source integration | limited | any life fragments |

Core architecture: **storage and intelligence are decoupled**.

```
any fragments -> MEMO (local Git) -> any AI / code agent
        ^                          v
  you own the repo             models are replaceable CPUs
```

---

## Layout

```text
.
├── 00_Protocol/             # Protocol: schemas, usage/privacy, templates
├── 01_Inbox/                # Ephemeral inputs
├── 02_Desires/              # Upstream drivers (values/preferences)
├── 03_Goal-Projects/        # Projects (TPCD)
├── 04_Assets/               # Assets (ME): stable “what I have”
├── 05_Resources/            # Resources (MO): callable external leverage
└── 06_Infra/                # Infra (optional): scripts / agent skills
```

Note: the repo layout will keep evolving; when docs and folders disagree, trust the current directory structure.

### Assets vs Resources

| | Assets | Resources |
|---|---|---|
| Question | what I HAVE | what I can USE |
| Nature | stable, “showcase” | requires maintenance |
| Examples | resume, portfolio, skills | people, APIs, venues |

Transformation: `Resource + Action = Asset`

### Project shape (TPCD)

```text
03_Goal-Projects/active/<project>/
├── README.md     # Target
├── PLAN.md       # Plan
├── cognition/    # Cognition notes
└── decisions/    # ADR-style decisions
```

---

## Quick start

1. Fork / clone / use as template
2. (Optional) If you want to start from an “empty skeleton”: `python3 06_Infra/cleanup_examples.py --apply` (archived & restorable)
3. Generate `AGENTS.md` at repo root via your code agent `/init` (recommended)
4. Use `rg` (ripgrep) to search-first
5. Start from `01_Inbox/` and review weekly

```bash
rg -n "keyword" 05_Resources/network/people
rg -n "#resource/intro" 05_Resources/network/people
```

### AI native (recommended)

- Use `AGENTS.md` to pin constraints (boundaries, naming, safety baseline, checks).
- Use `00_Protocol/AGENTS.md.template` as a starting point: keep `00_Protocol/` “protocol only”, and put executable skills/scripts in `06_Infra/`.

### Language switch (optional)

Switch key docs (README / prompts / skills / selected templates & examples) via `06_Infra/i18n/`:

- List languages: `python3 06_Infra/i18n/switch_language.py --list`
- Switch to Chinese: `python3 06_Infra/i18n/switch_language.py --lang zh --apply --backup`
- Switch to English: `python3 06_Infra/i18n/switch_language.py --lang en --apply --backup`

### Clean examples (optional)

This repo ships with a small set of **sanitized examples** (people card / projects / desires / profile) to demonstrate structure. You can archive-clean them and restore anytime:

- Dry-run: `python3 06_Infra/cleanup_examples.py`
- Apply (archive & restorable): `python3 06_Infra/cleanup_examples.py --apply`
- List archives: `python3 06_Infra/cleanup_examples.py --list-archives`
- Restore: `python3 06_Infra/cleanup_examples.py --restore <timestamp> --apply` (add `--force` if needed)

---

## Core workflows

| Workflow | Entry | Purpose / cadence |
|---|---|---|
| Desires | [`02_Desires/README.md`](02_Desires/README.md) | monthly/quarterly review of drivers |
| Inbox | [`01_Inbox/README.md`](01_Inbox/README.md) | weekly: turn into objects or delete |
| Personal CRM | [`05_Resources/network/index.md`](05_Resources/network/index.md) | when you need intros / recall / follow-up |
| Projects (TPCD) | [`03_Goal-Projects/README.md`](03_Goal-Projects/README.md) | one goal = one project folder |
| Usage | [`00_Protocol/USAGE.md`](00_Protocol/USAGE.md) | onboarding & conventions |
| Privacy baseline | [`00_Protocol/PRIVACY.md`](00_Protocol/PRIVACY.md) | read before publishing |

---

## How to publish

If this template lives inside a larger private repo, and you want **zero Git history** (e.g. the parent repo contains sensitive history), do a clean export (single commit):

```bash
# 1) Copy into a new directory (without .git)
rsync -a --exclude '.git' --exclude '.memo_examples_archive' MEMO/public/repo/ /path/to/memo-public-repo/

# 2) Init and push to GitHub (public)
cd /path/to/memo-public-repo
git init -b main
git add -A
git commit -m "Initial public template"
git remote add origin <your-github-repo-url>
git push -u origin main
```

If you are sure the history of `MEMO/public/repo/` itself is safe to publish, you can publish it via `git subtree`:

```bash
git subtree split --prefix MEMO/public/repo -b memo-public
git push <your-remote> memo-public:main
```

---

## License

MIT
