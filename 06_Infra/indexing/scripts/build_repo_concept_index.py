#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
CODE_RE = re.compile(r"`([^`\n]+)`")

DEFAULT_V1_1_KIND_QUOTA = {
    "review": 4,
    "decision": 4,
    "cognition": 3,
    "index": 1,
}
DEFAULT_PLACEHOLDER_PATTERNS = [
    r"<[^>]+>",
    r"\bxxx\b",
    r"\btbd\b",
    r"\btodo\b",
    r"^private/?$",
    r"^private/README\.md$",
    r"^YYYY/MM/?$",
    r"^active/?$",
    r"^/?\.agents/?$",
    r"^/?cognition/?$",
    r"^/?decisions/?$",
    r"^/?04-review/?$",
    r"^/?timeline/?$",
    r"^/?plans/?$",
    r"^/?notes/?$",
]


@dataclass
class Concept:
    concept_id: str
    concept: str
    aliases: list[str]
    scope: list[str]


@dataclass
class MdDoc:
    path: Path
    title: str
    headings: list[str]
    haystack: str
    content: str


def parse_seed_list(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        body = value[1:-1].strip()
        if not body:
            return []
        return [x.strip().strip('"').strip("'") for x in body.split(",") if x.strip()]
    return [value.strip().strip('"').strip("'")] if value else []


def parse_kind_quota(value: str | None) -> dict[str, int]:
    if not value:
        return {}
    out: dict[str, int] = {}
    for part in value.split(","):
        chunk = part.strip()
        if not chunk:
            continue
        if ":" not in chunk:
            raise ValueError(f"Invalid kind quota item: {chunk!r}. Expected kind:n")
        kind, raw_n = chunk.split(":", 1)
        kind = kind.strip().lower()
        try:
            n = int(raw_n.strip())
        except ValueError as exc:
            raise ValueError(f"Invalid quota number in item: {chunk!r}") from exc
        if n < 0:
            raise ValueError(f"Quota must be >= 0: {chunk!r}")
        out[kind] = n
    return out


def quota_to_arg(quota: dict[str, int]) -> str:
    if not quota:
        return ""
    return ",".join(f"{k}:{v}" for k, v in quota.items())


def load_concepts(seed_path: Path) -> list[Concept]:
    concepts: list[Concept] = []
    current: dict[str, str] = {}

    for raw in seed_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#") or line.strip() == "concepts:":
            continue

        if line.strip().startswith("- id:"):
            if current:
                concepts.append(
                    Concept(
                        concept_id=current.get("id", ""),
                        concept=current.get("concept", ""),
                        aliases=parse_seed_list(current.get("aliases", "")),
                        scope=parse_seed_list(current.get("scope", "")),
                    )
                )
                current = {}
            current["id"] = line.split(":", 1)[1].strip()
            continue

        if ":" in line:
            k, v = line.split(":", 1)
            current[k.strip()] = v.strip()

    if current:
        concepts.append(
            Concept(
                concept_id=current.get("id", ""),
                concept=current.get("concept", ""),
                aliases=parse_seed_list(current.get("aliases", "")),
                scope=parse_seed_list(current.get("scope", "")),
            )
        )

    return [c for c in concepts if c.concept_id and c.concept]


def iter_docs(scope_dirs: list[Path]) -> Iterable[MdDoc]:
    for scope in scope_dirs:
        for p in sorted(scope.rglob("*.md")):
            s = p.as_posix()
            if "/.agents/" in s or p.name.startswith("_"):
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            title_m = TITLE_RE.search(text)
            title = title_m.group(1).strip() if title_m else p.stem
            headings = [h.strip() for h in HEADING_RE.findall(text)]
            hay = "\n".join([str(p.as_posix()), title] + headings).lower()
            content = text.lower()
            yield MdDoc(path=p, title=title, headings=headings, haystack=hay, content=content)


def classify_kind(path: Path) -> str:
    s = path.as_posix().lower()
    if "/cognition/" in s:
        return "cognition"
    if "/decisions/" in s:
        return "decision"
    if "/04-review/" in s:
        return "review"
    if "/timeline/" in s:
        return "timeline"
    if "/plans/" in s:
        return "plan"
    if path.name.lower() in {"readme.md", "index.md"}:
        return "index"
    if "/notes/" in s:
        return "note"
    return "other"


def score_hit(term: str, doc: MdDoc) -> tuple[int, list[str]]:
    term_l = term.lower()
    basis: list[str] = []
    score = 0

    if term_l in doc.path.name.lower():
        score += 3
        basis.append("filename")
    if term_l in doc.title.lower():
        score += 3
        basis.append("title")
    if any(term_l in h.lower() for h in doc.headings):
        score += 2
        basis.append("heading")
    if term_l in doc.path.as_posix().lower():
        score += 1
        basis.append("path")
    if term_l in doc.content:
        score += 1
        basis.append("content")

    return score, basis


def apply_evidence_policy(
    evidences: list[dict],
    max_evidence_per_concept: int,
    kind_quota: dict[str, int],
) -> tuple[list[dict], dict]:
    before = len(evidences)
    if max_evidence_per_concept <= 0:
        return evidences, {"before": before, "after": before, "dropped": 0}

    if not kind_quota:
        selected = evidences[:max_evidence_per_concept]
        return selected, {
            "before": before,
            "after": len(selected),
            "dropped": before - len(selected),
        }

    selected: list[dict] = []
    selected_paths: set[str] = set()
    per_kind_counts = {k: 0 for k in kind_quota}

    # Pass 1: satisfy kind quotas using ranked evidence order.
    for e in evidences:
        k = str(e.get("kind", "")).lower()
        if k not in kind_quota:
            continue
        if per_kind_counts[k] >= kind_quota[k]:
            continue
        p = str(e.get("path", ""))
        if p in selected_paths:
            continue
        selected.append(e)
        selected_paths.add(p)
        per_kind_counts[k] += 1
        if len(selected) >= max_evidence_per_concept:
            break

    # Pass 2: fill remaining slots with best ranked leftovers.
    if len(selected) < max_evidence_per_concept:
        for e in evidences:
            p = str(e.get("path", ""))
            if p in selected_paths:
                continue
            selected.append(e)
            selected_paths.add(p)
            if len(selected) >= max_evidence_per_concept:
                break

    return selected, {
        "before": before,
        "after": len(selected),
        "dropped": before - len(selected),
    }


def build_index(
    concepts: list[Concept],
    docs: list[MdDoc],
    scope_names: list[str],
    *,
    profile: str,
    version_tag: str,
    max_evidence_per_concept: int,
    kind_quota: dict[str, int],
) -> dict:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    out = {
        "version": version_tag,
        "profile": profile,
        "built_at": now,
        "scope": scope_names,
        "files_scanned": len(docs),
        "policy": {
            "max_evidence_per_concept": max_evidence_per_concept,
            "kind_quota": kind_quota,
        },
        "concepts": [],
    }

    for c in concepts:
        search_terms = [c.concept] + c.aliases
        evidences = []

        for d in docs:
            best_score = 0
            best_basis: list[str] = []
            for term in search_terms:
                if not term:
                    continue
                score, basis = score_hit(term, d)
                if score > best_score:
                    best_score = score
                    best_basis = basis
            if best_score > 0:
                evidences.append(
                    {
                        "path": d.path.as_posix(),
                        "title": d.title,
                        "kind": classify_kind(d.path),
                        "match_basis": best_basis,
                        "score": best_score,
                        "last_verified_at": now,
                    }
                )

        evidences.sort(key=lambda x: (-x["score"], x["path"]))
        if profile == "v1_1":
            selected, policy_stats = apply_evidence_policy(
                evidences,
                max_evidence_per_concept=max_evidence_per_concept,
                kind_quota=kind_quota,
            )
        else:
            selected = evidences
            policy_stats = {
                "before": len(evidences),
                "after": len(evidences),
                "dropped": 0,
            }

        out["concepts"].append(
            {
                "concept_id": c.concept_id,
                "concept": c.concept,
                "aliases": c.aliases,
                "scope": c.scope or scope_names,
                "last_built_at": now,
                "evidence_total_before_policy": policy_stats["before"],
                "evidence": selected,
            }
        )

    return out


def write_md(index_obj: dict, out_md: Path, *, top_evidence_md: int) -> None:
    version = index_obj.get("version", "v1")
    lines = []
    lines.append(f"# Repo Concept Index ({version})")
    lines.append("")
    lines.append(f"- Profile: `{index_obj.get('profile', 'v1')}`")
    lines.append(f"- Built at: `{index_obj['built_at']}`")
    lines.append(f"- Scope: `{', '.join(index_obj['scope'])}`")
    lines.append(f"- Files scanned: `{index_obj['files_scanned']}`")
    policy = index_obj.get("policy", {})
    lines.append(f"- Max evidence per concept: `{policy.get('max_evidence_per_concept', 0)}`")
    kind_quota = policy.get("kind_quota", {})
    if kind_quota:
        quota_desc = ", ".join(f"{k}:{v}" for k, v in kind_quota.items())
        lines.append(f"- Kind quota: `{quota_desc}`")
    lines.append("")

    base = out_md.parent

    for c in index_obj["concepts"]:
        lines.append(f"## {c['concept']} (`{c['concept_id']}`)")
        if c.get("aliases"):
            lines.append(f"- Aliases: `{', '.join(c['aliases'])}`")
        lines.append(f"- Evidence count: `{len(c['evidence'])}`")
        lines.append(f"- Evidence before policy: `{c.get('evidence_total_before_policy', len(c['evidence']))}`")
        top = c["evidence"][:top_evidence_md]
        if not top:
            lines.append("- Evidence: none")
        else:
            lines.append("- Top evidence:")
            for e in top:
                rel = Path(e["path"])
                try:
                    rel = rel.relative_to(base)
                except ValueError:
                    rel = Path("../..") / rel
                lines.append(
                    f"  - [{e['title']}]({rel.as_posix()}) | `{e['kind']}` | score={e['score']} | basis={','.join(e['match_basis'])}"
                )
        lines.append("")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_placeholder_patterns(pattern_file: Path | None) -> list[re.Pattern[str]]:
    patterns = list(DEFAULT_PLACEHOLDER_PATTERNS)
    if pattern_file:
        for raw in pattern_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return [re.compile(pat, re.IGNORECASE) for pat in patterns]


def is_placeholder_like(token: str, patterns: list[re.Pattern[str]]) -> bool:
    for pat in patterns:
        if pat.search(token):
            return True
    return False


def in_template_context(path: Path) -> bool:
    s = path.as_posix()
    return "/_TEMPLATE/" in s or path.name.startswith("000-template")


def classify_missing_level(
    *,
    source: Path,
    target: str,
    is_code_path: bool,
    link_report_level: str,
    placeholder_patterns: list[re.Pattern[str]],
) -> str:
    if link_report_level == "strict":
        return "error"

    placeholder_like = is_placeholder_like(target, placeholder_patterns)
    template_like = in_template_context(source)

    if link_report_level == "lenient":
        if is_code_path:
            return "note"
        if placeholder_like or template_like:
            return "note"
        return "error"

    # balanced
    if placeholder_like or template_like:
        return "note"
    return "error"


def resolve_local_path(source_file: Path, target: str, repo_root: Path) -> bool:
    candidates = [target]
    # Support repo-prefixed paths, e.g. `<repo-name>/03_Goal-Projects/...`.
    if target.startswith(f"{repo_root.name}/"):
        candidates.append(target[len(repo_root.name) + 1 :])

    for c in candidates:
        if not c:
            continue
        resolved = source_file.parent / c
        resolved_root = repo_root / c
        if resolved.exists() or resolved_root.exists():
            return True
    return False


def build_link_report(
    scope_dirs: list[Path],
    report_path: Path,
    *,
    version_tag: str,
    link_report_level: str,
    placeholder_patterns: list[re.Pattern[str]],
) -> dict:
    repo_root = Path.cwd()
    md_files = []
    for s in scope_dirs:
        for p in sorted(s.rglob("*.md")):
            ps = p.as_posix()
            if "/.agents/" in ps or p.name.startswith("_"):
                continue
            md_files.append(p)

    checked = 0
    checked_code = 0
    markdown_errors: list[tuple[str, str]] = []
    markdown_notes: list[tuple[str, str]] = []
    code_errors: list[tuple[str, str]] = []
    code_notes: list[tuple[str, str]] = []

    for f in md_files:
        txt = f.read_text(encoding="utf-8", errors="ignore")

        for m in LINK_RE.finditer(txt):
            target = m.group(1).strip().split()[0]
            target = target.split("#", 1)[0]
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:", "tel:", "#"))
                or "<" in target
                or ">" in target
                or "://" in target
            ):
                continue
            checked += 1
            if resolve_local_path(f, target, repo_root):
                continue
            level = classify_missing_level(
                source=f,
                target=target,
                is_code_path=False,
                link_report_level=link_report_level,
                placeholder_patterns=placeholder_patterns,
            )
            if level == "note":
                markdown_notes.append((f.as_posix(), target))
            else:
                markdown_errors.append((f.as_posix(), target))

        # Also validate path-like inline code spans (repo style frequently uses backticks for paths).
        for m in CODE_RE.finditer(txt):
            token = m.group(1).strip()
            if "/" not in token:
                continue
            if (
                token.startswith(("http://", "https://", "mailto:", "python", "rg ", "find "))
                or "<" in token
                or ">" in token
                or any(ch in token for ch in ["*", "|", "$", "^"])
            ):
                continue
            if not (
                token.endswith(".md")
                or token.endswith("/")
                or token.startswith("./")
                or token.startswith("../")
                or token.startswith(f"{repo_root.name}/")
            ):
                continue
            checked_code += 1
            if resolve_local_path(f, token, repo_root):
                continue
            level = classify_missing_level(
                source=f,
                target=token,
                is_code_path=True,
                link_report_level=link_report_level,
                placeholder_patterns=placeholder_patterns,
            )
            if level == "note":
                code_notes.append((f.as_posix(), token))
            else:
                code_errors.append((f.as_posix(), token))

    report = {
        "version": version_tag,
        "link_report_level": link_report_level,
        "checked_local_links": checked,
        "checked_code_paths": checked_code,
        "markdown": {
            "error": len(markdown_errors),
            "note": len(markdown_notes),
            "error_samples": markdown_errors[:30],
            "note_samples": markdown_notes[:30],
        },
        "code_paths": {
            "error": len(code_errors),
            "note": len(code_notes),
            "error_samples": code_errors[:30],
            "note_samples": code_notes[:30],
        },
    }

    lines = [
        f"# Link Check Report ({version_tag})",
        "",
        f"- Link report level: `{link_report_level}`",
        f"- Checked local markdown links: `{checked}`",
        f"- Markdown errors: `{len(markdown_errors)}`",
        f"- Markdown notes: `{len(markdown_notes)}`",
        f"- Checked inline code paths: `{checked_code}`",
        f"- Inline code path errors: `{len(code_errors)}`",
        f"- Inline code path notes: `{len(code_notes)}`",
        "",
        "## Markdown Error Samples",
    ]

    if not markdown_errors:
        lines.append("- none")
    else:
        for src, tgt in markdown_errors[:30]:
            lines.append(f"- `{src}` -> `{tgt}`")

    lines.extend(["", "## Markdown Note Samples"])
    if not markdown_notes:
        lines.append("- none")
    else:
        for src, tgt in markdown_notes[:30]:
            lines.append(f"- `{src}` -> `{tgt}`")

    lines.extend(["", "## Inline Code Path Error Samples"])
    if not code_errors:
        lines.append("- none")
    else:
        for src, tgt in code_errors[:30]:
            lines.append(f"- `{src}` -> `{tgt}`")

    lines.extend(["", "## Inline Code Path Note Samples"])
    if not code_notes:
        lines.append("- none")
    else:
        for src, tgt in code_notes[:30]:
            lines.append(f"- `{src}` -> `{tgt}`")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report


