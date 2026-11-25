#!/usr/bin/env python3
"""TRAME° type edit — a 1950s salon show. Builds reel.html; every timing lives here, in seconds.
    python3 prep.py && python3 gen.py && node render.js 24.6 ../TRAME-type-edit-9x16.mp4"""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
A = '../../../trame/assets/'
LOOKS = [  # clip, first file, word, word colour, sky colour above the frame, still, caption
 ('form', 22, 'NOCTURNE', '#EDE6D8', '#0b0b0f', 'coll-nocturne', 'שחור אדריכלי · קווים שנחתכים בחושך'),
 ('movement', 22, 'ÉCLAT', '#8C2438', '#c9b9a2', 'coll-eclat', 'אור שנתפר למשי'),
 ('emotion', 150, 'ROUGE', '#EDE6D8', '#1a0608', 'coll-rouge', 'הזיכרון לובש בורדו'),
 ('future', 22, 'FUTURE', '#8C2438', '#a9adb6', 'coll-future', 'ירושה מהעתיד'),
]
WALK, STILL = 1.6, 0.5
shots = [dict(id='s1', t=[0, 4.6], seq='emotion', cut=1, f0=1, f1=241, sp=.8, r=[0, 0, 1080, 1920], s=[1.42, 1.56], a=[410, 1080], p=[540, 1920])]
t = 4.6
AT = t
for i, (f0, f1) in enumerate([(10, 60), (96, 150), (190, 250)]):
    shots.append(dict(id=f'at{i}', t=[t, t + .8], seq='maison', f0=f0, f1=f1, sp=1, r=[0, 0, 1080, 1920], s=[1.82, 1.9], a=[960, 540], p=[540, 960]))
    t += .8
html, cuts, looks = [], [AT, AT + .8, AT + 1.6], []
for i, (clip, f0, word, wc, sky, still, cap) in enumerate(LOOKS):
    html.append(f'''<div class="shot look" id="l{i}" style="background:{sky}"><img class="bgm"><img class="bg"><div class="sky" style="background:linear-gradient(to bottom,{sky} 0,{sky} 24%,transparent 37%)"></div><div class="mid">
  <div class="word" data-w="1030" data-x="25" data-y="185" style="color:{wc}"><b style="animation-delay:{t+.02:.2f}s">{word}</b></div></div><img class="fg"><div class="top">
  <div class="card" style="animation-delay:{t+.25:.2f}s"><small>Passage</small><b>N<sup>o</sup> 0{i+1}</b></div>
  <p class="cap" style="animation-delay:{t+.4:.2f}s">{cap}</p></div></div>
<div class="shot" id="k{i}"><img class="fg"><div class="top"><div class="card big" style="animation-delay:{t+WALK+.03:.2f}s"><small>{word.title()}</small><b>N<sup>o</sup> 0{i+1}</b></div></div></div>''')
    shots.append(dict(id=f'l{i}', t=[t, t + WALK], seq=clip, cut=1, f0=f0, f1=f0 + 60, sp=1, r=[0, 0, 1080, 1920], s=[1.30, 1.37], a=[410, 1080], p=[540, 1920]))
    shots.append(dict(id=f'k{i}', t=[t + WALK, t + WALK + STILL], img=f'{A}{still}.webp', r=[0, 0, 1080, 1920], s=[1.74, 1.78], a=[450, 560], p=[540, 960]))
    looks.append(t); cuts += [t, t + WALK]; t += WALK + STILL
