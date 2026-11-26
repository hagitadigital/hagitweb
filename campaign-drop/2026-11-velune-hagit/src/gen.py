#!/usr/bin/env python3
"""VELUNE° · Hagit presents one whole world — the site's own story (door, garden, fruit, drop, bottle, three hours, coffret)
in the typographic grammar of 2026-11-hagit-presents v2. 18s, every cut on the 120 BPM grid. Builds reel.html.
    python3 prep.py && python3 gen.py && node render.js 18 test/silent.mp4
All texts are headings of velune/index.html. Everything that matters sits between y=270 and y=1620 (4:5 = straight crop)."""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
R = '../../../'
FPS, BEAT = 30, 1.5
stats = json.loads((HERE / 'stats.json').read_text())
KEYS = ['hookA', 'hookB', 'door', 'garden', 'fruit', 'drop', 'bottle', 'one', 'three', 'coffret', 'cta']
T = {k: i * BEAT for i, k in enumerate(KEYS)}
DUR = 18.0
CUTS = [BEAT * i for i in range(1, 11)]
V = R + 'velune/assets/'
HE = "'David Libre',serif"
GRID = ['velune', 'encore', 'miel', 'oreva', 'pardon-me', 'chasen', 'trame', 'regard', 'rosee', 'signe', 'sonair', 'pancakerie', 'elvea', 'etage', 'soluna']

css = '''
:root{--cream:#FAF8F3;--ink:#2A201A;--copper:#C4765A;--copper2:#A45839}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--cream)}
#stage{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;background:var(--cream)}
.slot{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.bg,.mid,.top,.clip,.orb,.cam,.txt{position:absolute;inset:0}
.cam{transform-origin:0 0}
.swap{position:absolute;inset:0;visibility:hidden}
.fg{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;display:block}
.word{position:absolute;left:0;right:0;text-align:center;white-space:nowrap;direction:ltr}
.word b{display:inline-block;font-weight:inherit;animation:rise .4s cubic-bezier(.16,.9,.2,1) both}
.word.he{direction:rtl}
.word b.pf{color:transparent!important;background:var(--pr) center/700px;-webkit-background-clip:text;background-clip:text;-webkit-text-stroke:5px var(--st)}
.lt{display:inline-block;animation:letter .34s cubic-bezier(.2,1.3,.3,1) both}
.wd{display:inline-block;animation:pop .26s cubic-bezier(.2,1.5,.3,1) both}
@keyframes rise{from{opacity:0;transform:translateY(30%) scale(.94)}to{opacity:1;transform:none}}
@keyframes capin{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
@keyframes winin{from{opacity:0;transform:translateY(70px) scale(.94)}to{opacity:1;transform:none}}
@keyframes letter{from{opacity:0;transform:translateY(90%) rotate(8deg)}to{opacity:1;transform:none}}
@keyframes pop{from{opacity:0;transform:scale(.4) translateY(30px)}to{opacity:1;transform:none}}
@keyframes slam{0%{opacity:0;transform:scale(1.9)}60%{opacity:1;transform:scale(.96)}100%{opacity:1;transform:none}}
@keyframes strike{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fromL{from{transform:translateX(-100%)}to{transform:none}}
@keyframes fromR{from{transform:translateX(100%)}to{transform:none}}
@keyframes fromT{from{transform:translateY(-100%)}to{transform:none}}
@keyframes fromB{from{transform:translateY(100%)}to{transform:none}}
@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes drift{from{background-position:0 0}to{background-position:-120px -90px}}
@keyframes zoomin{from{transform:scale(1)}to{transform:scale(1.5)}}
@keyframes push{from{transform:scale(1)}to{transform:scale(1.09)}}
.tag{position:absolute;left:0;right:0;top:276px;text-align:center;direction:ltr;font:600 27px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.26em;text-transform:uppercase;animation:capin .3s ease-out both}
.win{position:absolute;overflow:hidden;box-shadow:0 30px 70px rgba(40,24,14,.28);animation:winin .42s cubic-bezier(.16,.9,.2,1) both}
.win.arch{border-radius:230px 230px 18px 18px}
.win img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.box{position:absolute;left:40px;right:40px;top:1368px;text-align:center;z-index:20}
.box p{display:inline-block;font:500 76px/1.16 'David Libre',serif;padding:16px 40px 24px;animation:capin .32s cubic-bezier(.16,.9,.2,1) both}
.box p em{font-style:normal}
.front{position:absolute;left:0;right:0;text-align:center;white-space:nowrap}
.panel{position:absolute;left:0;right:0;top:1424px;bottom:0;animation:fromB .3s cubic-bezier(.16,.9,.2,1) both}
.panel p{position:absolute;left:30px;right:30px;top:26px;text-align:center;font:500 80px/1.14 'David Libre',serif}
.panel p em{font-style:normal}
.band{position:absolute;top:0;bottom:0;width:132px;background:#9B1B47}
.band span{position:absolute;left:50%;top:50%;white-space:nowrap;direction:ltr;font:900 92px/1 'Bodoni Moda',serif;color:#F3EDE2;letter-spacing:.04em}
.strip{position:absolute;top:270px;height:1350px;width:348px;overflow:hidden;border-radius:14px}
.strip img.c{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.oi{position:absolute;left:0;top:0;transform-origin:50% 50%;will-change:transform}
.oi.card{border-radius:14px;box-shadow:0 14px 30px rgba(40,24,14,.3)}
.prod{position:absolute;left:0;top:0;transform-origin:50% 100%;filter:drop-shadow(0 26px 30px rgba(40,24,14,.35));z-index:5}
.row{position:absolute;left:0;display:flex;gap:14px;white-space:nowrap}
.row img{width:330px;height:173px;object-fit:cover;border-radius:10px;display:block}
.k{position:absolute;left:0;right:0;text-align:center;direction:ltr;font:600 27px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.28em;color:var(--copper)}
.ch{position:absolute;left:60px;right:60px;top:1040px;text-align:center;font:700 88px/1.12 'David Libre',serif;color:#1E2A38;animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.ch em{font-style:normal;color:#8E1E44}
.btn{position:absolute;left:190px;right:190px;top:1296px;text-align:center;background:#232A3F;color:#F4F6F9;border-radius:16px;padding:30px 20px 34px;animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.btn b{display:block;font:700 62px/1.1 'David Libre',serif}.btn span{display:block;margin-top:10px;font:400 34px/1 'Heebo',sans-serif;opacity:.85}
#flash{position:absolute;inset:0;z-index:25;background:#fff;opacity:0;pointer-events:none}
#grain{position:absolute;inset:0;z-index:31;pointer-events:none;opacity:.08;mix-blend-mode:overlay}
'''
def dl(t, d=.02): return 'animation:none' if t + d <= 0 else f'animation-delay:{t + d:.2f}s'
def win(img, panel, side, t, w=400, h=600, top=700, d=.06):
    x = 36 if side == 'l' else 1080 - 36 - w
    return f'<div class="win arch" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px;background:{panel};{dl(t, d)}"><img src="{R}{img}"></div>'
