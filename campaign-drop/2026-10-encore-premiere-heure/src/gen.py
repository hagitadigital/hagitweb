#!/usr/bin/env python3
"""ENCORE° · La Première Heure — brand-mode reel (9:16, 30s). Builds reel.html next to this file.

Assets come from the world itself (make_assets.sh): the landing sequence (a pendant settles on the neck),
the box with the date on its lid, the cuff and tag at sunset, the sign with the dial, and four pieces.
The pendant is a necklace, and in ENCORE° necklaces belong to noon — so the first hour it records is 12:14.
Timeline (s): hook 0–2.5 · logo 2.5–4 · the stamp (signature) 4–10 · four certificates 10–15 · 18:00 15–19 ·
a year later 19–24 · the sign 24–27 · outro 27–30 (holds to the last frame).
"""
import pathlib

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE.parents[2] / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
P = lambda t: f"{max(0, min(D, t)) / D * 100:.3f}%"
css = []

H06, H12, H18, H00 = '#6E4E4A', '#34405A', '#853A26', '#241212'
GOLD, GLINE, GTEXT, GON = '#D9B26A', '#B8955A', '#7A5A2A', '#E8CD96'
STONE, PAPER, INK, MUTED, ON = '#EFE8DD', '#FBF7F0', '#1E0F0E', '#5A4640', '#F6EEE4'
HEB = "'Frank Ruhl Libre', serif"
SERIF = "'Cormorant Garamond', 'Frank Ruhl Libre', serif"
SANS = "'Heebo', sans-serif"
STAMP = f"font-family: {SERIF}; letter-spacing: .18em; font-variant-numeric: lining-nums tabular-nums"


def kf(name, stops):
    body = ''.join(f"{P(t)}{{{d}}}" for t, d in stops)
    css.append(f"@keyframes {name}{{0%{{{stops[0][1]}}}{body}100%{{{stops[-1][1]}}}}}")
    css.append(f".{name}{{animation-name:{name}}}")


def wedge(i, r=50):
    """Quarter i of the dial: 0 = 00:00 top (night), 1 = 06:00 right, 2 = 12:00 bottom, 3 = 18:00 left."""
    import math
    a0, a1 = math.radians(-135 + i * 90), math.radians(-45 + i * 90)
    return f"M0 0L{r * math.cos(a0):.2f} {r * math.sin(a0):.2f}A{r} {r} 0 0 1 {r * math.cos(a1):.2f} {r * math.sin(a1):.2f}Z"


def mark(i, size, color, cls=''):
    """The hour mark: the dial as a line, one quarter lit."""
    return (f'<svg class="{cls}" viewBox="-52 -52 104 104" width="{size}" height="{size}" aria-hidden="true" style="display: block">'
            f'<path d="{wedge(i)}" fill="{color}"/><circle r="50" fill="none" stroke="{color}" stroke-width="2"/>'
            f'<line x1="-35.4" y1="-35.4" x2="35.4" y2="35.4" stroke="{color}" stroke-width="1.4" opacity=".7"/>'
            f'<line x1="35.4" y1="-35.4" x2="-35.4" y2="35.4" stroke="{color}" stroke-width="1.4" opacity=".7"/></svg>')


def dial(size):
    cols = [H00, H06, H12, H18]
    paths = ''.join(f'<path d="{wedge(i, 100)}" fill="{c}"/>' for i, c in enumerate(cols))
    return (f'<svg viewBox="-104 -104 208 208" width="{size}" height="{size}" aria-hidden="true" style="display: block">{paths}'
            f'<circle r="100" fill="none" stroke="{GOLD}" stroke-width="3"/><circle r="92" fill="none" stroke="{GON}" stroke-width=".8" opacity=".8"/></svg>')


def heb(text, size, color=INK, extra=''):
    return f'<div style="font-family: {HEB}; font-weight: 500; font-size: {size}px; line-height: 1.2; color: {color}; {extra}" dir="rtl">{text}</div>'