SPLIT, REV = t, t + 2.8
OUT, DUR = REV + 3.4, REV + 6.4
shots += [
 dict(id='sp1', t=[SPLIT, REV], img=f'{A}pair1-sketch.webp', r=[0, 0, 1080, 960], s=[1.04, 1.09], a=[700, 467], p=[540, 575]),
 dict(id='sp2', t=[SPLIT, REV], img=f'{A}pair1-dress.webp', r=[0, 960, 1080, 960], s=[1.14, 1.08], a=[700, 467], p=[540, 480]),
 dict(id='rv', t=[REV, DUR], img=f'{A}build-8-reveal.webp', r=[0, 0, 1080, 1920], s=[1.22, 1.36], a=[496, 793], p=[540, 960]),
]
cuts += [SPLIT, REV]
# bordeaux thread: y, start, draw duration, end
threads = [dict(y=1246, t0=1.0, d=.9, t1=2.6), dict(y=1580, t0=AT + .1, d=.9, t1=AT + 2.4), dict(y=960, t0=SPLIT, d=.7, t1=REV), dict(y=1330, t0=REV + .9, d=1.0, t1=DUR)]

css = '''
:root{--bord:#8C2438;--bord2:#5E1624;--ivory:#EDE6D8;--char:#14110D;--bronze:#9C7A55}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#FAF8F3}
#stage{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;background:#FAF8F3}
#world{position:absolute;inset:0;overflow:hidden;transform-origin:50% 46%;background:#0b0806}
#gate{position:absolute;inset:0}
#grade{position:absolute;inset:0}
.shot{position:absolute;overflow:hidden;visibility:hidden;background:#0b0806}
.shot img{position:absolute;left:0;top:0;transform-origin:0 0;display:block}
.sky{position:absolute;inset:0}
.mid,.top{position:absolute;inset:0}
.word{position:absolute;left:0;top:0;direction:ltr;white-space:nowrap;overflow:hidden;transform-origin:0 0}
.word b{display:block;font:500 520px/0.92 'Bodoni Moda',serif;letter-spacing:-.01em;padding:.13em .03em 0;animation:rise .5s cubic-bezier(.16,.9,.2,1) both}
@keyframes rise{from{transform:translateY(104%)}to{transform:none}}
@keyframes capin{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
@keyframes pop{from{opacity:0;transform:rotate(-5deg) translateY(50px) scale(.9)}to{opacity:1;transform:rotate(-5deg)}}
.card{position:absolute;left:64px;bottom:330px;direction:ltr;text-align:center;background:var(--ivory);color:var(--char);padding:22px 34px 20px;transform:rotate(-5deg);
  outline:2px dashed var(--bord);outline-offset:-10px;box-shadow:0 10px 30px rgba(0,0,0,.45);animation:pop .35s cubic-bezier(.2,1.3,.3,1) both}
.card small{display:block;font:italic 500 30px/1 'Cormorant Garamond',serif;letter-spacing:.04em;color:var(--bord)}
.card b{display:block;font:500 84px/1 'Bodoni Moda',serif;margin-top:6px}.card sup{font-size:.5em;vertical-align:.7em;text-decoration:underline}
.card.big{left:50%;bottom:210px;margin-left:-170px;width:340px}.card.big small{font-size:40px}.card.big b{font-size:104px}
.cap{position:absolute;left:60px;right:60px;bottom:170px;text-align:center;font:500 54px/1.3 'Frank Ruhl Libre',serif;color:var(--ivory);text-shadow:0 2px 26px rgba(0,0,0,.95),0 0 8px rgba(0,0,0,.7);animation:capin .5s ease-out both}
.hook{position:absolute;left:0;right:0;top:1300px;text-align:center;color:var(--ivory);text-shadow:0 2px 40px rgba(0,0,0,.95),0 0 12px rgba(0,0,0,.8)}
.hook .l1{font:400 72px/1.2 'Frank Ruhl Libre',serif}.hook .l2{font:500 108px/1.15 'Frank Ruhl Libre',serif;margin-top:8px}
#tag{position:absolute;left:0;right:0;top:92px;text-align:center;direction:ltr;font:500 54px/1 'Bodoni Moda',serif;letter-spacing:.3em;color:var(--ivory);text-shadow:0 2px 20px rgba(0,0,0,.8)}
#tag small{display:block;font:italic 400 28px/1 'Cormorant Garamond',serif;letter-spacing:.08em;margin-top:12px;opacity:.85}
.en{position:absolute;left:60px;right:60px;text-align:center;direction:ltr;color:var(--ivory);text-shadow:0 2px 30px rgba(0,0,0,.95),0 0 10px rgba(0,0,0,.7)}
.en.it{font:italic 500 78px/1.15 'Cormorant Garamond',serif}
.en.bd{font:500 128px/1.02 'Bodoni Moda',serif;letter-spacing:-.01em}
.sp{position:absolute;left:0;right:0;text-align:center;font:500 80px/1.1 'Frank Ruhl Libre',serif;animation:capin .4s ease-out both}
#threads{position:absolute;inset:0;width:1080px;height:1920px;z-index:8}
#threads path{fill:none;stroke:var(--bord);stroke-width:5;stroke-linecap:round;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}
/* vintage: faded blacks, warm cast, gate, dust, grain */
#fade{position:absolute;inset:0;z-index:20;background:#3b2616;mix-blend-mode:lighten;opacity:.55;pointer-events:none}
#warm{position:absolute;inset:0;z-index:21;background:#f6d9a8;mix-blend-mode:multiply;opacity:.2;pointer-events:none}
#leak{position:absolute;inset:0;z-index:22;background:radial-gradient(60% 80% at 0% 40%,rgba(255,150,60,.95),rgba(255,90,40,.35) 45%,transparent 75%);mix-blend-mode:screen;opacity:0;pointer-events:none}
#dust{position:absolute;inset:0;z-index:23;pointer-events:none}
#grain{position:absolute;inset:0;z-index:24;pointer-events:none;opacity:.12;mix-blend-mode:overlay}
#flick{position:absolute;inset:0;z-index:25;background:#000;opacity:0;pointer-events:none}
#gatemask{position:absolute;inset:0;z-index:26;pointer-events:none;box-shadow:inset 0 0 0 16px #0b0806,inset 0 0 160px 30px rgba(8,5,3,.75);border-radius:0}
#gatemask::after{content:"";position:absolute;inset:16px;border-radius:44px;box-shadow:0 0 0 60px #0b0806}
/* studio wrapper: cream, ink, copper — fixed across the studio's reels */
.st{position:absolute;inset:0;font-family:'Heebo',sans-serif;color:#6B563F;opacity:0}
.st .col{position:absolute;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;text-align:center}
.st .k{font:500 22px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.32em;color:#C4765A;direction:ltr}
.up{animation:capin .5s ease-out both}
#marks{position:absolute;inset:0;opacity:0}
#marks i{position:absolute;width:44px;height:44px;border:0 solid #C4765A}
#bline{position:absolute;left:0;top:0;width:1080px;height:1920px}
#bline path{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round}
#ball{position:absolute;left:0;top:0;width:104px;height:104px}
#ball .halo{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}
#ball .sph{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}
'''
page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>TRAME° — type edit</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500&family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Cormorant+Garamond:ital,wght@0,500;1,400;1,500&family=Frank+Ruhl+Libre:wght@400;500&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<div id="stage">
<div class="st" id="intro">
  <div class="col" style="top:120px;gap:18px"><div class="k up" style="animation-delay:2.75s">BRAND WORLDS STUDIO · HAGIT ANTEBI</div>
    <div class="up" style="animation-delay:2.85s;font-size:100px;font-weight:500;line-height:1.05">עולם מותג <em style="font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:400;color:#B8894A">21</em></div></div>
  <div class="col up" style="top:1500px;gap:14px;animation-delay:3.05s"><div style="font-size:64px;font-weight:600;line-height:1.15">עולם מותג קונספט</div>
    <div style="font-size:34px;line-height:1.5">בית אופנה עילית שבו כל סילואטה<br>מתחילה בחוט אחד.</div></div>
