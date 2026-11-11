"""Hanukkah 2026 · PARDON ME° "החנוכייה המנומסת" (studio mode, 30s, 9:16).

    python3 -I build.py            (run from this folder) → reel.html
    node ../../signe-card/src/render.js reel.html 30 ../out/PARDON-ME-9x16.mp4

The brand's code is the elliptical window in a polite cream sleeve. Here the sleeve carries a hanukkiah made of nine
windows. The copper ball rolls in, climbs the shamash arm and becomes the shamash flame. Each night a copper spark runs
the line to the next window: it opens onto a collection print, lights, and says something it is not sorry about.
Then the sleeve slides off (the site's signature move): "בפנים, אף פעם לא מתנצלים."

a/generic-candle.webp — gpt_image_2_6 (Higgsfield job 258c5009), the "ככה משווים" card. The rest are PARDON ME's own assets.
"""
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = 30.0
def P(t): return f'{max(0.0, min(D, t)) / D * 100:.3f}%'

PRINTS = {  # quadrant of a/prints.webp (1400×1400), collection, colour
    'hm': ('0% 100%', 'High Maintenance.', '#C2506F'),
    'wh': ('0% 0%', 'Well, Hello.', '#4E7FA6'),
    'bi': ('100% 100%', 'Bad Influence.', '#9B1B47'),
    'nb': ('100% 0%', 'None of Your Business.', '#1E3A2B'),
}
NIGHTS = [
    ('hm', 'סופגנייה שנייה.<br>לא מתנצלת.'),
    ('wh', 'הדלקתי<br>לפני כולם.'),
    ('bi', 'לא שיתפתי<br>את הלביבות.'),
    ('nb', 'מה קיבלתי במתנה?<br>לא עניינך.'),
    ('hm', 'שמונה לילות.<br>אפס דיאטה.'),
    ('wh', 'הזמנתי את עצמי<br>לכל מסיבה.'),
    ('bi', 'סביבון?<br>אצלי תמיד גימ״ל.'),
    ('nb', 'נתתי לנר<br>לדלוק עד הסוף.'),
]
WX = [960, 860, 760, 660, 420, 320, 220, 120]   # night 1 on the right
SHX = 540
WW, WH = 92, 250
WTOP, SHTOP = 680, 540
BASE_Y = 1050

HOOK_END = 2.4
PORTAL = (2.35, 3.2)
LINE_DRAW = (3.3, 4.2)
BALL_IN = (3.4, 4.5)            # ball rolls in on the base, climbs the shamash arm
SH_LIGHT = 4.6
T0, NIGHT = 5.0, 2.3
T = [T0 + k * NIGHT for k in range(8)]
SLEEVE = (T[-1] + NIGHT, T[-1] + NIGHT + 1.2)   # 23.4 → 24.6
OUTRO = 27.0

