#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RE_BULLET_KV = re.compile(r"^\s*-\s*(?P<key>[^:：]+?)\s*[:：]\s*(?P<value>.*?)\s*$")


def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _extract_first_date(text: str) -> dt.date | None:
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def _split_tags(value: str) -> list[str]:
    raw = re.split(r"[,\s]+", value.strip())
    tags: list[str] = []
    for token in raw:
        token = token.strip()
        if not token:
            continue
        if not token.startswith("#"):
            continue
        tags.append(token)
    return tags


ALLOWED_PREFIXES = (
    "#domain/",
    "#resource/",
    "#role/",
    "#city/",
    "#rel/",
    "#status/",
)


@dataclass(frozen=True)
class Issue:
    path: str
    level: str  # "error" | "warn"
    message: str

    def to_json(self) -> dict[str, Any]:
        return {"path": self.path, "level": self.level, "message": self.message}


def _parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = RE_BULLET_KV.match(line)
        if not m:
            continue
        key = _norm_space(m.group("key"))
        value = _norm_space(m.group("value"))
        if key and value:
            fields[key] = value
    return fields


def _get(fields: dict[str, str], *keys: str) -> str | None:
    for k in keys:
        if k in fields:
            return fields[k]
    return None


def validate_card(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    fields = _parse_fields(text)

    handle = _get(fields, "Handle/ID", "handle", "id")
    keywords = _get(fields, "关键词", "keywords")
    tags_value = _get(fields, "Tags", "tags")
    status = _get(fields, "状态", "status")
    last_contact = _get(fields, "最后联系", "last_contact")
    next_follow_up = _get(fields, "下次跟进", "next_follow_up", "next")
    reviewed_at = _get(fields, "最近复查（可选）", "最近复查", "reviewed_at")
    stage_anchor = _get(fields, "阶段锚点（可选）", "阶段锚点", "stage_anchor")
    birth_date = _get(fields, "出生日期（可选）", "出生日期", "birth_date", "birthday")
    expected_graduation = _get(fields, "预计毕业（可选）", "预计毕业", "毕业时间", "毕业日期", "expected_graduation")

    if not handle:
        issues.append(Issue(str(path), "error", "Missing required field: Handle/ID"))
    if not keywords:
        issues.append(Issue(str(path), "error", "Missing required field: 关键词"))
    if not tags_value:
        issues.append(Issue(str(path), "error", "Missing required field: Tags"))
    if not status:
        issues.append(Issue(str(path), "warn", "Missing field: 状态 (recommended)"))
    if not last_contact:
        issues.append(Issue(str(path), "warn", "Missing field: 最后联系 (recommended)"))

    tags = _split_tags(tags_value or "")
    if tags_value and not tags:
        issues.append(Issue(str(path), "warn", "Tags field present but no #tags parsed"))

    for t in tags:
        if not t.startswith(ALLOWED_PREFIXES):
            issues.append(
                Issue(
                    str(path),
                    "warn",
                    f"Tag prefix not in allowed set {ALLOWED_PREFIXES}: {t}",
                )
            )
        if any(ch.isupper() for ch in t):
            issues.append(Issue(str(path), "warn", f"Tag contains uppercase (drift risk): {t}"))

    if last_contact and not _extract_first_date(last_contact):
        issues.append(Issue(str(path), "warn", "最后联系 has no valid YYYY-MM-DD date"))

    if next_follow_up:
        if "暂无" not in next_follow_up and not _extract_first_date(next_follow_up):
            issues.append(Issue(str(path), "warn", "下次跟进 has no valid YYYY-MM-DD date (or mark 暂无)"))

    if reviewed_at and not _extract_first_date(reviewed_at):
        issues.append(Issue(str(path), "warn", "最近复查 has no valid YYYY-MM-DD date"))
    if stage_anchor and not _extract_first_date(stage_anchor):
        issues.append(Issue(str(path), "warn", "阶段锚点 has no valid YYYY-MM-DD date"))
    if birth_date:
        if not _extract_first_date(birth_date) and not re.search(r"\b\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日\b", birth_date):
            issues.append(Issue(str(path), "warn", "出生日期 has no valid YYYY-MM-DD (or YYYY年MM月DD日)"))
    if expected_graduation and not _extract_first_date(expected_graduation):
        issues.append(Issue(str(path), "warn", "预计毕业 has no valid YYYY-MM-DD date"))

    return issues


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate Me network people cards for agent-friendly querying.")
    ap.add_argument(
        "--people-dir",
        default="05_Resources/network/people",
        help="Directory containing people cards (default: 05_Resources/network/people).",
    )
    ap.add_argument("--json", action="store_true", help="Output JSON array of issues.")
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well.")
    args = ap.parse_args(argv)

    people_dir = Path(args.people_dir)
    if not people_dir.exists():
        print(f"People dir not found: {people_dir}", file=sys.stderr)
        return 2

    issues: list[Issue] = []
    for p in sorted(people_dir.glob("*.md")):
        if p.name.startswith("_"):
            continue
        issues.extend(validate_card(p))

    if args.json:
        print(json.dumps([i.to_json() for i in issues], ensure_ascii=False, indent=2))
    else:
        for i in issues:
            print(f"[{i.level}] {i.path}: {i.message}")

    if not issues:
        return 0

    has_error = any(i.level == "error" for i in issues)
    if has_error:
        return 1
    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
