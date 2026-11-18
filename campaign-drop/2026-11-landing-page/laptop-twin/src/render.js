const { chromium } = require('playwright'); const { spawn } = require('child_process'); const fs=require('fs');
const [,, out, only] = process.argv; const N=546;
(async()=>{
  const b=await chromium.launch({proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined,args:['--allow-file-access-from-files','--ignore-certificate-errors']});
  const p=await b.newPage({viewport:{width:1080,height:1920}});
  await p.goto('file://'+process.cwd()+'/film.html',{waitUntil:'load'});
  await p.evaluate(()=>document.fonts.ready);
  console.error('fonts:',await p.evaluate(()=>[...new Set([...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight))].join(', ')));
  const frames=only?only.split(',').map(Number):[...Array(N).keys()];
  let ff=null;
  if(!only) ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
  for(const f of frames){
    await p.evaluate(f=>window.setT(f),f);
    await p.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
    const buf=await p.screenshot({type:'jpeg',quality:93});
    if(ff){ if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); } else fs.writeFileSync(`${out}-${f}.jpg`,buf);
  }
  if(ff){ff.stdin.end(); await new Promise(r=>ff.on('close',r));}
  await b.close();
})();
