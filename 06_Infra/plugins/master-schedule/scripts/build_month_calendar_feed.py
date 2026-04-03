#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


TASK_LINE_RE = re.compile(r"^-\s*\[([ xX]?)\]\s*`([^`]+)`\s*(.*)$")
HEADER_RE = re.compile(r"^##\s+(\d{4}-\d{2})")
SOURCE_LINE_RE = re.compile(r"^\s*-\s*来源：`([^`]+)`")
DATE_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
EMBED_SOURCE_RE = re.compile(r"\s+-\s*来源：`([^`]+)`\s*$")
TAG_RE = re.compile(r"(?:^|\s)(#(?:tag|proj|project)/[^\s]+)")


@dataclass
class CalendarEvent:
    id: str
    date: str
    month: str
    month_only: bool
    done: bool
    title: str
    tags: list[str]
    source: str | None
    created_from: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a lightweight JS calendar data file from calendar.md",
    )
    parser.add_argument(
        "--calendar",
        default="08_Operations/00_Master-Schedule/calendar.md",
        help="Path to source calendar markdown",
    )
    parser.add_argument(
        "--output",
        default="08_Operations/00_Master-Schedule/calendar-page-data.js",
        help="Output JS file path (default: calendar page data file)",
    )
    return parser.parse_args()


def parse_source_and_clean_title(raw: str) -> tuple[str, str | None]:
    title = raw.strip()
    source: str | None = None

    embedded = EMBED_SOURCE_RE.search(title)
    if embedded:
        source = embedded.group(1).strip()
        title = title[: embedded.start()].rstrip(" -")

    return title, source


def parse_tags_and_clean_title(raw: str) -> tuple[str, list[str]]:
    tags: list[str] = []

    def _replace(match: re.Match[str]) -> str:
        token = match.group(1).strip()
        token = token.rstrip(",;，；")
        if token.startswith("#"):
            token = token[1:]
        if token:
            tags.append(token)
        return " "

    cleaned = TAG_RE.sub(_replace, raw)
    cleaned = " ".join(cleaned.split())
    return cleaned, tags


def load_events(calendar_path: Path) -> list[CalendarEvent]:
    lines = calendar_path.read_text(encoding="utf-8").splitlines()
    current_month = ""
    events: list[CalendarEvent] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        header = HEADER_RE.match(line)
        if header:
            current_month = header.group(1)
            i += 1
            continue

        task_match = TASK_LINE_RE.match(line)
        if task_match:
            raw_status = task_match.group(1)
            date_token = task_match.group(2).strip()
            remainder = task_match.group(3)
            done = bool(raw_status.strip())
            source = None

            if not DATE_DAY_RE.match(date_token) and not DATE_MONTH_RE.match(date_token):
                # skip unknown date formats to avoid bad entries
                i += 1
                continue

            month_only = bool(DATE_MONTH_RE.match(date_token))
            date_value = f"{date_token}-01" if month_only else date_token

            title, embedded_source = parse_source_and_clean_title(remainder)
            title, tags = parse_tags_and_clean_title(title)
            source = embedded_source
            if source is None and i + 1 < len(lines):
                next_line = lines[i + 1]
                source_match = SOURCE_LINE_RE.match(next_line)
                if source_match:
                    source = source_match.group(1).strip()
                    i += 1

            if not title and source is None:
                # keep a minimal fallback title
                title = "无标题任务"

            event_month = date_value[:7]
            normalized_month = date_value[:7]
            if current_month and current_month != normalized_month and not month_only:
                # keep source truth but guard minor format drift
                current_month = normalized_month

            if not current_month:
                current_month = normalized_month
            elif month_only and current_month != normalized_month:
                current_month = normalized_month

            event_id = f"{date_value}_{len(events)+1:03d}"
            events.append(
                CalendarEvent(
                    id=event_id,
                    date=date_value,
                    month=current_month,
                    month_only=month_only,
                    done=done,
                    title=title,
                    tags=tags,
                    source=source,
                    created_from=f"{calendar_path.name}:{i + 1}",
                )
            )

        i += 1

    return events


def to_js_payload(events: list[CalendarEvent]) -> dict[str, object]:
    sorted_events = sorted(
        events,
        key=lambda e: (e.date, e.id),
    )
    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(timespec="seconds"),
        "events": [
            {
                "id": e.id,
                "date": e.date,
                "month": e.month,
                "month_only": e.month_only,
                "done": e.done,
                "title": e.title,
                "tags": e.tags,
                "source": e.source,
                "created_from": e.created_from,
            }
            for e in sorted_events
        ],
    }


def write_js(payload: dict[str, object], output_path: Path) -> None:
    data = json.dumps(payload, ensure_ascii=False, indent=2)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "(function () {\n"
        "  const data = "
        + data.replace("\n", "\n  ")
        + ";\n"
        "  window.ME_CALENDAR_EVENTS = data.events;\n"
        "  window.ME_CALENDAR_DATA_META = {\n"
        "    generated_at: data.generated_at,\n"
        "    count: data.events.length\n"
        "  };\n"
        "}());\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    repo_root = Path(".").resolve()
    calendar_path = (repo_root / args.calendar).resolve()
    output_path = (repo_root / args.output).resolve()

    if not calendar_path.exists():
        raise SystemExit(f"Missing calendar file: {calendar_path}")

    events = load_events(calendar_path)
    payload = to_js_payload(events)
    write_js(payload, output_path)
    print(
        f"[OK] wrote {output_path} "
        f"({payload['generated_at']}), events={len(payload['events'])}"
    )


if __name__ == "__main__":
    main()
