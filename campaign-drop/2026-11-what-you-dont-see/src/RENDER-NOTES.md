# Render notes: "what you don't see in the picture" reels

Source only. The talking-head take, its extracted frames and the rendered MP4s are not in the repo.

## Files

- `rosee.html` (rendered as `reel4.html`), `chasen.html` (`reel-chasen.html`): the full 42 s reel, speaker in a brand frame.
- `pardon-me-v1.html` (`pm.html`), `pardon-me-v2.html` (`pm2.html`): the 18 s cut. v1: speaker in the large oval on the prints. v2: brand full screen, speaker in the small oval.
- `render*.cjs`: Playwright frame renderers. Each page exposes `window.seek(t)`; the renderer screenshots `#st` at 30 fps. The file names inside them are the working names in brackets above.
- `rec-pm.cjs`: records the PARDON ME site (window opening on scroll, sleeve tear) at 1080x1920.
- `matte.py`: cuts the speaker out of the take frames (rembg, `u2net_human_seg`).
- `music.py`: generates the ambient bed (`music.py out.wav seconds`).

## Inputs each page expects next to it

- `me/%04d.jpg`: the take at 30 fps, 720x1280 (`ffmpeg -i take.mp4 -q:v 3 me/%04d.jpg`).
- `pm/me/%04d.webp`: cut-outs from `matte.py` (PARDON ME only).
- `fonts/local.css`: Heebo, Cormorant Garamond, Plus Jakarta Sans, Assistant, Frank Ruhl Libre, Bodoni Moda.
- Brand stills and frame sequences, cut from the world folders in this repo (`rosee/`, `chasen/`, `pardon-me/`).

## Timing

All times are in take seconds, taken from one specific take. A new take needs new numbers in `CAP`, `HD` and the per-beat constants.

- Full reel: reel time = take time - 0.8.
- Short cut: part A = take 0.95-9.25, part B = take 32.75-39.55, joined at reel 8.3.

## Layout rules used

- Captions sit above the bottom 420 px, the top plate below 230 px (Instagram UI).
- Audio: voice normalised to -15 LUFS, bed at 0.20 gain rising to 0.55 on the closing screen, final -3 dB.
