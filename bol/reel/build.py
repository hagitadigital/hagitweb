"""BOL° reel (World No.09) — studio mode, 30s, 1080x1920.
Hook: the site's bowl swap from frame 0 under "הלקוחה גוללת. מה יעצור אותה דווקא אצלך?"
Signature scene: Le Quart — four toppings on a clockwise ring drop into the next quarter of a turning bowl,
the background takes the fruit's colour on each stop, the price grows, and the bowl shrinks into the checkout card.
Run: python3 bol/reel/build.py  →  bol/reel/reel.html (assets load from ../assets/)
"""
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '..', '..', '.claude', 'skills', 'brandos-brand-world-reel') + '/'
s = open(SK + 'assets/reel-template.html').read()
A_ = '../assets/'
def p(t): return '%.3f%%' % (max(0, min(30, t)) / 30 * 100)
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

BG, INK, FRAMB = '#F7F5F0', '#1F1B3A', '#C8284F'
H = "font-family: 'Assistant', sans-serif"
FR = "font-family: 'Fraunces', serif"
K = f"{FR}; font-style: italic; font-weight: 300; font-size: 46px; color: {FRAMB}"

rep("family=Cormorant+Garamond", "family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;1,9..144,300;1,9..144,400&amp;family=Cormorant+Garamond")
rep("--w-bg:#F7F0E6;", f"--w-bg:{BG};"); rep("--w-ink:#3B2E33;", f"--w-ink:{INK};"); rep("--w-accent:#C9878E;", f"--w-accent:{FRAMB};")
s = s.replace('<title>Brand World Reel</title>', '<title>BOL° reel</title>')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">09</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'בר קערות יוגורט שבו הקערה נבנית מול העיניים. בול מה שבחרת.')
rep('BRAND° · עולם מותג NN', '<span dir="ltr">BOL°</span> · עולם מותג 09')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'עולם שרוצים להיכנס אליו,<br>ולהישאר.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ומה יעצור את הלקוחה<br>דווקא אצלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 09')

# ── HOOK: the bowl swap from frame 0 (no generic card) ──
i = s.index('  <!-- proof mechanic 1'); j = s.index('-->', s.index('<!-- proof mechanic 2')) + 3
SW = [0.0, 0.6, 1.5]          # swap moments; the last one lands back on Le Soleil and stops
HB = ['soleil', 'foret', 'soleil']
hk_css = ''
for k, b in enumerate(HB):
    tin = SW[k]; d = 0.6
    tout = SW[k + 1] if k + 1 < len(SW) else None
    kf = ''
    if k == 0: kf += '0%{opacity:1;transform:none}'
    else: kf += f'0%,{p(tin)}{{opacity:0;transform:translateX(-70%) rotate(-150deg) scale(.72)}}{p(tin + d)}{{opacity:1;transform:none}}'
    if tout is not None:
        kf += f'{p(tout)}{{opacity:1;transform:none}}{p(tout + .55)},100%{{opacity:0;transform:translateX(70%) rotate(150deg) scale(.72)}}'
    else:
        kf += f'{p(tin + d + .12)}{{transform:scale(1.04)}}{p(tin + d + .3)},100%{{opacity:1;transform:none}}'
    hk_css += f'.hk{k}{{animation-name:hk{k}}}@keyframes hk{k}{{{kf}}}'
spin = '.spin{animation-name:spin;animation-timing-function:linear}@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(130deg)}}'
hbowls = ''.join(f'<div class="hk{k}" style="position: absolute; inset: 0"><div class="spin" style="position: absolute; inset: 0"><img src="{A_}bowl-{b}.webp" alt="" style="width: 100%; height: 100%; display: block; filter: drop-shadow(0 34px 34px rgba(31,27,58,.18))"></div></div>' for k, b in enumerate(HB))
hook_names = [('Le Soleil', 0, .55), ('La Forêt', .85, 1.45), ('Le Soleil', 1.75, 30)]
hlabels = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.2" style="display: flex; justify-content: center; align-items: center"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 54px; color: {INK}" dir="ltr">{n}</span></div>' for n, a, b in hook_names)
s = s[:i] + f'''<div style="position: absolute; top: 600px; left: 160px; width: 760px; height: 760px">{hbowls}</div>
  <div style="position: absolute; top: 1385px; left: 0; right: 0; height: 80px">{hlabels}</div>''' + s[j:]
