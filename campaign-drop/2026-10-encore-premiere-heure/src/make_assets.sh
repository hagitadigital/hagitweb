#!/usr/bin/env bash
# Cut ENCORE° assets for the reel: the landing sequence and touchpoints to 9:16 at 720x1280, pieces copied as-is.
set -euo pipefail
cd "$(dirname "$0")"
W=../../../encore/assets
mkdir -p seq/land tp pieces
i=0; for f in $W/hero/land/l*.webp; do i=$((i+1)); ffmpeg -y -loglevel error -i "$f" -vf "crop=503:894:548:0,scale=720:1280:flags=lanczos" -q:v 3 "seq/land/f_$(printf %03d $i).jpg"; done
ffmpeg -y -loglevel error -i $W/touchpoints/tag-cuff.webp -vf "crop=633:1125:180:0,scale=720:1280:flags=lanczos" -q:v 3 tp/tag-cuff.jpg
ffmpeg -y -loglevel error -i $W/touchpoints/box-open.webp -vf "crop=633:1125:90:0,scale=720:1280:flags=lanczos" -q:v 3 tp/box-open.jpg
ffmpeg -y -loglevel error -i $W/touchpoints/sign.webp     -vf "crop=633:1125:267:0,scale=720:1280:flags=lanczos" -q:v 3 tp/sign.jpg
cp $W/pieces/rings-1.webp $W/pieces/pendants-2.webp $W/pieces/bracelets-1.webp $W/pieces/earrings-3.webp pieces/
echo "land $(ls seq/land | wc -l) frames"
