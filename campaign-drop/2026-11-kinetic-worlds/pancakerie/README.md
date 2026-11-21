# PANCAKERIE° · "tempting, but does it sell?" · kinetic reel

- `PANCAKERIE-questions-24s.mp4` — 9:16, 1080×1920, 30fps, H.264, 24.0s, no audio. `cover.jpg` is frame 0.
- `PANCAKERIE-questions-24s-4x5.mp4` — 4:5, 1080×1350, a straight crop of the 9:16 (y 180–1530).

Source `src/reel.html` (reads dishes, builder layers, logo and box from `pancakerie/assets/` by relative path, so render inside the repo checkout).
Render: `node src/render.js src/reel.html 24 PANCAKERIE-questions-24s.mp4`
4:5:    `ffmpeg -i PANCAKERIE-questions-24s.mp4 -vf "crop=1080:1350:0:180,format=yuv420p" -c:v libx264 -crf 18 PANCAKERIE-questions-24s-4x5.mp4`
Timeline: 0–2.9 hook (turning table) · 2.9–7.5 Q1 first sentence · 7.5–12.1 Q2 choose a colour · 12.1–17.1 Q3 the builder ·
17.1–21.1 Q4 the box and the order · 21.1–24 outro + CTA. Every screen opens out of a falling drop of cream.
