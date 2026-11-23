const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const n of ['personal','business']){const p=await b.newPage({viewport:{width:1640,height:924},deviceScaleFactor:1.25});
await p.goto('file://'+__dirname+'/'+n+'.html',{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
console.log(n,await p.evaluate(()=>[...document.fonts].filter(f=>f.status=='loaded').length));
await p.screenshot({path:__dirname+'/../fb-cover-'+n+'.png'});}
await b.close()})()
