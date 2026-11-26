#!/usr/bin/env python3
"""WORLDS · Hagit presents the brand worlds — typographic edit of her own poses (16.5s, every cut on the 120 BPM grid).
Builds schedule.json (for prep.py) and reel.html. Every timing, text and placement lives here.
    python3 gen.py && python3 prep.py && python3 gen.py && node render.js 16.5 ../WORLDS-HAGIT-9x16.mp4
Everything that matters sits between y=270 and y=1620, so the 4:5 is a straight crop."""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
R = '../../../'
FPS, BEAT = 30, 1.5
Y0 = 505          # where the top of her head sits
# her shots: id, clip, first frame (30fps), scale, x of her head centre, optional y offset
SHOTS = [('hookA', '111634', 12, .82, 540, 0), ('hookB', '111634', 98, .82, 540, 0), ('pm', '111646', 28, .80, 650, 0), ('en', '111923', 10, .98, 430, 0),
         ('mi', '111741', 205, .95, 540, 0), ('ve', '111937', 25, .92, 430, 0), ('or', '111741', 35, .95, 470, 0), ('ch', '111923', 120, 1.0, 400, 0),
         ('n29', '111912', 60, 1.06, 540, 0)]
(HERE / 'schedule.json').write_text(json.dumps(dict(shots=[dict(id=i, clip=c, f0=f, n=45, track=i in ('mi', 'or')) for i, c, f, *_ in SHOTS] + [dict(id='cta', clip='111724', f0=100, n=1)])))
stats = json.loads((HERE / 'stats.json').read_text()) if (HERE / 'stats.json').exists() else {}

# the six worlds: shot, No., category line, name, name font, backdrop, word colour, window (shape, image, panel, fit), box colours, Hebrew line — all texts as they stand on brand-worlds/index.html
W = [
 ('pm', '29', 'Candles · Home Scent · Body Care', 'PARDON<br>ME°', "900 200px/0.92 'Bodoni Moda',serif", '#F3EDE2', '#9B1B47', ('oval', 'pardon-me/assets/high-maintenance.webp', '#F2C4CE', 'cover'), ('#1E3A2B', '#F3EDE2', '#CFE06A'), 'מנומס מבחוץ,<br><em>לא מתנצל מבפנים</em>', 880, 250),
 ('en', '28', 'Maison de Bijoux · Fine Jewellery', 'ENCORE°', "600 300px/1 'Cormorant Garamond',serif", '#6E4E4A', '#D9B26A', ('arch', 'encore/assets/touchpoints/box-open-sans.webp', '#3D2623', 'cover'), ('#F6EEE4', '#4A302C', '#A0672F'), 'תכשיט <em>שלא יורד</em>', 1010, 330),
 ('mi', '27', 'Maison Miel · Romance', 'MIEL°', "600 300px/1 'Cormorant Garamond',serif", '#F6EADF', '#C5293F', ('palm', 'miel/assets/sig-rose.webp', 560, 60), ('#4A2C24', '#F6EADF', '#E7C0BD'), 'רומנטיקה<br><em>מתחילה מבפנים</em>', 1000, 400),
 ('ve', '25', 'Maison de Parfum · Luxury', 'VELUNE°', "400 300px/1 'Marcellus',serif", '#DCE3EB', '#8E1E44', ('arch', 'velune/assets/09-bottle-blush-garden-m.webp', '#C4D2E0', 'cover'), ('#232A3F', '#DCE3EB', '#F1D9DC'), 'בושם הוא לא ריח,<br><em>הוא מקום</em>', 1010, 300),
 ('or', '24', 'Skin Studio · Beauty', 'ORÉVA°', "600 300px/1 'Cormorant Garamond',serif", '#F6EFE7', '#B87A57', ('palm', 'oreva/assets/p-glow.webp', 560, 40), ('#3A2E29', '#F6EFE7', '#EFCDBF'), 'קודם הידיים,<br><em>אחר כך הבקבוק</em>', 1010, 340),
 ('ch', '22', 'Bar à Matcha · Interactive world', 'CHASEN°', "600 300px/1 'Cormorant Garamond',serif", '#f4e7d5', '#4c6b33', ('arch', 'chasen/assets/verre.webp', '#e8d8bf', 'cover'), ('#22301f', '#f4e7d5', '#C9DD9A'), 'העולם הראשון<br><em>שמכינים</em>', 1010, 320),
]
T_W, T_29, CTA, DUR = 3.0, 12.0, 13.5, 16.5
CUTS = [BEAT * i for i in range(1, 10)]
GRID = ['velune', 'encore', 'miel', 'oreva', 'pardon-me', 'chasen', 'trame', 'regard', 'rosee', 'signe', 'sonair', 'pancakerie', 'elvea', 'etage', 'soluna']

