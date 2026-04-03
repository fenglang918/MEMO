#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path


ENTRY_RE = re.compile(
    r"^\s*(?:(?P<date>\d{4}-\d{2}-\d{2})\s+)?"
    r"(?P<start>\d{1,2}(?::|：)\d{2})\s*(?:-|~|～|—|到|至)\s*"
    r"(?P<end>\d{1,2}(?::|：)\d{2})\s*(?:[-:：]\s*)?(?P<task>.+?)\s*$"
)
PROJECT_TAG_RE = re.compile(r"(?:^|\s)#(?:proj|project)/([^\s#]+)")
YEAR_RE = re.compile(r"^\d{4}$")
MONTH_RE = re.compile(r"^\d{2}$")

CSV_FIELDS = [
    "entry_id",
    "date",
    "start",
    "end",
    "duration_min",
    "task",
    "project",
    "project_path",
    "match_type",
    "confidence",
    "raw_input",
    "created_at",
]

ASCII_STOPWORDS = {
    "and",
    "the",
    "for",
    "with",
    "from",
    "root",
    "refs",
    "readme",
    "offer",
    "plan",
    "work",
    "study",
    "project",
}


@dataclass(frozen=True)
class ProjectMeta:
    name: str
    rel_path: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class ParsedEntry:
    date: date
    start: str
    end: str
    task: str
    duration_min: int


@dataclass(frozen=True)
class MatchResult:
    project: str
    project_path: str
    match_type: str
    confidence: float
    candidate_hints: tuple[tuple[str, float], ...]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record rough time blocks and auto-link them to repo projects.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add one or more time entries.")
    add_parser.add_argument(
        "--entry",
        action="append",
        default=[],
        help='One entry line, e.g. "09:30-11:00 AgenQA 需求梳理"',
    )
    add_parser.add_argument(
        "--from-file",
        default="",
        help="Load entry lines from file (headings/blank lines are ignored).",
    )
    add_parser.add_argument(
        "--date",
        default="",
        help="Fallback date for entries without inline date (YYYY-MM-DD)",
    )
    add_parser.add_argument(
        "--csv",
        default="08_Operations/01_Time-Tracking/time_entries.csv",
        help="Path to time tracking csv file",
    )
    add_parser.add_argument(
        "--default-project",
        default="UNLINKED",
        help="Fallback project when auto-match is uncertain",
    )

    report_parser = subparsers.add_parser("report", help="Generate time investment summary.")
    report_parser.add_argument(
        "--csv",
        default="08_Operations/01_Time-Tracking/time_entries.csv",
        help="Path to time tracking csv file",
    )
    report_parser.add_argument(
        "--range",
        choices=["today", "week", "month", "all"],
        default="week",
        help="Preset date range used when from/to are not provided",
    )
    report_parser.add_argument(
        "--from-date",
        default="",
        help="Start date (YYYY-MM-DD), overrides --range when provided",
    )
    report_parser.add_argument(
        "--to-date",
        default="",
        help="End date (YYYY-MM-DD), overrides --range when provided",
    )
    report_parser.add_argument(
        "--top",
        type=int,
        default=12,
        help="Top N projects to show in report table",
    )
    report_parser.add_argument(
        "--output",
        default="08_Operations/01_Time-Tracking/reports/latest.md",
        help="Markdown report path",
    )
    report_parser.add_argument(
        "--default-project",
        default="UNLINKED",
        help="Fallback project label",
    )

    projects_parser = subparsers.add_parser("projects", help="List detected project catalog.")
    projects_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max projects to print",
    )
    return parser.parse_args()


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_time_token(value: str) -> time:
    normalized = value.replace("：", ":")
    return datetime.strptime(normalized, "%H:%M").time()


def format_hours(minutes: int) -> str:
    return f"{minutes / 60:.2f}"


def normalized_text(value: str) -> str:
    return "".join(
        ch.casefold()
        for ch in value
        if ch.isalnum() or ("\u4e00" <= ch <= "\u9fff")
    )


