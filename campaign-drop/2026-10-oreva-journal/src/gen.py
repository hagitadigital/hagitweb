#!/usr/bin/env python3
"""ORÉVA° · Le Journal des mains — brand-mode reel (9:16, 30s). Builds reel.html next to this file.

The hands move: two Kling clips (../kling/*.mp4) cut to 9:16 frame sequences by make_seq.sh; the bottle chapter plays
the world's own bloom sequence (assets/bottle, cut from oreva/assets/bloom) — the bottle alone, no hands.
Timeline (s): hook 0–3.0 · logo 3.0–4.4 · 01 the bed 4.4–9.6 · 02 the hand 9.6–13.6 · 03 the bottle 13.6–18.8 ·
the ribbon (signature) 18.8–26.6 · outro 26.6–30 (holds to the last frame).
"""
import pathlib

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE.parents[2] / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
P = lambda t: f"{max(0, min(D, t)) / D * 100:.3f}%"
css = []

CREAM, CREAM2, STONE, BLUSH = '#F6EFE7', '#FBF7F1', '#D9C7B3', '#EFCDBF'
COPPER, DEEP, INK, INK2 = '#B87A57', '#8F5A3C', '#3A2E29', '#6E5E55'
HEB = "'Frank Ruhl Libre', serif"
SERIF = "'Cormorant Garamond', 'Frank Ruhl Libre', serif"
SANS = "'Heebo', sans-serif"
PANEL = 700          # height of the cream panel above the moving hands
STEP = 1 / 12        # the sequences are 12 fps


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


def chapter(name, show, seq, start, frm, to, pos, opener, label, first, second, note=''):
    """A cream panel on top (opener, two-line headline), the copper ribbon, and the hands moving below it."""
    a, b = show
    kf(f'rib{name}', [(0, 'transform:scaleX(0)'), (a + .2, 'transform:scaleX(0)'), (a + 1.6, 'transform:scaleX(1)')])
    note_html = (f'<div data-in="{a + .9:.1f}" style="font-family: {SANS}; font-size: 36px; font-weight: 300; color: {INK2}" dir="rtl">{note}</div>'
                 if note else '')
    return f'''
<section class="scene" data-show="{a},{b}" style="background: {CREAM}">
  <div style="position: absolute; left: 0; right: 0; top: {PANEL}px; bottom: 0; overflow: hidden">
    <div class="stack" data-seq="{seq}" data-from="{frm}" data-to="{to}" data-by="1" data-start="{start}" data-step="{STEP:.4f}" data-fit="cover" data-pos="{pos}"></div>
  </div>
  <div style="position: absolute; left: 0; right: 0; top: 0; height: {PANEL}px; background: {CREAM}"></div>
  <div style="position: absolute; top: 150px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: flex-start; gap: 22px" dir="rtl">
    <div style="display: flex; align-items: center; gap: 16px">{bead(16)}<span style="font-family: {SERIF}; font-style: italic; font-size: 44px; color: {INK}" dir="ltr">{opener}</span><span style="font-family: {SANS}; font-size: 34px; color: {DEEP}">· {label}</span></div>
    {two_lines(first, second, 84)}
    {note_html}
  </div>
  <div style="position: absolute; left: 0; right: 0; top: {PANEL - 2}px; height: 0">
    <div class="rib{name}" style="position: absolute; left: 0; right: 30px; top: 0; height: 5px; background: {COPPER}; transform-origin: right"></div>
    <div style="position: absolute; right: 16px; top: -12px">{bead(28)}</div>
  </div>
</section>'''


# ── HOOK (0–3.0): the question over hands already moving ─────────────
kf('hk', [(0, 'opacity:1'), (3.0, 'opacity:1'), (3.3, 'opacity:0')])
hook = f'''
<div class="hk stack" style="background: {CREAM}">
  <div style="position: absolute; left: 0; right: 0; top: {PANEL}px; bottom: 0; overflow: hidden">
    <div class="stack" data-seq="seq/a/f_%03d.jpg" data-from="1" data-to="40" data-by="1" data-start="0" data-step="{STEP:.4f}" data-fit="cover" data-pos="50% 100%"></div>
  </div>
  <div style="position: absolute; top: 120px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: flex-start; gap: 26px" dir="rtl">
    <div style="display: flex; align-items: center; gap: 16px">{bead(16)}<span style="font-family: {SERIF}; font-size: 40px; letter-spacing: .3em; color: {INK}" dir="ltr">ORÉVA°</span></div>
    {two_lines('מאיפה הסרום', 'שלך הגיע?', 112)}
  </div>
  <div style="position: absolute; left: 0; right: 0; top: {PANEL - 2}px; height: 0">
    <div style="position: absolute; left: 0; right: 30px; top: 0; height: 5px; background: {COPPER}"></div>
    <div style="position: absolute; right: 16px; top: -12px">{bead(28)}</div>
  </div>
</div>'''

