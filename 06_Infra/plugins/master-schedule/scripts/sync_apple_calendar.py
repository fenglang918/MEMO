#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

from build_apple_calendar_ics import CalendarEvent, load_events, month_end_exclusive


@dataclass
class AppleEvent:
    id: str
    title: str
    start_date: str
    end_date: str
    description: str


@dataclass
class SyncStats:
    total_seen: int = 0
    synced: int = 0
    skipped_past: int = 0
    skipped_future: int = 0
    skipped_done: int = 0
    skipped_title: int = 0
    skipped_calendar: int = 0

    @property
    def skipped(self) -> int:
        return (
            self.skipped_past
            + self.skipped_future
            + self.skipped_done
            + self.skipped_title
            + self.skipped_calendar
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync future master-schedule events to Apple Calendar via Calendar.app.",
    )
    parser.add_argument(
        "--calendar",
        default="08_Operations/00_Master-Schedule/calendar.md",
        help="Path to source calendar markdown",
    )
    parser.add_argument(
        "--apple-calendar",
        default="Home",
        help="Target Apple Calendar name when --routing-mode=single",
    )
    parser.add_argument(
        "--routing-mode",
        choices=["single", "by-project", "by-quadrant", "by-type"],
        default="by-type",
        help="Routing mode: single calendar, by #proj/#project tag, by #q1~#q4 quadrant tag, or by #type/... tag",
    )
    parser.add_argument(
        "--inbox-calendar",
        default="Inbox",
        help="Fallback calendar when no routing tag is found in by-project / by-quadrant / by-type mode",
    )
    parser.add_argument(
        "--work-calendar",
        default="Work",
        help="Target calendar for #type/work when --routing-mode=by-type",
    )
    parser.add_argument(
        "--personal-calendar",
        default="Personal",
        help="Target calendar for #type/personal when --routing-mode=by-type",
    )
    parser.add_argument(
        "--explore-calendar",
        default="Explore",
        help="Target calendar for #type/explore when --routing-mode=by-type",
    )
    parser.add_argument(
        "--require-existing-calendars",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Require target calendars to already exist; default true for by-project/by-quadrant/by-type",
    )
    parser.add_argument(
        "--auto-create-missing-calendars",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Try to create missing target calendars before sync",
    )
    parser.add_argument(
        "--calendar-account",
        default="iCloud",
        help="Calendar account name for auto-creation target (e.g. iCloud, On My Mac)",
    )
    parser.add_argument(
        "--include-done",
        action="store_true",
        help="Include completed tasks",
    )
    parser.add_argument(
        "--from-date",
        default=date.today().isoformat(),
        help="Sync events on/after this date (YYYY-MM-DD), default: today",
    )
    parser.add_argument(
        "--to-date",
        default="",
        help="Sync events on/before this date (YYYY-MM-DD), optional",
    )
    parser.add_argument(
        "--title-contains",
        default="",
        help="Only sync tasks whose title contains this text (case-insensitive)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be synced without touching Calendar",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print filtered event details",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Only validate routing and calendar existence; do not write Calendar",
    )
    parser.add_argument(
        "--managed-calendars-state",
        default="06_Infra/plugins/master-schedule/state/apple-managed-calendars.txt",
        help="State file for managed calendars (used by full-coverage cleanup strategy)",
    )
    return parser.parse_args()


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def event_to_apple_event(event: CalendarEvent) -> AppleEvent:
    start_day = datetime.strptime(event.date, "%Y-%m-%d").date()
    end_day = month_end_exclusive(start_day) if event.month_only else (start_day + timedelta(days=1))

    title = event.title
    if event.month_only:
        title = f"[MONTH] {title}"
    if event.done:
        title = f"[DONE] {title}"

    description_lines: list[str] = [
        "[ME_SYNC]",
        f"id: {event.id}",
        f"created_from: {event.created_from}",
    ]
    if event.tags:
        description_lines.append("tags: " + ", ".join(f"#{t}" for t in event.tags))
    if event.sources:
        description_lines.append("sources:")
        description_lines.extend(f"- {s}" for s in event.sources)
    if event.month_only:
        description_lines.append("month_only: true")

    return AppleEvent(
        id=event.id,
        title=title,
        start_date=start_day.isoformat(),
        end_date=end_day.isoformat(),
        description="\n".join(description_lines),
    )