rep('<div class="hook stack" style="background: var(--s-cream)">', f'<div class="hook stack" style="background: {BG}">')
rep('>EDIT: למה תמיד<br>משווים אותך <span style="color: var(--s-copper)">במחיר</span>?</div>',
    '>הלקוחה גוללת.<br>מה יעצור אותה <span style="color: var(--s-copper)">דווקא אצלך</span>?</div>')

# ── HUD ──
tags = [('01 · The Core', 'בול מה שבחרת.'), ('02 · Le Quart', 'ארבעה רבעים. הקערה שלך.'),
        ('03 · La Glacerie', 'מבחוץ פרי. מבפנים <span dir="ltr">BOL°</span>.'), ('04 · Édition Hanoucca', 'שמונה לילות. שמונה מילויים.'),
        ('05 · The Promise', 'יוגורט לבן. כל השאר פרי.')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>'); s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i); e = s.index('</span>', k); s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,16.3"'), ('data-show="14.7,18.7"', 'data-show="16.3,19.7"'),
             ('data-show="18.7,22.7"', 'data-show="19.7,23.1"'), ('data-show="22.7,30"', 'data-show="23.1,30"')]:
    rep(a, b)

# ── Le Quart geometry (from bol/index.html) ──
R1, R2, GAP = 12.5, 41.4, 2.6
def pt(r, a):
    t = math.radians(a); return 50 + r * math.cos(t), 50 + r * math.sin(t)
def sector(sl):
    c = -90 - sl * 90; a0, a1 = c - 45 + GAP, c + 45 - GAP          # slots laid counter-clockwise; the bowl turns clockwise
    x0, y0 = pt(R2, a0); x1, y1 = pt(R2, a1); x2, y2 = pt(R1, a1); x3, y3 = pt(R1, a0)
    return f'M{x0:.2f} {y0:.2f} A{R2} {R2} 0 0 1 {x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f} A{R1} {R1} 0 0 0 {x3:.2f} {y3:.2f} Z'
TOP = [('mangue', 'Mangue', 'מנגו טרי בקוביות', 6, '#FBE6C0'), ('myrtille', 'Myrtilles', 'אוכמניות', 7, '#DADFF1'),
       ('granola', 'Granola', 'גרנולה בדבש ושקדים', 5, '#EFE0CC'), ('kiwi', 'Kiwi', 'קיווי פרוס', 5, '#E2EBCB')]
T0, STEP = 10.35, 0.95
ST = [T0 + k * STEP for k in range(4)]            # step k: turn (k>0) ST..ST+.45, drop ST+.45..ST+.85
CARD = 14.3
BW, BX, BY, RR = 600, 240, 800, 430            # bowl box; ring centre = (540, 1100)
qbg = f'0%,{p(ST[0] + .5)}{{background-color:{BG}}}'
for k, t in enumerate(ST):
    qbg += f'{p(t + .75)},{p(ST[k + 1] + .5) if k < 3 else p(CARD)}{{background-color:{TOP[k][4]}}}'
qbg += f'{p(CARD + .5)},100%{{background-color:{BG}}}'
turn = '0%,' + p(ST[1]) + '{transform:rotate(0deg)}'
for k in range(1, 4):
    nxt = p(ST[k + 1]) if k < 3 else '100%'
    turn += f'{p(ST[k] + .45)},{nxt}{{transform:rotate({90 * k}deg)}}'
ring = turn.replace('', '')
q_css = ''
for k, t in enumerate(ST):
    d0 = t + (.45 if k else 0)
    q_css += (f'.qd{k}{{animation-name:qd{k}}}@keyframes qd{k}{{0%,{p(d0)}{{transform:none;opacity:1}}{p(d0 + .38)},100%{{transform:translateY({RR - 90}px) scale(.35);opacity:0}}}}'
              f'.ql{k}{{animation-name:ql{k};transform-box:view-box;transform-origin:50px 50px}}@keyframes ql{k}{{0%,{p(d0 + .22)}{{opacity:0;transform:translate(0,-6px) scale(1.18)}}{p(d0 + .62)},100%{{opacity:1;transform:none}}}}')
