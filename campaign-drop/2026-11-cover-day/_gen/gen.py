#!/usr/bin/env python3
"""«מכסים את השם» wave 2 — ENCORE°, ROSÉE°, CHASEN° (series A of the cover-day campaign).

One 19s reel per world, built from the approved storyboard (Design canvas "מכסים את השם · סטוריבורד"):
  0.0–1.8   hook: the question over the world's strongest touchpoint, with the name, in the studio window
  1.8–2.2   the window rises into place, the code counter appears
  1.9–15.0  five touchpoints. On each one the name comes off inside the frame (no bar, no cut), the
            world's own codes light up one by one and the counter climbs 3 → 6 → 9 → 12 → 15.
            Between touchpoints, a transition taken from the world's own site:
              ENCORE°  gold veil on the name · the gold hand sweeps the touchpoint into the dial, the hour moves on
              ROSÉE°   a dew drop dissolves the name · the morning dial turns to the next hour
              CHASEN°  the whisk whisks the name away · the same cup swaps to the next flavour
  15.0–19.0 «השם ירד. עדיין ___. ואצלך?», the five touchpoints without the name, the CTA.
The 3s retargeting hook is the first 3 seconds of the same page (the counter reaches 3 at 2.8s).

Usage (from the repo root):  python3 campaign-drop/2026-11-cover-day/_gen/gen.py [world ...]
Writes campaign-drop/2026-11-cover-day/<world>/src/{reel.html,assets/…}. Render with render-all.sh."""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(__file__))
from film import Film

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'campaign-drop', '2026-11-cover-day')

# Brand Worlds Studio · feed tokens
CREAM, CREAM_DEEP, INK, INK_SOFT = '#F2EBDC', '#E7DEC9', '#15202E', '#3D4A5C'
COPPER, COPPER_SOFT, COPPER_TEXT = '#C28A5A', '#D9AE85', '#825630'
FONTS = ('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400'
         '&family=Plus+Jakarta+Sans:wght@500;600&display=swap')
DISPLAY = "'Cormorant Garamond','Frank Ruhl Libre',serif"
LABEL = "'Plus Jakarta Sans','Heebo',sans-serif"

# ───────────────────────── timeline (s) ─────────────────────────
D = 19.0
S = [1.9, 5.0, 7.5, 10.0, 12.5]          # touchpoint i starts
E = S[1:] + [15.0]                        # … and ends (the transition is centred on E[i])
F = [2.1] + [s + .5 for s in S[1:]]       # the name starts to come off
END = 15.0


def chip_t(i, k):
    return F[i] + .4 + k * .15


WW, WH = 920, 1150                        # the studio window (4:5), top 300, side margin 80
R0, RF = 229, 760                         # iris: the dial's radius, and a radius that clears the corners


def px(p, total):
    return float(str(p).rstrip('%')) / 100 * total


# ───────────────────────── assets ─────────────────────────
class Assets:
    def __init__(self, world):
        self.dir = os.path.join(OUT, world, 'src', 'assets')
        os.makedirs(self.dir, exist_ok=True)

    def __call__(self, src, name=None):
        name = name or os.path.basename(src)
        dst = os.path.join(self.dir, name)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(ROOT, src), dst)
        return 'assets/' + name


def dot(bg):
    return f'<span style="display:inline-block;width:22px;height:22px;border-radius:999px;background:{bg};vertical-align:-3px"></span>'


