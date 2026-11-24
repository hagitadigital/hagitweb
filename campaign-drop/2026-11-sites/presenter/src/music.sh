#!/bin/sh
# sh music.sh <track> : lays the track under the voice of v2 -> ../SITES-PRESENTER-v3-music-9x16.mp4
# Quiet under the voice, up for the voice-free beat while the frame lands (25.0-28.5s), fade in and out.
D=$(dirname "$0")/..
ffmpeg -y -loglevel error -i "$D/SITES-PRESENTER-v2-9x16.mp4" -i "$1" -filter_complex \
"[1:a]atrim=0:42.84,volume='0.10+0.34*clip((t-24.8)/0.5,0,1)*clip((28.8-t)/0.5,0,1)':eval=frame,afade=t=in:d=0.6,afade=t=out:st=41.3:d=1.5[m];[0:a]volume=1.5[v];[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]" \
-map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$D/SITES-PRESENTER-v3-music-9x16.mp4"
