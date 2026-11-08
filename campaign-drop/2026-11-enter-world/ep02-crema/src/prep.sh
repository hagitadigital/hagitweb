#!/bin/bash
# EP02 build inputs: frames of the Crema° world film (capsule ring, 8.8s–14.8s) → src/_build/film/f_001.jpg …
set -e; cd "$(dirname "$0")"; D=_build/film; rm -rf $D; mkdir -p $D
ffmpeg -v error -ss 8.8 -t 6.0 -i ../../../../images/home-worlds/live/films/crema.mp4 -vf "fps=30" -q:v 3 $D/f_%03d.jpg
ls $D | wc -l
