# ENCORE° pendulum — render notes

- `encore-pendulum-animatic-v1.mp4` — first animatic, drawn placeholder figure.
- `encore-pendulum-v2.mp4` — first pass with the real figure (two poses).
- `encore-pendulum-v3.mp4` — 1080×1920, 30fps, 10s seamless loop, no audio. Five figure cutouts in `src/figure/`: sit, wave, stand, hang, jump (jump shows only during a swap).
- Source: `src/pendulum.html` (canvas, `window.show(t)`), pieces in `src/pieces/` (cropped from `encore/assets/pieces`, upscaled ×2).
- Render: `node src/render.cjs <framesdir>` then `ffmpeg -framerate 30 -i <framesdir>/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 17 out.mp4`.
- Live preview: open `src/pendulum.html?play`.
- Timing: one pass = 1.25s, a new piece on every apex (8 pieces), background changes with the hour every second pass.
