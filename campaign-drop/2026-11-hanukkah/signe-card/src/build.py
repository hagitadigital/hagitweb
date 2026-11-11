"""Hanukkah 2026 · SIGNÉ° "כרטיס החתימה" (studio mode, 30s, 9:16). Direction B, approved 11.11 — no price on SIGNÉ's card.

    python3 -I build.py [--html]            (run from this folder; --html skips the video cuts)
    node render.js reel.html 30 ../out/SIGNE-carte-9x16.mp4      (render.js = the reel skill's + <video data-vstart> seeking)

Hook: a white catalogue shot of a generic sufganiya with a grey spec card ("ככה משווים" · grams · ₪12) pinned to it by a
thin line. Her copper ball sits on the card; it rolls down the line onto the sufganiya and a portal opens into SIGNÉ's dark
set. From there the card is SIGNÉ's: glass, the edition, what is inside, and where the price stood — the signature.
Four editions swap mid-spin, the card follows. Filling, coffret. Outro: the two cards side by side, the ball rolls from the
grey one to SIGNÉ's: "אותה סופגנייה? לא אותו כרטיס. כי זה לא אותו עולם."

Clips come from campaign-drop/2026-11-signe-hanukkah/clips/ on branch claude/kind-cannon-nojzbs (Kling, made for Les Lumières).
Set CLIPS=<folder with those mp4s> to rebuild the videos.
"""
import os, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = HERE / 'a'
D = 30.0
def P(t): return f'{max(0.0, min(D, t)) / D * 100:.3f}%'
def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *map(str, a)], check=True)

# ── timing (reel seconds) ───────────────────────────────────────────────────────────────
ROLL0 = (1.55, 2.45)                  # hook: the ball rolls from the card onto the generic sufganiya
PORTAL = (2.45, 3.3)
SPIN_B = 2.45                         # the spin video starts under the portal
DROP = (0.6, 4.0); LAND_SRC = 1.9     # drop-noir.mp4 source window; Le Noir lands at src 1.9
WHIPS = [('whip-noir-framboise', 0.2, 3.6, 1.7), ('whip-framboise-pistache', 0.6, 3.4, 1.3), ('whip-pistache-vanille', 0.5, 4.0, 1.55)]
t = SPIN_B + DROP[1] - DROP[0]
LAND = SPIN_B + LAND_SRC - DROP[0]
SWAPS = []
for _, a, b, m in WHIPS:
    SWAPS.append(t + m - a); t += b - a
SPIN_END = t                          # the vanille holds its last frame after this
COEUR = (16.7, 20.5)                  # filling.mp4 src 0 → 3.8
BOITE = (20.3, 24.7)                  # coffret-open.mp4 src 1.2 → 5.0 (+ hold)
OUTRO = 24.6

# card geometry
CARD = dict(x=80, y=410, w=500)
HOOK_LINE = 'M505 702 C565 722 605 782 600 840'          # grey card corner → the generic sugar top
SIG_LINE = 'M566 772 C600 810 596 860 580 900'           # glass card corner → Le Noir's top

EDITIONS = [  # name, line (from Les Lumières), latin no
    ('Le Noir', 'שוקולד 70% · עלי זהב', 'N°1'),
    ('La Framboise', 'פטל · קונפי בפנים', 'N°2'),
    ('La Pistache', 'פיסטוק סיציליאני', 'N°3'),
    ('La Vanille', 'וניל מדגסקר · סוכר שרוף', 'N°4'),
]
ED_WIN = [(LAND + .5, SWAPS[0] - .12), (SWAPS[0] + .12, SWAPS[1] - .12), (SWAPS[1] + .12, SWAPS[2] - .12), (SWAPS[2] + .12, COEUR[0] - .1)]