# ───────────────────────── the worlds ─────────────────────────
def encore(A):
    tp = 'encore/assets/touchpoints/'
    four = 'conic-gradient(#6E4E4A 0 25%,#34405A 0 50%,#853A26 0 75%,#241212 0)'
    rows = [
        ('box-open', 'La Boîte', 'הקופסה', '50.8%', '15.3%', '26%', ['ארבעה תאים, ארבע שעות', 'קו הזהב', 'התאריך החרוט'], '06:00', '#6E4E4A', 90),
        ('tag-cuff', 'L’Étiquette', 'התווית', '33.6%', '61.5%', '34%', ['חותמת השעה', 'צבע השעה', 'שם התכשיט'], '12:00', '#34405A', 180),
        ('bag-street', 'Le Sac', 'השקית', '55.6%', '61.2%', '26%', ['צבע השעה', 'חותמת השעה', 'ידית הזהב'], '18:00', '#853A26', 270),
        ('bags-four', 'Les Quatre Heures', 'ארבע השעות', '50%', '52%', '92%', ['ארבעה צבעי השעות', 'חותמת השעה', 'החוגה'], '00:00', '#241212', 360),
        ('sign', 'L’Enseigne', 'השלט', '60%', '25.2%', '30%', ['החוגה', 'ארבעה צבעי השעות', 'שנתות הזהב'], '06 · 12 · 18 · 00', four, 720),
    ]
    tps = [dict(on=A(f'{tp}{n}.webp'), off=A(f'{tp}{n}-sans.webp'), pos='50% 50%', fr=fr, he=he, x=x, y=y, w=w, codes=c,
                hour=h, col=col, ang=ang,
                eyebrow=f'<span dir="ltr">ENCORE°</span>&lrm; · {dot(col)} <span dir="ltr">{h}</span>')
           for n, fr, he, x, y, w, c, h, col, ang in rows]
    return dict(slug='encore', name='ENCORE°', tps=tps, mode='iris', ring='#D9B26A', winbg='#1E0F0E', proof=CREAM,
                fx=fx_veil, off_at=(.35, .8), dial=dial_hour)


def rosee(A):
    tp = 'rosee/assets/touchpoints/'
    rows = [
        ('box-card', 'La Boîte', 'הקופסה והכרטיס', '50% 50%', '33%', '45%', '30%', ['שעון השחר', 'השעה', 'קו הנחושת'], '05:30', 'La Brume', 'brume', -60),
        ('bag', 'Le Sac', 'השקית', '50% 50%', '54%', '57%', '30%', ['שעון השחר', 'צבעי השחר', 'ידיות נחושת'], '06:15', 'Le Réveil', 'reveil', -20),
        ('shelf', 'L’Étagère', 'המדף בבית', '50% 50%', '46%', '51%', '58%', ['השעה', 'מכסי נחושת', 'הטיפה'], '07:00', 'Le Voile', 'voile', 20),
        ('trousse', 'La Trousse', 'ערכת הנסיעה', '50% 45%', '48%', '48.5%', '50%', ['שלוש שעות בשורה', 'זכוכית ורודה', 'רוכסן נחושת'], '07:45', 'La Lumière', 'lumiere', 60),
        ('refill', 'La Recharge', 'המילוי', '50% 50%', '54%', '49.5%', '70%', ['השעה', 'זכוכית ורודה', 'מכסה נחושת'], '22:00', 'La Nuit', 'nuit', 150),
    ]
    # every place the name sits (the box and the card; three bottles; two packs), measured from the -sans diff
    spots = {'box-card': [('33%', '42%', '26%'), ('57%', '80%', '18%')],
             'shelf': [('27%', '51%', '18%'), ('48%', '54%', '18%'), ('64%', '48%', '14%')],
             'trousse': [('28%', '46%', '14%'), ('47%', '49%', '14%'), ('66%', '50%', '14%')],
             'refill': [('35%', '50%', '24%'), ('72%', '49%', '20%')]}
    tps = [dict(on=A(f'{tp}{n}.webp'), off=A(f'{tp}{n}-sans.webp'), pos=pos, fr=fr, he=he, x=x, y=y, w=w, codes=c,
                spots=spots.get(n, [(x, y, w)]),
                hour=h, prod=A(f'rosee/collection/{p}.webp'), ang=ang,
                eyebrow=f'<span dir="ltr">ROSÉE°</span>&lrm; · <span dir="ltr">{h}</span> · <span dir="ltr">{pn}</span>')
           for n, fr, he, pos, x, y, w, c, h, pn, p, ang in rows]
    return dict(slug='rosee', name='ROSÉE°', tps=tps, mode='iris', ring=COPPER, winbg='#FBF6EE', proof='#C9878E',
                fx=fx_drop, off_at=(.45, 1.0), dial=dial_morning)


