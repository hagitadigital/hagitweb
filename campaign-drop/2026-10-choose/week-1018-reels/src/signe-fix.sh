#!/usr/bin/env bash
# SIGNÉ° Monday reel = the site's world film (images/home-worlds/live/films/signe.mp4, 720×1280), fixed for the feed:
# frames 0–44 get the top of frame 45 (question + éclair card with the logo already covered), so frame 0 — the thumbnail —
# shows the hook and its proof; the ball line below stays live. Then upscaled to 1080×1920 and framed 4:5.
# The film's HTML source is not in this repo. Run from this folder after build.sh made f/frame-4x5.png.
set -euo pipefail
F=../../../../images/home-worlds/live/films/signe.mp4
ffmpeg -v error -y -i $F -filter_complex "[0:v]split=2[a][b];[b]select='eq(n\,45)',crop=720:1040:0:0,loop=loop=-1:size=1:start=0,setpts=N/30/TB[top];[a][top]overlay=0:0:enable='lt(n\,45)':shortest=1,scale=1080:1920:flags=lanczos,format=yuv420p[v]" -map "[v]" -r 30 -c:v libx264 -crf 17 -preset medium -movflags +faststart ../signe-17-logo.mp4
ffmpeg -y -loglevel error -i ../signe-17-logo.mp4 -i f/frame-4x5.png -filter_complex "color=c=0xF2EBDC:s=1080x1350:r=30[bg];[0:v]scale=760:1350:flags=lanczos[v];[bg][v]overlay=160:0:shortest=1[a];[a][1:v]overlay=0:0,format=yuv420p" -c:v libx264 -crf 18 -preset medium -movflags +faststart ../signe-17-logo-4x5.mp4