q_css += f'''.qbg{{animation-name:qbg}}@keyframes qbg{{{qbg}}}
.qturn{{animation-name:qturn}}@keyframes qturn{{{turn}}}
.qring{{animation-name:qring}}@keyframes qring{{{ring}}}
.qringf{{animation-name:qringf}}@keyframes qringf{{0%,{p(CARD - .3)}{{opacity:1}}{p(CARD)},100%{{opacity:0}}}}
.qshrink{{animation-name:qshrink;transform-origin:50% 50%}}@keyframes qshrink{{0%,{p(CARD)}{{transform:none}}{p(CARD + .6)},100%{{transform:translateY(250px) scale(.6)}}}}
.qcard{{animation-name:qcard}}@keyframes qcard{{0%,{p(CARD + .05)}{{opacity:0;transform:scale(.7)}}{p(CARD + .6)},100%{{opacity:1;transform:none}}}}
.qok{{animation-name:qok}}@keyframes qok{{0%,{p(CARD + .6)}{{stroke-dashoffset:30}}{p(CARD + 1.1)},100%{{stroke-dashoffset:0}}}}
.ql1a{{animation-name:ql1a}}@keyframes ql1a{{0%,{p(9.9)}{{transform:translateY(110%)}}{p(10.4)},100%{{transform:none}}}}
.ql2a{{animation-name:ql2a}}@keyframes ql2a{{0%,{p(10.2)}{{transform:translateY(110%)}}{p(10.7)},100%{{transform:none}}}}
'''

core_css = f'''.core-ttl{{animation-name:corettl}}@keyframes corettl{{0%,{p(5.6)}{{opacity:0;letter-spacing:.3em}}{p(6.6)},100%{{opacity:1;letter-spacing:.04em}}}}
.c-l1{{animation-name:cl1}}@keyframes cl1{{0%,{p(6.0)}{{transform:translateY(110%)}}{p(6.6)},100%{{transform:none}}}}
.c-l2{{animation-name:cl2}}@keyframes cl2{{0%,{p(6.4)}{{transform:translateY(110%)}}{p(7.0)},100%{{transform:none}}}}
.cs0{{animation-name:cs0}}@keyframes cs0{{0%,{p(7.7)}{{opacity:1;transform:none}}{p(8.65)},100%{{opacity:0;transform:translateX(70%) rotate(150deg) scale(.72)}}}}
.cs1{{animation-name:cs1}}@keyframes cs1{{0%,{p(7.7)}{{opacity:0;transform:translateX(-70%) rotate(-150deg) scale(.72)}}{p(8.65)},100%{{opacity:1;transform:none}}}}
'''
gl_css = ''
for k, (t, o) in enumerate([(17.15, 16.3), (18.9, 18.15)]):
    gl_css += (f'.gw{k}{{animation-name:gw{k}}}@keyframes gw{k}{{0%,{p(t)}{{opacity:1;transform:none}}{p(t + .45)},100%{{opacity:0;transform:scale(.97)}}}}'
               f'.gc{k}{{animation-name:gc{k}}}@keyframes gc{k}{{0%,{p(t + .05)}{{opacity:0;transform:scale(1.05)}}{p(t + .55)},100%{{opacity:1;transform:none}}}}'
               f'.gs{k}{{animation-name:gs{k}}}@keyframes gs{k}{{0%,{p(t - .3)}{{height:0;opacity:0}}{p(t - .29)}{{height:0;opacity:.9}}{p(t + .05)}{{height:900px;opacity:.9}}{p(t + .3)},100%{{height:900px;opacity:0}}}}')
