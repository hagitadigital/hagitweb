#!/usr/bin/env python3
"""REGARD° · World 16 — the world's 30s studio film.

Hook: five generic frames on a shelf, and she leaves with nothing. Signature scene: La Lentille —
one lens that never moves, five frames on a clockwise dial around it; each frame that reaches the
pointer turns the face inside the lens into her with that frame, and the room takes its colour.
Then Le Fil (the frame falls down the copper thread onto her face, which comes into focus and lives),
La Boutique, and the promise.

Fills the brandos-brand-world-reel template. Every timing lives here, in seconds.
    python3 regard/reel/build.py            -> regard/reel/reel.html
Render (from the repo root):
    node .claude/skills/brandos-brand-world-reel/scripts/render.js regard/reel/reel.html 30 regard/reel/out/REGARD-16.mp4
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TPL = ROOT / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


s = TPL.read_text()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# ── palette, from regard/index.html :root ─────────────────────────────
NAVY, NAVY2, CREAM, COPPER = '#0C1420', '#121E2C', '#F2EBDC', '#C28A5A'
MUTED = 'rgba(242,235,220,.66)'
FR = "font-family: 'Frank Ruhl Libre', 'Heebo', serif"
CG = "font-family: 'Cormorant Garamond', serif"
AS = "font-family: 'Assistant', 'Heebo', sans-serif"
PORT = '../assets/portraits/'

MODELS = [  # name, accent, line from the site, pose from the site
    ('La Muse', '#D9A8A2', 'היא לא מחפשת את האור. האור מחפש אותה.', 'מבט רך הצידה, חצי חיוך — מוארת', '01-la-muse'),
    ("L'Icône", '#D6C7A9', 'נכנסת לחדר. השאר היסטוריה.', 'פרונטלית, סנטר מעט למטה — לא מתנצלת', '02-licone'),
    ('La Poète', '#C89A6B', 'רואה את מה שאחרים פספסו.', 'שלושת-רבעי, מבט למעלה — חולמת', '03-la-poete'),
    ('La Directrice', '#8FA6C0', 'ההחלטה כבר התקבלה. עכשיו רק מנסחים אותה.', 'ישרה, כתפיים פתוחות — סמכותית', '04-la-directrice'),
    ("L'Étoile", '#C99A4F', 'כשהיא מסתכלת עלייך — את מרגישה נבחרת.', 'מבט מעבר לכתף — נבחרת', '05-letoile'),
]
PRICES = [240, 280, 260, 250, 320]

# ── template blocks ───────────────────────────────────────────────────
rep('--w-bg:#F7F0E6;', f'--w-bg:{NAVY};')
rep('--w-ink:#3B2E33;', f'--w-ink:{CREAM};')
rep('--w-accent:#C9878E;', f'--w-accent:{COPPER};')
rep('<title>Brand World Reel</title>', '<title>REGARD° reel</title>')
rep('&amp;family=Plus+Jakarta+Sans:wght@400;500', '&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;family=Frank+Ruhl+Libre:wght@300;400;500')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">16</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'בית אופטיקה שבו העדשה לא זזה.<br>העולם שעובר דרכה מתחלף.')
rep('BRAND° · עולם מותג NN', '<span dir="ltr">REGARD°</span> · עולם מותג 16')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'כי היא לא בחרה משקפיים.<br>היא בחרה <span style="color: var(--s-copper)">מבט</span>.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>מה בוחרים אצלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 16')

# ── HOOK: five generic frames on a shelf; one by one she puts them back ──
GEN = [  # generic catalogue frames, plain line drawings (never the world's own frames)
    '<circle cx="55" cy="42" r="30"/><circle cx="145" cy="42" r="30"/><path d="M85 40 Q100 30 115 40"/><path d="M25 38 L4 30 M175 38 L196 30"/>',
    '<rect x="16" y="18" width="74" height="48" rx="6"/><rect x="110" y="18" width="74" height="48" rx="6"/><path d="M90 34 H110"/><path d="M16 26 L2 22 M184 26 L198 22"/>',
    '<path d="M18 26 Q52 12 88 24 L84 56 Q52 70 24 58 Z"/><path d="M182 26 Q148 12 112 24 L116 56 Q148 70 176 58 Z"/><path d="M88 32 Q100 26 112 32"/>',
    '<path d="M20 22 H86 Q90 54 62 66 Q30 70 22 46 Z"/><path d="M180 22 H114 Q110 54 138 66 Q170 70 178 46 Z"/><path d="M86 26 H114 M86 34 H114"/>',
    '<rect x="14" y="14" width="78" height="56" rx="16"/><rect x="108" y="14" width="78" height="56" rx="16"/><path d="M92 36 Q100 30 108 36"/>',
]
GEN_PRICE = ['₪290', '₪340', '₪260', '₪310', '₪280']
GEN_CODE = ['דגם 1042', 'דגם 2210', 'דגם 0871', 'דגם 3305', 'דגם 1519']
X_AT = [0.7, 1.05, 1.4, 1.75, 2.1]


def tile(i):
    return f"""<div style="position: relative; width: 254px; height: 250px; box-sizing: border-box; padding: 26px 18px 18px; background: #F7F6F4; border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between">
      <svg viewBox="0 0 200 84" width="218" height="92" fill="none" stroke="#3A3633" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{GEN[i]}</svg>
      <div style="display: flex; justify-content: space-between; font-size: 23px; color: #6E6660" dir="rtl"><span>{GEN_CODE[i]}</span><strong style="color: #2E2A27">{GEN_PRICE[i]}</strong></div>
      <div data-show="{X_AT[i]},30" data-fade="0.18" style="position: absolute; inset: 0; border-radius: 12px; background: rgba(247,246,244,.72); display: flex; align-items: center; justify-content: center">
        <span style="width: 74px; height: 74px; border-radius: 50%; background: #2E2A27; color: #F4F2EF; font-size: 40px; line-height: 74px; text-align: center">✕</span></div>
    </div>"""


HOOK_PROOF = f"""<div style="position: absolute; top: 640px; left: 80px; width: 920px; box-sizing: border-box; padding: 34px 30px 40px; background: #FFFFFF; border-radius: 22px; box-shadow: 0 24px 60px rgba(62,47,37,.14)" dir="rtl">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 26px"><span style="padding: 8px 20px; border-radius: 999px; background: #2E2A27; color: #F4F2EF; font-size: 24px">ככה משווים</span><span style="font-size: 24px; color: #8A827B">מסגרות לנשים · 5 תוצאות</span></div>
    <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 22px">{''.join(tile(i) for i in range(5))}</div>
  </div>"""
i = s.index('<div class="hq"')
j = s.index('<svg class="stack" width="1080" height="1920"', i)
s = s[:i] + (f'<div style="position: absolute; top: 250px; left: 80px; right: 80px; text-align: right; font-size: 76px; font-weight: 600; '
             f'line-height: 1.18; color: var(--s-dark)" dir="rtl">חמש מסגרות על המדף.<br>למה היא יוצאת <span style="color: var(--s-copper)">בלי כלום</span>?</div>\n  '
             + HOOK_PROOF + '\n\n  ') + s[j:]

# ── HUD ───────────────────────────────────────────────────────────────
tags = [('01 · The Core', 'את מחליפה את המבט'), ('02 · La Lentille', 'עדשה אחת, חמישה מבטים'),
        ('03 · Le Fil', 'המסגרת נוחתת על הפנים'), ('04 · La Boutique', 'לקחת מבט הביתה'),
        ('05 · The Promise', 'אותם פנים. המבט מתחלף.')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>')
    s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i)
    e = s.index('</span>', k)
    s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,15.6"'), ('data-show="14.7,18.7"', 'data-show="15.6,19.5"'),
             ('data-show="18.7,22.7"', 'data-show="19.5,23.0"'), ('data-show="22.7,30"', 'data-show="23.0,30"')]:
    rep(a, b)

css = []


def held(name, prop, stops, first):
    """keyframes that arrive at each value and hold it until the next move (recipe 16)"""
    kf = f'0%,{P(stops[0][0])}{{{prop}:{first}}}'
    for k, (t0, t1, v) in enumerate(stops):
        nxt = P(stops[k + 1][0]) if k + 1 < len(stops) else '100%'
        kf += f'{P(t1)},{nxt}{{{prop}:{v}}}'
    css.append(f'.{name}{{animation-name:{name}}}@keyframes {name}{{{kf}}}')


def reveal(name, t, dur=.55):
    css.append(f'.{name}{{animation-name:{name}}}@keyframes {name}{{0%,{P(t)}{{transform:translateY(110%)}}{P(t + dur)},100%{{transform:none}}}}')


GT = f'<div style="position: absolute; left: 0; right: 0; top: 0; height: 560px; background: linear-gradient(to bottom, rgba(12,20,32,.96) 40%, rgba(12,20,32,0))"></div>'
GB = f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 640px; background: linear-gradient(to top, rgba(12,20,32,.97) 46%, rgba(12,20,32,0))"></div>'
BG = (f'<div class="stack" style="background: {NAVY}; background-image: radial-gradient(900px 700px at 50% 52%, #1A2838 0%, {NAVY} 70%)"></div>')


def lens_ring(cx, cy, r):
    return (f'<div style="position: absolute; left: {cx - r - 14}px; top: {cy - r - 14}px; width: {2 * r + 28}px; height: {2 * r + 28}px; border-radius: 50%; '
            f'box-shadow: 0 0 0 2px {COPPER}, 0 0 90px rgba(194,138,90,.28); pointer-events: none"></div>'
            f'<div style="position: absolute; left: {cx - r}px; top: {cy - r}px; width: {2 * r}px; height: {2 * r}px; border-radius: 50%; '
            f'background: radial-gradient(circle at 34% 24%, rgba(255,255,255,.16), rgba(255,255,255,0) 34%); pointer-events: none"></div>')


# ── A · The Core: the lens that never moves, frames pass through it ─────
LX, LY, LR = 540, 960, 290
OUT_W, OUT_GAP, IN_W, IN_GAP = 250, 270, 470, 460
A_STOPS = [(6.3, 6.8), (7.5, 8.0), (8.7, 9.2)]
held('a-out', 'transform', [(a, b, f'translateY(-{(k + 1) * OUT_GAP}px)') for k, (a, b) in enumerate(A_STOPS)], 'translateY(0)')
held('a-in', 'transform', [(a, b, f'translateY(-{(k + 1) * IN_GAP}px)') for k, (a, b) in enumerate(A_STOPS)], 'translateY(0)')
reveal('a-l1', 6.0)
reveal('a-l2', 6.5)
outer = ''.join(f'<img src="img/f{i + 1}.webp" alt="" style="position: absolute; left: {LX - OUT_W // 2}px; top: {LY + i * OUT_GAP - 55}px; width: {OUT_W}px; opacity: .42">' for i in range(5))
inner = ''.join(f'<img src="img/f{i + 1}.webp" alt="" style="position: absolute; left: {LR - IN_W // 2}px; top: {LR + i * IN_GAP - 100}px; width: {IN_W}px; filter: drop-shadow(0 26px 34px rgba(0,0,0,.55))">' for i in range(5))
A = f"""<section class="scene" data-show="0,10.1">
    {BG}
    <div style="position: absolute; left: {LX}px; top: 0; bottom: 0; width: 1px; background: linear-gradient(to bottom, transparent, {COPPER} 20%, {COPPER} 80%, transparent); opacity: .45"></div>
    <div class="stack a-out">{outer}</div>
    <div style="position: absolute; left: {LX - LR}px; top: {LY - LR}px; width: {2 * LR}px; height: {2 * LR}px; border-radius: 50%; overflow: hidden; background: radial-gradient(circle at 50% 40%, #243447, #101A27 72%)">
      <div class="stack a-in">{inner}</div>
    </div>
    {lens_ring(LX, LY, LR)}
    {GT}{GB}
    <div style="position: absolute; top: 190px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 16px">
      <div style="{AS}; font-size: 22px; font-weight: 600; letter-spacing: .42em; color: {COPPER}" dir="ltr">MAISON D'OPTIQUE · Nº 16</div>
      <div style="{CG}; font-size: 128px; font-weight: 400; line-height: 1; letter-spacing: .08em; color: {CREAM}" dir="ltr">REGARD<sup style="font-size: .32em; vertical-align: 1.6em; color: {COPPER}">°</sup></div>
    </div>
    <div style="position: absolute; bottom: 230px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="a-l1" style="display: block; {FR}; font-size: 74px; font-weight: 300; line-height: 1.2; color: {CREAM}">את לא מחליפה משקפיים.</span></span>
      <span class="mask"><span class="a-l2" style="display: block; {FR}; font-size: 74px; font-weight: 500; line-height: 1.2; color: {COPPER}">את מחליפה את המבט.</span></span>
      <div data-in="7.3" style="margin-top: 20px; {AS}; font-size: 32px; font-weight: 300; color: {MUTED}">איך את רואה, ואיך רואים אותך.</div>
    </div>
  </section>"""

# ── B · La Lentille: five frames on a clockwise dial, the face in the lens changes ──
BX, BY, BR, RR = 540, 1010, 280, 432
STEPS = [10.8, 11.8, 12.8, 13.8]           # the ring turns 72° clockwise at each stop
MOVE = .45
held('b-ring', 'transform', [(t, t + MOVE, f'rotate({72 * (k + 1)}deg)') for k, t in enumerate(STEPS)], 'rotate(0deg)')
held('b-cr', 'transform', [(t, t + MOVE, f'rotate({-72 * (k + 1)}deg)') for k, t in enumerate(STEPS)], 'rotate(0deg)')
held('b-wash', 'background-color', [(t + .1, t + MOVE + .1, MODELS[k + 1][1]) for k, t in enumerate(STEPS)], MODELS[0][1])
held('b-ptr', 'border-top-color', [(t + .1, t + MOVE + .1, MODELS[k + 1][1]) for k, t in enumerate(STEPS)], MODELS[0][1])
reveal('b-l1', 9.9)
reveal('b-l2', 10.25)
wins = [(9.7, STEPS[0] + .35)] + [(t + .35, (STEPS[k + 1] + .35) if k < 3 else 15.8) for k, t in enumerate(STEPS)]
faces = ''.join(f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.3"><img class="cover" src="{PORT}{m[4]}.webp" alt="" style="object-position: 50% 30%; transform: scale(1.08)"></div>'
                for m, (a, b) in zip(MODELS, wins))
labels = ''.join(f"""<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.22" style="display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center"><span style="{CG}; font-style: italic; font-size: 76px; line-height: 1; color: {m[1]}" dir="ltr">{m[0]}</span><span style="{FR}; font-size: 36px; font-weight: 300; color: {CREAM}" dir="rtl">{m[2]}</span></div>"""
                 for m, (a, b) in zip(MODELS, wins))
