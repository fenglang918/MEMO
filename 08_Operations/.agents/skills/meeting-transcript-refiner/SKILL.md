---
name: meeting-transcript-refiner
description: Convert machine-generated meeting transcripts (.srt/.vtt/.txt) into (1) full-fidelity polished documents that preserve complete original information and (2) intelligent meeting minutes with decisions, actions, owners, deadlines, risks, and open questions. Use when users ask to整理会议转录、润色口语稿、保留完整信息转文档、或基于转录生成纪要.
---

# Meeting Transcript Refiner

## Overview
Use this skill to process noisy transcript files into two outputs in strict order:
1. Full-fidelity polished transcript document (information-preserving)
2. Intelligent meeting minutes (decision/action oriented)

Always produce output 1 before output 2.

## Workflow

### Step 1: Ingest and Prepare Transcript
1. Identify source file format (`.srt`, `.vtt`, `.txt`).
2. For `.srt`, run:

```bash
python3 08_Operations/.agents/skills/meeting-transcript-refiner/scripts/srt_prepare.py <input.srt>
```

3. Use generated `*.prepared.md` as the working draft.
4. Keep the original transcript file unchanged.

### Step 2: Produce Full-Fidelity Polished Transcript
Use `references/full-fidelity-polish-template.md` and enforce these rules:
1. Preserve all factual information, claims, requests, commitments, and constraints.
2. Keep speaker attribution if present in source.
3. Repair grammar, punctuation, and sentence boundaries.
4. Remove pure filler words only when meaning is unchanged.
5. Mark low-confidence terms as `[疑似: ...]` rather than deleting.
6. Do not compress multiple unique points into one generic sentence.
7. Keep chronology intact.

Definition of done:
1. A reader can recover all key information without reopening raw transcript.
2. The polished text is readable as a document, not fragmented ASR lines.

### Step 3: Produce Intelligent Minutes
Use `references/intelligent-minutes-template.md`.
Extract and structure:
1. Meeting objective and scope
2. Key decisions
3. Action items (`Owner`, `Deadline`, `Deliverable`)
4. Risks/blockers
5. Open questions
6. Next checkpoint

Do not copy transcript verbatim into minutes except for short evidence quotes when needed.

### Step 4: Run Quality Checks
Before finalizing, verify:
1. No important decision or commitment is omitted.
2. Every action item has at least an owner or explicitly marked `TBD`.
3. Dates are explicit (`YYYY-MM-DD`) when source implies timeline.
4. Minutes are traceable to transcript content.

## Output Contract
When the user asks for "整理会议记录" or similar, return both:
1. `polished transcript`
2. `intelligent minutes`

If the user asks only one output, still propose the second as optional next step.

## Resources

### scripts/
- `scripts/srt_prepare.py`: Convert raw `.srt` into a clean chronological draft while preserving details.

### references/
- `references/full-fidelity-polish-template.md`: Template and checklist for full transcript polishing.
- `references/intelligent-minutes-template.md`: Template for decision/action-focused summary.
