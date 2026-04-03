# Output Templates

## README.md Template

```md
---
id: <archive-id>
kind: <archive-kind>
status: archived
last_updated: YYYY-MM-DD
---

# <Title>

## Purpose and Boundary

- Purpose: <why archived>
- Boundary: <what this is NOT>

## Source Mapping

| Source | Archived |
|---|---|
| <original path/file> | <raw-01-...> |

## Structured Summary

- Context:
- Key facts:
- Timeline:
- Costs/metrics:

## Uncertainty and Risk

- <uncertainty 1>
- <uncertainty 2>
```

## `*.v1.json` Template

```json
{
  "id": "<archive-id>",
  "kind": "<archive-kind>",
  "status": "archived",
  "snapshot_date": "YYYY-MM-DD",
  "source": {
    "origin": "<platform-or-channel>",
    "raw_files": [
      "raw-01-<name>",
      "raw-02-<name>"
    ]
  },
  "payload": {
    "summary": "<domain-specific content>"
  },
  "evidence_quality": {
    "level": "<self-report|mixed|official>",
    "limitations": [
      "<limitation>"
    ]
  }
}
```

## Minimum Required JSON Keys

- `id`
- `kind`
- `status`
- `snapshot_date`
- `source`
- one boundary key such as `evidence_quality` or `limitations`
