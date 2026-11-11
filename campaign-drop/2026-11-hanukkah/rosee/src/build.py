"""Hanukkah 2026 · ROSÉE° "פך אחד. שמונה לילות." (studio mode, 30s, 9:16).

    python3 -I build.py            (run from this folder) → reel.html
    node ../../signe-card/src/render.js reel.html 30 ../out/ROSEE-9x16.mp4

The oil-jar miracle in ROSÉE's language: one drop from the dropper fills a hanukkiah of nine glass oil cups, then the
floating wicks light one by one while the night walks toward dawn (ROSÉE is a dawn clock). La Nuit closes the night.

Images/clip (Higgsfield): a/empty.webp (gpt_image_2_6, job 40a72397) → a/full.webp (job fe179ade), both from Le Réveil's
dropper as reference; a/pour.webm = Kling 3.0 pro 8s between them (first + last frame); a/generic-oil.webp (job 5634a52d).
Wick tips measured on full.webp's 752×1344 source (below), scaled ×1080/752.
"""
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = 30.0
def P(t): return f'{max(0.0, min(D, t)) / D * 100:.3f}%'
S = 1080 / 752
WICKS = [695, 613, 536, 461, 289, 215, 137.5, 56.5]   # night 1 = rightmost
WICK_Y, SH_X, SH_Y = 677.5, 375, 628.5

HOOK_END = 2.4
PORTAL = (2.35, 3.2)
POUR = 5.0                     # the clip starts (8s)
SH_LIGHT = 13.4
T = [14.0 + k * .72 for k in range(8)]   # 14.0 … 19.04
NUIT = (20.4, 24.2)
OUTRO = 27.0

def css():
    c = []
    c.append(f'.hk{{animation-name:hk}}@keyframes hk{{0%,{P(PORTAL[1])}{{opacity:1}}{P(PORTAL[1] + .05)},100%{{opacity:0}}}}')
    c.append(f'.hl{{animation-name:hl;animation-timing-function:linear}}@keyframes hl{{0%{{stroke-dashoffset:.86}}{P(HOOK_END - .1)},100%{{stroke-dashoffset:0}}}}')
    c.append(f'.hb{{animation-name:hb;animation-timing-function:linear}}@keyframes hb{{0%{{offset-distance:14%;opacity:1}}{P(HOOK_END - .1)}{{offset-distance:100%;opacity:1;transform:scale(1)}}{P(PORTAL[0] + .25)}{{opacity:1;transform:scale(1.5)}}{P(PORTAL[0] + .45)},100%{{offset-distance:100%;opacity:0;transform:scale(1.5)}}}}')
    c.append(f'.hr{{animation-name:hr;animation-timing-function:linear}}@keyframes hr{{0%{{transform:rotate(0)}}{P(HOOK_END - .1)},100%{{transform:rotate(-560deg)}}}}')
    c.append(f'.portal{{animation-name:portal;animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes portal{{0%,{P(PORTAL[0])}{{clip-path:circle(0px at 540px 1700px)}}{P(PORTAL[1])},100%{{clip-path:circle(2300px at 540px 1700px)}}}}')
    lights = [SH_LIGHT] + T
    for i, t in enumerate(lights):
        c.append(f'.fl{i}{{animation-name:fl{i}}}@keyframes fl{i}{{0%,{P(t)}{{opacity:0;transform:scale(0)}}{P(t + .18)}{{opacity:1;transform:scale(1.4)}}{P(t + .4)},100%{{opacity:1;transform:scale(1)}}}}')
    rnd = random.Random(15)
    fk = ''.join(f'{i / 40 * 100:.2f}%{{transform:scaleY({rnd.uniform(.9, 1.08):.3f}) scaleX({rnd.uniform(.94, 1.04):.3f}) rotate({rnd.uniform(-3, 3):.1f}deg)}}' for i in range(41))
    c.append('.flk{animation-name:flk;animation-duration:6s!important;animation-timing-function:ease-in-out!important}@keyframes flk{' + fk + '}')
    # night → dawn: a warm dawn veil rises with every candle
    g = f'0%,{P(SH_LIGHT)}{{opacity:0}}' + ''.join(f'{P(t + .3)}{{opacity:{(i + 1) * .09:.2f}}}' for i, t in enumerate(T)) + f'{P(NUIT[0])},{P(D)}{{opacity:.85}}'
    c.append(f'.dawn{{animation-name:dawn}}@keyframes dawn{{{g}}}')
    c.append(f'.glow{{animation-name:glow}}@keyframes glow{{0%,{P(SH_LIGHT)}{{opacity:0}}{P(T[-1] + .5)},100%{{opacity:1}}}}')
    c.append(f'.nz{{animation-name:nz}}@keyframes nz{{0%,{P(NUIT[0])}{{transform:scale(.9)}}{P(NUIT[1])},100%{{transform:scale(1)}}}}')
    return '\n'.join(c)

FLAME = ('<div class="flk" style="position:absolute;inset:0;transform-origin:50% 90%">'
         '<div style="position:absolute;left:-18px;top:-16px;width:58px;height:74px;border-radius:50%;background:radial-gradient(ellipse at 50% 60%,rgba(255,200,130,.6),rgba(255,170,90,0) 70%)"></div>'
         '<div style="position:absolute;inset:0;border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;background:radial-gradient(ellipse at 50% 72%,#FFFDF3 0%,#FFE7A6 32%,#F6A84B 66%,rgba(214,104,40,0) 100%)"></div></div>')

def flame(i, x, y):
    sx, sy = x * S, y * S
    w, h = 22, 40
    return f'<div class="fl{i}" style="position:absolute;left:{sx - w / 2:.1f}px;top:{sy - h + 6:.1f}px;width:{w}px;height:{h}px;transform-origin:50% 90%">{FLAME}</div>'

def html():
    flames = flame(0, SH_X, SH_Y) + ''.join(flame(i + 1, x, WICK_Y) for i, x in enumerate(WICKS))
    counters = ''.join(
        f'<div class="stack" data-show="{t:.2f},{(T[i + 1] if i < 7 else NUIT[0]):.2f}" data-fade="0.08" style="display:flex;align-items:baseline;justify-content:center;gap:16px" dir="rtl">'
        f'<span style="font-family:\'Assistant\',sans-serif;font-size:40px;font-weight:300;color:#F7E7E2">לילה</span>'
        f'<span style="font-family:\'Cormorant Garamond\',serif;font-size:96px;color:#F2C9B8">{i + 1}</span></div>' for i, t in enumerate(T))
    rep = dict(CSS=css(), FLAMES=flames, COUNTERS=counters, POUR=POUR, NUIT0=NUIT[0], NUIT1=NUIT[1], OUTRO=OUTRO,
               SH=SH_LIGHT, T0=T[0])
    tpl = (HERE / 'reel.tpl.html').read_text(encoding='utf-8')
    for k, v in rep.items():
        tpl = tpl.replace('{{' + k + '}}', str(v))
    assert '{{' not in tpl, tpl[tpl.find('{{'):tpl.find('{{') + 40]
    (HERE / 'reel.html').write_text(tpl, encoding='utf-8')

if __name__ == '__main__':
    html()
    print('lights', [round(t, 2) for t in [SH_LIGHT] + T])
