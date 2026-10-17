# Thursday 22.10 — the offer reel, no world (20s). Hook: "איפה בדיוק המותג שלך מאבד פניות?"
# Frame 0 = the question + a landing-page wireframe with three copper markers. The camera zooms to each marker
# (first screen · price · button) with one question, then pulls back to the offer: אבחון פער המותג · 30 דק׳ · בלי עלות.
# Studio colours from the Brand Worlds Studio design system. Reuses reel.js from oreva-price.html.
# Run: python3 diagnosis-make.py → diagnosis-gap.html ; render: render.js diagnosis-gap.html 20 ../diagnosis-gap.mp4
import os
HERE = os.path.dirname(os.path.abspath(__file__))
DUR = 20
src = open(os.path.join(HERE, 'oreva-price.html')).read()
script = src[src.index('<script>'):]
def p(t): return '%.3f%%' % (t / DUR * 100)

# wireframe card (card coordinates, 620 wide) and the camera states: (from, to, tx, ty, scale), transform-origin 0 0
L, T = 230, 520
FX, FY = 540, 1150                       # where a focused point lands on screen
def focus(px, py, s=1.6): return (FX - s * px, FY - s * py, s)
STATES = [(0, 3.0, L, T, 1), (3.4, 6.3, *focus(310, 286)), (6.9, 9.8, *focus(310, 680)), (10.4, 13.3, *focus(466, 814)),
          (13.9, DUR, 540 - .62 * 310, 540, .62)]
cam = ''
for i, (a, b, tx, ty, s) in enumerate(STATES):
    cam += '%s,%s{transform:translate(%.1fpx,%.1fpx) scale(%.3f)}' % (p(a), p(b) if b < DUR else '100%', tx, ty, s)
cam = cam.replace(p(0) + ',', '0%,', 1)
# the active marker grows on its step
def pulse(k, a, b):
    return '@keyframes mk%d{0%%,%s{transform:scale(1)}%s,%s{transform:scale(1.35)}%s,100%%{transform:scale(1)}}' % (k, p(a - .1), p(a + .3), p(b - .2), p(b + .2))

COPPER, CT, INK, SOFT, CREAM, DEEP, CSOFT = '#C28A5A', '#825630', '#15202E', '#3D4A5C', '#F2EBDC', '#E7DEC9', '#D9AE85'
MK = [(0, 286, 3.4, 6.3), (620, 680, 6.9, 9.8), (330, 814, 10.4, 13.3)]
markers = ''.join(f'<div class="mk{i}" style="position: absolute; left: {x - 44}px; top: {y - 44}px; width: 88px; height: 88px; border-radius: 999px; background: {COPPER}; box-shadow: 0 0 0 14px rgba(217,174,133,.5), 0 10px 24px rgba(20,30,45,.2); display: flex; align-items: center; justify-content: center; font-size: 44px; font-weight: 600; color: {INK}">{i + 1}</div>'
                  for i, (x, y, a, b) in enumerate(MK))
