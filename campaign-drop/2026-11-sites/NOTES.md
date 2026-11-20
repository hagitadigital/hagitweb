# SITES reels — opening swap (2026-11-20)

- `SITES-RUE-v6-music-9x16.mp4` — from `SITES-RUE-v5-music-9x16.mp4`
- `SITES-ALIVE-v7-music-4x5.mp4` — from `SITES-ALIVE-v6-music-4x5.mp4`

Only frames 0–80 (0–2.7s) changed: the office selfie was replaced by the new clip with the
arch background (source clip 3.6s–6.3s, 720×1280 24fps, upscaled). The hook card is lifted from
frame 0 of the previous version, so its text is pixel-identical. Zoom-into-the-laptop transition
rebuilt. Everything from frame 81 on, and the music, is the previous version untouched.

Re-render: `python -I src/swap-opening.py <previous.mp4> <new-clip.mp4> <out.mp4> <work-dir> [--start 3.6]`
The previous versions and the source clip are not in this folder.
