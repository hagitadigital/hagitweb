# ORÉVA° — identity-build reel (render notes)

- `ORÉVA-identity-9x16-silent.mp4` (1080×1920, 30fps, 34s) and `-4x5-silent.mp4` (1080×1350): first cut, no audio, timed to an estimated voice-over.
- Source: `src/gen.py` → `src/reel.html` (assets in `src/a/`, copied from `oreva/assets`).
- Every timing is in `gen.py`: the `VO` list (caption start/end per line), the scene starts `T_*`, and `T_MOM` (the three palette moments).
- When the recording arrives: measure each line's start/end, update `VO`, `T_*`, `T_MOM` and `D`, run `python3 gen.py`,
  render with `.claude/skills/brandos-brand-world-reel/scripts/render.js src/reel.html <D> out.mp4`, then mux the audio with ffmpeg.
