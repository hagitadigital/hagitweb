#!/usr/bin/env bash
# Cuts the Kling clips (../clips/elvea-h*.mp4) into 9:16 frame sequences for elvea.html: _build/clips/<scene>/001.jpg …
# 150 frames each (5s at 30fps); elvea.html stretches them over their scene.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
for pair in hook:h1-hook draw:h2-drawing wall:h3-wall box:h4-box end:h5-end; do
  id=${pair%%:*}; f="$HERE/../clips/elvea-${pair#*:}.mp4"
  [ -f "$f" ] || { echo "missing $f"; continue; }
  rm -rf "$HERE/_build/clips/$id"; mkdir -p "$HERE/_build/clips/$id"
  ffmpeg -y -loglevel error -i "$f" -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -frames:v 150 -q:v 3 "$HERE/_build/clips/$id/%03d.jpg"
  echo "$id: $(ls "$HERE/_build/clips/$id" | wc -l) frames"
done
