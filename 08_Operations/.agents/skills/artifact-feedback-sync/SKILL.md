---
name: artifact-feedback-sync
description: "Archive feedback workflows for any deliverable (proposal/document/work): keep a lightweight 3-artifact pattern (raw-dialogue, feedback-log, deliverable internal index), enforce bidirectional links, capture git snapshot at send/record time, and keep private-notes INDEX in sync. Use when users ask to 记录商讨、归档对话、双向索引、标注发送版本、记录 git 快照、或更新 private-notes 索引; reviewers may be mentor/boss/friend/partner/AI."
---

# Artifact Feedback Sync

## Overview

Use this skill to keep feedback loops auditable for any target artifact, not only proposals.  
Create or update three linked artifacts plus INDEX navigation, with a timestamped git snapshot.

## Roles

- Author: the person who sends a deliverable.
- Reviewer: any feedback source (mentor, boss, friend, partner, other AI, etc.).

## Inputs

Required:
- `project_root`: project directory that contains `private-notes/`.
- `artifact_path`: path to the target deliverable file (proposal/doc/work).
- `raw_dialogue_path`: path to raw dialogue markdown file (or target path for creation).
- `feedback_log_path`: path to discussion/feedback markdown file (or target path for creation).
- `external_archive_link`: sent archive link (for example Feishu wiki link).

Optional:
- `recorded_at`: override timestamp (default: now in ISO-8601).
- `repo_root`: git repo root for snapshot (default: auto-detect from `artifact_path`).

## Outputs

- `raw-dialogue` contains:
  - archive link
  - links to artifact and feedback-log
  - artifact git snapshot block
- `feedback-log` contains:
  - links to raw-dialogue and artifact
  - send-version note (archive link + repo reference)
  - artifact git snapshot block
  - time-ordered summary
- `artifact` contains internal index links to raw-dialogue/feedback-log/archive link
- `private-notes/INDEX.md` contains navigation entry consistent with current paths

## Workflow

1. Confirm target paths and keep the pattern lightweight.
2. Capture artifact git snapshot by running:
   - `scripts/capture_file_git_snapshot.sh --repo-root <repo_root> --file-relpath <relpath> --label <artifact_label>`
3. Create or update `raw-dialogue` with canonical section:
   - `## 关联版本与索引（本次发送）`
4. Create or update `feedback-log` with canonical sections:
   - `## 1) 关联文档（双向索引）`
   - `## 2) 发送版本说明（外发存档 + repo 对照）`
   - `## 3) 目标产物 git 快照（记录时刻）`
   - `## 4) 本次反馈时间序（摘要）`
5. Update artifact internal index section:
   - `## 内部索引（仅内部）`
6. Update `private-notes/INDEX.md` navigation entries if paths changed.
7. Validate links by running:
   - `scripts/quick_feedback_link_check.sh --project-root <project_root> --artifact-path <artifact_path> --raw-dialogue-path <raw_dialogue_path> --feedback-log-path <feedback_log_path> [--index-path <index_path>]`

## Default Path Strategy (Reusable)

- Prefer `raw-dialogue` under `private-notes/04-review/`.
- Prefer `feedback-log` under `private-notes/03-proposal/` (or equivalent folder by project convention).
- Keep target artifact near its original authoring folder.
- Keep navigation in `private-notes/INDEX.md`.

Use AgenQA-like paths only as examples, not fixed requirements.

## Rules

- Do not over-map into heavy trace matrices. Keep one concise feedback-log.
- Keep raw-dialogue as evidence-first (verbatim + minimal index block).
- Keep target artifact as outward-facing text with a short internal index block only.
- If git metadata is unavailable, keep snapshot section with `N/A` and reason.
- Do not add extra docs (README/changelog) inside the skill folder.

## Templates And Scripts

- Templates:
  - `references/templates.md`
- Scripts:
  - `scripts/capture_file_git_snapshot.sh` (generic)
  - `scripts/quick_feedback_link_check.sh` (generic)

## Quick Start Commands

```bash
# 1) Capture git snapshot for any artifact
./scripts/capture_file_git_snapshot.sh \
  --repo-root /path/to/repo \
  --file-relpath path/to/any-artifact.md \
  --label artifact

# 2) Validate link consistency across 3 artifacts
./scripts/quick_feedback_link_check.sh \
  --project-root /path/to/project \
  --artifact-path private-notes/03-proposal/work.md \
  --raw-dialogue-path private-notes/04-review/raw-dialogue.md \
  --feedback-log-path private-notes/03-proposal/feedback-log.md \
  --index-path private-notes/INDEX.md
```
