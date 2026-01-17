#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


RE_TITLE = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)
RE_BULLET_KV = re.compile(r"^\s*-\s*(?P<key>[^:：]+?)\s*[:：]\s*(?P<value>.*?)\s*$")
RE_KV_ANY = re.compile(r"^\s*(?:-\s*)?(?P<key>[^:：]+?)\s*[:：]\s*(?P<value>.*?)\s*$")


def _parse_yyyy_mm_dd(s: str) -> dt.date | None:
    s = s.strip()
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        return None


def _extract_first_date(text: str) -> dt.date | None:
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
    if not m:
        return None
    return _parse_yyyy_mm_dd(m.group(1))


def _extract_birth_date(text: str) -> dt.date | None:
    d = _extract_first_date(text)
    if d:
        return d
    m = re.search(r"\b(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\b", text)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


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
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        if t in seen:
            continue
        seen.add(t)
        out.append(t)
    return out


@dataclass(frozen=True)
class PersonCard:
    path: str
    name: str
    handle: str | None
    aliases: str | None
    keywords: str | None
    tags: tuple[str, ...]
    status: str | None
    last_contact: str | None
    next_follow_up: str | None
    reviewed_at: str | None
    stage_anchor: str | None
    birth_date: str | None
    expected_graduation: str | None
    mtime: int

    def to_json(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "name": self.name,
            "handle": self.handle,
            "aliases": self.aliases,
            "keywords": self.keywords,
            "tags": list(self.tags),
            "status": self.status,
            "last_contact": self.last_contact,
            "next_follow_up": self.next_follow_up,
            "reviewed_at": self.reviewed_at,
            "stage_anchor": self.stage_anchor,
            "birth_date": self.birth_date,
            "expected_graduation": self.expected_graduation,
            "mtime": self.mtime,
        }


def _parse_card(path: Path) -> PersonCard:
    text = path.read_text(encoding="utf-8")

    title = path.stem
    m = RE_TITLE.search(text)
    if m:
        title = _norm_space(m.group("title"))

    handle: str | None = None
    aliases: str | None = None
    keywords: str | None = None
    status: str | None = None
    last_contact: str | None = None
    next_follow_up: str | None = None
    reviewed_at: str | None = None
    stage_anchor: str | None = None
    birth_date: str | None = None
    expected_graduation: str | None = None
    tags: list[str] = []

    for line in text.splitlines():
        m = RE_BULLET_KV.match(line)
        if not m:
            continue
        key = _norm_space(m.group("key")).lower()
        value = _norm_space(m.group("value"))

        if key in {"handle", "id", "handle/id", "handle/id（建议）"}:
            handle = value or handle
        elif key in {"别名/昵称/搜索词", "aliases", "alias"}:
            aliases = value or aliases
        elif key in {"关键词", "keywords"}:
            keywords = value or keywords
        elif key in {"tags", "tag"}:
            tags.extend(_split_tags(value))
        elif key in {"状态", "status"}:
            status = value or status
        elif key in {"最后联系", "last_contact"}:
            last_contact = value or last_contact
        elif key in {"下次跟进", "next_follow_up", "next"}:
            next_follow_up = value or next_follow_up
        elif key in {"最近复查（可选）", "最近复查", "reviewed_at"}:
            reviewed_at = value or reviewed_at
        elif key in {"阶段锚点（可选）", "阶段锚点", "stage_anchor"}:
            stage_anchor = value or stage_anchor
        elif key in {"出生日期（可选）", "出生日期", "birthday", "birth_date"}:
            birth_date = value or birth_date
        elif key in {
            "预计毕业（可选）",
            "预计毕业",
            "毕业时间",
            "毕业日期",
            "graduation",
            "graduation_date",
            "expected_graduation",
        }:
            expected_graduation = value or expected_graduation

    try:
        st = path.stat()
        mtime = int(st.st_mtime)
    except OSError:
        mtime = 0

    return PersonCard(
        path=str(path.as_posix()),
        name=title,
        handle=handle,
        aliases=aliases,
        keywords=keywords,
        tags=tuple(dict.fromkeys(tags)),
        status=status,
        last_contact=last_contact,
        next_follow_up=next_follow_up,
        reviewed_at=reviewed_at,
        stage_anchor=stage_anchor,
        birth_date=birth_date,
        expected_graduation=expected_graduation,
        mtime=mtime,
    )


def _iter_cards(people_dir: Path) -> Iterable[PersonCard]:
    if not people_dir.exists():
        return []
    for p in sorted(people_dir.glob("*.md")):
        if p.name.startswith("_"):
            continue
        yield _parse_card(p)


