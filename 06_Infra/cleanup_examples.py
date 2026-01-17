#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path


ARCHIVE_DIRNAME = ".memo_examples_archive"

EXAMPLE_PATHS = (
    Path("05_Resources/network/people/momo.md"),
    Path("03_Goal-Projects/active/2026-01-MEMO-开源模板发布"),
    Path("03_Goal-Projects/active/2026-01-读博-vs-直接工作"),
    Path("06_Infra/i18n/langpacks/zh/03_Goal-Projects/active/2026-01-MEMO-开源模板发布"),
    Path("06_Infra/i18n/langpacks/en/03_Goal-Projects/active/2026-01-MEMO-开源模板发布"),
    # Profile examples
    Path("04_Assets/profile/Me.example.md"),
    Path("04_Assets/profile/README.example.md"),
    Path("04_Assets/profile/signals.example.md"),
    Path("04_Assets/profile/timeline.example.md"),
    Path("04_Assets/profile/values.example.md"),
    # Desires examples
    Path("02_Desires/desires.example.md"),
    Path("02_Desires/preferences.example.md"),
    Path("02_Desires/values.example.md"),
    # i18n langpacks for examples (so switching language won't re-create them)
    Path("06_Infra/i18n/langpacks/zh/02_Desires/desires.example.md"),
    Path("06_Infra/i18n/langpacks/zh/02_Desires/preferences.example.md"),
    Path("06_Infra/i18n/langpacks/zh/02_Desires/values.example.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/desires.example.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/preferences.example.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/values.example.md"),
)

DOC_PATHS = (
    Path("03_Goal-Projects/active/README.md"),
    Path("03_Goal-Projects/README.md"),
    Path("06_Infra/i18n/README.md"),
    # Remove example references when examples are archived/deleted
    Path("04_Assets/profile/README.md"),
    Path("04_Assets/profile/Me.md"),
    Path("04_Assets/profile/signals.md"),
    Path("04_Assets/profile/timeline.md"),
    Path("04_Assets/profile/values.md"),
    Path("02_Desires/README.md"),
    Path("02_Desires/values.md"),
    Path("02_Desires/preferences.md"),
    Path("02_Desires/desires.md"),
    # Keep langpacks consistent with cleaned repo (avoid reintroducing example references)
    Path("06_Infra/i18n/langpacks/zh/02_Desires/README.md"),
    Path("06_Infra/i18n/langpacks/zh/02_Desires/values.md"),
    Path("06_Infra/i18n/langpacks/zh/02_Desires/preferences.md"),
    Path("06_Infra/i18n/langpacks/zh/02_Desires/desires.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/README.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/values.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/preferences.md"),
    Path("06_Infra/i18n/langpacks/en/02_Desires/desires.md"),
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _archives_root(repo_root: Path) -> Path:
    return repo_root / ARCHIVE_DIRNAME


def _remove_demo_references(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if "2026-01-MEMO-开源模板发布" in line:
            continue
        if "2026-01-读博-vs-直接工作" in line:
            continue
        if "本模板额外提供" in line:
            continue
        if "脱敏示例项目" in line and "TPCD" in line:
            continue
        if "（见 `03_Goal-Projects/active/2026-01-MEMO-开源模板发布/`）" in line:
            line = line.replace("（见 `03_Goal-Projects/active/2026-01-MEMO-开源模板发布/`）。", "。")
        if ".example.md" in line and "参考" in line:
            continue
        if ".example.md" in line and "本模板" in line:
            continue
        if "profile.example.md" in line:
            continue
        if "history.example.md" in line:
            continue
        if "`signals.example.md`" in line:
            continue
        lines.append(line)
    return "\n".join(lines).rstrip() + "\n"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _copy_for_backup(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=False)
    else:
        shutil.copy2(src, dst)


def _remove_path(p: Path) -> None:
    if p.is_dir():
        shutil.rmtree(p)
        return
    p.unlink()


def _move_to_archive(repo_root: Path, rel: Path, archive_root: Path) -> None:
    src = repo_root / rel
    dst = archive_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))


def _ensure_restore_dst_empty(repo_root: Path, rel: Path, *, force: bool) -> None:
    dst = repo_root / rel
    if not dst.exists():
        return
    if force:
        _remove_path(dst)
        return
    raise SystemExit(f"Restore would overwrite existing path. Use --force to overwrite: {rel}")


def _manifest_path(archive_root: Path) -> Path:
    return archive_root / "manifest.json"