medals = ''.join(f"""<div style="position: absolute; left: 0; top: 0; transform: rotate({-72 * i}deg) translateY(-{RR}px) rotate({72 * i}deg)"><div class="b-cr" style="position: absolute; left: -100px; top: -50px; width: 200px; height: 100px; display: flex; align-items: center; justify-content: center"><img src="img/f{i + 1}.webp" alt="{m[0]}" style="width: 196px; filter: drop-shadow(0 12px 18px rgba(0,0,0,.5))"></div></div>"""
                 for i, m in enumerate(MODELS))
B = f"""<section class="scene" data-show="9.7,15.8">
    {BG}
    <div class="stack b-wash" style="background-color: {MODELS[0][1]}; opacity: .30; -webkit-mask-image: radial-gradient(ellipse 62% 44% at 50% 53%, #000 0%, transparent 100%); mask-image: radial-gradient(ellipse 62% 44% at 50% 53%, #000 0%, transparent 100%)"></div>
    <div style="position: absolute; left: {BX - RR}px; top: {BY - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 1.5px dashed rgba(194,138,90,.5); box-sizing: border-box"></div>
    <div style="position: absolute; left: {BX - BR}px; top: {BY - BR}px; width: {2 * BR}px; height: {2 * BR}px; border-radius: 50%; overflow: hidden; background: {NAVY2}">{faces}</div>
    {lens_ring(BX, BY, BR)}
    <div class="b-ring" style="position: absolute; left: {BX}px; top: {BY}px; width: 0; height: 0">{medals}</div>
    <div class="b-ptr" style="position: absolute; top: {BY - RR - 96}px; left: {BX - 18}px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {MODELS[0][1]}"></div>
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="9.8" style="{CG}; font-style: italic; font-size: 44px; color: {COPPER}; margin-bottom: 6px" dir="ltr">La Lentille</div>
      <span class="mask"><span class="b-l1" style="display: block; {FR}; font-size: 66px; font-weight: 300; line-height: 1.18; color: {CREAM}">העדשה לא זזה.</span></span>
      <span class="mask"><span class="b-l2" style="display: block; {FR}; font-size: 66px; font-weight: 500; line-height: 1.18; color: {COPPER}">העולם שעובר דרכה מתחלף.</span></span>
    </div>
    <div style="position: absolute; top: 1560px; left: 40px; right: 40px; height: 170px">{labels}</div>
  </section>"""