</div>
<div class="st" id="outro">
  <div class="col" style="top:110px;gap:16px"><div class="up" style="animation-delay:{OUT+.25:.2f}s;font-size:28px;font-weight:500;letter-spacing:.06em;color:#C4765A"><span dir="ltr">TRAME°</span> · עולם מותג 21</div>
    <div class="up" style="animation-delay:{OUT+.4:.2f}s;font-size:64px;font-weight:600;line-height:1.2">הבטחה אחת. חוט אחד.<br>עולם שלם <span style="color:#C4765A">שנתפר סביבו</span>.</div></div>
  <div class="col up" style="top:1440px;gap:24px;animation-delay:{OUT+.9:.2f}s"><div style="font-size:46px;font-weight:500;line-height:1.3;color:#C4765A">ומה נתפר סביב<br>ההבטחה שלך?</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:22px 56px;background:#6B563F;color:#FAF8F3;border-radius:12px"><span style="font-size:36px;font-weight:500">אבחון פער המותג</span><span style="font-size:22px;opacity:.8">30 דק׳ · בלי עלות</span></div>
    <div class="k" style="letter-spacing:.3em;color:#8B7355">HAGITANTEBI.CO.IL</div></div>
</div>
<div id="marks"><i style="top:377px;left:244px;border-top-width:2px;border-left-width:2px"></i><i style="top:377px;left:792px;border-top-width:2px;border-right-width:2px"></i><i style="top:1345px;left:244px;border-bottom-width:2px;border-left-width:2px"></i><i style="top:1345px;left:792px;border-bottom-width:2px;border-right-width:2px"></i></div>
<svg id="bline"><path id="bpath" d="M-60 1440 H1140"/></svg>
<div id="ball"><div class="halo"></div><div class="sph"></div></div>

