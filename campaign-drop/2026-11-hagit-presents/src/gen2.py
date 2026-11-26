#!/usr/bin/env python3
"""WORLDS v2 · Hagit presents the brand worlds — same takes, texts and beat grid as gen.py, a livelier grammar:
text in front of her, her small inside the world, the worlds' own films, and products orbiting her and the product on her palm.
Builds reel2.html (uses frames/ and stats.json written by gen.py + prep.py, and frames/w_* from the worlds' films, see README).
    python3 gen2.py && REEL=reel2.html node render.js 16.5 test/silent2.mp4
Everything that matters sits between y=270 and y=1620, so the 4:5 is a straight crop."""
import pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
R = '../../../'
FPS, BEAT = 30, 1.5
stats = json.loads((HERE / 'stats.json').read_text())
T = {k: i * BEAT for i, k in enumerate(['hookA', 'hookB', 'pm', 'en', 'mi', 've', 'or', 'ch', 'n29', 'cta'])}
DUR = 16.5
CUTS = [BEAT * i for i in range(1, 10)]
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
@keyframes push{from{transform:scale(1)}to{transform:scale(1.09)}}
.tag{position:absolute;left:0;right:0;top:276px;text-align:center;direction:ltr;font:600 27px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.26em;text-transform:uppercase;animation:capin .3s ease-out both}
.win{position:absolute;overflow:hidden;box-shadow:0 30px 70px rgba(40,24,14,.28);animation:winin .42s cubic-bezier(.16,.9,.2,1) both}
.win.arch{border-radius:230px 230px 18px 18px}
.win img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.box{position:absolute;left:40px;right:40px;top:1368px;text-align:center;z-index:20}
.box p{display:inline-block;font:500 76px/1.16 'Frank Ruhl Libre',serif;padding:16px 40px 24px;animation:capin .32s cubic-bezier(.16,.9,.2,1) both}
.box p em{font-style:normal}
.front{position:absolute;left:0;right:0;text-align:center;white-space:nowrap}
.panel{position:absolute;left:0;right:0;top:1424px;bottom:0;animation:fromB .3s cubic-bezier(.16,.9,.2,1) both}
.panel p{position:absolute;left:30px;right:30px;top:26px;text-align:center;font:500 74px/1.14 'Frank Ruhl Libre',serif}
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
.ch{position:absolute;left:60px;right:60px;top:1040px;text-align:center;font:700 80px/1.14 'Frank Ruhl Libre',serif;color:var(--ink);animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.ch em{font-style:normal;color:var(--copper2)}
.btn{position:absolute;left:190px;right:190px;top:1296px;text-align:center;background:var(--ink);color:var(--cream);border-radius:16px;padding:30px 20px 34px;animation:capin .45s cubic-bezier(.16,.9,.2,1) both}
.btn b{display:block;font:700 62px/1.1 'Frank Ruhl Libre',serif}.btn span{display:block;margin-top:10px;font:400 34px/1 'Heebo',sans-serif;opacity:.85}
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
def slot(key, sid, bg, back, mid, top, x=None, y=505, sc=1, clip='', t=None, camtop='', zoom=None):
    """sid = her shot (frames/<sid>), or None for a slot without her."""
    t = T[key] if t is None else t
    fg = ''
    if sid:
        st = stats[sid]
        her.append(dict(el='s_' + key, id=sid, t=[t, t + BEAT], x=x, sc=sc, top=st['top'], cx=st['cx'], y=y, zoom=zoom, hand=[[h[0], h[2]] for h in st.get('hand', [])]))
        fg = f'<div class="clip" style="{clip}"><img class="fg"></div>'
    slots.append(f'<div class="slot" id="s_{key}" data-show="{t},{t + BEAT}" style="background:{bg}"><div class="cam"><div class="bg">{back}</div><div class="mid">{mid}<div class="orb ob"></div></div>{fg}<div class="top"><div class="orb of"></div>{camtop}</div></div><div class="txt">{top}</div></div>')

P = lambda n: f";--st:#A45839;--pr:url({R}pardon-me/assets/print-{n}.webp)"
HOOKW = "900 400px/1 'Frank Ruhl Libre',serif"
HOOKBOX = lambda: box('מותג שנבחר<br><em>לא מותג שמשווים.</em>', '#2A201A', '#FAF8F3', '#EFCDBF', -1)
STUDIO = '<div class="tag" style="color:#4F372C;animation:none">Brand Worlds Studio · Hagit Antebi</div>'
# 0–1.5 hook: the line and its proof (worlds in the windows) are in frame 0
t = T['hookA']
slot('hookA', 'hookA', '#FAF8F3', '', word('נבחר.', HOOKW, '#A45839', -1, 900, 470, 'he', P('high-maintenance'), 'pf') + win('velune/assets/09-bottle-blush-garden-m.webp', '#C4D2E0', 'l', -1) + win('encore/assets/touchpoints/box-open-sans.webp', '#3D2623', 'r', -1),
     STUDIO + HOOKBOX(), 540, 505, .82)
# 1.5–3.0 the word she is not: lands in front of her and gets struck out
t = T['hookB']
front = f'''<div class="front he" style="top:985px;direction:rtl"><b style="display:inline-block;position:relative;font:900 270px/1 'Frank Ruhl Libre',serif;color:#FAF8F3;-webkit-text-stroke:10px #2A201A;paint-order:stroke fill;text-shadow:0 12px 0 #2A201A;animation:slam .3s cubic-bezier(.2,.9,.3,1) both;animation-delay:{t + .04:.2f}s">משווים.<i style="position:absolute;left:-30px;right:-30px;top:52%;height:22px;background:#A45839;transform-origin:100% 50%;animation:strike .3s cubic-bezier(.5,0,.2,1) both;animation-delay:{t + .7:.2f}s"></i></b></div>'''
slot('hookB', 'hookB', '#FAF8F3', '', word('נבחר.', HOOKW, '#A45839', -1, 900, 470, 'he', P('well-hello'), 'pf') + win('miel/assets/08-still-slice-pink-topper.webp', '#E7C0BD', 'l', t) + win('chasen/assets/verre.webp', '#e8d8bf', 'r', t, d=.14),
     STUDIO + front + HOOKBOX(), 540, 505, .82)
# 3.0 PARDON ME° — NOT SORRY. as in the PARDON ME° type edit; the four collections swap in the brand's oval window (and inside the letters); she is small beside it
t = T['pm']
COL = ['well-hello', 'none-of-your-business', 'high-maintenance', 'bad-influence']
OV = 'ellipse(262px 338px at 330px 1086px)'
mid = ''
for i, c in enumerate(COL):
    a, b = t + i * BEAT / 4, t + (i + 1) * BEAT / 4
    pf = f";--st:#9B1B47;--pr:url({R}pardon-me/assets/print-{c}.webp)"
    mid += f'''<div class="swap" data-show="{a},{b}">{word('NOT', "900 250px/1 'Bodoni Moda',serif", '#9B1B47', -1, 9999, 420, '', pf, 'pf')}{word('SORRY.', "900 250px/1 'Bodoni Moda',serif", '#9B1B47', -1, 1000, 630, '', pf, 'pf')}
<div style="position:absolute;inset:0;background:#1E3A2B;clip-path:ellipse(274px 350px at 330px 1086px)"></div>
<div style="position:absolute;inset:0;clip-path:{OV}"><img src="{R}pardon-me/assets/{c}.webp" style="position:absolute;left:40px;top:724px;width:580px;height:725px"></div></div>'''
top = f'<div class="tag" style="color:#1E3A2B;{dl(t, .1)}">No. 29 · Candles · Home Scent · Body Care</div><div class="panel" style="background:#1E3A2B;animation-delay:{t + .02:.2f}s"><p style="color:#F3EDE2">מנומס מבחוץ,<br><em style="color:#CFE06A">לא מתנצל מבפנים</em></p></div>'
slot('pm', 'pm', '#F3EDE2', '', mid, top, 800, 800, .5)
# 4.5 ENCORE° — three strips: the world's own pendant film, her, the box; the name runs across in front
t = T['en']
strips = f'''<div class="strip" style="left:6px;width:300px;background:#3D2623;animation:fromT .34s cubic-bezier(.16,.9,.2,1) both;animation-delay:{t + .02:.2f}s">{seq('w_encore', 'b_', 'jpg', 1, 2, 240, t, 'position:absolute;left:-1058px;top:0;height:1350px;width:2416px;max-width:none')}</div>
<div class="strip" style="left:318px;width:444px;background:#6E4E4A"></div>
<div class="strip" style="left:774px;width:300px;background:#3D2623;animation:fromB .34s cubic-bezier(.16,.9,.2,1) both;animation-delay:{t + .1:.2f}s"><img class="c" src="{R}encore/assets/touchpoints/box-open-sans.webp" style="animation:push 1.5s linear both;animation-delay:{t:.2f}s"></div>'''
front = f'''<div class="front" style="top:1090px;direction:ltr;font:600 236px/1 'Cormorant Garamond',serif;color:#F3D9A4;text-shadow:0 0 34px rgba(217,178,106,.85),0 6px 0 #3D2623">{letters('ENCORE°', t, .06)}</div>
<div class="word" style="top:300px;font:600 27px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:.26em;color:#F6EEE4"><b style="{dl(t, .1)}">NO. 28</b></div>'''
slot('en', 'en', '#2A1917', strips, '', front + box('תכשיט <em>שלא יורד</em>', '#F6EEE4', '#4A302C', '#A0672F', t, 1420, 76, .3), 610, 560, .6, 'clip-path:inset(270px 318px 300px 318px round 14px)')
# 6.0 MIEL° — the cake on her palm, the Maison's bag, box, seal and toppings turning around it
t = T['mi']
mi_items = [('miel/assets/touchpoints/bag-sans.webp', 'card', 200, 360), ('miel/assets/top-macarons.webp', '', 250, 250), ('miel/assets/touchpoints/box-sans.webp', 'card', 200, 360),
            ('miel/assets/top-meringues.webp', '', 250, 250), ('miel/assets/touchpoints/seal-sans.webp', 'card', 200, 360), ('miel/assets/top-roses.webp', '', 250, 250)]
orbits.append(dict(el='s_mi', t=t, R=410, tilt=.3, speed=.42, phase=.3, follow=-250, split=False, turn=.55, n=len(mi_items)))
oi = ''.join(f'<img class="oi {c}" src="{R}{s}" style="width:{w}px;height:{h}px;object-fit:cover">' for s, c, w, h in mi_items)
camtop = f'<img class="prod" src="{R}miel/assets/sig-rose.webp" data-lift="60" style="height:560px">' + oi
top = f'<div class="tag" data-show="{t},{t + .62}" style="color:#3A2E29;{dl(t, .1)}">No. 27 · Maison Miel · Romance</div>' + box('רומנטיקה <em>מתחילה מבפנים</em>', '#4A2C24', '#F6EADF', '#E7C0BD', t, 1500, 58)
slot('mi', 'mi', '#F6EADF', '', word('MIEL°', "600 300px/1 'Cormorant Garamond',serif", '#C5293F', t, 1000, 495), top, 540, 505, .95, camtop=camtop, zoom=[.6, 1.05, 1.7, -230])
# 7.5 VELUNE° — the world itself: the door opens onto the garden, she stands small in front of it, the line lands word by word
t = T['ve']
back = f'<div style="position:absolute;inset:0;transform-origin:50% 45%;animation:push 1.5s linear both;animation-delay:{t:.2f}s">{seq(R + "velune/assets/porte", "d", "webp", 1, .9, 40, t, "position:absolute;left:-1162px;top:0;height:1920px;width:3404px;max-width:none", 2)}</div>'
HRS = [('aube', 'AUBE', 'בוקר', 'rgba(255,255,255,0)'), ('floraison', 'FLORAISON', 'צהריים', 'rgba(241,160,170,.22)'), ('crepuscule', 'CRÉPUSCULE', 'ערב', 'rgba(35,42,63,.5)')]
hrs = ''
for i, (f, nm, he, tint) in enumerate(HRS):
    a, b = t + i * .5, t + (i + 1) * .5
    hrs += f'''<div class="swap" data-show="{a},{b}"><div style="position:absolute;inset:0;background:{tint}"></div>
<img src="{R}velune/assets/bottle-{f}.webp" style="position:absolute;left:432px;top:392px;height:446px;filter:drop-shadow(0 24px 30px rgba(30,42,56,.45));animation:pop .22s cubic-bezier(.2,1.5,.3,1) both;animation-delay:{a + .01:.2f}s">
<div style="position:absolute;left:684px;top:560px;direction:ltr;font:400 44px/1.2 'Marcellus',serif;color:#FDF7F4;text-shadow:0 0 18px rgba(35,42,63,.9);animation:capin .2s ease-out both;animation-delay:{a + .05:.2f}s">{nm}<br><span style="font:500 46px/1.2 'Frank Ruhl Libre',serif">{he}</span></div></div>'''
front = f'''<div class="front" style="top:286px;direction:ltr;font:400 100px/1 'Marcellus',serif;color:#FDF7F4;text-shadow:0 0 30px rgba(142,30,68,.75),0 4px 0 #8E1E44"><span style="display:inline-block;animation:wipe .5s cubic-bezier(.3,.8,.2,1) both;animation-delay:{t + .04:.2f}s">VELUNE°</span></div>
<div class="panel" style="background:#232A3F;animation-delay:{t + .02:.2f}s"><p style="color:#DCE3EB">{words('בושם הוא לא ריח,| *הוא *מקום', t, .2, .12, '#F1D9DC')}</p><div class="tag" style="top:300px;color:#8FA9C2;animation-delay:{t + .3:.2f}s">No. 25 · Maison de Parfum · Luxury</div></div>'''
back += hrs
slot('ve', 've', '#DCE3EB', back, '', front, 540, 870, .5)
# 9.0 ORÉVA° — the bottle on her palm, the rest of the line turning around her; the line comes in two beats, in front
t = T['or']
or_items = [('calm', 201), ('cleanse', 184), ('eye', 237), ('dew', 188), ('essence', 158), ('cocoon', 560)]
orbits.append(dict(el='s_or', t=t, R=470, tilt=.2, speed=.38, phase=.12, cx=540, cy=1010, split=True, turn=0, n=len(or_items)))
oi = ''.join(f'<img class="oi" src="{R}oreva/assets/kit/{n}.webp" style="height:{340 if n != "cocoon" else 200}px;filter:drop-shadow(0 16px 18px rgba(58,46,41,.3))">' for n, _ in or_items)
two = f'''<div class="box" style="top:1470px" data-show="{t},{t + .75}"><p style="background:#3A2E29;color:#F6EFE7;font-size:84px;animation:slam .26s cubic-bezier(.2,.9,.3,1) both;animation-delay:{t + .06:.2f}s">קודם הידיים,</p></div>
<div class="box" style="top:1470px" data-show="{t + .75},{t + BEAT}"><p style="background:#B87A57;color:#FBF7F1;font-size:84px;animation:slam .26s cubic-bezier(.2,.9,.3,1) both;animation-delay:{t + .77:.2f}s">אחר כך הבקבוק</p></div>'''
camtop = f'<img class="prod" src="{R}oreva/assets/p-glow.webp" data-lift="40" style="height:560px">' + oi
top = f'<div class="tag" data-show="{t},{t + .62}" style="color:#3A2E29;{dl(t, .1)}">No. 24 · Skin Studio · Beauty</div>' + two
slot('or', 'or', '#F6EFE7', '', word('ORÉVA°', "600 300px/1 'Cormorant Garamond',serif", '#B87A57', t, 1010, 495), top, 540, 505, .95, camtop=camtop, zoom=[.6, 1.05, 1.6, -260])
# 10.5 CHASEN° — the world's own pour fills the frame; she presents it, small; the name rises letter by letter
t = T['ch']
back = seq('w_chasen', 'b_', 'jpg', 14, 2.7, 144, t, 'position:absolute;left:-228px;top:0;height:1920px;width:1536px;max-width:none')
front = f'''<div class="front" style="top:300px;direction:ltr;font:600 200px/1 'Cormorant Garamond',serif;color:#f4e7d5;text-shadow:0 0 34px rgba(34,48,31,.9),0 6px 0 #22301f">{letters('CHASEN°', t, .07)}</div>
<div class="panel" style="background:#22301f;animation-delay:{t + .02:.2f}s"><p style="color:#f4e7d5">{words('העולם הראשון| *שמכינים', t, .22, .2, '#C9DD9A')}</p><div class="tag" style="top:300px;color:#9DB37C;animation-delay:{t + .3:.2f}s">No. 22 · Bar à Matcha · Interactive world</div></div>'''
slot('ch', 'ch', '#f4e7d5', back, '', front, 235, 800, .6)
# 12.0 the count: 29 behind her, the worlds running past in three rows, the studio's name written across in front
t = T['n29']
rows = ''.join(f'<div class="row" data-mq="{[-150, 150, -110][r]},{t}" style="top:{[690, 880, 1070][r]}px;left:{[-200, -900, -500][r]}px">' + ''.join(f'<img src="{R}images/home-worlds/{g}.webp">' for g in (GRID[r * 5:] + GRID[:r * 5])[:8]) + '</div>' for r in range(3))
front = f'''<div class="front" style="top:1150px;direction:ltr;font:italic 500 190px/1 'Cormorant Garamond',serif;color:#FAF8F3;text-shadow:0 0 30px rgba(196,118,90,.9);transform:rotate(-4deg)"><span style="display:inline-block;padding:0 20px;animation:wipe .55s cubic-bezier(.3,.8,.2,1) both;animation-delay:{t + .12:.2f}s">Brand Worlds</span></div>'''
slot('n29', 'n29', '#2A201A', '', word('29', "600 440px/0.9 'Cormorant Garamond',serif", '#C4765A', t, 9999, 470, '', ';font-variant-numeric:lining-nums') + rows,
     front + box('עולמות מותג חיים', '#FAF8F3', '#2A201A', '#A45839', t, 1440, 88, .4), 540, 660, .78)
t = T['cta']
cta = f'''<div class="slot" data-show="{t},{DUR + 1}" style="background:#FAF8F3">
  <div class="k" style="top:296px">HAGIT ANTEBI · BRAND WORLDS STUDIO</div>
  <div class="win arch" style="left:320px;top:360px;width:440px;height:640px;background:#EFCDBF;animation-delay:{t + .02:.2f}s"><img src="frames/ctaraw/b_040.jpg" style="inset:auto;left:-212px;top:-236px;width:800px;height:1422px;filter:saturate(1.05) brightness(1.04)"></div>
  <div class="ch" style="animation-delay:{t + .25:.2f}s">לא בטוחים אם למותג שלכם<br><em>כבר יש עולם?</em></div>
  <div class="btn" style="animation-delay:{t + .55:.2f}s"><b>אבחון פער המותג</b><span>30 דקות · בלי עלות</span></div>
  <div class="k" style="top:1560px;color:#8B7355">HAGITANTEBI.CO.IL</div>
</div>'''
page = f'''<!doctype html>
<html lang="he" dir="rtl"><head><meta charset="utf-8"><title>WORLDS v2 — Hagit presents</title>
<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500&family=Plus+Jakarta+Sans:wght@500;600&family=Cormorant+Garamond:ital,wght@0,600;1,500&family=Frank+Ruhl+Libre:wght@500;700;900&family=Bodoni+Moda:wght@900&family=Marcellus&display=block" rel="stylesheet">
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
for(const h of HER){{h.slot=document.getElementById(h.el);h.fg=h.slot.querySelector('img.fg');h.prod=h.slot.querySelector('.prod');}}
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
(HERE / 'reel2.html').write_text(page)
print('slots', len(slots), 'her', len(her), 'orbits', len(orbits))
