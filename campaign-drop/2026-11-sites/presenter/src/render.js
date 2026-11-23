// node render.js [clean|guide]  -> ../P1..P4 mp4 (+ guide animatic)
const {chromium}=require('playwright'),{execSync}=require('child_process'),fs=require('fs'),path=require('path');
const mode=process.argv[2]||'clean',FPS=30,out=path.resolve(__dirname,'..'),tmp=process.argv[3]||'/tmp/frames';
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('file://'+__dirname+'/plates.html'+(mode==='guide'?'?guide=1':''));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
 const fonts=await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family));console.log('fonts',[...new Set(fonts)]);
 const D=await p.evaluate(()=>window.DUR);const names={p1:'P1-hook-before',p2:'P2-before-questions',p3:'P3-after-answers',p4:'P4-offer'};
 for(const s of Object.keys(D)){const d=`${tmp}/${mode}-${s}`;fs.rmSync(d,{recursive:true,force:true});fs.mkdirSync(d,{recursive:true});
  for(let i=0;i<D[s]*FPS;i++){await p.evaluate(([s,t])=>window.draw(s,t),[s,i/FPS]);await p.screenshot({path:`${d}/${String(i).padStart(4,'0')}.png`})}
  const f=`${mode==='guide'?tmp+'/g-'+s:out+'/'+names[s]}.mp4`;
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${d}/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 17 -movflags +faststart ${f}`);console.log(f)}
 if(mode==='guide'){fs.writeFileSync(tmp+'/l.txt',Object.keys(D).map(s=>`file '${tmp}/g-${s}.mp4'`).join('\n'));
  execSync(`ffmpeg -y -loglevel error -f concat -safe 0 -i ${tmp}/l.txt -c copy ${out}/GUIDE-animatic.mp4`)}
 await b.close()})();
