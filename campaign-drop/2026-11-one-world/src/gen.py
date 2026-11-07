#!/usr/bin/env python3
"""Campaign 2026-11 "One World" — two studio reels, 9:16, built from the worlds' own assets.

  reel-a-*.html  Direction 1 · 20s · four shots:
      1 (0–4)   a well-made generic serum            "יש עסקים שנראים טוב."
      2 (4–9)   hard cuts VELUNE° ↔ Crema°            "ויש מותגים שאי אפשר להתבלבל ביניהם."
      3 (9–15)  ROSÉE° box → its site in a phone     "אסטרטגיה. זהות. חוויה. עולם אחד."
      4 (15–20) studio window + CTA                  "בונים מותג עם נוכחות משלו."
      two CTA variants: -cta (short) and -gap (with the "גלי מה מונע…" line)
  reel-b.html    Direction 2 · 15s · "אל תהיי המותג שמשווים." → montage of worlds → "תהיי המותג שבוחרים."

Every motion is a keyframe generated from (seconds, css) pairs, so timings live here, in seconds.
Render: node render.js reel-a-cta.html 20 ../reel-a-cta.mp4
"""
import pathlib

HERE = pathlib.Path(__file__).parent
FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500'
         '&amp;family=Heebo:wght@300;400;500;600;700&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">')
S = dict(bg='#FAF8F3', cream='#EEE6D8', ink='#6B563F', copper='#C4765A', gold='#B8894A', dark='#3E2F25')


class Film:
    def __init__(self, dur):
        self.dur, self.css, self.n = dur, [], 0

    def p(self, t):
        return f'{max(0, min(self.dur, t)) / self.dur * 100:.3f}%'

    def kf(self, steps, ease='cubic-bezier(.4,0,.2,1)'):
        """steps: [(t, 'css'), ...] in seconds. Holds the first value before and the last value after."""
        self.n += 1
        name = f'k{self.n}'
        body = [f'0%{{{steps[0][1]}}}'] + [f'{self.p(t)}{{{c}}}' for t, c in steps] + [f'100%{{{steps[-1][1]}}}']
        self.css.append(f'@keyframes {name}{{{"".join(body)}}}')
        return f'animation-name:{name};animation-timing-function:{ease};'

    def show(self, a, b, f=.35):
        """visible a→b with fades of f (a<=0: visible from frame 0, b>=dur: holds to the last frame)."""
        st = []
        st += [(0, 'opacity:1')] if a <= 0 else [(a - f, 'opacity:0'), (a, 'opacity:1')]
        st += [(self.dur, 'opacity:1')] if b >= self.dur else [(b, 'opacity:1'), (b + f, 'opacity:0')]
        return self.kf(st, 'linear')

    def cut(self, a, b):
        return self.show(a, b, .001)

    def rise(self, t, d=.6, y=30):
        return self.kf([(t, f'opacity:0;transform:translateY({y}px)'), (t + d, 'opacity:1;transform:none')])

    def mask(self, t, d=.7):
        return self.kf([(t, 'transform:translateY(110%)'), (t + d, 'transform:none')])

    def page(self, title, body):
        return f'''<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>{title}</title>{FONTS}
<style>
html,body{{margin:0;background:{S['bg']}}}
body{{font-family:'Heebo',sans-serif}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{S['bg']}}}
.film *{{animation-duration:{self.dur}s;animation-iteration-count:infinite;animation-fill-mode:both}}
.st{{position:absolute;inset:0}}
.cv{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.mask{{display:block;overflow:hidden;padding-bottom:.08em}}
.mask>span{{display:block}}
.lat{{font-family:'Cormorant Garamond',serif}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}
{chr(10).join(self.css)}
</style></head>
<body><div id="stage"><div class="film st">
{body}
</div></div></body></html>'''


def studio_sig(color=S['dark'], sub='#8B7B6E'):
    return (f'<div style="position:absolute;top:84px;right:80px;display:flex;flex-direction:column;align-items:flex-end;gap:4px;z-index:5">'
            f'<div class="lat" style="font-style:italic;font-size:36px;color:{color}" dir="ltr">Brand Worlds Studio</div>'
            f'<div style="font-size:17px;letter-spacing:.3em;color:{sub}">חגית אנטבי</div></div>')


