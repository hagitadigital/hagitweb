# SOLUNA° (World 05) — world film. Hook: hidden logo over the pyramid opening in the cup.
# Signature scene: "כוס אחת, ארבע תחושות" — the four pyramids on a dial around one cup, then the lemon drop.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SK = '/home/user/hagitweb/.claude/skills/brandos-brand-world-reel/'
s = open(SK + 'assets/reel-template.html').read()
def p(t): return '%.3f%%' % (t / 30 * 100)
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

INK, BRASS, BG, SOFT = '#16222A', '#8C6A2E', '#EEF3F1', '#4A5A62'
HS = "font-family: 'Frank Ruhl Libre', serif"
H = "font-family: 'Heebo', sans-serif"
LAT = "font-family: 'Fraunces', serif"
K = f"{LAT}; font-style: italic; font-weight: 300; font-size: 44px; color: {BRASS}"
MONO = "font-family: 'Spline Sans Mono', monospace; letter-spacing: .2em; text-transform: uppercase"

s = s.replace('family=Cormorant+Garamond', 'family=Frank+Ruhl+Libre:wght@300;400;500&amp;family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;1,9..144,300&amp;family=Spline+Sans+Mono:wght@400&amp;family=Cormorant+Garamond')
rep("--w-bg:#F7F0E6;", f"--w-bg:{BG};"); rep("--w-ink:#3B2E33;", f"--w-ink:{INK};"); rep("--w-accent:#C9878E;", f"--w-accent:{BRASS};")
s = s.replace('<title>Brand World Reel</title>', '<title>SOLUNA world film</title>')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">05</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'חנות חליטות שבה כל מצב רוח צובע את המים בצבע אחר.')
rep('BRAND° · עולם מותג NN', 'SOLUNA° · עולם מותג 05')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'את <span dir="ltr">SOLUNA°</span> מזהים<br>גם בלי השם.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>יזהו גם בלי הלוגו?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 05')

# ---------- HOOK: opens on the wow (the blue pyramid colouring the water), logo hidden by the copper bar ----------
hook = f'''<div class="hook stack" style="background: #DCE6E6">
  <div class="stack" data-seq="f/calm_%03d.jpg" data-from="40" data-to="96" data-start="0" data-step="0.05" data-pos="50% 50%"></div>
  <div style="position: absolute; left: 0; right: 0; top: 0; height: 640px; background: linear-gradient(to bottom, rgba(238,243,241,.96) 42%, rgba(238,243,241,0))"></div>
  <div style="position: absolute; top: 88px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 36px; color: var(--s-dark)" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size: 17px; letter-spacing: .3em; color: #8B7B6E">חגית אנטבי</div>
  </div>
  <div style="position: absolute; top: 226px; left: 70px; right: 70px; text-align: right; font-size: 82px; font-weight: 600; line-height: 1.16; color: var(--s-dark)" dir="rtl">אם נסתיר את הלוגו,<br>עדיין <span style="color: var(--s-copper)">יזהו אותך</span>?</div>
  <div style="position: absolute; left: HBX; top: HBY; width: HBW; height: HBH; transform: rotate(HBRdeg)"><div class="hbar" style="position: absolute; inset: 0; background: var(--s-copper); border-radius: 8px; box-shadow: 0 10px 24px rgba(62,40,24,.3)"></div></div>
'''
hook = hook.replace('HBX', '530px').replace('HBY', '964px').replace('HBW', '330px').replace('HBH', '112px').replace('HBR', '9')
a, b = s.index('<div class="hook stack"'), s.index('  <svg class="stack" width="1080"')
s = s[:a] + hook + s[b:]
# the hook question is on screen at frame 0 (thumbnail); the bar slides at 0.9s
rep('@keyframes hbar{0%,3%{transform:scaleX(0)}4.6%,100%{transform:scaleX(1)}}', '@keyframes hbar{0%,2.6%{transform:scaleX(0)}4.2%,100%{transform:scaleX(1)}}')

