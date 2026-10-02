#!/usr/bin/env bash
# A site film (mp4) → an image sequence the template's data-seq can play.
# Usage: video2seq.sh <in.mp4> <out-dir> <prefix> [every-Nth-frame=6]
# Prefer the site's mobile (portrait) version of a film when it exists (e.g. 01-poudre-m.mp4, 720×900).
# 24fps source, every 6th–8th frame → 20–30 frames that play in ~1.5s at data-step 0.06.
set -euo pipefail
IN="$1"; OUT="$2"; PRE="$3"; N="${4:-6}"
FF="${FFMPEG:-$(command -v ffmpeg || python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')}"
mkdir -p "$OUT"
"$FF" -y -loglevel error -i "$IN" -vf "select='not(mod(n\,$N))'" -vsync vfr -q:v 3 "$OUT/${PRE}_%03d.jpg"
echo "$(ls "$OUT"/${PRE}_*.jpg | wc -l) frames → $OUT/${PRE}_%03d.jpg"