def build_summary(index_obj: dict, link_stats: dict, *, args: argparse.Namespace) -> dict:
    kind_counts: dict[str, int] = {}
    evidence_total = 0
    dropped_total = 0
    for c in index_obj.get("concepts", []):
        before = int(c.get("evidence_total_before_policy", len(c.get("evidence", []))))
        after = len(c.get("evidence", []))
        dropped_total += max(before - after, 0)
        for e in c.get("evidence", []):
            evidence_total += 1
            k = str(e.get("kind", "other"))
            kind_counts[k] = kind_counts.get(k, 0) + 1

    return {
        "version": index_obj.get("version"),
        "profile": index_obj.get("profile"),
        "built_at": index_obj.get("built_at"),
        "scope": index_obj.get("scope"),
        "files_scanned": index_obj.get("files_scanned"),
        "concepts": len(index_obj.get("concepts", [])),
        "evidence_total": evidence_total,
        "dropped_by_policy_total": dropped_total,
        "evidence_kind_counts": kind_counts,
        "policy": index_obj.get("policy", {}),
        "link_report": link_stats,
        "args": {
            "seeds": args.seeds,
            "out_json": args.out_json,
            "out_md": args.out_md,
            "link_report": args.link_report,
            "summary_json": args.summary_json,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build concept->evidence index for repo markdown docs.")
    ap.add_argument("--scope", action="append", default=[])
    ap.add_argument("--seeds", default="06_Infra/indexing/concept-seeds.yaml")
    ap.add_argument("--profile", choices=["v1", "v1_1"], default="v1_1")
    ap.add_argument("--out-json", default="06_Infra/indexing/repo-concept-index.v1.json")
    ap.add_argument("--out-md", default="06_Infra/indexing/repo-concept-index.v1.md")
    ap.add_argument("--link-report", default="06_Infra/indexing/reports/link-check.v1.md")
    ap.add_argument("--summary-json", default="")
    ap.add_argument("--max-evidence-per-concept", type=int, default=-1)
    ap.add_argument("--kind-quota", default="")
    ap.add_argument("--top-evidence-md", type=int, default=8)
    ap.add_argument("--link-report-level", choices=["strict", "balanced", "lenient"], default="")
    ap.add_argument("--placeholder-patterns", default="")
    args = ap.parse_args()

    scope_values = args.scope or [
        "00_Protocol",
        "03_Goal-Projects",
        "05_Resources/network",
        "07_Principles",
        "08_Operations",
    ]
    scopes = [Path(x) for x in scope_values]

    if args.max_evidence_per_concept >= 0:
        max_evidence_per_concept = args.max_evidence_per_concept
    else:
        max_evidence_per_concept = 12 if args.profile == "v1_1" else 0

    if args.kind_quota:
        kind_quota = parse_kind_quota(args.kind_quota)
    else:
        kind_quota = dict(DEFAULT_V1_1_KIND_QUOTA if args.profile == "v1_1" else {})

    if args.link_report_level:
        link_report_level = args.link_report_level
    else:
        link_report_level = "balanced" if args.profile == "v1_1" else "strict"

    placeholder_file = Path(args.placeholder_patterns) if args.placeholder_patterns else None
    placeholder_patterns = load_placeholder_patterns(placeholder_file)

    concepts = load_concepts(Path(args.seeds))
    docs = list(iter_docs(scopes))

    version_tag = "v1.1" if args.profile == "v1_1" else "v1"
    index_obj = build_index(
        concepts,
        docs,
        [s.as_posix() for s in scopes],
        profile=args.profile,
        version_tag=version_tag,
        max_evidence_per_concept=max_evidence_per_concept,
        kind_quota=kind_quota,
    )

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(index_obj, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(index_obj, out_md, top_evidence_md=args.top_evidence_md)

    link_report = Path(args.link_report)
    link_report.parent.mkdir(parents=True, exist_ok=True)
    link_stats = build_link_report(
        scopes,
        link_report,
        version_tag=version_tag,
        link_report_level=link_report_level,
        placeholder_patterns=placeholder_patterns,
    )

    if args.summary_json:
        summary_obj = build_summary(index_obj, link_stats, args=args)
        summary_path = Path(args.summary_json)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary_obj, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] summary_json={summary_path.as_posix()}")

    print(f"[OK] profile={args.profile} version={version_tag}")
    print(f"[OK] concepts={len(index_obj['concepts'])}, files_scanned={index_obj['files_scanned']}")
    print(
        "[OK] policy="
        f"max={max_evidence_per_concept} kind_quota={quota_to_arg(kind_quota) or 'none'} "
        f"link_level={link_report_level}"
    )
    print(f"[OK] out_json={out_json.as_posix()}")
    print(f"[OK] out_md={out_md.as_posix()}")
    print(
        "[OK] link_report="
        f"{link_report.as_posix()} md_error={link_stats['markdown']['error']} "
        f"md_note={link_stats['markdown']['note']} code_error={link_stats['code_paths']['error']} "
        f"code_note={link_stats['code_paths']['note']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