# ── HOOK (0–2.5): the pendant in the air, the certificate still blank ──
kf('hk', [(0, 'opacity:1'), (2.5, 'opacity:1'), (2.8, 'opacity:0')])
hook = f'''
<div class="hk stack" style="background: {STONE}">
  <img src="seq/land/f_001.jpg" alt="" class="cover" style="object-position: 50% 50%">
  <div class="stack" style="background: linear-gradient(180deg, rgba(239,232,221,.96) 0px, rgba(239,232,221,.85) 330px, rgba(239,232,221,0) 560px)"></div>
  <div style="position: absolute; top: 120px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: flex-start; gap: 18px" dir="rtl">
    <div style="{STAMP}; font-size: 34px; letter-spacing: .3em; color: {GTEXT}" dir="ltr">ENCORE°</div>
    {heb('באיזו שעה ענדת<br>אותו לראשונה?', 92)}
  </div>
  <div style="position: absolute; left: 230px; right: 230px; bottom: 120px; padding: 26px 0 30px; background: rgba(251,247,240,.94); outline: 1px solid {GLINE}; outline-offset: -10px; display: flex; flex-direction: column; align-items: center; gap: 6px">
    <div style="font-family: {SANS}; font-size: 26px; color: {GTEXT}" dir="rtl">תעודת שעה · נענד לראשונה</div>
    <div style="{STAMP}; font-size: 92px; color: {INK}" dir="ltr">-- : --</div>
  </div>
</div>'''

# ── LOGO (2.5–4.0) ─────────────────────────────────────────────────────
kf('lgline', [(0, 'transform:scaleX(0)'), (2.7, 'transform:scaleX(0)'), (3.5, 'transform:scaleX(1)')])
logo = f'''
<section class="scene" data-show="2.5,4.0" style="background: {H00}">
  <div style="position: absolute; top: 560px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 40px">
    <div data-in="2.5">{dial(260)}</div>
    <div style="{STAMP}; font-size: 120px; letter-spacing: .22em; padding-left: .22em; color: {GOLD}" dir="ltr">ENCORE°</div>
    <div class="lgline" style="width: 420px; height: 2px; background: {GOLD}"></div>
    <div data-in="2.9" style="font-family: {SERIF}; font-style: italic; font-size: 60px; color: {GON}" dir="ltr">La Première Heure</div>
  </div>
</section>'''

# ── THE STAMP (4.0–10.0): the pendant lands, the hour rolls to 12:14 and is signed ──
LAND0, LSTEP = 4.1, 0.06            # 72 frames → lands at ~8.4
TOUCH = 7.9
kf('m13', [(0, 'transform:translateY(0);opacity:1'), (TOUCH, 'transform:translateY(0);opacity:1'), (TOUCH + .35, 'transform:translateY(-100%);opacity:0')])
kf('m14', [(0, 'transform:translateY(100%);opacity:0'), (TOUCH, 'transform:translateY(100%);opacity:0'), (TOUCH + .35, 'transform:translateY(0);opacity:1')])
kf('press', [(0, 'transform:scale(1)'), (TOUCH + .35, 'transform:scale(1)'), (TOUCH + .5, 'transform:scale(1.08)'), (TOUCH + .7, 'transform:scale(1)')])
kf('cert', [(0, 'transform:translateY(1700px)'), (8.5, 'transform:translateY(1700px)'), (9.1, 'transform:translateY(0)')])
kf('noon', [(0, 'opacity:0'), (8.4, 'opacity:0'), (9.0, 'opacity:1')])
kf('qlit', [(0, 'opacity:0'), (TOUCH + .3, 'opacity:0'), (TOUCH + .6, 'opacity:1')])
stamp_scene = f'''
<section class="scene" data-show="4.0,10.2" style="background: {STONE}">
  <div class="stack" data-seq="seq/land/f_%03d.jpg" data-from="1" data-to="72" data-by="1" data-start="{LAND0}" data-step="{LSTEP}" data-fit="cover" data-pos="50% 50%"></div>
  <div class="stack" style="background: linear-gradient(180deg, rgba(239,232,221,.95) 0px, rgba(239,232,221,.8) 420px, rgba(239,232,221,0) 640px)"></div>
  <div style="position: absolute; top: 110px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 4px">
    <div data-in="4.3" style="font-family: {SANS}; font-size: 30px; color: {GTEXT}" dir="rtl">תעודת שעה · נענד לראשונה</div>
    <div class="press" style="position: relative; height: 150px; width: 640px; overflow: hidden">
      <div class="m13" style="position: absolute; inset: 0; text-align: center; {STAMP}; font-size: 136px; line-height: 150px; color: {INK}" dir="ltr">12 : 13</div>
      <div class="m14" style="position: absolute; inset: 0; text-align: center; {STAMP}; font-size: 136px; line-height: 150px; color: {INK}" dir="ltr">12 : 14</div>
    </div>
    <div style="position: relative; width: 70px; height: 70px">
      <div style="position: absolute; inset: 0">{mark(2, 70, GLINE)}</div>
    </div>
  </div>
  <div class="noon stack" style="background: {H12}"></div>
  <div class="cert" style="position: absolute; left: 110px; right: 110px; top: 330px; height: 1260px; background: {H12}; outline: 2px solid {GOLD}; outline-offset: -26px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 34px; color: {ON}">
    <div style="{STAMP}; font-size: 54px; letter-spacing: .3em; color: {GOLD}" dir="ltr">ENCORE°</div>
    <div class="qlit">{mark(2, 130, GOLD)}</div>
    <div style="font-family: {SERIF}; font-style: italic; font-size: 64px; color: {GON}" dir="ltr">Collier de midi</div>
    <div style="width: 120px; height: 2px; background: {GOLD}"></div>
    <div style="font-family: {SANS}; font-size: 34px; letter-spacing: .06em" dir="rtl">תעודת שעה · נענד לראשונה</div>
    <div style="{STAMP}; font-size: 150px; color: {GON}" dir="ltr">12 : 14</div>
    <div style="{STAMP}; font-size: 40px; color: {ON}; opacity: .85" dir="ltr">19 . 10 . 2026</div>
  </div>
  <div data-in="9.2" style="position: absolute; top: 120px; left: 0; right: 0; text-align: center">{heb('רשמנו את השעה.', 76, ON)}</div>
</section>'''

