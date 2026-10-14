#!/usr/bin/env python3
"""Crema° Caffè Torino · World 20 — the world's 30s studio film (9:16; replaces the old 4:5 cut that read "26").

Hook (the site's own line): "יש לך מוצר שקונים כל שבוע, ומשווים אותו לפי מחיר?" over three generic capsule boxes.
Signature scene: Sette Mattine — the seven capsules on a clockwise dial around one cup; every capsule that reaches
the pointer turns the cup into its own roast (the site's cup photos), tints the morning and names the roast.
Then Il Rito (heart → rosetta), Le Capsule, and the promise: "קפה לא מוכרים כקפסולה. מוכרים אותו כבוקר."

    python3 reels/crema/build.py            -> reels/crema/reel.html
    node .claude/skills/brandos-brand-world-reel/scripts/render.js reels/crema/reel.html 30 reels/crema/out/CREMA-20.mp4
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TPL = ROOT / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
IMG = '../../images/crema/'


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


s = TPL.read_text()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


CREAM, CREAM2, INK, INK2, MUTED, COPPER_T = '#F4EBE0', '#EADCC9', '#2E1E16', '#4A3528', '#6B5641', '#87502C'
FR = "font-family: 'Frank Ruhl Libre', 'Heebo', serif"
CG = "font-family: 'Cormorant Garamond', serif"
AS = "font-family: 'Assistant', 'Heebo', sans-serif"
ROASTS = [  # key, name, it, colour, intensity, note — from crema.html
    ('ristretto', 'Ristretto', 'Espresso · Corto', '#D2382B', 5, 'עז ונועז. גוף מלא וסיומת של קקאו מריר.'),
    ('arancia', 'Arancia', 'Espresso · Agrumi', '#E07F2A', 3, 'קלייה חמה עם רמז בהיר של קליפת תפוז.'),
    ('miele', 'Miele', 'Lungo · Dolce', '#E3B23C', 2, 'רכה ומעוגלת, נגיעה של דבש וחמאה.'),
    ('foresta', 'Foresta', 'Espresso · Nocciola', '#4F9D58', 3, 'צלולה ורעננה, ניחוח אגוזי לוז עדין.'),
    ('onda', 'Onda', 'Espresso · Classico', '#3C84C2', 4, 'מאוזנת וחלקה, גוף קטיפתי ויומיומי.'),
    ('viola', 'Viola', 'Espresso · Floreale', '#7C5BAF', 4, 'עמוקה ופרחונית עם סיומת ארוכה.'),
    ('rosa', 'Rosa', 'Lungo · Fruttato', '#D24E86', 2, 'עדינה ופירותית, חמיצות קלילה ומרעננת.'),
]


def rgb(h):
    n = int(h[1:], 16)
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255]


def mix(a, b, t):
    x, y = rgb(a), rgb(b)
    return '#%02X%02X%02X' % tuple(round(v + (y[i] - v) * t) for i, v in enumerate(x))


CID = [0]


def capsule(color, w):
    """the site's capsuleSVG, verbatim geometry"""
    CID[0] += 1
    i = f'c{CID[0]}'
    return (f'<svg viewBox="0 0 120 156" width="{w}" height="{round(w * 1.3)}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><defs>'
            f'<linearGradient id="{i}b" x1=".15" y1="0" x2=".7" y2="1"><stop offset="0" stop-color="{mix(color, "#FFFFFF", .4)}"/><stop offset=".46" stop-color="{color}"/><stop offset="1" stop-color="{mix(color, "#000000", .34)}"/></linearGradient>'
            f'<radialGradient id="{i}l" cx=".38" cy=".32" r=".9"><stop offset="0" stop-color="{mix(color, "#FFFFFF", .62)}"/><stop offset="1" stop-color="{mix(color, "#FFFFFF", .05)}"/></radialGradient></defs>'
            f'<path d="M14 30 C14 92 30 152 60 152 C90 152 106 92 106 30 Z" fill="url(#{i}b)"/>'
            f'<path d="M25 38 C25 88 32 130 44 144 C35 120 31 78 34 42 Z" fill="#fff" opacity=".34"/>'
            f'<ellipse cx="60" cy="30" rx="50" ry="13" fill="{mix(color, "#FFFFFF", .16)}"/>'
            f'<ellipse cx="60" cy="30" rx="50" ry="13" fill="none" stroke="{mix(color, "#000000", .26)}" stroke-width="1.3" opacity=".55"/>'
            f'<ellipse cx="60" cy="27" rx="41" ry="9.5" fill="url(#{i}l)"/><ellipse cx="49" cy="23.5" rx="17" ry="3.4" fill="#fff" opacity=".62"/></svg>')