# ── LOGO (3.0–4.4) ─────────────────────────────────────────────────────
kf('lgrib', [(0, 'transform:scaleX(0)'), (3.1, 'transform:scaleX(0)'), (4.0, 'transform:scaleX(1)')])
logo = f'''
<section class="scene" data-show="3.0,4.4" style="background: {CREAM}">
  <div style="position: absolute; top: 780px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px">
    <div style="font-family: {SERIF}; font-size: 140px; letter-spacing: .3em; padding-left: .3em; color: {INK}" dir="ltr">ORÉVA°</div>
    <div style="font-family: {SERIF}; font-weight: 500; font-size: 40px; letter-spacing: .42em; padding-left: .42em; color: {DEEP}" dir="ltr">SKIN STUDIO</div>
  </div>
  <div style="position: absolute; left: 140px; right: 140px; top: 1130px; height: 0">
    <div class="lgrib" style="position: absolute; left: 0; right: 0; height: 4px; background: {COPPER}; transform-origin: right"></div>
    <div style="position: absolute; left: -14px; top: -12px">{bead(28)}</div>
  </div>
  <div data-in="3.3" style="position: absolute; top: 1220px; left: 0; right: 0; text-align: center; font-family: {SERIF}; font-style: italic; font-size: 54px; color: {INK}" dir="ltr">Le Journal des mains</div>
</section>'''

ch1 = chapter('1', (4.4, 9.6), 'seq/b/f_%03d.jpg', 4.5, 1, 61, '50% 55%', 'Le soin · 01', 'המיטה',
              'קודם על העור', 'של לקוחות הקליניקה.', 'חודשים לפני שיש לו שם.')
ch2 = chapter('2', (9.6, 13.6), 'seq/a/f_%03d.jpg', 9.7, 22, 61, '50% 100%', 'Le soin · 02', 'היד',
              'קודם הידיים.', 'אחר כך הבקבוק.')
ch3 = chapter('3', (13.6, 18.8), 'assets/bottle/f_%03d.jpg', 13.7, 1, 48, '50% 50%', 'Le soin · 03', 'הבקבוק',
              'ורק אז,', 'הבקבוק.', 'זכוכית בגוון סומק, ונחושת בראש.')

# ── THE RIBBON (18.8–26.6): one copper line from the bed, through the hand, to the bottle ──
RIB = ('M 1040 380 L 1040 760 C 1040 812, 1012 831, 960 831 L 116 831 C 64 831, 36 858, 36 910 '
       'L 36 1232 C 36 1284, 64 1311, 116 1311 L 966 1311 C 1018 1311, 1046 1338, 1046 1390 L 1046 1520 C 1046 1545, 1036 1551, 1012 1551')
R0, R1 = 19.3, 24.0
kf('rdraw', [(0, 'stroke-dashoffset:1'), (R0, 'stroke-dashoffset:1'), (R1, 'stroke-dashoffset:0')])
kf('rbead', [(0, 'offset-distance:0%;opacity:0'), (R0 - .05, 'offset-distance:0%;opacity:0'), (R0, 'offset-distance:0%;opacity:1'),
             (R1, 'offset-distance:100%;opacity:1')])
