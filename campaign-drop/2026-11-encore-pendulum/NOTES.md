# ENCORE° pendulum — render notes

- `encore-pendulum-v4-9x16.mp4` — 1080×1920, 30fps, 10s seamless loop, with the sound bed.
- `encore-pendulum-v4-4x5.mp4` — 1080×1350 feed version of the same loop.
- `encore-pendulum-v3.mp4` — previous pass (low-res pieces, no audio). v1 and v2 are in git history.
- Source: `src/pendulum.html` (canvas, `window.show(t)`; `?play` for a live preview, `?fmt=45` for 4:5).
- Pieces: `src/pieces/` — the eight ENCORE pieces re-rendered at high resolution from `encore/assets/pieces`, background removed, 900px on the long side.
- Figure: `src/figure/` — five cutouts: sit, wave, stand, hang, jump (jump shows only during a swap).
- Sound: `src/sound.py` — synthesised tick on every pass, bell on every swap, lower bell on every hour change. No music track.
- Render: `node src/render.cjs <frames> [all] [45]`, `python src/sound.py bed.wav`, then
  `ffmpeg -framerate 30 -i <frames>/%04d.png -i bed.wav -c:v libx264 -pix_fmt yuv420p -crf 17 -c:a aac -shortest out.mp4`.
- Timing: one pass = 1.25s, a new piece on every apex (8 pieces), background changes with the hour every second pass.