# ---------- HUD ----------
tags = [('01 · The Core', 'בוחרים איך רוצים להרגיש'), ('02 · La Tasse', 'כוס אחת, ארבע תחושות'),
        ('03 · La Pyramide', 'סגורה על המדף, פתוחה במים'), ('04 · Hors de la boutique', 'השקית, בית הקפה, הכוס לדרך'),
        ('05 · The Promise', 'הצבע הוא המוצר')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>'); s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i); e = s.index('</span>', k); s = s[:k] + line + s[e:]
TB, TC, TD, TE = 9.8, 16.1, 19.4, 23.45     # scene starts (B, C, D, E)
for a_, b_ in [('data-show="9.9,14.7"', f'data-show="9.9,{TC}"'), ('data-show="14.7,18.7"', f'data-show="{TC},{TD}"'),
               ('data-show="18.7,22.7"', f'data-show="{TD},{TE}"'), ('data-show="22.7,30"', f'data-show="{TE},30"')]:
    rep(a_, b_)

# ---------- the dial ----------
# key, hebrew, latin, blend, strong colour, scene tint, last film frame
M = [('fresh', 'רעננות', 'Fraîcheur', 'נענע, למון גראס, ורבנה לימונית', '#6FB45E', '#DCEBCD', 94),
     ('clarity', 'חדות', 'Clarté', 'כורכום, ג׳ינג׳ר, קליפת תפוז', '#E79A1C', '#F7E4BC', 85),
     ('joy', 'שמחה', 'Joie', 'היביסקוס, עלי ורדים, קינמון', '#C7234E', '#F4D1D8', 94),
     ('calm', 'רוגע', 'Calme', 'אפונת הפרפר, לבנדר, לואיזה', '#2F4FCB', '#CFD9F4', 94)]
PURPLE, PURPLE_T = '#8A3CC0', '#E0D0F2'
STEPS = [10.7, 11.65, 12.6]          # the ring turns 90° clockwise at each
T_LEMON = 13.9                        # the drop falls; purple spreads until +0.8
GW, GH = 400, 708; GX, GY = 540 - GW // 2, 1100 - GH // 2; RR = 452
FS = GW / 720                         # film frame scale inside the niche
starts = [TB + .1] + [t + .35 for t in STEPS]          # when each mood's film starts in the niche
ends = [t + .55 for t in STEPS] + [TC + .5]

ring = '0%%,%s{transform:rotate(0deg)}' % p(STEPS[0]); cr = '0%%,%s{transform:rotate(0deg)}' % p(STEPS[0])
for k, t in enumerate(STEPS):
    nxt = p(STEPS[k + 1]) if k < 2 else '100%'
    ring += '%s,%s{transform:rotate(%ddeg)}' % (p(t + .5), nxt, 90 * (k + 1))
    cr += '%s,%s{transform:rotate(%ddeg)}' % (p(t + .5), nxt, -90 * (k + 1))
bg = '0%%,%s{background-color:%s}' % (p(STEPS[0] + .3), M[0][5])
for k, t in enumerate(STEPS):
    hold = STEPS[k + 1] + .3 if k < 2 else T_LEMON + .1
    bg += '%s,%s{background-color:%s}' % (p(t + .65), p(hold), M[k + 1][5])
bg += '%s,100%%{background-color:%s}' % (p(T_LEMON + .8), PURPLE_T)
tints = ''.join('.tint%d{animation-name:tint%d;animation-timing-function:cubic-bezier(.4,0,.3,1)}@keyframes tint%d{0%%,%s{clip-path:inset(100%% 0 0 0)}%s,100%%{clip-path:inset(0 0 0 0)}}'
                % (k, k, k, p(st + .3), p(st + .8)) for k, st in enumerate(starts))

css = f"""
.a-pan{{animation-name:apan;animation-timing-function:cubic-bezier(.45,0,.2,1)}}@keyframes apan{{0%,{p(5.2)}{{transform:translateX(-330px)}}{p(10.2)},100%{{transform:translateX(-663px)}}}}
.a-push{{animation-name:apush;transform-origin:47% 66%;animation-timing-function:cubic-bezier(.45,0,.2,1)}}@keyframes apush{{0%,{p(5.2)}{{transform:scale(1)}}{p(10.2)},100%{{transform:scale(1.14)}}}}
.c-l1{{animation-name:cl1}}@keyframes cl1{{0%,{p(6.0)}{{transform:translateY(110%)}}{p(6.6)},100%{{transform:none}}}}
.d-bg{{animation-name:dbg}}@keyframes dbg{{{bg}}}
.d-ring{{animation-name:dring;transform-origin:0 0}}@keyframes dring{{{ring}}}
.d-cr{{animation-name:dcr}}@keyframes dcr{{{cr}}}
{tints}
.d-l1{{animation-name:dl1}}@keyframes dl1{{0%,{p(TB + .1)}{{transform:translateY(110%)}}{p(TB + .6)},100%{{transform:none}}}}
.d-l2{{animation-name:dl2}}@keyframes dl2{{0%,{p(TB + .4)}{{transform:translateY(110%)}}{p(TB + .9)},100%{{transform:none}}}}
.drop{{animation-name:drop;animation-timing-function:cubic-bezier(.6,0,.9,.4)}}@keyframes drop{{0%,{p(T_LEMON - .45)}{{opacity:0;transform:translateY(-250px)}}{p(T_LEMON - .4)}{{opacity:1;transform:translateY(-250px)}}{p(T_LEMON)}{{opacity:1;transform:translateY(0)}}{p(T_LEMON + .12)},100%{{opacity:0;transform:translateY(14px) scale(1.6)}}}}
.lemon{{animation-name:lemon;animation-timing-function:cubic-bezier(.3,0,.3,1)}}@keyframes lemon{{0%,{p(T_LEMON)}{{clip-path:circle(0px at 50% 55%)}}{p(T_LEMON + .8)},100%{{clip-path:circle(520px at 50% 55%)}}}}
{''.join('.py-c%d{{animation-name:pyc%d}}@keyframes pyc%d{{0%,{a}{{opacity:1;transform:none}}{b},100%{{opacity:0;transform:scale(1.08)}}}}.py-o%d{{animation-name:pyo%d;animation-timing-function:cubic-bezier(.2,.9,.25,1.2)}}@keyframes pyo%d{{0%,{a}{{opacity:0;transform:scale(.8)}}{b},100%{{opacity:1;transform:none}}}}'.format(i, i, i, i, i, i, a=p(TC + .6 + i * .35), b=p(TC + 1.1 + i * .35)) for i in range(4))}
.p-l1{{animation-name:pl1}}@keyframes pl1{{0%,{p(TC)}{{transform:translateY(110%)}}{p(TC + .5)},100%{{transform:none}}}}
.p-l2{{animation-name:pl2}}@keyframes pl2{{0%,{p(TC + .3)}{{transform:translateY(110%)}}{p(TC + .8)},100%{{transform:none}}}}
.t-push{{animation-name:tpush;animation-timing-function:linear}}@keyframes tpush{{0%,{p(TD - .3)}{{transform:scale(1.09)}}{p(TE + .4)},100%{{transform:scale(1)}}}}
.t-l1{{animation-name:tl1}}@keyframes tl1{{0%,{p(TD)}{{transform:translateY(110%)}}{p(TD + .5)},100%{{transform:none}}}}
.t-l2{{animation-name:tl2}}@keyframes tl2{{0%,{p(TD + .3)}{{transform:translateY(110%)}}{p(TD + .8)},100%{{transform:none}}}}
.w-l1{{animation-name:wl1}}@keyframes wl1{{0%,{p(TE + .4)}{{transform:translateY(110%)}}{p(TE + 1.0)},100%{{transform:none}}}}
.w-l2{{animation-name:wl2}}@keyframes wl2{{0%,{p(TE + .8)}{{transform:translateY(110%)}}{p(TE + 1.4)},100%{{transform:none}}}}
"""
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · SOLUNA ── */' + css)

GB = lambda h, o=.96: f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: {h}px; background: linear-gradient(to top, rgba(238,243,241,{o}) 46%, rgba(238,243,241,0))"></div>'
GT = lambda h, o=.96: f'<div style="position: absolute; left: 0; right: 0; top: 0; height: {h}px; background: linear-gradient(to bottom, rgba(238,243,241,{o}) 52%, rgba(238,243,241,0))"></div>'

# A · the shop (the wall sign in the picture is the title)
A = f"""<section class="scene" data-show="0,{TB + .3}">
    <div class="stack a-push"><div class="a-pan" style="position: absolute; left: 0; top: 0; width: 2560px; height: 1920px"><img src="a/interior-4k.jpg" alt="" style="width: 100%; height: 100%; display: block"></div></div>
    {GB(600)}
    <div style="position: absolute; bottom: 150px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="c-l1" style="display: block; {HS}; font-size: 108px; font-weight: 300; line-height: 1.12; color: {INK}">איך את רוצה להרגיש?</span></span>
      <div data-in="7.2" style="margin-top: 14px; {H}; font-size: 36px; font-weight: 300; color: {SOFT}">ארבע פירמידות, ארבעה מצבי רוח.</div>
    </div>
  </section>"""

def niche_film(k):
    key, he, la, bl, col, tint, last = M[k]
    frm = last - 60
    return (f'<div class="stack" data-show="{starts[k] if k else 0:.2f},{ends[k]:.2f}" data-fade="0.2">'
            f'<div class="stack" data-seq="f/{key}_%03d.jpg" data-from="{frm}" data-to="{last}" data-by="3" data-start="{starts[k]:.2f}" data-step="0.042"></div>'
            f'<div class="tint{k}" style="position: absolute; left: {128 * FS:.0f}px; top: {656 * FS:.0f}px; width: {452 * FS:.0f}px; height: {424 * FS:.0f}px; border-radius: 4px 4px 60px 60px; background: {col}; mix-blend-mode: multiply; opacity: .42"></div></div>')
medals = ''.join(f"""<div style="position: absolute; left: 0; top: 0; transform: rotate({-90 * i}deg) translateY(-{RR}px) rotate({90 * i}deg)"><div class="d-cr" style="position: absolute; left: -78px; top: -78px; width: 156px; height: 156px; border-radius: 50%; background: #FFFFFF; box-shadow: 0 0 0 3px #FFFFFF, 0 0 0 5px {m[4]}, 0 14px 30px rgba(22,34,42,.18)"><img src="a/closed-{m[0]}.webp" alt="{m[2]}" style="position: absolute; left: 18px; top: 14px; width: 120px; height: 128px; object-fit: contain"></div></div>"""
                 for i, m in enumerate(M))
wins = [(TB + .2, STEPS[0] + .5)] + [(t + .5, (STEPS[k + 1] + .5) if k < 2 else T_LEMON + .3) for k, t in enumerate(STEPS)]
labels = ''.join(f"""<div class="stack" data-show="{a_:.2f},{b_:.2f}" data-fade="0.18" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="display: flex; align-items: baseline; gap: 22px; direction: rtl"><span style="{HS}; font-size: 76px; font-weight: 400; line-height: 1; color: {INK}">{m[1]}</span><span style="{LAT}; font-style: italic; font-weight: 300; font-size: 46px; color: {SOFT}" dir="ltr">{m[2]}</span></span><span style="{H}; font-size: 30px; font-weight: 300; color: {SOFT}" dir="rtl">{m[3]}</span></div>"""
                 for m, (a_, b_) in zip(M, wins))
labels += f"""<div class="stack" data-show="{T_LEMON + .5:.2f},{TC + .6:.2f}" data-fade="0.18" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{HS}; font-size: 70px; font-weight: 400; line-height: 1; color: {INK}" dir="rtl">טיפת לימון</span><span style="{H}; font-size: 32px; font-weight: 300; color: {SOFT}" dir="rtl">והכחול הופך לסגול.</span></div>"""
B = f"""<section class="scene" data-show="{TB},{TC + .3}">
    <div class="stack d-bg" style="background-color: {M[0][5]}"></div>
    <div style="position: absolute; top: 196px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="{TB}" style="{K}; margin-bottom: 6px" dir="ltr">La Tasse</div>
      <span class="mask"><span class="d-l1" style="display: block; {HS}; font-size: 76px; font-weight: 300; line-height: 1.14; color: {INK}">פירמידה אחת. כוס אחת.</span></span>
      <span class="mask"><span class="d-l2" style="display: block; {HS}; font-size: 76px; font-weight: 500; line-height: 1.14; color: {INK}">צבע אחד.</span></span>
    </div>
    <div style="position: absolute; left: {540 - RR}px; top: {1100 - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(140,106,46,.5); box-sizing: border-box"></div>
    <div style="position: absolute; left: {GX}px; top: {GY}px; width: {GW}px; height: {GH}px; border-radius: {GW // 2}px {GW // 2}px 28px 28px; overflow: hidden; background: #D9E2E2; box-shadow: 0 0 0 4px #FFFFFF, 0 0 0 6px rgba(140,106,46,.7), 0 30px 70px rgba(22,34,42,.2)">
      {niche_film(0)}{niche_film(1)}{niche_film(2)}{niche_film(3)}
      <div class="stack lemon"><img src="f/calm_094.jpg" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: hue-rotate(48deg) saturate(1.05)"><div style="position: absolute; left: {128 * FS:.0f}px; top: {656 * FS:.0f}px; width: {452 * FS:.0f}px; height: {424 * FS:.0f}px; border-radius: 4px 4px 60px 60px; background: {PURPLE}; mix-blend-mode: multiply; opacity: .42"></div></div>
      <div class="drop" style="position: absolute; left: {GW // 2 - 13}px; top: {648 * FS - 30:.0f}px; width: 26px; height: 32px; border-radius: 50% 50% 50% 50% / 62% 62% 40% 40%; background: radial-gradient(circle at 40% 35%, #FFF6C2, #F2D33A 70%); box-shadow: 0 0 14px rgba(242,211,58,.8)"></div>
    </div>
    <div class="d-ring" style="position: absolute; left: 540px; top: 1100px; width: 0; height: 0">{medals}</div>
    <div style="position: absolute; top: {1100 - RR - 78 - 44}px; left: 522px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {BRASS}"></div>
    <div style="position: absolute; top: 1690px; left: 40px; right: 40px; height: 130px">{labels}</div>
  </section>"""

# C · closed on the shelf, open in water
cards = ''
for i, m in enumerate(M):
    x = 560 if i % 2 == 0 else 70          # RTL: first card on the right
    y = 610 + (i // 2) * 590
    cards += f"""<div data-in="{TC + i * .12:.2f}" style="position: absolute; left: {x}px; top: {y}px; width: 450px; height: 560px; border-radius: 30px; background: rgba(255,255,255,.62); border: 1px solid rgba(255,255,255,.9); box-shadow: 0 30px 60px -36px rgba(22,34,42,.4)">
      <div style="position: absolute; left: 35px; top: 26px; width: 380px; height: 380px">
        <img class="py-c{i}" src="a/closed-{m[0]}.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain">
        <img class="py-o{i}" src="a/open-{m[0]}.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: contain">
      </div>
      <div style="position: absolute; left: 0; right: 0; top: 424px; display: flex; flex-direction: column; align-items: center; gap: 6px" dir="rtl"><span style="{HS}; font-size: 50px; line-height: 1; color: {INK}">{m[1]}</span><span style="{H}; font-size: 24px; font-weight: 300; color: {SOFT}">{m[3]}</span></div>
    </div>"""
C = f"""<section class="scene" data-show="{TC},{TD + .3}">
    <div class="stack" style="background: radial-gradient(90% 60% at 50% 45%, #FFFFFF, {BG} 75%)"></div>
    <div style="position: absolute; top: 196px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="{TC}" style="{K}; margin-bottom: 6px" dir="ltr">La Pyramide</div>
      <span class="mask"><span class="p-l1" style="display: block; {HS}; font-size: 82px; font-weight: 300; line-height: 1.14; color: {INK}">סגורה על המדף.</span></span>
      <span class="mask"><span class="p-l2" style="display: block; {HS}; font-size: 82px; font-weight: 500; line-height: 1.14; color: {INK}">פתוחה במים.</span></span>
    </div>
    {cards}
  </section>"""

# D · out of the shop: three full-bleed shots, ≥1.4s each
shots = [('sac', '42% 50%', 'Le Sac', 'השקית'), ('cafe', '56% 50%', 'Au Café', 'בבית הקפה'), ('emporter', '50% 50%', 'À Emporter', 'לקחת')]
DUR = (TE + .2 - TD) / 3
run = ''
for i, (f, pos, la, he) in enumerate(shots):
    a_, b_ = TD + i * DUR, TD + (i + 1) * DUR
    run += f"""<div class="stack" data-show="{0 if i == 0 else a_:.2f},{b_ if i < 2 else 30:.2f}" data-fade="0.42"><img class="cover" src="a/{f}-fix.png" alt="" style="object-position: {pos}">
      <div style="position: absolute; left: 0; right: 0; bottom: 150px; display: flex; justify-content: center"><span style="display: inline-flex; align-items: baseline; gap: 20px; padding: 16px 34px; border-radius: 999px; background: rgba(250,252,251,.9); border: 1px solid rgba(140,106,46,.6); direction: rtl"><span style="{HS}; font-size: 44px; color: {INK}">{he}</span><span style="{LAT}; font-style: italic; font-weight: 300; font-size: 34px; color: {SOFT}" dir="ltr">{la}</span></span></div></div>"""
D = f"""<section class="scene" data-show="{TD},{TE + .3}">
    <div class="stack t-push">{run}</div>
    {GT(640, .94)}
    <div style="position: absolute; top: 196px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="{TD}" style="{K}; margin-bottom: 6px" dir="ltr">Hors de la boutique</div>
      <span class="mask"><span class="t-l1" style="display: block; {HS}; font-size: 82px; font-weight: 300; line-height: 1.14; color: {INK}">יוצאים מהחנות.</span></span>
      <span class="mask"><span class="t-l2" style="display: block; {HS}; font-size: 82px; font-weight: 500; line-height: 1.14; color: {INK}">הצבע יוצא איתך.</span></span>
    </div>
  </section>"""

# E · the promise (stays in the studio window during the outro)
pots = ''.join(f"""<div data-in="{TE - .2 + i * .12:.2f}" style="width: 236px; height: 300px"><img src="a/pot-{m[0]}.webp" alt="" style="width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 16px 18px rgba(22,34,42,.2))"></div>""" for i, m in enumerate(M))
E = f"""<section class="scene" data-show="{TE},30">
    <div class="stack" style="background: radial-gradient(90% 60% at 50% 48%, #FFFFFF, {BG} 78%)"></div>
    <div data-in="{TE - .3}" style="position: absolute; top: 250px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 12px">
      <div style="{LAT}; font-weight: 300; font-size: 104px; letter-spacing: .3em; margin-right: -.3em; line-height: 1; color: {INK}" dir="ltr">SOLUNA<sup style="font-size: .42em; letter-spacing: 0; vertical-align: .9em">°</sup></div>
      <div style="{MONO}; font-size: 22px; color: {SOFT}" dir="ltr">Tisanes d'humeur</div>
    </div>
    <div style="position: absolute; top: 700px; left: 40px; right: 40px; display: flex; justify-content: space-between; align-items: flex-end" dir="ltr">{pots}</div>
    <div style="position: absolute; top: 1008px; left: 60px; right: 60px; height: 10px; border-radius: 3px; background: linear-gradient(180deg, #FFFFFF, rgba(200,220,215,.6)); box-shadow: 0 16px 22px -10px rgba(22,34,42,.35)"></div>
    <div style="position: absolute; top: 1150px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="w-l1" style="display: block; {HS}; font-size: 128px; font-weight: 300; line-height: 1.1; color: {INK}">הצבע הוא</span></span>
      <span class="mask"><span class="w-l2" style="display: block; {HS}; font-size: 128px; font-weight: 500; line-height: 1.1; color: {INK}">המוצר.</span></span>
      <div data-in="{TE + 1.6}" style="margin-top: 26px; {H}; font-size: 36px; font-weight: 300; line-height: 1.5; color: {SOFT}">ירוק לרעננות, זהב לחדות,<br>כחול לרוגע, אדום לשמחה.</div>
    </div>
  </section>"""

i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D, E]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
open(os.path.join(HERE, 'reel.html'), 'w').write(s)
print('ok', len(s))