def dots(n, color):
    return ''.join(f'<i style="display: inline-block; width: 14px; height: 14px; border-radius: 50%; margin: 0 3px; background: {color if k < n else "rgba(46,30,22,.15)"}"></i>' for k in range(5))


rep('--w-bg:#F7F0E6;', f'--w-bg:{CREAM};')
rep('--w-ink:#3B2E33;', f'--w-ink:{INK};')
rep('--w-accent:#C9878E;', '--w-accent:#C28A5A;')
rep('<title>Brand World Reel</title>', '<title>Crema° reel</title>')
rep('&amp;family=Plus+Jakarta+Sans:wght@400;500', '&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;family=Frank+Ruhl+Libre:wght@300;400;500')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">20</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'בית קפה מטורינו, שבע קלייות על חוגה,<br>ובוקר אחד בגוון שלך.')
rep('BRAND° · עולם מותג NN', '<span dir="ltr">Crema°</span> · עולם מותג 20')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'קפה לא מוכרים כקפסולה.<br>מוכרים אותו <span style="color: var(--s-copper)">כבוקר</span>.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>מה מוכרים אצלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 20')

# ── HOOK: three generic capsule boxes, a price each ───────────────────
BOX = ('<svg viewBox="0 0 200 150" width="230" height="172" fill="none" stroke="#3A3633" stroke-width="4" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M20 50 L100 20 L180 50 L100 80 Z"/><path d="M20 50 V120 L100 150 V80"/><path d="M180 50 V120 L100 150"/>'
       '<ellipse cx="60" cy="98" rx="14" ry="5"/><ellipse cx="140" cy="98" rx="14" ry="5"/><path d="M48 104 q12 18 24 0 M128 104 q12 18 24 0"/></svg>')
GEN = [('10 קפסולות', '₪19.90'), ('10 קפסולות', '₪21.90'), ('10 קפסולות', '₪18.50')]
tiles = ''.join(f'<div style="width: 268px; box-sizing: border-box; padding: 22px 14px 18px; background: #F7F6F4; border-radius: 12px; display: flex; flex-direction: column; align-items: center; gap: 12px">'
                f'{BOX}<div style="display: flex; justify-content: space-between; width: 100%; font-size: 23px; color: #6E6660" dir="rtl"><span>{a}</span><strong style="color: #2E2A27">{b}</strong></div></div>' for a, b in GEN)
HOPS = [(0.0, 0.6, 2), (0.6, 1.1, 0), (1.1, 1.6, 1), (1.6, 2.1, 2), (2.1, 3.2, 0)]
hops = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.08"><div style="position: absolute; left: {i * 290 - 6}px; top: -6px; width: 280px; bottom: -6px; border: 4px solid var(--s-copper); border-radius: 16px"></div></div>' for a, b, i in HOPS)
HOOK_PROOF = f"""<div style="position: absolute; top: 700px; left: 80px; width: 920px; box-sizing: border-box; padding: 30px 32px 36px; background: #FFFFFF; border-radius: 22px; box-shadow: 0 24px 60px rgba(62,47,37,.14)" dir="rtl">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px"><span style="padding: 8px 20px; border-radius: 999px; background: #2E2A27; color: #F4F2EF; font-size: 24px">ככה משווים</span><span style="font-size: 24px; color: #8A827B">קפסולות קפה · 3 תוצאות</span></div>
    <div style="position: relative; display: flex; gap: 22px" dir="ltr">{tiles}{hops}</div>
  </div>"""
i = s.index('<div class="hq"')
j = s.index('<svg class="stack" width="1080" height="1920"', i)
s = s[:i] + (f'<div style="position: absolute; top: 250px; left: 80px; right: 80px; text-align: right; font-size: 70px; font-weight: 600; '
             f'line-height: 1.2; color: var(--s-dark)" dir="rtl">יש לך מוצר שקונים כל שבוע,<br>ומשווים אותו <span style="color: var(--s-copper)">לפי מחיר</span>?</div>\n  '
             + HOOK_PROOF + '\n\n  ') + s[j:]

