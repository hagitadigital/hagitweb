#!/usr/bin/env python3
"""SITES · Hagit at the laptop — typographic edit of her own take. Builds schedule.json (for prep.py) and reel.html.
    python3 gen.py && python3 prep.py && node render.js 16.5 ../SITES-HAGIT-9x16.mp4
Every timing lives here, in seconds. Her shots are pre-composited per output frame by prep.py (screen replaced, figure cut out)."""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
FPS = 30
# her shots: id, start, end, first take frame, take speed (take is 24fps; 1 = one take frame per output frame)
HER = [('hook', 0.0, 3.0, 292, .66), ('work', 3.0, 4.5, 30, 1), ('turn', 4.5, 9.0, 200, .667), ('hold', 12.0, 13.5, 352, .88)]   # the hook opens on the laptop held to camera: the sites are the first thing seen
# what plays on the laptop screen: start, end, site, second in the site recording where it starts
SCREEN = [(0.0, 1.5, 'oreva', 0.3), (1.5, 3.0, 'rue', 0.2), (4.5, 6.0, 'oreva', 2.0), (6.0, 7.5, 'mirvach', 3.6), (7.5, 9.0, 'rue', 2.0), (12.0, 13.5, 'mirvach', 6.0)]   # every cut sits on the music's beat grid (120 BPM)
SITES_T, CTA, DUR = 9.0, 13.5, 16.5
CARD = 1.0
OUT = DUR + 9   # no studio window here: the call to action gets a clean screen of its own
FULL = [('oreva', 0.5, 'עמוד נחיתה', 'קוסמטיקאית'), ('mirvach', 4.0, 'עמוד נחיתה', 'מטפלת רגשית'), ('rue', 0.4, 'אתר תדמית', 'יזמות נדל״ן')]
sched = []
for sid, t0, t1, f0, sp in HER:
    for n in range(round((t1 - t0) * FPS)):
        t = t0 + n / FPS; tf = min(392, f0 + round(n * sp)); scr = None
        for a, b, site, s0 in SCREEN:
            if a - 1e-6 <= t < b - 1e-6: scr = [site, round((s0 + (t - a)) * 30) + 1]
        sched.append(dict(out=round(t * FPS), take=tf, screen=scr))
full = []
for i, (site, s0, _, _) in enumerate(FULL):
    for n in range(round(CARD * FPS)): full.append(dict(out=round((SITES_T + i * CARD) * FPS) + n, site=site, f=round(s0 * 30) + n + 1))
(HERE / 'schedule.json').write_text(json.dumps(dict(her=sched, full=full)))

