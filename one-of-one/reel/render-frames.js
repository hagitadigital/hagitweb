const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const out=process.argv[2];const b=await chromium.launch();
 const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('http://localhost:8765/one-of-one/reel/film.html',{waitUntil:'networkidle'});await p.evaluate(()=>pre());await p.waitForTimeout(600);
 fs.mkdirSync(out+'/s4',{recursive:true});fs.mkdirSync(out+'/s8',{recursive:true});
 for(let f=0;f<180;f++){await p.evaluate(f=>scene4(f),f);await p.waitForTimeout(f%12==0?120:15);await p.screenshot({path:`${out}/s4/${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}
 await p.evaluate(()=>{s4.style.display='none'});
 for(let f=0;f<90;f++){await p.evaluate(f=>scene8(f,90),f);await p.screenshot({path:`${out}/s8/${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92})}
 await p.evaluate(()=>{s8.style.display='none'});
 const O={o1:{big:'My mood.'},o2:{big:'My rules.',top:120},o3:{big:'My shirt.',top:1560,color:'#F4F1EA'},o5:{lab:'1/1 · BY NOA'},o6:{lab:'1/1 · BY DALIA'}};
 for(const k in O){await p.evaluate(o=>overlay(o),O[k]);await p.waitForTimeout(80);await p.screenshot({path:`${out}/${k}.png`,omitBackground:true})}
 await b.close();console.log('frames done')})();
