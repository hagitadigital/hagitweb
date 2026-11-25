# SITES · Hagit at the laptop — typographic edit (16.8s, no music yet)

- `SITES-HAGIT-9x16.mp4` (1080×1920) and `SITES-HAGIT-4x5.mp4` (1080×1350).
- Source take: Hagit's own 16s clip (720×1280, 24fps), kept out of the repo (`src/take.mp4`, gitignored).
- `src/gen.py` — timings, texts, `schedule.json` and `reel.html`.
- `src/screen.py` + `src/prep.py` — track the laptop's white screen per frame, lay the campaign's site recordings
  (`sites/a/oreva|mirvach|rue.mp4`) onto it under her fingers, and cut her out for the words behind her. Writes `src/frames/` (generated).
- `node src/render.js 16.8 SITES-HAGIT-9x16.mp4`.
