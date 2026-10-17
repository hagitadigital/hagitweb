#!/usr/bin/env python3
"""ORÉVA° · Le Journal des mains — v2 (9:16, 30s). Builds reel2.html next to this file.

Full-bleed: every Kling clip once, the two-person shots pan from Or Éva to the client (make_seq2.sh).
The signature is a copper ribbon across the top with five beads — one per step — that light up in order,
from the diagnosis to the bottle, and stay lit in the outro.
Timeline (s): hook 0–3.0 · logo 3.0–4.2 · 01 diagnosis 4.2–8.6 · 02 the bed 8.6–13.2 · 03 showing the serum 13.2–16.6 ·
04 the box 16.6–21.0 · 05 the bottle 21.0–25.2 · outro 25.2–30 (holds to the last frame).
"""
import pathlib

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE.parents[2] / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
P = lambda t: f"{max(0, min(D, t)) / D * 100:.3f}%"
css = []

CREAM, COPPER, DEEP, INK, INK2 = '#F6EFE7', '#B87A57', '#8F5A3C', '#3A2E29', '#6E5E55'
HEB = "'Frank Ruhl Libre', serif"
SERIF = "'Cormorant Garamond', 'Frank Ruhl Libre', serif"
SANS = "'Heebo', sans-serif"
STEP = 1 / 12


def kf(name, stops):
    body = ''.join(f"{P(t)}{{{d}}}" for t, d in stops)
    css.append(f"@keyframes {name}{{0%{{{stops[0][1]}}}{body}100%{{{stops[-1][1]}}}}}")
    css.append(f".{name}{{animation-name:{name}}}")


def bead(size, extra=''):
    return (f'<span style="display: block; width: {size}px; height: {size}px; border-radius: 50%; '
            f'background: radial-gradient(circle at 35% 30%, #F6DCC9, {COPPER} 55%, #6E4128); {extra}"></span>')


def two_lines(first, second, size, extra=''):
    return (f'<div style="font-family: {HEB}; font-size: {size}px; line-height: 1.12; font-weight: 500; color: {INK}; {extra}" dir="rtl">'
            f'{first}<br><span style="font-weight: 700; color: {DEEP}">{second}</span></div>')


CH = [  # (seq, frames, start, end, opener, label, first, second, note)
    ('diag', 53, 4.2, 8.6, 'Le soin · 01', 'האבחון', 'ארבעים דקות', 'בלי מוצרים.', 'רק העור שלך, אור טבעי, ושאלות.'),
    ('bed', 61, 8.6, 13.2, 'Le soin · 02', 'המיטה', 'קודם על העור', 'של לקוחות הקליניקה.', 'חודשים לפני שיש לו שם.'),
    ('show', 37, 13.2, 16.6, 'Le soin · 03', 'ההסבר', 'שתי לחיצות,', 'בטפיחות.', 'מה, מתי, כמה.'),
    ('kit', 53, 16.6, 21.0, 'Le soin · 04', 'הקופסה', 'שלושה או ארבעה מוצרים,', 'לא שבעה.', 'ודף אחד בכתב יד.'),
    ('bottle', 48, 21.0, 25.2, 'Le soin · 05', 'הבקבוק', 'ורק אז,', 'הבקבוק.', 'זכוכית בגוון סומק, ונחושת בראש.'),
]
LABELS = [c[5] for c in CH]


def chapter(i, seq, n, a, b, opener, label, first, second, note):
    return f'''
<section class="scene" data-show="{a},{b}" style="background: {CREAM}">
  <div class="stack" data-seq="seq2/{seq}/f_%03d.jpg" data-from="1" data-to="{n}" data-by="1" data-start="{a + .05:.2f}" data-step="{STEP:.4f}" data-fit="cover" data-pos="50% 50%"></div>
  <div class="stack" style="background: linear-gradient(180deg, rgba(246,239,231,0) 1120px, rgba(246,239,231,.9) 1480px, rgba(246,239,231,.97) 1920px)"></div>
  <div style="position: absolute; left: 80px; right: 80px; bottom: 130px; display: flex; flex-direction: column; align-items: flex-start; gap: 18px" dir="rtl">
    <div data-in="{a + .2:.1f}" style="display: flex; align-items: center; gap: 14px">{bead(14)}<span style="font-family: {SERIF}; font-style: italic; font-size: 40px; color: {INK}" dir="ltr">{opener}</span><span style="font-family: {SANS}; font-size: 32px; color: {DEEP}">· {label}</span></div>
    <div data-in="{a + .35:.2f}">{two_lines(first, second, 80)}</div>
    <div data-in="{a + .8:.1f}" style="font-family: {SANS}; font-size: 36px; font-weight: 300; color: {INK2}" dir="rtl">{note}</div>
  </div>
</section>'''


