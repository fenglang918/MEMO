#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path


REQUIRED_RELATIVE_PATHS = (
    Path("README.md"),
    Path("06_Infra/skills/portable/prism.md"),
    Path("06_Infra/skills/native/me-network-crm/SKILL.md"),
)


def _repo_root() -> Path:
    # .../MEMO/public/repo/06_Infra/i18n/switch_language.py -> repo root is parents[2]
    return Path(__file__).resolve().parents[2]


def _langpacks_dir(repo_root: Path) -> Path:
    return repo_root / "06_Infra" / "i18n" / "langpacks"


def _iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.name in {".DS_Store"}:
            continue
        if p.suffix == ".pyc":
            continue
        if "__pycache__" in p.parts:
            continue
        out.append(p)
    return sorted(out)


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _ensure_required(pack_root: Path) -> None:
    missing: list[str] = []
    for rel in REQUIRED_RELATIVE_PATHS:
        if not (pack_root / rel).is_file():
            missing.append(str(rel))
    if missing:
        msg = "\n".join(f"- {p}" for p in missing)
        raise SystemExit(f"Langpack missing required files under {pack_root}:\n{msg}")


def _write_state(repo_root: Path, lang: str, pack_root: Path, changed: list[Path]) -> None:
    state_path = repo_root / ".memo_lang"
    payload = {
        "lang": lang,
        "applied_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "pack_root": str(pack_root.relative_to(repo_root)),
        "changed_files": [str(p) for p in changed],
    }
    state_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Switch MEMO repo language by applying files from 06_Infra/i18n/langpacks/<lang>/ onto repo root."
    )
    parser.add_argument("--list", action="store_true", help="List available languages.")
    parser.add_argument("--lang", default=None, help="Language to apply (e.g. zh, en).")
    parser.add_argument("--apply", action="store_true", help="Actually write files (otherwise dry-run).")
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Backup overwritten files into .memo_lang_backup/<timestamp>_<lang>/ before writing.",
    )
    args = parser.parse_args(argv)

    repo_root = _repo_root()
    langpacks_dir = _langpacks_dir(repo_root)

    if args.list:
        if not langpacks_dir.exists():
            print(f"No langpacks dir found: {langpacks_dir}", file=sys.stderr)
            return 2
        langs = sorted([p.name for p in langpacks_dir.iterdir() if p.is_dir() and not p.name.startswith(".")])
        for l in langs:
            print(l)
        return 0

    if not args.lang:
        print("--lang is required (or use --list).", file=sys.stderr)
        return 2

    pack_root = langpacks_dir / args.lang
    if not pack_root.exists():
        print(f"Langpack not found: {pack_root}", file=sys.stderr)
        return 2

    _ensure_required(pack_root)

    src_files = _iter_files(pack_root)
    planned: list[tuple[Path, Path]] = []
    changed: list[Path] = []

    for src in src_files:
        rel = src.relative_to(pack_root)
        dst = repo_root / rel
        planned.append((src, dst))

        src_bytes = _read_bytes(src)
        if dst.exists():
            dst_bytes = _read_bytes(dst)
            if dst_bytes == src_bytes:
                continue
        changed.append(rel)

    if not args.apply:
        print(f"[dry-run] lang={args.lang} pack={pack_root}")
        for rel in changed:
            print(f"- would write: {rel}")
        print(f"total: {len(changed)} file(s)")
        return 0

    backup_root: Path | None = None
    if args.backup:
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_root = repo_root / ".memo_lang_backup" / f"{ts}_{args.lang}"

    for src, dst in planned:
        rel = src.relative_to(pack_root)
        if rel not in set(changed):
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if backup_root and dst.exists():
            backup_path = backup_root / rel
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dst, backup_path)
        shutil.copy2(src, dst)

    _write_state(repo_root, args.lang, pack_root, changed)
    print(f"[applied] lang={args.lang} total={len(changed)} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

