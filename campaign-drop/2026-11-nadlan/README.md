# NADLAN · «המספר נשאר» (18s, with music) — real-estate ad for /sites/nadlan/

- `NADLAN-14-9x16.mp4` (1080×1920) and `NADLAN-14-4x5.mp4` (1080×1350).
- Opening: 2s of Hagit's laptop take with the RUE° site on the screen (needs `../2026-11-hagit-worlds/src/frames/take`, generated from her take, which stays out of the repo).
- Then number 14 from the same camera: `rue/assets/01-old.webp` → `sites/nadlan/fence.webp` → `rue/assets/03-new.webp`, sky removed so the 14 sits behind the building.
- Three "doors" use the section screenshots in `sites/nadlan/`; the trust line sits on `rue/assets/16-flagship.webp`.
- `src/capture_stairs.js` records the site's own stairs animation for slide 01; the fan in the trust slide is the site's fan, ported into `gen.py`.
- `src/prep.py` (frames), `src/gen.py` (timings, texts → `reel.html`), `node src/render.js 18 out.mp4`. All cuts are on a 120 BPM grid; `src/music.mp3` is trimmed by 0.036s.
