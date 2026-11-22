# SIGNÉ° build-a-world — render notes

- `signe-build-v1-9x16.mp4` — 1080×1920, 30fps, 12s, with the sound bed. Not a loop: it ends on the finished world.
- `signe-build-v1-4x5.mp4` — 1080×1350 feed version.
- Source: `src/build.html` (canvas, `window.show(t)`; `?play` for a live preview, `?fmt=45` for 4:5).
- Assets: `src/assets/` — four SIGNÉ photos from `signe/assets` (product, box, bag, storefront), resized.
- Figure: `src/figure/` — the same cutouts as the ENCORE pendulum reel (sit, wave, jump).
- Sound: `src/sound.py` — synthesised snap on every drop, bell when the page turns into the world. No music track.
- Render: `node src/render.cjs <frames> [all] [45]`, `python src/sound.py bed.wav`, then
  `ffmpeg -framerate 30 -i <frames>/%04d.png -i bed.wav -c:v libx264 -pix_fmt yuv420p -crf 17 -c:a aac -shortest out.mp4`.
- Timing: element table `E` in build.html (drag start + 0.7s = drop), signature piped 3.25–4.45s, flood at 9.2s.