def box(html, bg, fg, em, t, top=1368, size=76, d=.08):
    return f'<div class="box" style="top:{top}px"><p style="background:{bg};color:{fg};font-size:{size}px;{dl(t, d)}">{html.replace("<em>", f"<em style=color:{em}>")}</p></div>'
def word(html, font, color, t, width, cy, cls='', extra='', bcls=''):
    return f'<div class="word {cls}" data-fit="{width}" data-cy="{cy}" style="font:{font};color:{color}"><b class="{bcls}" style="{dl(t)}{extra}">{html}</b></div>'
def letters(text, t, step=.07, d=.05): return ''.join(f'<span class="lt" style="animation-delay:{t + d + i * step:.2f}s">{c}</span>' for i, c in enumerate(text))
def words(text, t, step=.2, d=.1, em=None):
    out = []
    for i, w in enumerate(text.split(' ')):
        br = w.endswith('|'); w = w.rstrip('|'); col = f'color:{em};' if (em and w.startswith('*')) else ''
        out.append(f'<span class="wd" style="{col}animation-delay:{t + d + i * step:.2f}s">{w.lstrip("*")}</span>' + ('<br>' if br else ' '))
    return ''.join(out)
def seq(d, pre, ext, start, step, count, t, style, pad=3):
    return f'<img data-seq=\'{json.dumps(dict(d=d, pre=pre, ext=ext, start=start, step=step, count=count, t=t, pad=pad))}\' style="{style}">'