def chasen(A):
    tp = 'chasen/assets/touchpoints/'
    rows = [
        ('five', 'Les Cinq', 'חמש הכוסות', '50% 50%', '50%', '61%', '92%', ['חמשת צבעי הטעמים', 'סימן המטרפה', 'הכוס השכבתית'], 'Matcha Classique', '#6f9a3f', '#E3EBD6', 'classic'),
        ('kit', 'Le Coffret', 'ערכת הבית', '50% 0%', '50%', '16%', '44%', ['המטרפה', 'חמשת צבעי הטעמים', 'קרם חם'], 'Matcha Fraise', '#d98a95', '#F6E1E3', 'fraise'),
        ('wall', 'Le Mur', 'קיר המטרפות', '50% 0%', '50%', '17.5%', '52%', ['המטרפה', 'חמשת צבעי הטעמים', 'קרם חם'], 'Hōjicha', '#a8794f', '#EFE3D6', 'hojicha'),
        ('bag', 'Le Sac', 'השקית', '50% 50%', '49.7%', '68.4%', '26%', ['המטרפה, ביד', 'סימן המטרפה', 'קרם חם'], 'Matcha Yuzu', '#e5c85a', '#F8F0D2', 'yuzu'),
        ('hand', 'À emporter', 'לדרך', '50% 50%', '51.6%', '61.7%', '26%', ['סימן המטרפה', 'צבע הטעם', 'הכוס השכבתית'], 'Matcha Bleu', '#7f8fc9', '#E2E6F4', 'bleu'),
    ]
    tps = [dict(on=A(f'{tp}{n}.webp'), off=A(f'{tp}{n}-sans.webp'), pos=pos, fr=fr, he=he, x=x, y=y, w=w, codes=c,
                flav=fl, col=col, tint=tint, glass=A(f'chasen/img/glass_{g}.webp'),
                eyebrow=f'<span dir="ltr">CHASEN°</span>&lrm; · {dot(col)} <span dir="ltr">{fl}</span>')
           for n, fr, he, pos, x, y, w, c, fl, col, tint, g in rows]
    return dict(slug='chasen', name='CHASEN°', tps=tps, mode='swap', winbg='#F4E7D5', proof=COPPER,
                fx=fx_whisk, off_at=(.5, .75))


WORLDS = {'encore': encore, 'rosee': rosee, 'chasen': chasen}


# ───────────────────────── the name comes off ─────────────────────────
def fx_veil(fm, t, f):
    """ENCORE°: the gold veil of the site's cover test opens across the name and fades."""
    x, y, w, h = px(t['x'], WW), px(t['y'], WH), px(t['w'], WW), 104
    return (f'<div style="position:absolute;left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h}px;border-radius:50%;filter:blur(3px);'
            f'background:radial-gradient(closest-side,rgba(217,178,106,.9),rgba(217,178,106,.3) 60%,rgba(217,178,106,0));'
            f'{fm.kf([(f, "opacity:0;transform:scaleX(.3)"), (f + .45, "opacity:1;transform:scaleX(1)"), (f + 1.2, "opacity:0;transform:scaleX(1.15)")])}"></div>')


def fx_drop(fm, t, f):
    """ROSÉE°: a dew drop from the site's opening falls on every place the name sits; a rose ripple spreads and the letters melt."""
    return ''.join(fx_drop1(fm, sx, sy, sw, f + k * .1) for k, (sx, sy, sw) in enumerate(t['spots']))


def fx_drop1(fm, sx, sy, sw, f):
    x, y, w = px(sx, WW), px(sy, WH), min(max(px(sw, WW), 150), 700)
    drop = (f'<div style="position:absolute;left:{x - 22:.0f}px;top:0;width:44px;height:58px;'
            f'{fm.kf([(f - .01, "opacity:0;transform:translateY(-60px)"), (f, "opacity:1;transform:translateY(-60px)"), (f + .36, f"opacity:1;transform:translateY({y - 50:.0f}px)"), (f + .4, f"opacity:0;transform:translateY({y - 40:.0f}px)")], "cubic-bezier(.55,0,1,.45)")}">'
            f'<div style="position:absolute;inset:0;border-radius:50% 50% 50% 50% / 60% 60% 40% 40%;border:3px solid #FBF6EE;'
            f'background:radial-gradient(circle at 38% 32%,#FFFFFF 0%,#F3D3D5 30%,#E8B4B8 70%,#C9878E 100%);box-shadow:0 6px 14px rgba(20,30,45,.25)"></div></div>')

    def ripple(d, sty):
        return (f'<div style="position:absolute;left:{x - w / 2:.0f}px;top:{y - w * .16:.0f}px;width:{w:.0f}px;height:{w * .32:.0f}px;border-radius:50%;{sty};'
                f'{fm.kf([(f + .34 + d, "opacity:0;transform:scale(.12)"), (f + .38 + d, "opacity:1;transform:scale(.22)"), (f + 1.15 + d, "opacity:0;transform:scale(1.15)")], "cubic-bezier(.2,.6,.3,1)")}"></div>')
    return (drop + ripple(0, 'border:6px solid #C9878E')
            + ripple(.1, 'background:radial-gradient(closest-side,rgba(251,246,238,.97),rgba(232,180,184,.75) 62%,rgba(232,180,184,0))'))


