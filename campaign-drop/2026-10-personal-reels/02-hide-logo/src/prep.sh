#!/usr/bin/env bash
# Builds what reel.html and render.js read, into src/_build/ (not committed):
#   _build/placeholder.mp4     — stand-in talking head (Hagit's portrait, slow push-in), 22s, silent
#   _build/films/rosee/NN.jpg  — 4.5s of the ROSÉE° film at 15fps (title, dew drop, cloud) for the world card
# Run from anywhere:  bash campaign-drop/2026-10-personal-reels/02-hide-logo/src/prep.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
B="$HERE/_build"
mkdir -p "$B/films/rosee"

ffmpeg -y -loglevel error -loop 1 -framerate 30 -t 22 -i "$ROOT/hagit-portrait-2026.png" \
  -f lavfi -t 22 -i anullsrc=r=48000:cl=stereo \
  -filter_complex "[0:v]scale=-2:2400,crop=1350:2400,scale=1080:1920,\
zoompan=z='1+0.06*on/660':x='iw/2-(iw/zoom/2)+12*sin(on/40)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p[v]" \
  -map "[v]" -map 1:a -c:v libx264 -crf 20 -preset veryfast -c:a aac -shortest "$B/placeholder.mp4"

ffmpeg -y -loglevel error -ss 3.2 -t 4.5 -i "$ROOT/images/home-worlds/live/films/rosee.mp4" \
  -vf "fps=15,scale=400:-2" -q:v 3 "$B/films/rosee/%02d.jpg"
echo "built: $B"
