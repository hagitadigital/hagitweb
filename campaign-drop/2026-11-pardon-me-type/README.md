# PARDON ME° — type edit (22s, 9:16, studio intro and outro)

Typography-led edit with an AI presenter: big collection words sit behind her head, backdrop colour per collection.

- `PARDON-ME-type-edit-9x16.mp4` — 1080×1920, 30fps.
- `src/base/a.png` — the presenter still all shots start from (b, c: the options not chosen).
- `src/clips/01–05` — five 5s shots, Kling 3.0 pro via Higgsfield, 1076×1924, plain cream backdrop.
- `src/prep.py` then `src/despill.py` — cut the figure out of every frame into `src/frames/` (generated, not committed).
  The product shot reads `frames/reveal/b_###.jpg`: `ffmpeg -i pardon-me/assets/film-reveal.mp4 -q:v 2 frames/reveal/b_%03d.jpg`.
- `src/reel.html` — the timeline (`SHOTS` table); `node src/render.js 22 PARDON-ME-type-edit-9x16.mp4`.
