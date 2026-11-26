#!/usr/bin/env python3
"""NADLAN · «המספר נשאר» — builds reel.html. Every timing lives here, in seconds; all cuts sit on a 120 BPM grid.
    python3 prep.py && python3 gen.py && node render.js 18 ../NADLAN-14-9x16.mp4"""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
R = '../../../'
HER, OLD, SITE, NEW, DOORS, TRUST, CTA, DUR = 0, 2.0, 4.5, 6.0, 8.0, 12.5, 15.0, 18.0
DOOR = [('01', 'הדיירים', '״לאן אני חוזר, מתי,<br>ומי מלווה אותי?״', 'sites/nadlan/s-steps.webp'),
        ('02', 'הרוכשים', '״מה אני קונה כאן,<br>חוץ מדירה?״', 'sites/nadlan/s-address.webp'),
        ('03', 'העירייה והשכונה', '״מה הרחוב מקבל מזה?״', 'sites/nadlan/s-annex.webp')]
css = '''
:root{--indigo:#1D1942;--nuit:#14122A;--violet:#382C66;--stone:#EFE6D8;--apricot:#F2A977;--peach:#F7C9A3;--rose:#A8718F;--cream:#FAF8F3;--ink:#2A201A;--copper:#C4765A}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--nuit)}
#stage{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;background:var(--nuit)}
.sc{position:absolute;inset:0;overflow:hidden;visibility:hidden}
@keyframes rise{from{opacity:0;transform:translateY(30%) scale(.95)}to{opacity:1;transform:none}}
@keyframes capin{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
.n14{position:absolute;left:0;right:0;text-align:center;direction:ltr;font:700 820px/0.86 'Bodoni Moda',serif;letter-spacing:-.04em;font-variant-numeric:lining-nums}
/* her */
#her img{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:50% 60%}
.box{position:absolute;left:50px;right:50px;text-align:center}
.box p{display:inline-block;font:500 76px/1.2 'Frank Ruhl Libre',serif;color:var(--stone);background:var(--indigo);padding:16px 40px 24px}
.box p em{font-style:normal;color:var(--apricot)}
/* the building */
#bld{background:#d9d6cf}
#sky{position:absolute;inset:0}
#scene{position:absolute;inset:0;transform-origin:50% 70%}
#scene img{position:absolute;left:0;top:0;width:1344px;height:752px;transform-origin:0 0;transform:translate(-348px,578px) scale(1.2)}
#wline{position:absolute;top:578px;width:5px;height:902px;background:var(--apricot);box-shadow:0 0 24px rgba(242,169,119,.9);opacity:0}
#panel{position:absolute;left:0;right:0;top:1480px;bottom:0;background:var(--indigo)}
#year{position:absolute;left:70px;top:58px;direction:ltr;font:500 150px/1 'Bodoni Moda',serif;color:var(--apricot);font-variant-numeric:lining-nums tabular-nums}
#plate{position:absolute;right:70px;top:64px;direction:ltr;font:600 30px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.3em;color:var(--stone);opacity:.8;text-align:right}
.line{position:absolute;left:60px;right:60px;top:238px;text-align:right;font:500 84px/1.15 'Frank Ruhl Libre',serif;color:var(--stone);visibility:hidden}
.line span{display:inline-block;animation:capin .4s cubic-bezier(.16,.9,.2,1) both}
/* doors */
.door{background:var(--indigo)}
.door .num{position:absolute;left:70px;top:120px;direction:ltr;font:500 300px/0.9 'Bodoni Moda',serif;color:var(--apricot);font-variant-numeric:lining-nums;animation:rise .4s cubic-bezier(.16,.9,.2,1) both}
.door .who{position:absolute;right:70px;top:230px;font:700 96px/1 'Frank Ruhl Libre',serif;color:var(--stone);animation:capin .4s ease-out both}
.door .k{position:absolute;right:74px;top:168px;direction:ltr;font:600 26px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.3em;color:var(--peach);opacity:.8}
.door .win{position:absolute;left:40px;top:470px;width:1000px;height:625px;border-radius:16px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.5),0 0 0 2px rgba(239,230,216,.25);animation:capin .45s ease-out both}
.door .win img{display:block;width:1000px;height:625px}
.door .q{position:absolute;left:70px;right:70px;top:1190px;text-align:center;font:500 92px/1.2 'Frank Ruhl Libre',serif;color:var(--stone);animation:capin .45s ease-out both}
.door .note{position:absolute;left:0;right:0;bottom:130px;text-align:center;font:400 34px/1.3 'Heebo',sans-serif;color:rgba(239,230,216,.6)}
/* trust */
#trust img{position:absolute;left:0;top:0;transform-origin:0 0}
#trust .shade{position:absolute;inset:0;background:linear-gradient(to top,rgba(20,18,42,.92) 0,rgba(20,18,42,.55) 38%,rgba(20,18,42,.1) 62%)}
#trust p{position:absolute;left:70px;right:70px;bottom:260px;text-align:right;font:500 96px/1.18 'Frank Ruhl Libre',serif;color:var(--stone)}
#trust p span{display:block;animation:capin .45s ease-out both}#trust p em{font-style:normal;color:var(--apricot);font-size:150px;font-weight:700;line-height:1.1}
/* cta */
#cta{background:var(--cream)}
.tag{position:absolute;left:0;right:0;text-align:center;direction:ltr;font:600 30px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.3em;color:var(--copper)}
.arch{position:absolute;left:270px;top:230px;width:540px;height:760px;border-radius:270px 270px 22px 22px;overflow:hidden;box-shadow:0 30px 70px rgba(62,40,24,.22);animation:capin .45s ease-out both}
.arch img{position:absolute;left:-50px;top:0;width:640px;height:800px;object-fit:cover}
.ctah{position:absolute;left:60px;right:60px;top:1060px;text-align:center;font:700 80px/1.15 'Frank Ruhl Libre',serif;color:var(--ink);animation:capin .45s ease-out both}
.ctab{position:absolute;left:110px;right:110px;top:1290px;text-align:center;font:700 64px/1.2 'Frank Ruhl Libre',serif;color:var(--cream);background:var(--indigo);padding:36px 30px 44px;border-radius:16px;animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.cnote{position:absolute;left:0;right:0;bottom:120px;text-align:center;font:400 30px/1.3 'Heebo',sans-serif;color:#786A5E}
#flash{position:absolute;inset:0;z-index:25;background:#fff;opacity:0;pointer-events:none}
#grain{position:absolute;inset:0;z-index:31;pointer-events:none;opacity:.09;mix-blend-mode:overlay}
'''
doors = ''.join(f'''<div class="sc door" data-show="{DOORS+i*1.5},{DOORS+(i+1)*1.5}"><div class="num" style="animation-delay:{DOORS+i*1.5+.02:.2f}s">{n}</div>
  <div class="k">THE SITE ANSWERS</div><div class="who" style="animation-delay:{DOORS+i*1.5+.08:.2f}s{';font-size:70px;top:244px' if len(who) > 9 else ''}">{who}</div>
  <div class="win" style="animation-delay:{DOORS+i*1.5+.05:.2f}s"><img src="{R}{img}"></div>
  <div class="q" style="animation-delay:{DOORS+i*1.5+.2:.2f}s">{q}</div><div class="note">RUE° הוא פרויקט קונספט של הסטודיו</div></div>''' for i, (n, who, q, img) in enumerate(DOOR))
