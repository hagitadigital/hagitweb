# EP02 · Crema° · «נכנסים לעולם מותג»

Arc (after the EP01 critique): hook to camera (S6, lip-synced) → «בואי ניכנס» + board → entry through the code panel →
world: demo (capsule ring, seven cups), problem (generic café), proof (pan along the seven cups → only the rims stay), insight →
exit → S6: business line + question (lip-synced) → name + «אבחון פער המותג» CTA only at the very end.
World scenes are full-bleed with camera moves, no framed cards.

- `ep02-crema-v1.mp4` — with the business line (`../shared/biz.wav`) and the lip-synced close; hook text only (hook not recorded yet).
- Script, copy: `brandos/briefs/series-enter-world-2026-11/EP02-crema.md`.

## Build
```
bash src/prep.sh                                   # world-film frames → src/_build/film
# recordings: voice/hook.wav (hook), voice/biz.wav (business line, same file every episode)
python3 src/mux.py audio                           # voice/_ask.wav = biz + pause + question → lip-sync clip for S6 (Wan 2.7)
bash src/prep-talk.sh <hook-clip.mp4> hook && python3 src/align_talk.py ../studio/series-S6-ask.webp --dir src/_build/talk-hook
bash src/prep-talk.sh ../talk/ask-wan.mp4 ask && python3 src/align_talk.py ../studio/series-S6-ask.webp --dir src/_build/talk-ask
python3 src/mux.py config                          # writes src/config.js (lengths + frame counts)
node src/render.js src/ep02.html src/_build-silent.mp4 && python3 src/mux.py mux src/_build-silent.mp4 ep02-crema-v1.mp4
```
Note: prep-talk.sh / align_talk.py paths are relative to src/ (prep-talk.sh cds into src).
