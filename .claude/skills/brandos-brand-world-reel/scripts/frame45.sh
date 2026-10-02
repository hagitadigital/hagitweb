#!/usr/bin/env bash
# 9:16 reel → 4:5 feed version (1080×1350) for LinkedIn and the Facebook feed.
# The reel is never cropped: it sits whole in the centre (760×1350) between the studio's cream side panels
# with a thin copper rule and vertical "BRAND WORLDS STUDIO" / "HAGITANTEBI.CO.IL".
# Usage: frame45.sh <in-9x16.mp4> <out-4x5.mp4>
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
IN="$1"; OUT="$2"
FF="${FFMPEG:-$(command -v ffmpeg || python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')}"
PNG="$HERE/../assets/frame-4x5.png"
if [ ! -f "$PNG" ]; then
  node -e '
    const p=require("path");let pw;for(const n of ["playwright","/opt/node22/lib/node_modules/playwright","/usr/lib/node_modules/playwright"]){try{pw=require(n);break}catch(e){}}
    (async()=>{const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
      const b=await pw.chromium.launch({proxy,args:["--ignore-certificate-errors"]});const t=await b.newPage({viewport:{width:1080,height:1350}});
      await t.goto("file://"+p.resolve(process.argv[1]),{waitUntil:"networkidle"});await t.evaluate(()=>document.fonts.ready);
      await t.screenshot({path:process.argv[2],omitBackground:true});await b.close();})();
  ' "$HERE/../assets/frame-4x5.html" "$PNG"
fi
"$FF" -y -loglevel error -i "$IN" -i "$PNG" -filter_complex \
  "color=c=0xFAF8F3:s=1080x1350:r=30[bg];[0:v]scale=760:1350:flags=lanczos[v];[bg][v]overlay=160:0:shortest=1[a];[a][1:v]overlay=0:0,format=yuv420p" \
  -c:v libx264 -crf 18 -preset medium -movflags +faststart "$OUT"
echo "wrote $OUT"
