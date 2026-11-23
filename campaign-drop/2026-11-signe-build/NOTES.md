# SIGNÉ° — render notes

## v4: intro reel (current). Two jumps in total; the figure rests on the exact top of one letter per word (`glyph()`)
- `signe-intro-v4-9x16.mp4` — 1080×1920, 30fps, 15s, with the sound bed. `signe-intro-v4-4x5.mp4` — 1080×1350.
- Source: `src/intro.html`. Beats (table `B`): "היי" 0s, "אני חגית" 1.0s, "בונה עולמות מותג" 2.1s, "קבלו את SIGNÉ°" 3.6s,
  carousel of six parts 5.0s (1.1s per card; the first card plays the pour frame sequence from the site), ring 11.6s.
- Render: `node src/render-intro.cjs <frames> [all] [45]`, `python src/sound-intro.py bed.wav`, then mux as below.
- Extra assets: `src/assets/pour/` (35 frames from `signe/assets/pour`, cropped to 3:4), `src/assets/bowl.jpg`.

## v1: build-a-world on an editor page

- `signe-build-v1-9x16.mp4` — 1080×1920, 30fps, 12s, with the sound bed. Not a loop: it ends on the finished world.
- `signe-build-v1-4x5.mp4` — 1080×1350 feed version.
- Source: `src/build.html` (canvas, `window.show(t)`; `?play` for a live preview, `?fmt=45` for 4:5).
- Assets: `src/assets/` — four SIGNÉ photos from `signe/assets` (product, box, bag, storefront), resized.
- Figure: `src/figure/` — the same cutouts as the ENCORE pendulum reel (sit, wave, jump).
- Sound: `src/sound.py` — synthesised snap on every drop, bell when the page turns into the world. No music track.
- Render: `node src/render.cjs <frames> [all] [45]`, `python src/sound.py bed.wav`, then
  `ffmpeg -framerate 30 -i <frames>/%04d.png -i bed.wav -c:v libx264 -pix_fmt yuv420p -crf 17 -c:a aac -shortest out.mp4`.
- Timing: element table `E` in build.html (drag start + 0.7s = drop), signature piped 3.25–4.45s, flood at 9.2s.
