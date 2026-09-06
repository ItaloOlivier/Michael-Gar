#!/usr/bin/env python3
"""Generate the scroll-driven hero camera move from the Hamburg dive photo.

The brief: the camera starts where the photographer stood (low, to the side,
looking up at Michael as he leaves the pontoon), swings round and above him as
if mounted on his back, and rides him down through the surface. Scroll position
drives it. It must not read as a pan-and-zoom over a flat photo, which is why
this generates real novel views instead of transforming the still.

Pipeline
  1. image-to-video on fal.ai, seeded with images/gallery/hamburg-dive.jpg
  2. extract N evenly spaced frames with ffmpeg
  3. write them to images/hero-frames/ as progressively numbered JPEGs
  4. the page paints frame[round(scrollProgress * (N-1))] onto a canvas

Usage
  export FAL_KEY=...            # not stored in this repo
  python3 redesign/generate-hero.py            # generate + extract
  python3 redesign/generate-hero.py --frames-only   # re-extract from an existing mp4

Notes
  - The request id is written to .hero-job before the first poll, so a killed
    shell does not lose a paid job. Re-running picks the id back up.
  - Models drift. If MODEL 4xxs, check the live catalogue rather than guessing.
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "images" / "gallery" / "hamburg-dive.jpg"
OUT_DIR = ROOT / "images" / "hero-frames"
VIDEO = ROOT / "redesign" / "hero-move.mp4"
JOB_FILE = ROOT / "redesign" / ".hero-job"

MODEL = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
FRAMES = 48
FRAME_WIDTH = 1280

PROMPT = (
    "The camera begins low at the water's edge looking up at the diving "
    "triathlete, then sweeps upward and rotates behind him until it sits just "
    "above his back, locked to him like a body-mounted camera, and follows him "
    "down as he plunges into the water, breaking the surface with him. "
    "Continuous single take, smooth flying camera move, no cuts. "
    "Real daylight, overcast Hamburg sky, spectators and blue race barriers "
    "along the canal, splashing water."
)
NEGATIVE = "cuts, jump cuts, text, watermark, warped limbs, extra people, slideshow, zoom only"


def key() -> str:
    k = os.environ.get("FAL_KEY")
    if not k:
        sys.exit("FAL_KEY is not set. Export it, or source the .env that holds it.")
    return k


def post(url: str, payload: dict, k: str) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Key {k}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def get(url: str, k: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Key {k}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def upload(path: Path, k: str) -> str:
    """Put the source photo somewhere fal can read it."""
    import base64
    import mimetypes

    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def generate() -> None:
    k = key()
    if JOB_FILE.exists():
        request_id = JOB_FILE.read_text().strip()
        print(f"resuming job {request_id}")
    else:
        payload = {
            "prompt": PROMPT,
            "negative_prompt": NEGATIVE,
            "image_url": upload(SOURCE, k),
            "duration": "5",
            "cfg_scale": 0.5,
        }
        job = post(f"https://queue.fal.run/{MODEL}", payload, k)
        request_id = job["request_id"]
        JOB_FILE.write_text(request_id)  # before the first poll, not after
        print(f"queued {request_id}")

    status_url = f"https://queue.fal.run/{MODEL}/requests/{request_id}/status"
    result_url = f"https://queue.fal.run/{MODEL}/requests/{request_id}"
    for _ in range(120):
        st = get(status_url, k)
        if st.get("status") == "COMPLETED":
            break
        if st.get("status") == "FAILED":
            sys.exit(f"generation failed: {st}")
        print(f"  {st.get('status')} ...")
        time.sleep(10)
    else:
        sys.exit("timed out waiting for the job; re-run to resume")

    res = get(result_url, k)
    url = res["video"]["url"]
    print(f"downloading {url}")
    urllib.request.urlretrieve(url, VIDEO)
    JOB_FILE.unlink(missing_ok=True)


def extract() -> None:
    if not VIDEO.exists():
        sys.exit(f"{VIDEO} not found; run without --frames-only first")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.jpg"):
        old.unlink()
    dur = float(
        subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(VIDEO)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    )
    fps = FRAMES / dur
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(VIDEO),
         "-vf", f"fps={fps:.4f},scale={FRAME_WIDTH}:-2",
         "-q:v", "6", "-frames:v", str(FRAMES),
         str(OUT_DIR / "f%03d.jpg")],
        check=True,
    )
    got = sorted(OUT_DIR.glob("*.jpg"))
    total = sum(f.stat().st_size for f in got)
    print(f"{len(got)} frames, {total / 1_048_576:.1f} MB total")
    if total > 8 * 1_048_576:
        print("WARNING: over 8 MB. Lower FRAME_WIDTH or raise -q:v before shipping.")


if __name__ == "__main__":
    if "--frames-only" not in sys.argv:
        generate()
    extract()