# ── C · Le Fil: La Directrice falls down the copper thread onto her face ──
CX, CY, CRAD = 540, 1090, 300
EYE = CY - CRAD + int(2 * CRAD * .45)
THREAD = f'M 120 520 C 260 760, 640 640, {CX} {EYE}'
FW = int(2 * CRAD * .74)
css.append(f'.c-th{{animation-name:cth;animation-timing-function:linear}}@keyframes cth{{0%,{P(15.5)}{{stroke-dashoffset:1}}{P(16.6)},100%{{stroke-dashoffset:0}}}}')
css.append(f'.c-tr{{animation-name:ctr;animation-timing-function:cubic-bezier(.45,0,.3,1)}}@keyframes ctr{{0%,{P(15.7)}{{offset-distance:0%;opacity:0}}{P(15.8)}{{opacity:1}}{P(16.9)}{{offset-distance:100%;opacity:1}}{P(17.45)},100%{{offset-distance:100%;opacity:0}}}}')
css.append(f'.c-sp{{animation-name:csp;animation-timing-function:cubic-bezier(.45,0,.3,1)}}@keyframes csp{{0%,{P(15.7)}{{transform:rotate(-200deg) scale(.55)}}{P(16.9)}{{transform:rotate(0deg) scale(1)}}{P(17.45)},100%{{transform:scale(1.4)}}}}')
css.append(f'.c-face{{animation-name:cface}}@keyframes cface{{0%,{P(16.85)}{{filter:blur(16px) brightness(.38) saturate(.6);transform:scale(1.1)}}{P(17.6)},100%{{filter:none;transform:none}}}}')
reveal('c-l1', 15.5)
reveal('c-l2', 15.85)
C = f"""<section class="scene" data-show="15.5,19.6">
    {BG}
    <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="c-th" pathLength="1" d="{THREAD}" fill="none" stroke="{COPPER}" stroke-width="3" stroke-dasharray="1 1" opacity=".75"/></svg>
    <div style="position: absolute; left: {CX - CRAD}px; top: {CY - CRAD}px; width: {2 * CRAD}px; height: {2 * CRAD}px; border-radius: 50%; overflow: hidden; background: {NAVY2}">
      <div class="stack c-face"><div class="stack" data-seq="seq/d_%03d.jpg" data-from="1" data-to="41" data-start="17.35" data-step="0.05" data-pos="50% 26%"></div></div>
    </div>
    {lens_ring(CX, CY, CRAD)}
    <div class="c-tr" style="position: absolute; left: 0; top: 0; width: {FW}px; height: {int(FW * 303 / 840)}px; offset-path: path('{THREAD}'); offset-rotate: 0deg">
      <img class="c-sp" src="img/f4.webp" alt="" style="width: 100%; height: 100%; display: block; filter: drop-shadow(0 24px 30px rgba(0,0,0,.55))">
    </div>
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="15.5" style="{CG}; font-style: italic; font-size: 44px; color: {COPPER}; margin-bottom: 6px" dir="ltr">Le Fil</div>
      <span class="mask"><span class="c-l1" style="display: block; {FR}; font-size: 62px; font-weight: 300; line-height: 1.2; color: {CREAM}">מה משתנה כשהיא מרכיבה את</span></span>
      <span class="mask"><span class="c-l2" style="display: block; {CG}; font-style: italic; font-size: 84px; line-height: 1.1; color: {MODELS[3][1]}" dir="ltr">La Directrice?</span></span>
    </div>
    <div data-in="17.6" style="position: absolute; top: 1470px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center" dir="rtl">
      <div style="{AS}; font-size: 28px; color: {MUTED}"><span dir="ltr">Nº 04</span> · ישרה, כתפיים פתוחות — סמכותית</div>
      <div style="{FR}; font-size: 48px; font-weight: 300; line-height: 1.3; color: {CREAM}">ההחלטה כבר התקבלה.<br><b style="font-weight: 500; color: {MODELS[3][1]}">עכשיו רק מנסחים אותה.</b></div>
    </div>
  </section>"""