page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>NADLAN — 14</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500&family=Plus+Jakarta+Sans:wght@600&family=Bodoni+Moda:opsz,wght@6..96,500;6..96,700&family=Frank+Ruhl+Libre:wght@500;700&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<div id="stage">
<div class="sc" id="her" data-show="{HER},{OLD}"><img id="hb"><div class="n14" style="top:210px;color:var(--violet)">14</div><img id="hf">
  <div class="box" style="top:56px"><p>לפרויקט אין שם.<br><em>יש לו כתובת.</em></p></div></div>
<div class="sc" id="bld" data-show="{OLD},{DOORS}"><div id="sky"></div><div class="n14" id="n14" style="top:330px">14</div>
  <div id="scene"><img id="i0" src="frames/bld/old.webp"><img id="i1" src="frames/bld/site.webp"><img id="i2" src="frames/bld/new.webp"><div id="wline"></div></div>
  <div id="panel"><div id="year">1961</div><div id="plate">SAME ADDRESS<br><br>SAME CAMERA</div>
    <div class="line" data-show="{OLD},{NEW}"><span style="animation-delay:{OLD+.15:.2f}s">הבניין מתחלף.</span></div>
    <div class="line" data-show="{NEW},{DOORS}"><span style="animation-delay:{NEW+.1:.2f}s;color:var(--apricot)">המספר נשאר.</span></div></div></div>
{doors}
<div class="sc" id="trust" data-show="{TRUST},{CTA}"><img id="tr" src="{R}rue/assets/16-flagship.webp"><div class="shade"></div>
  <p><span style="animation-delay:{TRUST+.1:.2f}s">בהתחדשות עירונית,</span><span style="animation-delay:{TRUST+.35:.2f}s">לא מוכרים רק דירות.</span><span style="animation-delay:{TRUST+1.0:.2f}s"><em>בונים אמון.</em></span></p></div>
