#!/usr/bin/env python3
import argparse
import json
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def _fmt_ts(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    ms = int(round(seconds * 1000))
    s = ms // 1000
    ms = ms % 1000
    h = s // 3600
    m = (s % 3600) // 60
    s = s % 60
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"
    return f"{m:02d}:{s:02d}.{ms:03d}"


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main(argv: Optional[list[str]] = None) -> int:
    # Suppress known noisy numpy warnings occasionally triggered in mel extraction.
    warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*encountered in matmul.*")

    parser = argparse.ArgumentParser(prog="transcribe_impl")
    parser.add_argument("--audio", required=True, help="Input audio file path.")
    parser.add_argument("--out-dir", required=True, help="Output directory.")
    parser.add_argument("--model-dir", required=True, help="Local CTranslate2 model directory.")
    parser.add_argument("--language", default="zh", help="Language code or 'auto'.")
    parser.add_argument("--vad", action="store_true", help="Enable VAD filter.")
    parser.add_argument("--beam-size", type=int, default=5, help="Beam size.")
    parser.add_argument("--device", default="cpu", help="Device (default: cpu).")
    parser.add_argument("--compute-type", default="int8", help="Compute type (default: int8).")
    args = parser.parse_args(argv)

    audio_path = Path(args.audio).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    model_dir = Path(args.model_dir).expanduser().resolve()

    out_dir.mkdir(parents=True, exist_ok=True)

    from faster_whisper import WhisperModel  # noqa: WPS433

    model = WhisperModel(str(model_dir), device=args.device, compute_type=args.compute_type)

    language = None if args.language == "auto" else args.language
    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=args.beam_size,
        vad_filter=bool(args.vad),
    )

    meta = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "audio_path": str(audio_path),
        "out_dir": str(out_dir),
        "model_dir": str(model_dir),
        "model": "whisper-small (ctranslate2)",
        "settings": {
            "language": args.language,
            "vad_filter": bool(args.vad),
            "beam_size": args.beam_size,
            "device": args.device,
            "compute_type": args.compute_type,
        },
        "info": {
            "duration": getattr(info, "duration", None),
            "language": getattr(info, "language", None),
            "language_probability": getattr(info, "language_probability", None),
        },
    }

    meta_path = out_dir / "meta.v1.json"
    md_path = out_dir / "transcript.md"
    txt_path = out_dir / "transcript.txt"
    jsonl_path = out_dir / "segments.v1.jsonl"

    _write_json(meta_path, meta)

    with md_path.open("w", encoding="utf-8") as md, txt_path.open(
        "w", encoding="utf-8"
    ) as txt, jsonl_path.open("w", encoding="utf-8") as jsonl:
        md.write("# Transcript\n\n")
        md.write(f"- Source: `{audio_path}`\n")
        md.write(f"- Model: `{model_dir}` (whisper-small, ctranslate2)\n")
        md.write(f"- Language: `{args.language}`\n")
        if meta["info"]["duration"] is not None:
            md.write(f"- Duration (s): `{meta['info']['duration']}`\n")
        md.write("\n## Segments\n\n")

        for seg in segments_iter:
            start = float(seg.start)
            end = float(seg.end)
            text = (seg.text or "").strip()

            jsonl.write(
                json.dumps({"start": start, "end": end, "text": text}, ensure_ascii=False)
                + "\n"
            )
            md.write(f"- [{_fmt_ts(start)} → {_fmt_ts(end)}] {text}\n")
            if text:
                txt.write(text + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
