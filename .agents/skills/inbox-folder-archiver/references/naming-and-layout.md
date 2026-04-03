# Naming and Layout

## Folder Naming

- Prefer lowercase hyphen slug.
- Keep names concise and domain-informative.
- Example:
  - `2025-06-shanghai-fdeent-septoplasty-xiaohongshu`

## Raw File Naming

- Preserve source files as ordered raw records:
  - `raw-01-<short-name>.<ext>`
  - `raw-02-<short-name>.<ext>`
- Keep extension unchanged.
- Keep ordering stable by source chronology or capture sequence.

## Destination Layout

Use dynamic routing, then place files as:

```text
<destination-root>/<topic-slug>/
├── README.md
├── <topic>.v1.json
└── raw-*.*
```

For case libraries, prefer:

```text
05_Resources/<domain>/cases/<topic-slug>/
```

## Collision Handling

- If destination folder exists and is unrelated, append suffix:
  - `<topic-slug>-v2`
- Note collision handling in final report.
