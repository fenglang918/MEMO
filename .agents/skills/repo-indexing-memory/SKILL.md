---
name: repo-indexing-memory
description: Build and validate repo-level concept-to-evidence indexing outputs for `06_Infra/indexing/` using `build_repo_concept_index.py` with default `v1_1` policy, optional `v1` fallback comparison, and actionable regression summary. Use when the user asks to run/update indexing, check link quality (`error`/`note`), compare profiles, or refresh indexing artifacts/docs after protocol/content changes.
---

# Repo Indexing Memory

Run the repository indexing pipeline in a deterministic way, keep outputs in canonical paths, and summarize quality/regression signals for decision making.

## Workflow

1. Confirm repo root is the current working directory.
2. Run default build (`v1_1`) and write canonical outputs:
   - `06_Infra/indexing/repo-concept-index.v1.json`
   - `06_Infra/indexing/repo-concept-index.v1.md`
   - `06_Infra/indexing/reports/link-check.v1.md`
   - `06_Infra/indexing/reports/index-summary.v1_1.json`
3. If the user asks for comparison or regression check, run `v1` into `/tmp/*` and compare:
   - evidence total
   - code path `error` and `note`
   - markdown link `error` and `note`
4. Report findings as:
   - What changed
   - What improved/regressed
   - Which files are updated
5. If behavior/flags changed, sync docs:
   - `06_Infra/indexing/README.md`
   - `00_Protocol/schemas/indexing-contract.v1.md`
   - relevant plan doc under `develop/plans/`

## Commands

Default build (`v1_1`):

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --summary-json 06_Infra/indexing/reports/index-summary.v1_1.json
```

Comparison baseline (`v1`, temporary outputs):

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1 \
  --out-json /tmp/repo-concept-index.v1.compare.json \
  --out-md /tmp/repo-concept-index.v1.compare.md \
  --link-report /tmp/link-check.v1.compare.md \
  --summary-json /tmp/index-summary.v1.compare.json
```

Scope-only build:

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --scope <subtree-path> \
  --out-json /tmp/repo-concept-index.scope.json \
  --out-md /tmp/repo-concept-index.scope.md \
  --link-report /tmp/link-check.scope.md \
  --summary-json /tmp/index-summary.scope.json
```

## Guardrails

- Always use `06_Infra/indexing/scripts/build_repo_concept_index.py` as the single entrypoint.
- Prefer `v1_1` unless the user explicitly asks for fallback.
- Do not overwrite canonical outputs with `v1` comparison artifacts.
- Treat `error` as actionable breakage; treat `note` as low-priority/template-like unless user asks to clean all.
- Keep summaries concise and numeric.

## References

- `references/runbook.md`: command snippets and metric interpretation templates.