<div id="world"><div id="gate">
<div id="grade">
<div class="shot look" id="s1" style="background:#1a0608"><img class="bgm"><img class="bg"><div class="sky" style="background:linear-gradient(to bottom,#1a0608 0,#1a0608 15%,transparent 25%)"></div><img class="fg"></div>
<div class="shot" id="at0"><img class="fg"></div><div class="shot" id="at1"><img class="fg"></div><div class="shot" id="at2"><img class="fg"></div>
{chr(10).join(html)}
<div class="shot" id="sp1" style="background:#fbefe1"><img class="fg"><div class="top"><p class="sp" style="top:34px;font-size:68px;color:var(--char);animation-delay:{SPLIT+.15:.2f}s">פעם על נייר.</p></div></div>
<div class="shot" id="sp2"><img class="fg"><div class="top"><p class="sp" style="bottom:70px;color:var(--ivory);text-shadow:0 2px 26px rgba(0,0,0,.9);animation-delay:{SPLIT+1.1:.2f}s">פעם על גוף.</p></div></div>
<div class="shot" id="rv"><img class="fg"></div>
</div><!-- /grade -->
<svg id="threads"></svg>
<div class="top" style="z-index:9">
  <div class="hook" id="hook"><p class="l1">אנחנו לא תופרים שמלות.</p><p class="l2">אנחנו בונים <span style="color:#E7B9A0">תנועה.</span></p></div>
  <div id="tag">TRAME°<small>Maison de Couture</small></div>
  <p class="en it" id="atx" style="top:1350px;visibility:hidden">Every silhouette<br>begins with a thread.</p>
  <div id="rvx" style="visibility:hidden"><p class="en bd up" style="top:1050px;animation-delay:{REV+.25:.2f}s">Made once.</p><p class="en it up" style="top:1380px;font-size:92px;animation-delay:{REV+1.3:.2f}s">Remembered forever.</p></div>