def matches_title_filter(event: CalendarEvent, title_contains: str) -> bool:
    if not title_contains:
        return True
    return title_contains.casefold() in event.title.casefold()


def to_filtered_events(
    events: list[CalendarEvent],
    include_done: bool,
    from_date_value: date,
    to_date_value: date | None,
    title_contains: str,
) -> tuple[list[CalendarEvent], SyncStats]:
    filtered: list[CalendarEvent] = []
    stats = SyncStats()

    for event in events:
        stats.total_seen += 1
        start_day = datetime.strptime(event.date, "%Y-%m-%d").date()
        if start_day < from_date_value:
            stats.skipped_past += 1
            continue
        if to_date_value is not None and start_day > to_date_value:
            stats.skipped_future += 1
            continue
        if event.done and not include_done:
            stats.skipped_done += 1
            continue
        if not matches_title_filter(event, title_contains):
            stats.skipped_title += 1
            continue

        filtered.append(event)

    filtered.sort(key=lambda e: (e.date, e.id))
    return filtered, stats


def _normalize_tag_token(token: str) -> str:
    value = token.strip()
    value = value.lstrip("#")
    return value.strip(" \t,:;，；")


def project_calendar_name(tags: list[str], inbox_calendar: str) -> str:
    for token in tags:
        normalized = _normalize_tag_token(token)
        lowered = normalized.lower()
        if lowered.startswith("proj/"):
            name = normalized.split("/", 1)[1].strip()
            if name:
                return name
            return inbox_calendar
        if lowered.startswith("project/"):
            name = normalized.split("/", 1)[1].strip()
            if name:
                return name
            return inbox_calendar
    return inbox_calendar


def quadrant_calendar_name(tags: list[str], inbox_calendar: str) -> str:
    quadrant_map = {
        "q1": "Q1",
        "q2": "Q2",
        "q3": "Q3",
        "q4": "Q4",
    }

    for token in tags:
        normalized = _normalize_tag_token(token).lower()
        if normalized.startswith("q1") and (normalized == "q1" or normalized.startswith("q1/")):
            return quadrant_map["q1"]
        if normalized.startswith("q2") and (normalized == "q2" or normalized.startswith("q2/")):
            return quadrant_map["q2"]
        if normalized.startswith("q3") and (normalized == "q3" or normalized.startswith("q3/")):
            return quadrant_map["q3"]
        if normalized.startswith("q4") and (normalized == "q4" or normalized.startswith("q4/")):
            return quadrant_map["q4"]
    return inbox_calendar


def type_calendar_name(
    tags: list[str],
    inbox_calendar: str,
    work_calendar: str,
    personal_calendar: str,
    explore_calendar: str,
) -> str:
    type_to_calendar = {
        "work": work_calendar,
        "personal": personal_calendar,
        "explore": explore_calendar,
    }

    for token in tags:
        normalized = _normalize_tag_token(token)
        lowered = normalized.lower()
        if lowered.startswith("type/"):
            type_name = lowered.split("/", 1)[1].strip()
            if not type_name:
                return inbox_calendar
            return type_to_calendar.get(type_name, inbox_calendar)
    return inbox_calendar


def route_payload(
    filtered_events: list[CalendarEvent],
    routing_mode: str,
    apple_calendar: str,
    inbox_calendar: str,
    work_calendar: str,
    personal_calendar: str,
    explore_calendar: str,
) -> dict[str, list[AppleEvent]]:
    routed: dict[str, list[AppleEvent]] = {}
    for event in filtered_events:
        if routing_mode == "single":
            target_calendar = apple_calendar
        elif routing_mode == "by-project":
            target_calendar = project_calendar_name(event.tags, inbox_calendar)
        elif routing_mode == "by-quadrant":
            target_calendar = quadrant_calendar_name(event.tags, inbox_calendar)
        elif routing_mode == "by-type":
            target_calendar = type_calendar_name(
                event.tags,
                inbox_calendar,
                work_calendar,
                personal_calendar,
                explore_calendar,
            )
        else:
            raise ValueError(f"Unsupported routing mode: {routing_mode}")
        routed.setdefault(target_calendar, []).append(event_to_apple_event(event))
    return routed


