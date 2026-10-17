#!/usr/bin/env bash
# Cut SIGNÉ° assets for the world film (9:16, 1080×1920 stage). Run from anywhere.
set -euo pipefail
cd "$(dirname "$0")"
W=../../../../signe/assets
K=../../kling/coupe-splash.mp4
rm -rf a; mkdir -p a/pour a/drop a/noir a/framboise a/pistache
# 01 · the pour: 41 frames 1280×720 → 9:16 around the ball (x≈48.5%)
i=0; for f in $W/pour/f*.webp; do i=$((i+1)); ffmpeg -y -loglevel error -i "$f" -vf "crop=405:720:418:0,scale=1080:1920:flags=lanczos" -q:v 3 "a/pour/f_$(printf %03d $i).jpg"; done
# 02 · the plate for the dial + the drop clip (from 0.7s, every 2nd frame)
ffmpeg -y -loglevel error -i $W/coupe-bowl2.webp -q:v 2 a/plate.jpg
ffmpeg -y -loglevel error -ss 0.70 -i $K -vf "select='not(mod(n\,2))',scale=1000:1000:flags=lanczos" -vsync vfr -q:v 3 a/drop/f_%03d.jpg
# hook · Le Noir éclair, portrait crop
ffmpeg -y -loglevel error -i $W/hero-eclair.webp -vf "crop=918:1080:541:0,scale=700:824:flags=lanczos" -q:v 2 a/eclair.jpg
# 03 · the piping hand (kept wide for a pan along the line)
ffmpeg -y -loglevel error -i $W/piping-signature.webp -q:v 2 a/piping.jpg
# 04 · La Carte Vivante holograms (2.2s → 6.0s, every 6th frame) + the counter
for n in noir framboise pistache; do ffmpeg -y -loglevel error -ss 1.6 -t 4.4 -i $W/carte/$n.mp4 -vf "fps=8,crop=608:720:336:0,scale=1080:1280:flags=lanczos" -q:v 3 a/$n/f_%03d.jpg; done
ffmpeg -y -loglevel error -i $W/boutique.webp -q:v 2 a/boutique.jpg
# 05 · the four éditions
for n in noir pistache framboise vanille; do ffmpeg -y -loglevel error -i $W/coll-$n.webp -vf "crop=600:800:150:250,scale=420:560:flags=lanczos" -q:v 2 a/ed-$n.jpg; done
echo "pour $(ls a/pour|wc -l) · drop $(ls a/drop|wc -l) · noir $(ls a/noir|wc -l)"