def looks_good_token(token: str) -> bool:
    token = token.strip()
    if not token:
        return False
    if re.fullmatch(r"[A-Za-z0-9]+", token):
        return len(token) >= 4 and token.casefold() not in ASCII_STOPWORDS
    cjk_count = sum(1 for ch in token if "\u4e00" <= ch <= "\u9fff")
    return cjk_count >= 2


def build_aliases(project_name: str) -> tuple[str, ...]:
    aliases: set[str] = {project_name}
    stripped = re.sub(r"^\d{4}-\d{2}-", "", project_name)
    if stripped and stripped != project_name:
        aliases.add(stripped)

    for token in re.split(r"[-_/]+", stripped):
        if looks_good_token(token):
            aliases.add(token)

    ordered = sorted(aliases, key=lambda x: (-len(x), x.casefold()))
    return tuple(ordered)


def infer_project_from_parts(parts: tuple[str, ...]) -> tuple[str, str] | None:
    if not parts:
        return None
    head = parts[0]
    if head in {"_TEMPLATE", "_docs"}:
        return None

    if head == "evergreen":
        if len(parts) >= 3 and parts[1] == "00__root":
            project_name = parts[2]
            rel_path = str(Path("03_Goal-Projects") / "evergreen" / "00__root" / project_name)
            return project_name, rel_path
        if len(parts) >= 2:
            project_name = parts[1]
            rel_path = str(Path("03_Goal-Projects") / "evergreen" / project_name)
            return project_name, rel_path
        return None

    if len(parts) >= 3 and YEAR_RE.match(parts[0]) and MONTH_RE.match(parts[1]):
        project_name = parts[2]
        rel_path = str(Path("03_Goal-Projects") / parts[0] / parts[1] / project_name)
        return project_name, rel_path

    return None


def load_project_catalog(repo_root: Path) -> list[ProjectMeta]:
    goal_root = repo_root / "03_Goal-Projects"
    if not goal_root.exists():
        return []

    unique: dict[tuple[str, str], ProjectMeta] = {}
    for readme in sorted(goal_root.rglob("README.md")):
        rel = readme.relative_to(repo_root)
        inferred = infer_project_from_parts(rel.parts[1:-1])
        if inferred is None:
            continue
        project_name, rel_path = inferred
        key = (project_name, rel_path)
        unique[key] = ProjectMeta(
            name=project_name,
            rel_path=rel_path,
            aliases=build_aliases(project_name),
        )

    return sorted(unique.values(), key=lambda p: p.name.casefold())


