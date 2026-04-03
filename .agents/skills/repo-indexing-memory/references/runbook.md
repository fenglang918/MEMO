# Runbook

## Canonical v1_1 run

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --summary-json 06_Infra/indexing/reports/index-summary.v1_1.json
```

## Compare against v1

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1 \
  --out-json /tmp/repo-concept-index.v1.compare.json \
  --out-md /tmp/repo-concept-index.v1.compare.md \
  --link-report /tmp/link-check.v1.compare.md \
  --summary-json /tmp/index-summary.v1.compare.json
```

```bash
python3 - <<'PY'
import json
from pathlib import Path
old = json.loads(Path('/tmp/index-summary.v1.compare.json').read_text())
new = json.loads(Path('06_Infra/indexing/reports/index-summary.v1_1.json').read_text())
print('evidence_total', old['evidence_total'], '->', new['evidence_total'])
print('code_error', old['link_report']['code_paths']['error'], '->', new['link_report']['code_paths']['error'])
print('code_note', old['link_report']['code_paths']['note'], '->', new['link_report']['code_paths']['note'])
print('md_error', old['link_report']['markdown']['error'], '->', new['link_report']['markdown']['error'])
print('md_note', old['link_report']['markdown']['note'], '->', new['link_report']['markdown']['note'])
PY
```

## Interpretation

- `markdown.error`: local markdown links that are broken and should usually be fixed first.
- `code_paths.error`: path-like backtick references likely broken.
- `code_paths.note`: placeholder/template/legacy-style paths; lower priority by default.
- `dropped_by_policy_total`: reduction caused by v1_1 evidence policy; expected to be > 0.