gl_css += f'''.g-l1{{animation-name:gl1}}@keyframes gl1{{0%,{p(16.4)}{{transform:translateY(110%)}}{p(16.9)},100%{{transform:none}}}}
.g-l2{{animation-name:gl2}}@keyframes gl2{{0%,{p(16.7)}{{transform:translateY(110%)}}{p(17.2)},100%{{transform:none}}}}
'''
SF = ['foret', 'framboise', 'fraise', 'cerise', 'myrtille', 'peche', 'mangue', 'kiwi']
HT = [19.95 + i * .32 for i in range(8)]
h_css = ''.join(f'.hd{i}{{animation-name:hd{i}}}@keyframes hd{i}{{0%,{p(t)}{{opacity:0;transform:translateY(-60px) scale(1.15)}}{p(t + .35)},100%{{opacity:1;transform:none}}}}'
                f'.hf{i}{{animation-name:hf{i}}}@keyframes hf{i}{{0%,{p(t + .1)}{{background-color:rgba(31,27,58,.12);box-shadow:none}}{p(t + .35)},100%{{background-color:#F4A21C;box-shadow:0 0 16px 5px rgba(244,162,28,.5)}}}}' for i, t in enumerate(HT))
h_css += f'''.h-l1{{animation-name:hl1}}@keyframes hl1{{0%,{p(19.7)}{{transform:translateY(110%)}}{p(20.2)},100%{{transform:none}}}}
.h-l2{{animation-name:hl2}}@keyframes hl2{{0%,{p(20.0)}{{transform:translateY(110%)}}{p(20.5)},100%{{transform:none}}}}
'''
e_css = f'''.w-push{{animation-name:wpush}}@keyframes wpush{{0%,{p(23.0)}{{transform:scale(1.12)}}100%{{transform:none}}}}
.w-l1{{animation-name:wl1}}@keyframes wl1{{0%,{p(23.5)}{{transform:translateY(110%)}}{p(24.1)},100%{{transform:none}}}}
.w-l2{{animation-name:wl2}}@keyframes wl2{{0%,{p(23.9)}{{transform:translateY(110%)}}{p(24.5)},100%{{transform:none}}}}
'''
# frame 0 already shows the question
rep('@keyframes hq{0%,.5%{opacity:0;transform:translateY(24px)}2.5%,100%{opacity:1;transform:none}}', '@keyframes hq{0%,100%{opacity:1;transform:none}}')
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */",
    '/* ── WORLD scenes · BOL° ── */' + hk_css + spin + core_css + q_css + gl_css + h_css + e_css)

GT = f'<div style="position: absolute; left: 0; right: 0; top: 0; height: 420px; background: linear-gradient(to bottom, {BG} 40%, rgba(247,245,240,0))"></div>'
bowl = lambda b, cls='', extra='': f'<div class="{cls}" style="position: absolute; inset: 0{extra}"><div class="spin" style="position: absolute; inset: 0"><img src="{A_}bowl-{b}.webp" alt="" style="width: 100%; height: 100%; display: block; filter: drop-shadow(0 34px 34px rgba(31,27,58,.18))"></div></div>'

A = f"""<section class="scene" data-show="0,10.2">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 190px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 12px">
      <div class="core-ttl" style="{FR}; font-size: 150px; font-weight: 600; line-height: 1; color: {INK}" dir="ltr">BOL<span style="color: {FRAMB}">°</span></div>
      <div data-in="6.3" style="{H}; font-size: 24px; font-weight: 600; letter-spacing: .34em; color: rgba(31,27,58,.55)" dir="ltr">BAR À YAOURT · TEL AVIV</div>
    </div>
    <div style="position: absolute; top: 500px; left: 180px; width: 720px; height: 720px">{bowl('soleil', 'cs0')}{bowl('foret', 'cs1')}</div>
    <div style="position: absolute; top: 1250px; left: 0; right: 0; height: 80px">
      <div class="stack" data-show="0,8.1" data-fade="0.25" style="display: flex; justify-content: center; gap: 22px; align-items: baseline"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 52px; color: {INK}" dir="ltr">Le Soleil</span><span style="{FR}; font-size: 40px; font-weight: 600; color: {FRAMB}" dir="ltr">₪38</span></div>
      <div class="stack" data-show="8.4,30" data-fade="0.25" style="display: flex; justify-content: center; gap: 22px; align-items: baseline"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 52px; color: {INK}" dir="ltr">La Forêt</span><span style="{FR}; font-size: 40px; font-weight: 600; color: {FRAMB}" dir="ltr">₪36</span></div>
    </div>
    <div style="position: absolute; top: 1400px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="c-l1" style="display: block; {H}; font-size: 112px; font-weight: 200; line-height: 1.1; color: {INK}">בול</span></span>
      <span class="mask"><span class="c-l2" style="display: block; {H}; font-size: 112px; font-weight: 600; line-height: 1.1; color: {INK}">מה שבחרת.</span></span>
      <div data-in="7.2" style="margin-top: 16px; {H}; font-size: 34px; font-weight: 300; color: rgba(31,27,58,.66)">יוגורט יווני סמיך, פרי שנחתך הבוקר.</div>
    </div>
  </section>"""

