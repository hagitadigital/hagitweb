# Dessert worlds reel · render notes
- `DESSERT-WORLDS-9x16.mp4` 1080x1920, 22.5s, 30fps. `DESSERT-WORLDS-4x5.mp4` 1080x1350 (reel whole in the centre, cream side panels).
- Source: `src/gen.py` writes `src/reel.html`; render with the brandos-brand-world-reel skill's `scripts/render.js src/reel.html 22.5 <out.mp4>`.
- 4:5: `src/frame-4x5.png` over a `#F2EBDC` ground (ffmpeg scale 760:1350, overlay 160:0).
- No audio track.

## Mini reel (character)
- `mini/DESSERT-WORLDS-MINI-9x16.mp4` 1080x1920, 15.5s; `mini/DESSERT-WORLDS-MINI-4x5.mp4` 1080x1350. No audio.
- Source: `mini/src/gen.py` writes `mini/src/reel.html`; render with the skill's `render.js src/reel.html 15.5 <out.mp4>`.
- `character/`: character sheet, three scene stills and two cut-outs, generated with Higgsfield (gpt_image_2_6) from the sheet plus the worlds' own product images as references.