slots, her, orbits = [], [], []
def slot(key, sid, bg, back, mid, top, x=None, y=505, sc=1, clip='', t=None, camtop='', zoom=None, mirror=False):
    """sid = her shot (frames/<sid>), or None for a slot without her."""
    t = T[key] if t is None else t
    fg = ''
    if sid:
        st = stats[sid]
        her.append(dict(el='s_' + key, id=sid, t=[t, t + BEAT], x=x, sc=sc, top=st['top'], cx=st['cx'], y=y, zoom=zoom, hand=[[h[0], h[2]] for h in st.get('hand', [])]))
        fg = f'<div class="clip" style="{clip}"><img class="fg">{"<img class=\"fg fg2\">" if mirror else ""}</div>'
    slots.append(f'<div class="slot" id="s_{key}" data-show="{t},{t + BEAT}" style="background:{bg}"><div class="cam"><div class="bg">{back}</div><div class="mid">{mid}<div class="orb ob"></div></div>{fg}<div class="top"><div class="orb of"></div>{camtop}</div></div><div class="txt">{top}</div></div>')


NUIT, MARBRE, LITCHI, CHAIR = '#232A3F', '#DCE3EB', '#8E1E44', '#F1D9DC'
def cover(img, t, left, top, w, h, anim='push'):
    return f'<div style="position:absolute;inset:0;transform-origin:50% 42%;animation:{anim} 1.5s linear both;animation-delay:{t:.2f}s"><img src="{V}{img}" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;max-width:none"></div>'
def fseq(pre, start, step, t, origin='50% 42%', anim='push'):
    """the site's fruit / drop / bottle frames (1280x722), scaled 2.4 and lifted so the marble sits above the text panel"""
    return f'<div style="position:absolute;inset:0;transform-origin:{origin};animation:{anim} 1.5s cubic-bezier(.5,0,.3,1) both;animation-delay:{t:.2f}s">' + seq(V + 'fruit', pre, 'webp', start, step, 40, t, 'position:absolute;left:-996px;top:-140px;width:3072px;height:1733px;max-width:none', 2) + '</div>'
def panel(t, html, size=68, tag='No. 25 · Maison de Parfum · Luxury'):
    return f'<div class="panel" style="background:{NUIT};animation-delay:{t + .02:.2f}s"><p style="color:{MARBRE};font-size:{size}px">{html}</p><div class="tag" style="top:300px;color:#8FA9C2;animation-delay:{t + .3:.2f}s">{tag}</div></div>'
def name(t, size=100, top=286):
    return f'<div class="front" style="top:{top}px;direction:ltr;font:400 {size}px/1 \'Marcellus\',serif;color:#FDF7F4;text-shadow:0 0 30px rgba(142,30,68,.75),0 4px 0 {LITCHI}"><span style="display:inline-block;animation:wipe .5s cubic-bezier(.3,.8,.2,1) both;animation-delay:{t + .04:.2f}s">VELUNE°</span></div>'
def one(text, t, d=.1):
    return f'<span class="wd" style="font-size:104px;animation:slam .28s cubic-bezier(.2,.9,.3,1) both;animation-delay:{t + d:.2f}s">{text}</span>'
HOOK = lambda: box('יש לך מוצר שמריחים,<br><em>ועדיין אין לו מקום?</em>', NUIT, '#F4F6F9', CHAIR, -1)
STUDIO = '<div class="tag" style="color:#1E2A38;animation:none">VELUNE° · Brand Worlds Studio</div>'
MAQOM = lambda: word('מקום.', "700 430px/1 'David Libre',serif", LITCHI, -1, 940, 470, 'he')
DOOR = "position:absolute;left:-1162px;top:0;height:1920px;width:3404px;max-width:none"
# 0–3.0 hook: the question, and its answer already standing behind her (the door of a place), in frame 0
slot('hookA', 'hookA', MARBRE, f'<img src="{V}porte/d01.webp" style="{DOOR}">', MAQOM(), STUDIO + HOOK(), 296, 505, .82)
t = T['hookB']
slot('hookB', 'hookB', MARBRE, f'<div style="position:absolute;inset:0;transform:scale(1.12);transform-origin:50% 42%">{seq(V + "porte", "d", "webp", 1, .3, 40, t, DOOR, 2)}</div>', MAQOM(), STUDIO + HOOK(), 852, 505, .82)
# 3.0 the door opens; she steps back into it
t = T['door']
slot('door', 'pock', MARBRE, f'<div style="position:absolute;inset:0;transform-origin:50% 45%;animation:push 1.5s linear both;animation-delay:{t:.2f}s">{seq(V + "porte", "d", "webp", 1, .9, 40, t, DOOR, 2)}</div>',
     '', name(t, 150, 300) + panel(t, words('מאחורי הדלת| *יש *גן.', t, .22, .15, CHAIR)), 540, 830, .54)
