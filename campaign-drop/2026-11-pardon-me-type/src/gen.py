#!/usr/bin/env python3
"""PARDON ME° type edit, v2 — builds reel.html. Every timing lives here, in seconds.
The presenter's polite outside gives way to the prints: word solid -> word filled with the collection print ->
the brand's oval window opens behind her onto the full print -> cut to the collection's product.
    python3 gen.py && node render.js 26.3 ../PARDON-ME-type-edit-9x16.mp4"""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
A = '../../../pardon-me/assets/'
head = (HERE / 'reel-v1.html').read_text().split('<div id="stage">')[0]
head = head.replace('background:var(--porc);color:var(--garden);border-radius:2px', 'background:var(--garden);color:var(--porc);border-radius:2px')
head = head.replace('</style>', '''.word b.pf{color:transparent!important;background-image:var(--pr);-webkit-background-clip:text;background-clip:text;-webkit-text-stroke:5px var(--st)}
.burst,.oval{position:absolute;inset:0;background:var(--pr) center/900px}
.oval{clip-path:ellipse(400px 610px at 50% 43%)}
.ovalring{position:absolute;inset:0;background:var(--garden);clip-path:ellipse(410px 620px at 50% 43%)}
.full{position:absolute;inset:0;background:var(--pr) center/760px}
.pname{position:absolute;left:0;right:0;top:96px;text-align:center;direction:ltr;white-space:nowrap;font:italic 500 88px/1 'Bodoni Moda',serif;animation:capin .3s ease-out both}
.notes{position:absolute;left:0;right:0;bottom:170px;text-align:center;direction:ltr;font:700 34px/1 'Bodoni Moda',serif;letter-spacing:.3em;text-transform:uppercase;animation:capin .3s ease-out both}
.line2{position:absolute;left:50px;right:50px;bottom:190px;text-align:center;direction:ltr}
.line2 b{display:inline-block;font:900 104px/1.05 'Bodoni Moda',serif;letter-spacing:-.01em;color:var(--porc);background:var(--garden);padding:16px 36px 22px;animation:capin .28s cubic-bezier(.16,.9,.2,1) both}
.line2 i{display:inline-block;margin-top:14px;font:italic 500 62px/1.1 'Bodoni Moda',serif;color:var(--garden);background:var(--lime);padding:10px 30px 14px;animation:capin .28s cubic-bezier(.16,.9,.2,1) both}
.boxed{display:inline-block;background:var(--berry);color:var(--porc);padding:6px 40px 20px}
</style>''').replace('animation:run 2.6s linear 11.4s both', 'animation:run 2.2s linear 13.8s both')

