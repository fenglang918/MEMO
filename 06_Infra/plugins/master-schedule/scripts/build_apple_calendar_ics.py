#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


TASK_LINE_RE = re.compile(r"^-\s*\[([ xX]?)\]\s*`([^`]+)`\s*(.*)$")
SOURCE_LINE_RE = re.compile(r"^\s*-\s*来源：`([^`]+)`")
DATE_DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
EMBED_SOURCE_RE = re.compile(r"\s+-\s*来源：`([^`]+)`\s*$")
TAG_RE = re.compile(r"(?:^|\s)(#(?:tag|proj|project|type|q[1-4])(?:/[^\s]+)?)")


@dataclass
class CalendarEvent:
    id: str
    date: str
    month_only: bool
    done: bool
    title: str
    tags: list[str]
    sources: list[str]
    created_from: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Apple Calendar compatible ICS from master schedule markdown.",
    )
    parser.add_argument(
        "--calendar",
        default="08_Operations/00_Master-Schedule/calendar.md",
        help="Path to source calendar markdown",
    )
    parser.add_argument(
        "--output",
        default="08_Operations/00_Master-Schedule/calendar.ics",
        help="Output ICS path",
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
    events: list[CalendarEvent] = []
    i = 0

    while i < len(lines):
        task_match = TASK_LINE_RE.match(lines[i].strip())
        if not task_match:
            i += 1
            continue

        raw_status = task_match.group(1)
        date_token = task_match.group(2).strip()
        remainder = task_match.group(3)
        done = bool(raw_status.strip())
        sources: list[str] = []

        if not DATE_DAY_RE.match(date_token) and not DATE_MONTH_RE.match(date_token):
            i += 1
            continue

        month_only = bool(DATE_MONTH_RE.match(date_token))
        date_value = f"{date_token}-01" if month_only else date_token

        title, embedded_source = parse_source_and_clean_title(remainder)
        title, tags = parse_tags_and_clean_title(title)
        if embedded_source:
            sources.append(embedded_source)

        j = i + 1
        while j < len(lines):
            source_match = SOURCE_LINE_RE.match(lines[j])
            if not source_match:
                break
            source = source_match.group(1).strip()
            if source:
                sources.append(source)
            j += 1

        if j > i + 1:
            i = j - 1

        if not title:
            title = "Untitled task"

        event_id = f"{date_value}_{len(events)+1:03d}"
        events.append(
            CalendarEvent(
                id=event_id,
                date=date_value,
                month_only=month_only,
                done=done,
                title=title,
                tags=tags,
                sources=sources,
                created_from=f"{calendar_path.name}:{i + 1}",
            )
        )
        i += 1

    return events


def escape_ics_text(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", r"\;")
        .replace(",", r"\,")
        .replace("\n", r"\n")
    )


def fold_ics_line(line: str, limit: int = 75) -> list[str]:
    if len(line) <= limit:
        return [line]
    chunks: list[str] = []
    remaining = line
    while len(remaining) > limit:
        chunks.append(remaining[:limit])
        remaining = " " + remaining[limit:]
    chunks.append(remaining)
    return chunks


def month_end_exclusive(start_day: date) -> date:
    if start_day.month == 12:
        return date(start_day.year + 1, 1, 1)
    return date(start_day.year, start_day.month + 1, 1)


def to_ics(events: list[CalendarEvent]) -> str:
    now_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    sorted_events = sorted(events, key=lambda e: (e.date, e.id))

    out: list[str] = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//MEMO Master Schedule//Apple Calendar Export//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:MEMO Master Schedule",
    ]

    for event in sorted_events:
        start_day = datetime.strptime(event.date, "%Y-%m-%d").date()
        end_day = month_end_exclusive(start_day) if event.month_only else (start_day + timedelta(days=1))

        summary = event.title
        if event.month_only:
            summary = f"[MONTH] {summary}"
        if event.done:
            summary = f"[DONE] {summary}"

        desc_lines: list[str] = []
        if event.tags:
            desc_lines.append("tags: " + ", ".join(f"#{t}" for t in event.tags))
        if event.sources:
            desc_lines.append("sources:")
            desc_lines.extend(f"- {s}" for s in event.sources)
        desc_lines.append(f"created_from: {event.created_from}")
        if event.month_only:
            desc_lines.append("month_only: true")
        description = "\n".join(desc_lines)

        categories = ",".join(event.tags) if event.tags else ""
        vevent = [
            "BEGIN:VEVENT",
            f"UID:{event.id}@me-master-schedule",
            f"DTSTAMP:{now_stamp}",
            f"DTSTART;VALUE=DATE:{start_day.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{end_day.strftime('%Y%m%d')}",
            f"SUMMARY:{escape_ics_text(summary)}",
            f"DESCRIPTION:{escape_ics_text(description)}",
            "STATUS:CONFIRMED",
            "TRANSP:OPAQUE",
            f"X-ME-MONTH-ONLY:{'TRUE' if event.month_only else 'FALSE'}",
            f"X-ME-CREATED-FROM:{escape_ics_text(event.created_from)}",
            "END:VEVENT",
        ]
        if categories:
            vevent.insert(-3, f"CATEGORIES:{escape_ics_text(categories)}")

        for raw_line in vevent:
            out.extend(fold_ics_line(raw_line))

    out.append("END:VCALENDAR")
    return "\r\n".join(out) + "\r\n"


def write_ics(content: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def main() -> None:
    args = parse_args()
    repo_root = Path(".").resolve()
    calendar_path = (repo_root / args.calendar).resolve()
    output_path = (repo_root / args.output).resolve()

    if not calendar_path.exists():
        raise SystemExit(f"Missing calendar file: {calendar_path}")

    events = load_events(calendar_path)
    content = to_ics(events)
    write_ics(content, output_path)
    print(f"[OK] wrote {output_path}, events={len(events)}")


if __name__ == "__main__":
    main()
