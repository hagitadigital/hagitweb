// node render.js <outdir> <story> [fps]  -> frames to <outdir>/_frames/<story>/
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const [out,s,fps='30']=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920}});
const base='file://'+path.resolve(__dirname,'copper.html');
await p.goto(base+'?s='+s+'&guides');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
const D=await p.evaluate(()=>DUR);
await p.evaluate(t=>setT(t),D);await p.screenshot({path:path.join(out,'_guides',s+'.png')});
await p.goto(base+'?s='+s);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
const dir=path.join(out,'_frames',s);fs.mkdirSync(dir,{recursive:true});
const n=Math.round(D*fps);for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/fps);await p.screenshot({path:path.join(dir,String(i).padStart(4,'0')+'.jpg'),type:'jpeg',quality:93});}
await p.evaluate(t=>setT(t),D);await p.screenshot({path:path.join(out,s+'-still.png')});
await b.close();})();