NS_DEFS = '''<defs><filter id="soft" x="-15%" y="-15%" width="130%" height="130%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency=".14" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".6"/></filter>
<filter id="pile" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy=".5" stdDeviation=".6" flood-color="#1F1B3A" flood-opacity=".22"/></filter>
<radialGradient id="rimShade" cx="50%" cy="50%" r="50%"><stop offset="78%" stop-color="#1F1B3A" stop-opacity="0"/><stop offset="100%" stop-color="#1F1B3A" stop-opacity=".16"/></radialGradient>''' + \
    ''.join(f'<mask id="m{k}"><path d="{sector(k)}" fill="#fff" filter="url(#soft)"/></mask>' for k in range(4)) + '</defs>'
quarters = ''.join(f'<g class="ql{k}"><g filter="url(#pile)"><g mask="url(#m{k})"><image href="{A_}t-{t[0]}.webp" x="4" y="4" width="92" height="92" preserveAspectRatio="xMidYMid slice" transform="rotate({-k * 90 + 15} 50 50)"/></g></g></g>' for k, t in enumerate(TOP))
medals = ''.join(f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-90 * k}deg) translateY(-{RR}px)"><div class="qd{k}" style="position: absolute; left: -82px; top: -82px; width: 164px; height: 164px"><div style="width: 100%; height: 100%; border-radius: 50%; background: url({A_}t-{t[0]}.webp) center/cover; transform: rotate({90 * k}deg); box-shadow: 0 0 0 5px #FFFFFF, 0 16px 34px rgba(31,27,58,.22)"></div></div></div>' for k, t in enumerate(TOP))
totals = [24]
for t in TOP: totals.append(totals[-1] + t[3])
qlabels = f'<div class="stack" data-show="9.7,{ST[0] + .5:.2f}" data-fade="0.15" style="display: flex; flex-direction: column; align-items: center; gap: 4px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 58px; color: {INK}" dir="ltr">Yaourt grec</span><span style="{H}; font-size: 32px; color: rgba(31,27,58,.66)" dir="rtl">קערה ריקה · <b style="color: {FRAMB}">₪24</b></span></div>'
for k, t in enumerate(TOP):
    a = ST[k] + .5 + (.45 if k else 0); b = (ST[k + 1] + .95) if k < 3 else CARD
    qlabels += f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.15" style="display: flex; flex-direction: column; align-items: center; gap: 4px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 58px; color: {INK}" dir="ltr">+ {t[1]}</span><span style="{H}; font-size: 32px; color: rgba(31,27,58,.66)" dir="rtl">{t[2]} · <b style="color: {FRAMB}">₪{totals[k + 1]}</b></span></div>'
