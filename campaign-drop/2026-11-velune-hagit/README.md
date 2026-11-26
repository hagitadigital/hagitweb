# VELUNE° · Hagit presents one whole world — typographic edit (18s, with music; every cut on the 120 BPM beat grid)

- `VELUNE-HAGIT-9x16.mp4` (1080×1920) and `VELUNE-HAGIT-4x5.mp4` (1080×1350, a straight crop: `crop=1080:1350:0:270`).
- The site's own story in order: door, garden, fruit, drop, bottle, one bottle, three hours, coffret. All texts are headings of `velune/index.html`.
- Source takes: the same phone clips as `2026-11-hagit-presents`, kept out of the repo (`src/shots/`, gitignored), plus her chosen closing still.
- `src/prep.py` — cuts her out per `schedule.json` into `src/frames/` (generated) and writes `stats.json`.
- `src/gen.py` — timings, texts, placements → `reel.html`; `node src/render.js 18 test/silent.mp4`, then mux `src/music.mp3` (trimmed by 0.036s, 0.8s fade out).
- World footage is read straight from `velune/assets/` (`porte/d01–d40`, `fruit/a|c|b01–40`, bottles, notes, écrin).
