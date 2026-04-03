---
name: memo-audio-transcribe
description: Offline audio transcription into the MEMO repo. Use when the user asks to transcribe audio (mp3/m4a/wav), extract a transcript/文字稿, or turn a recording into transcript.md/transcript.txt/segments.jsonl in `01_Inbox/`.
---

# MEMO Audio Transcribe

Transcribe local audio files **offline** (no upload) and write transcript outputs into the MEMO inbox.

## Run

From the MEMO repo root:

`python3 plugins/memo-audio-transcribe/scripts/run_transcribe.py /absolute/path/to/audio.mp3`

Batch:

`python3 plugins/memo-audio-transcribe/scripts/run_transcribe.py /path/a.mp3 /path/b.m4a`

## Outputs

For each input audio, the default output directory is:

`01_Inbox/<YYYYMMDD_HHMMSS>_<audio-basename>/`

Files:

- `transcript.md` (timestamped segments)
- `transcript.txt` (plain text)
- `segments.v1.jsonl` (structured segments)
- `meta.v1.json` (settings + provenance)

## Notes

- Default model: Whisper **small** (CTranslate2), CPU `int8`.
- Dependencies and model files are cached under the user cache directory (not committed into git).
