# ELVÉA · "if we hide the name" with the character · render notes
- `ELVEA-NAME-9x16.mp4` 1080x1920, 15.52s, 30fps; `ELVEA-NAME-4x5.mp4` 1080x1350 is the reel whole between the studio side panels (`src/frame-4x5.png` over `#F2EBDC`).
- `*-music.mp4`: the same renders with `source/music-cut.m4a`, a cut of the Suno track "Patisserie Perfection" starting at 17.17s (116 BPM). Scene cuts sit on its beats and its lift (27.0s of the track) lands on the moment the name is revealed (9.83s).
- Source: `src/gen.py` writes `src/reel.html`; render with the brandos-brand-world-reel skill: `node render.js src/reel.html 15.52 <out.mp4>`.
- `character/`: stills from Higgsfield (gpt_image_2_6); `character/clips/`: Kling kling-video-v4_0 clips, 720p. `reveal.mp4` was generated from a first frame (name covered) and a last frame (name shown, aligned to the first).
- Clip frames are not in the repo: `ffmpeg -i character/clips/<name>.mp4 -q:v 2 src/assets/<name>/f%03d.jpg`. A scene without frames falls back to its still.