# 4.5 the garden
t = T['garden']
slot('garden', 'en', MARBRE, cover('05-allee-garden-water.webp', t, -1166, 0, 3412, 1920, 'zoomin'), '', panel(t, words('בגן עץ אחד.| על העץ *פרי *אחד.', t, .17, .1, CHAIR)), 950, 840, .56)
# 6.0 the fruit opens — she offers her palm under it
t = T['fruit']
slot('fruit', 'or', MARBRE, fseq('a', 1, .9, t), '', panel(t, one('הפרי נפתח.', t)), 250, 800, .6)
# 7.5 one drop — the camera goes in
t = T['drop']
slot('drop', 'or2', MARBRE, fseq('c', 6, .8, t, '50% 36%', 'zoomin'), '', panel(t, one('טיפה אחת.', t)), 250, 800, .6)
# 9.0 and it is already a bottle
t = T['bottle']
slot('bottle', 'n29', MARBRE, fseq('b', 12, .64, t, '50% 55%'), '', name(t, 110, 290) + panel(t, words('והיא כבר *בקבוק.', t, .25, .55, CHAIR), 96), 215, 860, .5)
# 10.5 one bottle — she looks up at it
t = T['one']
back = cover('04-porte-open-garden.webp', t, -1166, 0, 3412, 1920) + f'<img src="{V}bottle-aube.webp" style="position:absolute;left:412px;top:330px;height:530px;filter:drop-shadow(0 24px 30px rgba(30,42,56,.45));animation:pop .3s cubic-bezier(.2,1.5,.3,1) both;animation-delay:{t + .03:.2f}s">'
slot('one', 'hrs', MARBRE, back, '', panel(t, one('בקבוק אחד.', t, .12)), 540, 900, .48)
# 12.0 three hours — the bottle on her palm, the other two and their notes turning around it, the light moving from morning to evening
t = T['three']
HRS = [('AUBE', 'בוקר', MARBRE), ('FLORAISON', 'צהריים', CHAIR), ('CRÉPUSCULE', 'ערב', '#3A4263')]
back = ''.join(f'<div class="swap" data-show="{t + i * .5},{t + (i + 1) * .5}" style="inset:-900px;background:{c}"></div>' for i, (_, _, c) in enumerate(HRS))
CARD = 'width:250px;height:300px;object-fit:cover'
items = [('bottle-aube.webp', '', 'height:330px'), ('13-notes-aube-bergamot-tea.webp', 'card', CARD), ('bottle-crepuscule.webp', '', 'height:330px'),
         ('15-notes-crepuscule-iris-oud.webp', 'card', CARD), ('14-notes-floraison-rose-peony.webp', 'card', CARD)]