def _haystack(card: PersonCard) -> str:
    parts = [
        card.name,
        card.handle or "",
        card.aliases or "",
        card.keywords or "",
        card.status or "",
        card.last_contact or "",
        card.next_follow_up or "",
        " ".join(card.tags),
    ]
    return "\n".join(parts).lower()


def _match_all_substrings(haystack: str, needles: list[str]) -> bool:
    for needle in needles:
        if needle.lower() not in haystack:
            return False
    return True


def _match_tags(card: PersonCard, required_tags: list[str]) -> bool:
    if not required_tags:
        return True
    have = set(card.tags)
    for t in required_tags:
        if t not in have:
            return False
    return True


def _match_status(card: PersonCard, statuses: list[str]) -> bool:
    if not statuses:
        return True
    s = (card.status or "").strip()
    if not s:
        return False
    return any(st in s for st in statuses)


def _follow_up_due(card: PersonCard) -> dt.date | None:
    if not card.next_follow_up:
        return None
    if "暂无" in card.next_follow_up:
        return None
    return _extract_first_date(card.next_follow_up)


def _sort_key(card: PersonCard) -> tuple[int, int]:
    due = _follow_up_due(card)
    if due:
        return (0, due.toordinal())
    return (1, -card.mtime)


def _cn_numeral_to_int(s: str) -> int | None:
    s = s.strip()
    table = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6}
    if s in table:
        return table[s]
    if s.isdigit():
        try:
            return int(s)
        except ValueError:
            return None
    return None


def _int_to_cn_numeral(n: int) -> str:
    table = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六"}
    return table.get(n, str(n))


def _academic_year_start_year(d: dt.date) -> int:
    return d.year if d.month >= 9 else (d.year - 1)


def _parse_stage_anchor(text: str) -> tuple[dt.date, str | None] | None:
    anchor_date = _extract_first_date(text)
    if not anchor_date:
        return None
    label = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", "", text).strip()
    label = label.strip(" -–—()（）")
    if not label:
        return (anchor_date, None)
    return (anchor_date, label)


def _infer_stage_from_anchor(stage_anchor: str, as_of: dt.date) -> dict[str, Any] | None:
    parsed = _parse_stage_anchor(stage_anchor)
    if not parsed:
        return None
    anchor_date, anchor_label = parsed
    anchor_ay = _academic_year_start_year(anchor_date)
    as_of_ay = _academic_year_start_year(as_of)
    delta_ay = as_of_ay - anchor_ay

    label = anchor_label or ""
    m_undergrad = re.search(r"(本科)?\s*大\s*([一二三四1-4])", label)
    if m_undergrad:
        n0 = _cn_numeral_to_int(m_undergrad.group(2))
        if n0:
            entry_ay = anchor_ay - (n0 - 1)
            n = as_of_ay - entry_ay + 1
            if n <= 0:
                inferred = "本科未入学（推算）"
            elif 1 <= n <= 4:
                inferred = f"本科大{_int_to_cn_numeral(n)}（推算）"
            else:
                inferred = "本科已毕业（推算）"
            return {
                "anchor_date": anchor_date.isoformat(),
                "anchor_label": anchor_label,
                "as_of": as_of.isoformat(),
                "delta_academic_years": delta_ay,
                "track": "undergrad",
                "entry_academic_year": entry_ay,
                "year_number": n,
                "inferred": inferred,
            }

    m_master = re.search(r"(硕士)?\s*研\s*([一二三1-3])", label)
    if m_master:
        n0 = _cn_numeral_to_int(m_master.group(2))
        if n0:
            entry_ay = anchor_ay - (n0 - 1)
            n = as_of_ay - entry_ay + 1
            inferred = f"研{_int_to_cn_numeral(max(1, n))}（推算）"
            return {
                "anchor_date": anchor_date.isoformat(),
                "anchor_label": anchor_label,
                "as_of": as_of.isoformat(),
                "delta_academic_years": delta_ay,
                "track": "master",
                "entry_academic_year": entry_ay,
                "year_number": n,
                "inferred": inferred,
            }

    m_phd = re.search(r"(博士)?\s*博\s*([一二三四五六1-6])", label)
    if m_phd:
        n0 = _cn_numeral_to_int(m_phd.group(2))
        if n0:
            entry_ay = anchor_ay - (n0 - 1)
            n = as_of_ay - entry_ay + 1
            inferred = f"博{_int_to_cn_numeral(max(1, n))}（推算）"
            return {
                "anchor_date": anchor_date.isoformat(),
                "anchor_label": anchor_label,
                "as_of": as_of.isoformat(),
                "delta_academic_years": delta_ay,
                "track": "phd",
                "entry_academic_year": entry_ay,
                "year_number": n,
                "inferred": inferred,
            }

    return {
        "anchor_date": anchor_date.isoformat(),
        "anchor_label": anchor_label,
        "as_of": as_of.isoformat(),
        "delta_academic_years": delta_ay,
        "track": None,
        "entry_academic_year": None,
        "year_number": None,
        "inferred": None,
    }


