#!/usr/bin/env bash
# v2: full-bleed 9:16 sequences at 12 fps. Two-person shots pan from Or Éva to the client.
set -euo pipefail
cd "$(dirname "$0")"
K=../kling
mkdir -p seq2/hand seq2/diag seq2/bed seq2/show seq2/kit seq2/bottle
ffmpeg -y -loglevel error -i $K/01-cream-on-hand.mp4     -vf "crop=608:1080:368:0,scale=720:1280:flags=lanczos,fps=12" -q:v 4 seq2/hand/f_%03d.jpg
ffmpeg -y -loglevel error -i $K/04-consultation.mp4      -vf "crop=608:1080:'99+557*min(t\,4.4)/4.4':0,scale=720:1280:flags=lanczos,fps=12" -q:v 4 seq2/diag/f_%03d.jpg
ffmpeg -y -loglevel error -i $K/02-facial-treatment.mp4  -vf "crop=608:1080:466:0,scale=720:1280:flags=lanczos,fps=12" -q:v 4 seq2/bed/f_%03d.jpg
ffmpeg -y -loglevel error -ss 2 -i $K/03-pump-into-palm.mp4 -vf "crop=661:1176:'146+688*min(t\,3)/3':0,scale=720:1280:flags=lanczos,fps=12" -q:v 4 seq2/show/f_%03d.jpg
ffmpeg -y -loglevel error -i $K/05-kit-box.mp4           -vf "crop=608:1080:310:0,scale=720:1280:flags=lanczos,fps=12" -q:v 4 seq2/kit/f_%03d.jpg
B="$(cd ../../../oreva/assets/bloom && pwd)"
for i in $(seq -w 1 48); do x=$(( 437 + 135 * (10#$i - 1) / 47 )); ffmpeg -y -loglevel error -i "$B/f$i.webp" -vf "crop=406:722:$x:0,scale=720:1280:flags=lanczos" -q:v 4 seq2/bottle/f_0$i.jpg; done
for d in seq2/*; do echo "$d $(ls $d | wc -l)"; done
