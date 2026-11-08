#!/bin/bash
# EP03 inputs: the VELUNE° door sequence (d01–d40 opens, e01–e40 dolly into the garden) → src/_build/door/f_001.jpg … (sorted)
set -e; cd "$(dirname "$0")"; D=_build/door; rm -rf $D; mkdir -p $D; i=1
for f in $(ls ../../../../velune/assets/porte/*.webp | sort); do ffmpeg -v error -i "$f" -q:v 3 $D/f_$(printf %03d $i).jpg; i=$((i+1)); done
ls $D | wc -l