LIST_SCRIPT = r'''
on run argv
  tell application "Calendar"
    set outText to ""
    set allCalendars to every calendar
    repeat with calObj in allCalendars
      set outText to outText & (name of calObj as text) & linefeed
    end repeat
  end tell

  return outText
end run
'''


CLEAN_SCRIPT = r'''
on run argv
  if (count of argv) < 1 then error "usage: osascript <calendar_name>"
  set calName to item 1 of argv
  set deletedCount to 0

  tell application "Calendar"
    set targetCalendar to first calendar whose name is calName
    set oldEvents to every event of targetCalendar
    repeat with ev in oldEvents
      try
        set evDesc to description of ev
        if evDesc contains "[ME_SYNC]" then
          delete ev
          set deletedCount to deletedCount + 1
        end if
      end try
    end repeat
  end tell

  return (deletedCount as text)
end run
'''

CREATE_SCRIPT = r'''
on run argv
  if (count of argv) < 2 then error "usage: osascript <calendar_name> <calendar_account>"
  set calName to item 1 of argv
  set accountName to item 2 of argv

  tell application "Calendar"
    set calNames to name of every calendar
    repeat with calObjName in calNames
      if (calObjName as text) is calName then
        return "exists"
      end if
    end repeat

    try
      make new calendar with properties {name:calName}
    on error errMsg number errNum
      return "create_failed_" & (errNum as text) & ":" & errMsg
    end try

    return "created"
  end tell
end run
'''


ADD_SCRIPT = r'''
on isoDateToDate(isoText)
  set y to (text 1 thru 4 of isoText) as integer
  set m to (text 6 thru 7 of isoText) as integer
  set d to (text 9 thru 10 of isoText) as integer
  set dt to (current date)
  set year of dt to y
  set month of dt to m
  set day of dt to d
  set time of dt to 0
  return dt
end isoDateToDate

on run argv
  if (count of argv) < 5 then error "usage: osascript <calendar_name> <title> <start_date> <end_date> <description>"
  set calName to item 1 of argv
  set titleText to item 2 of argv
  set startISO to item 3 of argv
  set endISO to item 4 of argv
  set descText to item 5 of argv

  set startDate to my isoDateToDate(startISO)
  set endDate to my isoDateToDate(endISO)

  tell application "Calendar"
    set targetCalendar to first calendar whose name is calName
    make new event at end of events of targetCalendar with properties {summary:titleText, start date:startDate, end date:endDate, allday event:true, description:descText}
  end tell

  return "ok"
end run
'''


def run_osascript(script: str, args: list[str]) -> str:
    proc = subprocess.run(
        ["osascript", "-", *args],
        input=script,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "AppleScript sync failed")
    return proc.stdout.strip()


def list_calendar_name_counts() -> dict[str, int]:
    output = run_osascript(LIST_SCRIPT, [])
    names = [line.strip() for line in output.splitlines() if line.strip()]
    counts = Counter(names)
    return dict(counts)


def clean_calendar(calendar_name: str, dry_run: bool) -> int:
    if dry_run:
        return 0
    output = run_osascript(CLEAN_SCRIPT, [calendar_name])
    try:
        return int(output)
    except ValueError:
        return 0


def create_calendar(calendar_name: str, calendar_account: str, dry_run: bool) -> str:
    if dry_run:
        return "would_create"
    return run_osascript(CREATE_SCRIPT, [calendar_name, calendar_account]).strip()


