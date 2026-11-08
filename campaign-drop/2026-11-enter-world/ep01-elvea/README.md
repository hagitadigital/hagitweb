# EP01 · ELVÉA° · «נכנסים לעולם מותג»

- `ep01-elvea-v4.mp4` — 39.4s, 9:16, Hagit's Cartesia VO + piano/strings bed (ducked) + paper whoosh on the entry and exit. v2: ELVÉA° wordmark on the after-tiles is erased on «עוד לפני שרואים את השם»; CTA button «אבחון פער המותג · חינם» in the signature.
  v4: S1–S4 and S6 lip-synced to the VO with soft natural motion — Wan 2.7 on Higgsfield (start_image = the still,
  audio_references = that shot's slice of the VO, 1080p, 12.5 credits/clip). It is audio-driven: its output carries the VO and the mouth follows it.
  Rejected: Seedance 2.5 (audio is only a loose reference, mouth not synced — v3), Intone (re-stages the shot).
  Raw clips in `talk/`. The board stays the still: the clip is blended in only right of the `mask` x-range in the TALK block.
- Script, timings and copy: `brandos/briefs/series-enter-world-2026-11/EP01-elvea.md`.

## Render
```
bash src/prep-talk.sh ../talk/s1-wan.mp4 S1           # each talking clip → 30fps frames (S1 S2 S3 S4 S6)
python3 src/align_talk.py ../studio/series-S1-open.webp --dir src/_build/talk-S1   # align frames to the still (needs opencv)
node src/render.js src/ep01.html src/_build-silent.mp4      # frames → silent mp4 (needs ../../../../elvea/assets)
bash src/mux.sh src/_build-silent.mp4 ep01-elvea-v4.mp4      # VO (shifted), music, whooshes
node src/render.js src/ep01.html <prefix> 0,300,600          # QA stills
```
- Retime in the TIMING block at the top of `src/ep01.html`. The VO is shifted in `src/mux.sh` (`VO_SHIFT`): +0.6s after 11.9s (room for the entry), +1.4s after 28.76s (exit).
- Board: corner quads per still in `../studio/quads.json` (also inlined as `QUADS`), the hands that sit over the board are `../studio/fg/*.png` (`python3 src/make_fg.py`).
- Next episode: copy this folder, change the board content (palette, code SVG, product), the world scenes and `CAPS`.