B = f"""<section class="scene" data-show="9.7,16.5">
    <div class="stack qbg" style="background-color: {BG}"></div>
    <div style="position: absolute; top: 190px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="9.8" style="{K}; margin-bottom: 6px" dir="ltr">L'Atelier</div>
      <span class="mask"><span class="ql1a" style="display: block; {H}; font-size: 80px; font-weight: 200; line-height: 1.12; color: {INK}">ארבעה רבעים.</span></span>
      <span class="mask"><span class="ql2a" style="display: block; {H}; font-size: 80px; font-weight: 600; line-height: 1.12; color: {INK}">הקערה שלך.</span></span>
    </div>
    <div class="qringf" style="position: absolute; inset: 0">
      <div style="position: absolute; left: {540 - RR}px; top: {1100 - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(31,27,58,.22); box-sizing: border-box"></div>
      <div style="position: absolute; top: {1100 - RR - 82 - 44}px; left: 522px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {FRAMB}"></div>
    </div>
    <div class="qcard" style="position: absolute; left: 230px; top: 640px; width: 620px; height: 860px; border-radius: 40px; background: {INK}; box-shadow: 0 40px 90px -30px rgba(31,27,58,.6); overflow: hidden">
      <div style="position: absolute; top: 56px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px; color: {BG}">
        <div style="{FR}; font-size: 22px; letter-spacing: .3em; opacity: .6" dir="ltr">À PAYER</div>
        <div style="{FR}; font-size: 104px; font-weight: 300; line-height: 1" dir="ltr">₪{totals[-1]}</div>
        <div style="width: 74px; height: 74px; border-radius: 50%; border: 2px solid rgba(247,245,240,.5); display: flex; align-items: center; justify-content: center; margin-top: 8px"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="{BG}" stroke-width="2.2"><path class="qok" d="M5 12.5l4.5 4.5L19 7.5" style="stroke-dasharray: 30"/></svg></div>
        <div style="{FR}; font-style: italic; font-size: 34px; opacity: .85; margin-top: 8px" dir="ltr">Mangue · Myrtilles · Granola · Kiwi</div>
      </div>
    </div>
    <div class="qshrink" style="position: absolute; inset: 0">
      <div class="qturn" style="position: absolute; left: {BX}px; top: {BY}px; width: {BW}px; height: {BW}px">
        <img src="{A_}bowl-nu.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; filter: drop-shadow(0 34px 34px rgba(31,27,58,.18))">
        <svg viewBox="0 0 100 100" style="position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible">{NS_DEFS}{quarters}<circle cx="50" cy="50" r="42.4" fill="url(#rimShade)"/></svg>
      </div>
      <div class="qring" style="position: absolute; left: 540px; top: 1100px; width: 0; height: 0">{medals}</div>
    </div>
    <div class="qringf" style="position: absolute; top: 1640px; left: 40px; right: 40px; height: 140px">{qlabels}</div>
  </section>"""

fruit = lambda f, k: f'''<div class="gw{k}" style="position: absolute; inset: 0"><img src="{A_}gl-{f}-whole.webp" alt="" style="width: 100%; height: 100%; filter: drop-shadow(0 30px 30px rgba(31,27,58,.16))"></div>
      <div class="gc{k}" style="position: absolute; inset: 0"><img src="{A_}gl-{f}-cut.webp" alt="" style="width: 100%; height: 100%; filter: drop-shadow(0 30px 30px rgba(31,27,58,.16))"></div>
      <div class="gs{k}" style="position: absolute; left: 50%; top: -40px; width: 3px; background: {INK}"></div>'''
C = f"""<section class="scene" data-show="16.3,19.9">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 190px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="16.3" style="{K}; margin-bottom: 6px" dir="ltr">La Glacerie</div>
      <span class="mask"><span class="g-l1" style="display: block; {H}; font-size: 80px; font-weight: 200; line-height: 1.12; color: {INK}">מבחוץ פרי.</span></span>
      <span class="mask"><span class="g-l2" style="display: block; {H}; font-size: 80px; font-weight: 600; line-height: 1.12; color: {INK}">מבפנים <span dir="ltr">BOL°</span>.</span></span>
    </div>
    <div class="stack" data-show="16.3,18.25" data-fade="0.3"><div style="position: absolute; top: 560px; left: 130px; width: 820px; height: 820px">{fruit('mangue', 0)}</div></div>
    <div class="stack" data-show="18.05,30" data-fade="0.3"><div style="position: absolute; top: 560px; left: 130px; width: 820px; height: 820px">{fruit('myrtille', 1)}</div></div>
    <div style="position: absolute; top: 1450px; left: 40px; right: 40px; height: 140px">
      <div class="stack" data-show="16.3,18.2" data-fade="0.2" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 60px; color: {INK}" dir="ltr">La Mangue</span><span style="{H}; font-size: 32px; color: rgba(31,27,58,.66)" dir="rtl">קליפת מנגו קפואה, ובפנים יוגורט לבן</span></div>
      <div class="stack" data-show="18.2,30" data-fade="0.2" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 60px; color: {INK}" dir="ltr">La Myrtille</span><span style="{H}; font-size: 32px; color: rgba(31,27,58,.66)" dir="rtl">קליפת אוכמניות קפואה, ובפנים ריבה ויוגורט</span></div>
    </div>
  </section>"""