# ── FOUR CERTIFICATES (10–15): every hour has its piece ───────────────
HOURS = [('06:00', 'Bague de l\'aube', 'שחר · טבעות', H06, 1, 'rings-1'),
         ('12:00', 'Collier de midi', 'צהריים · שרשראות', H12, 2, 'pendants-2'),
         ('18:00', 'Bracelet du soir', 'שקיעה · צמידים', H18, 3, 'bracelets-1'),
         ('00:00', 'Boucles de minuit', 'לילה · עגילים', H00, 0, 'earrings-3')]
T0, DUR = 10.2, 1.2
bg = [(0, f'background-color:{HOURS[0][3]}')]
for k in range(1, 4):
    t = T0 + k * DUR
    bg += [(t - .25, f'background-color:{HOURS[k - 1][3]}'), (t, f'background-color:{HOURS[k][3]}')]
kf('hourbg', bg)
cards = ''
for k, (hr, fr, he, col, q, img) in enumerate(HOURS):
    a = T0 + k * DUR
    b = a + DUR if k < 3 else 15.2
    cards += f'''
  <div class="stack" data-show="{a - .05:.2f},{b - .1:.2f}" data-fade="0.2">
    <div style="position: absolute; left: 150px; right: 150px; top: 560px; height: 1060px; background: rgba(0,0,0,.08); outline: 2px solid {GOLD}; outline-offset: -22px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px">
      <img src="pieces/{img}.webp" alt="" style="height: 330px; width: auto; filter: drop-shadow(0 18px 24px rgba(0,0,0,.35))">
      {mark(q, 90, GOLD)}
      <div style="font-family: {SERIF}; font-style: italic; font-size: 56px; color: {GON}" dir="ltr">{fr}</div>
      <div style="{STAMP}; font-size: 96px; color: {GON}" dir="ltr">{hr[:2]} : {hr[3:]}</div>
      <div style="font-family: {SANS}; font-size: 32px; color: {ON}" dir="rtl">{he}</div>
    </div>
  </div>'''
four = f'''
<section class="scene" data-show="10.0,15.2">
  <div class="hourbg stack"></div>
  <div style="position: absolute; top: 150px; left: 80px; right: 80px; text-align: center">{heb('לכל שעה,<br>התכשיט שלה.', 84, ON)}</div>
  {cards}
</section>'''