# ── D · La Boutique ─────────────────────────────────────────────────────
ADD_AT = 21.3


def card(i, x, y):
    m = MODELS[i]
    btn = (f'<div style="position: relative; height: 54px; margin-top: 14px">'
           f'<div class="stack" data-show="0,{ADD_AT}" data-fade="0.15" style="display: flex; align-items: center; justify-content: center; border: 1.5px solid rgba(194,138,90,.7); border-radius: 999px; {AS}; font-size: 22px; font-weight: 600; color: {CREAM}">הוספה לסל</div>'
           + (f'<div class="stack" data-show="{ADD_AT},30" data-fade="0.15" style="display: flex; align-items: center; justify-content: center; background: {COPPER}; border-radius: 999px; {AS}; font-size: 22px; font-weight: 600; color: {NAVY}">נוסף לסל ✓</div>' if i == 3 else '')
           + '</div>')
    return (f'<div data-in="{19.55 + i * .14:.2f}" style="position: absolute; left: {x}px; top: {y}px; width: 300px; box-sizing: border-box; padding: 30px 24px 26px; '
            f'background: {NAVY2}; border: 1px solid rgba(242,235,220,.12); border-radius: 10px; display: flex; flex-direction: column; align-items: center; text-align: center">'
            f'<div style="height: 120px; display: flex; align-items: center"><img src="img/f{i + 1}.webp" alt="{m[0]}" style="width: 244px; filter: drop-shadow(0 14px 18px rgba(0,0,0,.5))"></div>'
            f'<div style="{CG}; font-size: 20px; letter-spacing: .3em; color: {COPPER}; margin-top: 14px" dir="ltr">Nº 0{i + 1}</div>'
            f'<div style="{CG}; font-style: italic; font-size: 44px; line-height: 1.1; color: {m[1]}" dir="ltr">{m[0]}</div>'
            f'<div style="{AS}; font-size: 26px; color: {CREAM}; margin-top: 6px" dir="ltr">€ {PRICES[i]}</div>{btn}</div>')


