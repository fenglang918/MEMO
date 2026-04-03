#!/usr/bin/env python3
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


MODEL_REPO = "Systran/faster-whisper-small"
MODELSCOPE_BASE = f"https://modelscope.cn/models/{MODEL_REPO}/resolve/master"
MODEL_FILES = [
    "config.json",
    "configuration.json",
    "tokenizer.json",
    "vocabulary.txt",
    "model.bin",
]
MODEL_BIN_SHA256 = (
    "3e305921506d8872816023e4c273e75d2419fb89b24da97b4fe7bce14170d671"
)

DEFAULT_PIP_INDEX_URL = "https://pypi.tuna.tsinghua.edu.cn/simple"
DEFAULT_PIP_TRUSTED_HOST = "pypi.tuna.tsinghua.edu.cn"


@dataclass(frozen=True)
class CachePaths:
    root: Path
    venv_dir: Path
    model_dir: Path


def _repo_root_from_here() -> Path:
    # plugins/memo-audio-transcribe/scripts/run_transcribe.py -> repo root is parents[3]
    here = Path(__file__).resolve()
    try:
        return here.parents[3]
    except IndexError as e:
        raise RuntimeError(f"Cannot infer repo root from {here}") from e


def _default_cache_dir() -> Path:
    override = os.environ.get("MEMO_AUDIO_TRANSCRIBE_CACHE_DIR")
    if override:
        return Path(override).expanduser()

    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg).expanduser() / "memo-audio-transcribe"

    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "memo-audio-transcribe"

    return Path.home() / ".cache" / "memo-audio-transcribe"


def _cache_paths() -> CachePaths:
    cache_root = _default_cache_dir()
    return CachePaths(
        root=cache_root,
        venv_dir=cache_root / "venv",
        model_dir=cache_root / "models" / "whisper-small-ct2",
    )


