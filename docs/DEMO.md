# Demo: how `demo.gif` and `demo.mp4` were made (and how to re-record)

GitHub renders GIFs everywhere but does not autoplay all MP4s in every view.
This repo ships both from the same verified source so the README works in both places.

## What is included

- `docs/demo.gif` — plays inline in README and on the Pages site. Under 1 MB target.
- `docs/demo.mp4` — higher quality, with player controls on the Pages site.
- `docs/screenshot.png` — full-page capture of `docs/preview.html` via automated browser.
- `docs/screenshot-full.png` — viewport capture for the README hero.

## How they were generated (reproducible)

1. `python scripts/run_all.py` produces `results/e0*.json` from the live API.
2. `python docs/make_demo.py` reads those JSON files and renders frames with matplotlib/Pillow
   (no hand-typed numbers — frames come from `results/`).
3. Frames are stitched to GIF (Pillow) and MP4 (imageio-ffmpeg if available, else GIF only).
4. Screenshots are captured with an automated Chromium visit to `file://.../docs/preview.html`.

## Re-record your own terminal session (optional, best quality)

For a real typing demo, use terminal capture:

```bash
# asciinema: lightweight terminal recording
pip install asciinema
asciinema rec docs/terminal.cast
# ... run: pytest -v tests/ && python scripts/run_all.py
# exit, then:
# agg docs/terminal.cast docs/demo.gif   (install agg + gifski)
```

Keep the GIF under 1 MB and under 30 seconds. Place the camera above the fold in the README:
hero image first, then quick start, then details.
