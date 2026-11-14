# MIEL · "same product, same price" · render notes
- `MIEL-CHOOSE-9x16.mp4` 1080x1920; `MIEL-CHOOSE-4x5.mp4` 1080x1350 is the 9:16 reel whole between the studio side panels with the name (`src/frame-4x5.png` over `#F2EBDC`); `MIEL-CHOOSE-4x5-full.mp4` is a full-bleed 4:5 without the panels. 17.1s, 30fps, no audio.
- Source: `src/gen.py` writes `src/reel-4x5.html` and `src/reel-9x16.html`.
  Render with the brandos-brand-world-reel skill: `REEL_H=1350 node render.js src/reel-4x5.html 17.1 <out>` and `node render.js src/reel-9x16.html 17.1 <out>`.
- `character/`: three scene stills generated with Higgsfield (gpt_image_2_6) from the character sheet and MIEL's own vitrine and bag images. The vitrine and bag scenes are 720p clips (seedance_2_5, 4s) in `character/clips/`; their frames are not in the repo: `ffmpeg -i character/clips/<name>.mp4 -q:v 2 src/assets/<name>/f%03d.jpg`.
- The comparison card is a generic no-name product; price tags and the "ככה משווים" tag are drawn in CSS.
- `source/drag.mp4` and `source/bags.mp4` are cut from the existing MIEL film (inner 9:16 reel, sped up); frames: `ffmpeg -i source/<name>.mp4 -q:v 2 src/assets/<name>/f%03d.jpg`.
- `*-music.mp4`: the same renders with `source/music-cut.m4a`, a 17.1s cut of the Suno track "Patisserie Perfection" starting at 13.03s (116 BPM); scene cuts sit on its beats and the CTA lands on the lift at 27.0s of the track.