<div class="sc" id="cta" data-show="{CTA},{DUR}"><div class="tag" style="top:120px">HAGIT ANTEBI · BRAND WORLDS STUDIO</div>
  <div class="arch" style="animation-delay:{CTA+.02:.2f}s"><img src="{R}sites/a/hagit.webp"></div>
  <div class="ctah" style="animation-delay:{CTA+.25:.2f}s">אתר לחברה או לפרויקט,<br>שעונה לכל אחד מהם.</div>
  <div class="ctab" style="animation-delay:{CTA+.5:.2f}s">לתאם שיחה על הפרויקט</div>
  <div class="tag" style="bottom:190px;letter-spacing:.2em;color:#8B7355">HAGITANTEBI.CO.IL/SITES/NADLAN</div></div>
<div id="flash"></div>
<svg id="grain" width="1080" height="1920"><filter id="n"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="1"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1920" filter="url(#n)"/></svg>
</div>
<script>
const FPS=30, OLD={OLD}, SITE={SITE}, NEW={NEW}, DOORS={DOORS}, TRUST={TRUST}, CTA={CTA}, CUTS={json.dumps([OLD, DOORS, DOORS + 1.5, DOORS + 3, TRUST, CTA])};
const pad=n=>String(n).padStart(3,'0'), cl=x=>Math.min(1,Math.max(0,x)), io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, mix=(a,b,k)=>a.map((v,i)=>Math.round(v+(b[i]-v)*k));
async function put(img,u){{if(!img||img.dataset.u===u)return;img.dataset.u=u;img.src=u;try{{await img.decode()}}catch(e){{}}}}
const shows=[...document.querySelectorAll('[data-show]')].map(e=>[e,...e.dataset.show.split(',').map(Number)]);
window.seek=async function(t){{
  const F=Math.round(t*FPS), jobs=[];
  for(const [e,a,b] of shows) e.style.visibility=(t>=a-1e-6&&t<b-1e-6)?'visible':'hidden';
  if(t<OLD-1e-6){{const n=Math.min(59,F);jobs.push(put(document.getElementById('hb'),`frames/her/b_${{pad(n)}}.jpg`),put(document.getElementById('hf'),`frames/her/f_${{pad(n)}}.webp`));
    const k=1+.03*Math.pow(Math.max(0,1-F/7),2)+.012*t;for(const id of ['hb','hf'])document.getElementById(id).style.transform=`scale(${{k}})`;}}
  // the building: old (black and white) -> site -> new, wiped right to left; the 14 never moves
  const w1=io(cl((t-SITE)/.55)), w2=io(cl((t-NEW)/.55)), col=io(cl((t-SITE+.1)/.9));
  document.getElementById('i0').style.filter=`grayscale(${{1-col*.2}}) contrast(1.05)`;
  document.getElementById('i1').style.clipPath=`inset(0 0 0 ${{(1-w1)*100}}%)`;
  document.getElementById('i2').style.clipPath=`inset(0 0 0 ${{(1-w2)*100}}%)`;
  const wl=document.getElementById('wline'), wq=(t>=NEW)?w2:w1, wa=(t>=NEW)?cl((t-NEW)/.05)-cl((t-NEW-.5)/.1):cl((t-SITE)/.05)-cl((t-SITE-.5)/.1);
  wl.style.left=(-348+1344*1.2*(1-wq))+'px'; wl.style.opacity=wa;
  const skyA=mix(mix([201,200,196],[146,178,212],w1),[122,150,205],w2), skyB=mix(mix([233,230,223],[226,234,238],w1),[247,201,163],w2);
  document.getElementById('sky').style.background=`linear-gradient(to bottom,rgb(${{skyA}}) 0,rgb(${{skyB}}) 72%)`;
  document.getElementById('n14').style.color=`rgb(${{mix(mix([58,56,60],[29,25,66],w1),[29,25,66],w2)}})`;
  document.getElementById('scene').style.transform=`scale(${{1+.035*cl((t-OLD)/(DOORS-OLD))}})`;
  const yq=io(cl((t-SITE)/(NEW+.55-SITE)));document.getElementById('year').textContent=Math.round(1961+68*yq);
  if(t>=TRUST&&t<CTA){{const k=1.6+.07*(t-TRUST)/(CTA-TRUST);document.getElementById('tr').style.transform=`translate(${{540-600*k}}px,${{880-750*k}}px) scale(${{k}})`;}}
  let fl=0;for(const c of CUTS){{const n=Math.round((t-c)*FPS);if(n>=0&&n<3)fl=[.26,.12,.05][n];}}
  document.getElementById('flash').style.opacity=fl;
  document.getElementById('turb').setAttribute('seed',1+F%97);
  document.getAnimations().forEach(a=>{{a.currentTime=t*1000}});
  await Promise.all(jobs);
}};
window.ready=(async()=>{{await document.fonts.ready;await Promise.all([...document.images].filter(i=>i.src).map(i=>i.decode().catch(()=>{{}})));document.getAnimations().forEach(a=>a.pause());await seek(0);}})();
</script></body></html>
'''
(HERE / 'reel.html').write_text(page)
print('DUR', DUR)