css = '''
:root{--cream:#FAF8F3;--beige:#F5F1E8;--ink:#2A201A;--deep:#4F372C;--copper:#C4765A;--copper2:#A45839;--line:#D4C9BC}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--cream)}
#stage{position:absolute;inset:0;width:1080px;height:1920px;overflow:hidden;background:var(--cream)}
.slot{position:absolute;inset:0;overflow:hidden;visibility:hidden}
.mid,.top{position:absolute;inset:0}
.fg{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;display:block}
.word{position:absolute;left:0;right:0;text-align:center;white-space:nowrap;direction:ltr}
.word b{display:inline-block;font-weight:inherit;animation:rise .4s cubic-bezier(.16,.9,.2,1) both}
.word.he{direction:rtl}
.word b.pf{color:transparent!important;background:var(--pr) center/700px;-webkit-background-clip:text;background-clip:text;-webkit-text-stroke:5px var(--st)}
@keyframes rise{from{opacity:0;transform:translateY(30%) scale(.94)}to{opacity:1;transform:none}}
@keyframes capin{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
@keyframes winin{from{opacity:0;transform:translateY(70px) scale(.94)}to{opacity:1;transform:none}}
.tag{position:absolute;left:0;right:0;top:276px;text-align:center;direction:ltr;font:600 27px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.26em;text-transform:uppercase;animation:capin .3s ease-out both}
.win{position:absolute;overflow:hidden;box-shadow:0 30px 70px rgba(40,24,14,.28);animation:winin .42s cubic-bezier(.16,.9,.2,1) both}
.win.arch{border-radius:230px 230px 18px 18px}.win.oval{border-radius:50%}
.win img{position:absolute;inset:0;width:100%;height:100%}
.box{position:absolute;left:40px;right:40px;top:1400px;text-align:center}
.box p{display:inline-block;font:500 76px/1.16 'Frank Ruhl Libre',serif;padding:16px 40px 24px;animation:capin .32s cubic-bezier(.16,.9,.2,1) both}
.box p em{font-style:normal}
.prod{position:absolute;left:0;top:0;transform-origin:50% 100%;filter:drop-shadow(0 26px 30px rgba(40,24,14,.35))}
.grid{position:absolute;left:16px;top:640px;width:1048px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px;animation:capin .4s ease-out both}
.grid img{width:100%;height:178px;object-fit:cover;border-radius:10px;display:block}
.k{position:absolute;left:0;right:0;text-align:center;direction:ltr;font:600 27px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.28em;color:var(--copper)}
.ch{position:absolute;left:60px;right:60px;top:1040px;text-align:center;font:700 80px/1.14 'Frank Ruhl Libre',serif;color:var(--ink);animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.ch em{font-style:normal;color:var(--copper2)}
.btn{position:absolute;left:190px;right:190px;top:1296px;text-align:center;background:var(--ink);color:var(--cream);border-radius:16px;padding:30px 20px 34px;animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.btn b{display:block;font:700 62px/1.1 'Frank Ruhl Libre',serif}.btn span{display:block;margin-top:10px;font:400 34px/1 'Heebo',sans-serif;opacity:.85}
#flash{position:absolute;inset:0;z-index:25;background:#fff;opacity:0;pointer-events:none}
#grain{position:absolute;inset:0;z-index:31;pointer-events:none;opacity:.08;mix-blend-mode:overlay}
'''
def delay(t, d=.02): return 'animation:none' if t == 0 else f'animation-delay:{t + d:.2f}s'
def win(shape, img, panel, fit, side, t, w=430, h=640, top=690, d=.06):
    x = 36 if side == 'l' else 1080 - 36 - w
    pad = ';padding:60px 40px 40px;object-position:50% 60%' if fit == 'contain' else ''
    return f'<div class="win {shape}" style="left:{x}px;top:{top}px;width:{w}px;height:{h}px;background:{panel};{delay(t, d)}"><img src="{R}{img}" style="object-fit:{fit}{pad}"></div>'