def add_event(calendar_name: str, event: AppleEvent, dry_run: bool, verbose: bool) -> None:
    if verbose:
        print(f"[ADD] {calendar_name}: {event.title} ({event.start_date} -> {event.end_date})")
    if dry_run:
        return
    run_osascript(
        ADD_SCRIPT,
        [
            calendar_name,
            event.title,
            event.start_date,
            event.end_date,
            event.description,
        ],
    )


def load_managed_calendars(state_path: Path) -> set[str]:
    if not state_path.exists():
        return set()
    lines = state_path.read_text(encoding="utf-8").splitlines()
    return {line.strip() for line in lines if line.strip()}


def write_managed_calendars(state_path: Path, calendars: set[str]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = state_path.with_suffix(state_path.suffix + ".tmp")
    body = "\n".join(sorted(calendars))
    if body:
        body += "\n"
    tmp_path.write_text(body, encoding="utf-8")
    tmp_path.replace(state_path)


def format_list(values: list[str]) -> str:
    if not values:
        return "none"
    return ",".join(values)


def format_map(values: dict[str, int]) -> str:
    if not values:
        return "none"
    return ",".join(f"{key}:{values[key]}" for key in sorted(values))


def main() -> None:
    args = parse_args()
    from_date_value = parse_iso_date(args.from_date)
    to_date_value = parse_iso_date(args.to_date) if args.to_date else None
    auto_create = args.auto_create_missing_calendars

    if to_date_value is not None and to_date_value < from_date_value:
        raise SystemExit("Invalid date range: --to-date cannot be earlier than --from-date")

    repo_root = Path(".").resolve()
    calendar_path = (repo_root / args.calendar).resolve()
    state_path = (repo_root / args.managed_calendars_state).resolve()
    if not calendar_path.exists():
        raise SystemExit(f"Missing calendar file: {calendar_path}")

    events = load_events(calendar_path)
    title_contains = args.title_contains.strip()
    filtered_events, stats = to_filtered_events(
        events,
        include_done=args.include_done,
        from_date_value=from_date_value,
        to_date_value=to_date_value,
        title_contains=title_contains,
    )
    routed_payload = route_payload(
        filtered_events,
        routing_mode=args.routing_mode,
        apple_calendar=args.apple_calendar,
        inbox_calendar=args.inbox_calendar,
        work_calendar=args.work_calendar,
        personal_calendar=args.personal_calendar,
        explore_calendar=args.explore_calendar,
    )
    target_calendars = sorted(routed_payload.keys())
    events_per_calendar = {calendar_name: len(payload) for calendar_name, payload in routed_payload.items()}

    require_existing = args.require_existing_calendars
    if require_existing is None:
        require_existing = args.routing_mode in {"by-project", "by-quadrant", "by-type"}

    calendar_counts = list_calendar_name_counts()
    missing_calendars = sorted([name for name in target_calendars if calendar_counts.get(name, 0) == 0])
    ambiguous_calendars = sorted([name for name in target_calendars if calendar_counts.get(name, 0) > 1])
    created_calendars: list[str] = []
    create_failures: list[str] = []

    if auto_create and missing_calendars:
        for calendar_name in missing_calendars:
            try:
                status = create_calendar(calendar_name, args.calendar_account, args.dry_run)
                if status in {"created", "exists", "would_create"}:
                    created_calendars.append(calendar_name)
                else:
                    create_failures.append(f"{calendar_name}:{status}")
            except Exception as exc:
                create_failures.append(f"{calendar_name}:{exc}")

        if create_failures:
            print(
                "[ME_APPLE_SYNC_CREATE] "
                + f"route_mode={args.routing_mode} "
                + f"target_calendars={format_list(target_calendars)} "
                + f"missing_calendars={format_list(missing_calendars)} "
                + f"created_calendars={format_list(created_calendars)} "
                + f"create_failures={','.join(create_failures)} "
                + f"calendar_account={args.calendar_account} "
                + f"dry_run={str(args.dry_run).lower()}"
            )
            raise SystemExit("Calendar preflight failed: cannot create missing calendars. Check account and permissions.")

        if not args.dry_run:
            for name in created_calendars:
                calendar_counts[name] = 1
            missing_calendars = sorted([name for name in target_calendars if calendar_counts.get(name, 0) == 0])

    if args.verbose:
        print("[ME_APPLE_SYNC_FILTER]")
        print(f"total_seen={stats.total_seen}")
        print(f"candidate_after_filters={len(filtered_events)}")
        print(f"skipped_past={stats.skipped_past}")
        print(f"skipped_future={stats.skipped_future}")
        print(f"skipped_done={stats.skipped_done}")
        print(f"skipped_title={stats.skipped_title}")
        print(f"route_mode={args.routing_mode}")
        print(f"target_calendars={format_list(target_calendars)}")
        print(f"events_per_calendar={format_map(events_per_calendar)}")
        for calendar_name in sorted(routed_payload):
            for event in routed_payload[calendar_name]:
                print(f"  [PLAN] {calendar_name} | {event.start_date} | {event.title}")

    if (missing_calendars or ambiguous_calendars) and require_existing:
        print(
            "[ME_APPLE_SYNC_PREFLIGHT] "
            + f"route_mode={args.routing_mode} "
            + f"target_calendars={format_list(target_calendars)} "
            + f"missing_calendars={format_list(missing_calendars)} "
            + f"ambiguous_calendars={format_list(ambiguous_calendars)} "
            + f"auto_create_missing_calendars={str(auto_create).lower()} "
            + f"created_calendars={format_list(created_calendars)} "
            + f"events_per_calendar={format_map(events_per_calendar)} "
            + f"require_existing_calendars={str(require_existing).lower()} "
            + f"preflight_only={str(args.preflight_only).lower()}"
        )
        raise SystemExit(
            "Calendar preflight failed: missing or ambiguous target calendars. "
            "Create/fix calendars in iCloud and retry."
        )

    if (missing_calendars or ambiguous_calendars) and not require_existing:
        dropped = 0
        for calendar_name in (missing_calendars + ambiguous_calendars):
            dropped += len(routed_payload.pop(calendar_name, []))
            events_per_calendar.pop(calendar_name, None)
        stats.skipped_calendar += dropped
        target_calendars = sorted(routed_payload.keys())

    if args.preflight_only:
        stats.synced = sum(len(payload) for payload in routed_payload.values())
        print(
            "[ME_APPLE_SYNC_SUMMARY] "
            + f"route_mode={args.routing_mode} "
            + f"calendar={args.apple_calendar if args.routing_mode == 'single' else 'multi'} "
            + f"inbox_calendar={args.inbox_calendar if args.routing_mode in {'by-project', 'by-quadrant', 'by-type'} else 'none'} "
            + f"type_work_calendar={args.work_calendar if args.routing_mode == 'by-type' else 'none'} "
            + f"type_personal_calendar={args.personal_calendar if args.routing_mode == 'by-type' else 'none'} "
            + f"type_explore_calendar={args.explore_calendar if args.routing_mode == 'by-type' else 'none'} "
            + f"from={from_date_value.isoformat()} "
            + f"to={to_date_value.isoformat() if to_date_value else 'none'} "
            + f"include_done={str(args.include_done).lower()} "
            + f"title_contains={title_contains if title_contains else 'none'} "
            + f"total_seen={stats.total_seen} "
            + f"synced={stats.synced} "
            + f"skipped={stats.skipped} "
            + f"skipped_past={stats.skipped_past} "
            + f"skipped_future={stats.skipped_future} "
            + f"skipped_done={stats.skipped_done} "
            + f"skipped_title={stats.skipped_title} "
            + f"skipped_calendar={stats.skipped_calendar} "
            + f"target_calendars={format_list(target_calendars)} "
            + f"missing_calendars={format_list(missing_calendars)} "
            + f"ambiguous_calendars={format_list(ambiguous_calendars)} "
            + f"auto_create_missing_calendars={str(auto_create).lower()} "
            + f"created_calendars={format_list(created_calendars)} "
            + f"events_per_calendar={format_map(events_per_calendar)} "
            + "cleaned_calendars=none "
            + "clean_skipped_missing=none "
            + "clean_skipped_ambiguous=none "
            + f"managed_state={state_path} "
            + f"require_existing_calendars={str(require_existing).lower()} "
            + f"calendar_account={args.calendar_account} "
            + f"dry_run={str(args.dry_run).lower()} "
            + "preflight_only=true "
            + "result=preflight-ok"
        )
        return

    historical_managed = load_managed_calendars(state_path)
    calendars_to_clean = sorted(historical_managed | set(target_calendars))
    cleaned_calendars: dict[str, int] = {}
    clean_skipped_missing = sorted([name for name in calendars_to_clean if calendar_counts.get(name, 0) == 0])
    clean_skipped_ambiguous = sorted([name for name in calendars_to_clean if calendar_counts.get(name, 0) > 1])
    clean_candidates = [name for name in calendars_to_clean if calendar_counts.get(name, 0) == 1]

    for calendar_name in clean_candidates:
        cleaned_calendars[calendar_name] = clean_calendar(calendar_name, dry_run=args.dry_run)

    synced_count = 0
    for calendar_name in target_calendars:
        payload = routed_payload.get(calendar_name, [])
        for event in payload:
            add_event(calendar_name, event, dry_run=args.dry_run, verbose=args.verbose)
            synced_count += 1

    stats.synced = synced_count
    if not args.dry_run:
        write_managed_calendars(state_path, set(target_calendars))

    result = f"synced={synced_count}" + (" (dry-run)" if args.dry_run else "")

    print(
        "[ME_APPLE_SYNC_SUMMARY] "
        + f"route_mode={args.routing_mode} "
        + f"calendar={args.apple_calendar if args.routing_mode == 'single' else 'multi'} "
        + f"inbox_calendar={args.inbox_calendar if args.routing_mode in {'by-project', 'by-quadrant', 'by-type'} else 'none'} "
        + f"type_work_calendar={args.work_calendar if args.routing_mode == 'by-type' else 'none'} "
        + f"type_personal_calendar={args.personal_calendar if args.routing_mode == 'by-type' else 'none'} "
        + f"type_explore_calendar={args.explore_calendar if args.routing_mode == 'by-type' else 'none'} "
        + f"from={from_date_value.isoformat()} "
        + f"to={to_date_value.isoformat() if to_date_value else 'none'} "
        + f"include_done={str(args.include_done).lower()} "
        + f"title_contains={title_contains if title_contains else 'none'} "
        + f"total_seen={stats.total_seen} "
        + f"synced={stats.synced} "
        + f"skipped={stats.skipped} "
        + f"skipped_past={stats.skipped_past} "
        + f"skipped_future={stats.skipped_future} "
        + f"skipped_done={stats.skipped_done} "
        + f"skipped_title={stats.skipped_title} "
        + f"skipped_calendar={stats.skipped_calendar} "
        + f"target_calendars={format_list(target_calendars)} "
        + f"missing_calendars={format_list(missing_calendars)} "
        + f"ambiguous_calendars={format_list(ambiguous_calendars)} "
            + f"events_per_calendar={format_map(events_per_calendar)} "
            + f"auto_create_missing_calendars={str(auto_create).lower()} "
            + f"created_calendars={format_list(created_calendars)} "
            + f"cleaned_calendars={format_map(cleaned_calendars)} "
            + f"clean_skipped_missing={format_list(clean_skipped_missing)} "
            + f"clean_skipped_ambiguous={format_list(clean_skipped_ambiguous)} "
            + f"managed_state={state_path} "
            + f"require_existing_calendars={str(require_existing).lower()} "
            + f"calendar_account={args.calendar_account} "
            + f"dry_run={str(args.dry_run).lower()} "
            + "preflight_only=false "
            + f"result={result}"
        )

    if not args.dry_run:
        print(f"[OK] {result}, route_mode={args.routing_mode}, calendars={len(target_calendars)}, events={stats.synced}")


if __name__ == "__main__":
    main()
