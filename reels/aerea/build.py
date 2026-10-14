#!/usr/bin/env python3
"""AERÉA — the world's 30s studio film (concept world, no number).

Hook: five generic perfumes on a catalogue card, all alike — how will she know which one is hers?
Signature scene: Le Choix — the site's new hero rebuilt as film: the five scents swap at the centre
and colour the room, a copper ring measures how long she stays; on Nude Amber it closes, the five
line up, Amber lifts, settles into its box, the lid closes with a ribbon.
Then La Piramide (Amber's notes in layers), La Collezione, and the promise with the model.

Fills the brandos-brand-world-reel template. Every timing lives here, in seconds.
    python3 reels/aerea/build.py            -> reels/aerea/reel.html
Render (from the repo root):
    node .claude/skills/brandos-brand-world-reel/scripts/render.js reels/aerea/reel.html 30 reels/aerea/out/AEREA.mp4
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TPL = ROOT / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
IMG = '../../images/aerea/'


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


s = TPL.read_text()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# ── palette, from aerea.html SCENTS ────────────────────────────────────
INK, INK_SOFT, ROSE = '#5B4A44', '#8A766D', '#B76E5D'
FR = "font-family: 'Frank Ruhl Libre', 'Heebo', serif"
CG = "font-family: 'Cormorant Garamond', serif"
AS = "font-family: 'Assistant', 'Heebo', sans-serif"
SC = {  # key: name, family, price, bg1, bg2, accent, accentSoft, top, heart, base
    'cloud': ('רוח קלאוד', 'אוויר · רענן', 118, '#F7F4F2', '#EFE7E2', '#A98C84', '#E7DAD3', 'ברגמוט · מלח ים · אגס לבן', 'פריזיה · תה לבן', 'מושק לבן · ארז בהיר'),
    'bloom': ('וולוס בלום', 'פרחוני', 124, '#FBF2EF', '#F3DDD7', '#C77F77', '#EBC8C2', 'ליצ׳י · פלפל ורוד', 'ורד דמשק · אדמונית · יסמין', 'עץ קשמיר · מושק'),
    'solar': ('סולאר נקטר', 'נקטר · הדרים', 124, '#FBF1E4', '#F4E0C2', '#C9913F', '#F0D9A8', 'מנדרינה · נרולי', 'פריחת תפוז · דבש', 'ענבר · וניל בורבון'),
    'amber': ('נייד אמבר', 'אמבר · עוטף', 138, '#F8EDE5', '#EAD0BC', '#B76E5D', '#E2BCA4', 'זעפרן · הל', 'עוד · ורד', 'ענבר · לבונה · עורות'),
    'musk': ('סקין מאסק', 'מושק · על העור', 118, '#F5F1EC', '#E5D8CC', '#9C8472', '#DACABA', 'אגס · ברגמוט רך', 'איריס · שקד', 'מושק לבן · ענבר לבן · עץ רך'),
}
ORDER = ['cloud', 'bloom', 'solar', 'amber', 'musk']

# ── template blocks ───────────────────────────────────────────────────
rep('--w-bg:#F7F0E6;', '--w-bg:#F7F4F2;')
rep('--w-ink:#3B2E33;', f'--w-ink:{INK};')
rep('--w-accent:#C9878E;', f'--w-accent:{ROSE};')
rep('<title>Brand World Reel</title>', '<title>AERÉA reel</title>')
rep('&amp;family=Plus+Jakarta+Sans:wght@400;500', '&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;family=Frank+Ruhl+Libre:wght@300;400;500')
rep('עולם מותג <em style="font-family: \'Cormorant Garamond\', serif; font-weight: 400; color: var(--s-gold)">NN</em>',
    'עולם מותג <em style="font-family: \'Cormorant Garamond\', serif; font-weight: 400; color: var(--s-gold)" dir="ltr">AERÉA</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'חמישה ניחוחות, וגלילה שבוחרת<br>את זה שהתעכבת עליו.')
rep('BRAND° · עולם מותג NN', '<span dir="ltr">AERÉA</span> · עולם מותג קונספט')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'את <span dir="ltr">AERÉA</span> לא בוחרים מהמדף.<br>הוא יודע במה <span style="color: var(--s-copper)">התעכבת</span>.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>במה מתעכבים אצלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג קונספט')

# ── HOOK: five generic perfumes, all alike; a copper frame hops between them, undecided ──
GEN = [('EDP · 50ml', '₪189', 'none'), ('EDP · 50ml', '₪210', 'hue-rotate(28deg) saturate(.8)'),
       ('EDP · 50ml', '₪175', 'hue-rotate(-24deg)'), ('EDP · 50ml', '₪199', 'grayscale(.7)'),
       ('EDP · 50ml', '₪220', 'hue-rotate(50deg) saturate(.6)')]
HOPS = [(0.0, 0.55, 0), (0.55, 1.0, 3), (1.0, 1.4, 1), (1.4, 1.75, 4), (1.75, 2.1, 2), (2.1, 2.45, 0), (2.45, 3.2, 3)]
POS = [(0, 0), (1, 0), (2, 0), (0.5, 1), (1.5, 1)]   # tile grid positions (col, row), RTL handled by left offsets
TW, TH, GAP, X0, Y0 = 254, 312, 22, 41, 0


def tile_xy(i):
    c, r = POS[i]
    return X0 + (2 - c) * (TW + GAP) - 0, Y0 + r * (TH + GAP)


tiles = ''
for i, (code, price, flt) in enumerate(GEN):
    x, y = tile_xy(i)
    tiles += (f'<div style="position: absolute; left: {x}px; top: {y}px; width: {TW}px; height: {TH}px; box-sizing: border-box; padding: 10px 12px 14px; '
              f'background: #F7F6F4; border-radius: 12px; display: flex; flex-direction: column; justify-content: space-between">'
              f'<img src="../../images/bw-lp/generic-perfume.jpg" alt="" style="width: 100%; height: 232px; object-fit: cover; object-position: 50% 52%; border-radius: 8px; filter: {flt}">'
              f'<div style="display: flex; justify-content: space-between; font-size: 22px; color: #6E6660" dir="rtl"><span dir="ltr">{code}</span><strong style="color: #2E2A27">{price}</strong></div></div>')
hops = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.08" style="pointer-events: none"><div style="position: absolute; left: {tile_xy(i)[0] - 6}px; top: {tile_xy(i)[1] - 6}px; width: {TW + 12}px; height: {TH + 12}px; '
               f'box-sizing: border-box; border: 4px solid var(--s-copper); border-radius: 16px"></div></div>' for a, b, i in HOPS)
HOOK_PROOF = f"""<div style="position: absolute; top: 640px; left: 80px; width: 920px; box-sizing: border-box; padding: 30px 30px 36px; background: #FFFFFF; border-radius: 22px; box-shadow: 0 24px 60px rgba(62,47,37,.14)" dir="rtl">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 22px"><span style="padding: 8px 20px; border-radius: 999px; background: #2E2A27; color: #F4F2EF; font-size: 24px">ככה משווים</span><span style="font-size: 24px; color: #8A827B">בשמים לנשים · 5 תוצאות</span></div>
    <div style="position: relative; height: {2 * TH + GAP}px" dir="ltr">{tiles}{hops}</div>
  </div>"""
i = s.index('<div class="hq"')
j = s.index('<svg class="stack" width="1080" height="1920"', i)
s = s[:i] + (f'<div style="position: absolute; top: 250px; left: 80px; right: 80px; text-align: right; font-size: 76px; font-weight: 600; '
             f'line-height: 1.18; color: var(--s-dark)" dir="rtl">חמישה בשמים על המדף.<br>איך היא תדע <span style="color: var(--s-copper)">איזה שלה</span>?</div>\n  '
             + HOOK_PROOF + '\n\n  ') + s[j:]

# ── HUD ───────────────────────────────────────────────────────────────
tags = [('01 · The Core', 'חמישה ניחוחות, בוקר אחד'), ('02 · Le Choix', 'הניחוח שהתעכבת עליו'),
        ('03 · La Piramide', 'הניחוח נפתח בשכבות'), ('04 · La Collezione', 'גוון לכל ניחוח'),
        ('05 · The Promise', 'בושם לא נשאר במקום')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>')
    s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i)
    e = s.index('</span>', k)
    s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,17.0"'), ('data-show="14.7,18.7"', 'data-show="17.0,20.2"'),
             ('data-show="18.7,22.7"', 'data-show="20.2,23.1"'), ('data-show="22.7,30"', 'data-show="23.1,30"')]:
    rep(a, b)

css = []


def kf(name, frames, timing=None):
    """frames: list of (t, 'css') — written as held keyframes"""
    body = ''.join(f'{P(t)}{{{v}}}' for t, v in frames)
    first = frames[0][1]
    t_fn = f';animation-timing-function:{timing}' if timing else ''
    css.append(f'.{name}{{animation-name:{name}{t_fn}}}@keyframes {name}{{0%{{{first}}}{body}100%{{{frames[-1][1]}}}}}')


def reveal(name, t, dur=.55):
    css.append(f'.{name}{{animation-name:{name}}}@keyframes {name}{{0%,{P(t)}{{transform:translateY(110%)}}{P(t + dur)},100%{{transform:none}}}}')


GT = '<div style="position: absolute; left: 0; right: 0; top: 0; height: 600px; background: linear-gradient(to bottom, rgba(247,244,242,.95) 40%, rgba(247,244,242,0))"></div>'
GB = '<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 700px; background: linear-gradient(to top, rgba(247,244,242,.97) 46%, rgba(247,244,242,0))"></div>'
WORD = f'<div style="{CG}; font-size: 92px; font-weight: 400; letter-spacing: .32em; color: {ROSE}; padding-left: .32em" dir="ltr">AERÉA</div>'

# ── A · The Core: the bottle on silk ───────────────────────────────────
kf('a-push', [(0, 'transform:scale(1.02)'), (7.8, 'transform:scale(1.1)')], 'linear')
kf('a-push2', [(7.4, 'transform:scale(1.02)'), (10.2, 'transform:scale(1.08)')], 'linear')
reveal('a-l1', 6.0)
reveal('a-l2', 6.45)
A = f"""<section class="scene" data-show="0,10.1">
    <div class="stack"><img class="cover a-push" src="{IMG}scene-a.png" alt="" style="object-position: 50% 46%"></div>
    <div class="stack" data-show="7.6,10.2" data-fade="0.6"><img class="cover a-push2" src="{IMG}scene-b.png" alt="" style="object-position: 50% 46%"></div>
    {GT}{GB}
    <div style="position: absolute; top: 200px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px">
      {WORD}
      <div style="{AS}; font-size: 22px; font-weight: 600; letter-spacing: .4em; color: {INK_SOFT}" dir="ltr">SCENT. REIMAGINED</div>
    </div>
    <div style="position: absolute; bottom: 240px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="a-l1" style="display: block; {FR}; font-size: 86px; font-weight: 300; line-height: 1.15; color: {INK}">חמישה ניחוחות.</span></span>
      <span class="mask"><span class="a-l2" style="display: block; {FR}; font-size: 86px; font-weight: 400; line-height: 1.15; color: {ROSE}">בוקר אחד בכל פעם.</span></span>
    </div>
  </section>"""

# ── B · Le Choix: swap, the ring measures her, the five line up, Amber goes into its box ──
SWAP = [('cloud', 10.0), ('bloom', 10.75), ('solar', 11.5), ('musk', 12.25), ('amber', 13.0)]
ROW_T, LIFT_T, BOX_T, FLY_T, IN_T, LID_T, CARD_T, B_END = 14.15, 14.6, 14.95, 15.05, 15.65, 16.05, 16.25, 17.25
BW_C = 720                              # centre bottle width (1122×1402 source)
BH_C = int(BW_C * 1402 / 1122)
CX, CY = 540, 1020
# background colour per stop, held (recipe 16)
bg = [(9.7, f'background-color:{SC["cloud"][3]}')]
for key, t in SWAP[1:]:
    bg += [(t - .05, f'background-color:{bg[-1][1].split(":")[1]}'), (t + .35, f'background-color:{SC[key][3]}')]
kf('b-bg', bg)
glow = [(9.7, f'background-color:{SC["cloud"][6]}')]
for key, t in SWAP[1:]:
    glow += [(t - .05, f'background-color:{glow[-1][1].split(":")[1]}'), (t + .35, f'background-color:{SC[key][6]}')]
kf('b-glow', glow)
bottles = ''
for n, (key, t) in enumerate(SWAP):
    last = n == len(SWAP) - 1
    out_t = SWAP[n + 1][1] if not last else ROW_T
    frames = [(t - .05, 'opacity:0;transform:translateY(340px) scale(.86);filter:blur(6px)'),
              (t + .4, 'opacity:1;transform:none;filter:blur(0)')]
    if last:
        frames += [(ROW_T - .05, 'opacity:1;transform:none;filter:blur(0)'), (ROW_T + .3, 'opacity:0;transform:scale(.4) translateY(80px);filter:blur(0)')]
    else:
        frames += [(out_t - .05, 'opacity:1;transform:none;filter:blur(0)'), (out_t + .4, 'opacity:0;transform:translateY(-380px) scale(.9);filter:blur(8px)')]
    kf(f'b-c{n}', frames, 'cubic-bezier(.3,0,.2,1)')
    bottles += (f'<img class="b-c{n}" src="{IMG}bottle-{key}.png" alt="" style="position: absolute; left: {CX - BW_C // 2}px; top: {CY - BH_C // 2}px; width: {BW_C}px; height: {BH_C}px; '
                f'filter: drop-shadow(0 40px 50px rgba(120,70,50,.22))">')
# the copper ring: a little on each scent, closes on Amber
R = 330
ring = f'<svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="rgba(183,110,93,.18)" stroke-width="3"/>'
for n, (key, t) in enumerate(SWAP):
    last = n == len(SWAP) - 1
    end = SWAP[n + 1][1] - .1 if not last else 13.95
    full = 1 if last else .22
    frames = [(t + .2, 'stroke-dashoffset:1;opacity:1'), (t + .2 + (0.95 if last else .45), f'stroke-dashoffset:{1 - full:.2f};opacity:1'),
              (end, f'stroke-dashoffset:{1 - full:.2f};opacity:1'), (end + .15, f'stroke-dashoffset:{1 - full:.2f};opacity:0')]
    kf(f'b-r{n}', frames, 'linear')
    ring += (f'<circle class="b-r{n}" cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{SC[key][5]}" stroke-width="6" stroke-linecap="round" pathLength="1" '
             f'stroke-dasharray="1 1" transform="rotate(-90 {CX} {CY})" style="opacity: 0"/>')
ring += '</svg>'
kf('b-ringwrap', [(ROW_T - .1, 'opacity:1'), (ROW_T + .2, 'opacity:0')])
labels = ''
for n, (key, t) in enumerate(SWAP):
    nm, fam, price, *_ , top = SC[key][0], SC[key][1], SC[key][2], SC[key][7]
    end = SWAP[n + 1][1] - .05 if n < 4 else ROW_T
    labels += (f'<div class="stack" data-show="{t + .25:.2f},{end:.2f}" data-fade="0.18" style="display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center" dir="rtl">'
               f'<span style="{FR}; font-size: 64px; line-height: 1.1; color: {SC[key][5]}">{nm}</span>'
               f'<span style="{AS}; font-size: 30px; color: {INK_SOFT}">{fam} · <span dir="ltr">€{price}</span></span>'
               f'<span style="{AS}; font-size: 28px; color: {INK}">תווי ראש · {top}</span></div>')
amber_tag = (f'<div data-show="13.55,{ROW_T}" data-fade="0.15" style="position: absolute; top: {CY - R - 70}px; left: 0; right: 0; text-align: center">'
             f'<span style="display: inline-block; padding: 8px 22px; border-radius: 999px; background: {SC["amber"][5]}; color: #fff; {AS}; font-size: 26px; font-weight: 600">התעכבת כאן</span></div>')
# the row: five small bottles on the table, Amber lifts
RW = 200
RH = int(RW * 1402 / 1122)
ROW_ORDER = ['cloud', 'bloom', 'solar', 'amber', 'musk']   # RTL: first on the right
row = ''
for n, key in enumerate(ROW_ORDER):
    x = 540 + (2 - n) * 196 - RW // 2
    y = 1000 - RH // 2
    is_ch = key == 'amber'
    frames = [(ROW_T, 'opacity:0;transform:translateY(40px)'), (ROW_T + .35 + n * .05, 'opacity:1;transform:none')]
    if is_ch:
        frames += [(LIFT_T, 'opacity:1;transform:none'), (LIFT_T + .3, 'opacity:1;transform:translateY(-70px) scale(1.25)'),
                   (FLY_T, 'opacity:1;transform:translateY(-70px) scale(1.25)'),
                   (IN_T, f'opacity:1;transform:translate({590 - (x + RW // 2)}px,{1050 - 1000}px) scale(3.15) rotate(0deg)'),
                   (IN_T + .2, f'opacity:0;transform:translate({590 - (x + RW // 2)}px,{1050 - 1000}px) scale(3.15) rotate(0deg)')]
    else:
        frames += [(BOX_T, 'opacity:1;transform:none'), (BOX_T + .3, 'opacity:0;transform:translateY(60px)')]
    kf(f'b-row{n}', frames, 'cubic-bezier(.4,0,.2,1)')
    row += (f'<img class="b-row{n}" src="{IMG}bottle-{key}.png" alt="" style="position: absolute; left: {x}px; top: {y}px; width: {RW}px; height: {RH}px; '
            f'opacity: 0; filter: drop-shadow(0 18px 24px rgba(120,70,50,.22))">')
# the box: open box rises, the in-box Amber replaces the flying bottle, then the lid
BXW = 880
BXH = int(BXW * 1500 / 1200)
BX, BY = 540 - BXW // 2, 1120 - BXH // 2
kf('b-box', [(BOX_T, 'opacity:0;transform:translateY(500px)'), (BOX_T + .45, 'opacity:1;transform:none'), (IN_T, 'opacity:1;transform:none'), (IN_T + .2, 'opacity:0;transform:none')],
   'cubic-bezier(.2,.7,.2,1)')
kf('b-boxin', [(IN_T - .02, 'opacity:0'), (IN_T + .18, 'opacity:1'), (LID_T, 'opacity:1'), (LID_T + .35, 'opacity:0')])
kf('b-boxlid', [(LID_T, 'opacity:0;transform:translateY(-30px)'), (LID_T + .35, 'opacity:1;transform:none')], 'cubic-bezier(.2,.7,.2,1)')
box = (f'<img class="b-box" src="{IMG}box-open.webp" alt="" style="position: absolute; left: {BX}px; top: {BY}px; width: {BXW}px; height: {BXH}px; opacity: 0; filter: drop-shadow(0 40px 50px rgba(120,70,50,.18))">'
       f'<img class="b-boxin" src="{IMG}box-amber.webp" alt="" style="position: absolute; left: {BX}px; top: {BY}px; width: {BXW}px; height: {BXH}px; opacity: 0; filter: drop-shadow(0 40px 50px rgba(120,70,50,.18))">'
       f'<img class="b-boxlid" src="{IMG}box-closed.webp" alt="" style="position: absolute; left: {BX}px; top: {BY}px; width: {BXW}px; height: {BXH}px; opacity: 0; filter: drop-shadow(0 40px 50px rgba(120,70,50,.18))">')
card = (f'<div data-in="{CARD_T}" style="position: absolute; left: 0; right: 0; top: 1640px; display: flex; justify-content: center">'
        f'<div style="display: flex; align-items: center; gap: 22px; background: rgba(255,255,255,.8); border: 1px solid rgba(183,110,93,.25); border-radius: 999px; padding: 14px 16px 14px 34px" dir="rtl">'
        f'<span style="{AS}; font-size: 22px; letter-spacing: .14em; color: {INK_SOFT}"><span dir="ltr">AERÉA</span> · הניחוח שלך</span>'
        f'<span style="{FR}; font-size: 40px; color: {SC["amber"][5]}">נייד אמבר</span>'
        f'<span style="padding: 14px 30px; border-radius: 999px; background: {SC["amber"][5]}; color: #fff; {AS}; font-size: 24px; font-weight: 600">+ הוסיפי לסל</span></div></div>')
heads = (f'<div class="stack" data-show="9.7,{ROW_T + .1}" data-fade="0.25" style="top: 200px; height: 220px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">'
         f'<div style="{CG}; font-style: italic; font-size: 46px; color: {ROSE}" dir="ltr">Le Choix</div>'
         f'<div style="{FR}; font-size: 70px; font-weight: 300; line-height: 1.2; color: {INK}">כל גלילה, ניחוח אחר.</div></div>'
         f'<div class="stack" data-show="{ROW_T + .1},{IN_T - .1}" data-fade="0.2" style="top: 230px; height: 200px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">'
         f'<div style="{FR}; font-size: 84px; font-weight: 300; line-height: 1.2; color: {INK}">זה <span style="color: {SC["amber"][5]}">שהתעכבת עליו</span>.</div></div>'
         f'<div class="stack" data-show="{IN_T + .25},{B_END + .3}" data-fade="0.2" style="top: 230px; height: 200px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">'
         f'<div style="{FR}; font-size: 84px; font-weight: 300; line-height: 1.2; color: {INK}">נבחר <span style="color: {SC["amber"][5]}">בשבילך</span>.</div></div>')
B = f"""<section class="scene" data-show="9.7,{B_END}">
    <div class="stack b-bg" style="background-color: {SC['cloud'][3]}"></div>
    <div class="stack b-glow" style="background-color: {SC['cloud'][6]}; opacity: .7; -webkit-mask-image: radial-gradient(circle 560px at 540px 1020px, #000 0%, transparent 100%); mask-image: radial-gradient(circle 560px at 540px 1020px, #000 0%, transparent 100%)"></div>
    <div class="stack b-ringwrap">{ring}</div>
    {bottles}
    {amber_tag}
    {box}
    {row}
    {heads}
    <div data-show="9.9,{ROW_T}" data-fade="0.2" style="position: absolute; top: 1560px; left: 40px; right: 40px; height: 200px">{labels}</div>
    {card}
  </section>"""

# ── C · La Piramide: Amber opens in layers ─────────────────────────────
LAY = [('תווי הראש', '0–15 דק׳', SC['amber'][7], .30, 17.6), ('תווי הלב', '15 דק׳–3 שעות', SC['amber'][8], .70, 18.15),
       ('תווי הבסיס', '3 שעות+', SC['amber'][9], 1.0, 18.7)]
layers = ''
for k, (h, tm, notes, w, t) in enumerate(LAY):
    css.append(f'.c-bar{k}{{animation-name:cbar{k};transform-origin:right}}@keyframes cbar{k}{{0%,{P(t + .2)}{{transform:scaleX(0)}}{P(t + 1.0)},100%{{transform:scaleX({w})}}}}')
    layers += (f'<div data-in="{t}" style="box-sizing: border-box; width: 100%; padding: 26px 32px; background: rgba(255,255,255,.62); border: 1px solid rgba(183,110,93,.2); border-radius: 22px; display: flex; flex-direction: column; gap: 8px" dir="rtl">'
               f'<div style="display: flex; justify-content: space-between; align-items: baseline"><span style="{FR}; font-size: 42px; color: {INK}">{h}</span><span style="{AS}; font-size: 24px; color: {INK_SOFT}">{tm}</span></div>'
               f'<div style="{AS}; font-size: 32px; font-weight: 600; color: {SC["amber"][5]}">{notes}</div>'
               f'<div style="height: 6px; border-radius: 3px; background: rgba(183,110,93,.15); overflow: hidden"><div class="c-bar{k}" style="height: 100%; background: linear-gradient(90deg,{SC["amber"][6]},{SC["amber"][5]})"></div></div></div>')
kf('c-float', [(17.0, 'transform:translateY(20px)'), (20.3, 'transform:translateY(-20px)')], 'linear')
C = f"""<section class="scene" data-show="17.0,20.4">
    <div class="stack" style="background: {SC['amber'][3]}; background-image: radial-gradient(800px 700px at 50% 34%, {SC['amber'][6]} 0%, {SC['amber'][3]} 70%)"></div>
    <div style="position: absolute; top: 200px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="17.05" style="{CG}; font-style: italic; font-size: 46px; color: {ROSE}" dir="ltr">La Piramide</div>
      <div data-in="17.2" style="{FR}; font-size: 72px; font-weight: 300; line-height: 1.2; color: {INK}">הניחוח נפתח <span style="color: {SC['amber'][5]}">בשכבות</span>.</div>
    </div>
    <div class="c-float" style="position: absolute; left: 330px; top: 430px; width: 420px; height: {int(420 * 1402 / 1122)}px"><img src="{IMG}bottle-amber.png" alt="" style="width: 100%; height: 100%; filter: drop-shadow(0 30px 40px rgba(120,70,50,.25))"></div>
    <div style="position: absolute; left: 70px; right: 70px; top: 1000px; display: flex; flex-direction: column; gap: 22px">{layers}</div>
  </section>"""

# ── D · Il Film → La Collezione ────────────────────────────────────────
ADD_T = 22.35
cards = ''
for n, key in enumerate(ROW_ORDER):
    nm, price = SC[key][0], SC[key][2]
    cards += (f'<div data-in="{21.4 + n * .1:.2f}" style="width: 188px; display: flex; flex-direction: column; align-items: center; gap: 6px">'
              f'<img src="{IMG}bottle-{key}.png" alt="" style="width: 188px; height: {int(188 * 1402 / 1122)}px; filter: drop-shadow(0 16px 20px rgba(120,70,50,.2))">'
              f'<span style="{FR}; font-size: 30px; color: {SC[key][5]}; white-space: nowrap" dir="rtl">{nm}</span>'
              f'<span style="{CG}; font-size: 28px; color: {INK}" dir="ltr">€{price}</span></div>')
css.append(f'.d-cart{{animation-name:dcart}}@keyframes dcart{{0%,{P(ADD_T)}{{transform:scale(1)}}{P(ADD_T + .2)}{{transform:scale(1.2)}}{P(ADD_T + .45)},100%{{transform:scale(1)}}}}')
DD = f"""<section class="scene" data-show="20.0,23.3">
    <div class="stack" data-show="20.0,21.45" data-fade="0.3">
      <div class="stack" data-seq="seq/f_%03d.jpg" data-from="1" data-to="38" data-start="20.0" data-step="0.04"></div>
      <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 520px; background: linear-gradient(to top, rgba(40,26,22,.7), rgba(40,26,22,0))"></div>
      <div style="position: absolute; bottom: 230px; left: 60px; right: 60px; text-align: center" dir="rtl">
        <div style="{CG}; font-style: italic; font-size: 46px; color: #F3DDD0" dir="ltr">Il Film</div>
        <div style="{FR}; font-size: 72px; font-weight: 300; color: #FFF8F2">עשר שניות בתוך הבקבוק.</div>
      </div>
    </div>
    <div class="stack" data-show="21.35,23.4" data-fade="0.3" style="background: #F7F4F2">
      <div style="position: absolute; top: 230px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
        <div style="{CG}; font-style: italic; font-size: 46px; color: {ROSE}" dir="ltr">La Collezione</div>
        <div style="{FR}; font-size: 70px; font-weight: 300; line-height: 1.2; color: {INK}">חמישה ניחוחות,<br><span style="color: {ROSE}">גוון לכל אחד.</span></div>
      </div>
      <div style="position: absolute; top: 760px; left: 30px; right: 30px; display: flex; justify-content: space-between" dir="rtl">{cards}</div>
      <div class="d-cart" style="position: absolute; left: 80px; top: 1500px; width: 110px; height: 110px; border-radius: 50%; border: 2px solid {ROSE}; background: rgba(255,255,255,.7); display: flex; align-items: center; justify-content: center">
        <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke="{ROSE}" stroke-width="1.5" aria-hidden="true"><path d="M6 8h12l-1.2 11.2a2 2 0 0 1-2 1.8H9.2a2 2 0 0 1-2-1.8L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>
        <div data-show="{ADD_T},30" data-fade="0.15" style="position: absolute; top: -6px; right: -6px; width: 44px; height: 44px; border-radius: 50%; background: {ROSE}; color: #fff; {AS}; font-weight: 700; font-size: 24px; line-height: 44px; text-align: center">1</div>
      </div>
      <div data-in="21.9" style="position: absolute; top: 1520px; left: 230px; right: 80px; {AS}; font-size: 30px; color: {INK_SOFT}; line-height: 1.5" dir="rtl">נייד אמבר כבר בסל.<br>הקופסה סגורה, בסרט.</div>
    </div>
  </section>"""

# ── E · The Promise: the model and the bottle ──────────────────────────
reveal('e-l1', 23.5)
reveal('e-l2', 23.9)
kf('e-push', [(23.0, 'transform:scale(1.04)'), (30, 'transform:scale(1)')], 'linear')
E = f"""<section class="scene" data-show="23.0,30">
    <div class="stack" style="background: #F7F4F2; background-image: radial-gradient(900px 800px at 50% 62%, #EFE3DA 0%, #F7F4F2 70%)"></div>
    <div class="e-push" style="position: absolute; left: 90px; top: 560px; width: 900px; height: {int(900 * 1402 / 1122)}px"><img src="{IMG}presenter.png" alt="" style="width: 100%; height: 100%"></div>
    <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 360px; background: linear-gradient(to top, #F7F4F2 30%, rgba(247,244,242,0))"></div>
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="23.15" style="margin-bottom: 14px">{WORD}</div>
      <span class="mask"><span class="e-l1" style="display: block; {FR}; font-size: 72px; font-weight: 300; line-height: 1.2; color: {INK}">בושם לא נשאר במקום.</span></span>
      <span class="mask"><span class="e-l2" style="display: block; {FR}; font-size: 72px; font-weight: 400; line-height: 1.2; color: {ROSE}">גם העולם שלו לא.</span></span>
    </div>
  </section>"""

rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · AERÉA ── */\n' + '\n'.join(css))
i = s.index('  <!-- A · The Core')
j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, DD, E]) + '\n' + s[j:]

body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
(HERE / 'reel.html').write_text(s)
print('ok', len(s))
