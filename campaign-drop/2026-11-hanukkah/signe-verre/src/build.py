"""Hanukkah 2026 · SIGNÉ° "רואים מה בפנים" — transparent sufganiyot (studio mode, 30s, 9:16).

    python3 -I build.py            (run from this folder) → reel.html
    node render.js reel.html 30 ../out/SIGNE-verre-9x16.mp4

Hook: everyone sells a sufganiya, nobody shows what is inside. On SIGNÉ's dark set a hollow glass sufganiya is filled through
the piping nozzle (Kling, one clip per edition); when it is full, the glass "sets" into the real Les Lumières sufganiya,
signature on top. Four editions, then the coffret, then the studio close.

Higgsfield: a/empty.webp = gpt_image_2_6 job 1fb35bee (from the Les Lumières Noir still); full glasses: noir cdc87ca6,
framboise cb089005, pistache ccdd8fc5, vanille 1a28733b; pours = Kling 3.0 pro 5s first+last frame (see README).
a/real-*.webp = the Les Lumières stills (campaign-drop/2026-11-signe-hanukkah/assets/sufg-*-v1.png) cropped to 9:16.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = 30.0
def P(t): return f'{max(0.0, min(D, t)) / D * 100:.3f}%'

EDS = [('noir', 'Le Noir', 'שוקולד 70% · עלי זהב', 'N°1'),
       ('framboise', 'La Framboise', 'פטל · קונפי בפנים', 'N°2'),
       ('pistache', 'La Pistache', 'פיסטוק סיציליאני', 'N°3'),
       ('vanille', 'La Vanille', 'וניל מדגסקר · סוכר שרוף', 'N°4')]
HOOK_END, PORTAL = 2.4, (2.35, 3.2)
E0, EDUR, POUR = 3.6, 5.3, 3.9        # edition k starts at E0 + k*EDUR; the (sped) pour lasts POUR
S = [E0 + k * EDUR for k in range(4)]
COFFRET = S[-1] + EDUR                # 24.8
OUTRO = 27.3

def css():
    c = []
    c.append(f'.hk{{animation-name:hk}}@keyframes hk{{0%,{P(PORTAL[1])}{{opacity:1}}{P(PORTAL[1] + .05)},100%{{opacity:0}}}}')
    c.append(f'.hl{{animation-name:hl;animation-timing-function:linear}}@keyframes hl{{0%{{stroke-dashoffset:.86}}{P(HOOK_END - .1)},100%{{stroke-dashoffset:0}}}}')
    c.append(f'.hb{{animation-name:hb;animation-timing-function:linear}}@keyframes hb{{0%{{offset-distance:14%;opacity:1}}{P(HOOK_END - .1)}{{offset-distance:100%;opacity:1;transform:scale(1)}}{P(PORTAL[0] + .25)}{{opacity:1;transform:scale(1.5)}}{P(PORTAL[0] + .45)},100%{{offset-distance:100%;opacity:0;transform:scale(1.5)}}}}')
    c.append(f'.hr{{animation-name:hr;animation-timing-function:linear}}@keyframes hr{{0%{{transform:rotate(0)}}{P(HOOK_END - .1)},100%{{transform:rotate(-560deg)}}}}')
    c.append(f'.portal{{animation-name:portal;animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes portal{{0%,{P(PORTAL[0])}{{clip-path:circle(0px at 540px 1700px)}}{P(PORTAL[1])},100%{{clip-path:circle(2300px at 540px 1700px)}}}}')
    for k, s in enumerate(S):
        a = s + POUR - .1
        # the glass sets: real sufganiya fades in over the full glass, with a light sweep
        c.append(f'.rl{k}{{animation-name:rl{k}}}@keyframes rl{k}{{0%,{P(a)}{{opacity:0;filter:brightness(1.6)}}{P(a + .55)}{{opacity:1;filter:brightness(1.15)}}{P(a + .9)},100%{{opacity:1;filter:none}}}}')
        c.append(f'.sw{k}{{animation-name:sw{k};animation-timing-function:ease-in-out}}@keyframes sw{k}{{0%,{P(a)}{{transform:translateX(-120%) skewX(-18deg);opacity:0}}{P(a + .05)}{{opacity:1}}{P(a + .7)},100%{{transform:translateX(160%) skewX(-18deg);opacity:0}}}}')
    return '\n'.join(c)

def html():
    eds = ''
    for k, (key, name, line, no) in enumerate(EDS):
        s = S[k]
        end = S[k + 1] + .05 if k < 3 else COFFRET + .5
        eds += (f'<div class="stack" data-show="{s:.2f},{end:.2f}" data-fade="0.12">'
                f'<video class="cover" src="a/pour-{key}.webm" data-vstart="{s:.2f}" muted playsinline preload="auto"></video>'
                f'<img class="cover rl{k}" src="a/real-{key}.webp" alt="SIGNÉ {name}">'
                f'<div class="stack" style="overflow:hidden;pointer-events:none"><div class="sw{k}" style="position:absolute;top:0;bottom:0;left:0;width:40%;background:linear-gradient(90deg,rgba(255,230,190,0),rgba(255,230,190,.28),rgba(255,230,190,0))"></div></div>'
                f'<div class="stack" style="background:linear-gradient(to top,rgba(14,11,8,.92) 0,rgba(14,11,8,0) 32%)"></div>'
                f'<div class="stack" data-show="{s + .3:.2f},{end - .2:.2f}" data-fade="0.2"><div style="position:absolute;top:1450px;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center">'
                f'<div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:20px;letter-spacing:.28em;color:#E3A77C" dir="ltr">{no} · LES LUMIÈRES</div>'
                f'<div style="font-family:\'Cormorant Garamond\',serif;font-style:italic;font-size:84px;line-height:1;color:#FBF3E6" dir="ltr">{name}</div>'
                f'<div style="font-size:36px;color:#F1E4D2" dir="rtl">{line}</div></div></div>'
                f'<div class="stack" data-show="{s + .3:.2f},{s + POUR - .2:.2f}" data-fade="0.2"><div style="position:absolute;top:250px;left:60px;right:60px;text-align:center;font-size:58px;font-weight:500;color:#F7EEDF" dir="rtl">מה בפנים?</div></div>'
                f'<div class="stack" data-show="{s + POUR + .3:.2f},{end - .2:.2f}" data-fade="0.2"><div style="position:absolute;top:250px;left:60px;right:60px;text-align:center;font-size:58px;font-weight:500;color:#E3A77C" dir="rtl">ועכשיו — חתום.</div></div>'
                f'</div>')
    tpl = (HERE / 'reel.tpl.html').read_text(encoding='utf-8')
    for k, v in dict(CSS=css(), EDS=eds, S0=S[0], COFFRET=COFFRET, OUTRO=OUTRO).items():
        tpl = tpl.replace('{{' + k + '}}', str(v))
    assert '{{' not in tpl, tpl[tpl.find('{{'):tpl.find('{{') + 40]
    (HERE / 'reel.html').write_text(tpl, encoding='utf-8')

if __name__ == '__main__':
    html()
    print('editions', [round(s, 2) for s in S], 'coffret', COFFRET, 'outro', OUTRO)