def ball(fl, d, t0, t1, fade_at=None):
    """her copper ball rolling on a line (recipe 5)."""
    line = fl.kf([(t0, 'stroke-dashoffset:1'), (t1, 'stroke-dashoffset:0')], 'linear')
    steps = [(t0 - .01, 'offset-distance:0%;opacity:0'), (t0, 'offset-distance:0%;opacity:1'), (t1, 'offset-distance:100%;opacity:1')]
    if fade_at:
        steps += [(fade_at, 'offset-distance:100%;opacity:1'), (fade_at + .3, 'offset-distance:100%;opacity:0')]
    move = fl.kf(steps, 'linear')
    spin = fl.kf([(t0, 'transform:rotate(0deg)'), (t1, 'transform:rotate(-400deg)')], 'linear')
    return (f'<svg class="st" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">'
            f'<path class="line" style="{line}" pathLength="1" d="{d}"></path></svg>'
            f'<div class="ball" style="offset-path:path(\'{d}\');{move}"><div class="halo"></div><div class="sph">'
            f'<div style="position:absolute;inset:0;{spin}"><div style="position:absolute;left:13px;top:13px;width:52px;height:52px;border-radius:50%;border:1px solid rgba(250,228,200,.65)"></div>'
            f'<div class="lat" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:21px;color:#F5DEC4" dir="ltr">BW</div>'
            f'<div style="position:absolute;left:12px;top:46px;width:14px;height:14px;border-radius:50%;background:#FFF7EC;box-shadow:0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>')


def phone(inner, x=240, y=200, w=600, h=1300, style=''):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:64px;overflow:hidden;'
            f'background:#F6EAE2;box-shadow:0 0 0 14px #2B2320,0 0 0 16px #5A4B42,0 60px 120px rgba(80,40,30,.35);{style}">{inner}</div>')


def cta(variant, t):
    gap = ''
    if variant == 'gap':
        gap = (f'<div style="font-size:36px;line-height:1.45;color:{S["ink"]};max-width:900px">'
               'גלי מה מונע מהנראות של העסק שלך<br>לשקף את הערך האמיתי שלו.</div>')
    return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:26px;text-align:center" dir="rtl">{gap}'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:30px 80px;background:{S["ink"]};color:{S["bg"]};border-radius:14px">'
            f'<span style="font-size:54px;font-weight:500">אבחון פער המותג</span><span style="font-size:32px;opacity:.85">ללא עלות</span></div>'
            f'<div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:26px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div></div>')


def marks(x, y, w, h, style=''):
    c = S['copper']
    m = []
    for (l, t, b1, b2) in [(x - 22, y - 22, 'top', 'left'), (x + w - 22, y - 22, 'top', 'right'),
                           (x - 22, y + h - 22, 'bottom', 'left'), (x + w - 22, y + h - 22, 'bottom', 'right')]:
        m.append(f'<div style="position:absolute;left:{l}px;top:{t}px;width:44px;height:44px;border-{b1}:2px solid {c};border-{b2}:2px solid {c}"></div>')
    return f'<div class="st" style="{style}">{"".join(m)}</div>'


