# EP01 · ELVÉA° · «נכנסים לעולם מותג»

- `ep01-elvea-v2.mp4` — 39.4s, 9:16, Hagit's Cartesia VO + piano/strings bed (ducked) + paper whoosh on the entry and exit. v2: ELVÉA° wordmark on the after-tiles is erased on «עוד לפני שרואים את השם»; CTA button «אבחון פער המותג · חינם» in the signature.
  Studio stills are static (Ken Burns only); lip-sync/animation of S1 and S6 is the next step.
- Script, timings and copy: `brandos/briefs/series-enter-world-2026-11/EP01-elvea.md`.

## Render
```
node src/render.js src/ep01.html src/_build-silent.mp4      # frames → silent mp4 (needs ../../../../elvea/assets)
bash src/mux.sh src/_build-silent.mp4 ep01-elvea-v2.mp4      # VO (shifted), music, whooshes
node src/render.js src/ep01.html <prefix> 0,300,600          # QA stills
```
- Retime in the TIMING block at the top of `src/ep01.html`. The VO is shifted in `src/mux.sh` (`VO_SHIFT`): +0.6s after 11.9s (room for the entry), +1.4s after 28.76s (exit).
- Board: corner quads per still in `../studio/quads.json` (also inlined as `QUADS`), the hands that sit over the board are `../studio/fg/*.png` (`python3 src/make_fg.py`).
- Next episode: copy this folder, change the board content (palette, code SVG, product), the world scenes and `CAPS`.