P = lambda n: f"var(--pr);--pr:url({A}print-{n}.webp)"   # helper for inline --pr
COL = [  # key, clip, first frame, backdrop, word, word colour, script, script colour/pos, caption, cap class, print, product, name, notes, product text colour
 ('hello', '02-hello', 70, 'var(--blue)', 'HELLO', 'var(--garden)', 'Well,', 'color:var(--berry);left:60px;top:150px', 'הבוקר שנכנס לחדר בלי לדפוק.', '', 'well-hello', 'Well, Hello.', 'Citrus · Blossom · Green Leaves', 'var(--garden)'),
 ('business', '03-business', 28, 'var(--garden)', 'BUSINESS', 'var(--lime)', 'None of your', 'color:var(--porc);left:60px;top:140px;font-size:120px', 'הערב שלא מספרים עליו.', '', 'none-of-your-business', 'None of Your Business.', 'Fig · Amber · Wood', 'var(--porc)'),
 ('high', '04-high', 22, 'var(--petal)', 'HIGH', 'var(--berry)', 'Maintenance.', 'color:var(--garden);left:300px;top:150px;font-size:120px', 'Worth it. Obviously.', ' en', 'high-maintenance', 'High Maintenance.', 'Rose · Musk · Vanilla', 'var(--berry)'),
 ('bad', '05-bad', 12, 'var(--berry)', 'BAD', 'var(--petal)', 'Influence.', 'color:var(--lime);left:420px;top:150px;font-size:130px', 'Smells like bad decisions. The good kind.', ' en" data-s="42', 'bad-influence', 'Bad Influence.', 'Berry · Pink Pepper · Blossom', 'var(--garden)'),
]
T0, PRES, PROD = 4.6, 1.7, 0.6
shots, cuts, html, phases = [], [], [], []
shots.append(dict(id='s1', t=[0, 4.6], src='01-hook', f0=30, f1=121, sp=.7, r=[0, 0, 1080, 1920], s=[1.12, 1.2], a=[538, 960], p=[540, 880]))
t = T0
for i, (k, clip, f0, bg, word, wc, script, sst, cap, capc, pr, name, notes, pc) in enumerate(COL):
    run = len(word) > 6
    wattr = f'id="run" data-w="2500" data-x="60" data-y="250" style="color:{wc};overflow:visible;--st:{wc};--pr:url({A}print-{pr}.webp)"' if run else \
            f'data-w="1040" data-x="20" data-y="250" style="color:{wc};--st:{wc};--pr:url({A}print-{pr}.webp)"'
    banim = 'animation:none' if run else f'animation-delay:{t+.02:.2f}s'
    html.append(f'''<div class="shot" id="c{i}" style="background:{bg}"><div class="mid">
  <div class="word" {wattr}><b style="{banim}">{word}</b></div>
  <div class="burst" style="--pr:url({A}print-{pr}.webp)"></div></div><img class="fg"><div class="top">
  <div class="script" style="{sst};animation-delay:{t+.2:.2f}s">{script}</div>
  <p class="cap{capc}" style="animation-delay:{t+.35:.2f}s"><span>{cap}</span></p></div></div>
<div class="shot" id="p{i}" style="background:{bg}"><img class="fg"><div class="top">
  <div class="pname" style="color:{pc};animation-delay:{t+PRES+.03:.2f}s">{name}</div>
  <div class="notes" style="color:{pc};animation-delay:{t+PRES+.1:.2f}s">{notes}</div></div></div>''')
    shots.append(dict(id=f'c{i}', t=[t, t + PRES], src=clip, f0=f0, f1=121, sp=1, r=[0, 0, 1080, 1920], s=[1.0, 1.05], a=[538, 1924], p=[540, 1920]))
    shots.append(dict(id=f'p{i}', t=[t + PRES, t + PRES + PROD], img=f'{A}{pr}.webp', r=[0, 0, 1080, 1920], s=[1.3, 1.37], a=[600, 750], p=[540, 960]))
    phases.append(dict(id=f'c{i}', t0=t, run=run))
    cuts += [t, t + PRES]
    t += PRES + PROD
SPLIT, TAKE, ADS, CLOSE = t, t + 2.2, t + 4.0, t + 6.7
OUT, DUR = CLOSE + 2.8, CLOSE + 5.8
shots += [
 dict(id='s6a', t=[SPLIT, TAKE], src='01-hook', f0=34, f1=121, sp=.6, r=[0, 0, 1080, 960], s=[1.05, 1.1], a=[538, 960], p=[540, 610]),
 dict(id='s6b', t=[SPLIT, TAKE], src='05-bad', f0=14, f1=121, sp=1, r=[0, 960, 1080, 960], s=[1.15, 1.1], a=[538, 960], p=[540, 430]),
 dict(id='s7', t=[TAKE, ADS], seq='reveal', f0=1, f1=202, sp=3.4, r=[0, 0, 1080, 1920], s=[1.8, 1.9], a=[440, 549], p=[540, 1080]),
 dict(id='a1', t=[ADS, ADS + .9], img=f'{A}ad-touch-yourself.webp', r=[0, 0, 1080, 1920], s=[1.3, 1.38], a=[600, 750], p=[540, 960]),
 dict(id='a2', t=[ADS + .9, ADS + 1.8], img=f'{A}ad-i-kept-it.webp', r=[0, 0, 1080, 1920], s=[1.38, 1.3], a=[600, 750], p=[540, 960]),
 dict(id='a3', t=[ADS + 1.8, CLOSE], img=f'{A}line.webp', r=[0, 0, 1080, 1920], s=[1.62, 1.62], a=[560, 597], a2=[1240, 597], p=[540, 960]),
 dict(id='s8', t=[CLOSE, DUR], src='01-hook', f0=62, f1=121, sp=.7, r=[0, 0, 1080, 1920], s=[1.0, 1.1], a=[538, 1924], p=[540, 1920]),
]
cuts += [SPLIT, TAKE, ADS, ADS + .9, ADS + 1.8, CLOSE]
PRINTS = [f'url({A}print-{n}.webp)' for n in ('high-maintenance', 'well-hello', 'bad-influence', 'none-of-your-business')]

