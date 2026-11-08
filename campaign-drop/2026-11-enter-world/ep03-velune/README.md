# EP03 · VELUNE° (No.25) · ההבטחה, והדלת שחוזרת

Same arc as EP02. The entry is the world's own door: the code panel shows the closed door, it opens (velune/assets/porte d01–d40)
and we walk into the garden (e01–e40). Proof: the arch traced in gold on the door, the box (which then opens) and the boutique;
insight: the three arches alone.

- `ep03-velune-preview.mp4` — without the hook and the business line (not recorded yet).
- Script, copy: `brandos/briefs/series-enter-world-2026-11/EP03-velune.md`.

## Build
```
bash src/prep.sh                         # door sequence → src/_build/door
# voice/hook.wav, voice/biz.wav when recorded → python3 src/mux.py audio → lip-sync clips (Wan 2.7) → prep-talk.sh hook|ask + align_talk.py
python3 src/mux.py config && node src/render.js src/ep03.html src/_build-silent.mp4 && python3 src/mux.py mux src/_build-silent.mp4 ep03-velune-v1.mp4
```