def css():
    c = []
    c.append(f'.hk{{animation-name:hk}}@keyframes hk{{0%,{P(PORTAL[1])}{{opacity:1}}{P(PORTAL[1] + .05)},100%{{opacity:0}}}}')
    c.append(f'.hl{{animation-name:hl;animation-timing-function:linear}}@keyframes hl{{0%{{stroke-dashoffset:.86}}{P(HOOK_END - .1)},100%{{stroke-dashoffset:0}}}}')
    c.append(f'.hb{{animation-name:hb;animation-timing-function:linear}}@keyframes hb{{0%{{offset-distance:14%;opacity:1}}{P(HOOK_END - .1)}{{offset-distance:100%;opacity:1;transform:scale(1)}}{P(PORTAL[0] + .25)}{{opacity:1;transform:scale(1.5)}}{P(PORTAL[0] + .45)},100%{{offset-distance:100%;opacity:0;transform:scale(1.5)}}}}')
    c.append(f'.hr{{animation-name:hr;animation-timing-function:linear}}@keyframes hr{{0%{{transform:rotate(0)}}{P(HOOK_END - .1)},100%{{transform:rotate(-560deg)}}}}')
    c.append(f'.portal{{animation-name:portal;animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes portal{{0%,{P(PORTAL[0])}{{clip-path:ellipse(0px 0px at 540px 1700px)}}{P(PORTAL[1])},100%{{clip-path:ellipse(1500px 2600px at 540px 1700px)}}}}')
    # world line + ball
    c.append(f'.wl{{animation-name:wl;animation-timing-function:linear}}@keyframes wl{{0%,{P(LINE_DRAW[0])}{{stroke-dashoffset:1}}{P(LINE_DRAW[1])},100%{{stroke-dashoffset:0}}}}')
    c.append(f'.wb{{animation-name:wb;animation-timing-function:cubic-bezier(.4,0,.5,1)}}@keyframes wb{{0%,{P(BALL_IN[0])}{{offset-distance:0%;opacity:0}}{P(BALL_IN[0] + .05)}{{opacity:1}}{P(BALL_IN[1])}{{offset-distance:100%;opacity:1;transform:scale(1)}}{P(SH_LIGHT)}{{offset-distance:100%;opacity:1;transform:scale(.3)}}{P(SH_LIGHT + .08)},100%{{offset-distance:100%;opacity:0;transform:scale(.2)}}}}')
    c.append(f'.wr{{animation-name:wr;animation-timing-function:linear}}@keyframes wr{{0%,{P(BALL_IN[0])}{{transform:rotate(0)}}{P(BALL_IN[1])},100%{{transform:rotate(-900deg)}}}}')
    # windows: shamash + 8 nights
    opens = [SH_LIGHT - .25] + [t + .6 for t in T]
    for i, t in enumerate(opens):
        c.append(f'.wo{i}{{animation-name:wo{i}}}@keyframes wo{i}{{0%,{P(t)}{{clip-path:inset(100% 0 0 0)}}{P(t + .4)},100%{{clip-path:inset(0 0 0 0)}}}}')
        c.append(f'.fl{i}{{animation-name:fl{i}}}@keyframes fl{i}{{0%,{P(t + .3)}{{opacity:0;transform:scale(0)}}{P(t + .48)}{{opacity:1;transform:scale(1.35)}}{P(t + .66)},100%{{opacity:1;transform:scale(1)}}}}')
    for i, t in enumerate(T):  # the spark
        c.append(f'.sp{i}{{animation-name:sp{i};animation-timing-function:cubic-bezier(.45,0,.55,1)}}@keyframes sp{i}{{0%,{P(t)}{{offset-distance:0%;opacity:0}}{P(t + .03)}{{opacity:1}}{P(t + .6)}{{offset-distance:100%;opacity:1}}{P(t + .7)},100%{{offset-distance:100%;opacity:0}}}}')
    rnd = random.Random(29)
    fk = ''.join(f'{i / 40 * 100:.2f}%{{transform:scaleY({rnd.uniform(.9, 1.08):.3f}) scaleX({rnd.uniform(.94, 1.04):.3f}) rotate({rnd.uniform(-3, 3):.1f}deg)}}' for i in range(41))
    c.append('.flk{animation-name:flk;animation-duration:6s!important;animation-timing-function:ease-in-out!important}@keyframes flk{' + fk + '}')
    c.append(f'.slv{{animation-name:slv;animation-timing-function:cubic-bezier(.6,0,.25,1)}}@keyframes slv{{0%,{P(SLEEVE[0])}{{transform:none}}{P(SLEEVE[1])},100%{{transform:translateX(-1160px)}}}}')
    c.append(f'.bh{{animation-name:bh}}@keyframes bh{{0%,{P(SLEEVE[0] + .6)}{{transform:scale(1.08)}}{P(OUTRO)},100%{{transform:scale(1)}}}}')
    c.append(f'.seal{{animation-name:seal}}@keyframes seal{{0%,{P(SLEEVE[1] + .5)}{{opacity:0;transform:rotate(-14deg) scale(1.6)}}{P(SLEEVE[1] + .75)}{{opacity:1;transform:rotate(-14deg) scale(.94)}}{P(SLEEVE[1] + .95)},100%{{opacity:1;transform:rotate(-14deg) scale(1)}}}}')
    return '\n'.join(c)

