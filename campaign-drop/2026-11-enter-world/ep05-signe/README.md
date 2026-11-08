# EP05 · SIGNÉ° (No.17) · רגע חתימה שזוכרים

- `ep05-signe-v1.mp4` — 50s: hook to camera (lip-synced, cards) → board (noir palette, the cream signature line, Le Noir) → entry → piping
  the signature (push to the nib) → generic vitrine with price tags → the signed éclair → the box sealed with the signature, broken to open
  → zoom on «the moment» → business line + question (lip-synced, zoom-ins on «ברורה», «דווקא בך», «הרגע», cards one after another) → CTA.
- Waiting for two stills in `../studio/`: `series-S7-side.webp` (side camera, middle phrase of the business line) and
  `series-S8-sign.webp` (Hagit signs; ink drawn on the card, then the series signature). `python3 src/mux.py config` detects them
  (HAS_S7 / HAS_S8); set the card box with `window.SIGNCARD = {x, y, w, h}` (stage px) once S8 is in.
- Recordings in `voice/` (hook, studio, world, ask-q + shared biz). Script: `brandos/briefs/series-enter-world-2026-11/EP05-signe.md`.

## Build
Same as EP04: `python3 src/mux.py audio` → Wan 2.7 lip-sync → `prep-talk.sh` + `align_talk.py` → `mux.py config` → `render.js` → `mux.py mux`.
