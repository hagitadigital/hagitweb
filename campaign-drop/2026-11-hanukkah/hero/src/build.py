"""Hanukkah 2026 · hero film "8 לילות · 8 עולמות" (studio mode, 30s, 9:16).

    python3 -I build.py                     (run from this folder)
    node ../../../../.claude/skills/brandos-brand-world-reel/scripts/render.js reel.html 30 ../out/HANUKKAH-8-worlds-9x16.mp4

Story: the hook shows a generic Hanukkah feed (the same sufganiya in six businesses). Her copper ball, a sugar-dusted
copper sufganiya, rolls along the copper line under the feed; the line becomes the base of a hanukkiah. Each night the
ball rolls to the next cup, the line draws that arm, a candle rises and lights, and a portal opens from the flame into
another world's Hanukkah. Outro: all eight worlds, the hanukkiah fully lit, the question back to the viewer + CTA.
"""
import shutil, subprocess, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
A = HERE / 'a'
D = 30.0
def P(t): return f'{max(0.0, min(D, t)) / D * 100:.3f}%'
def ff(*a): subprocess.run(['ffmpeg', '-v', 'error', '-y', *map(str, a)], check=True)

# ── the eight worlds (night order: right to left) ────────────────────────────────────────
WORLDS = [
    # key, source, no, business, name, line, object-position
    ('signe', 'a/noir.png', 17, 'בית קינוחים', 'SIGNÉ°', 'ארבע סופגניות.<br>כל אחת חתומה ביד.', '50% 52%'),
    ('miel', 'miel/assets/38-slice-chocolat-framboise.webp', 27, 'בייקרי', 'MIEL°', 'שמונה נרות.<br>שמונה פרוסות.', '50% 50%'),
    ('pardon', 'pardon-me/assets/gift.webp', 29, 'נרות וריחות לבית', 'PARDON ME°', 'שמונה נרות.<br>אף אחד לא מתנצל.', '50% 50%'),
    ('rosee', 'rosee/collection/lumiere.webp', 15, 'טיפוח', 'ROSÉE°', 'נס פך השמן?<br>אצלנו: טיפה אחת עם שחר.', '50% 55%'),
    ('encore', 'encore/assets/touchpoints/box-open.webp', 28, 'תכשיטים', 'ENCORE°', 'מתנה לחג<br>שלא יורדת אחרי החג.', '50% 50%'),
    ('pancakerie', 'pancakerie/assets/stack-pistache.webp', 26, 'ארוחות בוקר', 'PANCAKERIE°', 'השנה גם הלביבה<br>מגיעה בצבע.', '50% 50%'),
    ('regard', 'regard/assets/portraits/01-la-muse.webp', 16, 'אופטיקה', 'REGARD°', 'בחנוכה<br>רואים את האור אחרת.', '50% 35%'),
    ('oreva', 'oreva/assets/founder-counter-full-line.webp', 24, 'סטודיו לטיפוח', 'ORÉVA°', 'מתנה לחג:<br>קודם הידיים.', '42% 50%'),
]

# ── geometry (stage px) ──────────────────────────────────────────────────────────────────
WX, WY, WW, WH = 80, 170, 920, 1120                     # the world window
BASE_Y = 1840                                           # hanukkiah base = the hook's copper line
CUP_Y, SH_CUP_Y = 1740, 1690                            # top of the arms (candles / shamash)
CANDLE_H = 100
CX = [960, 860, 760, 660, 420, 320, 220, 120]           # night 1 on the right
SH_X = 540
BALL_R = 34
PATH_X0, PATH_X1 = 1160, 40                             # the ball's path: M1160 y H40
BALL_Y = BASE_Y - BALL_R - 2
HOOK_X0 = 980                                          # where the ball sits on frame 0
def odist(x): return (PATH_X0 - x) / (PATH_X0 - PATH_X1) * 100

# ── timing ───────────────────────────────────────────────────────────────────────────────
HOOK_END = 2.9
NIGHT0, NIGHT = 5.0, 2.65
T = [NIGHT0 + k * NIGHT for k in range(8)]
OUTRO = T[-1] + NIGHT - 0.05                             # 26.2

