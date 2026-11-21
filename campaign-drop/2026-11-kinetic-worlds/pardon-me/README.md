# PARDON ME° · World 29 · kinetic reel

- `PARDON-ME-29-kinetic-24s.mp4` — 9:16, 1080×1920, 30fps, H.264, 24.0s, no audio. `cover.jpg` is frame 0.
- `PARDON-ME-29-kinetic-24s-4x5.mp4` — 4:5, 1080×1350. A straight crop of the 9:16 (y 180–1530): every text sits inside
  that band, so the feed version stays full-bleed instead of using the studio side panels.

Source `src/reel.html` (reads images from `pardon-me/assets/` by relative path, so render inside the repo checkout).
Render: `node src/render.js src/reel.html 24 PARDON-ME-29-kinetic-24s.mp4`
4:5:    `ffmpeg -i PARDON-ME-29-kinetic-24s.mp4 -vf "crop=1080:1350:0:180,format=yuv420p" -c:v libx264 -crf 18 PARDON-ME-29-kinetic-24s-4x5.mp4`
Timeline: 0–2.6 hook · 2.6–5.2 decision · 5.2–10.5 code 01 window (+03 print) · 10.5–13.3 code 02 sleeve ·
13.3–18.2 code 04 names · 18.2–21.2 touchpoints · 21.2–24 outro + CTA.
