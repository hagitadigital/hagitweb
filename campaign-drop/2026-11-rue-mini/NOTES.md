# RUE° mini ad · render notes
- `RUE-MINI-9x16.mp4` 1080x1920, 15.5s, 30fps; `RUE-MINI-4x5.mp4` 1080x1350 (reel whole in the centre, cream side panels). No audio.
- First cut. Built from the character's existing cut-outs (`walk.webp`, `sit.webp`, from `2026-11-dessert-worlds/character/` on branch `claude/tender-cannon-lf0opi`) composited over RUE°'s own renders. No newly generated character scenes: Higgsfield image generation was failing on 2026-11-16 (every job failed and was refunded, with and without references).
- Scenes: hook on the site's hero lighting up (she walks the copper line) · the street of addresses · the plate "14" with the building changing behind it (she sits on it) · the fan of rooms · CTA.
- Source: `src/gen.py` writes `src/reel.html`; render with the brandos-brand-world-reel skill's `scripts/render.js src/reel.html 15.5 <out.mp4>`.
- 4:5: `src/frame-4x5.png` over a `#F2EBDC` ground (ffmpeg scale 760:1350, overlay 160:0).