def build_assets():
    for key, src, *_ in WORLDS:
        s = HERE / src if src.startswith('a/') else REPO / src
        ff('-i', s, '-vf', 'scale=1100:-1:flags=lanczos', '-quality', '88', A / f'w-{key}.webp')
    ff('-i', A / 'generic.png', '-vf', 'scale=420:-1:flags=lanczos', '-quality', '88', A / 'generic.webp')

def css():
    c = []
    # ball travel along the base line
    k = [f'0%{{offset-distance:{odist(HOOK_X0):.2f}%}}',
         f'{P(2.5)},{P(T[0])}{{offset-distance:{odist(SH_X):.2f}%}}']
    deg = lambda x: -(PATH_X0 - x) / (2 * 3.14159 * BALL_R) * 360
    deg0 = deg(HOOK_X0)
    rot = [f'0%{{transform:rotate({deg0:.0f}deg)}}']
    rot.append(f'{P(2.5)},{P(T[0])}{{transform:rotate({deg(SH_X):.0f}deg)}}')
    for i, t in enumerate(T):
        k.append(f'{P(t + .55)},{P(T[i + 1] if i < 7 else D)}{{offset-distance:{odist(CX[i]):.2f}%}}')
        rot.append(f'{P(t + .55)},{P(T[i + 1] if i < 7 else D)}{{transform:rotate({deg(CX[i]):.0f}deg)}}')
    c.append('.bmove{animation-name:bmove}@keyframes bmove{' + ''.join(k) + '}')
    c.append('.broll{animation-name:broll}@keyframes broll{' + ''.join(rot) + '}')
    # base line draws right → left: to the centre with the hook, then to the end
    c.append(f'.base{{animation-name:base;animation-timing-function:linear}}@keyframes base{{0%{{stroke-dashoffset:{1 - (PATH_X0 - HOOK_X0) / (PATH_X0 - 90):.3f}}}'
             f'{P(2.5)}{{stroke-dashoffset:{1 - (PATH_X0 - SH_X) / (PATH_X0 - 90):.3f}}}{P(3.8)},100%{{stroke-dashoffset:0}}}}')
    # shamash
    arms = [(SH_X, SH_CUP_Y, 3.3)] + [(x, CUP_Y, t + .5) for x, t in zip(CX, T)]
    for i, (x, y, t) in enumerate(arms):
        c.append(f'.arm{i}{{animation-name:arm{i};animation-timing-function:linear}}@keyframes arm{i}{{0%,{P(t)}{{stroke-dashoffset:1}}{P(t + .3)},100%{{stroke-dashoffset:0}}}}')
        c.append(f'.cdl{i}{{animation-name:cdl{i}}}@keyframes cdl{i}{{0%,{P(t + .2)}{{transform:scaleY(0)}}{P(t + .45)},100%{{transform:scaleY(1)}}}}')
        c.append(f'.fl{i}{{animation-name:fl{i}}}@keyframes fl{i}{{0%,{P(t + .45)}{{opacity:0;transform:scale(0)}}{P(t + .62)}{{opacity:1;transform:scale(1.35)}}{P(t + .8)},100%{{opacity:1;transform:scale(1)}}}}')
    # flicker (one shared keyframe, phase-shifted per flame)
    rnd = random.Random(8)
    fk = ''.join(f'{i / 40 * 100:.2f}%{{transform:scaleY({rnd.uniform(.9, 1.08):.3f}) scaleX({rnd.uniform(.94, 1.04):.3f}) rotate({rnd.uniform(-3, 3):.1f}deg)}}' for i in range(41))
    c.append('.flk{animation-name:flk;animation-duration:6s!important;animation-timing-function:ease-in-out!important}@keyframes flk{' + fk + '}')
    # warm glow grows with every candle
    g = f'0%,{P(3.6)}{{opacity:0}}{P(4.4)}{{opacity:.25}}' + ''.join(f'{P(t + 1.0)}{{opacity:{.25 + (i + 1) * .09:.2f}}}' for i, t in enumerate(T)) + '100%{opacity:1}'
    c.append(f'.glow{{animation-name:glow}}@keyframes glow{{{g}}}')
    # portals: each world opens from its own flame
    for i, t in enumerate(T):
        cx, cy = CX[i] - WX, CUP_Y - CANDLE_H - 28 - WY
        c.append(f'.pt{i}{{animation-name:pt{i};animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes pt{i}{{0%,{P(t + 1.0)}{{clip-path:circle(0px at {cx}px {cy}px)}}{P(t + 1.85)},100%{{clip-path:circle(1700px at {cx}px {cy}px)}}}}')
        c.append(f'.rg{i}{{animation-name:rg{i};animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes rg{i}{{0%,{P(t + 1.0)}{{r:0;opacity:0}}{P(t + 1.05)}{{opacity:1}}{P(t + 1.85)}{{r:1700px;opacity:1}}{P(t + 2.1)},100%{{r:1700px;opacity:0}}}}')
        c.append(f'.zm{i}{{animation-name:zm{i};animation-timing-function:linear}}@keyframes zm{i}{{0%,{P(t + 1.0)}{{transform:scale(1.14)}}{P(t + 1.0 + NIGHT + 1.2)},100%{{transform:scale(1)}}}}')
    return '\n'.join(c)