def _expected_graduation(card: PersonCard, stage: dict[str, Any] | None) -> dt.date | None:
    if card.expected_graduation:
        d = _extract_first_date(card.expected_graduation)
        if d:
            return d
    if not stage:
        return None
    track = stage.get("track")
    entry_ay = stage.get("entry_academic_year")
    if not isinstance(entry_ay, int):
        return None
    if track == "undergrad":
        return dt.date(entry_ay + 4, 6, 30)
    if track == "master":
        return dt.date(entry_ay + 3, 6, 30)
    return None


def _load_me_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    out: dict[str, Any] = {}
    for line in text.splitlines():
        m = RE_KV_ANY.match(line)
        if not m:
            continue
        key = _norm_space(m.group("key"))
        value = _norm_space(m.group("value"))
        if not key or not value:
            continue
        if key in {"出生日期", "出生日期（可选）", "birth_date", "birthday"}:
            out["birth_date_raw"] = value
        elif key in {"阶段锚点", "阶段锚点（可选）", "stage_anchor"}:
            out["stage_anchor"] = value
        elif key in {"预计毕业", "预计毕业（可选）", "毕业时间", "毕业日期", "expected_graduation"}:
            out["expected_graduation_raw"] = value

    birth_date = _extract_birth_date(out.get("birth_date_raw", "")) if out.get("birth_date_raw") else None
    if birth_date:
        out["birth_date"] = birth_date
    grad = _extract_first_date(out.get("expected_graduation_raw", "")) if out.get("expected_graduation_raw") else None
    if grad:
        out["expected_graduation"] = grad
    return out