css = '''
:root{--cream:#FAF8F3;--beige:#F5F1E8;--ink:#2A201A;--deep:#4F372C;--copper:#C4765A;--copper2:#A45839;--line:#D4C9BC}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--cream)}
#stage{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;background:var(--cream)}
#world{position:absolute;inset:0;overflow:hidden;transform-origin:50% 46%;background:var(--beige)}
#her{position:absolute;inset:0;overflow:hidden}
#her img{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:50% 60%;display:block}
.mid,.top{position:absolute;inset:0}
.w{position:absolute;left:0;right:0;text-align:center;white-space:nowrap;visibility:hidden}
.w b{display:inline-block;animation:rise .42s cubic-bezier(.16,.9,.2,1) both}
.w.he b{font:900 440px/1 'Frank Ruhl Libre',serif;color:var(--copper2);letter-spacing:-.02em}
.w.num b{font:600 620px/0.9 'Cormorant Garamond',serif;color:var(--copper2);letter-spacing:-.03em;direction:ltr;font-variant-numeric:lining-nums}
@keyframes rise{from{opacity:0;transform:translateY(34%) scale(.94)}to{opacity:1;transform:none}}
@keyframes capin{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
.box{position:absolute;left:50px;right:50px;text-align:center;visibility:hidden}
.box p{display:inline-block;font:500 88px/1.2 'Frank Ruhl Libre',serif;color:var(--cream);background:var(--ink);padding:16px 40px 24px;animation:capin .32s cubic-bezier(.16,.9,.2,1) both}
.box p em{font-style:normal;color:#EFCDBF}
.box.sm p{font-size:72px}
.tag{position:absolute;left:0;right:0;top:70px;text-align:center;direction:ltr;font:600 30px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.3em;color:var(--deep)}
.card{position:absolute;inset:0;background:var(--cream);visibility:hidden}
.win{position:absolute;left:40px;top:330px;width:1000px;border-radius:18px;overflow:hidden;background:#fff;box-shadow:0 30px 80px rgba(62,40,24,.28),0 0 0 2px var(--line)}
.win .bar{height:54px;background:#EFE8DC;display:flex;align-items:center;gap:10px;padding:0 22px;direction:ltr}
.win .bar i{width:14px;height:14px;border-radius:50%;background:#D4C9BC}.win .bar i:first-child{background:var(--copper)}
.win img{display:block;width:1000px;height:625px}
.kind{position:absolute;left:0;right:0;top:1090px;text-align:center;font:900 190px/1 'Frank Ruhl Libre',serif;color:var(--ink);letter-spacing:-.02em;animation:rise .35s cubic-bezier(.16,.9,.2,1) both}
.who{position:absolute;left:0;right:0;top:1310px;text-align:center;font:500 84px/1.1 'Frank Ruhl Libre',serif;color:var(--copper2);animation:capin .35s ease-out both}
.idx{position:absolute;left:0;right:0;top:150px;text-align:center;direction:ltr;font:600 120px/1 'Cormorant Garamond',serif;font-variant-numeric:lining-nums;color:var(--copper);animation:capin .3s ease-out both}
.note{position:absolute;left:0;right:0;bottom:150px;text-align:center;font:400 38px/1.3 'Heebo',sans-serif;color:#786A5E}
.ctab{position:absolute;left:90px;right:90px;top:1130px;text-align:center;font:700 66px/1.2 'Frank Ruhl Libre',serif;color:var(--cream);background:var(--ink);padding:38px 30px 46px;border-radius:16px;animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.ctas{position:absolute;left:0;right:0;top:1370px;text-align:center;font:400 44px/1.3 'Heebo',sans-serif;color:#6B563F;animation:capin .45s ease-out both}
#flash{position:absolute;inset:0;z-index:25;background:#fff;opacity:0;pointer-events:none}
#grain{position:absolute;inset:0;z-index:31;pointer-events:none;opacity:.08;mix-blend-mode:overlay}
.st{position:absolute;inset:0;font-family:'Heebo',sans-serif;color:#6B563F;opacity:0}
.st .col{position:absolute;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;text-align:center}
.st .k{font:500 22px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.32em;color:#C4765A;direction:ltr}
.up{animation:capin .5s ease-out both}
#marks{position:absolute;inset:0;opacity:0}
#marks i{position:absolute;width:44px;height:44px;border:0 solid #C4765A}
'''
def W(cls, top, text, t0, t1, extra=''):
    anim = 'animation:none' if t0 == 0 else f'animation-delay:{t0+.02:.2f}s'
    return f'<div class="w {cls}" data-show="{t0},{t1}" style="top:{top}px"><b style="{anim}{extra}">{text}</b></div>'
def B(top, html, t0, t1, cls=''):
    anim = 'animation:none' if t0 == 0 else f'animation-delay:{t0+.05:.2f}s'
    return f'<div class="box {cls}" data-show="{t0},{t1}" style="top:{top}px"><p style="{anim}">{html}</p></div>'
mid = [W('he', 300, 'יפה.', 0, 1.5, ';font-size:400px'), W('he', 320, 'מדויק.', 1.5, 3.0, ';font-size:340px'), W('num', 60, '5', 3.0, 4.5),
       W('num', 150, '01', 4.5, 6.0), W('num', 150, '02', 6.0, 7.5), W('num', 150, '03', 7.5, 9.0), W('he', 210, 'פניות.', 12.0, 13.5, ';font-size:340px')]