def fx_whisk(fm, t, f):
    """CHASEN°: the whisk whisks across the name in a quick zigzag; the name goes under the foam and the foam settles."""
    x, y = px(t['x'], WW), px(t['y'], WH)
    w = min(px(t['w'], WW) + 40, 860)
    n = 9
    pts = ' '.join(f'{i * w / (n - 1):.0f},{(86 if i % 2 == 0 else 14)}' for i in range(n))
    whisk = (f'<div style="position:absolute;left:{x - w / 2:.0f}px;top:{y - 50:.0f}px;width:{w:.0f}px;height:100px;'
             f'{fm.kf([(f + .5, "opacity:1"), (f + .8, "opacity:0")], "linear")}">'
             f'<svg viewBox="0 0 {w:.0f} 100" width="{w:.0f}" height="100" style="overflow:visible" aria-hidden="true">'
             f'<polyline points="{pts}" fill="none" stroke="#4C6B33" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" pathLength="1" '
             f'stroke-dasharray="1 1" style="{fm.kf([(f, "stroke-dashoffset:1"), (f + .45, "stroke-dashoffset:0")], "cubic-bezier(.3,0,.4,1)")}"></polyline></svg></div>')
    foam = (f'<div style="position:absolute;left:{x - w / 2:.0f}px;top:{y - 70:.0f}px;width:{w:.0f}px;height:140px;border-radius:50%;filter:blur(2px);'
            f'background:radial-gradient(closest-side,rgba(250,243,232,1),rgba(244,231,213,.95) 55%,rgba(244,231,213,.5) 78%,rgba(244,231,213,0));'
            f'{fm.kf([(f + .15, "opacity:0;transform:scaleX(.4)"), (f + .45, "opacity:1;transform:scaleX(1)"), (f + .8, "opacity:1;transform:scaleX(1.02)"), (f + 1.2, "opacity:0;transform:scaleX(1.06)")])}"></div>')
    return foam + whisk


# ───────────────────────── the dial between touchpoints ─────────────────────────
def circle_box(inner, extra=''):
    return (f'<div style="position:absolute;left:{(WW - 2 * R0) // 2}px;top:{(WH - 2 * R0) // 2}px;width:{2 * R0}px;height:{2 * R0}px;'
            f'box-sizing:border-box;border-radius:50%;{extra}">{inner}</div>')


def hand(fm, a0, a1, T, color, length, width=6):
    return (f'<div style="position:absolute;left:{R0 - width // 2}px;top:{R0 - length}px;width:{width}px;height:{length}px;border-radius:{width}px;'
            f'background:{color};transform-origin:50% 100%;{fm.kf([(T - .34, f"transform:rotate({a0}deg)"), (T - .04, f"transform:rotate({a1}deg)")], "cubic-bezier(.6,0,.2,1)")}"></div>'
            f'<div style="position:absolute;left:{R0 - 10}px;top:{R0 - 10}px;width:20px;height:20px;border-radius:999px;background:{color}"></div>')


def ticks(n, color, size=26, width=4, inset=10):
    return ''.join(f'<div style="position:absolute;left:{R0 - width // 2}px;top:{inset}px;width:{width}px;height:{size}px;background:{color};'
                   f'transform-origin:50% {R0 - inset}px;transform:rotate({k * 360 / n}deg)"></div>' for k in range(n))


def dial_hour(fm, w, i, T):
    """ENCORE°: the dial takes the colour of the next hour; the gold hand sweeps to it."""
    a, b = w['tps'][i], w['tps'][i + 1]
    gold = '#D9B26A'
    inner = (ticks(4, gold, 34, 5, 12) + hand(fm, a['ang'], b['ang'], T, gold, 170)
             )
    label = (f'<div dir="ltr" style="position:absolute;left:0;right:0;top:{(WH + 2 * R0) // 2 + 34}px;text-align:center;font-family:{DISPLAY};'
             f'font-size:72px;font-weight:500;color:#F6EEE4">{b["hour"]}</div>')
    return circle_box(inner, f'background:{b["col"]};box-shadow:inset 0 0 0 5px {gold}') + label


