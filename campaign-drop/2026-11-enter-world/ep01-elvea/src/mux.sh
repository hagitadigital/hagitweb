#!/bin/bash
# Mux EP01: Hagit's Cartesia VO (shifted to make room for the entry and exit), music bed, two paper whooshes.
# VO_SHIFT: VO 0–11.9 → +0 · 11.9–28.76 → +0.6 · 28.76–end → +1.4   (matches the TIMING block in ep01.html)
# usage: bash src/mux.sh <silent.mp4> <out.mp4>
set -e; cd "$(dirname "$0")/.."
V=voice/ep01-vo-cartesia.wav; M=voice/bed-piano-strings-v1.mp3; DUR=38.2
ffmpeg -y -loglevel error -i "$1" -i $V -i $M -f lavfi -t 0.9 -i "anoisesrc=color=pink:amplitude=0.6:r=44100" -filter_complex "
[1:a]asplit=3[a][b][c];
[a]atrim=0:11.9,asetpts=PTS-STARTPTS[v1];
[b]atrim=11.9:28.76,asetpts=PTS-STARTPTS,adelay=12500|12500[v2];
[c]atrim=28.76,asetpts=PTS-STARTPTS,adelay=30160|30160[v3];
[v1][v2][v3]amix=inputs=3:normalize=0,aformat=channel_layouts=stereo,volume=1.0[vo];
[3:a]bandpass=f=1800:w=1600,afade=t=in:d=0.45,afade=t=out:st=0.45:d=0.45,volume=0.22,asplit=2[w1][w2];
[w1]adelay=11800|11800[wa];[w2]adelay=29300|29300[wb];
[2:a]atrim=0:$DUR,afade=t=in:d=1.0,afade=t=out:st=$(echo "$DUR-2.5"|bc):d=2.5,volume=0.16[mus];
[vo]asplit=2[vo1][sc];
[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];
[vo1][duck][wa][wb]amix=inputs=4:normalize=0,alimiter=limit=0.95[aout]" \
 -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -t $DUR -movflags +faststart "$2"