# ───────────────────────────── Reel A ─────────────────────────────
def reel_a(variant):
    fl = Film(20)
    out = []

    # SHOT 4 · invitation (15–20) — bottom layer, holds to the last frame
    win = (260, 520, 560, 700)  # x, y, w, h — a small studio window cycling through the worlds
    pics = ['09-bottle-blush-garden-m.webp', 'shelf.webp', 'cup-rosa-heart.jpg', 'bag-street.webp', '20-ecrin-box-open-m.webp']
    cyc = []
    for i, src in enumerate(pics):
        a = 15.2 + i * .9
        b = 30 if i == len(pics) - 1 else a + .9
        cyc.append(f'<img class="cv" src="a/{src}" alt="" style="{fl.show(a, b, .3)}">')
    push = fl.kf([(15, 'transform:scale(1.08)'), (20, 'transform:scale(1)')], 'linear')
    head_top = 230 if variant == 'cta' else 200
    out.append(f'''<section class="st" style="background:{S['bg']};{fl.show(15, 30, .45)}">
  {studio_sig()}
  <div style="position:absolute;top:{head_top}px;left:60px;right:60px;text-align:center;font-size:84px;font-weight:600;line-height:1.15;color:{S['dark']}" dir="rtl">
    <span class="mask"><span style="{fl.mask(15.4)}">בונים מותג</span></span>
    <span class="mask"><span style="{fl.mask(15.75)}">עם נוכחות <span style="color:{S['copper']}">משלו.</span></span></span>
  </div>
  <div style="position:absolute;left:{win[0]}px;top:{win[1]}px;width:{win[2]}px;height:{win[3]}px;overflow:hidden;box-shadow:0 40px 100px rgba(62,47,37,.22);{fl.kf([(15, 'opacity:0;transform:scale(.92)'), (15.8, 'opacity:1;transform:none')])}">
    <div class="st" style="{push}">{''.join(cyc)}</div>
  </div>
  {marks(*win, style=fl.show(15.9, 30, .4))}
  <div style="position:absolute;top:{1310 if variant == 'cta' else 1270}px;left:0;right:0;{fl.rise(16.6)}">{cta(variant, 16.6)}</div>
  {ball(fl, 'M1140 1820 C900 1780 700 1800 540 1800', 16.0, 17.6)}
</section>''')

    # SHOT 3 · ROSÉE: the box becomes the site (9–15)
    ph = (240, 190, 600, 1300)
    clip = fl.kf([(10.3, 'clip-path:inset(0px 0px 0px 0px round 0px)'),
                  (11.1, f'clip-path:inset({ph[1]}px {1080 - ph[0] - ph[2]}px {1920 - ph[1] - ph[3]}px {ph[0]}px round 64px)')])
    boxpush = fl.kf([(9, 'transform:scale(1.12)'), (11.1, 'transform:scale(1)')], 'cubic-bezier(.3,0,.3,1)')
    screens = []
    for i, (src, a, b) in enumerate([('rosee-site-0.jpg', 10.6, 12.25), ('rosee-site-3600.jpg', 12.2, 13.55), ('rosee-site-5000.jpg', 13.5, 30)]):
        mv = fl.kf([(a, 'transform:translateY(70px)'), (a + .7, 'transform:none')]) if i else ''
        screens.append(f'<div class="st" style="{fl.show(a, b, .3)}"><img class="cv" src="a/{src}" alt="" style="{mv}"></div>')
    words = [('אסטרטגיה.', 9.4), ('זהות.', 11.0), ('חוויה.', 12.3)]
    w_html = ' '.join(f'<span style="display:inline-block;{fl.rise(t, .5, 24)}">{w}</span>' for w, t in words)
    out.append(f'''<section class="st" style="background:linear-gradient(180deg,#F7E9E1 0%,#EED6CB 100%);{fl.kf([(8.999, 'opacity:0'), (9, 'opacity:1'), (15, 'opacity:1'), (15.45, 'opacity:0')], 'linear')}">
  <div class="st" style="{clip}">
    <div class="st" style="{boxpush}"><img class="cv" src="a/box-card.webp" alt="" style="object-position:50% 40%"></div>
    <div class="st" style="left:{ph[0]}px;top:{ph[1]}px;width:{ph[2]}px;height:{ph[3]}px;right:auto;bottom:auto">{''.join(screens)}</div>
  </div>
  <div style="position:absolute;left:{ph[0]}px;top:{ph[1]}px;width:{ph[2]}px;height:{ph[3]}px;border-radius:64px;box-shadow:0 0 0 14px #2B2320,0 0 0 16px #5A4B42,0 60px 120px rgba(80,40,30,.35);{fl.show(11.0, 30, .3)}"></div>
  <div class="st" style="background:linear-gradient(180deg,rgba(247,233,225,0) 62%,rgba(247,233,225,.92) 80%,#F4E2D9 100%)"></div>
  <div style="position:absolute;top:1560px;left:40px;right:40px;text-align:center;color:#4A3530" dir="rtl">
    <div style="font-size:62px;font-weight:600;line-height:1.2">{w_html}</div>
    <div style="font-size:92px;font-weight:700;line-height:1.25;color:{S['copper']};{fl.rise(13.7, .6, 30)}">עולם אחד.</div>
  </div>
  <div class="lat" style="position:absolute;top:96px;left:0;right:0;text-align:center;font-size:30px;letter-spacing:.5em;color:#7A5A50;{fl.show(9, 10.8, .3)}" dir="ltr">ROSÉE°</div>
</section>''')

    # SHOT 2 · hard cuts VELUNE° ↔ Crema° (4–9)
    V = dict(name='VELUNE°', band='#1F2A44', ink='#F3EEE6', sub='#B9A9C9', font="font-family:'Cormorant Garamond',serif;letter-spacing:.42em;font-weight:500",
             tag='Maison de Parfum · בושם הוא לא ריח. הוא מקום.')
    C = dict(name='Crema°', band='#F0E6DA', ink='#3A2A22', sub='#B5532F', font="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:64px",
             tag='Caffè Torino · הבוקר שלך, בגוון שלך.')
    cuts = [(V, '12-bottle-crepuscule-dusk-m.webp'), (C, 'cup-rosa-heart.jpg'), (V, '20-ecrin-box-open-m.webp'),
            (C, 'cup-foresta-rosetta.jpg'), (V, '01-lineup-three-editions-arch-m.webp'), (C, 'cup-viola-heart.jpg')]
    for i, (w, src) in enumerate(reversed(cuts)):
        k = len(cuts) - 1 - i
        a = 4 + k * .8
        b = 9.0 if k == len(cuts) - 1 else a + .8
        zoom = fl.kf([(a, 'transform:scale(1.07)'), (a + .8, 'transform:scale(1)')], 'linear')
        first = k == 0
        l1 = f'<span class="mask"><span style="{fl.mask(4.15) if first else ""}">ויש מותגים</span></span>'
        l2 = f'<span class="mask"><span style="{fl.mask(4.45) if first else ""}">שאי אפשר להתבלבל ביניהם.</span></span>'
        out.append(f'''<section class="st" style="background:{w['band']};{fl.cut(a, b if k == len(cuts) - 1 else b)}">
  <div style="position:absolute;left:0;top:0;width:1080px;height:1350px;overflow:hidden"><img class="cv" src="a/{src}" alt="" style="{zoom}"></div>
  <div style="position:absolute;top:70px;left:70px;font-size:46px;color:{'#FFFFFF' if w is V else w['ink']};{w['font']};text-shadow:{'0 2px 18px rgba(20,25,45,.45)' if w is V else 'none'}" dir="ltr">{w['name']}</div>
  <div style="position:absolute;top:1350px;left:0;right:0;height:570px;background:{w['band']}"></div>
  <div style="position:absolute;top:1420px;left:70px;right:70px;text-align:right;font-size:70px;font-weight:600;line-height:1.18;color:{w['ink']}" dir="rtl">{l1}{l2}</div>
  <div style="position:absolute;top:1700px;left:70px;right:70px;text-align:right;font-size:26px;letter-spacing:.04em;color:{w['sub']}" dir="rtl">{w['tag']}</div>
</section>''')

    # SHOT 1 · hook (0–4): a generic, well-made serum — looks good, belongs to nobody
    push1 = fl.kf([(0, 'transform:scale(1)'), (4, 'transform:scale(1.07)')], 'linear')
    sweep = fl.kf([(.3, 'transform:translateX(-120%) skewX(-12deg)'), (2.6, 'transform:translateX(120%) skewX(-12deg)')], 'cubic-bezier(.5,0,.5,1)')
    out.append(f'''<section class="st" style="background:radial-gradient(ellipse at 50% 62%,#FBF7F1 0%,#EEE6D8 58%,#E2D6C4 100%);{fl.cut(0, 4)}">
  {studio_sig()}
  <div style="position:absolute;top:240px;left:80px;right:80px;text-align:right;font-size:96px;font-weight:600;line-height:1.12;color:{S['dark']}" dir="rtl">יש עסקים<br><span style="color:{S['copper']}">שנראים טוב.</span></div>
  <div style="position:absolute;left:130px;top:560px;width:820px;height:1025px">
    <img src="a/generic-serum.jpg" alt="" style="width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply;filter:brightness(1.055) contrast(1.04);-webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 72%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 72%,transparent 100%);display:block;{push1}">
    <div class="st" style="overflow:hidden;mix-blend-mode:screen"><div class="st" style="background:linear-gradient(90deg,transparent 30%,rgba(255,250,240,.55) 50%,transparent 70%);{sweep}"></div></div>
  </div>
  <div style="position:absolute;left:0;right:0;top:1500px;height:30px;background:radial-gradient(ellipse at 50% 0%,rgba(80,60,40,.18),transparent 70%)"></div>
  {ball(fl, 'M1140 1700 H540', .2, 3.0)}
</section>''')

    out.append(f'<div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18)">'
               f'<div style="height:6px;background:{S["copper"]};transform-origin:right;{fl.kf([(0, "transform:scaleX(0)"), (20, "transform:scaleX(1)")], "linear")}"></div></div>')
    return fl.page('One World · A', '\n'.join(out))


