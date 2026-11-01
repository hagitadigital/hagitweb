#!/usr/bin/env bash
# Renders every world: the 26.5s reel and the 3s hook, each as 9:16 and 4:5.  Run from the repo root.
set -euo pipefail
R=.claude/skills/brandos-brand-world-reel/scripts/render.js
C=campaign-drop/2026-11-worlds
node -e '
  const p=require("path");let pw;for(const n of ["playwright","/opt/node22/lib/node_modules/playwright","/usr/lib/node_modules/playwright"]){try{pw=require(n);break}catch(e){}}
  (async()=>{const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
    const b=await pw.chromium.launch({proxy,args:["--ignore-certificate-errors"]});const t=await b.newPage({viewport:{width:1080,height:1350}});
    await t.goto("file://"+p.resolve(process.argv[1]),{waitUntil:"networkidle"});await t.evaluate(()=>document.fonts.ready);
    await t.screenshot({path:process.argv[2],omitBackground:true});await b.close();})();
' $C/_gen/frame-4x5.html $C/_gen/frame-4x5.png
to45(){ ffmpeg -y -loglevel error -i "$1" -i $C/_gen/frame-4x5.png -filter_complex \
  "color=c=0xF2EBDC:s=1080x1350:r=30[bg];[0:v]scale=760:1350:flags=lanczos[v];[bg][v]overlay=160:0:shortest=1[a];[a][1:v]overlay=0:0,format=yuv420p" \
  -c:v libx264 -crf 18 -preset medium -movflags +faststart "$2"; }
one(){ w=$1; W=$(echo $w | tr a-z A-Z)
  node $R $C/$w/src/reel.html 26.5 $C/$w/$W-hidden-logo-9x16.mp4
  node $R $C/$w/src/hook.html 3 $C/$w/$W-hook-3s-9x16.mp4
  to45 $C/$w/$W-hidden-logo-9x16.mp4 $C/$w/$W-hidden-logo-4x5.mp4
  to45 $C/$w/$W-hook-3s-9x16.mp4 $C/$w/$W-hook-3s-4x5.mp4
  echo "done $w"; }
for w in ${@:-oreva encore miel}; do one $w & done; wait
