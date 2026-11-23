# ROSÉE° intro reel — render notes

Second world in the "קבלו את ___" series. Same template as `campaign-drop/2026-11-signe-build/src/intro.html` (v5, envelope version).

- `rosee-intro-v1-9x16.mp4` — 1080×1920, 30fps, 15.4s, with the sound bed. `rosee-intro-v1-4x5.mp4` — 1080×1350.
- Source: `src/intro.html` (canvas, `window.show(t)`; `?play` for a live preview, `?fmt=45` for 4:5).
- What changes per world: the colour constants at the top (`NOIR` = world background, `CREAM` = world ink, `GOLD` = accent),
  `LOGO` / `LOGO_STAND` (the letter she stands on), the world background in `bg()`, the flourish in `squiggle()`,
  the `CARDS` list and the designed cards in `makeCards()`, and the files in `src/assets/`.
- Cards: strategy line and palette from `rosee/brand-book.html`; language card = the hour before the name (06:15 · Le Réveil);
  packaging = bag touchpoint; site = phone-size screenshot of `rosee/index.html`; social = mock grid of the world's own photos;
  videos = 40 frames of the falling drop from `rosee/frames-desktop` (every second frame, cropped to 3:4).
- Render: `node src/render.cjs <frames> [all] [45]`, `python src/sound.py bed.wav`, then
  `ffmpeg -framerate 30 -i <frames>/%04d.png -i bed.wav -c:v libx264 -pix_fmt yuv420p -crf 17 -c:a aac -shortest out.mp4`.