def box(html, bg, fg, em, t, top=1368, size=76):
    return f'<div class="box" style="top:{top}px"><p style="background:{bg};color:{fg};font-size:{size}px;{delay(t, .08)}">{html.replace("<em>", f"<em style=color:{em}>")}</p></div>'
def word(html, font, color, t, width, cy, cls='', extra=''):
    return f'<div class="word {cls}" data-fit="{width}" data-cy="{cy}" style="font:{font};color:{color}"><b style="{delay(t)}{extra}">{html}</b></div>'

slots, her = [], []
def slot(sid, t0, t1, bg, mid, top, x, sc, dy=0):
    st = stats.get(sid, dict(top=200, cx=540))
    her.append(dict(id=sid, t=[t0, t1], x=x, sc=sc, top=st['top'], cx=st['cx'], y=Y0 + dy))
    slots.append(f'<div class="slot" id="{sid}" data-show="{t0},{t1}" style="background:{bg}"><div class="mid">{mid}</div><img class="fg"><div class="top">{top}</div></div>')
S = {i: (sc, x, dy) for i, _, _, sc, x, dy in SHOTS}
P = lambda n: f";--st:#A45839;--pr:url({R}pardon-me/assets/print-{n}.webp)"
# 0–3.0 hook: the line and its proof (worlds in the windows) are in frame 0
for sid, t0, wl, wr, pr in (('hookA', 0, W[3][7], W[1][7], 'high-maintenance'), ('hookB', BEAT, ('arch', 'miel/assets/08-still-slice-pink-topper.webp', '#E7C0BD', 'cover'), W[5][7], 'well-hello')):
    mid = word('נבחר.', "900 400px/1 'Frank Ruhl Libre',serif", '#A45839', t0, 900, 470, 'he', P(pr)).replace('<b ', '<b class="pf" ') + win(*wl, 'l', t0, 400, 600, 700) + win(*wr, 'r', t0, 400, 600, 700, .14)
    top = '<div class="tag" style="color:#4F372C;animation:none">Brand Worlds Studio · Hagit Antebi</div>' + box('מותג שנבחר<br><em>לא מותג שמשווים.</em>', '#2A201A', '#FAF8F3', '#EFCDBF', 0)
    slot(sid, t0, t0 + BEAT, '#FAF8F3', mid, top, S[sid][1], S[sid][0], S[sid][2])
for i, (sid, no, cat, name, font, bg, wc, wn, (bb, bf, be), he, fitw, cy) in enumerate(W):
    t = T_W + i * BEAT; sc, x, dy = S[sid]; side = 'l' if x > 540 else 'r'
    dark = bg == '#6E4E4A'
    palm = wn[0] == 'palm'
    mid = word(name, font, wc, t, fitw, 495, '', '') + ('' if palm else win(*wn, side, t))
    prod = f'<img class="prod" id="prod-{sid}" src="{R}{wn[1]}" style="height:{wn[2]}px"><i class="pin" style="{delay(t, .05)}"></i>' if palm else ''
    top = prod + f'<div class="tag" style="color:{"#F6EEE4" if dark else "#3A2E29"};{delay(t, .1)}">No. {no} · {cat}</div>' + (box(he.replace('<br>', ' '), bb, bf, be, t, 1500, 58) if palm else box(he, bb, bf, be, t))
    slot(sid, t, t + BEAT, bg, mid, top, x, sc, dy)
    if palm: her[-1].update(hand=[[h[0], h[2]] for h in stats.get(sid, {}).get('hand', [[540, 1200, 1200, 0]] * 45)], lift=wn[3])
grid = '<div class="grid" style="animation-delay:%.2fs">%s</div>' % (T_29 + .04, ''.join(f'<img src="{R}images/home-worlds/{g}.webp">' for g in GRID))
slot('n29', T_29, CTA, '#2A201A', word('29', "600 440px/0.9 'Cormorant Garamond',serif", '#C4765A', T_29, 9999, 490, '', ';font-variant-numeric:lining-nums') + grid,
     box('עולמות מותג חיים', '#FAF8F3', '#2A201A', '#A45839', T_29, 1440, 88), S['n29'][1], S['n29'][0], S['n29'][2])
