# WORLDS · Hagit presents the brand worlds — typographic edit (16.5s, with music; every cut on the 120 BPM beat grid)

- `WORLDS-HAGIT-9x16.mp4` (1080×1920) and `WORLDS-HAGIT-4x5.mp4` (1080×1350, a straight crop: `crop=1080:1350:0:270`).
- Source takes: Hagit's own phone clips (1080×1920, 30fps), kept out of the repo (`src/shots/`, gitignored).
- `src/gen.py` — timings, texts, placements; writes `schedule.json` and `reel.html`.
- `src/prep.py` — cuts her out of every scheduled frame (rembg) into `src/frames/` (generated) and writes `stats.json`:
  head position per shot, and the open palm per frame for the two shots where the product sits on her hand (MIEL°, ORÉVA°).
- `python3 gen.py && python3 prep.py && python3 gen.py && node render.js 16.5 test/silent.mp4`, then mux `src/music.mp3` (trimmed by 0.036s, 0.8s fade out).
- Product images, prints and world cards are read straight from the worlds' own folders and `images/home-worlds/`.
- Unused takes: 111657 (wink), 111947 (hands in pockets), 112003 (empty wall).