NIGHTS = ['א׳', 'ב׳', 'ג׳', 'ד׳', 'ה׳', 'ו׳', 'ז׳', 'ח׳']
cells = ''.join(f'<div style="position: relative; width: 206px; height: 206px; border-radius: 18px; background: #FFFFFF; box-shadow: inset 0 0 0 1px rgba(31,27,58,.06), inset 0 8px 18px rgba(31,27,58,.07)"><span style="position: absolute; left: 0; right: 0; bottom: 10px; text-align: center; {H}; font-size: 18px; letter-spacing: .1em; color: rgba(31,27,58,.35)" dir="rtl">לילה {NIGHTS[i]}</span><img class="hd{i}" src="{A_}sfg-{f}-s.webp" alt="" style="position: absolute; left: 14px; top: 10px; width: 178px; height: 178px; filter: drop-shadow(0 8px 8px rgba(31,27,58,.2))"></div>' for i, f in enumerate(SF))
flames = ''.join(f'<i class="hf{i}" style="display: block; width: 16px; height: 26px; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%"></i>' for i in range(8))
D = f"""<section class="scene" data-show="19.5,23.4">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 190px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="19.5" style="{H}; font-size: 24px; font-weight: 600; letter-spacing: .3em; color: {FRAMB}; margin-bottom: 14px" dir="ltr">ÉDITION LIMITÉE · HANOUCCA</div>
      <span class="mask"><span class="h-l1" style="display: block; {H}; font-size: 80px; font-weight: 200; line-height: 1.12; color: {INK}">שמונה לילות.</span></span>
      <span class="mask"><span class="h-l2" style="display: block; {H}; font-size: 80px; font-weight: 600; line-height: 1.12; color: {INK}">שמונה מילויים.</span></span>
    </div>
    <div style="position: absolute; top: 640px; left: 0; right: 0; display: flex; justify-content: center; gap: 34px" dir="ltr">{flames}</div>
    <div style="position: absolute; top: 720px; left: 50px; width: 980px; box-sizing: border-box; padding: 26px; border-radius: 28px; background: #F1EEE7; box-shadow: inset 0 3px 14px rgba(31,27,58,.08)">
      <div style="display: grid; grid-template-columns: repeat(4, 206px); justify-content: space-between; row-gap: 22px" dir="ltr">{cells}</div>
    </div>
    <div data-in="21.6" style="position: absolute; top: 1290px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 6px">
      <div style="{FR}; font-style: italic; font-weight: 300; font-size: 58px; color: {INK}" dir="ltr">La Boîte des Huit Nuits</div>
      <div style="{H}; font-size: 32px; color: rgba(31,27,58,.66)" dir="rtl">סופגניות יוגורט קפואות · <b style="color: {FRAMB}">₪99</b> לקופסה</div>
    </div>
  </section>"""

E = f"""<section class="scene" data-show="23.1,30">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 470px; left: 190px; width: 700px; height: 700px"><div class="w-push" style="position: absolute; inset: 0">{bowl('miel')}</div></div>
    <div data-in="23.2" style="position: absolute; top: 190px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px">
      <div style="{FR}; font-size: 120px; font-weight: 600; line-height: 1; color: {INK}" dir="ltr">BOL<span style="color: {FRAMB}">°</span></div>
      <div style="{H}; font-size: 22px; font-weight: 600; letter-spacing: .34em; color: rgba(31,27,58,.55)" dir="ltr">NOTRE YAOURT</div>
    </div>
    <div style="position: absolute; top: 1260px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="w-l1" style="display: block; {H}; font-size: 96px; font-weight: 200; line-height: 1.12; color: {INK}">יוגורט לבן.</span></span>
      <span class="mask"><span class="w-l2" style="display: block; {H}; font-size: 96px; font-weight: 600; line-height: 1.12; color: {INK}">כל השאר פרי.</span></span>
      <div data-in="24.9" style="margin-top: 18px; {FR}; font-style: italic; font-weight: 300; font-size: 42px; color: {FRAMB}" dir="ltr">Le blanc d'abord. La couleur, c'est vous.</div>
    </div>
  </section>"""

i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D, E]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
open(os.path.join(HERE, 'reel.html'), 'w').write(s)
print('ok', len(s))