FLAME = ('<div class="flk" style="position:absolute;inset:0;transform-origin:50% 90%">'
         '<div style="position:absolute;left:-22px;top:-20px;width:76px;height:96px;border-radius:50%;background:radial-gradient(ellipse at 50% 60%,rgba(255,196,110,.55),rgba(255,160,70,0) 70%)"></div>'
         '<div style="position:absolute;inset:0;border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;background:radial-gradient(ellipse at 50% 72%,#FFFDF3 0%,#FFE7A6 30%,#F6A84B 64%,rgba(214,104,40,.0) 100%)"></div>'
         '<div style="position:absolute;left:11px;top:30px;width:10px;height:18px;border-radius:50%;background:rgba(120,170,255,.35)"></div></div>')

def candle(i, x, cup_y):
    top = cup_y - CANDLE_H
    return (f'<div class="cdl{i}" style="position:absolute;left:{x - 13}px;top:{top}px;width:26px;height:{CANDLE_H}px;transform-origin:50% 100%;'
            f'border-radius:4px 4px 2px 2px;background:linear-gradient(90deg,#E9D9BE,#FBF3E4 45%,#E2CFAF)">'
            f'<div style="position:absolute;left:12px;top:-10px;width:2px;height:12px;background:#3A2A1E"></div></div>'
            f'<div class="fl{i}" style="position:absolute;left:{x - 16}px;top:{top - 58}px;width:32px;height:54px;transform-origin:50% 90%">{FLAME}</div>')

