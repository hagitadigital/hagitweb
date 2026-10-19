# Explainer · Hagit breaks down the hidden-logo ads

- `ELVEA-explainer-v3-animated.mp4` — ELVÉA° "הקו", 31s, 9:16, silent (captions carry it; add music in the app, or lay Hagit's voice under it later).
  Hagit's stills animated in Kling 3.0 Turbo (`clips/`, 5s each, gentle motion only); `bash src/prep-clips.sh` cuts them into frames,
  `src/elvea.html?stills` falls back to the still images.
  Source: `src/elvea.html` (retime in its SCENES / CAPS / MARKS block), render: `node src/render.js src/elvea.html out.mp4`.
- `stills/elvea-h1..h5` — Hagit's own generated stills (hook, drawing, wall, box, end); `elvea-h0-style-ref` is the look they follow.
- `frames/` + `src/mock.html` — the first concept frames (ELVÉA° and the dessert worlds) over the placeholder portrait.
- `src/_build/ad/` (not committed) — frames cut from the two ads: `ffmpeg -ss <t> -i <ad.mp4> -frames:v 1 -q:v 3 src/_build/ad/elvea-<t>.jpg`
  (ELVÉA times used: 0.3, 4.6, 6.8, 9.0, 13.2, 17.8, 20.0, 25.5).
