# Example: Medical Case Archive Mapping

This example mirrors the current repository archive for septoplasty notes.

## Source

```text
01_Inbox/鼻中隔偏曲手术 Case/
├── 1.md
└── 2.md
```

## Archived Destination

```text
05_Resources/medical/cases/2025-06-shanghai-fdeent-septoplasty-xiaohongshu/
├── README.md
├── case.v1.json
├── raw-01-preop-post.md
└── raw-02-op-post-and-comments.md
```

## Backlink Update

Added links under:

`05_Resources/medical/doctors.md`

pointing to:

- `05_Resources/medical/cases/2025-06-shanghai-fdeent-septoplasty-xiaohongshu/README.md`
- `05_Resources/medical/cases/2025-06-shanghai-fdeent-septoplasty-xiaohongshu/case.v1.json`

## Reporting Example

- Routing reason: external medical experience sample -> reusable medical resource case library.
- Data preservation: original files kept as `raw-*`.
- Structured outputs: `README.md` + `case.v1.json`.
