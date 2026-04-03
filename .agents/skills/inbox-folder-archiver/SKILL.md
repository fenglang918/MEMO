---
name: inbox-folder-archiver
description: Archive a folder dropped into `01_Inbox/` into a proper long-term domain directory with deterministic renaming, raw preservation (`raw-*`), structured outputs (`README.md` + `*.v1.json`), and index backlinks. Use when users ask to整理/归档/重命名/结构化某个 Inbox 文件夹，或要求把临时收集材料迁移到 `05_Resources` / `03_Goal-Projects` / `04_Assets` 等稳定位置。
---

# Inbox Folder Archiver

Use this workflow to convert temporary Inbox folders into stable, searchable repo records without losing source material.

## Protocol First

1. Read `00_Protocol/schemas/protocol-federation-map.v1.md`.
2. Confirm content-domain semantics from `00_Protocol/schemas/repo-contents-contract.v1.md`.
3. Only then inspect the target Inbox folder and decide destination.
4. Never claim "no suitable destination" before protocol + minimal repo search.

## Input Contract

Collect and restate these inputs before mutation:

- `source_dir`: folder under `01_Inbox/` to process
- `routing_note`: why the destination domain is chosen
- `raw_policy`: default is move + preserve as `raw-*`
- `output_bundle`: always `README.md` + `*.v1.json` + `raw-*`
- `index_backlink_target`: which upper-level index/README should be updated

If `source_dir` is not under `01_Inbox/`, stop and ask for confirmation.

## Dynamic Routing

Dynamic routing is allowed. Choose one destination root by content intent:

- `05_Resources/` for reusable external references, contacts, tools, doctors, case libraries
- `03_Goal-Projects/` for active project decision/process artifacts
- `04_Assets/` for stable personal facts, long-term owned records
- keep inside `01_Inbox/` only if clearly not ready for archiving

When routing is ambiguous:

1. propose one recommended destination
2. list one alternative
3. include explicit routing reason in output report

Do not split a single source folder into multiple destination roots unless user requests it.

## Normalization

Normalize folder and filenames before final write:

1. Destination folder name uses lowercase hyphen slug when feasible.
2. Preserve source material as `raw-*` filenames in stable order:
   - `raw-01-...`
   - `raw-02-...`
3. Keep original extensions.
4. Avoid destructive overwrite:
   - if destination exists, append suffix like `-v2` and explain in report.

Detailed rules: `references/naming-and-layout.md`.

## Structured Output

Every archived folder must contain:

1. `README.md` with:
   - purpose and boundary
   - source mapping table (`source -> archived file`)
   - structured summary (timeline/costs/signals if applicable)
   - uncertainty/risk notes
2. one `*.v1.json` file (domain fields are flexible) with minimum keys:
   - `id`
   - `kind`
   - `status`
   - `snapshot_date`
   - `source` (platform/origin/raw_files)
   - `evidence_quality` or equivalent boundary field
3. preserved `raw-*` source files

Template snippets: `references/output-templates.md`.

## Index Backlink

After archive write, update one upstream index entry in destination domain.

Examples:

- domain `README.md`
- `cases/README.md`
- other aggregator index files

The backlink must include the exact relative path to the archived folder.

## Validation

Before finalizing:

1. Confirm source folder is no longer stranded in `01_Inbox/` (unless user asked copy-mode).
2. Confirm all expected files exist in destination (`README.md`, `*.v1.json`, `raw-*`).
3. Confirm every new relative link resolves.
4. Confirm no raw source data is lost.
5. Confirm report includes routing reason and rename mapping.

Use `references/workflow-checklist.md` as runbook.

## Report

Return a concise report with:

1. source -> destination path
2. rename mapping table
3. routing reason
4. files created/updated
5. validation result

## References

- `references/workflow-checklist.md`
- `references/naming-and-layout.md`
- `references/output-templates.md`
- `references/examples-medical-case.md`