orbits.append(dict(el='s_three', t=t, R=400, tilt=.3, speed=.42, phase=.1, follow=-260, split=False, turn=.5, n=len(items)))
camtop = f'<img class="prod" src="{V}bottle-floraison.webp" data-lift="40" style="height:520px">' + ''.join(f'<img class="oi {c}" src="{V}{s}" style="{st}">' for s, c, st in items)
top = ''.join(f'<div class="tag" data-show="{t + i * .5},{t + (i + 1) * .5}" style="top:1376px;z-index:21;animation:none;font-size:32px"><span style="display:inline-block;background:{NUIT};color:#F4F6F9;padding:14px 30px 16px;border-radius:40px">{n} · <span style="font:500 38px {HE};letter-spacing:0">{h}</span></span></div>' for i, (n, h, _) in enumerate(HRS))
top += box('שלוש שעות.', LITCHI, '#FDF7F4', CHAIR, t, 1466, 92)
slot('three', 'mi', MARBRE, back, word('VELUNE°', "400 300px/1 'Marcellus',serif", LITCHI, t, 1010, 495), top, 570, 505, .95, camtop=camtop, zoom=[.7, 1.15, 1.6, -230])
# 13.5 the door comes back, as a box — she stands on both sides of it
t = T['coffret']
back = f'<div class="swap" data-show="{t},{t + .6}">{cover("19-ecrin-box-closed.webp", t, -1166, -60, 3412, 1920)}</div><div class="swap" data-show="{t + .6},{t + BEAT}">{cover("20-ecrin-box-open.webp", t, -1166, -60, 3412, 1920)}</div>'
slot('coffret', 'ch', MARBRE, back, '', panel(t, words('הדלת חוזרת.| *הפעם *בקופסה.', t, .2, .12, CHAIR)), 200, 885, .56, mirror=True)
t = T['cta']
cta = f'''<div class="slot" data-show="{t},{DUR + 1}" style="background:{MARBRE}">
  <div class="k" style="top:290px;color:{LITCHI}">HAGIT ANTEBI · BRAND WORLDS STUDIO</div>
  <div class="win arch" style="left:320px;top:350px;width:440px;height:640px;background:#C4D2E0;animation-delay:{t + .02:.2f}s"><img src="shots/closing.jpg" style="inset:auto;left:-202px;top:-251px;width:780px;height:1690px;object-fit:fill"></div>
  <div class="ch" style="top:1030px;animation-delay:{t + .25:.2f}s">בושם הוא לא ריח.<br><em>הוא מקום.</em></div>
  <div class="btn" style="top:1290px;animation-delay:{t + .55:.2f}s"><b>לאבחון פער המותג</b></div>
  <div class="k" style="top:1560px;color:#6E8399">HAGITANTEBI.CO.IL/VELUNE</div>
</div>'''
page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>VELUNE — Hagit presents</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500&family=Plus+Jakarta+Sans:wght@500;600&family=David+Libre:wght@400;500;700&family=Marcellus&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<div id="stage">
{chr(10).join(slots)}
{cta}
<div id="flash"></div>
<svg id="grain" width="1080" height="1920"><filter id="n"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="1"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1920" filter="url(#n)"/></svg>
</div>
<script>
const FPS=30, BEAT={BEAT}, HER={json.dumps(her)}, ORB={json.dumps(orbits)}, CUTS={json.dumps(CUTS)};
const pad=(n,w=3)=>String(n).padStart(w,'0');
async function put(img,u){{if(!img||img.dataset.u===u)return;img.dataset.u=u;img.src=u;try{{await img.decode()}}catch(e){{}}}}
const shows=[...document.querySelectorAll('[data-show]')].map(e=>[e,...e.dataset.show.split(',').map(Number)]);
const seqs=[...document.querySelectorAll('[data-seq]')].map(e=>[e,JSON.parse(e.dataset.seq)]);
const mqs=[...document.querySelectorAll('[data-mq]')].map(e=>[e,...e.dataset.mq.split(',').map(Number)]);
for(const h of HER){{h.slot=document.getElementById(h.el);h.fg=h.slot.querySelector('img.fg');h.fg2=h.slot.querySelector('img.fg2');h.prod=h.slot.querySelector('.prod');}}
for(const o of ORB){{o.slot=document.getElementById(o.el);o.items=[...o.slot.querySelectorAll('.oi')];o.back=o.slot.querySelector('.ob');o.front=o.slot.querySelector('.of');o.her=HER.find(h=>h.el===o.el);}}
function fit(){{for(const w of document.querySelectorAll('.word[data-fit]')){{const b=w.firstElementChild,max=parseFloat(getComputedStyle(w).fontSize);
  const k=Math.min(1,+w.dataset.fit/b.scrollWidth);w.style.fontSize=(max*k)+'px';w.style.top=(+w.dataset.cy-b.offsetHeight/2)+'px';}}}}
window.seek=async function(t){{
  const F=Math.round(t*FPS), jobs=[];
  for(const [e,a,b] of shows) e.style.visibility=(t>=a-1e-6&&t<b-1e-6)?'inherit':'hidden';
  for(const [e,a,b] of shows) if(e.classList.contains('slot')) e.style.visibility=(t>=a-1e-6&&t<b-1e-6)?'visible':'hidden';
  for(const h of HER){{ if(!(t>=h.t[0]-1e-6&&t<h.t[1]-1e-6))continue;
    const n=Math.min(45,Math.round((t-h.t[0])*FPS)+1); jobs.push(put(h.fg,`frames/${{h.id}}/f_${{pad(n)}}.webp`));
    const k=1+.035*Math.pow(Math.max(0,1-(n-1)/7),2)+.012*(t-h.t[0]), s=h.sc*k, PY=h.y+650*h.sc;
    const tx=h.x-h.cx*s, ty=PY-(PY-h.y)*k-h.top*s; h.tx=tx;h.ty=ty;h.s=s;h.n=n; const u=t-h.t[0];
    h.fg.style.transform=`translate(${{tx}}px,${{ty}}px) scale(${{s}})`;
    if(h.fg2){{jobs.push(put(h.fg2,`frames/${{h.id}}/f_${{pad(n)}}.webp`));h.fg2.style.transform=`translate(${{1080-tx}}px,${{ty}}px) scale(${{-s}},${{s}})`;}}
    if(h.prod){{const p=h.prod,[hx,hy]=h.hand[n-1],pop=1-.3*Math.pow(Math.max(0,1-(n-1)/8),2);h.px=tx+hx*s;h.py=ty+hy*s;
      p.style.transform=`translate(${{h.px-p.offsetWidth/2}}px,${{h.py+(+p.dataset.lift)-p.offsetHeight}}px) scale(${{pop}})`;p.style.opacity=Math.min(1,n/3);
      if(h.zoom){{const [z0,z1,K0,dy]=h.zoom, x=Math.min(1,Math.max(0,(u-z0)/(z1-z0))), e=x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2, K=1+(K0-1)*e, ox=h.px, oy=h.py+dy;
        h.slot.querySelector('.cam').style.transform=`translate(${{(540-ox)*e+ox*(1-K)}}px,${{(900-oy)*e+oy*(1-K)}}px) scale(${{K}})`;}} }} }}
  for(const o of ORB){{ if(!(t>=o.t-1e-6&&t<o.t+BEAT-1e-6))continue;
    const u=t-o.t, grow=1-Math.pow(Math.max(0,1-u/.35),3), cx=o.follow!==undefined?o.her.px:o.cx, cy=o.follow!==undefined?o.her.py+o.follow:o.cy;
    o.items.forEach((e,i)=>{{const th=2*Math.PI*(o.phase+i/o.n+o.speed*u), d=Math.cos(th), x=cx+o.R*grow*Math.sin(th), y=cy+o.R*o.tilt*d, sc=(.8+.22*d)*(.5+.5*grow);
      if(o.split){{const par=d<0?o.back:o.front;if(e.parentNode!==par)par.appendChild(e);}} else e.style.zIndex=d<0?1:9;
      e.style.transform=`translate(${{x-e.offsetWidth/2}}px,${{y-e.offsetHeight/2}}px) perspective(900px) rotateY(${{-Math.sin(th)*o.turn*60}}deg) scale(${{sc}})`;
      e.style.opacity=Math.min(1,u/.15);e.style.filter=(e.dataset.f||(e.dataset.f=e.style.filter||' '))+` brightness(${{.86+.14*(d+1)/2}})`;}}); }}
  for(const [e,q] of seqs){{const n=Math.round((t-q.t)*FPS); if(n<0||n>=45)continue; const f=Math.min(q.count,Math.max(1,Math.round(q.start+n*q.step)));
    jobs.push(put(e,(q.d.startsWith('.')?q.d:'frames/'+q.d)+'/'+q.pre+pad(f,q.pad)+'.'+q.ext));}}
  for(const [e,v,t0] of mqs) e.style.transform=`translateX(${{v*(t-t0)}}px)`;
  let fl=0;for(const c of CUTS){{const n=Math.round((t-c)*FPS);if(n>=0&&n<3)fl=[.26,.12,.05][n];}}
  document.getElementById('flash').style.opacity=fl;
  document.getElementById('turb').setAttribute('seed',1+F%97);
  document.getAnimations().forEach(a=>{{a.currentTime=t*1000}});
  await Promise.all(jobs);
}};
window.ready=(async()=>{{await document.fonts.ready;fit();document.getAnimations().forEach(a=>a.pause());await Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>i.decode().catch(()=>0)));await seek(0);}})();
</script></body></html>
'''
(HERE / 'reel.html').write_text(page)
print('slots', len(slots), 'her', len(her), 'orbits', len(orbits))
