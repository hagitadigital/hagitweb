# TRAME° — type edit, 1950s salon show (24.6s, studio intro and outro, with music)

- `TRAME-type-edit-9x16.mp4` (1080×1920) and `TRAME-type-edit-4x5.mp4` (1080×1350, studio side panels).
- All footage is from `trame/assets/`: the four runway clips, the atelier film, the sketch/dress pair, the collection stills.
- `src/prep.py` — crops each runway clip around the model and cuts her out, into `src/frames/` (generated, not committed).
- `src/gen.py` — builds `src/reel.html`; all timings and the vintage treatment (fade, gate weave, dust, grain, light leaks) live there.
- `node src/render.js 24.6 out.mp4` renders the picture; `src/music.mp3` is trimmed by 0.474s so a downbeat lands on the first look (7.0s).
