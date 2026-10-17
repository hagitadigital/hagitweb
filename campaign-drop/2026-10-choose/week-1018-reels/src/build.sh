#!/usr/bin/env bash
# Rebuild the ORÉVA° Sunday reel (oreva-24-price.mp4 + 4:5) from the repo root's oreva/assets films.
# Run from this folder. Frames go to f/ (gitignored).
set -euo pipefail
ROOT=../../../..; SK=$ROOT/.claude/skills/brandos-brand-world-reel/scripts
for n in hands treatment kit pump diagnosis; do bash $SK/video2seq.sh $ROOT/oreva/assets/$n-loop.mp4 f $n 2; done
bash $SK/video2seq.sh $ROOT/oreva/assets/texture.mp4 f texture 3
node $SK/render.js oreva-price.html 30 ../oreva-24-price.mp4
# 4:5 feed version with the design system's cream side panels (the skill's frame45.sh uses the website cream)
node -e '
  const p=require("path");let pw;for(const n of ["playwright","/opt/node22/lib/node_modules/playwright"]){try{pw=require(n);break}catch(e){}}
  (async()=>{const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
    const b=await pw.chromium.launch({proxy,args:["--ignore-certificate-errors"]});const t=await b.newPage({viewport:{width:1080,height:1350}});
    await t.goto("file://"+p.resolve("frame-4x5.html"),{waitUntil:"networkidle"});await t.evaluate(()=>document.fonts.ready);
    await t.screenshot({path:"f/frame-4x5.png",omitBackground:true});await b.close();})();'
ffmpeg -y -loglevel error -i ../oreva-24-price.mp4 -i f/frame-4x5.png -filter_complex \
  "color=c=0xF2EBDC:s=1080x1350:r=30[bg];[0:v]scale=760:1350:flags=lanczos[v];[bg][v]overlay=160:0:shortest=1[a];[a][1:v]overlay=0:0,format=yuv420p" \
  -c:v libx264 -crf 18 -preset medium -movflags +faststart ../oreva-24-price-4x5.mp4