def studio(o):
    return f'''<div class="st" id="intro">
  <div class="col" style="top:120px;gap:18px"><div class="k up" style="animation-delay:2.75s">BRAND WORLDS STUDIO · HAGIT ANTEBI</div>
    <div class="up" style="animation-delay:2.85s;font-size:100px;font-weight:500;line-height:1.05">עולם מותג <em style="font-family:'Cormorant Garamond',serif;font-style:italic;font-weight:400;color:#B8894A">29</em></div></div>
  <div class="col up" style="top:1500px;gap:14px;animation-delay:3.05s"><div style="font-size:64px;font-weight:600;line-height:1.15">עולם מותג קונספט</div>
    <div style="font-size:34px;line-height:1.5">מנומס מבחוץ.<br>לא מתנצל מבפנים.</div></div>
</div>
<div class="st" id="outro">
  <div class="col" style="top:110px;gap:16px"><div class="up" style="animation-delay:{o+.25:.2f}s;font-size:28px;font-weight:500;letter-spacing:.06em;color:#C4765A"><span dir="ltr">PARDON ME°</span> · עולם מותג 29</div>
    <div class="up" style="animation-delay:{o+.4:.2f}s;font-size:64px;font-weight:600;line-height:1.2">מנומס מבחוץ.<br><span style="color:#C4765A">לא מתנצל</span> מבפנים.</div></div>
  <div class="col up" style="top:1440px;gap:24px;animation-delay:{o+.9:.2f}s"><div style="font-size:46px;font-weight:500;line-height:1.3;color:#C4765A">מה המותג שלך מסתיר<br>מאחורי החזית המנומסת?</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:22px 56px;background:#6B563F;color:#FAF8F3;border-radius:12px"><span style="font-size:36px;font-weight:500">אבחון פער המותג</span><span style="font-size:22px;opacity:.8">30 דק׳ · בלי עלות</span></div>
    <div class="k" style="letter-spacing:.3em;color:#8B7355">HAGITANTEBI.CO.IL</div></div>
</div>
<div id="marks"><i style="top:377px;left:244px;border-top-width:2px;border-left-width:2px"></i><i style="top:377px;left:792px;border-top-width:2px;border-right-width:2px"></i><i style="top:1345px;left:244px;border-bottom-width:2px;border-left-width:2px"></i><i style="top:1345px;left:792px;border-bottom-width:2px;border-right-width:2px"></i></div>
<svg id="bline"><path id="bpath" d="M-60 1440 H1140"/></svg>
<div id="ball"><div class="halo"></div><div class="sph"></div></div>'''

