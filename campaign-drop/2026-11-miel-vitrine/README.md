# MIEL° · La Vitrine — reel (Nov 2026)

Studio mode, "live screen" format, 18s. Render notes only; caption/copy live in brandos/briefs.

- `out/MIEL-27-vitrine.mp4` — 9:16, 1080×1920, 30fps, 18.0s (Reels/Stories)
- `out/MIEL-27-vitrine-4x5.mp4` — 4:5 feed version (frame45.sh)
- `src/gen.py` → `src/reel.html` (all timing in seconds at the top of gen.py), `src/assets/` copied from miel/assets + images/bw-lp/generic-cake.jpg

Re-render: `cd src && python3 gen.py && node ../../../.claude/skills/brandos-brand-world-reel/scripts/render.js reel.html 18 ../out/MIEL-27-vitrine.mp4`
then `bash ../../../.claude/skills/brandos-brand-world-reel/scripts/frame45.sh ../out/MIEL-27-vitrine.mp4 ../out/MIEL-27-vitrine-4x5.mp4`.
No audio: add a trending sound in Instagram.
