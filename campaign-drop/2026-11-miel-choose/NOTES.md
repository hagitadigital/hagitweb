# MIEL · "same product, same price" · render notes
- `MIEL-CHOOSE-4x5.mp4` 1080x1350 (native 4:5, not a framed reel) and `MIEL-CHOOSE-9x16.mp4` 1080x1920. 17s, 30fps, no audio.
- Source: `src/gen.py` writes `src/reel-4x5.html` and `src/reel-9x16.html`.
  Render with the brandos-brand-world-reel skill: `REEL_H=1350 node render.js src/reel-4x5.html 17 <out>` and `node render.js src/reel-9x16.html 17 <out>`.
- `character/`: three scene stills generated with Higgsfield (gpt_image_2_6) from the character sheet and MIEL's own vitrine and bag images. The vitrine and bag scenes are 720p clips (seedance_2_5, 4s) in `character/clips/`; their frames are not in the repo: `ffmpeg -i character/clips/<name>.mp4 -q:v 2 src/assets/<name>/f%03d.jpg`.
- The comparison card is a generic no-name product; price tags and the "ככה משווים" tag are drawn in CSS.
- `source/drag.mp4` and `source/bags.mp4` are cut from the existing MIEL film (inner 9:16 reel, sped up); frames: `ffmpeg -i source/<name>.mp4 -q:v 2 src/assets/<name>/f%03d.jpg`.
