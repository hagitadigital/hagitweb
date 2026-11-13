# Beauty worlds mini reel · render notes
- `mini/BEAUTY-WORLDS-MINI-9x16.mp4` 1080x1920, 15.5s, 30fps; `mini/BEAUTY-WORLDS-MINI-4x5.mp4` 1080x1350. No audio.
- Worlds: ROSÉE° (No.15), VELUNE° (No.25), SOUFFLÉ° (No.11). Same character as the dessert mini reel.
- Source: `mini/src/gen.py` writes `mini/src/reel.html`; render with the brandos-brand-world-reel skill's `render.js src/reel.html 15.5 <out.mp4>`.
- Clip frames are not in the repo. Rebuild them from `character/clips/*.mp4`:
  - `ffmpeg -i ../character/clips/walk.mp4 -vf colorchannelmixer=rr=1.0082:gg=1.0087:bb=1.0167 -q:v 2 src/assets/walk/f%03d.jpg`
  - `ffmpeg -i ../character/clips/rosee.mp4 -q:v 2 src/assets/rosee/f%03d.jpg` (same for `velune`)
- `character/`: scene stills (Higgsfield, gpt_image_2_6) and clips (seedance_2_5, 720p, 4s).
