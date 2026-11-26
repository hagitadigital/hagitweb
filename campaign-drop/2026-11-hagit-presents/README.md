# WORLDS · Hagit presents the brand worlds — typographic edit (16.5s, with music; every cut on the 120 BPM beat grid)

- `WORLDS-HAGIT-9x16.mp4` (1080×1920) and `WORLDS-HAGIT-4x5.mp4` (1080×1350, a straight crop: `crop=1080:1350:0:270`).
- Source takes: Hagit's own phone clips (1080×1920, 30fps), kept out of the repo (`src/shots/`, gitignored).
- `src/gen.py` — timings, texts, placements; writes `schedule.json` and `reel.html`.
- `src/prep.py` — cuts her out of every scheduled frame (rembg) into `src/frames/` (generated) and writes `stats.json`:
  head position per shot, and the open palm per frame for the two shots where the product sits on her hand (MIEL°, ORÉVA°).
- `python3 gen.py && python3 prep.py && python3 gen.py && node render.js 16.5 test/silent.mp4`, then mux `src/music.mp3` (trimmed by 0.036s, 0.8s fade out).
- Product images, prints and world cards are read straight from the worlds' own folders and `images/home-worlds/`.
- Unused takes: 111657 (wink), 111947 (hands in pockets), 112003 (empty wall).

## v2 — text in front, her small inside the world, the worlds' own films, products in orbit

- `WORLDS-HAGIT-v2-9x16.mp4` and `WORLDS-HAGIT-v2-4x5.mp4`: same takes, texts, music and beat grid as v1.
- `src/gen2.py` → `reel2.html`; `REEL=reel2.html node render.js 16.5 test/silent2.mp4`, then mux the music as in v1.
- Needs two generated frame folders from the worlds' films (not committed):
  `ffmpeg -i chasen/film/03-verre-m.mp4 -q:v 2 src/frames/w_chasen/b_%03d.jpg`
  `ffmpeg -i encore/assets/hero/float-loop.mp4 -vf "fps=24,scale=-2:1350" -q:v 2 src/frames/w_encore/b_%03d.jpg`
  The VELUNE° door is read straight from `velune/assets/porte/d01–d40.webp`.
- Orbits are flat images on a tilted ring (no 3D models): MIEL° bag, box, seal and toppings around the cake on her palm;
  the ORÉVA° kit around her, passing behind and in front. Reference recording stays out of the repo (`src/ref/`).
- The closing arch in v2 shows her real frame, not a cut-out: `ffmpeg -ss 2.6 -i src/shots/111724.mp4 -frames:v 60 -q:v 2 src/frames/ctaraw/b_%03d.jpg` (frame 040).
- MIEL° and ORÉVA° end on a camera push-in to the product on her palm (`zoom=` in `gen2.py`).
