"""Hanukkah 2026 · MIEL° "השולחן מתמלא" (brand mode, 30s, 9:16). Direction A, approved 11.11.

    python3 -I build.py            (run from this folder) → reel.html
    node ../../signe-card/src/render.js reel.html 30 ../out/MIEL-table-9x16.mp4

A profile screen in MIEL's own design (not Instagram's). Its highlight bubbles are the eight nights. Each night the gold
ball rolls along the line under the bubbles to the next one, the bubble lifts off, flies into the post and lands on the
table as that night's slice — and that night's candle on the hanukkiah lights. By night eight: a full Hanukkah table.

Images (a/): the six slices are MIEL's own (miel/assets/35–41), pistachio + ריבת חלב were generated from slice 35 with
gpt_image_2_6; all eight cut out with Higgsfield's background remover. The table (a/table.webp) is gpt_image_2_6 from the
same reference. Candle wick positions below are measured on that image (896×1120).
"""
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = 30.0
def P(t): return f'{max(0.0, min(D, t)) / D * 100:.3f}%'

# night order: colours alternate light / dark
SLICES = [  # file, Hebrew line
    ('vanille-framboise', 'ביסקוויט וניל · לב פטל'),
    ('chocolat-caramel', 'ביסקוויט שוקולד · לב קרמל'),
    ('pistache', 'ביסקוויט וניל · לב פיסטוק'),
    ('chocolat-vanille', 'ביסקוויט שוקולד · לב קרם וניל'),
    ('ribat-chalav', 'ביסקוויט וניל · לב ריבת חלב'),
    ('chocolat-framboise', 'ביסקוויט שוקולד · לב פטל'),
    ('vanille-caramel', 'ביסקוויט וניל · לב קרמל'),
    ('vanille-vanille', 'ביסקוויט וניל · לב קרם וניל'),
]

# post = the table image, 896×1120 → 960×1200 at (60, 660)
PX, PY, PS = 60, 660, 960 / 896
def tp(x, y): return PX + x * PS, PY + y * PS
WICKS = [635, 591.5, 547.5, 505, 402.5, 359, 315, 272.5]        # right → left: night 1 is the rightmost candle
FLAME_BASE_Y, SH_X, SH_BASE_Y = 160, 456, 110

# highlight bubbles
BW, BGAP, BY = 104, 16, 520                                      # size, gap, centre y
BX = [1080 / 2 + (3.5 - i) * (BW + BGAP) for i in range(8)]      # i=0 rightmost
LINE_Y = BY + BW / 2 + 54                                        # the line under the labels

# where each slice lands (screen px: centre-bottom of the cut-out, width)
LAND = [(840, 1385, 205), (635, 1375, 205), (430, 1385, 205), (228, 1375, 205),
        (848, 1655, 245), (622, 1665, 245), (396, 1655, 245), (192, 1668, 232)]
SL_H = 0.65                                                      # cut-out h/w

T0, NIGHT = 2.7, 2.65
T = [T0 + k * NIGHT for k in range(8)]
OUTRO = T[-1] + NIGHT                                            # 24.25
SH_LIGHT = 2.0