css.append(f'.d-fab{{animation-name:dfab}}@keyframes dfab{{0%,{P(ADD_AT + .1)}{{transform:scale(1)}}{P(ADD_AT + .3)}{{transform:scale(1.18)}}{P(ADD_AT + .55)},100%{{transform:scale(1)}}}}')
DD = f"""<section class="scene" data-show="19.3,23.3">
    {BG}
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center" dir="rtl">
      <div data-in="19.4" style="{CG}; font-style: italic; font-size: 44px; color: {COPPER}" dir="ltr">La Boutique</div>
      <div data-in="19.55" style="{FR}; font-size: 66px; font-weight: 300; line-height: 1.2; color: {CREAM}">בחרי את המבט שלך.<br><b style="font-weight: 500; color: {COPPER}">קחי אותו איתך.</b></div>
    </div>
    {card(0, 750, 600)}{card(1, 390, 600)}{card(2, 30, 600)}{card(3, 570, 1080)}{card(4, 210, 1080)}
    <div data-in="20.3" style="position: absolute; top: 1580px; left: 80px; right: 80px; text-align: center; {AS}; font-size: 30px; font-weight: 300; color: {MUTED}" dir="rtl">כל מסגרת מגיעה בקופסת נייבי עם חוט נחושת.</div>
    <div class="d-fab" style="position: absolute; left: 70px; top: 1680px; width: 96px; height: 96px; border-radius: 50%; border: 1.5px solid {COPPER}; display: flex; align-items: center; justify-content: center">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="{CREAM}" stroke-width="1.6" aria-hidden="true"><path d="M5 8h14l-1.4 11H6.4z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>
      <div data-show="{ADD_AT + .1},30" data-fade="0.15" style="position: absolute; top: -6px; right: -6px; width: 40px; height: 40px; border-radius: 50%; background: {COPPER}; color: {NAVY}; {AS}; font-weight: 700; font-size: 22px; line-height: 40px; text-align: center">1</div>
    </div>
  </section>"""

