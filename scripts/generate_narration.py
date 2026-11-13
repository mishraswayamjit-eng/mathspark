"""Generate pre-recorded narration audio with Sarvam text-to-speech.

What it does
    1. Pulls the narration script (question + solution-step sentences) from the
       deployed app's read-only admin export, /api/admin/narration-manifest.
       The app builds that text with the same function it speaks with, so the
       recording always says exactly what the on-screen walkthrough shows.
    2. Sends each sentence to Sarvam's text-to-speech API.
    3. Saves one audio file per part as  <out>/<questionId>/<part>.<ext>
       (part = "question" or "step-N"), the layout the app's read-aloud expects.

It only ever reads verified content and writes audio files. It never changes a
question, an answer or the database.

Secrets come from environment variables and are never written anywhere:
    SEED_SECRET       the app's admin secret (same one the seed routes use)
    SARVAM_API_KEY    your Sarvam API subscription key (not needed for --dry-run)

Typical use (PowerShell)
    $env:SEED_SECRET = "..."; $env:SARVAM_API_KEY = "..."
    # 1. See how much there is, without calling Sarvam:
    python scripts/generate_narration.py --base-url https://<your-app> --dry-run --max-questions 50
    # 2. Record a small pilot into the app's public folder:
    python scripts/generate_narration.py --base-url https://<your-app> --max-questions 50 --out public/narration
    # 3. Tell the app where the files are (Vercel env var), then redeploy:
    #    NEXT_PUBLIC_NARRATION_AUDIO_BASE=/narration

Safe to stop and re-run: parts that already have a file are skipped.

Sarvam request fields (endpoint, header, "text", "target_language_code",
"model", "speaker", "pace", "speech_sample_rate") follow Sarvam's published
REST example. "output_audio_codec" is the documented way to ask for MP3; if
your account returns WAV anyway the file is saved as .wav and the script tells
you to set NEXT_PUBLIC_NARRATION_AUDIO_EXT=wav. Check the model and speaker
names against your Sarvam dashboard before a large run.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SARVAM_URL = "https://api.sarvam.ai/text-to-speech"
MAX_CHARS = 2400          # Sarvam caps one request at about 2500 characters
SAFE_ID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")


def fail(message: str) -> None:
    print(f"\nStopped: {message}", file=sys.stderr)
    sys.exit(1)


def fetch_json(url: str, *, data: bytes | None = None, headers: dict | None = None, timeout: int = 60) -> dict:
    request = urllib.request.Request(url, data=data, headers=headers or {}, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_manifest_page(base_url: str, secret: str, page: int, limit: int, source: str | None, topic: str | None) -> dict:
    query = {"secret": secret, "page": str(page), "limit": str(limit)}
    if source:
        query["source"] = source
    if topic:
        query["topicId"] = topic
    url = f"{base_url.rstrip('/')}/api/admin/narration-manifest?{urllib.parse.urlencode(query)}"
    try:
        return fetch_json(url)
    except urllib.error.HTTPError as err:
        if err.code == 401:
            fail("the app rejected SEED_SECRET (401).")
        if err.code == 404:
            fail("the app has no /api/admin/narration-manifest route yet. Deploy the latest code first.")
        fail(f"the narration export returned HTTP {err.code}.")
    except urllib.error.URLError as err:
        fail(f"could not reach {base_url}: {err.reason}")
    return {}


def audio_extension(audio: bytes) -> str:
    """Work out what Sarvam actually sent, from the file's first bytes."""
    if audio[:4] == b"RIFF":
        return "wav"
    if audio[:3] == b"ID3" or (len(audio) > 1 and audio[0] == 0xFF and (audio[1] & 0xE0) == 0xE0):
        return "mp3"
    if audio[:4] == b"OggS":
        return "ogg"
    if audio[:4] == b"fLaC":
        return "flac"
    return "bin"