FLAME = ('<div class="flk" style="position:absolute;inset:0;transform-origin:50% 90%">'
         '<div style="position:absolute;left:-22px;top:-20px;width:76px;height:96px;border-radius:50%;background:radial-gradient(ellipse at 50% 60%,rgba(255,196,110,.55),rgba(255,160,70,0) 70%)"></div>'
         '<div style="position:absolute;inset:0;border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;background:radial-gradient(ellipse at 50% 72%,#FFFDF3 0%,#FFE7A6 30%,#F6A84B 64%,rgba(214,104,40,0) 100%)"></div></div>')

def window(i, x, top, key):
    pos = PRINTS[key][0]
    return (f'<div style="position:absolute;left:{x - WW / 2}px;top:{top}px;width:{WW}px;height:{WH}px;border-radius:50%;overflow:hidden;background:#E9E1D3;box-shadow:inset 0 3px 8px rgba(30,40,30,.18),0 0 0 1.5px rgba(30,58,43,.35)">'
            f'<div class="wo{i}" style="position:absolute;inset:0;background:url(a/prints.webp);background-size:1100px 1100px;background-position:{pos}"></div></div>'
            f'<div class="fl{i}" style="position:absolute;left:{x - 16}px;top:{top - 60}px;width:32px;height:54px;transform-origin:50% 90%">{FLAME}</div>')

def html():
    wins = window(0, SHX, SHTOP, 'hm') + ''.join(window(i + 1, x, WTOP, NIGHTS[i][0]) for i, x in enumerate(WX))
    stems = f'M{SHX} {SHTOP + WH} V{BASE_Y}' + ''.join(f' M{x} {WTOP + WH} V{BASE_Y}' for x in WX)
    sparks, texts, counters = '', '', ''
    for i, (key, line) in enumerate(NIGHTS):
        x = WX[i]
        sparks += (f'<div class="sp{i}" style="position:absolute;left:0;top:0;width:24px;height:24px;border-radius:50%;offset-path:path(\'M{SHX} {SHTOP + WH} V{BASE_Y} H{x} V{WTOP + WH}\');offset-rotate:0deg;'
                   f'background:radial-gradient(circle at 38% 30%,#F2C9A0,#C98552 45%,#8A4F28);box-shadow:0 0 14px 4px rgba(240,170,100,.6)"></div>')
        a, b = T[i] + .85, (T[i + 1] + .75) if i < 7 else SLEEVE[0] + .2
        _, name, col = PRINTS[key]
        texts += (f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.15" style="display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center">'
                  f'<div style="font-family:\'Bodoni Moda\',serif;font-style:italic;font-size:40px;color:{col}" dir="ltr">{name}</div>'
                  f'<div style="font-family:\'Frank Ruhl Libre\',serif;font-size:66px;font-weight:500;line-height:1.12;color:#1B1F1C" dir="rtl">{line}</div></div>')
        counters += (f'<div class="stack" data-show="{T[i] + .6:.2f},{(T[i + 1] + .6) if i < 7 else SLEEVE[0]:.2f}" data-fade="0.15" style="display:flex;align-items:center;gap:10px" dir="ltr">'
                     f'<span style="font-family:\'Bodoni Moda\',serif;font-style:italic;font-size:30px;color:#5A6359">Nuit</span><span style="font-family:\'Bodoni Moda\',serif;font-size:44px;color:#1E3A2B">{i + 1}</span></div>')
    rep = dict(CSS=css(), WINDOWS=wins, STEMS=stems, BASE=f'M1140 {BASE_Y} H100', BALLPATH=f'M1140 {BASE_Y - 23} H{SHX} V{SHTOP + WH / 2}',
               SPARKS=sparks, TEXTS=texts, COUNTERS=counters, SLEEVE1=f'{SLEEVE[1]:.2f}', SLEEVE0=f'{SLEEVE[0]:.2f}', OUTRO=OUTRO, T0=T0 + .5)
    tpl = (HERE / 'reel.tpl.html').read_text(encoding='utf-8')
    for k, v in rep.items():
        tpl = tpl.replace('{{' + k + '}}', str(v))
    assert '{{' not in tpl, tpl[tpl.find('{{'):tpl.find('{{') + 40]
    (HERE / 'reel.html').write_text(tpl, encoding='utf-8')

if __name__ == '__main__':
    html()
    print('nights', [round(t, 2) for t in T], 'sleeve', SLEEVE, 'outro', OUTRO)
