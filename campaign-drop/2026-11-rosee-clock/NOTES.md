# ROSÉE° dawn clock — render notes

- `rosee-clock-v1-9x16.mp4` — 1080×1920, 30fps, 10s seamless loop, with the sound bed.
- `rosee-clock-v1-4x5.mp4` — 1080×1350 feed version of the same loop.
- Source: `src/clock.html` (canvas, `window.show(t)`; `?play` for a live preview, `?fmt=45` for 4:5).
- Products: `src/products/` — the five collection photos from `rosee/collection` (640px), shown as round medallions.
- Figure: `src/figure/` — the same cutouts as the ENCORE pendulum reel (sit, wave, stand, jump).
- Sound: `src/sound.py` — synthesised tick, water drop and bell on every product. No music track.
- Render: `node src/render.cjs <frames> [all] [45]`, `python src/sound.py bed.wav`, then
  `ffmpeg -framerate 30 -i <frames>/%04d.png -i bed.wav -c:v libx264 -pix_fmt yuv420p -crf 17 -c:a aac -shortest out.mp4`.
- Timing: 2s per product: the hand rests 1.1s, then travels 0.9s to the next one.