body = f'''<div id="stage">
{studio(OUT)}
<div id="world">

<div class="shot" id="s1" style="background:var(--porc)"><div class="mid"><div class="ovalring"></div><div class="oval" id="hookoval"></div></div><img class="fg"><div class="top">
  <div class="hook"><p>המותג שלך<br><em>מנומס מדי?</em></p></div></div></div>

{chr(10).join(html)}

<div class="shot" id="s6a" style="background:var(--porc)"><div class="mid"><p class="big" style="top:50px;font-size:132px;color:var(--garden);animation-delay:{SPLIT+.1:.2f}s">Good manners.</p></div><img class="fg"></div>
<div class="shot" id="s6b" style="background:var(--berry)"><div class="mid"><div class="full" style="--pr:url({A}print-bad-influence.webp)"></div></div><img class="fg"><div class="top"><p class="big" style="bottom:60px;font-size:132px;animation-delay:{SPLIT+.7:.2f}s"><span class="boxed">Bad habits.</span></p></div></div>
<div id="band"><div>GOOD MANNERS<i>·</i>BAD HABITS<i>·</i>GOOD MANNERS<i>·</i>BAD HABITS<i>·</i>GOOD MANNERS<i>·</i>BAD HABITS</div></div>

<div class="shot" id="s7" style="background:var(--petal)"><img class="fg"><div class="top">
  <p class="big" style="top:150px;color:var(--berry);animation-delay:{TAKE+.05:.2f}s">TAKE<br>IT OFF.</p></div></div>
<div class="shot" id="a1"><img class="fg"><div class="top"><div class="line2"><b style="animation-delay:{ADS+.04:.2f}s">Touch yourself.</b><br><i style="animation-delay:{ADS+.3:.2f}s">It’s skincare.</i></div></div></div>
<div class="shot" id="a2"><img class="fg"><div class="top"><div class="line2"><b style="font-size:84px;animation-delay:{ADS+.94:.2f}s">I bought you something.</b><br><i style="animation-delay:{ADS+1.2:.2f}s">I kept it.</i></div></div></div>
<div class="shot" id="a3"><img class="fg"><div class="top"><div class="line2"><b style="animation-delay:{ADS+1.84:.2f}s">Clean hands.</b><br><i style="animation-delay:{ADS+2.1:.2f}s">Dirty mind.</i></div></div></div>

<div class="shot" id="s8" style="background:var(--porc)"><div class="mid">
  <div class="word ns" data-w="1040" data-x="20" data-y="60" style="color:var(--berry);--st:var(--berry)"><b style="font-size:420px;animation-delay:{CLOSE+.02:.2f}s">NOT</b></div>
  <div class="word ns" data-w="1040" data-x="20" data-y="400" style="color:var(--berry);--st:var(--berry)"><b style="font-size:420px;animation-delay:{CLOSE+.2:.2f}s">SORRY.</b></div></div><img class="fg"><div class="top">
  <div class="end"><span style="animation-delay:{CLOSE+1.1:.2f}s">מבפנים, אף פעם לא מתנצלים.</span></div></div></div>

<div id="tag">PARDON ME</div>
<div id="flash"></div>
<svg id="grain" width="1080" height="1920"><filter id="n"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="1"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1920" filter="url(#n)"/></svg>
</div><!-- /world -->
</div>
<script>
const FPS=30, SHOTS={json.dumps(shots)}, CUTS={json.dumps(cuts)}, PH={json.dumps(phases)}, PRINTS={json.dumps(PRINTS)};
const SPLIT={SPLIT}, TAKE={TAKE}, CLOSE={CLOSE}, OUT={OUT};
const pad=n=>String(n).padStart(3,'0');
const url=(s,f)=>s.img?s.img:s.seq?`frames/${{s.seq}}/b_${{pad(f)}}.jpg`:`frames/${{s.src}}/f_${{pad(f)}}.webp`;
for(const s of SHOTS){{const el=document.getElementById(s.id);s.el=el;s.fg=el.querySelector('img.fg');
  Object.assign(el.style,{{left:s.r[0]+'px',top:s.r[1]+'px',width:s.r[2]+'px',height:s.r[3]+'px'}});}}
function fit(){{document.querySelectorAll('.word').forEach(w=>{{const b=w.firstElementChild;const k=+w.dataset.w/b.offsetWidth;
  w.dataset.k=k;w.style.transform=`translate(${{w.dataset.x}}px,${{w.dataset.y}}px) scale(${{k}},1)`;b.style.backgroundSize=`${{620/k}}px 620px`;}});
  document.querySelectorAll('[data-s]').forEach(e=>e.style.fontSize=e.dataset.s+'px');}}
const cl=x=>Math.min(1,Math.max(0,x)), ease=x=>1-Math.pow(1-x,3), io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
async function put(img,u){{if(!img||img.dataset.u===u)return;img.dataset.u=u;img.src=u;try{{await img.decode()}}catch(e){{}}}}
window.seek=async function(t){{
  const jobs=[];
  for(const s of SHOTS){{const on=t>=s.t[0]-1e-6&&t<s.t[1]-1e-6;s.el.style.visibility=on?'visible':'hidden';if(!on)continue;
    const n=Math.round((t-s.t[0])*FPS), f=s.img?0:Math.min(s.f1,s.f0+Math.round(n*s.sp)), p=(t-s.t[0])/(s.t[1]-s.t[0]);
    const punch=1+.04*Math.pow(Math.max(0,1-n/7),2), k=(s.s[0]+(s.s[1]-s.s[0])*p)*punch;
    const ax=s.a2?s.a[0]+(s.a2[0]-s.a[0])*p:s.a[0];
    s.fg.style.transform=`translate(${{s.p[0]-ax*k}}px,${{s.p[1]-s.a[1]*k}}px) scale(${{k}})`;
    jobs.push(put(s.fg,url(s,f)));
  }}
  // each collection shot: solid word -> print inside the letters -> the oval window opens onto the full print
  for(const ph of PH){{const el=document.getElementById(ph.id), d=t-ph.t0; if(d<0||d>1.75)continue;
    const w=el.querySelector('.word'), b=w.firstElementChild; b.classList.toggle('pf',d>=.55);
    const q=ease(cl((d-1.15)/.4)), rx=q*1250; el.querySelector('.burst').style.clipPath=`ellipse(${{rx}}px ${{rx*1.5}}px at 50% 40%)`;
    el.querySelector('.burst').style.backgroundPosition=`${{540+d*40}}px ${{d*-30}}px`;
    el.querySelector('.script').style.opacity=1-cl((d-1.15)/.15);
    const pop=d>=.55?1+.05*Math.pow(Math.max(0,1-(d-.55)*FPS/6),2):1;
    if(ph.run){{const qq=cl(d/1.7); w.style.transform=`translate(${{60-(2500-1000)*(qq*.9+.1*ease(qq))}}px,250px) scale(${{w.dataset.k}},1)`;}}
    else w.style.transform=`translate(${{w.dataset.x}}px,${{w.dataset.y}}px) scale(${{w.dataset.k*pop}},${{pop}})`;
  }}
  // hook: the window behind her shows a different print on every beat
  document.getElementById('hookoval').style.setProperty('--pr',PRINTS[Math.floor(t/.65)%4]);
  document.getElementById('hookoval').style.backgroundPosition=`${{t*30}}px ${{t*-20}}px`;
  // close: NOT SORRY fills with the prints, one per beat
  const dc=t-CLOSE; document.querySelectorAll('.ns').forEach(w=>{{const b=w.firstElementChild;b.classList.toggle('pf',dc>=.7);
    w.style.setProperty('--pr',PRINTS[Math.max(0,Math.floor((dc-.7)/.42))%4]);}});
  document.getElementById('band').style.visibility=(t>=SPLIT&&t<TAKE)?'visible':'hidden';
  document.getElementById('tag').style.visibility=(t>=4.6)?'hidden':'visible';
  let fl=0;for(const c of CUTS){{const n=Math.round((t-c)*FPS);if(n>=0&&n<3)fl=[.3,.14,.05][n];}}
  document.getElementById('flash').style.opacity=fl;
  document.getElementById('turb').setAttribute('seed',1+Math.round(t*FPS)%97);
  const shrink=io(cl((t-2.6)/.4))-io(cl((t-4.15)/.45))+io(cl((t-OUT)/.45));
  document.getElementById('world').style.transform=`scale(${{1-.5*shrink}})`;
  document.getElementById('intro').style.opacity=cl((t-2.7)/.25)-cl((t-4.1)/.2);
  document.getElementById('outro').style.opacity=cl((t-OUT-.15)/.3);
  document.getElementById('marks').style.opacity=Math.max(cl((t-2.95)/.2)-cl((t-4.1)/.15),cl((t-OUT-.4)/.25));
  document.querySelector('.hook').style.opacity=1-cl((t-2.45)/.2);
  const bq=cl((t-2.8)/1.3), L=1200, bx=1140-L*bq, bo=cl((t-2.8)/.1)-cl((t-4.1)/.12);
  const bp=document.getElementById('bpath');bp.style.strokeDasharray=L;bp.style.strokeDashoffset=-(L-L*bq);bp.style.opacity=bo;
  const ball=document.getElementById('ball');ball.style.transform=`translate(${{bx-52}}px,${{1440-52}}px)`;ball.style.opacity=bo;
  document.getAnimations().forEach(a=>{{a.currentTime=t*1000}});
  await Promise.all(jobs);
}};
window.ready=(async()=>{{await document.fonts.ready;fit();document.getAnimations().forEach(a=>a.pause());await seek(0);}})();
</script></body></html>
'''
(HERE / 'reel.html').write_text(head + body)
print('DUR', DUR, 'SPLIT', SPLIT, 'TAKE', TAKE, 'ADS', ADS, 'CLOSE', CLOSE, 'OUT', OUT)