def _run(cmd: list[str], *, check: bool = True, env: Optional[dict[str, str]] = None) -> None:
    print(f"+ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=check, env=env)


def _venv_python(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def _ensure_venv(venv_dir: Path) -> Path:
    python_path = _venv_python(venv_dir)
    if python_path.exists():
        return python_path

    venv_dir.parent.mkdir(parents=True, exist_ok=True)
    _run([sys.executable, "-m", "venv", str(venv_dir)])
    return python_path


def _parse_trusted_host(index_url: str) -> Optional[str]:
    try:
        host = urlparse(index_url).hostname
        return host
    except Exception:
        return None


def _ensure_deps(venv_python: Path) -> None:
    try:
        _run([str(venv_python), "-c", "import faster_whisper"], check=True)
        return
    except subprocess.CalledProcessError:
        pass

    index_url = os.environ.get("PIP_INDEX_URL", DEFAULT_PIP_INDEX_URL)
    trusted_host = os.environ.get(
        "PIP_TRUSTED_HOST",
        _parse_trusted_host(index_url) or DEFAULT_PIP_TRUSTED_HOST,
    )

    pip_env = os.environ.copy()
    pip_env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")

    pip_cmd = [
        str(venv_python),
        "-m",
        "pip",
        "install",
        "-i",
        index_url,
        "--trusted-host",
        trusted_host,
        "faster-whisper==1.2.1",
    ]
    _run(pip_cmd, env=pip_env)


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _download_with_curl(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)

    curl = shutil.which("curl")
    if not curl:
        raise RuntimeError("curl is required but not found in PATH")

    cmd = [
        curl,
        "-L",
        "--fail",
        "--retry",
        "5",
        "--retry-delay",
        "2",
        "-o",
        str(dest),
        url,
    ]
    # Resume if a partial file exists (safe even when starting from scratch).
    if dest.exists() and dest.stat().st_size > 0:
        cmd.insert(1, "-C")
        cmd.insert(2, "-")

    _run(cmd)


def _ensure_model(model_dir: Path) -> None:
    model_dir.mkdir(parents=True, exist_ok=True)

    # Download required files.
    for fname in MODEL_FILES:
        url = f"{MODELSCOPE_BASE}/{fname}"
        dest = model_dir / fname

        if fname == "model.bin" and dest.exists():
            # Verify sha first; redownload if mismatch.
            try:
                if _sha256_file(dest) == MODEL_BIN_SHA256:
                    continue
            except Exception:
                pass
            dest.unlink(missing_ok=True)

        if dest.exists() and dest.stat().st_size > 0 and fname != "model.bin":
            continue

        _download_with_curl(url, dest)

        if fname == "model.bin":
            got = _sha256_file(dest)
            if got != MODEL_BIN_SHA256:
                dest.unlink(missing_ok=True)
                raise RuntimeError(
                    "Downloaded model.bin sha256 mismatch: "
                    f"got {got}, expected {MODEL_BIN_SHA256}"
                )


def _sanitize_stem(stem: str) -> str:
    s = stem.strip()
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s)
    s = re.sub(r"-{2,}", "-", s)
    s = s.strip("-")
    return s or "audio"


def _unique_out_dir(out_root: Path, base_name: str) -> Path:
    out_root.mkdir(parents=True, exist_ok=True)
    candidate = out_root / base_name
    if not candidate.exists():
        return candidate
    for i in range(2, 1000):
        p = out_root / f"{base_name}_{i:02d}"
        if not p.exists():
            return p
    raise RuntimeError(f"Too many collisions under {out_root} for {base_name}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="memo-audio-transcribe",
        description="Offline audio transcription into MEMO/01_Inbox (bootstrap venv + download model).",
    )
    parser.add_argument("audio", nargs="+", help="Input audio file paths (mp3/m4a/wav).")
    parser.add_argument(
        "--out-root",
        default=None,
        help="Output root directory (default: <repo>/01_Inbox).",
    )
    parser.add_argument(
        "--language",
        default="zh",
        help="Language code (e.g., zh/en) or 'auto' (default: zh).",
    )
    parser.add_argument(
        "--vad",
        action="store_true",
        help="Enable VAD filter (default: off).",
    )
    parser.add_argument(
        "--beam-size",
        type=int,
        default=5,
        help="Beam size (default: 5).",
    )
    args = parser.parse_args(argv)

    repo_root = _repo_root_from_here()
    out_root = Path(args.out_root).expanduser() if args.out_root else (repo_root / "01_Inbox")

    cache = _cache_paths()
    cache.root.mkdir(parents=True, exist_ok=True)

    venv_python = _ensure_venv(cache.venv_dir)
    _ensure_deps(venv_python)
    _ensure_model(cache.model_dir)

    impl = repo_root / "plugins" / "memo-audio-transcribe" / "scripts" / "transcribe_impl.py"
    if not impl.exists():
        raise RuntimeError(f"Missing implementation script: {impl}")

    failures = 0
    for audio in args.audio:
        audio_path = Path(audio).expanduser().resolve()
        if not audio_path.exists():
            print(f"ERROR: audio not found: {audio_path}", file=sys.stderr)
            failures += 1
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stem = _sanitize_stem(audio_path.stem)
        out_dir = _unique_out_dir(out_root, f"{timestamp}_{stem}")

        cmd = [
            str(venv_python),
            str(impl),
            "--audio",
            str(audio_path),
            "--out-dir",
            str(out_dir),
            "--model-dir",
            str(cache.model_dir),
            "--beam-size",
            str(args.beam_size),
        ]
        if args.language:
            cmd.extend(["--language", args.language])
        if args.vad:
            cmd.append("--vad")

        try:
            _run(cmd)
            print(f"OK: wrote transcript to {out_dir}", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: transcription failed for {audio_path}: {e}", file=sys.stderr)
            failures += 1

    if failures:
        print(f"Done with failures={failures}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