</div>
<div id="fade"></div><div id="warm"></div><div id="leak"></div><canvas id="dust" width="1080" height="1920"></canvas>
<svg id="grain" width="1080" height="1920"><filter id="n"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="1"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1920" filter="url(#n)"/></svg>
<div id="flick"></div><div id="gatemask"></div>
</div></div><!-- /gate /world -->
</div>
<script>
const FPS=30, SHOTS={json.dumps(shots)}, CUTS={json.dumps(cuts)}, TH={json.dumps(threads)};
const AT={AT}, SPLIT={SPLIT}, REV={REV}, OUT={OUT};
const pad=n=>String(n).padStart(3,'0'), cl=x=>Math.min(1,Math.max(0,x)), ease=x=>1-Math.pow(1-x,3), io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
function rnd(seed){{let a=seed>>>0;return()=>{{a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}}}
for(const s of SHOTS){{const el=document.getElementById(s.id);s.el=el;s.fg=el.querySelector('img.fg');s.bg=el.querySelector('img.bg');s.bgm=el.querySelector('img.bgm');
  Object.assign(el.style,{{left:s.r[0]+'px',top:s.r[1]+'px',width:s.r[2]+'px',height:s.r[3]+'px'}});}}
const svg=document.getElementById('threads');
TH.forEach((h,i)=>{{let d=`M-20 ${{h.y}}`;for(let x=40;x<=1120;x+=60)d+=` Q${{x-30}} ${{h.y+((x/60)%2?9:-9)}} ${{x}} ${{h.y}}`;
  const p=document.createElementNS('http://www.w3.org/2000/svg','path');p.setAttribute('d',d);svg.appendChild(p);h.el=p;h.len=p.getTotalLength();p.style.strokeDasharray=h.len;}});
function fit(){{document.querySelectorAll('.word').forEach(w=>{{const b=w.firstElementChild;const k=+w.dataset.w/b.offsetWidth;w.dataset.k=k;
  w.style.transform=`translate(${{w.dataset.x}}px,${{w.dataset.y}}px) scale(${{k}},1)`;}});}}
async function put(img,u){{if(!img||img.dataset.u===u)return;img.dataset.u=u;img.src=u;try{{await img.decode()}}catch(e){{}}}}
const dust=document.getElementById('dust').getContext('2d');
window.seek=async function(t){{
  const jobs=[], F=Math.round(t*FPS), R=rnd(F*7919+13);
  for(const s of SHOTS){{const on=t>=s.t[0]-1e-6&&t<s.t[1]-1e-6;s.el.style.visibility=on?'visible':'hidden';if(!on)continue;
    const n=Math.round((t-s.t[0])*FPS), f=s.img?0:Math.min(s.f1,s.f0+Math.round(n*s.sp)), p=(t-s.t[0])/(s.t[1]-s.t[0]);
    const punch=1+.035*Math.pow(Math.max(0,1-n/7),2), k=(s.s[0]+(s.s[1]-s.s[0])*p)*punch;
    const x=s.p[0]-s.a[0]*k, y=s.p[1]-s.a[1]*k, tr=`translate(${{x}}px,${{y}}px) scale(${{k}})`;
    if(s.cut){{s.bg.style.transform=tr;s.fg.style.transform=tr;s.bgm.style.transform=`translate(${{x}}px,${{y}}px) scale(${{k}},${{-k}})`;
      const b=`frames/${{s.seq}}/b_${{pad(f)}}.jpg`;jobs.push(put(s.bg,b),put(s.bgm,b),put(s.fg,`frames/${{s.seq}}/f_${{pad(f)}}.webp`));}}
    else{{s.fg.style.transform=tr;jobs.push(put(s.fg,s.img?s.img:`frames/${{s.seq}}/b_${{pad(f)}}.jpg`));}}
  }}
  // the hook starts in black and white; colour arrives with the thread
  const bw=1-io(cl((t-1.1)/.8));
  document.getElementById('grade').style.filter=`grayscale(${{bw}}) sepia(.22) saturate(.86) contrast(.96) brightness(1.03)`;
  for(const h of TH){{const q=ease(cl((t-h.t0)/h.d));h.el.style.strokeDashoffset=h.len*(1-q);h.el.style.opacity=(t>=h.t0&&t<h.t1)?1:0;}}
  document.getElementById('hook').style.opacity=1-cl((t-2.45)/.2);
  document.getElementById('tag').style.visibility=t<4.6?'visible':'hidden';
  const atx=document.getElementById('atx');atx.style.visibility=(t>=AT&&t<AT+2.4)?'visible':'hidden';atx.style.opacity=cl((t-AT-.05)/.3);
  document.getElementById('rvx').style.visibility=t>=REV?'visible':'hidden';
  // vintage: gate weave, flicker, light leak on the cuts, dust and scratches, grain
  document.getElementById('gate').style.transform=`translate(${{Math.sin(t*1.7)*1.2+Math.sin(t*4.1)*.5}}px,${{Math.sin(t*1.3+1)*1.6+Math.sin(t*3.3)*.6}}px)`;   // slow drift, no per-frame jitter
  document.getElementById('flick').style.opacity=0;
  let lk=0;for(const c of CUTS){{const n=Math.round((t-c)*FPS);if(n>=0&&n<5)lk=[.42,.34,.22,.12,.05][n];}}
  const leak=document.getElementById('leak');leak.style.opacity=lk;leak.style.transform=`scaleX(${{F%2?1:-1}})`;
  dust.clearRect(0,0,1080,1920);
  const nd=F%3?0:1+Math.floor(R()*3);for(let i=0;i<nd;i++){{const x=R()*1080,y=R()*1920,r=1+R()*3.2;dust.fillStyle=R()<.6?`rgba(20,12,8,${{.35+R()*.4}})`:`rgba(255,246,230,${{.3+R()*.4}})`;dust.beginPath();dust.ellipse(x,y,r,r*(.5+R()),R()*3,0,7);dust.fill();}}
  if(R()<.02){{dust.strokeStyle='rgba(20,12,8,.5)';dust.lineWidth=1.4;dust.beginPath();const x=R()*1080,y=R()*1920;dust.moveTo(x,y);dust.bezierCurveTo(x+30*R(),y+40,x-40*R(),y+90,x+20,y+140*R());dust.stroke();}}
  document.getElementById('turb').setAttribute('seed',1+F%97);
  const shrink=io(cl((t-2.6)/.4))-io(cl((t-4.15)/.45))+io(cl((t-OUT)/.45));
  document.getElementById('world').style.transform=`scale(${{1-.5*shrink}})`;
  document.getElementById('intro').style.opacity=cl((t-2.7)/.25)-cl((t-4.1)/.2);
  document.getElementById('outro').style.opacity=cl((t-OUT-.15)/.3);
  document.getElementById('marks').style.opacity=Math.max(cl((t-2.95)/.2)-cl((t-4.1)/.15),cl((t-OUT-.4)/.25));
  const bq=cl((t-2.8)/1.3), L=1200, bx=1140-L*bq, bo=cl((t-2.8)/.1)-cl((t-4.1)/.12);
  const bp=document.getElementById('bpath');bp.style.strokeDasharray=L;bp.style.strokeDashoffset=-(L-L*bq);bp.style.opacity=bo;
  const ball=document.getElementById('ball');ball.style.transform=`translate(${{bx-52}}px,${{1440-52}}px)`;ball.style.opacity=bo;
  document.getAnimations().forEach(a=>{{a.currentTime=t*1000}});
  await Promise.all(jobs);
}};
window.ready=(async()=>{{await document.fonts.ready;fit();document.getAnimations().forEach(a=>a.pause());await seek(0);}})();
</script></body></html>
'''
(HERE / 'reel.html').write_text(page)
print('AT', AT, 'looks', looks, 'SPLIT', SPLIT, 'REV', REV, 'OUT', OUT, 'DUR', DUR)
