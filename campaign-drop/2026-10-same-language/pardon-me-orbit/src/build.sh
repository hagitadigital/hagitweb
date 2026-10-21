#!/usr/bin/env bash
# PARDON ME° orbit (25s): reel.html → ../pardon-me-29-orbit.mp4 (+ soundtrack) and the 4:5 feed version.
# Run from this folder. Intermediate files go to f/ (gitignored).
set -euo pipefail
SK=../../../../.claude/skills/brandos-brand-world-reel/scripts
OUT=../pardon-me-29-orbit
mkdir -p f
python3 make.py
node $SK/render.js reel.html 25 f/silent.mp4
# Arrête Chic (the campaign's soundtrack), first 25s, soft in, fade out over the last 1.5s
ffmpeg -y -loglevel error -i f/silent.mp4 -i media/arrete-chic-30.m4a -filter_complex "[1:a]atrim=0:25,afade=t=in:d=0.3,afade=t=out:st=23.5:d=1.5[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $OUT.mp4
node -e '
  const p=require("path");let pw;for(const n of ["playwright","/opt/node22/lib/node_modules/playwright"]){try{pw=require(n);break}catch(e){}}
  (async()=>{const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
    const b=await pw.chromium.launch({proxy,args:["--ignore-certificate-errors"]});const t=await b.newPage({viewport:{width:1080,height:1350}});
    await t.goto("file://"+p.resolve("frame-4x5.html"),{waitUntil:"networkidle"});await t.evaluate(()=>document.fonts.ready);
    await t.screenshot({path:"f/frame-4x5.png",omitBackground:true});await b.close();})();'
ffmpeg -y -loglevel error -i $OUT.mp4 -i f/frame-4x5.png -filter_complex \
  "color=c=0xFAF8F3:s=1080x1350:r=30[bg];[0:v]scale=760:1350:flags=lanczos[v];[bg][v]overlay=160:0:shortest=1[a];[a][1:v]overlay=0:0,format=yuv420p[o]" \
  -map "[o]" -map 0:a -c:v libx264 -crf 18 -preset medium -c:a copy -movflags +faststart $OUT-4x5.mp4
echo "wrote $OUT.mp4 and $OUT-4x5.mp4"