def synthesize(text: str, api_key: str, args: argparse.Namespace) -> bytes:
    body = {
        "text": text,
        "target_language_code": args.language,
        "model": args.model,
        "speaker": args.speaker,
        "pace": args.pace,
        "speech_sample_rate": args.sample_rate,
        "output_audio_codec": args.codec,
    }
    headers = {"api-subscription-key": api_key, "Content-Type": "application/json"}
    payload = json.dumps(body).encode("utf-8")

    for attempt in range(1, 5):
        try:
            result = fetch_json(SARVAM_URL, data=payload, headers=headers, timeout=90)
            audios = result.get("audios") or []
            if not audios:
                raise ValueError("Sarvam returned no audio")
            return base64.b64decode(audios[0])
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")[:300]
            if err.code in (401, 403):
                fail(f"Sarvam rejected the API key (HTTP {err.code}).")
            if err.code in (400, 422):
                fail(f"Sarvam rejected the request (HTTP {err.code}): {detail}\n"
                     "Check --model / --speaker / --codec against your Sarvam dashboard.")
            if attempt == 4:
                raise
            wait = 2 ** attempt
            print(f"    Sarvam HTTP {err.code}; retrying in {wait}s")
            time.sleep(wait)
        except (urllib.error.URLError, ValueError) as err:
            if attempt == 4:
                raise
            wait = 2 ** attempt
            print(f"    {err}; retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate narration audio with Sarvam text-to-speech.")
    parser.add_argument("--base-url", required=True, help="Deployed app URL, e.g. https://your-app.vercel.app")
    parser.add_argument("--out", default="public/narration", help="Folder to write audio into (default: public/narration)")
    parser.add_argument("--source", help="Only questions with this source, e.g. hand_crafted")
    parser.add_argument("--topic", help="Only questions in this topicId, e.g. ch11 or grade5")
    parser.add_argument("--max-questions", type=int, default=50, help="Stop after this many questions (default 50; 0 = all)")
    parser.add_argument("--page-size", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true", help="Count parts and characters only; do not call Sarvam")
    parser.add_argument("--language", default="en-IN")
    parser.add_argument("--model", default="bulbul:v3", help="Sarvam model (confirm in your dashboard)")
    parser.add_argument("--speaker", default="shubh", help="Sarvam speaker for that model (confirm in your dashboard)")
    parser.add_argument("--pace", type=float, default=0.95)
    parser.add_argument("--sample-rate", type=int, default=24000)
    parser.add_argument("--codec", default="mp3")
    parser.add_argument("--delay", type=float, default=0.25, help="Seconds to wait between Sarvam calls")
    args = parser.parse_args()

    secret = os.environ.get("SEED_SECRET", "")
    if not secret:
        fail("set the SEED_SECRET environment variable first.")
    api_key = os.environ.get("SARVAM_API_KEY", "")
    if not args.dry_run and not api_key:
        fail("set the SARVAM_API_KEY environment variable first (or use --dry-run).")

    out_dir = Path(args.out)
    questions_seen = 0
    parts_total = parts_made = parts_skipped = parts_too_long = 0
    chars_total = 0
    extensions_seen: set[str] = set()
    page = 0

    while True:
        data = fetch_manifest_page(args.base_url, secret, page, args.page_size, args.source, args.topic)
        items = data.get("items") or []

        current_question = None
        for item in items:
            qid, part, text = item.get("questionId", ""), item.get("part", ""), item.get("text", "")
            if not qid or not part or not text:
                continue
            if qid != current_question:
                if args.max_questions and questions_seen >= args.max_questions:
                    break
                current_question = qid
                questions_seen += 1

            # Question ids become folder names: refuse anything that is not a plain id.
            if any(ch not in SAFE_ID_CHARS for ch in qid) or any(ch not in SAFE_ID_CHARS for ch in part):
                print(f"  skipping {qid}/{part}: unexpected characters in the id")
                continue

            parts_total += 1
            chars_total += len(text)
            if len(text) > MAX_CHARS:
                parts_too_long += 1
                print(f"  skipping {qid}/{part}: {len(text)} characters is over Sarvam's limit")
                continue
            if args.dry_run:
                continue

            folder = out_dir / qid
            if any(folder.glob(f"{part}.*")):
                parts_skipped += 1
                continue

            audio = synthesize(text, api_key, args)
            ext = audio_extension(audio)
            extensions_seen.add(ext)
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"{part}.{ext}").write_bytes(audio)
            parts_made += 1
            print(f"  {qid}/{part}.{ext}  ({len(audio) // 1024} KB)")
            time.sleep(args.delay)

        reached_cap = bool(args.max_questions) and questions_seen >= args.max_questions
        if data.get("done") or not items or reached_cap:
            break
        page += 1

    print("\nSummary")
    print(f"  questions covered : {questions_seen}")
    print(f"  narration parts   : {parts_total}  ({chars_total:,} characters)")
    if parts_too_long:
        print(f"  too long, skipped : {parts_too_long}")
    if args.dry_run:
        print("  dry run: nothing was sent to Sarvam and no files were written.")
        return
    print(f"  recorded now      : {parts_made}")
    print(f"  already on disk   : {parts_skipped}")
    print(f"  written under     : {out_dir}")
    if extensions_seen and extensions_seen != {"mp3"}:
        print(f"\n  Note: Sarvam returned {sorted(extensions_seen)} rather than mp3.")
        print("  Set NEXT_PUBLIC_NARRATION_AUDIO_EXT to that extension in Vercel, or the app will not find the files.")


if __name__ == "__main__":
    main()
