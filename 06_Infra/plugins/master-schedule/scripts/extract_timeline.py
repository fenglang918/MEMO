#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


DATE_PATTERN = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{4}/\d{2}/\d{2}|\d{4}-\d{2})\b")


@dataclass
class Hit:
    date: str
    rel_path: str
    line_no: int
    line_text: str


def scan_markdown(projects_dir: Path, skip_dir: Path) -> list[Hit]:
    hits: list[Hit] = []
    for md in projects_dir.rglob("*.md"):
        if skip_dir in md.parents:
            continue
        rel = md.relative_to(projects_dir.parent)
        text = md.read_text(encoding="utf-8", errors="ignore")
        for idx, raw in enumerate(text.splitlines(), start=1):
            line = raw.strip()
            if not line:
                continue
            found = DATE_PATTERN.findall(line)
            if not found:
                continue
            for d in found:
                hits.append(
                    Hit(
                        date=d.replace("/", "-"),
                        rel_path=str(rel),
                        line_no=idx,
                        line_text=line,
                    )
                )
    return hits


def render(hits: list[Hit], out_file: Path) -> None:
    hits.sort(key=lambda x: (x.date, x.rel_path, x.line_no))
    lines: list[str] = []
    lines.append("# Auto Timeline (from Projects)")
    lines.append("")
    lines.append("自动生成：从 `03_Goal-Projects/` Markdown 抽取日期行。")
    lines.append("")
    lines.append("使用命令：")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 06_Infra/plugins/master-schedule/scripts/extract_timeline.py")
    lines.append("```")
    lines.append("")
    if not hits:
        lines.append("_No timeline items found._")
    else:
        for item in hits:
            lines.append(
                f"- `{item.date}` | `{item.rel_path}:{item.line_no}` | {item.line_text}"
            )
    lines.append("")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract date-like timeline lines from 03_Goal-Projects."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Path to repo root (default: current directory).",
    )
    parser.add_argument(
        "--output",
        default="08_Operations/00_Master-Schedule/auto-timeline.md",
        help="Output markdown path relative to repo root.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    projects_dir = repo_root / "03_Goal-Projects"
    master_dir = projects_dir / "00_Master-Schedule"
    out_file = repo_root / args.output

    if not projects_dir.exists():
        raise SystemExit(f"Missing directory: {projects_dir}")

    hits = scan_markdown(projects_dir=projects_dir, skip_dir=master_dir)
    render(hits=hits, out_file=out_file)
    print(f"[OK] wrote {out_file} with {len(hits)} item(s)")


if __name__ == "__main__":
    main()