cta = f'''<div class="slot" data-show="{CTA},{DUR + 1}" style="background:#FAF8F3">
  <div class="k" style="top:296px">HAGIT ANTEBI · BRAND WORLDS STUDIO</div>
  <div class="win arch" style="left:320px;top:360px;width:440px;height:640px;background:#EFCDBF;animation-delay:{CTA + .02:.2f}s"><img src="shots/closing.jpg" style="inset:auto;left:-202px;top:-251px;width:780px;height:1690px;object-fit:fill"></div>
  <div class="ch" style="animation-delay:{CTA + .25:.2f}s">לא בטוחים אם למותג שלכם<br><em>כבר יש עולם?</em></div>
  <div class="btn" style="animation-delay:{CTA + .55:.2f}s"><b>אבחון פער המותג</b><span>30 דקות · בלי עלות</span></div>
  <div class="k" style="top:1560px;color:#8B7355">HAGITANTEBI.CO.IL</div>
</div>'''
page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>WORLDS — Hagit presents</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500&family=Plus+Jakarta+Sans:wght@500;600&family=Cormorant+Garamond:wght@600&family=Frank+Ruhl+Libre:wght@500;700;900&family=Bodoni+Moda:wght@900&family=Marcellus&display=block" rel="stylesheet">
<style>{css}</style></head><body>
<div id="stage">
{chr(10).join(slots)}
{cta}
<div id="flash"></div>
<svg id="grain" width="1080" height="1920"><filter id="n"><feTurbulence id="turb" type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="1"/><feColorMatrix type="saturate" values="0"/></filter><rect width="1080" height="1920" filter="url(#n)"/></svg>
</div>
<script>
const FPS=30, HER={json.dumps(her)}, CUTS={json.dumps(CUTS)};
const pad=n=>String(n).padStart(3,'0');
async function put(img,u){{if(!img||img.dataset.u===u)return;img.dataset.u=u;img.src=u;try{{await img.decode()}}catch(e){{}}}}
const shows=[...document.querySelectorAll('[data-show]')].map(e=>[e,...e.dataset.show.split(',').map(Number)]);
for(const h of HER)h.fg=document.querySelector('#'+h.id+' img.fg');
function fit(){{for(const w of document.querySelectorAll('.word[data-fit]')){{const b=w.firstElementChild,max=parseFloat(getComputedStyle(w).fontSize);
  const k=Math.min(1,+w.dataset.fit/b.scrollWidth);w.style.fontSize=(max*k)+'px';w.style.top=(+w.dataset.cy-b.offsetHeight/2)+'px';}}}}
window.seek=async function(t){{
  const F=Math.round(t*FPS), jobs=[];
  for(const [e,a,b] of shows) e.style.visibility=(t>=a-1e-6&&t<b-1e-6)?'visible':'hidden';
  for(const h of HER){{ if(!(t>=h.t[0]-1e-6&&t<h.t[1]-1e-6))continue;
    const n=Math.min(45,Math.round((t-h.t[0])*FPS)+1); jobs.push(put(h.fg,`frames/${{h.id}}/f_${{pad(n)}}.webp`));
    const k=1+.035*Math.pow(Math.max(0,1-(n-1)/7),2)+.012*(t-h.t[0]), s=h.sc*k, PY=1150;
    const tx=h.x-h.cx*s, ty=PY-(PY-h.y)*k-h.top*s;
    h.fg.style.transform=`translate(${{tx}}px,${{ty}}px) scale(${{s}})`;
    if(h.hand){{const p=document.getElementById('prod-'+h.id),[hx,hy]=h.hand[n-1],pop=1-.3*Math.pow(Math.max(0,1-(n-1)/8),2);
      p.style.transform=`translate(${{tx+hx*s-p.offsetWidth/2}}px,${{ty+hy*s+h.lift-p.offsetHeight}}px) scale(${{pop}})`;p.style.opacity=Math.min(1,n/3);}} }}
  let fl=0;for(const c of CUTS){{const n=Math.round((t-c)*FPS);if(n>=0&&n<3)fl=[.26,.12,.05][n];}}
  document.getElementById('flash').style.opacity=fl;
  document.getElementById('turb').setAttribute('seed',1+F%97);
  document.getAnimations().forEach(a=>{{a.currentTime=t*1000}});
  await Promise.all(jobs);
}};
window.ready=(async()=>{{await document.fonts.ready;fit();document.getAnimations().forEach(a=>a.pause());await Promise.all([...document.images].filter(i=>i.src).map(i=>i.decode().catch(()=>0)));await seek(0);}})();
</script></body></html>
'''
(HERE / 'reel.html').write_text(page)
print('shots', len(her), 'DUR', DUR, 'stats', len(stats))