def css():
    c = []
    # the ball on the line under the bubbles: x positions
    xs = [1140] + [BX[i] for i in range(8)]
    total = xs[0] - 20
    od = lambda x: (xs[0] - x) / total * 100
    k = [f'0%,{P(.6)}{{offset-distance:0%}}', f'{P(T0 - .3)}{{offset-distance:{od(1120):.2f}%}}']
    rot = [f'0%,{P(.6)}{{transform:rotate(0)}}']
    deg = lambda x: -(xs[0] - x) / (3.14159 * 46) * 360
    for i, t in enumerate(T):
        k.append(f'{P(t + .45)},{P(T[i + 1] if i < 7 else D)}{{offset-distance:{od(BX[i]):.2f}%}}')
        rot.append(f'{P(t + .45)},{P(T[i + 1] if i < 7 else D)}{{transform:rotate({deg(BX[i]):.0f}deg)}}')
    c.append('.bm{animation-name:bm}@keyframes bm{' + ''.join(k) + '}')
    c.append('.br{animation-name:br}@keyframes br{' + ''.join(rot) + '}')
    c.append(f'.ln{{animation-name:ln;animation-timing-function:linear}}@keyframes ln{{0%,{P(.6)}{{stroke-dashoffset:1}}' + ''.join(
        f'{P(t + .45)},{P(T[i + 1] if i < 7 else D)}{{stroke-dashoffset:{1 - od(BX[i]) / 100:.3f}}}' for i, t in enumerate(T)) + '}')
    for i, t in enumerate(T):
        tap, fly0, fly1 = t + .5, t + .7, t + 1.55
        # bubble: tap (ring turns gold, press), then it lifts away and a soft empty ring stays
        c.append(f'.bb{i}{{animation-name:bb{i}}}@keyframes bb{i}{{0%,{P(tap)}{{transform:scale(1)}}{P(tap + .12)}{{transform:scale(.88)}}{P(fly0)},100%{{transform:scale(1)}}}}')
        c.append(f'.bi{i}{{animation-name:bi{i}}}@keyframes bi{i}{{0%,{P(fly0)}{{opacity:1}}{P(fly0 + .05)},100%{{opacity:.28}}}}')
        c.append(f'.bg{i}{{animation-name:bg{i}}}@keyframes bg{i}{{0%,{P(tap)}{{opacity:0}}{P(tap + .15)},100%{{opacity:1}}}}')
        # the flying bubble
        c.append(f'.fl{i}{{animation-name:fl{i};animation-timing-function:cubic-bezier(.45,0,.3,1)}}@keyframes fl{i}{{0%,{P(fly0)}{{offset-distance:0%;opacity:0}}{P(fly0 + .02)}{{opacity:1}}{P(fly1)}{{offset-distance:100%;opacity:1}}{P(fly1 + .12)},100%{{offset-distance:100%;opacity:0}}}}')
        c.append(f'.fs{i}{{animation-name:fs{i};animation-timing-function:cubic-bezier(.45,0,.3,1)}}@keyframes fs{i}{{0%,{P(fly0)}{{transform:scale(1)}}{P(fly0 + .45)}{{transform:scale(1.5)}}{P(fly1)},100%{{transform:scale(1.15)}}}}')
        # the slice lands
        c.append(f'.ls{i}{{animation-name:ls{i}}}@keyframes ls{i}{{0%,{P(fly1 - .05)}{{opacity:0;transform:scale(.55) translateY(-30px)}}{P(fly1 + .1)}{{opacity:1;transform:scale(1.06) translateY(4px)}}{P(fly1 + .3)},100%{{opacity:1;transform:none}}}}')
        c.append(f'.rp{i}{{animation-name:rp{i};animation-timing-function:ease-out}}@keyframes rp{i}{{0%,{P(fly1)}{{opacity:0;transform:scale(.3)}}{P(fly1 + .05)}{{opacity:.9}}{P(fly1 + .7)},100%{{opacity:0;transform:scale(1.5)}}}}')
        # the candle lights with the landing
        c.append(f'.cf{i}{{animation-name:cf{i}}}@keyframes cf{i}{{0%,{P(fly1)}{{opacity:0;transform:scale(0)}}{P(fly1 + .18)}{{opacity:1;transform:scale(1.35)}}{P(fly1 + .4)},100%{{opacity:1;transform:scale(1)}}}}')
    c.append(f'.cfs{{animation-name:cfs}}@keyframes cfs{{0%,{P(SH_LIGHT)}{{opacity:0;transform:scale(0)}}{P(SH_LIGHT + .2)}{{opacity:1;transform:scale(1.35)}}{P(SH_LIGHT + .4)},100%{{opacity:1;transform:scale(1)}}}}')
    rnd = random.Random(27)
    fk = ''.join(f'{i / 40 * 100:.2f}%{{transform:scaleY({rnd.uniform(.9, 1.08):.3f}) scaleX({rnd.uniform(.94, 1.04):.3f}) rotate({rnd.uniform(-3, 3):.1f}deg)}}' for i in range(41))
    c.append('.flk{animation-name:flk;animation-duration:6s!important;animation-timing-function:ease-in-out!important}@keyframes flk{' + fk + '}')
    g = f'0%,{P(SH_LIGHT)}{{opacity:0}}{P(SH_LIGHT + .4)}{{opacity:.2}}' + ''.join(f'{P(t + 1.6)}{{opacity:{.2 + (i + 1) * .1:.2f}}}' for i, t in enumerate(T)) + '100%{opacity:1}'
    c.append(f'.glow{{animation-name:glow}}@keyframes glow{{{g}}}')
    return '\n'.join(c)

FLAME = ('<div class="flk" style="position:absolute;inset:0;transform-origin:50% 90%">'
         '<div style="position:absolute;left:-16px;top:-14px;width:50px;height:64px;border-radius:50%;background:radial-gradient(ellipse at 50% 60%,rgba(255,200,120,.6),rgba(255,170,90,0) 70%)"></div>'
         '<div style="position:absolute;inset:0;border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;background:radial-gradient(ellipse at 50% 72%,#FFFDF3 0%,#FFE7A6 32%,#F6A84B 66%,rgba(214,104,40,0) 100%)"></div></div>')

def flame(cls, x, y):
    sx, sy = tp(x, y)
    w, h = 18, 32
    return f'<div class="{cls}" style="position:absolute;left:{sx - w / 2:.1f}px;top:{sy - h + 4:.1f}px;width:{w}px;height:{h}px;transform-origin:50% 90%">{FLAME}</div>'

