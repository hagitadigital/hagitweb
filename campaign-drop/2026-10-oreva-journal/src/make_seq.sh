#!/usr/bin/env bash
# Cut the three Kling clips (../kling) to 9:16 frame sequences at 12 fps for gen.py / reel.html.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p seq/a seq/b seq/c
ffmpeg -y -loglevel error -i ../kling/01-cream-on-hand.mp4     -vf "crop=608:1080:368:0,scale=1080:1920:flags=lanczos,fps=12" -q:v 4 seq/a/f_%03d.jpg
ffmpeg -y -loglevel error -i ../kling/02-facial-treatment.mp4  -vf "crop=608:1080:466:0,scale=1080:1920:flags=lanczos,fps=12" -q:v 4 seq/b/f_%03d.jpg
ffmpeg -y -loglevel error -i ../kling/03-pump-into-palm.mp4    -vf "crop=661:1176:290:0,scale=1080:1920:flags=lanczos,fps=12" -q:v 4 seq/c/f_%03d.jpg
echo "seq ready"
