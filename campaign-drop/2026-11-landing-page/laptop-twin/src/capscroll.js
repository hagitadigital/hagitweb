// node capscroll.js <outdir> <width> <height> <frames> <y0> <y1> [hold0 frames] [hold1 frames]
const { chromium } = require('playwright'); const fs=require('fs');
const [,, out, W, H, N, y0, y1, h0='0', h1='0'] = process.argv;
(async()=>{
  fs.mkdirSync(out,{recursive:true});
  const b = await chromium.launch();
  const M=process.env.MOBILE; const p = await b.newPage(M?{viewport:{width:390,height:693},deviceScaleFactor:1080/390,isMobile:true,hasTouch:true}:{viewport:{width:+W,height:+H}});
  await p.route(/facebook|google-analytics|googletagmanager/, r=>r.abort());
  await p.goto('http://localhost:8765/velune/index.html',{waitUntil:'load'});
  await p.addStyleTag({content:'html{scroll-behavior:auto!important}::-webkit-scrollbar{display:none}'});
  // preload by walking the range
  for (let y=+y0; y<=+y1+ +H; y+=300){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(120); }
  await p.waitForTimeout(1500);
  const n=+N, a=+h0, z=+h1, mv=n-a-z;
  const ease=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
  for (let i=0;i<n;i++){
    let t = i<a?0 : i>=n-z?1 : (i-a)/(mv-1);
    const y = +y0 + (+y1- +y0)*ease(t);
    await p.evaluate(y=>scrollTo(0,y),y);
    await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
    await p.waitForTimeout(40);
    await p.screenshot({path:`${out}/s${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});
  }
  await b.close();
})();
