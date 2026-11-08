# EP04 · CHASEN° (No.22) · שפה: לא מזמינים, מרכיבים

- `ep04-chasen-v1.mp4` — 54s: hook to camera (lip-synced) → board → entry through the whisk → the film (powder, whisk, pour) with
  «לא מזמינים. / מרכיבים.» as type → generic café menu → the glass answers each verb (flavour swaps, cream layer, the named card)
  → workshop hands → business line + question (lip-synced) → CTA.
- Recordings in `voice/` (hook, studio, world, ask-q + shared biz). Script: `brandos/briefs/series-enter-world-2026-11/EP04-chasen.md`.

## Build
```
bash src/prep.sh                                   # film chapters + workshop hands → src/_build/
python3 src/mux.py audio                           # _hook.mp3 / _ask.mp3 → Wan 2.7 lip-sync on S6 → talk/hook-wan.mp4, talk/ask-wan.mp4
bash src/prep-talk.sh ../talk/hook-wan.mp4 hook && python3 src/align_talk.py ../studio/series-S6-ask.webp --dir src/_build/talk-hook
bash src/prep-talk.sh ../talk/ask-wan.mp4 ask && python3 src/align_talk.py ../studio/series-S6-ask.webp --dir src/_build/talk-ask
python3 src/mux.py config && node src/render.js src/ep04.html src/_build-silent.mp4 && python3 src/mux.py mux src/_build-silent.mp4 ep04-chasen-v1.mp4
```
