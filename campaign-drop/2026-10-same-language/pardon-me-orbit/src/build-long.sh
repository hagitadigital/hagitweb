#!/usr/bin/env bash
# PARDON ME° orbit, long cut: each card opens to a full window and PARDON ME's own site plays in it.
# Run from this folder. Intermediate files go to f/ (gitignored).
#   1. (once, or after the site changes) node record-site.js ../../../../pardon-me/index.html media/clips
#   2. bash build-long.sh
set -euo pipefail
SK=../../../../.claude/skills/brandos-brand-world-reel/scripts
mkdir -p f
for c in peek tear ads colls; do
  ffmpeg -y -loglevel error -i media/clips/$c.mp4 -frames:v 1 -q:v 3 media/clips/$c-first.jpg
  ffmpeg -y -loglevel error -sseof -0.05 -i media/clips/$c.mp4 -frames:v 1 -q:v 3 media/clips/$c-last.jpg
done
REEL=long python3 make.py
D=$(python3 -c 'import json;print(json.load(open("long-overlays.json"))["duration"])')
node -e '
  const p=require("path");let pw;for(const n of ["playwright","/opt/node22/lib/node_modules/playwright"]){try{pw=require(n);break}catch(e){}}
  (async()=>{const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
    const b=await pw.chromium.launch({proxy,args:["--ignore-certificate-errors"]});
    for(const [src,out,w,h] of [["frame-4x5.html","f/frame-4x5.png",1080,1350],...[0,1,2,3].map(k=>["f/chip-"+k+".html","f/chip-"+k+".png",1080,1920])]){
      const t=await b.newPage({viewport:{width:w,height:h}});await t.goto("file://"+p.resolve(src),{waitUntil:"networkidle"});
      await t.evaluate(()=>document.fonts.ready);await t.screenshot({path:out,omitBackground:true});await t.close();}
    await b.close();})();'
node $SK/render.js reel-long.html $D f/silent-long.mp4
python3 compose-long.py f/silent-long.mp4 ../pardon-me-29-orbit-long
