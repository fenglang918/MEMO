#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}$")
PULL_ID_RE = re.compile(r"APPLE_PULL_ID:([a-f0-9]{16})")


@dataclass
class PulledEvent:
    pull_id: str
    calendar: str
    title: str
    start_day: str
    start_at: str
    all_day: bool
    uid: str


APPLE_PULL_SCRIPT = r'''
on pad2(n)
  if n < 10 then return "0" & (n as text)
  return n as text
end pad2

on replaceText(findText, replaceText, sourceText)
  set tid to AppleScript's text item delimiters
  set AppleScript's text item delimiters to findText
  set textItems to text items of sourceText
  set AppleScript's text item delimiters to replaceText
  set sourceText to textItems as text
  set AppleScript's text item delimiters to tid
  return sourceText
end replaceText

on sanitizeField(valueText)
  set t to valueText as text
  set t to my replaceText(linefeed, " ", t)
  set t to my replaceText(return, " ", t)
  set t to my replaceText("|||", " ", t)
  return t
end sanitizeField

on isoDateStart(isoText)
  set y to (text 1 thru 4 of isoText) as integer
  set m to (text 6 thru 7 of isoText) as integer
  set d to (text 9 thru 10 of isoText) as integer
  set dt to (current date)
  set year of dt to y
  set month of dt to m
  set day of dt to d
  set time of dt to 0
  return dt
end isoDateStart

on isoDateEnd(isoText)
  set dt to my isoDateStart(isoText)
  set time of dt to 86399
  return dt
end isoDateEnd

on run argv
  if (count of argv) < 3 then error "usage: osascript <from_yyyy_mm_dd> <to_yyyy_mm_dd> <comma_calendars>"
  set fromISO to item 1 of argv
  set toISO to item 2 of argv
  set calendarCsv to item 3 of argv
  set fromDate to my isoDateStart(fromISO)
  set toDate to my isoDateEnd(toISO)

  set tid to AppleScript's text item delimiters
  set AppleScript's text item delimiters to ","
  set calendarNames to text items of calendarCsv
  set AppleScript's text item delimiters to tid

  set outText to ""
  tell application "Calendar"
    repeat with calName in calendarNames
      set calText to calName as text
      if calText is not "" and (exists calendar calText) then
        set evs to every event of calendar calText whose start date ≥ fromDate and start date ≤ toDate
        repeat with ev in evs
          set descText to ""
          try
            set descText to description of ev
          end try
          if descText does not contain "[ME_SYNC]" then
            set sd to start date of ev
            set y to year of sd as integer
            set mo to month of sd as integer
            set dd to day of sd as integer
            set hh to hours of sd as integer
            set mm to minutes of sd as integer
            set dayText to (y as text) & "-" & my pad2(mo) & "-" & my pad2(dd)
            set atText to dayText & " " & my pad2(hh) & ":" & my pad2(mm)

            set uidText to ""
            try
              set uidText to uid of ev as text
            end try

            set summaryText to my sanitizeField(summary of ev as text)
            set uidText to my sanitizeField(uidText)
            set lineText to uidText & "|||" & calText & "|||" & dayText & "|||" & atText & "|||" & ((allday event of ev) as text) & "|||" & summaryText
            set outText to outText & lineText & linefeed
          end if
        end repeat
      end if
    end repeat
  end tell
  return outText
end run
'''


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull manual Apple Calendar events back into master-schedule inbox.md.",
    )
    parser.add_argument(
        "--inbox",
        default="08_Operations/00_Master-Schedule/inbox.md",
        help="Target inbox markdown path",
    )
    parser.add_argument(
        "--from-date",
        default=date.today().isoformat(),
        help="Include events on/after this date (YYYY-MM-DD), default: today",
    )
    parser.add_argument(
        "--to-date",
        default=(date.today() + timedelta(days=365)).isoformat(),
        help="Include events on/before this date (YYYY-MM-DD), default: today+365d",
    )
    parser.add_argument(
        "--calendars",
        default="Work,Personal,Explore,Inbox",
        help="Comma-separated calendar names to pull from",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview imported lines only, do not modify inbox",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed event lines",
    )
    return parser.parse_args()


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def run_osascript(script: str, args: list[str]) -> str:
    proc = subprocess.run(
        ["osascript", "-", *args],
        input=script,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "AppleScript pull failed")
    return proc.stdout.strip()


def build_pull_id(uid: str, calendar: str, start_at: str, title: str) -> str:
    base = uid.strip() if uid.strip() else f"{calendar}|{start_at}|{title}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()[:16]