# ── E · The Promise: the same face, five gazes ─────────────────────────
order = [(4, -2), (2, -1), (0, 0), (1, 1), (3, 2)]   # (model, slot); centre = La Muse
fan = ''
for m_i, slot in sorted(order, key=lambda o: -abs(o[1])):
    sc = [1, .8, .66][abs(slot)]
    w, h = int(360 * sc), int(482 * sc)
    x = 540 + slot * 200 - w // 2
    y = 980 - h // 2
    fan += (f'<div data-in="{23.1 + abs(slot) * .18:.2f}" style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; border-radius: 8px; overflow: hidden; '
            f'box-shadow: 0 30px 70px rgba(0,0,0,.55), 0 0 0 1px rgba(242,235,220,.14); opacity: {1 if slot == 0 else .92}">'
            f'<img class="cover" src="{PORT}{MODELS[m_i][4]}.webp" alt="{MODELS[m_i][0]}" style="object-position: 50% 30%"></div>')
reveal('e-l1', 23.4)
reveal('e-l2', 23.8)
E = f"""<section class="scene" data-show="23.0,30">
    {BG}
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="23.1" style="{CG}; font-style: italic; font-size: 44px; color: {COPPER}; margin-bottom: 6px" dir="ltr">Cinq Regards</div>
      <span class="mask"><span class="e-l1" style="display: block; {FR}; font-size: 76px; font-weight: 300; line-height: 1.18; color: {CREAM}">אותם פנים. בדיוק.</span></span>
      <span class="mask"><span class="e-l2" style="display: block; {FR}; font-size: 76px; font-weight: 500; line-height: 1.18; color: {COPPER}">המבט הוא זה שמתחלף.</span></span>
    </div>
    {fan}
    <div data-in="24.6" style="position: absolute; top: 1330px; left: 40px; right: 40px; text-align: center; {CG}; font-style: italic; font-size: 34px; line-height: 1.5; color: {MUTED}" dir="ltr">La Muse · L'Icône · La Poète<br>La Directrice · L'Étoile</div>
  </section>"""

css_text = '\n'.join(css)
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · REGARD° ── */\n' + css_text)

i = s.index('  <!-- A · The Core')
j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, DD, E]) + '\n' + s[j:]

body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
(HERE / 'reel.html').write_text(s)
print('ok', len(s))