def dial_morning(fm, w, i, T):
    """ROSÉE°: the morning dial of the site turns one step; the product of the next hour sits in its centre."""
    b = w['tps'][i + 1]
    a = w['tps'][i]
    inner = (f'<img src="{b["prod"]}" alt="" style="position:absolute;left:{R0 - 150}px;top:{R0 - 150}px;width:300px;height:300px;border-radius:50%;object-fit:cover">'
             + ticks(12, COPPER, 22, 4, 10) + hand(fm, a['ang'], b['ang'], T, COPPER, 190))
    label = (f'<div dir="ltr" style="position:absolute;left:0;right:0;top:{(WH + 2 * R0) // 2 + 34}px;text-align:center;font-family:{DISPLAY};'
             f'font-size:72px;font-weight:500;color:{INK}">{b["hour"]}</div>')
    return circle_box(inner, f'background:#FBF6EE;box-shadow:inset 0 0 0 5px {COPPER}') + label


# ───────────────────────── the studio window ─────────────────────────
def clip(r):
    return f'clip-path:circle({r}px at 50% 50%)'


def tp_layer(fm, w, i):
    t = w['tps'][i]
    st = f'position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{t["pos"]};display:block'
    o0, o1 = w['off_at']
    inner = (f'<img src="{t["on"]}" alt="" style="{st}">'
             f'<img src="{t["off"]}" alt="" style="{st};{fm.kf([(F[i] + o0, "opacity:0"), (F[i] + o1, "opacity:1")], "ease-in-out")}">'
             + w['fx'](fm, t, F[i]))
    push = f'<div style="position:absolute;inset:0;{fm.kf([(S[i], "transform:scale(1.045)"), (E[i] + .3, "transform:scale(1)")], "linear")}">{inner}</div>'
    if w['mode'] == 'iris':
        pts = [(0, clip(RF))] if i == 0 else [(S[i] - .03, clip(0)), (S[i] - .02, clip(R0)), (S[i] + .35, clip(RF))]
        if i < 4:
            pts += [(E[i] - .55, clip(RF)), (E[i] - .35, clip(R0)), (E[i] - .3, clip(R0)), (E[i] - .29, clip(0))]
        vis = fm.kf(pts)
    else:
        vis = fm.show(0 if i == 0 else S[i] - .05, E[i] - .05 if i < 4 else D, .05)
    return f'<div style="position:absolute;inset:0;{vis}">{push}</div>'


def ring(fm, w, T):
    s = RF / R0
    return circle_box('', f'border:5px solid {w["ring"]};' + fm.kf([
        (T - .56, f'opacity:0;transform:scale({s:.2f})'), (T - .55, f'opacity:1;transform:scale({s:.2f})'), (T - .35, 'opacity:1;transform:scale(1)'),
        (T - .02, 'opacity:1;transform:scale(1)'), (T + .35, f'opacity:1;transform:scale({s:.2f})'), (T + .36, f'opacity:0;transform:scale({s:.2f})')]))


def swap(fm, w, i, T):
    """CHASEN°: the cup from La Métamorphose — the same cup, pixel-aligned, swaps to the next flavour."""
    a, b = w['tps'][i], w['tps'][i + 1]
    gh = 880
    gw = round(852 / 1820 * gh)
    g = f'position:absolute;left:{(WW - gw) // 2}px;top:60px;width:{gw}px;height:{gh}px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 16%,#000 84%,transparent),linear-gradient(180deg,transparent,#000 5%,#000 95%,transparent);-webkit-mask-composite:source-in;mask-composite:intersect'
    tint = (f'<div style="position:absolute;inset:0;background:#F4E7D5;{fm.show(T - .3, T + .15, .2)}"></div>')
    name = (f'<div dir="ltr" style="position:absolute;left:0;right:0;top:{WH - 150}px;text-align:center;font-family:{DISPLAY};font-style:italic;font-size:64px;color:{INK};'
            f'{fm.kf([(T - .2, "opacity:0;transform:translateY(16px)"), (T - .05, "opacity:1;transform:none"), (T + .15, "opacity:1;transform:none"), (T + .35, "opacity:0;transform:none")])}">'
            f'{dot(b["col"])} {b["flav"]}</div>')
    cur = (f'<img src="{a["glass"]}" alt="" style="{g};'
           f'{fm.kf([(T - .5, "opacity:0;transform:translateY(90px)"), (T - .3, "opacity:1;transform:none"), (T - .1, "opacity:1;transform:none"), (T - .02, "opacity:0;transform:none")])}">')
    nxt = (f'<img src="{b["glass"]}" alt="" style="{g};'
           f'{fm.kf([(T - .16, "opacity:0;transform:none"), (T - .05, "opacity:1;transform:none"), (T + .15, "opacity:1;transform:none"), (T + .35, "opacity:0;transform:scale(1.05)")])}">')
    return tint + cur + nxt + name