# ── HUD ───────────────────────────────────────────────────────────────
tags = [('01 · The Core', 'הבוקר שלך, בגוון שלך'), ('02 · Sette Mattine', 'שבעה גוונים של בוקר אחד'),
        ('03 · Il Rito', 'ככה זה נראה בשש וחצי'), ('04 · Le Capsule', 'אוסף הקפסולות'),
        ('05 · The Promise', 'קפה נמכר כבוקר')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>')
    s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i)
    e = s.index('</span>', k)
    s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,16.0"'), ('data-show="14.7,18.7"', 'data-show="16.0,19.6"'),
             ('data-show="18.7,22.7"', 'data-show="19.6,23.1"'), ('data-show="22.7,30"', 'data-show="23.1,30"')]:
    rep(a, b)

css = []


def kf(name, frames, timing=None):
    body = ''.join(f'{P(t)}{{{v}}}' for t, v in frames)
    t_fn = f';animation-timing-function:{timing}' if timing else ''
    css.append(f'.{name}{{animation-name:{name}{t_fn}}}@keyframes {name}{{0%{{{frames[0][1]}}}{body}100%{{{frames[-1][1]}}}}}')


def reveal(name, t, dur=.55):
    css.append(f'.{name}{{animation-name:{name}}}@keyframes {name}{{0%,{P(t)}{{transform:translateY(110%)}}{P(t + dur)},100%{{transform:none}}}}')


BGD = f'<div class="stack" style="background: {CREAM}; background-image: radial-gradient(900px 800px at 50% 52%, #FBF5EE 0%, {CREAM} 70%)"></div>'

# ── A · The Core: seven capsules fan in, the promise ──────────────────
reveal('a-l1', 6.2)
reveal('a-l2', 6.65)
fan = ''
for k, r in enumerate(ROASTS):
    ang = (k - 3) * 15
    fan += (f'<div data-in="{2.7 + k * .12:.2f}" style="position: absolute; left: {540 - 70 + (k - 3) * 118}px; top: {860 + abs(k - 3) * 26}px; width: 140px">'
            f'<div style="transform: rotate({ang}deg); filter: drop-shadow(0 18px 18px rgba(46,30,22,.25))">{capsule(r[3], 140)}</div></div>')
A = f"""<section class="scene" data-show="0,10.1">
    {BGD}
    <div style="position: absolute; top: 230px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px">
      <div style="{AS}; font-size: 22px; font-weight: 600; letter-spacing: .4em; color: {COPPER_T}" dir="ltr">CAFFÈ IN CAPSULE · TORINO</div>
      <div style="{CG}; font-size: 150px; font-weight: 500; line-height: 1; color: {INK}" dir="ltr">Crema°</div>
    </div>
    {fan}
    <div style="position: absolute; bottom: 300px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="a-l1" style="display: block; {FR}; font-size: 90px; font-weight: 300; line-height: 1.15; color: {INK}">הבוקר שלך,</span></span>
      <span class="mask"><span class="a-l2" style="display: block; {FR}; font-size: 90px; font-weight: 500; line-height: 1.15; color: {COPPER_T}">בגוון שלך.</span></span>
    </div>
  </section>"""

# ── B · Sette Mattine: the dial of seven around one cup ───────────────
N = 7
STEP = 360 / N
STEPS = [10.5, 11.3, 12.1, 12.9, 13.7, 14.5]
MOVE, CX, CY, CUP, RR = .45, 540, 1030, 520, 440


def held(name, prop, vals):
    fr = [(9.7, f'{prop}:{vals[0]}')]
    for k, t in enumerate(STEPS):
        fr += [(t, f'{prop}:{vals[k]}'), (t + MOVE, f'{prop}:{vals[k + 1]}')]
    kf(name, fr)