css.append('.rline{fill:none;stroke:%s;stroke-width:6;stroke-linecap:round;stroke-dasharray:1 1}' % COPPER)
wins = [  # (still, x, y, label, opener, appears)
    ('founder-facial-treatment', 330, 400, 'המיטה', 'Le soin · 01', 19.0),
    ('founder-cream-on-hand', 70, 880, 'היד', 'Le soin · 02', 21.3),
    ('bottle-f48', 330, 1360, 'הבקבוק', 'Le soin · 03', 23.3),
]
wh = ''
for i, (img, x, y, lab, op, t) in enumerate(wins):
    kf(f'w{i}', [(0, 'opacity:0;transform:scale(.94)'), (t, 'opacity:0;transform:scale(.94)'), (t + .6, 'opacity:1;transform:none')])
    side = f'left: {x + 700}px' if x < 200 else f'right: {1080 - x + 20}px'
    wh += f'''
  <div class="w{i}" style="position: absolute; left: {x}px; top: {y}px; width: 680px; height: 382px; border-radius: 22px; overflow: hidden; box-shadow: 0 24px 60px rgba(58,46,41,.18)">
    <img src="assets/{img}.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block">
  </div>
  <div class="w{i}" style="position: absolute; top: {y + 140}px; {side}; display: flex; flex-direction: column; align-items: {'flex-start' if x < 200 else 'flex-end'}; gap: 4px; width: 230px">
    <span style="font-family: {SERIF}; font-style: italic; font-size: 30px; color: {INK2}" dir="ltr">{op}</span>
    <span style="font-family: {HEB}; font-size: 52px; font-weight: 700; color: {DEEP}" dir="rtl">{lab}</span>
  </div>'''
ribbon = f'''
<section class="scene" data-show="18.8,26.6" style="background: radial-gradient(120% 70% at 80% 0%, #F5DED3 0%, {CREAM} 60%)">
  <div data-in="18.9" style="position: absolute; top: 110px; left: 80px; right: 80px">{two_lines('קו אחד,', 'מהיד עד הבקבוק.', 92)}</div>
  {wh}
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true" style="pointer-events: none"><path class="rline rdraw" pathLength="1" d="{RIB}"></path></svg>
  <div class="rbead" style="position: absolute; left: 0; top: 0; width: 40px; height: 40px; offset-path: path('{RIB}'); offset-rotate: 0deg">{bead(40)}</div>
</section>'''

# ── OUTRO (26.6–30, holds) ─────────────────────────────────────────────
kf('orib', [(0, 'transform:scaleX(0)'), (27.0, 'transform:scaleX(0)'), (28.0, 'transform:scaleX(1)')])
outro = f'''
<section class="scene" data-show="26.6,30" style="background: {CREAM}">
  <div data-in="26.7" style="position: absolute; top: 300px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px">
    <div style="font-family: {SERIF}; font-size: 120px; letter-spacing: .3em; padding-left: .3em; color: {INK}" dir="ltr">ORÉVA°</div>
    <div style="font-family: {SERIF}; font-weight: 500; font-size: 34px; letter-spacing: .42em; padding-left: .42em; color: {DEEP}" dir="ltr">SKIN STUDIO</div>
  </div>
  <div data-in="27.1" style="position: absolute; top: 760px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center">
    {two_lines('כל מוצר בליין יצא', 'קודם מהידיים שלי.', 84, 'text-align: center')}
    <div style="font-family: {SERIF}; font-style: italic; font-size: 46px; color: {INK2}" dir="ltr">Or Éva</div>
  </div>
  <div style="position: absolute; left: 140px; right: 140px; top: 1300px; height: 0">
    <div class="orib" style="position: absolute; left: 0; right: 0; height: 4px; background: {COPPER}; transform-origin: right"></div>
    <div style="position: absolute; left: -14px; top: -12px">{bead(28)}</div>
  </div>
  <div data-in="27.8" style="position: absolute; top: 1400px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 22px">
    <div style="padding: 30px 70px; border-radius: 14px; background: {INK}; color: {CREAM}; font-family: {SANS}; font-size: 46px; font-weight: 500" dir="rtl">לקבוע אבחון</div>
    <div style="font-family: {SANS}; font-size: 36px; font-weight: 300; color: {INK2}" dir="rtl">ארבעים דקות · בלי מוצרים · רק העור שלך</div>
  </div>
</section>'''

t = TEMPLATE.read_text(encoding='utf8')
head = t.split('/* ── STUDIO wrapper')[0].replace('<title>Brand World Reel</title>', '<title>ORÉVA° · Le Journal des mains</title>')
head = head.replace('family=Cormorant+Garamond', 'family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Cormorant+Garamond', 1)
script = '<script>' + t.split('<script>', 1)[1]
html = head + '\n'.join(css) + f'''
#stage{{background:{CREAM}}}
</style>
</head>
<body data-duration="30">
<div id="stage">
<div class="film stack">
{ch1}
{ch2}
{ch3}
{ribbon}
{outro}
{logo}
{hook}
</div>
</div>
''' + script
(HERE / 'reel.html').write_text(html, encoding='utf8')
print('wrote', HERE / 'reel.html', len(html), 'bytes')