def build_videos():
    C = Path(os.environ.get('CLIPS', HERE / 'clips'))
    vp9 = ['-an', '-c:v', 'libvpx-vp9', '-crf', '20', '-b:v', '0', '-g', '12', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2']
    ins = ['-i', C / 'drop-noir.mp4'] + sum([['-i', C / f'{n}.mp4'] for n, *_ in WHIPS], [])
    ch = [f'[0:v]trim={DROP[0]}:{DROP[1]},setpts=PTS-STARTPTS[s0]'] + \
         [f'[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS[s{i}]' for i, (_, a, b, _) in enumerate(WHIPS, 1)] + \
         ['[s0][s1][s2][s3]concat=n=4:v=1:a=0,fps=30[v]']
    ff(*ins, '-filter_complex', ';'.join(ch), '-map', '[v]', *vp9, A / 'spin.webm')
    ff('-i', C / 'filling.mp4', '-t', '3.9', *vp9, A / 'coeur.webm')
    ff('-ss', '1.2', '-i', C / 'coffret-open.mp4', '-t', '3.8', *vp9, A / 'boite.webm')

SIGN_PATH = 'M6 40 C30 8 44 8 46 30 C48 50 60 50 72 22 C80 6 92 8 90 28 C88 44 104 46 128 20 C140 8 152 12 170 26'

def glass_card(inner, cls='', style=''):
    return (f'<div class="{cls}" style="position:absolute;left:{CARD["x"]}px;top:{CARD["y"] - 20}px;width:{CARD["w"]}px;box-sizing:border-box;padding:28px 32px 26px;'
            f'border-radius:20px;background:linear-gradient(150deg,rgba(255,250,240,.16),rgba(255,250,240,.05));border:1px solid rgba(255,240,220,.32);'
            f'box-shadow:0 30px 70px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.25);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);{style}" dir="rtl">{inner}</div>')

def css():
    c = []
    # hook line + ball (copper grows behind the ball)
    c.append(f'.hl{{animation-name:hl;animation-timing-function:linear}}@keyframes hl{{0%,{P(ROLL0[0])}{{stroke-dashoffset:1}}{P(ROLL0[1])},100%{{stroke-dashoffset:0}}}}')
    c.append(f'.hb{{animation-name:hb;animation-timing-function:cubic-bezier(.5,0,.6,1)}}@keyframes hb{{0%,{P(ROLL0[0])}{{offset-distance:0%;opacity:1}}{P(ROLL0[1])}{{offset-distance:100%;opacity:1;transform:scale(1)}}{P(PORTAL[0] + .3)}{{opacity:1;transform:scale(1.6)}}{P(PORTAL[0] + .55)},100%{{offset-distance:100%;opacity:0;transform:scale(1.6)}}}}')
    c.append(f'.hr{{animation-name:hr;animation-timing-function:linear}}@keyframes hr{{0%,{P(ROLL0[0])}{{transform:rotate(0)}}{P(ROLL0[1])},100%{{transform:rotate(-260deg)}}}}')
    c.append(f'.portal{{animation-name:portal;animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes portal{{0%,{P(PORTAL[0])}{{clip-path:circle(0px at 600px 840px)}}{P(PORTAL[1])},100%{{clip-path:circle(2300px at 600px 840px)}}}}')
    c.append(f'.pring{{animation-name:pring;animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes pring{{0%,{P(PORTAL[0])}{{r:0;opacity:1}}{P(PORTAL[1])}{{r:2300px;opacity:1}}{P(PORTAL[1] + .2)},100%{{r:2300px;opacity:0}}}}')
    # SIGNÉ line + ball: draws, rolls, settles after the landing; a small hop at every swap; gone for the filling
    a0 = LAND + .35
    c.append(f'.sl{{animation-name:sl;animation-timing-function:linear}}@keyframes sl{{0%,{P(a0)}{{stroke-dashoffset:1;opacity:1}}{P(a0 + .5)},{P(COEUR[0] - .3)}{{stroke-dashoffset:0;opacity:1}}{P(COEUR[0])},100%{{stroke-dashoffset:0;opacity:0}}}}')
    c.append(f'.sb{{animation-name:sb;animation-timing-function:cubic-bezier(.5,0,.6,1)}}@keyframes sb{{0%,{P(a0)}{{offset-distance:0%;opacity:0}}{P(a0 + .05)}{{offset-distance:0%;opacity:1}}{P(a0 + .55)},{P(COEUR[0] - .3)}{{offset-distance:100%;opacity:1}}{P(COEUR[0])},100%{{offset-distance:100%;opacity:0}}}}')
    c.append(f'.sr{{animation-name:sr;animation-timing-function:linear}}@keyframes sr{{0%,{P(a0)}{{transform:rotate(0)}}{P(a0 + .55)},100%{{transform:rotate(-240deg)}}}}')
    hop = '0%{transform:none}' + ''.join(f'{P(s - .35)}{{transform:none}}{P(s - .1)}{{transform:translateY(-34px)}}{P(s + .2)}{{transform:none}}' for s in SWAPS) + '100%{transform:none}'
    c.append(f'.hop{{animation-name:hop}}@keyframes hop{{{hop}}}')
    # signature on the card draws for every edition
    for i, (a, b) in enumerate(ED_WIN):
        c.append(f'.sg{i}{{animation-name:sg{i};animation-timing-function:ease-out}}@keyframes sg{i}{{0%,{P(a + .2)}{{stroke-dashoffset:1}}{P(a + 1.0)},100%{{stroke-dashoffset:0}}}}')
    # outro: the ball rolls from the grey card to SIGNÉ's
    c.append(f'.ob{{animation-name:ob;animation-timing-function:cubic-bezier(.5,0,.4,1)}}@keyframes ob{{0%,{P(OUTRO + 1.2)}{{offset-distance:0%;opacity:0}}{P(OUTRO + 1.3)}{{offset-distance:0%;opacity:1}}{P(OUTRO + 2.2)},100%{{offset-distance:100%;opacity:1}}}}')
    c.append(f'.or{{animation-name:or_;animation-timing-function:linear}}@keyframes or_{{0%,{P(OUTRO + 1.3)}{{transform:rotate(0)}}{P(OUTRO + 2.2)},100%{{transform:rotate(-300deg)}}}}')
    c.append(f'.ol{{animation-name:ol;animation-timing-function:cubic-bezier(.5,0,.4,1)}}@keyframes ol{{0%,{P(OUTRO + 1.3)}{{stroke-dashoffset:1}}{P(OUTRO + 2.2)},100%{{stroke-dashoffset:0}}}}')
    return '\n'.join(c)

BALL = ('<div class="sph"><div class="{r}" style="position:absolute;inset:0"><div style="position:absolute;left:9px;top:9px;width:26px;height:26px;border-radius:50%;border:1px solid rgba(250,228,200,.6)"></div>'
        '<div style="position:absolute;left:8px;top:24px;width:9px;height:9px;border-radius:50%;background:#FFF7EC;box-shadow:0 0 10px 3px rgba(255,240,215,.75)"></div></div></div>')

def signe_card_inner(i, name, line, no):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center"><span style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:17px;letter-spacing:.24em;color:#E3A77C" dir="ltr">{no} · LES LUMIÈRES</span>'
            f'<span style="font-family:\'Cormorant Garamond\',serif;font-size:24px;letter-spacing:.14em;color:#F3E6D2" dir="ltr">SIGNÉ°</span></div>'
            f'<div style="font-family:\'Cormorant Garamond\',serif;font-style:italic;font-size:66px;line-height:1.05;color:#FBF3E6;margin-top:14px" dir="ltr">{name}</div>'
            f'<div style="font-size:28px;color:#F1E4D2;margin-top:8px">{line}</div>'
            f'<div style="height:1px;background:rgba(255,236,214,.3);margin:18px 0 14px"></div>'
            f'<div style="font-size:22px;line-height:1.5;color:#D9C8B4">מתמלאת רק ברגע שהיא נבחרת.</div>'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-top:16px"><span style="font-size:22px;color:#E3A77C">חתום ביד</span>'
            f'<svg width="176" height="52" viewBox="0 0 176 52"><path class="sg{i}" pathLength="1" d="{SIGN_PATH}" style="fill:none;stroke:#E8C58F;stroke-width:3.2;stroke-linecap:round;stroke-dasharray:1 1"></path></svg></div>')