def window(fm, w):
    layers = []
    if w['mode'] == 'iris':
        for i in range(4):  # the window takes the next ground while the touchpoint closes into the dial
            bg = w['tps'][i + 1]['col'] if w['slug'] == 'encore' else w['winbg']
            layers.append(f'<div style="position:absolute;inset:0;background:{bg};{fm.show(E[i] - .4, E[i] + .45, .15)}"></div>')
        for i in range(5):
            layers.append(tp_layer(fm, w, i))
            if i < 4:
                T = E[i]
                layers.append(f'<div style="position:absolute;inset:0;{fm.show(T - .36, T + .3, .06)}">{w["dial"](fm, w, i, T)}</div>')
        layers += [ring(fm, w, E[i]) for i in range(4)]
    else:
        layers += [tp_layer(fm, w, i) for i in range(5)]
        layers += [swap(fm, w, i, E[i]) for i in range(4)]
    t0 = w['tps'][0]
    proof = ''
    for sx, sy, sw in t0.get('spots', [(t0['x'], t0['y'], t0['w'])]):
        rx, ry, rw = px(sx, WW), px(sy, WH), min(max(px(sw, WW) + 60, 200), 880)
        proof += (f'<div style="position:absolute;left:{rx - rw / 2:.0f}px;top:{ry - 64:.0f}px;width:{rw:.0f}px;height:128px;border-radius:50%;'
                  f'border:4px dashed {w["proof"]};{fm.show(0, 1.75, .2)}"></div>')
    marks = ''.join(f'<div style="position:absolute;{v}:-24px;{h}:-24px;width:48px;height:48px;border-{v}:4px solid {COPPER};border-{h}:4px solid {COPPER}"></div>'
                    for v in ('top', 'bottom') for h in ('left', 'right'))
    return (f'<div style="position:absolute;top:300px;left:80px;width:{WW}px;height:{WH}px;'
            f'{fm.kf([(1.8, "transform:translateY(320px);opacity:1"), (2.25, "transform:none;opacity:1"), (END, "transform:none;opacity:1"), (END + .4, "transform:scale(.92);opacity:0")])}">'
            f'{marks}<div style="position:absolute;inset:0;border-radius:20px;overflow:hidden;background:{w["winbg"]};box-shadow:0 24px 60px rgba(20,30,45,.16)">'
            f'{"".join(layers)}{proof}</div></div>')


# ───────────────────────── the frame around it ─────────────────────────
def ball(fm, x0, x1, y, t0, t1, size=44, right=80):
    """the studio's copper ball rolling right to left on its copper line."""
    line = (f'<div style="position:absolute;top:{y + size // 2 - 2}px;left:{x1 + size // 2}px;right:{right}px;height:4px;border-radius:4px;background:{COPPER};'
            f'transform-origin:right;{fm.kf([(t0, "transform:scaleX(0)"), (t1, "transform:scaleX(1)")])}"></div>')
    rot = -(x0 - x1) / (3.1416 * size) * 360
    b = (f'<div style="position:absolute;top:{y}px;left:0;width:{size}px;height:{size}px;'
         f'{fm.kf([(t0, f"transform:translateX({x0}px)"), (t1, f"transform:translateX({x1}px)")])}">'
         f'<div style="position:absolute;inset:-12px;border-radius:999px;background:{COPPER_SOFT};opacity:.55"></div>'
         f'<div style="position:absolute;inset:0;border-radius:999px;overflow:hidden;box-shadow:0 6px 14px rgba(20,30,45,.25);'
         f'background:radial-gradient(circle at 36% 30%,#F4D3B0 0%,{COPPER} 36%,#8A5530 72%,#4E2D16 100%);'
         f'{fm.kf([(t0, "transform:rotate(0deg)"), (t1, f"transform:rotate({rot:.0f}deg)")])}">'
         f'<div style="position:absolute;left:22%;top:16%;width:22%;height:14%;border-radius:999px;background:rgba(255,255,255,.55)"></div></div></div>')
    return line + b


