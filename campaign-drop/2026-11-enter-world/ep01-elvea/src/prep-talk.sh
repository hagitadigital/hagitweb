#!/bin/bash
# Cut a lip-sync clip into 30fps 1080x1920 frames for ep01.html.  usage: bash src/prep-talk.sh <clip.mp4> <S1|S6>
# Then set n (frame count printed here) in the TALK block of ep01.html.
set -e; cd "$(dirname "$0")"; D=_build/talk-$2; rm -rf $D; mkdir -p $D
ffmpeg -v error -i "$1" -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -q:v 3 $D/f_%04d.jpg
ls $D | wc -l
