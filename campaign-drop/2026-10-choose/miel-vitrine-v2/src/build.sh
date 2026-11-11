#!/usr/bin/env bash
# MIEL° vitrine ad v2: 18s recut of MIEL-vitrine-ad-v1-4x5.mp4.
#   0.0–3.0   hook (new, scenes.html#hook): question + generic grid vs. MIEL vitrine, both ₪290, in frame 0
#   3.0–5.5   v1 5.0–7.5   drag a slice in the vitrine
#   5.5–8.5   v1 12.0–15.0 bags fill under the laptop
#   8.5–11.5  v1 16.0–19.0 «חמש עוגות. חמש שקיות.»
#   11.5–14.0 bridge (new): «אותו מחיר. ₪290.» / «אבל עכשיו יש סיבה לקנות דווקא אצלך.»
#   14.0–18.5 end card (new), holds to the last frame. Two versions: -lpB (send a link, 3 points) and -lpLong (30-min diagnosis).
# Usage: build.sh <v1-4x5.mp4> <out-dir>
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
V1="$(realpath "$1")"; mkdir -p "$2"; OUT="$(realpath "$2")"
SK="$HERE/../../../../.claude/skills/brandos-brand-world-reel/scripts"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cd "$HERE"
node "$SK/render.js" 'scenes.html#hook'     3.0 "$TMP/hook.mp4"
node "$SK/render.js" 'scenes.html#bridge'   2.5 "$TMP/bridge.mp4"
node "$SK/render.js" 'scenes.html#end-b'    4.5 "$TMP/end-b.mp4"
node "$SK/render.js" 'scenes.html#end-long' 4.5 "$TMP/end-long.mp4"
# v1 is 4:5 with the reel whole in the centre column (x 160–920); take that column back up to 9:16.
CUT="crop=760:1350:160:0,scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
for end in b long; do
  ffmpeg -y -loglevel error -i "$TMP/hook.mp4" \
    -ss 5.0 -t 2.5 -i "$V1" -ss 12.0 -t 3.0 -i "$V1" -ss 16.0 -t 3.0 -i "$V1" \
    -i "$TMP/bridge.mp4" -i "$TMP/end-$end.mp4" -filter_complex \
    "[0:v]setsar=1,fps=30,format=yuv420p[a];[1:v]$CUT[b];[2:v]$CUT[c];[3:v]$CUT[d];[4:v]setsar=1,fps=30,format=yuv420p[e];[5:v]setsar=1,fps=30,format=yuv420p[f];[a][b][c][d][e][f]concat=n=6:v=1:a=0[v]" \
    -map "[v]" -an -c:v libx264 -crf 18 -preset medium -movflags +faststart "$OUT/MIEL-vitrine-v2-lp$( [ $end = b ] && echo B || echo Long )-9x16.mp4"
done
for f in "$OUT"/MIEL-vitrine-v2-*-9x16.mp4; do bash "$SK/frame45.sh" "$f" "${f%-9x16.mp4}-4x5.mp4"; done
ls -la "$OUT"
