# ORÉVA° · World 24 · "four questions to your site" · kinetic reel

- `OREVA-24-questions-24s.mp4` — 9:16, 1080×1920, 30fps, H.264, 24.0s, no audio. `cover.jpg` is frame 0.
- `OREVA-24-questions-24s-4x5.mp4` — 4:5, 1080×1350, a straight crop of the 9:16 (y 180–1530).

Source `src/reel.html` (v2, richer motion; the first flat cut is `src/reel-v1-flat.html`).
`src/seq/` holds three short image sequences cut from the site's own loops (hands, treatment, diagnosis). `src/oreva-mobile.jpg` is the real first screen of `oreva/index.html` at 390×844 @3x,
captured by `node src/shot-mobile.js` (re-run it if the site's hero changes; the lit regions in reel.html follow its layout).
Render: `node src/render.js src/reel.html 24 OREVA-24-questions-24s.mp4`
4:5:    `ffmpeg -i OREVA-24-questions-24s.mp4 -vf "crop=1080:1350:0:180,format=yuv420p" -c:v libx264 -crf 18 OREVA-24-questions-24s-4x5.mp4`
Timeline: 0–3 hook · 3–7.5 Q1 first sentence · 7.5–12.1 Q2 reason · 12.1–16.1 Q3 next step · 16.1–21.1 Q4 phone · 21.1–24 outro + CTA.