def parse_pulled_events(raw_text: str) -> list[PulledEvent]:
    events: list[PulledEvent] = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|||", 5)
        if len(parts) != 6:
            continue

        uid, calendar, start_day, start_at, all_day_raw, title = [part.strip() for part in parts]
        if not DATE_RE.match(start_day):
            continue
        if not DATE_TIME_RE.match(start_at):
            start_at = f"{start_day} 00:00"
        all_day = all_day_raw.lower() == "true"
        pull_id = build_pull_id(uid=uid, calendar=calendar, start_at=start_at, title=title)
        events.append(
            PulledEvent(
                pull_id=pull_id,
                calendar=calendar,
                title=title or "Untitled event",
                start_day=start_day,
                start_at=start_at,
                all_day=all_day,
                uid=uid,
            )
        )
    events.sort(key=lambda e: (e.start_at, e.calendar, e.title, e.pull_id))
    return events


def load_existing_pull_ids(inbox_path: Path) -> set[str]:
    if not inbox_path.exists():
        return set()
    text = inbox_path.read_text(encoding="utf-8")
    return set(PULL_ID_RE.findall(text))


def render_inbox_line(event: PulledEvent) -> str:
    when_text = event.start_day if event.all_day else event.start_at
    uid_text = f", uid={event.uid}" if event.uid else ""
    return (
        f"- [ ] {when_text} | [{event.calendar}] {event.title} | "
        f"Apple Calendar 手动新增（calendar={event.calendar}{uid_text}） "
        f"<!-- APPLE_PULL_ID:{event.pull_id} -->"
    )


def append_lines(inbox_path: Path, lines: list[str]) -> None:
    inbox_path.parent.mkdir(parents=True, exist_ok=True)
    if inbox_path.exists():
        body = inbox_path.read_text(encoding="utf-8")
    else:
        body = "# Schedule Inbox\n\n临时时间项，确认后再搬运到 `calendar.md` / `milestones.md`。\n\n"
    if body and not body.endswith("\n"):
        body += "\n"
    body += "\n".join(lines) + "\n"
    inbox_path.write_text(body, encoding="utf-8")


def main() -> None:
    args = parse_args()
    from_date_value = parse_iso_date(args.from_date)
    to_date_value = parse_iso_date(args.to_date)
    if to_date_value < from_date_value:
        raise SystemExit("Invalid date range: --to-date cannot be earlier than --from-date")

    repo_root = Path(".").resolve()
    inbox_path = (repo_root / args.inbox).resolve()
    calendars = [part.strip() for part in args.calendars.split(",") if part.strip()]
    if not calendars:
        raise SystemExit("No calendars configured. Use --calendars with comma-separated names.")

    raw_output = run_osascript(
        APPLE_PULL_SCRIPT,
        [from_date_value.isoformat(), to_date_value.isoformat(), ",".join(calendars)],
    )
    pulled = parse_pulled_events(raw_output)
    existing_pull_ids = load_existing_pull_ids(inbox_path)

    imported: list[PulledEvent] = []
    skipped_existing = 0
    for event in pulled:
        if event.pull_id in existing_pull_ids:
            skipped_existing += 1
            continue
        imported.append(event)

    if args.verbose:
        for event in imported:
            print(f"[PULL_PLAN] {render_inbox_line(event)}")

    if args.dry_run:
        print(
            "[ME_APPLE_PULL_SUMMARY] "
            + f"inbox={inbox_path} "
            + f"calendars={','.join(calendars)} "
            + f"from={from_date_value.isoformat()} "
            + f"to={to_date_value.isoformat()} "
            + f"pulled_total={len(pulled)} "
            + f"imported={len(imported)} "
            + f"skipped_existing={skipped_existing} "
            + "result=dry-run"
        )
        return

    if imported:
        append_lines(inbox_path, [render_inbox_line(event) for event in imported])

    print(
        "[ME_APPLE_PULL_SUMMARY] "
        + f"inbox={inbox_path} "
        + f"calendars={','.join(calendars)} "
        + f"from={from_date_value.isoformat()} "
        + f"to={to_date_value.isoformat()} "
        + f"pulled_total={len(pulled)} "
        + f"imported={len(imported)} "
        + f"skipped_existing={skipped_existing} "
        + "result=ok"
    )
    if imported:
        print(f"[OK] imported={len(imported)} into inbox")


if __name__ == "__main__":
    main()