tiles = ''.join(f'<div style="height: 150px; border-radius: 12px; background: {CREAM}; display: flex; flex-direction: column; justify-content: flex-end; padding: 12px; box-sizing: border-box; gap: 8px"><div style="height: 10px; width: 70%; border-radius: 5px; background: {CSOFT}"></div><div style="font-size: 22px; font-weight: 600; color: {SOFT}">₪ —</div></div>' for _ in range(3))
card = f"""<div class="cam" style="position: absolute; left: 0; top: 0; width: 620px; height: 890px; transform-origin: 0 0">
  <div style="position: absolute; inset: 0; border-radius: 20px; background: {DEEP}; box-shadow: 0 24px 60px rgba(20,30,45,.14)"></div>
  <div style="position: absolute; left: 44px; right: 44px; top: 48px; display: flex; justify-content: space-between; align-items: center"><div style="width: 120px; height: 20px; border-radius: 6px; background: {SOFT}"></div><div style="display: flex; gap: 14px"><div style="width: 56px; height: 12px; border-radius: 6px; background: {CSOFT}"></div><div style="width: 56px; height: 12px; border-radius: 6px; background: {CSOFT}"></div><div style="width: 56px; height: 12px; border-radius: 6px; background: {CSOFT}"></div></div></div>
  <div style="position: absolute; left: 44px; right: 44px; top: 96px; height: 380px; border-radius: 14px; border: 3px solid {CSOFT}; background: {CREAM}"></div>
  <div style="position: absolute; right: 44px; top: 504px; width: 420px; height: 28px; border-radius: 8px; background: {SOFT}"></div>
  <div style="position: absolute; right: 44px; top: 556px; width: 340px; height: 16px; border-radius: 8px; background: {CSOFT}"></div>
  <div style="position: absolute; left: 44px; right: 44px; top: 604px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px" dir="rtl">{tiles}</div>
  <div style="position: absolute; right: 44px; top: 782px; width: 220px; height: 64px; border-radius: 12px; background: {SOFT}"></div>
  {markers}
</div>"""

H = "font-family: 'Heebo', sans-serif"
def panel(a, b, inner, first=False):
    show = f'data-show="{a},{b}"' if not first else f'data-show="0,{b}"'
    return f'<div class="stack" {show} data-fade="0.3" style="display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-end; padding: 0 80px 40px; box-sizing: border-box" dir="rtl">{inner}</div>'
def step(n, title, q):
    return (f'<div style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 24px; font-weight: 500; letter-spacing: .3em; color: {CT}" dir="ltr">0{n} / 03</div>'
            f'<div style="font-size: 84px; font-weight: 600; line-height: 1.1; color: {INK}">{title}</div>'
            f'<div style="font-size: 44px; line-height: 1.3; color: {SOFT}; text-align: right">{q}</div>')
panels = (panel(0, 3.0, f'<div style="font-size: 84px; font-weight: 600; line-height: 1.16; color: {INK}; text-align: right">איפה בדיוק המותג שלך<br>מאבד <span style="color: {COPPER}">פניות</span>?</div>', first=True)
          + panel(3.3, 6.4, step(1, 'המסך הראשון', 'מה רואים לפני שגוללים?'))
          + panel(6.8, 9.9, step(2, 'המחיר', 'המחיר מגיע לפני הסיבה לשלם אותו?'))
          + panel(10.3, 13.4, step(3, 'הכפתור', 'ברור מה קורה אחרי הלחיצה?'))
          + panel(13.8, DUR, f'<div style="font-size: 76px; font-weight: 600; line-height: 1.16; color: {INK}; text-align: right">שלוש הנקודות האלה,<br>על האתר <span style="color: {COPPER}">שלך</span>.</div>'))

