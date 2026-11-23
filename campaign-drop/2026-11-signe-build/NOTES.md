# SIGNÉ° — render notes

## v5: intro reel, envelope version (current)
- `signe-intro-v5-envelope-9x16.mp4` — 1080×1920, 30fps, 15.4s, with the sound bed. `signe-intro-v5-envelope-4x5.mp4` — 1080×1350.
- `signe-intro-v4-*.mp4` — the previous version: same intro and ring, carousel of six things from the world instead of the envelope.
- Source: `src/intro.html`. Beats (table `B`): "היי" 0s, "אני חגית" 1.0s, "בונה עולמות מותג" 2.1s, "קבלו את SIGNÉ°" 3.6s,
  carousel 5.0s (seven cards, 1.0s each), ring 12.0s.
- Carousel cards (`CARDS`): strategy, language, colours, packaging, site, social, videos. Strategy, colours, site and social are
  drawn in `makeCards()`; the strategy line and the colours come from `signe/brand-book.html`; the site card is a phone-size
  screenshot of `signe/index.html`; the social card is a mock grid of the world's own photos; videos plays the pour frame sequence.
- The figure rests on the exact top of one letter per word (`glyph()`); two jumps in total.
- Render: `node src/render-intro.cjs <frames> [all] [45]`, `python src/sound-intro.py bed.wav`, then mux as below.

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