def _age_years(birth_date: dt.date, as_of: dt.date) -> float:
    return (as_of - birth_date).days / 365.2425


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Query people cards in 05_Resources/network/people (agent-friendly, no deps)."
    )
    parser.add_argument(
        "--people-dir",
        default=str(Path("05_Resources/network/people")),
        help="People cards directory (default: 05_Resources/network/people).",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Require tag (repeatable), e.g. --tag '#resource/intro'.",
    )
    parser.add_argument(
        "--status",
        action="append",
        default=[],
        help="Substring match against 状态/status, repeatable (e.g. --status '#status/active').",
    )
    parser.add_argument(
        "--needs-followup",
        action="store_true",
        help="Only show cards that have a next follow-up date (and not marked '暂无').",
    )
    parser.add_argument(
        "--due-before",
        default=None,
        help="Only show cards whose follow-up due date <= YYYY-MM-DD.",
    )
    parser.add_argument(
        "--as-of",
        default=None,
        help="Compute time-based fields as of YYYY-MM-DD (default: today).",
    )
    parser.add_argument(
        "--relative-to-me",
        action="store_true",
        help="Attach relative fields vs your Me profile (birth/stage/graduation if present).",
    )
    parser.add_argument(
        "--me-path",
        default=str(Path("04_Assets/profile/Me.md")),
        help="Path to Me profile (default: 04_Assets/profile/Me.md).",
    )
    parser.add_argument("--me-birth-date", default=None, help="Override Me birth date (YYYY-MM-DD).")
    parser.add_argument("--me-stage-anchor", default=None, help="Override Me stage anchor text.")
    parser.add_argument("--me-expected-graduation", default=None, help="Override Me expected graduation (YYYY-MM-DD).")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON array for agents.",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Free-text substrings to match (AND).",
    )
    args = parser.parse_args(argv)

    due_before: dt.date | None = None
    if args.due_before:
        due_before = _parse_yyyy_mm_dd(args.due_before)
        if not due_before:
            print(f"Invalid --due-before date: {args.due_before}", file=sys.stderr)
            return 2

    as_of = dt.date.today()
    if args.as_of:
        parsed_as_of = _parse_yyyy_mm_dd(args.as_of)
        if not parsed_as_of:
            print(f"Invalid --as-of date: {args.as_of}", file=sys.stderr)
            return 2
        as_of = parsed_as_of

    people_dir = Path(args.people_dir)
    cards = list(_iter_cards(people_dir))

    required_tags = [t.strip() for t in args.tag if t and t.strip()]
    statuses = [s.strip() for s in args.status if s and s.strip()]
    needles = [_norm_space(t) for t in args.text if _norm_space(t)]

    out: list[PersonCard] = []
    for card in cards:
        haystack = _haystack(card)
        if not _match_all_substrings(haystack, needles):
            continue
        if not _match_tags(card, required_tags):
            continue
        if not _match_status(card, statuses):
            continue
        if args.needs_followup and not _follow_up_due(card):
            continue
        if due_before:
            due = _follow_up_due(card)
            if not due:
                continue
            if due > due_before:
                continue
        out.append(card)

    out.sort(key=_sort_key)

    me: dict[str, Any] | None = None
    me_stage: dict[str, Any] | None = None
    if args.relative_to_me:
        me = _load_me_profile(Path(args.me_path))
        if args.me_birth_date:
            me_birth = _parse_yyyy_mm_dd(args.me_birth_date)
            if not me_birth:
                print(f"Invalid --me-birth-date: {args.me_birth_date}", file=sys.stderr)
                return 2
            me["birth_date"] = me_birth
        if args.me_stage_anchor:
            me["stage_anchor"] = args.me_stage_anchor
        if args.me_expected_graduation:
            me_grad = _parse_yyyy_mm_dd(args.me_expected_graduation)
            if not me_grad:
                print(f"Invalid --me-expected-graduation: {args.me_expected_graduation}", file=sys.stderr)
                return 2
            me["expected_graduation"] = me_grad
        if me.get("stage_anchor"):
            me_stage = _infer_stage_from_anchor(str(me["stage_anchor"]), as_of)

    if args.json:
        payload: list[dict[str, Any]] = []
        for c in out:
            item = c.to_json()
            stage = _infer_stage_from_anchor(c.stage_anchor, as_of) if c.stage_anchor else None
            if stage:
                item["stage"] = stage
                grad = _expected_graduation(c, stage)
                if grad:
                    item["graduation"] = {"date": grad.isoformat(), "source": "expected_graduation|inferred"}
                    item["time_to_graduation_days"] = (grad - as_of).days
            if c.birth_date:
                bd = _extract_birth_date(c.birth_date)
                if bd:
                    item["age_years"] = _age_years(bd, as_of)

            if args.relative_to_me and me is not None:
                rel: dict[str, Any] = {}
                me_birth = me.get("birth_date")
                if isinstance(me_birth, dt.date) and c.birth_date:
                    bd = _extract_birth_date(c.birth_date)
                    if bd:
                        rel["age_delta_days"] = (bd - me_birth).days
                        rel["age_delta_years"] = _age_years(bd, as_of) - _age_years(me_birth, as_of)

                me_grad = me.get("expected_graduation")
                their_grad = _expected_graduation(c, stage) if stage else None
                if isinstance(me_grad, dt.date) and isinstance(their_grad, dt.date):
                    rel["graduation_delta_days"] = (their_grad - me_grad).days
                    rel["graduation_delta_years"] = (their_grad - me_grad).days / 365.2425
                    rel["me_time_to_graduation_days"] = (me_grad - as_of).days
                    rel["their_time_to_graduation_days"] = (their_grad - as_of).days

                if me_stage and stage:
                    if (
                        me_stage.get("track") == stage.get("track")
                        and isinstance(me_stage.get("year_number"), int)
                        and isinstance(stage.get("year_number"), int)
                    ):
                        rel["stage_year_delta"] = int(stage["year_number"]) - int(me_stage["year_number"])

                if rel:
                    item["relative_to_me"] = rel
            payload.append(item)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    for c in out:
        tag_str = " ".join(c.tags)
        kw = c.keywords or ""
        nxt = c.next_follow_up or ""
        stat = c.status or ""
        stage = _infer_stage_from_anchor(c.stage_anchor, as_of) if c.stage_anchor else None
        print(f"- {c.name} ({c.path})")
        if kw:
            print(f"  关键词: {kw}")
        if tag_str:
            print(f"  Tags: {tag_str}")
        if stat:
            print(f"  状态: {stat}")
        if stage and stage.get("inferred"):
            print(f"  阶段(推算 @ {as_of.isoformat()}): {stage['inferred']}")
        if c.birth_date:
            bd = _extract_birth_date(c.birth_date)
            if bd:
                print(f"  年龄(推算 @ {as_of.isoformat()}): {int(_age_years(bd, as_of))} 岁左右")
        grad = _expected_graduation(c, stage) if stage else None
        if grad:
            print(f"  预计毕业: {grad.isoformat()}（距离 {as_of.isoformat()}：{(grad - as_of).days} 天）")
        if nxt:
            print(f"  下次跟进: {nxt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
