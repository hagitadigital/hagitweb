// node render.js <seconds> <out.mp4>            full render, 1080x1920 30fps
// node render.js <seconds> <prefix> 0,90,200    stills
const path=require('path'),fs=require('fs'),{spawn}=require('child_process');
const {chromium}=require('playwright');
const [,,durS,out,only]=process.argv;const FPS=30;
(async()=>{
  const proxy=process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined;
  const br=await chromium.launch({proxy,args:['--allow-file-access-from-files','--ignore-certificate-errors']});
  const tab=await br.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  tab.on('pageerror',e=>console.error('PAGE',e.message));
  await tab.goto('file://'+path.resolve(__dirname,process.env.REEL||'reel.html'),{waitUntil:'load'});
  await tab.evaluate(()=>window.ready);
  console.error('fonts:',await tab.evaluate(()=>[...new Set([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family))].join(', ')));
  const frames=only?only.split(',').map(Number):[...Array(Math.round(+durS*FPS)).keys()];
  let ff=null;
  if(!only)ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','png','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','16','-preset','slow','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
  for(const f of frames){
    await tab.evaluate(t=>window.seek(t),f/FPS);
    await tab.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
    if(ff){const b=await tab.screenshot({type:'png'});if(!ff.stdin.write(b))await new Promise(r=>ff.stdin.once('drain',r));if(f%90===0)console.error('frame',f);}
    else fs.writeFileSync(`${out}-${String(f).padStart(3,'0')}.jpg`,await tab.screenshot({type:'jpeg',quality:88}));
  }
  if(ff){ff.stdin.end();await new Promise(r=>ff.on('close',r));}
  await br.close();
})();
