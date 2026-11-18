# Landing-page film with the digital twin

`landing-twin-v4-music.mp4` — 1080×1920, 30fps, 18.2s: v3 with the music bed (`audio/bed-piano-strings-v1.mp3`, from the October explainer reel), no narration yet.
`landing-twin-v5-vo.mp4` — v3 with Hagit's Cartesia narration (`audio/narration-cartesia.wav`, one file, cut at its pauses into eight phrases and placed on the captions) over the music bed, ducked under the voice.
`landing-twin-v3.mp4` — the same film, silent. The page on the screens is the ORÉVA° concept landing page
(`../concept-page-oreva/index.html`; its media are the files of `oreva/assets/`, copied to `a/` next to the page).
v1 used a still for the opening shot, v2 the real clip, both with VELUNE° on screen.

Rebuild (from `src/`, the concept page served at `localhost:8766/preview.html` — the page wrapped in a plain html/body):
1. `ffmpeg -i front-clip.mp4 clip/f%04d.png` · `ffmpeg -i back-clip.mp4 clipB/f%04d.png`
2. `node cap2.js oB 138 30 "0:0,40:0,137:1750"` · `node cap2.js oC 145 24 "0:6520,60:7330,85:7330,144:8080"` ·
   `MOBILE=1 node cap2.js oM 180 30 "0:2934,125:4043,152:4650,179:4650"` (frames:scrollY keyframes; CSS animations and videos follow frame time)
3. `python3 comp.py clip oC outC` — tracks the laptop screen in the front clip and composites the page.
4. `python3 base.py` — builds the three scenes into `base/`.
5. `node render.js landing-twin-v3.mp4` — text overlays and end card from `film.html`.

Screen corners are hard-coded for these two shots (`comp.py` C0, `base.py` C).
