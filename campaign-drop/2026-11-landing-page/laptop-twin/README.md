# Landing-page film with the digital twin · v1 draft

`landing-twin-v2.mp4` (opening shot is the real clip; v1 used a still) — 1080×1920, 30fps, 18.2s, no audio yet.

Rebuild (from `src/`, site served at `localhost:8765` from the repo root):
1. `ffmpeg -i front-clip.mp4 clip/f%04d.png` · `ffmpeg -i back-clip.mp4 clipB/f%04d.png`
2. `node capscroll.js scrB 1440 900 138 0 2750 30 10` · `node capscroll.js scrC 1440 900 145 7300 8650 10 30` · `MOBILE=1 node capscroll.js scrM 390 693 180 700 4250 6 30`
3. `python3 comp.py clip scrC outC` — tracks the laptop screen in the front clip and composites the page.
4. `python3 base.py` — builds the three scenes into `base/`.
5. `node render.js landing-twin-v1.mp4` — text overlays and end card from `film.html`.

Screen corners are hard-coded for these two shots (`comp.py` C0, `base.py` C).
