#!/usr/bin/env python3
"""Prepare a readable, information-preserving markdown draft from SRT.

Usage:
  python3 srt_prepare.py input.srt [-o output.prepared.md] [--merge-gap-sec 15]
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path

TIME_RE = re.compile(
    r"(?P<start>\d{2}:\d{2}:\d{2})(?:[,\.]\d{3})?\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2})(?:[,\.]\d{3})?"
)
SPEAKER_RE = re.compile(r"^\s*([^:：\n]{1,40})[：:]\s*(.+)$")


@dataclass
class Segment:
    start: str
    end: str
    start_sec: int
    end_sec: int
    speaker: str
    text: str


def ts_to_sec(ts: str) -> int:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def parse_srt(content: str) -> list[Segment]:
    blocks = re.split(r"\n\s*\n+", content.strip())
    segments: list[Segment] = []

    for block in blocks:
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not lines:
            continue

        time_idx = -1
        start = end = ""
        for idx, line in enumerate(lines):
            m = TIME_RE.search(line)
            if m:
                time_idx = idx
                start = m.group("start")
                end = m.group("end")
                break

        if time_idx < 0:
            continue

        text_lines = lines[time_idx + 1 :]
        if not text_lines:
            continue

        raw_text = " ".join(text_lines)
        raw_text = re.sub(r"\s+", " ", raw_text).strip()
        if not raw_text:
            continue

        speaker = "未标注说话人"
        text = raw_text
        sm = SPEAKER_RE.match(raw_text)
        if sm:
            speaker = sm.group(1).strip()
            text = sm.group(2).strip()

        segments.append(
            Segment(
                start=start,
                end=end,
                start_sec=ts_to_sec(start),
                end_sec=ts_to_sec(end),
                speaker=speaker,
                text=text,
            )
        )

    return segments


def merge_segments(segments: list[Segment], merge_gap_sec: int) -> list[Segment]:
    if not segments:
        return []

    merged: list[Segment] = [segments[0]]
    for seg in segments[1:]:
        prev = merged[-1]
        gap = seg.start_sec - prev.end_sec
        if seg.speaker == prev.speaker and gap <= merge_gap_sec:
            prev.text = f"{prev.text} {seg.text}".strip()
            prev.end = seg.end
            prev.end_sec = seg.end_sec
        else:
            merged.append(seg)

    for seg in merged:
        seg.text = re.sub(r"\s+", " ", seg.text).strip()

    return merged


def render_markdown(src: Path, segments: list[Segment], merged: list[Segment]) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out: list[str] = []

    out.append("# Transcript Prepared Draft")
    out.append("")
    out.append(f"> Source: `{src}`")
    out.append(f"> Generated: {now}")
    out.append(f"> Raw segments: {len(segments)}")
    out.append(f"> Merged turns: {len(merged)}")
    out.append("")

    out.append("## 1) Chronological Segments (Lossless Cleanup)")
    out.append("")
    for i, seg in enumerate(segments, start=1):
        out.append(f"{i}. `[{seg.start} - {seg.end}]` **{seg.speaker}**: {seg.text}")
    out.append("")

    out.append("## 2) Merged Speaker Turns (Editing Draft)")
    out.append("")
    for i, seg in enumerate(merged, start=1):
        out.append(f"{i}. `[{seg.start} - {seg.end}]` **{seg.speaker}**: {seg.text}")
    out.append("")

    out.append("## 3) Editing Notes")
    out.append("")
    out.append("- Keep complete information coverage when polishing.")
    out.append("- Mark uncertain tokens with `[疑似: ...]` instead of deleting content.")
    out.append("- Preserve chronology and ownership statements.")
    out.append("")

    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare markdown draft from SRT transcript.")
    parser.add_argument("input", type=Path, help="Input .srt file")
    parser.add_argument("-o", "--output", type=Path, help="Output markdown path")
    parser.add_argument(
        "--merge-gap-sec",
        type=int,
        default=15,
        help="Merge adjacent same-speaker segments within this gap (seconds)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input not found: {args.input}")

    content = args.input.read_text(encoding="utf-8", errors="ignore")
    segments = parse_srt(content)
    merged = merge_segments(segments, args.merge_gap_sec)

    output = args.output
    if output is None:
        output = args.input.with_suffix(args.input.suffix + ".prepared.md")

    md = render_markdown(args.input, segments, merged)
    output.write_text(md, encoding="utf-8")
    print(f"Wrote: {output}")
    print(f"Segments: {len(segments)} | Merged: {len(merged)}")


if __name__ == "__main__":
    main()