def grey_card(style=''):
    return (f'<div style="box-sizing:border-box;padding:24px 28px;border-radius:16px;background:#F3F2F0;border:1px solid #DAD7D2;box-shadow:0 18px 40px rgba(40,36,32,.12);{style}" dir="rtl">'
            '<span style="display:inline-block;padding:6px 16px;border-radius:999px;background:#2E2A27;color:#F4F2EF;font-size:20px">ככה משווים</span>'
            '<div style="font-size:44px;font-weight:600;color:#2E2A27;margin-top:12px">סופגנייה</div>'
            '<div style="font-size:24px;line-height:1.55;color:#6E6660">ריבת תות · אבקת סוכר<br>90 גר׳ · יחידה</div>'
            '<div style="height:1px;background:#D8D4CE;margin:14px 0 10px"></div>'
            '<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-size:22px;color:#6E6660">מחיר</span><strong style="font-size:40px;color:#2E2A27">₪12</strong></div></div>')

def html():
    eds = ''.join(f'<div data-show="{a:.2f},{b:.2f}" data-fade="0.12">{glass_card(signe_card_inner(i, *e))}</div>' for i, (e, (a, b)) in enumerate(zip(EDITIONS, ED_WIN)))
    tpl = (HERE / 'reel.tpl.html').read_text(encoding='utf-8')
    rep = dict(CSS=css(), EDITIONS=eds, GREY=grey_card(f'position:absolute;left:{CARD["x"]}px;top:{CARD["y"]}px;width:{CARD["w"] - 20}px'),
               GREY_SMALL=grey_card('width:100%'), HOOK_LINE=HOOK_LINE, SIG_LINE=SIG_LINE, SPIN_B=SPIN_B,
               COEUR0=COEUR[0], COEUR1=COEUR[1], BOITE0=BOITE[0], BOITE1=BOITE[1], OUTRO=OUTRO, BALL_H=BALL.format(r='hr'),
               BALL_S=BALL.format(r='sr'), BALL_O=BALL.format(r='or'), SIGN_PATH=SIGN_PATH,
               NOIR_SMALL=signe_card_inner(9, *EDITIONS[0]))
    for k, v in rep.items():
        tpl = tpl.replace('{{' + k + '}}', str(v))
    assert '{{' not in tpl, tpl[tpl.find('{{'):tpl.find('{{') + 40]
    (HERE / 'reel.html').write_text(tpl, encoding='utf-8')

if __name__ == '__main__':
    if '--html' not in sys.argv: build_videos()
    html()
    print('land', round(LAND, 2), 'swaps', [round(s, 2) for s in SWAPS], 'spin end', round(SPIN_END, 2), 'editions', [(round(a, 2), round(b, 2)) for a, b in ED_WIN])