# ───────────────────────────── Reel B ─────────────────────────────
def reel_b():
    fl = Film(15)
    out = []
    # OUTRO (11.4–15): the answer
    strip = ['12-bottle-crepuscule-dusk-m.webp', 'box-card.webp', 'bag-street.webp', 'cup-rosa-heart.jpg']
    tiles = ''.join(
        f'<div style="width:210px;height:280px;overflow:hidden;border-radius:6px;{fl.rise(11.9 + i * .12, .5, 40)}"><img src="a/{s}" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
        for i, s in enumerate(strip))
    out.append(f'''<section class="st" style="background:{S['bg']};{fl.show(11.4, 30, .45)}">
  {studio_sig()}
  <div style="position:absolute;top:270px;left:70px;right:70px;text-align:center;font-size:40px;font-weight:400;color:#A4927F;text-decoration:line-through;text-decoration-color:{S['copper']};text-decoration-thickness:3px;{fl.rise(11.6, .5, 20)}" dir="rtl">אל תהיי המותג שמשווים.</div>
  <div style="position:absolute;top:360px;left:50px;right:50px;text-align:center;font-size:104px;font-weight:600;line-height:1.12;color:{S['dark']}" dir="rtl">
    <span class="mask"><span style="{fl.mask(11.8)}">תהיי המותג</span></span>
    <span class="mask"><span style="{fl.mask(12.1)}"><span style="color:{S['copper']}">שבוחרים.</span></span></span>
  </div>
  <div style="position:absolute;top:740px;left:0;right:0;display:flex;justify-content:center;gap:18px" dir="ltr">{tiles}</div>
  <div style="position:absolute;top:1170px;left:0;right:0;{fl.rise(12.8)}">{cta('cta', 12.8)}</div>
  {ball(fl, 'M1140 1690 C900 1640 720 1660 540 1660', 12.6, 14.0)}
</section>''')

    # MONTAGE (2.6–11.6): product, packaging, digital, atmosphere — each a world with its own identity
    shots = [
        ('12-bottle-crepuscule-dusk-m.webp', 'מוצר', 'VELUNE°', 'cover', '50% 50%', '#1F2A44'),
        ('box-card.webp', 'אריזה', 'ROSÉE°', 'cover', '50% 40%', '#F4E2D9'),
        ('PHONE', 'דיגיטל', 'ROSÉE°', '', '', '#EED6CB'),
        ('bag-street.webp', 'אווירה', 'ENCORE°', 'cover', '50% 50%', '#3A2A20'),
        ('20-ecrin-box-open-m.webp', 'אריזה', 'VELUNE°', 'cover', '50% 50%', '#7A1E30'),
        ('cup-rosa-heart.jpg', 'חוויה', 'Crema°', 'contain', '50% 50%', '#F0E6DA'),
    ]
    T0, STEP = 2.6, 1.5
    for i, (src, cat, world, fit, pos, bg) in reversed(list(enumerate(shots))):
        a = 2.25 if i == 0 else T0 + i * STEP
        b = a + STEP if i < len(shots) - 1 else 11.85
        push = fl.kf([(a - .4, 'transform:scale(1.1)'), (b + .4, 'transform:scale(1)')], 'linear')
        if src == 'PHONE':
            inner = f'<div class="st" style="background:linear-gradient(180deg,#F7E9E1,#EBCFC3)"></div><div class="st" style="{push}">' + phone(
                f'<img class="cv" src="a/rosee-site-5000.jpg" alt="">', 250, 260, 580, 1256) + '</div>'
        else:
            inner = f'<div class="st" style="background:{bg}"></div><div class="st" style="{push}"><img class="cv" src="a/{src}" alt="" style="object-fit:{fit};object-position:{pos}"></div>'
        dark = bg in ('#1F2A44', '#3A2A20', '#7A1E30')
        fade = .001 if i == 0 else .4
        out.append(f'''<section class="st" style="{fl.show(a, b, fade)}">
  {inner}
  <div class="st" style="background:linear-gradient(0deg,rgba(30,22,18,.55) 0%,rgba(30,22,18,0) 26%)"></div>
  <div style="position:absolute;bottom:120px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:flex-end;color:#FFF8EE" dir="rtl">
    <div style="font-size:58px;font-weight:500;{fl.rise(a + .1, .5, 20)}">{cat}</div>
    <div class="lat" style="font-size:40px;letter-spacing:.24em;{fl.rise(a + .25, .5, 20)}" dir="ltr">{world}</div>
  </div>
</section>''')

    # HOOK (0–2.9): two near-identical generic cards — frame 0 already shows the line and the proof
    def card(src, name, price):
        return (f'<div style="width:430px;box-sizing:border-box;padding:16px;background:#FFF;border-radius:18px;box-shadow:0 24px 60px rgba(62,47,37,.14);display:flex;flex-direction:column;gap:14px" dir="rtl">'
                f'<div style="position:relative"><img src="a/{src}" alt="" style="width:100%;height:500px;object-fit:cover;border-radius:10px;display:block">'
                f'<span style="position:absolute;top:12px;right:12px;padding:7px 16px;border-radius:999px;background:#2E2A27;color:#F4F2EF;font-size:20px">ככה משווים</span></div>'
                f'<div style="display:flex;justify-content:space-between;font-size:24px;color:#6E6660"><span>{name}</span><strong style="color:#2E2A27">{price}</strong></div></div>')
    portal = fl.kf([(2.3, 'clip-path:circle(0px at 540px 1700px)'), (3.1, 'clip-path:circle(2300px at 540px 1700px)')])
    hook = f'''<section class="st" style="background:{S['cream']};{fl.cut(0, 3.1)}">
  {studio_sig()}
  <div style="position:absolute;top:250px;left:80px;right:80px;text-align:right;font-size:96px;font-weight:600;line-height:1.12;color:{S['dark']}" dir="rtl">אל תהיי<br>המותג <span style="color:{S['copper']}">שמשווים.</span></div>
  <div style="position:absolute;top:640px;left:0;right:0;display:flex;justify-content:center;gap:40px" dir="rtl">
    {card('generic-serum.jpg', 'סרום · 30ml', '₪149')}{card('generic-perfume.jpg', 'בושם · 50ml', '₪159')}
  </div>
  <div style="position:absolute;top:1340px;left:0;right:0;text-align:center;font-size:34px;color:#8B7B6E" dir="rtl">כשאין עולם, נשאר רק המחיר.</div>
  {ball(fl, 'M1140 1700 H540', .2, 2.3, fade_at=2.6)}
</section>'''
    # the montage enters through a copper portal at the ball's end point
    out.insert(len(out), '')
    body = '\n'.join(out)
    # wrap montage sections + outro under the hook; the hook sits on top until the portal opens
    ring = fl.kf([(2.3, 'r:44;opacity:1'), (3.1, 'r:1400;opacity:0')])
    portal_layer = (f'<div class="st" style="z-index:3;{portal}">{"".join(out[1:])}</div>'
                    f'<svg class="st" style="z-index:4" width="1080" height="1920" viewBox="0 0 1080 1920"><circle cx="540" cy="1700" r="44" fill="none" stroke="{S["copper"]}" stroke-width="5" style="{ring}"></circle></svg>')
    body = f'{out[0]}\n<div class="st" style="z-index:2">{hook}</div>\n{portal_layer}'
    body += (f'<div style="position:absolute;left:0;right:0;bottom:0;height:6px;z-index:9;background:rgba(196,118,90,.18)">'
             f'<div style="height:6px;background:{S["copper"]};transform-origin:right;{fl.kf([(0, "transform:scaleX(0)"), (15, "transform:scaleX(1)")], "linear")}"></div></div>')
    return fl.page('One World · B', body)


if __name__ == '__main__':
    (HERE / 'reel-a-cta.html').write_text(reel_a('cta'), encoding='utf-8')
    (HERE / 'reel-a-gap.html').write_text(reel_a('gap'), encoding='utf-8')
    (HERE / 'reel-b.html').write_text(reel_b(), encoding='utf-8')
    print('wrote reel-a-cta.html, reel-a-gap.html, reel-b.html')
