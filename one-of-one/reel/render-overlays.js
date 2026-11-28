const {chromium}=require('playwright');
(async()=>{const out=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
 await p.goto('http://localhost:8765/one-of-one/reel/film.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
 const O={o1:{big:'My mood.'},o2:{big:'My rules.',top:1600},o3:{big:'My shirt.',top:1560,color:'#F4F1EA'},o5:{lab:'1/1 · BY NOA',ltop:1730,color:'#F4F1EA'},o6:{lab:'1/1 · BY DALIA',ltop:1790}};
 for(const k in O){await p.evaluate(o=>overlay(o),O[k]);await p.waitForTimeout(80);await p.screenshot({path:`${out}/${k}.png`,omitBackground:true})}
 await b.close()})();
