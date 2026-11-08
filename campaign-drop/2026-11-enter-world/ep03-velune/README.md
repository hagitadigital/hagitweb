# EP03 · VELUNE° (No.25) · ההבטחה, והדלת שחוזרת

Same arc as EP02. The entry is the world's own door: the code panel shows the closed door, it opens (velune/assets/porte d01–d40)
and we walk into the garden (e01–e40). Proof: the arch traced in gold on the door, the box (which then opens) and the boutique;
insight: the three arches alone.

- `ep03-velune-v4.mp4` — 51s, world cards presented one after another beside Hagit (caption CSS fixed in v4) in the to-camera parts (`src/mode.js`: orbit | seq, `../shared/cards.js`). v2 (v2: «ולמקום נכנסים דרך דלת» cut from world.wav at 3.40–5.86; the full take is voice/world-take.wav): hook to camera (lip-synced) → board → door → world → business line + question (lip-synced) → CTA.
- Recordings are separate files in `voice/`: hook, studio, world, ask-q (+ `biz.wav` from `../shared/`). Sentence times inside each file come from its pauses (`src/align_text.py` + `src/script-*.txt`).
- Script, copy: `brandos/briefs/series-enter-world-2026-11/EP03-velune.md`.

## Build
```
bash src/prep.sh                         # door sequence → src/_build/door
python3 src/mux.py audio                 # voice/_hook.mp3, voice/_ask.mp3 → lip-sync on S6 with Wan 2.7 → talk/hook-wan.mp4, talk/ask-wan.mp4
bash src/prep-talk.sh ../talk/hook-wan.mp4 hook && python3 src/align_talk.py ../studio/series-S6-ask.webp --dir src/_build/talk-hook
bash src/prep-talk.sh ../talk/ask-wan.mp4 ask && python3 src/align_talk.py ../studio/series-S6-ask.webp --dir src/_build/talk-ask
python3 src/mux.py config && node src/render.js src/ep03.html src/_build-silent.mp4 && python3 src/mux.py mux src/_build-silent.mp4 ep03-velune-v1.mp4
```
