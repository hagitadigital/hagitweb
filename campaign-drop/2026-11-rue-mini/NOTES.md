# RUE° mini ad · render notes
- `RUE-MINI-9x16.mp4` 1080x1920, 15.5s, 30fps; `RUE-MINI-4x5.mp4` 1080x1350 (reel whole in the centre, cream side panels). No audio.
- First cut. Built from the character's existing cut-outs (`walk.webp`, `sit.webp`, from `2026-11-dessert-worlds/character/` on branch `claude/tender-cannon-lf0opi`) composited over RUE°'s own renders. No newly generated character scenes: Higgsfield image generation was failing on 2026-11-16 (every job failed and was refunded, with and without references).
- Scenes: hook in the series look (her real walking clip on the copper line, cream ground, with the site's hero lighting up under the line) · the street of addresses · the plate "14" with the building changing behind it (she sits on it) · the fan of rooms · CTA.
- Source: `src/gen.py` writes `src/reel.html`; render with the brandos-brand-world-reel skill's `scripts/render.js src/reel.html 15.5 <out.mp4>`.
- 4:5: `src/frame-4x5.png` over a `#F2EBDC` ground (ffmpeg scale 760:1350, overlay 160:0).
- Clip frames are not in the repo. Rebuild them from `character/clips/walk.mp4`:
  `ffmpeg -i character/clips/walk.mp4 -vf "colorchannelmixer=rr=1.0082:gg=1.0087:bb=1.0167,crop=720:800:0:0,scale=1080:1200:flags=lanczos" -q:v 2 src/assets/walk/f%03d.jpg`
- She walks only in the hook (the clip). In the street and plate scenes she sits (cut-out); the fan scene has no figure.
