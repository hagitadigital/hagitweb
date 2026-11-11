#!/usr/bin/env bash
# «כמה עולה? ונעלמה»: renders both end-card versions in 9:16 and 4:5.
# Usage: bash src/build.sh [out-dir]   (default: the folder above src/)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$(realpath "${1:-$HERE/..}")"
SK="$HERE/../../../../.claude/skills/brandos-brand-world-reel/scripts"
cd "$HERE"
for v in b long; do
  name="kama-ole-lp$( [ $v = b ] && echo B || echo Long )"
  node "$SK/render.js" "reel.html#$v" 17.5 "$OUT/$name-9x16.mp4"
  bash "$SK/frame45.sh" "$OUT/$name-9x16.mp4" "$OUT/$name-4x5.mp4"
done
ls -la "$OUT"