def _write_manifest(archive_root: Path, payload: dict) -> None:
    _manifest_path(archive_root).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_manifest(archive_root: Path) -> dict:
    p = _manifest_path(archive_root)
    if not p.exists():
        raise SystemExit(f"Archive manifest not found: {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def _new_archive_id() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Clean up sanitized example content from a MEMO template repo.\n"
            "Dry-run by default. When applying, default mode is ARCHIVE (recoverable)."
        )
    )
    ap.add_argument("--list-archives", action="store_true", help=f"List archives under {ARCHIVE_DIRNAME}/.")
    ap.add_argument(
        "--restore",
        default=None,
        help=f"Restore from a previous archive id (folder name under {ARCHIVE_DIRNAME}/).",
    )
    ap.add_argument("--apply", action="store_true", help="Actually apply changes (default: dry-run).")
    ap.add_argument(
        "--mode",
        choices=("archive", "delete"),
        default="archive",
        help="When applying: archive (default) moves example paths into a local archive; delete removes them.",
    )
    ap.add_argument("--force", action="store_true", help="On restore, overwrite existing destination paths.")
    ap.add_argument(
        "--backup",
        action="store_true",
        help="When --mode=delete: backup removed/modified paths into .memo_cleanup_backup/<timestamp>/ before deleting.",
    )
    args = ap.parse_args(argv)

    repo_root = _repo_root()
    archives_root = _archives_root(repo_root)

    missing: list[str] = []
    for must in (repo_root / "00_Protocol", repo_root / "06_Infra"):
        if not must.exists():
            missing.append(str(must))
    if missing:
        msg = "\n".join(f"- {p}" for p in missing)
        print(f"Not a MEMO public template repo root: {repo_root}\nMissing:\n{msg}", file=sys.stderr)
        return 2

    if args.list_archives:
        if not archives_root.exists():
            return 0
        for p in sorted([p for p in archives_root.iterdir() if p.is_dir() and not p.name.startswith(".")]):
            print(p.name)
        return 0

    if args.restore:
        archive_root = archives_root / args.restore
        if not archive_root.exists():
            print(f"Archive not found: {archive_root}", file=sys.stderr)
            return 2
        manifest = _load_manifest(archive_root)
        moved = [Path(p) for p in manifest.get("moved_paths", [])]
        edited = [Path(p) for p in manifest.get("edited_docs", [])]

        if not args.apply:
            print(f"[dry-run] restore repo={repo_root} archive={archive_root.relative_to(repo_root)}")
            for rel in moved:
                print(f"- would restore (move back): {rel}")
            for rel in edited:
                print(f"- would restore (overwrite): {rel}")
            print(f"total: moved={len(moved)} edited={len(edited)}")
            return 0

        for rel in moved:
            src = archive_root / rel
            if not src.exists():
                raise SystemExit(f"Archive missing path: {rel}")
            _ensure_restore_dst_empty(repo_root, rel, force=args.force)
            (repo_root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(repo_root / rel))

        for rel in edited:
            src = archive_root / rel
            if not src.exists():
                raise SystemExit(f"Archive missing doc backup: {rel}")
            _ensure_restore_dst_empty(repo_root, rel, force=args.force)
            (repo_root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, repo_root / rel)

        print(f"[restored] repo={repo_root} archive={archive_root.relative_to(repo_root)}")
        return 0

    planned_remove: list[Path] = []
    for rel in EXAMPLE_PATHS:
        p = repo_root / rel
        if p.exists():
            planned_remove.append(rel)

    planned_edit: list[Path] = []
    for rel in DOC_PATHS:
        p = repo_root / rel
        if not p.exists():
            continue
        before = _read_text(p)
        after = _remove_demo_references(before)
        if after != before:
            planned_edit.append(rel)

    if not args.apply:
        print(f"[dry-run] repo={repo_root} mode={args.mode}")
        for rel in planned_remove:
            action = "archive" if args.mode == "archive" else "remove"
            print(f"- would {action}: {rel}")
        for rel in planned_edit:
            print(f"- would edit:   {rel} (remove demo references)")
        print(f"total: remove={len(planned_remove)} edit={len(planned_edit)}")
        return 0

    archive_root: Path | None = None
    backup_root: Path | None = None

    if args.mode == "archive":
        archive_id = _new_archive_id()
        archive_root = archives_root / archive_id
        archive_root.mkdir(parents=True, exist_ok=True)
    elif args.backup:
        archive_id = _new_archive_id()
        backup_root = repo_root / ".memo_cleanup_backup" / archive_id
        backup_root.mkdir(parents=True, exist_ok=True)

    if args.mode == "archive":
        assert archive_root is not None
        for rel in planned_remove:
            _move_to_archive(repo_root, rel, archive_root)
    else:
        for rel in planned_remove:
            p = repo_root / rel
            if backup_root:
                _copy_for_backup(p, backup_root / rel)
            _remove_path(p)

    for rel in planned_edit:
        p = repo_root / rel
        before = _read_text(p)
        after = _remove_demo_references(before)
        if before == after:
            continue
        if archive_root:
            _copy_for_backup(p, archive_root / rel)
        if backup_root:
            _copy_for_backup(p, backup_root / rel)
        _write_text(p, after)

    if archive_root:
        _write_manifest(
            archive_root,
            {
                "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "mode": args.mode,
                "moved_paths": [str(p) for p in planned_remove],
                "edited_docs": [str(p) for p in planned_edit],
            },
        )

    verb = "archived" if args.mode == "archive" else "deleted"
    print(f"[applied] repo={repo_root} {verb}={len(planned_remove)} edit={len(planned_edit)}")
    if archive_root:
        print(f"[archive] {archive_root.relative_to(repo_root)}")
    if backup_root:
        print(f"[backup] {backup_root.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
