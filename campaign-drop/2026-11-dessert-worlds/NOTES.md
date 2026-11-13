# Dessert worlds reel · render notes
- `DESSERT-WORLDS-9x16.mp4` 1080x1920, 33s, 30fps. `DESSERT-WORLDS-4x5.mp4` 1080x1350 (reel whole in the centre, cream side panels).
- Source: `src/gen.py` writes `src/reel.html`; render with the brandos-brand-world-reel skill's `scripts/render.js src/reel.html 33 <out.mp4>`.
- 4:5: `src/frame-4x5.png` over a `#F2EBDC` ground (ffmpeg scale 760:1350, overlay 160:0).
- No audio track.
