# ONE OF ONE° — 30-second film (source)

Output: `images/home-worlds/live/films/one-of-one.mp4` + `.jpg` (720×1280, 30 fps, 30.0 s, no audio).

- `clips/` — six Kling image-to-video clips (Kling 3.0 Turbo, 5 s, 1080p), audio stripped.
- `frames/` — the 9:16 opening frames the clips were generated from (rendered from the world's own assets).
- `film.html` — the code-made scenes (mood swap, box end card) and the text overlays.
- `render-frames.js`, `render-overlays.js` — Playwright scripts that render `film.html` to frames and transparent overlays.
- `build.sh` — trims, overlays and concatenates everything with ffmpeg.

To rebuild: serve the repo root on localhost:8765, run the two render scripts with a work folder as their argument, copy `clips/*.mp4` into that folder, then run `build.sh` there.