def hook(fm, w):
    return (f'<div style="position:absolute;inset:0;{fm.kf([(1.6, "opacity:1;transform:none"), (2.0, "opacity:0;transform:translateY(-60px)")])}">'
            f'<div dir="rtl" style="position:absolute;top:80px;right:80px;left:80px;font-family:{LABEL};font-size:22px;font-weight:500;letter-spacing:.16em;color:{COPPER_TEXT}">'
            f'<span dir="ltr">{w["name"]}</span>&lrm; · עולם מותג קונספט</div>'
            f'<div dir="rtl" style="position:absolute;top:150px;right:80px;left:80px;height:340px;box-sizing:border-box;padding:40px;background:{CREAM_DEEP};border-radius:20px;'
            f'display:flex;align-items:center;justify-content:center;text-align:center;font-size:76px;line-height:1.18;font-weight:600;color:{INK}">'
            f'אם נסתיר את הלוגו, עדיין יזהו אותך?</div>'
            f'{ball(fm, 956, 660, 518, .2, 1.5)}</div>')


def header(fm, w):
    tps = w['tps']
    brows = ''.join(f'<div style="position:absolute;bottom:0;right:0;white-space:nowrap;{fm.show(1.95 if i == 0 else S[i], E[i] if i < 4 else D, .15)}">{t["eyebrow"]}</div>'
                    for i, t in enumerate(tps))
    times = [1.95] + [chip_t(i, k) for i in range(5) for k in range(3)]
    nums = ''.join(f'<span style="position:absolute;bottom:0;left:0;{fm.show(t, times[v + 1] if v < 15 else D, .06)}">{v}</span>'
                   for v, t in enumerate(times))
    pts = [(1.95, 'transform:scaleX(0)')]
    for v, t in enumerate(times[1:], 1):
        if t - .12 > pts[-1][0]:
            pts.append((t - .12, f'transform:scaleX({(v - 1) / 15:.3f})'))
        pts.append((t, f'transform:scaleX({v / 15:.3f})'))
    return (f'<div style="position:absolute;inset:0;{fm.show(1.95, END, .3)}">'
            f'<div dir="rtl" style="position:absolute;top:72px;right:80px;left:80px;height:130px">'
            f'<div style="position:absolute;right:0;bottom:18px;width:640px;height:40px;font-family:{LABEL};font-size:22px;font-weight:500;letter-spacing:.16em;color:{COPPER_TEXT}">{brows}</div>'
            f'<div style="position:absolute;left:0;bottom:0;display:flex;align-items:baseline;gap:16px;direction:rtl">'
            f'<span style="font-size:28px;color:{INK_SOFT}">קודים נשארו</span>'
            f'<span dir="ltr" style="position:relative;display:block;width:150px;height:120px;font-family:{DISPLAY};font-size:120px;line-height:1;font-weight:500;color:{COPPER}">{nums}</span>'
            f'</div></div>'
            f'<div style="position:absolute;top:1830px;right:80px;left:80px;height:6px;border-radius:6px;background:{CREAM_DEEP}">'
            f'<div style="position:absolute;inset:0;border-radius:6px;background:{COPPER};transform-origin:right;{fm.kf(pts, "cubic-bezier(.3,0,.2,1)")}"></div></div>'
            f'</div>')


def captions(fm, w):
    out = []
    for i, t in enumerate(w['tps']):
        a, b = (2.05 if i == 0 else S[i] + .15), (E[i] - .35 if i < 4 else END)
        out.append(f'<div dir="rtl" style="position:absolute;top:1500px;right:80px;left:80px;display:flex;align-items:baseline;gap:20px;{fm.window_rise(a, b)}">'
                   f'<span lang="fr" dir="ltr" style="font-family:{DISPLAY};font-style:italic;font-size:56px;line-height:1.1;color:{INK}">{t["fr"]}</span>'
                   f'<span style="font-size:30px;color:{INK_SOFT}">{t["he"]}</span></div>')
        chips = ''.join(
            f'<span style="border:2px solid {COPPER};background:rgba(194,138,90,.12);border-radius:999px;padding:10px 28px;font-size:30px;font-weight:500;color:{INK};'
            f'{fm.kf([(chip_t(i, k) - .25, "opacity:0;transform:translateY(24px)"), (chip_t(i, k), "opacity:1;transform:none")])}">{c}</span>'
            for k, c in enumerate(t['codes']))
        out.append(f'<div dir="rtl" style="position:absolute;top:1600px;right:80px;left:80px;display:flex;flex-wrap:wrap;gap:16px;'
                   f'{fm.show(F[i] + .1, E[i] - .35 if i < 4 else END, .2)}">{chips}</div>')
    return ''.join(out)


