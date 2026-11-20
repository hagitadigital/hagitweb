# Sites reel · render notes

`sites-reel-9x16.mp4` — 1080×1920, 30 fps, 23.6 s, H.264, no audio.

## Source

- `src/reel.html` — the whole timeline. `renderAt(t)` sets every element from `t` alone.
  Open with `?play` to watch it loop in a browser.
- `src/quads.js` — the four corners of the laptop screen for clip frames 156–266 (24 fps),
  tracked from the white screen and smoothed. The site is pinned to them with a homography.
- `src/render.js` — captures PNG frames with Playwright.
- `src/fonts/` — Heebo, Cormorant Garamond, Plus Jakarta Sans (local copies, so the capture needs no network).

## Inputs (not in the repo)

A sequence folder with four subfolders of `%04d.jpg` frames:

- `hf/` — the Higgsfield clip (job `2b6977d1-b3eb-4ebe-8df4-270ad059ff08`, 1080p, 12.4 s), all frames at 24 fps.
- `oreva/`, `mirvach/`, `rue/` — `sites/a/<name>.mp4` from this repo, all frames at 30 fps.

```bash
ffmpeg -i hf.mp4 -q:v 2 seq/hf/%04d.jpg
```

```bash
for k in oreva mirvach rue; do ffmpeg -i sites/a/$k.mp4 -q:v 2 seq/$k/%04d.jpg; done
```

## Render

```bash
node src/render.js seq out
```

```bash
ffmpeg -framerate 30 -i out/%05d.png -c:v libx264 -preset slow -crf 15 -pix_fmt yuv420p -movflags +faststart sites-reel-9x16.mp4
```

## Timeline

| Seconds | What plays |
|---|---|
| 0.0–2.1 | Hook frame: clip in a window, ORÉVA° page card as proof |
| 2.1–6.5 | Clip full frame: typing, then the turn |
| 6.5–9.0 | ORÉVA° page on the laptop screen, three answers light up |
| 9.0–9.6 | Push in through the screen |
| 9.6–18.6 | Inside the pages: ORÉVA°, מרווח, RUE° (3 s each, two moments per page) |
| 18.6–20.6 | Pull out, RUE° on the screen |
| 20.6–23.6 | Clip frozen on its last clean frame, the screen becomes the button |

Ground colour sampled in the encoded frame 0: `rgb(242,233,218)` against cream `#F2EBDC` — 2 per channel, inside the limit.