def html():
    bubbles, flyers, slices, ripples, flames, caps = '', '', '', '', '', ''
    for i, (f, line) in enumerate(SLICES):
        x = BX[i]
        bubbles += (f'<div style="position:absolute;left:{x - BW / 2:.1f}px;top:{BY - BW / 2}px;width:{BW}px;display:flex;flex-direction:column;align-items:center;gap:10px">'
                    f'<div class="bb{i}" style="position:relative;width:{BW}px;height:{BW}px">'
                    f'<div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 200deg,#E7C0BD,#C98989,#B8956A,#E7C0BD)"></div>'
                    f'<div class="bg{i}" style="position:absolute;inset:0;border-radius:50%;background:#D9CFC4"></div>'
                    f'<div style="position:absolute;inset:4px;border-radius:50%;background:#FBF4F1"></div>'
                    f'<div class="bi{i}" style="position:absolute;inset:8px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 50% 40%,#FFF8F5,#F3E4DF)">'
                    f'<img src="a/s-{f}.webp" alt="" style="position:absolute;left:4px;top:18px;width:{BW - 24}px"></div></div>'
                    f'<div style="font-family:\'Assistant\',sans-serif;font-size:21px;font-weight:600;color:#4A2C24" dir="rtl">לילה {i + 1}</div></div>')
        lx, ly, lw = LAND[i]
        lh = lw * SL_H
        path = f'M{x:.1f} {BY} C{x:.1f} {BY + 260} {lx:.1f} {ly - lh / 2 - 380:.1f} {lx:.1f} {ly - lh / 2:.1f}'
        flyers += (f'<div class="fl{i}" style="position:absolute;left:0;top:0;width:{BW}px;height:{BW}px;offset-path:path(\'{path}\');offset-rotate:0deg">'
                   f'<div class="fs{i}" style="position:absolute;inset:0;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 50% 40%,#FFF8F5,#F3E4DF);box-shadow:0 0 0 4px #FBF4F1,0 0 0 7px #C98989,0 18px 34px rgba(74,44,36,.25)">'
                   f'<img src="a/s-{f}.webp" alt="" style="position:absolute;left:4px;top:18px;width:{BW - 8}px"></div></div>')
        ripples += f'<div class="rp{i}" style="position:absolute;left:{lx - lw * .55:.1f}px;top:{ly - lw * .14:.1f}px;width:{lw * 1.1:.1f}px;height:{lw * .28:.1f}px;border-radius:50%;border:2px solid rgba(184,149,106,.7)"></div>'
        slices += (f'<img class="ls{i}" src="a/s-{f}.webp" alt="MIEL slice · {line}" style="position:absolute;left:{lx - lw / 2:.1f}px;top:{ly - lh:.1f}px;width:{lw}px;'
                   f'transform-origin:50% 100%;filter:drop-shadow(0 14px 12px rgba(110,60,50,.22))">')
        flames += flame(f'cf{i}', WICKS[i], FLAME_BASE_Y)
        a, b = T[i] + 1.6, (T[i + 1] + 1.55) if i < 7 else OUTRO
        caps += (f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.2" style="display:flex;align-items:center;justify-content:center">'
                 f'<div style="display:flex;align-items:center;gap:14px;padding:12px 26px;border-radius:999px;background:rgba(251,244,241,.92);box-shadow:0 10px 26px rgba(74,44,36,.14)" dir="rtl">'
                 f'<span style="font-family:\'Cormorant Garamond\',serif;font-style:italic;font-size:30px;color:#B8956A" dir="ltr">Nuit {i + 1}</span>'
                 f'<span style="font-family:\'Assistant\',sans-serif;font-size:26px;font-weight:600;color:#4A2C24">{line}</span></div></div>')
    flames += flame('cfs', SH_X, SH_BASE_Y)
    line_d = f'M1140 {LINE_Y} H20'
    tpl = (HERE / 'reel.tpl.html').read_text(encoding='utf-8')
    for k, v in dict(CSS=css(), BUBBLES=bubbles, FLYERS=flyers, SLICES=slices, RIPPLES=ripples, FLAMES=flames, CAPS=caps,
                     LINE=line_d, LINE_Y=LINE_Y, BALL_Y=LINE_Y - 23, OUTRO=f'{OUTRO:.2f}', PX=PX, PY=PY).items():
        tpl = tpl.replace('{{' + k + '}}', str(v))
    assert '{{' not in tpl, tpl[tpl.find('{{'):tpl.find('{{') + 40]
    (HERE / 'reel.html').write_text(tpl, encoding='utf-8')

if __name__ == '__main__':
    html()
    print('nights', [round(t, 2) for t in T], 'outro', round(OUTRO, 2))