def outro(fm, w):
    t0 = END + .3
    thumbs = ''.join(f'<img src="{t["off"]}" alt="" style="width:160px;height:200px;object-fit:cover;object-position:{t["pos"]};border-radius:12px;'
                     f'box-shadow:0 10px 24px rgba(20,30,45,.14);{fm.rise(t0 + .9 + k * .1, 30, .5)}">' for k, t in enumerate(w['tps']))
    return (f'<div style="position:absolute;inset:0;{fm.show(END + .1, D, .35)}">'
            f'<div dir="rtl" style="position:absolute;top:180px;right:80px;left:80px;text-align:center;display:flex;flex-direction:column;gap:8px;'
            f'font-size:96px;line-height:1.1;font-weight:600;color:{INK}">'
            f'<span style="{fm.rise(t0)}">השם ירד.</span>'
            f'<span style="{fm.rise(t0 + .25)}">עדיין <span dir="ltr" style="font-family:{DISPLAY};font-weight:500;font-size:112px;color:{COPPER}">{w["name"]}</span>&lrm;.</span>'
            f'<span style="{fm.rise(t0 + .5)}">ואצלך?</span></div>'
            f'<div style="position:absolute;top:700px;right:100px;left:100px;display:flex;justify-content:space-between;direction:rtl">{thumbs}</div>'
            f'<div dir="rtl" style="position:absolute;top:940px;right:80px;left:80px;text-align:center;font-size:34px;color:{INK_SOFT};{fm.rise(t0 + 1.4)}">'
            f'חמש נקודות מגע. 15 קודים. אף לוגו.</div>'
            f'{ball(fm, 956, 120, 1062, t0 + 1.5, t0 + 2.3, 44, 80)}'
            f'<div dir="rtl" style="position:absolute;top:1200px;right:160px;left:160px;display:flex;flex-direction:column;align-items:center;gap:24px;{fm.rise(t0 + 1.9)}">'
            f'<div style="width:100%;height:132px;border-radius:12px;background:{INK};color:{CREAM};display:flex;align-items:center;justify-content:center;font-size:52px;font-weight:600">אבחון פער המותג</div>'
            f'<div style="font-size:36px;color:{INK_SOFT}">30 דק׳ · בלי עלות</div>'
            f'<div dir="ltr" style="font-family:{LABEL};font-size:24px;font-weight:500;letter-spacing:.28em;color:{INK_SOFT}">HAGITANTEBI.CO.IL</div></div>'
            f'<div style="position:absolute;top:1660px;right:80px;left:80px;display:flex;flex-direction:column;align-items:center;gap:6px;color:{INK};{fm.rise(t0 + 2.2)}">'
            f'<span dir="ltr" style="font-family:{DISPLAY};font-style:italic;font-size:48px">Brand Worlds Studio</span>'
            f'<span style="font-size:24px;letter-spacing:.3em;color:{INK_SOFT}">חגית אנטבי</span></div>'
            f'</div>')


PAGE = """<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="{fonts}">
<style>
html,body{{margin:0;background:{cream}}}
body{{font-family:'Heebo',sans-serif;font-variant-numeric:lining-nums}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{cream}}}
.film *{{animation-duration:{dur}s;animation-iteration-count:1;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
{css}
</style></head>
<body><div id="stage" class="film">{body}</div></body></html>"""


def build(world):
    A = Assets(world)
    w = WORLDS[world](A)
    fm = Film(D)
    body = window(fm, w) + header(fm, w) + captions(fm, w) + hook(fm, w) + outro(fm, w)
    html = PAGE.format(title=f'{w["name"]} · מכסים את השם', fonts=FONTS.replace('&', '&amp;'), cream=CREAM, dur=D, css=fm.style(), body=body)
    open(os.path.join(OUT, world, 'src', 'reel.html'), 'w', encoding='utf-8').write(html)
    print('built', world)


if __name__ == '__main__':
    for n in sys.argv[1:] or list(WORLDS):
        build(n)