held('b-ring', 'transform', [f'rotate({STEP * k:.3f}deg)' for k in range(N)])
held('b-cr', 'transform', [f'rotate({-STEP * k:.3f}deg)' for k in range(N)])
held('b-bg', 'background-color', [mix(r[3], CREAM, .82) for r in ROASTS])
wins = [(9.7, STEPS[0] + .3)] + [(t + .3, (STEPS[k + 1] + .3) if k < len(STEPS) - 1 else 16.2) for k, t in enumerate(STEPS)]
cups = ''.join(f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.28"><img class="cover" src="{IMG}cup-{r[0]}-heart.jpg" alt=""></div>' for r, (a, b) in zip(ROASTS, wins))
labels = ''.join(f'<div class="stack" data-show="{a + .12:.2f},{(b - .3) if b < 16 else b:.2f}" data-fade="0.16" style="display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center">'
                 f'<span style="{CG}; font-size: 76px; line-height: 1; color: {mix(r[3], "#000000", .25)}" dir="ltr">{r[1]}</span>'
                 f'<span style="{AS}; font-size: 26px; letter-spacing: .14em; color: {MUTED}" dir="ltr">{r[2].upper()}</span>'
                 f'<span style="{AS}; font-size: 32px; color: {INK2}" dir="rtl">{r[5]}</span><span>{dots(r[4], r[3])}</span></div>'
                 for r, (a, b) in zip(ROASTS, wins))
caps = ''.join(f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-STEP * k:.3f}deg) translateY(-{RR}px) rotate({STEP * k:.3f}deg)"><div class="b-cr" style="position: absolute; left: -48px; top: -62px; width: 96px; filter: drop-shadow(0 12px 14px rgba(46,30,22,.28))">{capsule(r[3], 96)}</div></div>'
               for k, r in enumerate(ROASTS))
reveal('b-l1', 9.9)
B = f"""<section class="scene" data-show="9.7,16.2">
    <div class="stack b-bg" style="background-color: {mix(ROASTS[0][3], CREAM, .82)}"></div>
    <div style="position: absolute; left: {CX - RR}px; top: {CY - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(46,30,22,.22); box-sizing: border-box"></div>
    <div style="position: absolute; left: {CX - CUP // 2}px; top: {CY - CUP // 2}px; width: {CUP}px; height: {CUP}px; border-radius: 50%; overflow: hidden; box-shadow: 0 30px 70px rgba(46,30,22,.3)">{cups}</div>
    <div class="b-ring" style="position: absolute; left: {CX}px; top: {CY}px; width: 0; height: 0">{caps}</div>
    <div style="position: absolute; top: {CY - RR - 104}px; left: {CX - 18}px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {INK}"></div>
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="9.8" style="{CG}; font-style: italic; font-size: 46px; color: {COPPER_T}" dir="ltr">Sette Mattine</div>
      <span class="mask"><span class="b-l1" style="display: block; {FR}; font-size: 74px; font-weight: 300; line-height: 1.2; color: {INK}">שבעה גוונים של בוקר אחד.</span></span>
    </div>
    <div style="position: absolute; top: 1560px; left: 40px; right: 40px; height: 260px">{labels}</div>
  </section>"""

# ── C · Il Rito: the pour decides the art — heart → rosetta ───────────
reveal('c-l1', 16.1)
kf('c-rot', [(16.0, 'transform:rotate(-6deg) scale(1.04)'), (19.8, 'transform:rotate(4deg) scale(1)')], 'linear')
C = f"""<section class="scene" data-show="16.0,19.8">
    {BGD}
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="16.0" style="{CG}; font-style: italic; font-size: 46px; color: {COPPER_T}" dir="ltr">La Tazza Vera</div>
      <span class="mask"><span class="c-l1" style="display: block; {FR}; font-size: 72px; font-weight: 300; line-height: 1.2; color: {INK}">ככה זה נראה בשש וחצי בבוקר.</span></span>
    </div>
    <div class="c-rot" style="position: absolute; left: 140px; top: 560px; width: 800px; height: 800px; border-radius: 50%; overflow: hidden; box-shadow: 0 40px 90px rgba(46,30,22,.3)">
      <img class="cover" src="{IMG}cup-foresta-heart.jpg" alt="">
      <div class="stack" data-show="17.9,30" data-fade="0.5"><img class="cover" src="{IMG}cup-foresta-rosetta.jpg" alt=""></div>
    </div>
    <div class="stack" data-show="16.4,17.9" data-fade="0.2" style="top: 1460px; height: 120px; text-align: center"><span style="{FR}; font-size: 48px; color: {INK2}" dir="rtl">Foresta · לב</span></div>
    <div class="stack" data-show="17.9,19.8" data-fade="0.2" style="top: 1460px; height: 120px; text-align: center"><span style="{FR}; font-size: 48px; color: {INK2}" dir="rtl">Foresta · רוזטה</span></div>
    <div data-in="16.6" style="position: absolute; top: 1560px; left: 90px; right: 90px; text-align: center; {AS}; font-size: 34px; line-height: 1.5; color: {MUTED}" dir="rtl">צבע הקפסולה עבר לפס על שפת הכוס,<br>והמזיגה קובעת את הציור בקצף.</div>
  </section>"""