top = [B(56, 'אתר יפה מושך את העין.<br><em>אתר מדויק מניע לפעולה.</em>', 0, 3.0, 'sm'), B(1420, 'לקוח צריך להבין<br><em>תוך 5 שניות:</em>', 3.0, 4.5),
       B(60, 'מה אתם מציעים', 4.5, 6.0, 'sm'), B(60, 'למה דווקא אתם', 6.0, 7.5, 'sm'), B(60, 'מה הצעד הבא', 7.5, 9.0, 'sm'),
       B(60, 'אתר ברור <em>מביא פניות.</em>', 12.0, 13.5, 'sm')]
cards = ''.join(f'''<div class="card" data-show="{SITES_T+i*CARD},{SITES_T+(i+1)*CARD}"><div class="idx" style="animation-delay:{SITES_T+i*CARD+.02:.2f}s">0{i+1} / 03</div>
  <div class="win"><div class="bar"><i></i><i></i><i></i></div><img id="full{i}"></div>
  <div class="kind" style="animation-delay:{SITES_T+i*CARD+.03:.2f}s">{k}</div><div class="who" style="animation-delay:{SITES_T+i*CARD+.12:.2f}s">{who}</div>
  <div class="note">שלושה פרויקטי קונספט של הסטודיו</div></div>''' for i, (_, _, k, who) in enumerate(FULL))
page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>SITES — Hagit</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500;600&family=Cormorant+Garamond:ital,wght@0,600;1,500&family=Frank+Ruhl+Libre:wght@400;500;700;900&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<div id="stage">
<div class="st" id="outro">
  <div class="col" style="top:110px;gap:16px"><div class="k up" style="animation-delay:{OUT+.25:.2f}s">HAGIT ANTEBI · BRAND WORLDS STUDIO</div>
    <div class="up" style="animation-delay:{OUT+.4:.2f}s;font-family:'Frank Ruhl Libre',serif;font-size:84px;font-weight:700;line-height:1.15;color:#2A201A">יפה זה לא מספיק.<br><span style="color:#A45839">אתר ברור מביא פניות.</span></div></div>
  <div class="col up" style="top:1420px;gap:22px;animation-delay:{OUT+.9:.2f}s"><div style="font-size:40px;font-weight:500;line-height:1.35;color:#6B563F">עמוד נחיתה · אתר תדמית · שדרוג אתר</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:24px 56px;background:#2A201A;color:#FAF8F3;border-radius:12px"><span style="font-size:40px;font-weight:500">לקבל 3 נקודות על האתר שלי</span><span style="font-size:24px;opacity:.8">שיחת התאמה קצרה · בלי התחייבות</span></div>
    <div class="k" style="letter-spacing:.3em;color:#8B7355">HAGITANTEBI.CO.IL/SITES</div></div>