page = f"""<!doctype html>
<!-- Thursday 22.10 · offer reel (no world) — generated by diagnosis-make.py -->
<html lang="he">
<head>
<meta charset="utf-8">
<title>איפה בדיוק המותג שלך מאבד פניות?</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Heebo:wght@400;500;600&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">
<style>
html,body{{margin:0;background:{CREAM}}}
body{{{H};color:{INK}}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
.film *{{animation-duration:{DUR}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
.cam{{animation-name:cam}}@keyframes cam{{{cam}}}
{''.join('.mk%d{animation-name:mk%d}' % (i, i) + pulse(i, a, b) for i, (x, y, a, b) in enumerate(MK))}
.line{{fill:none;stroke:{COPPER};stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1}}
.ln0{{animation-name:ln0;animation-timing-function:linear}}@keyframes ln0{{0%,{p(.3)}{{stroke-dashoffset:1}}{p(2.6)},100%{{stroke-dashoffset:0}}}}
.lnfade{{animation-name:lnfade}}@keyframes lnfade{{0%,{p(2.8)}{{opacity:1}}{p(3.2)},100%{{opacity:0}}}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(217,174,133,.45);border:1.5px solid {CSOFT};box-shadow:0 10px 28px rgba(20,30,45,.22)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#EBC9A4 0%,#C28A5A 34%,#8A5A34 70%,#4E2F18 100%)}}
.bl0{{animation-name:bl0;animation-timing-function:linear}}@keyframes bl0{{0%,{p(.25)}{{offset-distance:0%;opacity:0}}{p(.35)}{{offset-distance:0%;opacity:1}}{p(2.6)},{p(2.8)}{{offset-distance:100%;opacity:1}}{p(3.2)},100%{{offset-distance:100%;opacity:0}}}}
.rl0{{position:absolute;inset:0;animation-name:rl0;animation-timing-function:linear}}@keyframes rl0{{0%,{p(.35)}{{transform:rotate(0)}}{p(2.6)},100%{{transform:rotate(-400deg)}}}}
@keyframes ln1{{0%,{p(15.0)}{{stroke-dashoffset:1}}{p(16.8)},100%{{stroke-dashoffset:0}}}}
@keyframes bl1{{0%,{p(14.9)}{{offset-distance:0%;opacity:0}}{p(15.0)}{{offset-distance:0%;opacity:1}}{p(16.8)},100%{{offset-distance:100%;opacity:1}}}}
@keyframes rl1{{0%,{p(15.0)}{{transform:rotate(0)}}{p(16.8)},100%{{transform:rotate(-400deg)}}}}
.progress{{animation-name:prog;animation-timing-function:linear;transform-origin:right}}@keyframes prog{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}
</style>
</head>
<body data-duration="{DUR}">
<div id="stage">
<div class="film stack">
{card}
<!-- top panel: cream, above the card, carries the hook and each step's line -->
<div style="position: absolute; left: 0; right: 0; top: 0; height: 500px; background: linear-gradient(to bottom, {CREAM} 86%, rgba(242,235,220,0))">
  <div style="position: absolute; top: 88px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 36px; color: {INK}" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size: 18px; letter-spacing: .3em; color: {SOFT}">חגית אנטבי</div>
  </div>
  <div style="position: absolute; left: 0; right: 0; top: 150px; bottom: 0">{panels}</div>
</div>
<div class="lnfade stack">
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line ln0" pathLength="1" d="M1140 1560 H540"></path></svg>
</div>
<div class="ball bl0" style="offset-path: path('M1140 1560 H540')"><div class="halo"></div><div class="sph"><div class="rl0"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>
<svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line" style="animation-name:ln1;animation-timing-function:linear" pathLength="1" d="M1140 1520 H540"></path></svg>
<div class="ball" style="offset-path: path('M1140 1520 H540'); animation-name:bl1; animation-timing-function:linear"><div class="halo"></div><div class="sph"><div style="position:absolute;inset:0;animation-name:rl1;animation-timing-function:linear"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>
<!-- the offer -->
<div data-in="14.6" style="position: absolute; top: 1190px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center">
  <div style="display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 30px 72px; background: {INK}; color: {CREAM}; border-radius: 12px" dir="rtl"><span style="font-size: 52px; font-weight: 600">אבחון פער המותג</span><span style="font-size: 32px">30 דק׳ · בלי עלות</span></div>
</div>
<div data-show="0,3.1" data-fade="0.3" style="position: absolute; bottom: 110px; left: 0; right: 0; text-align: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; letter-spacing: .3em; color: {SOFT}" dir="ltr">HAGITANTEBI.CO.IL</div>
<div data-show="13.9,20" data-fade="0.3" style="position: absolute; bottom: 110px; left: 0; right: 0; text-align: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 24px; font-weight: 500; letter-spacing: .3em; color: {SOFT}" dir="ltr">HAGITANTEBI.CO.IL</div>
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: rgba(194,138,90,.2)"><div class="progress" style="height: 6px; background: {COPPER}"></div></div>
</div>
</div>
{script}"""
open(os.path.join(HERE, 'diagnosis-gap.html'), 'w').write(page)
print('ok', len(page))
