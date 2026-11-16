# ORÉVA° — identity-build reel (render notes)

- `ORÉVA-identity-9x16.mp4` (1080×1920, 30fps, 55s) and `ORÉVA-identity-4x5.mp4` (1080×1350): with the Cartesia voice-over (`src/vo-cartesia.wav`, 51.6s, starts 0.25s in).
- Source: `src/gen.py` → `src/reel.html` (assets in `src/a/`, stills and frame sequences cut from `oreva/assets`).
- Every timing is in `gen.py`: scene starts `T_*`, `PROM`, `TOUCH`, and the caption cards `CAPS`. They were set from the pauses in the recording
  (`ffmpeg -af silencedetect=noise=-30dB:d=0.09`), not from a transcript.
- Re-render: `python3 src/gen.py`, then `.claude/skills/brandos-brand-world-reel/scripts/render.js src/reel.html 55 v.mp4`, `frame45.sh` for 4:5,
  and mux: `-af "adelay=250,apad=whole_dur=55,loudnorm=I=-16:TP=-1.5"`.
- Music bed: `src/music-bed.mp3` (generated instrumental), mixed about 15 LU under the voice, 1s fade-in, 2.2s fade-out.