</div>
<div id="marks"><i style="top:377px;left:244px;border-top-width:2px;border-left-width:2px"></i><i style="top:377px;left:792px;border-top-width:2px;border-right-width:2px"></i><i style="top:1345px;left:244px;border-bottom-width:2px;border-left-width:2px"></i><i style="top:1345px;left:792px;border-bottom-width:2px;border-right-width:2px"></i></div>
<div id="world">
  <div id="her"><img id="bg"><div class="mid">{''.join(mid)}</div><img id="fg"><div class="top">{''.join(top)}<div class="tag" id="tag">SITES · HAGIT ANTEBI</div></div></div>
  {cards}
  <div class="card" data-show="{CTA},{DUR}">
    <div class="tag" style="top:150px;color:#C4765A">HAGIT ANTEBI · BRAND WORLDS STUDIO</div>
    <div class="w num" style="top:330px;visibility:inherit"><b style="font-size:760px;animation-delay:{CTA+.05:.2f}s">3</b></div>
    <div class="ctab" style="animation-delay:{CTA+.45:.2f}s">לקבל 3 נקודות על האתר שלי</div>
    <div class="ctas" style="animation-delay:{CTA+.75:.2f}s">שיחת התאמה קצרה · בלי התחייבות</div>
    <div class="tag" style="top:auto;bottom:170px;letter-spacing:.24em">HAGITANTEBI.CO.IL/SITES</div>
  </div>
  <div id="flash"></div>
  <svg id="grain" width="1080" height="1920"><filter id="n"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="1"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1920" filter="url(#n)"/></svg>
</div>
</div>
<script>
const FPS=30, HER={json.dumps([[a, b] for _, a, b, _, _ in HER])}, OUT={OUT}, CUTS={json.dumps([1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.0, 11.0, 12.0, 13.5])}, FULL={json.dumps([[round((SITES_T + i * CARD) * FPS), FULL[i][0], round(FULL[i][1] * 30) + 1] for i in range(3)])};
const pad=(n,w=3)=>String(n).padStart(w,'0'), cl=x=>Math.min(1,Math.max(0,x)), io=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
async function put(img,u){{if(!img||img.dataset.u===u)return;img.dataset.u=u;img.src=u;try{{await img.decode()}}catch(e){{}}}}
const shows=[...document.querySelectorAll('[data-show]')].map(e=>[e,...e.dataset.show.split(',').map(Number)]);
window.seek=async function(t){{
  const F=Math.round(t*FPS), jobs=[];
  document.getElementById('tag').style.visibility=(t>=3.0&&t<4.5)?'visible':'hidden';
  for(const [e,a,b] of shows) e.style.visibility=(t>=a-1e-6&&t<b-1e-6)?'visible':'hidden';
  const on=HER.some(([a,b])=>t>=a-1e-6&&t<b-1e-6), her=document.getElementById('her'); her.style.visibility=on?'visible':'hidden';
  if(on){{jobs.push(put(document.getElementById('bg'),`frames/out/b_${{pad(F)}}.jpg`),put(document.getElementById('fg'),`frames/out/f_${{pad(F)}}.webp`));
    let since=1e9;for(const c of [0,...CUTS])if(t>=c-1e-6)since=Math.min(since,Math.round((t-c)*FPS));
    let c0=0;for(const c of CUTS)if(t>=c-1e-6)c0=c;
    const k=1+.03*Math.pow(Math.max(0,1-since/7),2)+.012*(t-c0);
    for(const id of ['bg','fg'])document.getElementById(id).style.transform=`scale(${{k}})`;}}
  FULL.forEach(([f0,site,s0],i)=>{{const n=F-f0;if(n>=0&&n<30)jobs.push(put(document.getElementById('full'+i),`frames/site/${{site}}_${{pad(s0+n)}}.jpg`));}});
  let fl=0;for(const c of CUTS){{const n=Math.round((t-c)*FPS);if(n>=0&&n<3)fl=[.28,.13,.05][n];}}
  document.getElementById('flash').style.opacity=fl;
  document.getElementById('turb').setAttribute('seed',1+F%97);
  const shrink=io(cl((t-OUT)/.45));
  document.getElementById('world').style.transform=`scale(${{1-.5*shrink}})`;
  document.getElementById('outro').style.opacity=cl((t-OUT-.15)/.3);
  document.getElementById('marks').style.opacity=cl((t-OUT-.4)/.25);
  document.getAnimations().forEach(a=>{{a.currentTime=t*1000}});
  await Promise.all(jobs);
}};
window.ready=(async()=>{{await document.fonts.ready;document.getAnimations().forEach(a=>a.pause());await seek(0);}})();
</script></body></html>
'''
(HERE / 'reel.html').write_text(page)
print('frames', len(sched), 'full', len(full), 'DUR', DUR)