def html():
    hook_names = [('קונדיטוריה', '412'), ('בית קפה', '388'), ('סטודיו לטיפוח', '291'), ('חנות תכשיטים', '356'), ('מאפייה', '407'), ('חנות לבית', '274')]
    tiles = ''.join(
        f'<div style="background:#FFFFFF;border-radius:16px;overflow:hidden;box-shadow:0 14px 34px rgba(62,47,37,.12);display:flex;flex-direction:column">'
        f'<img src="a/generic.webp" alt="" style="width:100%;height:250px;object-fit:cover;display:block">'
        f'<div style="padding:12px 16px 14px;display:flex;flex-direction:column;gap:4px" dir="rtl"><span style="font-size:22px;font-weight:600;color:#2E2A27">{n}</span>'
        f'<span style="font-size:20px;color:#7A716A">חג אורים שמח! · ♡ {l}</span></div></div>' for n, l in hook_names)
    worlds = ''
    for i, (key, _, no, biz, name, line, pos) in enumerate(WORLDS):
        worlds += (f'<div class="stack pt{i}"><img class="cover zm{i}" src="a/w-{key}.webp" alt="{name} · Hanukkah" style="object-position:{pos}">'
                   f'<div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(to top,rgba(23,17,12,.55),rgba(23,17,12,0))"></div>'
                   f'<div style="position:absolute;top:26px;right:26px;padding:10px 18px;border-radius:999px;background:rgba(23,17,12,.62);color:#F4E9D8;font-size:20px;letter-spacing:.06em" dir="rtl">עולם מותג {no}</div></div>')
    rings = ''.join(f'<circle class="rg{i}" cx="{CX[i] - WX}" cy="{CUP_Y - CANDLE_H - 28 - WY}" r="0" fill="none" stroke="#D99A6C" stroke-width="5"></circle>' for i in range(8))
    texts, counters = '', ''
    for i, (key, _, no, biz, name, line, pos) in enumerate(WORLDS):
        a, b = T[i] + 1.3, (T[i + 1] + 1.0) if i < 7 else OUTRO
        texts += (f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.25" style="display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center" dir="rtl">'
                  f'<div style="font-size:25px;font-weight:500;letter-spacing:.05em;color:#D99A6C">{biz} · <span dir="ltr" style="font-family:\'Cormorant Garamond\',serif;font-size:31px;letter-spacing:.08em">{name}</span></div>'
                  f'<div style="font-size:54px;font-weight:500;line-height:1.18;color:#F7EEDF">{line}</div></div>')
        counters += (f'<div class="stack" data-show="{T[i] + 1.0:.2f},{(T[i + 1] + 1.0) if i < 7 else D:.2f}" data-fade="0.2" style="display:flex;align-items:center;gap:12px;justify-content:flex-start" dir="rtl">'
                     f'<span style="font-size:24px;color:#CDBFAE">לילה</span><span style="font-family:\'Cormorant Garamond\',serif;font-size:46px;color:#E8B48A">{i + 1}</span></div>')
    arms = f'<path class="line arm0" pathLength="1" d="M{SH_X} {BASE_Y} V{SH_CUP_Y}"></path>' + ''.join(
        f'<path class="line arm{i + 1}" pathLength="1" d="M{x} {BASE_Y} V{CUP_Y}"></path>' for i, x in enumerate(CX))
    cups = ''.join(f'<path class="line arm{i}" pathLength="1" d="M{x - 26} {y} H{x + 26}"></path>' for i, (x, y) in enumerate([(SH_X, SH_CUP_Y)] + [(x, CUP_Y) for x in CX]))
    candles = candle(0, SH_X, SH_CUP_Y) + ''.join(candle(i + 1, x, CUP_Y) for i, x in enumerate(CX))
    mosaic = ''.join(f'<div style="position:relative;border-radius:12px;overflow:hidden"><img class="cover" src="a/w-{k}.webp" alt="" style="object-position:{pos}">'
                     f'<div style="position:absolute;left:0;right:0;bottom:0;padding:8px 0 10px;text-align:center;background:linear-gradient(to top,rgba(23,17,12,.75),rgba(23,17,12,0));font-family:\'Cormorant Garamond\',serif;font-size:22px;letter-spacing:.06em;color:#F7EEDF" dir="ltr">{n}</div></div>'
                     for k, _, _, _, n, _, pos in WORLDS)
    tpl = (HERE / 'reel.tpl.html').read_text(encoding='utf-8')
    for k, v in dict(CSS=css(), TILES=tiles, WORLDS=worlds, RINGS=rings, TEXTS=texts, COUNTERS=counters, ARMS=arms, CUPS=cups,
                     CANDLES=candles, MOSAIC=mosaic, BALLPATH=f'M{PATH_X0} {BALL_Y} H{PATH_X1}', BASEPATH=f'M{PATH_X0} {BASE_Y} H90',
                     OUTRO=f'{OUTRO:.2f}', WX=WX, WY=WY, WW=WW, WH=WH, HOOK_END=HOOK_END).items():
        tpl = tpl.replace('{{' + k + '}}', str(v))
    assert '{{' not in tpl, tpl[tpl.find('{{'):tpl.find('{{') + 40]
    (HERE / 'reel.html').write_text(tpl, encoding='utf-8')

if __name__ == '__main__':
    import sys
    if '--html' not in sys.argv: build_assets()
    html()
    print('nights', [round(t, 2) for t in T], 'outro', round(OUTRO, 2))