# ── HOOK (0–3.0): the hands already moving, the question on top ──────
kf('hk', [(0, 'opacity:1'), (3.0, 'opacity:1'), (3.3, 'opacity:0')])
hook = f'''
<div class="hk stack" style="background: {CREAM}">
  <div class="stack" data-seq="seq2/hand/f_%03d.jpg" data-from="1" data-to="40" data-by="1" data-start="0" data-step="{STEP:.4f}" data-fit="cover" data-pos="50% 50%"></div>
  <div class="stack" style="background: linear-gradient(180deg, rgba(246,239,231,.95) 0px, rgba(246,239,231,.82) 300px, rgba(246,239,231,0) 540px)"></div>
  <div style="position: absolute; top: 80px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: flex-start; gap: 16px" dir="rtl">
    <div style="display: flex; align-items: center; gap: 14px">{bead(14)}<span style="font-family: {SERIF}; font-size: 38px; letter-spacing: .3em; color: {INK}" dir="ltr">ORÉVA°</span></div>
    {two_lines('מאיפה הסרום', 'שלך הגיע?', 92)}
  </div>
</div>'''

# ── LOGO (3.0–4.2) ─────────────────────────────────────────────────────
kf('lgrib', [(0, 'transform:scaleX(0)'), (3.1, 'transform:scaleX(0)'), (3.9, 'transform:scaleX(1)')])
logo = f'''
<section class="scene" data-show="3.0,4.2" style="background: {CREAM}">
  <div style="position: absolute; top: 790px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px">
    <div style="font-family: {SERIF}; font-size: 136px; letter-spacing: .3em; padding-left: .3em; color: {INK}" dir="ltr">ORÉVA°</div>
    <div style="font-family: {SERIF}; font-weight: 500; font-size: 38px; letter-spacing: .42em; padding-left: .42em; color: {DEEP}" dir="ltr">SKIN STUDIO</div>
  </div>
  <div style="position: absolute; left: 160px; right: 160px; top: 1130px; height: 0">
    <div class="lgrib" style="position: absolute; left: 0; right: 0; height: 4px; background: {COPPER}; transform-origin: right"></div>
    <div style="position: absolute; left: -14px; top: -12px">{bead(28)}</div>
  </div>
  <div style="position: absolute; top: 1210px; left: 0; right: 0; text-align: center; font-family: {SERIF}; font-style: italic; font-size: 52px; color: {INK}" dir="ltr">Le Journal des mains</div>
</section>'''

chapters = ''.join(chapter(i, *c) for i, c in enumerate(CH))

# ── OUTRO (25.2–30, holds) ─────────────────────────────────────────────
outro = f'''
<section class="scene" data-show="25.2,30" style="background: radial-gradient(120% 60% at 80% 0%, #F5DED3 0%, {CREAM} 58%)">
  <div data-in="25.4" style="position: absolute; top: 420px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px">
    <div style="font-family: {SERIF}; font-size: 120px; letter-spacing: .3em; padding-left: .3em; color: {INK}" dir="ltr">ORÉVA°</div>
    <div style="font-family: {SERIF}; font-weight: 500; font-size: 34px; letter-spacing: .42em; padding-left: .42em; color: {DEEP}" dir="ltr">SKIN STUDIO</div>
  </div>
  <div data-in="25.8" style="position: absolute; top: 820px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: center; gap: 20px">
    {two_lines('כל מוצר בליין יצא', 'קודם מהידיים שלי.', 84, 'text-align: center')}
    <div style="font-family: {SERIF}; font-style: italic; font-size: 46px; color: {INK2}" dir="ltr">Or Éva</div>
  </div>
  <div data-in="26.6" style="position: absolute; top: 1330px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 22px">
    <div style="padding: 30px 70px; border-radius: 14px; background: {INK}; color: {CREAM}; font-family: {SANS}; font-size: 46px; font-weight: 500" dir="rtl">לקבוע אבחון</div>
    <div style="font-family: {SANS}; font-size: 36px; font-weight: 300; color: {INK2}" dir="rtl">ארבעים דקות · בלי מוצרים · רק העור שלך</div>
  </div>
</section>'''