# ── D · Le Capsule: the collection ────────────────────────────────────
cards = ''
for k, r in enumerate(ROASTS):
    col, row = k % 4, k // 4
    x = 812 - col * 245 - (122 if row else 0)
    y = 700 + row * 540
    cards += (f'<div data-in="{19.75 + k * .1:.2f}" style="position: absolute; left: {x}px; top: {y}px; width: 232px; box-sizing: border-box; padding: 26px 12px 22px; background: #FFFDF9; border-radius: 18px; '
              f'box-shadow: 0 16px 34px rgba(46,30,22,.12); display: flex; flex-direction: column; align-items: center; gap: 8px">'
              f'<div style="filter: drop-shadow(0 12px 14px rgba(46,30,22,.25))">{capsule(r[3], 128)}</div>'
              f'<span style="{CG}; font-size: 42px; line-height: 1; color: {mix(r[3], "#000000", .25)}" dir="ltr">{r[1]}</span>'
              f'<span style="{AS}; font-size: 17px; letter-spacing: .1em; color: {MUTED}" dir="ltr">{r[2].upper()}</span><span>{dots(r[4], r[3])}</span></div>')
D_ = f"""<section class="scene" data-show="19.6,23.3">
    {BGD}
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="19.7" style="{CG}; font-style: italic; font-size: 46px; color: {COPPER_T}" dir="ltr">Le Capsule</div>
      <div data-in="19.8" style="{FR}; font-size: 72px; font-weight: 300; line-height: 1.2; color: {INK}">אוסף הקפסולות.</div>
      <div data-in="20.0" style="{AS}; font-size: 32px; color: {MUTED}; margin-top: 8px">כל קלייה, צבע. כל צבע, בוקר.</div>
    </div>
    {cards}
  </section>"""

# ── E · The Promise ────────────────────────────────────────────────────
reveal('e-l1', 23.5)
reveal('e-l2', 23.9)
kf('e-spin', [(23.0, 'transform:rotate(0deg)'), (30, 'transform:rotate(40deg)')], 'linear')
ring = ''.join(f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-STEP * k:.3f}deg) translateY(-380px) rotate({STEP * k:.3f}deg)"><div style="position: absolute; left: -36px; top: -46px; width: 72px">{capsule(r[3], 72)}</div></div>' for k, r in enumerate(ROASTS))
E = f"""<section class="scene" data-show="23.0,30">
    {BGD}
    <div class="e-spin" style="position: absolute; left: 540px; top: 1000px; width: 0; height: 0; opacity: .9">{ring}</div>
    <div style="position: absolute; left: 290px; top: 750px; width: 500px; height: 500px; border-radius: 50%; overflow: hidden; box-shadow: 0 30px 70px rgba(46,30,22,.28)"><img class="cover" src="{IMG}cup-onda-rosetta.jpg" alt=""></div>
    <div style="position: absolute; top: 215px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="23.1" style="{CG}; font-size: 92px; font-weight: 500; line-height: 1; color: {INK}; margin-bottom: 18px" dir="ltr">Crema°</div>
      <span class="mask"><span class="e-l1" style="display: block; {FR}; font-size: 70px; font-weight: 300; line-height: 1.2; color: {INK}">קפה לא מוכרים כקפסולה.</span></span>
      <span class="mask"><span class="e-l2" style="display: block; {FR}; font-size: 70px; font-weight: 500; line-height: 1.2; color: {COPPER_T}">מוכרים אותו כבוקר.</span></span>
    </div>
  </section>"""

rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · Crema° ── */\n' + '\n'.join(css))
i = s.index('  <!-- A · The Core')
j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D_, E]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
(HERE / 'reel.html').write_text(s)
print('ok', len(s))
