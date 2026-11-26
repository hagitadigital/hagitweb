// Records the RUE° site's own "five stairs" animation, frame by frame, into frames/stairs/###.jpg (1200x750).
// The section's CSS transitions are paused and stepped, so the capture is exact.   node capture_stairs.js
const path=require('path'),fs=require('fs'),{chromium}=require('playwright');
(async()=>{
  const out=path.join(__dirname,'frames/stairs');fs.mkdirSync(out,{recursive:true});
  const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
  const b=await chromium.launch({proxy,args:['--allow-file-access-from-files','--ignore-certificate-errors']});
  const p=await b.newPage({viewport:{width:1200,height:750},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve(__dirname,'../../../rue/index.html'),{waitUntil:'load'});
  await p.evaluate(()=>document.fonts.ready);
  const y=await p.evaluate(()=>{const s=document.querySelector('.stairs');const sec=s.closest('section');const r=sec.getBoundingClientRect();return r.top+scrollY;});
  await p.evaluate(y=>scrollTo(0,y-10),y); await p.waitForTimeout(1800);
  await p.evaluate(async()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager');await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})));});
  await p.evaluate(()=>{const s=document.querySelector('.stairs');s.classList.remove('in');void s.offsetWidth;});
  await p.waitForTimeout(400);
  await p.evaluate(()=>{const s=document.querySelector('.stairs');s.classList.add('in');void s.offsetWidth;window.__a=document.getAnimations().filter(a=>s.contains(a.effect.target));window.__a.forEach(a=>a.pause());});
  const n=await p.evaluate(()=>window.__a.length);console.log('transitions',n);
  for(let f=0;f<75;f++){await p.evaluate(t=>window.__a.forEach(a=>{try{a.currentTime=t}catch(e){}}),f*1000/30);
    await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
    await p.screenshot({path:path.join(out,String(f).padStart(3,'0')+'.jpg'),type:'jpeg',quality:92});}
  await b.close();
})();