# ── THE RIBBON (4.0–30): one copper line, five beads, lit step by step ─
XS = [1000, 770, 540, 310, 80]           # bead centres, right to left (RTL)
Y = 150
starts = [c[2] for c in CH]
kf('rbar', [(0, 'opacity:0'), (3.9, 'opacity:0'), (4.3, 'opacity:1')])
prog = [(0, 'transform:scaleX(0)')]
for k, t in enumerate(starts):
    if k:
        prog.append((t - .1, f'transform:scaleX({(k - 1) / 4:.3f})'))
        prog.append((t + .5, f'transform:scaleX({k / 4:.3f})'))
kf('rprog', prog)
beads = ''
for k, (x, t, lab) in enumerate(zip(XS, starts, LABELS)):
    on = t + (.5 if k else .1)
    kf(f'bl{k}', [(0, 'opacity:0;transform:scale(.4)'), (on - .1, 'opacity:0;transform:scale(.4)'), (on + .15, 'opacity:1;transform:scale(1.25)'), (on + .4, 'opacity:1;transform:scale(1)')])
    kf(f'lb{k}', [(0, 'opacity:.55'), (on - .1, 'opacity:.55'), (on + .2, 'opacity:1')])
    beads += f'''
    <div style="position: absolute; left: {x - 13}px; top: {Y - 13}px; width: 26px; height: 26px; border-radius: 50%; border: 2px solid {COPPER}; box-sizing: border-box; background: {CREAM}"></div>
    <div class="bl{k}" style="position: absolute; left: {x - 15}px; top: {Y - 15}px">{bead(30)}</div>
    <div class="lb{k}" style="position: absolute; left: {x - 90}px; width: 180px; top: {Y + 28}px; text-align: center; font-family: {SANS}; font-size: 28px; font-weight: 500; color: {INK}" dir="rtl">{lab}</div>'''
ribbon = f'''
<div class="rbar stack" style="pointer-events: none">
  <div style="position: absolute; left: 0; right: 0; top: 0; height: 330px; background: linear-gradient(180deg, rgba(246,239,231,.94) 0px, rgba(246,239,231,.8) 170px, rgba(246,239,231,0) 330px)"></div>
  <div style="position: absolute; left: {XS[-1]}px; width: {XS[0] - XS[-1]}px; top: {Y - 1}px; height: 3px; background: rgba(184,122,87,.35)"></div>
  <div class="rprog" style="position: absolute; left: {XS[-1]}px; width: {XS[0] - XS[-1]}px; top: {Y - 2}px; height: 5px; background: {COPPER}; transform-origin: right"></div>
  {beads}
</div>'''

t = TEMPLATE.read_text(encoding='utf8')
head = t.split('/* ── STUDIO wrapper')[0].replace('<title>Brand World Reel</title>', '<title>ORÉVA° · Le Journal des mains · v2</title>')
head = head.replace('family=Cormorant+Garamond', 'family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Cormorant+Garamond', 1)
script = '<script>' + t.split('<script>', 1)[1]
html = head + '\n'.join(css) + f'''
#stage{{background:{CREAM}}}
</style>
</head>
<body data-duration="30">
<div id="stage">
<div class="film stack">
{chapters}
{outro}
{ribbon}
{logo}
{hook}
</div>
</div>
''' + script
(HERE / 'reel2.html').write_text(html, encoding='utf8')
print('wrote', HERE / 'reel2.html', len(html), 'bytes')
