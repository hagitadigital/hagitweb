#!/bin/bash
# EP04 inputs: CHASEN° film chapters + workshop hands → src/_build/<name>/f_001.jpg … (15 fps)
set -e; cd "$(dirname "$0")"; C=../../../../chasen
for x in "poudre film/01-poudre-m.mp4" "chasen film/02-chasen-m.mp4" "verre film/03-verre-m.mp4" "mains assets/lecon/mains.mp4"; do set -- $x
  D=_build/$1; rm -rf $D; mkdir -p $D; ffmpeg -v error -i $C/$2 -vf fps=15 -q:v 3 $D/f_%03d.jpg; echo "$1 $(ls $D | wc -l)"; done