def parse_entry_line(raw_line: str, fallback_date: date | None) -> ParsedEntry:
    matched = ENTRY_RE.match(raw_line.strip())
    if not matched:
        raise ValueError(
            f"Cannot parse line: {raw_line!r}. Expect format like '09:30-11:00 任务描述'"
        )

    date_token = (matched.group("date") or "").strip()
    if date_token:
        target_date = parse_iso_date(date_token)
    elif fallback_date is not None:
        target_date = fallback_date
    else:
        raise ValueError(
            f"Missing date in line: {raw_line!r}. "
            "Use 'YYYY-MM-DD HH:MM-HH:MM ...' or pass --date YYYY-MM-DD"
        )

    start = parse_time_token(matched.group("start"))
    end = parse_time_token(matched.group("end"))
    task = matched.group("task").strip()
    if not task:
        raise ValueError(f"Task description is empty: {raw_line!r}")

    start_dt = datetime.combine(target_date, start)
    end_dt = datetime.combine(target_date, end)
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)
    duration_min = int((end_dt - start_dt).total_seconds() // 60)
    if duration_min <= 0:
        raise ValueError(f"Invalid duration in line: {raw_line!r}")

    return ParsedEntry(
        date=target_date,
        start=f"{start.hour:02d}:{start.minute:02d}",
        end=f"{end.hour:02d}:{end.minute:02d}",
        task=task,
        duration_min=duration_min,
    )


def score_project_match(task_text: str, project: ProjectMeta) -> float:
    raw_cf = task_text.casefold()
    flat = normalized_text(task_text)
    score = 0.0

    for alias in project.aliases:
        alias_cf = alias.casefold()
        alias_flat = normalized_text(alias)
        if not alias_flat:
            continue
        if alias_cf in raw_cf:
            score += 90.0 if alias == project.name else 32.0
            continue
        if alias_flat in flat:
            score += 72.0 if alias == project.name else 24.0

    return score


def detect_project(
    task_text: str,
    projects: list[ProjectMeta],
    default_project: str,
) -> MatchResult:
    explicit = PROJECT_TAG_RE.search(task_text)
    if explicit:
        explicit_project = explicit.group(1).strip().strip(",.;，；")
        return MatchResult(
            project=explicit_project or default_project,
            project_path="",
            match_type="explicit-tag",
            confidence=1.0,
            candidate_hints=(),
        )

    scored: list[tuple[float, ProjectMeta]] = []
    for project in projects:
        score = score_project_match(task_text, project)
        if score > 0:
            scored.append((score, project))

    if not scored:
        return MatchResult(
            project=default_project,
            project_path="",
            match_type="unlinked",
            confidence=0.0,
            candidate_hints=(),
        )

    scored.sort(key=lambda item: (item[0], len(item[1].name)), reverse=True)
    top_score, top_project = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0

    confidence = min(0.95, 0.45 + top_score / 160.0)
    if second_score and top_score - second_score < 28.0:
        confidence = min(confidence, 0.62)

    hints = tuple((item[1].name, round(item[0], 1)) for item in scored[:3])

    if confidence < 0.55:
        return MatchResult(
            project=default_project,
            project_path="",
            match_type="unlinked",
            confidence=0.0,
            candidate_hints=hints,
        )

    return MatchResult(
        project=top_project.name,
        project_path=top_project.rel_path,
        match_type="auto-match",
        confidence=round(confidence, 2),
        candidate_hints=hints,
    )


def normalize_input_line(line: str) -> str:
    stripped = line.strip()
    if not stripped:
        return ""
    if stripped.startswith("#"):
        return ""

    stripped = re.sub(r"^-\s*\[[ xX]?\]\s*", "", stripped)
    stripped = re.sub(r"^[-*]\s+", "", stripped)
    return stripped.strip()


def load_entry_lines(args: argparse.Namespace) -> list[str]:
    lines: list[str] = [line.strip() for line in args.entry if line.strip()]
    if args.from_file:
        path = Path(args.from_file).resolve()
        if not path.exists():
            raise SystemExit(f"Missing --from-file path: {path}")
        for line in path.read_text(encoding="utf-8").splitlines():
            normalized = normalize_input_line(line)
            if normalized:
                lines.append(normalized)
    if not lines:
        raise SystemExit("No entries provided. Use --entry or --from-file.")
    return lines


def ensure_csv(csv_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if csv_path.exists():
        return
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()


def load_existing_ids(csv_path: Path) -> set[str]:
    if not csv_path.exists():
        return set()
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return {row.get("entry_id", "").strip() for row in reader if row.get("entry_id")}


def build_entry_id(parsed: ParsedEntry) -> str:
    key = f"{parsed.date.isoformat()}|{parsed.start}|{parsed.end}|{parsed.task}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def append_rows(csv_path: Path, rows: list[dict[str, str]]) -> None:
    with csv_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        for row in rows:
            writer.writerow(row)


def run_add(args: argparse.Namespace, repo_root: Path) -> None:
    fallback_date = parse_iso_date(args.date) if args.date else None
    csv_path = (repo_root / args.csv).resolve()
    ensure_csv(csv_path)
    existing_ids = load_existing_ids(csv_path)
    project_catalog = load_project_catalog(repo_root)
    lines = load_entry_lines(args)

    created_rows: list[dict[str, str]] = []
    skipped = 0
    now_iso = datetime.now().isoformat(timespec="seconds")

    for line in lines:
        parsed = parse_entry_line(line, fallback_date)
        entry_id = build_entry_id(parsed)
        if entry_id in existing_ids:
            skipped += 1
            print(
                f"[SKIP] duplicate: "
                f"{parsed.date.isoformat()} {parsed.start}-{parsed.end} {parsed.task}"
            )
            continue

        match = detect_project(
            task_text=parsed.task,
            projects=project_catalog,
            default_project=args.default_project,
        )
        row = {
            "entry_id": entry_id,
            "date": parsed.date.isoformat(),
            "start": parsed.start,
            "end": parsed.end,
            "duration_min": str(parsed.duration_min),
            "task": parsed.task,
            "project": match.project,
            "project_path": match.project_path,
            "match_type": match.match_type,
            "confidence": f"{match.confidence:.2f}",
            "raw_input": line,
            "created_at": now_iso,
        }
        created_rows.append(row)
        existing_ids.add(entry_id)

        msg = (
            f"[ADD] {row['date']} {row['start']}-{row['end']} "
            f"{format_hours(parsed.duration_min)}h -> {match.project} "
            f"({match.match_type}, conf={row['confidence']}) | {parsed.task}"
        )
        print(msg)
        if match.match_type == "unlinked" and match.candidate_hints:
            hints = ", ".join(f"{name}:{score}" for name, score in match.candidate_hints)
            print(f"       hints: {hints}")

    if created_rows:
        append_rows(csv_path, created_rows)

    total_min = sum(int(row["duration_min"]) for row in created_rows)
    print(
        f"[DONE] added={len(created_rows)}, skipped={skipped}, "
        f"duration={format_hours(total_min)}h, csv={csv_path}"
    )


def parse_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        return []
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def resolve_report_window(args: argparse.Namespace, today: date) -> tuple[date | None, date | None]:
    if args.from_date or args.to_date:
        from_date = parse_iso_date(args.from_date) if args.from_date else None
        to_date = parse_iso_date(args.to_date) if args.to_date else None
        return from_date, to_date

    if args.range == "today":
        return today, today
    if args.range == "week":
        monday = today - timedelta(days=today.weekday())
        return monday, today
    if args.range == "month":
        month_start = today.replace(day=1)
        return month_start, today
    return None, None


def in_window(day: date, from_date: date | None, to_date: date | None) -> bool:
    if from_date is not None and day < from_date:
        return False
    if to_date is not None and day > to_date:
        return False
    return True


def build_report_markdown(
    rows: list[dict[str, str]],
    from_date: date | None,
    to_date: date | None,
    top_n: int,
    default_project: str,
) -> str:
    project_minutes: Counter[str] = Counter()
    project_entries: Counter[str] = Counter()
    daily_minutes: Counter[str] = Counter()
    daily_entries: Counter[str] = Counter()
    unlinked_rows: list[dict[str, str]] = []

    total_minutes = 0
    for row in rows:
        minutes = int(row.get("duration_min", "0") or "0")
        project = row.get("project", "").strip() or default_project
        day = row.get("date", "")
        total_minutes += minutes
        project_minutes[project] += minutes
        project_entries[project] += 1
        daily_minutes[day] += minutes
        daily_entries[day] += 1
        if project == default_project:
            unlinked_rows.append(row)

    if from_date is None and to_date is None:
        window_text = "all"
    else:
        left = from_date.isoformat() if from_date else "start"
        right = to_date.isoformat() if to_date else "end"
        window_text = f"{left} ~ {right}"

    lines: list[str] = []
    lines.append("# Time Tracking Report")
    lines.append("")
    lines.append(f"- Generated at: `{datetime.now().isoformat(timespec='seconds')}`")
    lines.append(f"- Window: `{window_text}`")
    lines.append(f"- Entries: `{len(rows)}`")
    lines.append(f"- Total: `{format_hours(total_minutes)} h`")
    lines.append("")
    lines.append("## By Project")
    lines.append("")
    lines.append("| Project | Hours | Share | Entries |")
    lines.append("| --- | ---: | ---: | ---: |")
    for project, minutes in project_minutes.most_common(top_n):
        share = (minutes / total_minutes * 100.0) if total_minutes else 0.0
        lines.append(
            f"| {project} | {format_hours(minutes)} | {share:.1f}% | {project_entries[project]} |"
        )
    if not project_minutes:
        lines.append("| (no data) | 0.00 | 0.0% | 0 |")

    lines.append("")
    lines.append("## By Day")
    lines.append("")
    lines.append("| Date | Hours | Entries |")
    lines.append("| --- | ---: | ---: |")
    for day in sorted(daily_minutes.keys()):
        lines.append(f"| {day} | {format_hours(daily_minutes[day])} | {daily_entries[day]} |")
    if not daily_minutes:
        lines.append("| (no data) | 0.00 | 0 |")

    lines.append("")
    lines.append(f"## {default_project} Details")
    lines.append("")
    if unlinked_rows:
        lines.append("| Date | Slot | Hours | Task |")
        lines.append("| --- | --- | ---: | --- |")
        for row in sorted(unlinked_rows, key=lambda x: (x.get("date", ""), x.get("start", ""))):
            slot = f"{row.get('start', '')}-{row.get('end', '')}"
            lines.append(
                f"| {row.get('date', '')} | {slot} | "
                f"{format_hours(int(row.get('duration_min', '0') or '0'))} | {row.get('task', '').strip()} |"
            )
    else:
        lines.append("- none")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- `explicit-tag` means task text contains `#proj/<name>` or `#project/<name>`.")
    lines.append("- `auto-match` means project was inferred from existing repo project names.")
    lines.append(f"- `unlinked` means no confident match; keep as `{default_project}` or add explicit tag.")
    lines.append("")
    return "\n".join(lines)


def run_report(args: argparse.Namespace, repo_root: Path) -> None:
    csv_path = (repo_root / args.csv).resolve()
    rows = parse_csv_rows(csv_path)
    if not rows:
        raise SystemExit(f"No rows found in {csv_path}")

    today = date.today()
    from_date, to_date = resolve_report_window(args, today)

    filtered: list[dict[str, str]] = []
    for row in rows:
        try:
            day = parse_iso_date(row.get("date", ""))
        except ValueError:
            continue
        if in_window(day, from_date, to_date):
            filtered.append(row)

    report_md = build_report_markdown(
        rows=filtered,
        from_date=from_date,
        to_date=to_date,
        top_n=args.top,
        default_project=args.default_project,
    )

    output_path = (repo_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_md, encoding="utf-8")

    total_minutes = sum(int(row.get("duration_min", "0") or "0") for row in filtered)
    project_counter = Counter((row.get("project", "") or args.default_project) for row in filtered)
    print(
        f"[DONE] rows={len(filtered)}, total={format_hours(total_minutes)}h, "
        f"projects={len(project_counter)}, report={output_path}"
    )
    for project, count in project_counter.most_common(8):
        minutes = sum(
            int(row.get("duration_min", "0") or "0")
            for row in filtered
            if (row.get("project", "") or args.default_project) == project
        )
        print(f"  - {project}: {format_hours(minutes)}h ({count} entries)")


def run_projects(args: argparse.Namespace, repo_root: Path) -> None:
    catalog = load_project_catalog(repo_root)
    if not catalog:
        raise SystemExit("No project catalog found under 03_Goal-Projects")

    print(f"[OK] projects={len(catalog)}")
    for item in catalog[: args.limit]:
        alias_preview = ", ".join(item.aliases[:6])
        print(f"- {item.name} | {item.rel_path} | aliases: {alias_preview}")
    if len(catalog) > args.limit:
        print(f"... ({len(catalog) - args.limit} more)")


def main() -> None:
    args = parse_args()
    repo_root = Path(".").resolve()

    if args.command == "add":
        run_add(args, repo_root)
        return
    if args.command == "report":
        run_report(args, repo_root)
        return
    if args.command == "projects":
        run_projects(args, repo_root)
        return
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