# ── PHOTO SCENES: 18:00 · a year later · the sign ─────────────────────
def photo(name, a, b, img, push, stamp, line, sub, color, pos='50% 50%'):
    kf(f'push{name}', [(0, 'transform:scale(1.08)'), (a, 'transform:scale(1.08)'), (b + .3, 'transform:scale(1)')])
    stamp_html = f'<div style="{STAMP}; font-size: 56px; color: {GON}" dir="ltr">{stamp}</div>' if stamp else ''
    return f'''
<section class="scene" data-show="{a},{b}" style="background: {color}">
  <img class="push{name}" src="tp/{img}.jpg" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: {pos}">
  <div class="stack" style="background: linear-gradient(180deg, rgba(0,0,0,0) 900px, rgba(20,8,8,.55) 1350px, rgba(20,8,8,.82) 1920px)"></div>
  <div style="position: absolute; left: 80px; right: 80px; bottom: 140px; display: flex; flex-direction: column; align-items: flex-start; gap: 18px" dir="rtl">
    {stamp_html}
    <div data-in="{a + .3:.1f}">{heb(line, 80, ON)}</div>
    <div data-in="{a + .8:.1f}" style="font-family: {SERIF}; font-style: italic; font-size: 46px; color: {GON}" dir="ltr">{sub}</div>
  </div>
</section>'''


sunset = photo('s', 15.0, 19.2, 'tag-cuff', True, '18 : 00', 'הצמיד שראית<br>עוד מחכה לשעה שלו.', 'Bracelet du soir', H18)
year = photo('y', 19.0, 24.2, 'box-open', True, '12 : 14', 'שנה בדיוק.<br>אותה שעה.', "L'Anniversaire", H00)
sign = photo('g', 24.0, 27.2, 'sign', True, '', 'השעה<br>היא הלוגו.', 'ENCORE°', H00)

# ── OUTRO (27–30, holds) ───────────────────────────────────────────────
outro = f'''
<section class="scene" data-show="27.0,30" style="background: {STONE}">
  <div data-in="27.1" style="position: absolute; left: 230px; right: 230px; top: 260px; padding: 40px 0 44px; background: {H12}; outline: 2px solid {GOLD}; outline-offset: -16px; display: flex; flex-direction: column; align-items: center; gap: 14px; color: {ON}">
    <div style="{STAMP}; font-size: 34px; letter-spacing: .3em; color: {GOLD}" dir="ltr">ENCORE°</div>
    {mark(2, 70, GOLD)}
    <div style="font-family: {SERIF}; font-style: italic; font-size: 40px; color: {GON}" dir="ltr">Collier de midi</div>
    <div style="{STAMP}; font-size: 96px; color: {GON}" dir="ltr">12 : 14</div>
    <div style="{STAMP}; font-size: 28px; opacity: .85" dir="ltr">19 . 10 . 2026</div>
  </div>
  <div data-in="27.5" style="position: absolute; top: 1020px; left: 80px; right: 80px; text-align: center">{heb('רשמנו את השעה<br>שבה ענדת אותו לראשונה.', 76, INK, 'text-align: center')}</div>
  <div data-in="28.0" style="position: absolute; top: 1380px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 26px">
    <div style="padding: 30px 70px; background: {INK}; color: {PAPER}; font-family: {SANS}; font-size: 46px; font-weight: 500" dir="rtl">לבחור את השעה שלך</div>
    <div style="{STAMP}; font-size: 40px; letter-spacing: .3em; color: {GTEXT}" dir="ltr">ENCORE°</div>
  </div>
</section>'''

t = TEMPLATE.read_text(encoding='utf8')
head = t.split('/* ── STUDIO wrapper')[0].replace('<title>Brand World Reel</title>', '<title>ENCORE° · La Première Heure</title>')
head = head.replace('family=Cormorant+Garamond', 'family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Cormorant+Garamond', 1)
script = '<script>' + t.split('<script>', 1)[1]
html = head + '\n'.join(css) + f'''
#stage{{background:{STONE}}}
</style>
</head>
<body data-duration="30">
<div id="stage">
<div class="film stack">
{stamp_scene}
{four}
{sunset}
{year}
{sign}
{outro}
{logo}
{hook}
</div>
</div>
''' + script
(HERE / 'reel.html').write_text(html, encoding='utf8')
print('wrote', HERE / 'reel.html', len(html), 'bytes')
