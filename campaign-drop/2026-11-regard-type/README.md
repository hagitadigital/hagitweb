# REGARD° — type edit (style test, 15s, 9:16)

Typography-led edit on the five portrait clips from `regard/assets/portraits/`: big words sit behind the head.

- `REGARD-type-edit-9x16.mp4` — 1080×1920, 30fps.
- `src/prep.py` — cuts the figure out of every frame (rembg, isnet-general-use) into `src/frames/` (generated, not committed).
- `src/reel.html` — the timeline; shots and timings are in the `SHOTS` table.
- `src/render.js` — `node render.js 15 ../REGARD-type-edit-9x16.mp4`, or stills: `node render.js 15 test/r 0,95,300`.

Source clips are 834×1112, shown at 1.2–1.9×.
