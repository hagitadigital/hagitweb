// node final.js <tmpdir>  -> ../SITES-PRESENTER-v2-9x16.mp4
// Plates in final mode (timed to the voice) + the avatar take on top: bottom half in scene 1, a circle after.
const {chromium}=require('playwright'),{execSync}=require('child_process'),fs=require('fs'),path=require('path');
const FPS=30,out=path.resolve(__dirname,'..'),tmp=process.argv[2]||'/tmp/final',take=out+'/take/avatar-take-01.mp4';
const sh=c=>execSync(c,{stdio:['ignore','ignore','inherit']});
(async()=>{fs.mkdirSync(tmp,{recursive:true});
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
 await p.goto('file://'+__dirname+'/plates.html?final=1');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1200);
 const D=await p.evaluate(()=>window.DUR),starts=[];let n=0;
 for(const s of Object.keys(D)){starts.push(n/FPS);const d=`${tmp}/f-${s}`;fs.rmSync(d,{recursive:true,force:true});fs.mkdirSync(d,{recursive:true});
  const N=Math.round(D[s]*FPS);n+=N;
  for(let i=0;i<N;i++){await p.evaluate(([s,t])=>window.draw(s,t),[s,i/FPS]);await p.screenshot({path:`${d}/${String(i).padStart(4,'0')}.png`})}
  sh(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${d}/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 14 ${tmp}/f-${s}.mp4`);
  if(s==='p4')sh(`ffmpeg -y -loglevel error -i ${tmp}/f-p4.mp4 -ss 4.3 -i ${out}/regard-after/landing-desktop.webm -filter_complex "[1:v]setpts=PTS/1.25,fps=${FPS},scale=1080:608[v];[0:v][v]overlay=0:400:shortest=1" -c:v libx264 -pix_fmt yuv420p -crf 14 ${tmp}/f-p4b.mp4`)}
 await b.close();
 fs.writeFileSync(tmp+'/fl.txt',Object.keys(D).map(s=>`file '${tmp}/f-${s==='p4'?'p4b':s}.mp4'`).join('\n'));
 sh(`ffmpeg -y -loglevel error -f concat -safe 0 -i ${tmp}/fl.txt -c copy ${tmp}/base.mp4`);
 const [t1,t2,t3,t4,t5,t6]=starts.map(x=>x.toFixed(3));console.log('scene starts',starts.map(x=>x.toFixed(2)).join(' '));
 // circle masks and copper rings
 sh(`python3 -I ${__dirname}/masks.py ${tmp}`);
 // the voice pauses while the frame lands on the model: the take holds (no picture, no sound) for the beat at the end of scene 4
 const CUT=25.03,BEAT=+(starts[4]-CUT).toFixed(3),tb=(CUT).toFixed(3);
 const circ=(d,i)=>`[c${i}]crop=520:520:124:90,scale=${d}:${d}[s${i}];[s${i}][${i+2}:v]alphamerge[m${i}]`;
 const fc=[`[1:v]fps=${FPS},split=2[va][vb]`,`[va]trim=0:${CUT},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=${BEAT}[va2]`,`[vb]trim=start=${CUT},setpts=PTS-STARTPTS[vb2]`,`[va2][vb2]concat=n=2:v=1:a=0,split=4[h][c0][c1][c2]`,
  `[1:a]asplit=2[aa][ab]`,`[aa]atrim=0:${CUT},asetpts=PTS-STARTPTS,apad=pad_dur=${BEAT}[aa2]`,`[ab]atrim=start=${CUT},asetpts=PTS-STARTPTS[ab2]`,`[aa2][ab2]concat=n=2:v=0:a=1[a]`,
  `[h]crop=720:553:0:130,scale=1080:830[half]`,circ(420,0),circ(300,1),circ(420,2),
  `[0:v][half]overlay=0:1090:enable='lt(t,${t2})'[v1]`,
  `[v1][m0]overlay=330:1130:enable='between(t,${t2},${tb})'[v2]`,`[v2][5:v]overlay=324:1124:enable='between(t,${t2},${tb})'[v3]`,
  `[v3][m1]overlay=390:1300:enable='between(t,${t5},${t6})'[v4]`,`[v4][6:v]overlay=384:1294:enable='between(t,${t5},${t6})'[v5]`,
  `[v5][m2]overlay=330:1130:enable='gte(t,${t6})'[v6]`,`[v6][7:v]overlay=324:1124:enable='gte(t,${t6})'[v]`].join(';');
 sh(`ffmpeg -y -loglevel error -i ${tmp}/base.mp4 -i ${take} -loop 1 -i ${tmp}/mask420.png -loop 1 -i ${tmp}/mask300.png -loop 1 -i ${tmp}/mask420.png -loop 1 -i ${tmp}/ring420.png -loop 1 -i ${tmp}/ring300.png -loop 1 -i ${tmp}/ring420.png -filter_complex "${fc}" -map "[v]" -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 18 -preset slow -c:a aac -b:a 192k -t ${(n/FPS).toFixed(3)} -movflags +faststart ${out}/SITES-PRESENTER-v2-9x16.mp4`);
 console.log('done')})();
