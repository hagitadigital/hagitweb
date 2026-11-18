// node cap2.js <outdir> <frames> <fps> <keyframes: "f:y,f:y,...">   (MOBILE=1 for phone)  deterministic: CSS animations + videos follow frame time
const { chromium } = require('playwright'); const fs=require('fs');
const [,, out, N, FPS, keys] = process.argv;
const K=keys.split(',').map(s=>s.split(':').map(Number));
const ez=t=>t<.5?2*t*t:1-Math.pow(-2*t+2,2)/2;
function yAt(f){ if(f<=K[0][0]) return K[0][1]; for(let i=0;i<K.length-1;i++){const [a,ya]=K[i],[b,yb]=K[i+1]; if(f<=b) return ya+(yb-ya)*ez((f-a)/(b-a));} return K[K.length-1][1]; }
(async()=>{
  fs.mkdirSync(out,{recursive:true});
  const b = await chromium.launch({proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY,bypass:'localhost'}:undefined,args:['--ignore-certificate-errors','--autoplay-policy=no-user-gesture-required']});
  const p = await b.newPage(process.env.MOBILE?{viewport:{width:390,height:693},deviceScaleFactor:1080/390,isMobile:true,hasTouch:true}:{viewport:{width:1440,height:900}});
  await p.goto('http://localhost:8766/preview.html',{waitUntil:'load'});
  await p.addStyleTag({content:'html{scroll-behavior:auto!important}::-webkit-scrollbar{display:none}'});
  await p.evaluate(()=>document.fonts.ready);
  const H=await p.evaluate(()=>document.documentElement.scrollHeight);
  for (let y=0;y<H;y+=500){ await p.evaluate(y=>scrollTo(0,y),y); await p.waitForTimeout(90); }   // warm lazy images + frames
  await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(1200);
  await p.evaluate(()=>{ document.querySelectorAll('video').forEach(v=>{v.pause(); v.play=()=>Promise.resolve();}); });
  for (let i=0;i<+N;i++){
    const t=i/+FPS;
    await p.evaluate(y=>scrollTo(0,y),yAt(i));
    await p.evaluate(async t=>{
      document.getAnimations().forEach(a=>{ if(a instanceof CSSAnimation && !(a.timeline instanceof ViewTimeline)){ a.pause(); a.currentTime=t*1000; } });
      await Promise.all([...document.querySelectorAll('video')].filter(v=>v.classList.contains('on')||v.closest('.hero')).map(v=>new Promise(r=>{ const d=v.duration||10, tt=t%d; if(Math.abs(v.currentTime-tt)<.001) return r(); v.addEventListener('seeked',r,{once:true}); v.currentTime=tt; setTimeout(r,800); })));
      await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
    },t);
    await p.waitForTimeout(45);
    await p.screenshot({path:`${out}/s${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});
  }
  await b.close();
})();
