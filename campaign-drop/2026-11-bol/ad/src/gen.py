"""BOL° brand ad (brand mode: the brand speaks to its own customers; no studio window, no HUD).
Hook A: "מה יש לך בקערה היום?" over a bowl that is already half full at frame 0 and keeps filling quarter by quarter.
Builds two cuts from one plan:  python3 gen.py  →  ad-30.html, ad-15.html  (assets in ./assets)
"""
import os, re, math
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '..', '..', '..', '..', '.claude', 'skills', 'brandos-brand-world-reel') + '/'
TPL = open(SK + 'assets/reel-template.html').read()
A_ = 'assets/'
BG, INK, FRAMB = '#F7F5F0', '#1F1B3A', '#C8284F'
H = "font-family: 'Assistant', sans-serif"
FR = "font-family: 'Fraunces', serif"
K = f"{FR}; font-style: italic; font-weight: 300; font-size: 46px; color: {FRAMB}"
TOP = [('mangue', 'Mangue', 'מנגו טרי בקוביות', 6, '#FBE6C0'), ('myrtille', 'Myrtilles', 'אוכמניות', 7, '#DADFF1'),
       ('granola', 'Granola', 'גרנולה בדבש ושקדים', 5, '#EFE0CC'), ('kiwi', 'Kiwi', 'קיווי פרוס', 5, '#E2EBCB')]
R1, R2, GAP = 12.5, 41.4, 2.6

def build(D, plan):
    css = []
    def p(t): return '%.3f%%' % (max(0, min(D, t)) / D * 100)
    def kf(name, body, extra=''):
        css.append(f'.{name}{{animation-name:{name}{extra}}}@keyframes {name}{{{body}}}')
    def mask_up(name, a, b):
        kf(name, f'0%,{p(a)}{{transform:translateY(110%)}}{p(b)},100%{{transform:none}}')
    def pt(r, a):
        t = math.radians(a); return 50 + r * math.cos(t), 50 + r * math.sin(t)
    def sector(sl):
        c = -90 - sl * 90; a0, a1 = c - 45 + GAP, c + 45 - GAP
        x0, y0 = pt(R2, a0); x1, y1 = pt(R2, a1); x2, y2 = pt(R1, a1); x3, y3 = pt(R1, a0)
        return f'M{x0:.2f} {y0:.2f} A{R2} {R2} 0 0 1 {x1:.2f} {y1:.2f} L{x2:.2f} {y2:.2f} A{R1} {R1} 0 0 0 {x3:.2f} {y3:.2f} Z'
    def quarter_bowl(px, lands, turns, size):
        """A bowl that turns clockwise; quarter k lands at lands[k] (None = there from frame 0).
        turns = [(t0, t1, deg)] held between moves."""
        tb = f'0%,{p(turns[0][0])}{{transform:rotate({turns[0][2] if turns[0][0] <= 0 else 0}deg)}}' if turns and turns[0][0] > 0 else ''
        body = ''
        prev = 0
        for i, (a, b, deg) in enumerate(turns):
            if a <= 0:
                body += f'0%,{p(turns[i + 1][0]) if i + 1 < len(turns) else "100%"}{{transform:rotate({deg}deg)}}'
            else:
                if not body: body += f'0%,{p(a)}{{transform:rotate({prev}deg)}}'
                nxt = p(turns[i + 1][0]) if i + 1 < len(turns) else '100%'
                body += f'{p(b)},{nxt}{{transform:rotate({deg}deg)}}'
            prev = deg
        kf(px + 'turn', body)
        defs = f'<defs><filter id="{px}soft" x="-15%" y="-15%" width="130%" height="130%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency=".14" numOctaves="2" seed="7" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G" result="d"/><feGaussianBlur in="d" stdDeviation=".6"/></filter>' \
               f'<filter id="{px}pile" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy=".5" stdDeviation=".6" flood-color="#1F1B3A" flood-opacity=".22"/></filter>' \
               f'<radialGradient id="{px}rim" cx="50%" cy="50%" r="50%"><stop offset="78%" stop-color="#1F1B3A" stop-opacity="0"/><stop offset="100%" stop-color="#1F1B3A" stop-opacity=".16"/></radialGradient>' + \
               ''.join(f'<mask id="{px}m{k}"><path d="{sector(k)}" fill="#fff" filter="url(#{px}soft)"/></mask>' for k in range(4)) + '</defs>'
        qs = ''
        for k, t in enumerate(TOP):
            cls = ''
            if lands[k] is not None:
                cls = f'{px}q{k}'
                kf(cls, f'0%,{p(lands[k])}{{opacity:0;transform:translate(0,-6px) scale(1.18)}}{p(lands[k] + .4)},100%{{opacity:1;transform:none}}', ';transform-box:view-box;transform-origin:50px 50px')
            qs += f'<g class="{cls}"><g filter="url(#{px}pile)"><g mask="url(#{px}m{k})"><image href="{A_}t-{t[0]}.webp" x="4" y="4" width="92" height="92" preserveAspectRatio="xMidYMid slice" transform="rotate({-k * 90 + 15} 50 50)"/></g></g></g>'
        return f'''<div class="{px}turn" style="position: absolute; inset: 0">
          <img src="{A_}bowl-nu.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; filter: drop-shadow(0 34px 34px rgba(31,27,58,.18))">
          <svg viewBox="0 0 100 100" style="position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible">{defs}{qs}<circle cx="50" cy="50" r="42.4" fill="url(#{px}rim)"/></svg></div>'''
    def bowl(b, cls=''):
        return f'<div class="{cls}" style="position: absolute; inset: 0"><div class="spin" style="position: absolute; inset: 0"><img src="{A_}bowl-{b}.webp" alt="" style="width: 100%; height: 100%; display: block; filter: drop-shadow(0 34px 34px rgba(31,27,58,.18))"></div></div>'
    kf('spin', f'0%{{transform:rotate(0)}}100%{{transform:rotate({D * 4.3:.0f}deg)}}', ';animation-timing-function:linear')
    lines = lambda px, l1, l2, top=190, size=80, tag='': f'''<div style="position: absolute; top: {top}px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">{tag}
      <span class="mask"><span class="{px}1" style="display: block; {H}; font-size: {size}px; font-weight: 200; line-height: 1.12; color: {INK}">{l1}</span></span>
      <span class="mask"><span class="{px}2" style="display: block; {H}; font-size: {size}px; font-weight: 600; line-height: 1.12; color: {INK}">{l2}</span></span></div>'''
    scenes = []

    # ── HOOK (frame 0: question + a half-full bowl; granola and kiwi land) ──
    h0, h1 = plan['hook']
    hl = [None, None, .85, 1.75]
    turns = [(0, 0, 90), (.35, .75, 180), (1.25, 1.65, 270)]
    hdrop = ''
    for k, t in [(2, .85), (3, 1.75)]:
        kf(f'hm{k}', f'0%,{p(t - .45)}{{opacity:0;transform:translateY(-120px) scale(.8)}}{p(t - .3)}{{opacity:1;transform:translateY(-60px) scale(1)}}{p(t + .1)}{{opacity:1;transform:translateY(170px) scale(.55)}}{p(t + .25)},100%{{opacity:0;transform:translateY(190px) scale(.4)}}')
        hdrop += f'<div class="hm{k}" style="position: absolute; left: 458px; top: 520px; width: 164px; height: 164px; border-radius: 50%; background: url({A_}t-{TOP[k][0]}.webp) center/cover; box-shadow: 0 0 0 5px #FFFFFF, 0 16px 34px rgba(31,27,58,.22)"></div>'
    scenes.append(f'''<section class="scene" data-show="0,{h1}">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 200px; left: 70px; right: 70px; text-align: center; {H}; font-size: 104px; font-weight: 600; line-height: 1.1; color: {INK}" dir="rtl">מה יש לך<br><span style="font-weight: 200">בקערה </span><span style="color: {FRAMB}">היום?</span></div>
    <div style="position: absolute; top: 660px; left: 170px; width: 740px; height: 740px">{quarter_bowl('h', hl, turns, 740)}</div>
    {hdrop}
    <div style="position: absolute; top: 1520px; left: 0; right: 0; text-align: center; {FR}; font-style: italic; font-weight: 300; font-size: 50px; color: rgba(31,27,58,.7)" dir="ltr">Mangue · Myrtilles · Granola · Kiwi</div>
  </section>''')

    # ── LOGO (the ° is a tiny bowl that turns) ──
    l0, l1 = plan['logo']
    kf('lg', f'0%,{p(l0 + .05)}{{opacity:0;letter-spacing:.3em}}{p(l0 + .7)},100%{{opacity:1;letter-spacing:.02em}}')
    kf('lgd', f'0%,{p(l0 + .3)}{{opacity:0;transform:scale(.2) rotate(-200deg)}}{p(l0 + .9)},100%{{opacity:1;transform:none}}')
    logo_html = lambda size, cls='', dcls='': f'''<div style="display: flex; align-items: flex-start; justify-content: center" dir="ltr"><span class="{cls}" style="{FR}; font-size: {size}px; font-weight: 600; line-height: 1; color: {INK}">BOL</span><span class="{dcls}" style="display: block; width: {int(size * .42)}px; height: {int(size * .42)}px; margin-left: {int(size * .06)}px; margin-top: {int(size * .02)}px"><span class="spin" style="display: block; width: 100%; height: 100%"><img src="{A_}bowl-soleil.webp" alt="" style="width: 100%; height: 100%; display: block"></span></span></div>'''
    scenes.append(f'''<section class="scene" data-show="{l0},{l1}" data-fade="0.25">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 760px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 26px">
      {logo_html(230, 'lg', 'lgd')}
      <div data-in="{l0 + .6}" style="{H}; font-size: 30px; font-weight: 600; letter-spacing: .34em; color: rgba(31,27,58,.55)" dir="ltr">BAR À YAOURT · TEL AVIV</div>
    </div>
  </section>''')

    # ── LA CARTE (30s only): the four bowls turn in one after another ──
    if 'carte' in plan:
        c0, c1, swaps = plan['carte']
        names = [('soleil', 'Le Soleil', 'מנגו, פסיפלורה, קוקוס ודבש', 38), ('foret', 'La Forêt', 'אוכמניות, פטל וגרנולה', 36),
                 ('jardin', 'Le Jardin', 'קיווי, ענבים, פיסטוק ודבש', 37), ('miel', 'Le Miel', 'יוגורט, דבש ושקדים', 29)]
        bw = ''
        for k, (b, n, d, pr) in enumerate(names):
            tin = swaps[k - 1] if k else None; tout = swaps[k] if k < 3 else None
            body = '0%' + (f',{p(tin)}{{opacity:0;transform:translateX(-70%) rotate(-150deg) scale(.72)}}{p(tin + .7)}{{opacity:1;transform:none}}' if tin else '{opacity:1;transform:none}')
            body += (f'{p(tout)}{{opacity:1;transform:none}}{p(tout + .7)},100%{{opacity:0;transform:translateX(70%) rotate(150deg) scale(.72)}}' if tout else ',100%{opacity:1;transform:none}' if not tin else '100%{opacity:1;transform:none}')
            kf(f'cb{k}', body)
            bw += bowl(b, f'cb{k}')
        labels = ''
        for k, (b, n, d, pr) in enumerate(names):
            a = c0 if k == 0 else swaps[k - 1] + .35; e = swaps[k] + .35 if k < 3 else c1
            labels += f'<div class="stack" data-show="{a:.2f},{e:.2f}" data-fade="0.25" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><div style="display: flex; gap: 22px; align-items: baseline"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 64px; color: {INK}" dir="ltr">{n}</span><span style="{FR}; font-size: 46px; font-weight: 600; color: {FRAMB}" dir="ltr">₪{pr}</span></div><span style="{H}; font-size: 34px; color: rgba(31,27,58,.66)" dir="rtl">{d}</span></div>'
        mask_up('ca1', c0 + .1, c0 + .6); mask_up('ca2', c0 + .4, c0 + .9)
        scenes.append(f'''<section class="scene" data-show="{c0},{c1}">
    <div class="stack" style="background: {BG}"></div>
    {lines('ca', 'ארבע קערות.', 'אחת מהן שלך.', tag=f'<div data-in="{c0}" style="{K}; margin-bottom: 6px" dir="ltr">La Carte</div>')}
    <div style="position: absolute; top: 560px; left: 170px; width: 740px; height: 740px">{bw}</div>
    <div style="position: absolute; top: 1380px; left: 40px; right: 40px; height: 160px">{labels}</div>
  </section>''')

    # ── LE QUART: toppings on a clockwise ring, the bowl fills, then the order card ──
    q0, q1, T0, STEP = plan['quart']
    ST = [T0 + k * STEP for k in range(4)]; CARD = ST[3] + .95
    RR = 430
    bgk = f'0%,{p(ST[0] + .5)}{{background-color:{BG}}}'
    for k, t in enumerate(ST):
        bgk += f'{p(t + .75)},{p(ST[k + 1] + .5) if k < 3 else p(CARD)}{{background-color:{TOP[k][4]}}}'
    bgk += f'{p(CARD + .5)},100%{{background-color:{BG}}}'
    kf('qbg', bgk)
    turns = [(0, 0, 0)] + [(ST[k], ST[k] + .45, 90 * k) for k in range(1, 4)]
    ring = '0%,' + p(ST[1]) + '{transform:rotate(0deg)}' + ''.join(f'{p(ST[k] + .45)},{p(ST[k + 1]) if k < 3 else "100%"}{{transform:rotate({90 * k}deg)}}' for k in range(1, 4))
    kf('qring', ring)
    medals = ''
    for k, t in enumerate(ST):
        d0 = t + (.45 if k else 0)
        kf(f'qd{k}', f'0%,{p(d0)}{{transform:none;opacity:1}}{p(d0 + .38)},100%{{transform:translateY({RR - 90}px) scale(.35);opacity:0}}')
        medals += f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-90 * k}deg) translateY(-{RR}px)"><div class="qd{k}" style="position: absolute; left: -82px; top: -82px; width: 164px; height: 164px"><div style="width: 100%; height: 100%; border-radius: 50%; background: url({A_}t-{TOP[k][0]}.webp) center/cover; transform: rotate({90 * k}deg); box-shadow: 0 0 0 5px #FFFFFF, 0 16px 34px rgba(31,27,58,.22)"></div></div></div>'
    lands = [t + (.45 if k else 0) + .22 for k, t in enumerate(ST)]
    kf('qringf', f'0%,{p(CARD - .3)}{{opacity:1}}{p(CARD)},100%{{opacity:0}}')
    kf('qshrink', f'0%,{p(CARD)}{{transform:none}}{p(CARD + .6)},100%{{transform:translateY(250px) scale(.6)}}', ';transform-origin:50% 50%')
    kf('qcard', f'0%,{p(CARD + .05)}{{opacity:0;transform:scale(.7)}}{p(CARD + .6)},100%{{opacity:1;transform:none}}')
    kf('qok', f'0%,{p(CARD + .6)}{{stroke-dashoffset:30}}{p(CARD + 1.1)},100%{{stroke-dashoffset:0}}')
    mask_up('qa1', q0 + .2, q0 + .7); mask_up('qa2', q0 + .5, q0 + 1.0)
    totals = [24]
    for t in TOP: totals.append(totals[-1] + t[3])
    ql = f'<div class="stack" data-show="{q0},{ST[0] + .5:.2f}" data-fade="0.15" style="display: flex; flex-direction: column; align-items: center; gap: 4px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 60px; color: {INK}" dir="ltr">Yaourt grec</span><span style="{H}; font-size: 34px; color: rgba(31,27,58,.66)" dir="rtl">מתחילים מקערה לבנה · <b style="color: {FRAMB}">₪24</b></span></div>'
    for k, t in enumerate(TOP):
        a = ST[k] + .5 + (.45 if k else 0); b = (ST[k + 1] + .95) if k < 3 else CARD
        ql += f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.15" style="display: flex; flex-direction: column; align-items: center; gap: 4px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 60px; color: {INK}" dir="ltr">+ {t[1]}</span><span style="{H}; font-size: 34px; color: rgba(31,27,58,.66)" dir="rtl">{t[2]} · <b style="color: {FRAMB}">₪{totals[k + 1]}</b></span></div>'
    scenes.append(f'''<section class="scene" data-show="{q0},{q1}">
    <div class="stack qbg" style="background-color: {BG}"></div>
    {lines('qa', 'ארבעה רבעים.', 'הקערה שלך.', tag=f'<div data-in="{q0}" style="{K}; margin-bottom: 6px" dir="ltr">L\'Atelier</div>')}
    <div class="qringf" style="position: absolute; inset: 0">
      <div style="position: absolute; left: {540 - RR}px; top: {1100 - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(31,27,58,.22); box-sizing: border-box"></div>
      <div style="position: absolute; top: {1100 - RR - 82 - 44}px; left: 522px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {FRAMB}"></div>
    </div>
    <div class="qcard" style="position: absolute; left: 230px; top: 640px; width: 620px; height: 860px; border-radius: 40px; background: {INK}; box-shadow: 0 40px 90px -30px rgba(31,27,58,.6); overflow: hidden">
      <div style="position: absolute; top: 56px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px; color: {BG}">
        <div style="{FR}; font-size: 22px; letter-spacing: .3em; opacity: .6" dir="ltr">À PAYER</div>
        <div style="{FR}; font-size: 104px; font-weight: 300; line-height: 1" dir="ltr">₪{totals[-1]}</div>
        <div style="width: 74px; height: 74px; border-radius: 50%; border: 2px solid rgba(247,245,240,.5); display: flex; align-items: center; justify-content: center; margin-top: 8px"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="{BG}" stroke-width="2.2"><path class="qok" d="M5 12.5l4.5 4.5L19 7.5" style="stroke-dasharray: 30"/></svg></div>
        <div style="{H}; font-size: 34px; font-weight: 300; margin-top: 6px" dir="rtl">הקערה שלך מוכנה בעוד 7 דקות</div>
      </div>
    </div>
    <div class="qshrink" style="position: absolute; inset: 0">
      <div style="position: absolute; left: 240px; top: 800px; width: 600px; height: 600px">{quarter_bowl('q', lands, turns, 600)}</div>
      <div class="qring" style="position: absolute; left: 540px; top: 1100px; width: 0; height: 0">{medals}</div>
    </div>
    <div class="qringf" style="position: absolute; top: 1640px; left: 40px; right: 40px; height: 140px">{ql}</div>
  </section>''')

    # ── LA GLACERIE ──
    if 'glacerie' in plan:
        g0, g1, cuts = plan['glacerie']
        fr = [('mangue', 'La Mangue', 'קליפת מנגו קפואה, ובפנים יוגורט לבן'), ('myrtille', 'La Myrtille', 'קליפת אוכמניות קפואה, ובפנים ריבה ויוגורט')][:len(cuts)]
        blocks, labs = '', ''
        for k, ((f, n, d), t) in enumerate(zip(fr, cuts)):
            kf(f'gw{k}', f'0%,{p(t)}{{opacity:1;transform:none}}{p(t + .45)},100%{{opacity:0;transform:scale(.97)}}')
            kf(f'gc{k}', f'0%,{p(t + .05)}{{opacity:0;transform:scale(1.05)}}{p(t + .55)},100%{{opacity:1;transform:none}}')
            kf(f'gs{k}', f'0%,{p(t - .3)}{{height:0;opacity:0}}{p(t - .29)}{{height:0;opacity:.9}}{p(t + .05)}{{height:900px;opacity:.9}}{p(t + .3)},100%{{height:900px;opacity:0}}')
            a = g0 if k == 0 else cuts[k - 1] + 1.3; e = (cuts[k] + 1.0) if k + 1 < len(cuts) else D
            blocks += f'''<div class="stack" data-show="{a:.2f},{e:.2f}" data-fade="0.3"><div style="position: absolute; top: 560px; left: 130px; width: 820px; height: 820px">
        <div class="gw{k}" style="position: absolute; inset: 0"><img src="{A_}gl-{f}-whole.webp" alt="" style="width: 100%; height: 100%; filter: drop-shadow(0 30px 30px rgba(31,27,58,.16))"></div>
        <div class="gc{k}" style="position: absolute; inset: 0"><img src="{A_}gl-{f}-cut.webp" alt="" style="width: 100%; height: 100%; filter: drop-shadow(0 30px 30px rgba(31,27,58,.16))"></div>
        <div class="gs{k}" style="position: absolute; left: 50%; top: -40px; width: 3px; background: {INK}"></div></div></div>'''
            labs += f'<div class="stack" data-show="{a:.2f},{e:.2f}" data-fade="0.2" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{FR}; font-style: italic; font-weight: 300; font-size: 62px; color: {INK}" dir="ltr">{n}</span><span style="{H}; font-size: 34px; color: rgba(31,27,58,.66)" dir="rtl">{d}</span></div>'
        mask_up('ga1', g0 + .1, g0 + .6); mask_up('ga2', g0 + .4, g0 + .9)
        scenes.append(f'''<section class="scene" data-show="{g0},{g1}">
    <div class="stack" style="background: {BG}"></div>
    {lines('ga', 'מבחוץ פרי.', 'מבפנים <span dir="ltr">BOL°</span>.', tag=f'<div data-in="{g0}" style="{K}; margin-bottom: 6px" dir="ltr">La Glacerie</div>')}
    {blocks}
    <div style="position: absolute; top: 1450px; left: 40px; right: 40px; height: 140px">{labs}</div>
  </section>''')

    # ── ÉDITION HANOUCCA ──
    if 'hanoucca' in plan:
        n0, n1, first = plan['hanoucca']
        SF = ['foret', 'framboise', 'fraise', 'cerise', 'myrtille', 'peche', 'mangue', 'kiwi']
        NIGHTS = ['א׳', 'ב׳', 'ג׳', 'ד׳', 'ה׳', 'ו׳', 'ז׳', 'ח׳']
        cells, flames = '', ''
        for i, f in enumerate(SF):
            t = first + i * .32
            kf(f'hd{i}', f'0%,{p(t)}{{opacity:0;transform:translateY(-60px) scale(1.15)}}{p(t + .35)},100%{{opacity:1;transform:none}}')
            kf(f'hf{i}', f'0%,{p(t + .1)}{{background-color:rgba(31,27,58,.12);box-shadow:none}}{p(t + .35)},100%{{background-color:#F4A21C;box-shadow:0 0 16px 5px rgba(244,162,28,.5)}}')
            cells += f'<div style="position: relative; width: 206px; height: 206px; border-radius: 18px; background: #FFFFFF; box-shadow: inset 0 0 0 1px rgba(31,27,58,.06), inset 0 8px 18px rgba(31,27,58,.07)"><span style="position: absolute; left: 0; right: 0; bottom: 10px; text-align: center; {H}; font-size: 18px; letter-spacing: .1em; color: rgba(31,27,58,.35)" dir="rtl">לילה {NIGHTS[i]}</span><img class="hd{i}" src="{A_}sfg-{f}-s.webp" alt="" style="position: absolute; left: 14px; top: 10px; width: 178px; height: 178px; filter: drop-shadow(0 8px 8px rgba(31,27,58,.2))"></div>'
            flames += f'<i class="hf{i}" style="display: block; width: 16px; height: 26px; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%"></i>'
        mask_up('na1', n0 + .2, n0 + .7); mask_up('na2', n0 + .5, n0 + 1.0)
        scenes.append(f'''<section class="scene" data-show="{n0},{n1}">
    <div class="stack" style="background: {BG}"></div>
    {lines('na', 'שמונה לילות.', 'שמונה מילויים.', tag=f'<div data-in="{n0}" style="{H}; font-size: 24px; font-weight: 600; letter-spacing: .3em; color: {FRAMB}; margin-bottom: 14px" dir="ltr">ÉDITION LIMITÉE · HANOUCCA</div>')}
    <div style="position: absolute; top: 640px; left: 0; right: 0; display: flex; justify-content: center; gap: 34px" dir="ltr">{flames}</div>
    <div style="position: absolute; top: 720px; left: 50px; width: 980px; box-sizing: border-box; padding: 26px; border-radius: 28px; background: #F1EEE7; box-shadow: inset 0 3px 14px rgba(31,27,58,.08)">
      <div style="display: grid; grid-template-columns: repeat(4, 206px); justify-content: space-between; row-gap: 22px" dir="ltr">{cells}</div>
    </div>
    <div data-in="{first + 1.7}" style="position: absolute; top: 1290px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 6px">
      <div style="{FR}; font-style: italic; font-weight: 300; font-size: 60px; color: {INK}" dir="ltr">La Boîte des Huit Nuits</div>
      <div style="{H}; font-size: 34px; color: rgba(31,27,58,.66)" dir="rtl">סופגניות יוגורט קפואות · <b style="color: {FRAMB}">₪99</b> לקופסה · רק עד סוף החג</div>
    </div>
  </section>''')

    # ── PROMISE ──
    if 'promise' in plan:
        w0, w1 = plan['promise']
        kf('wpush', f'0%,{p(w0)}{{transform:scale(1.12)}}100%{{transform:none}}')
        mask_up('wa1', w0 + .3, w0 + .9); mask_up('wa2', w0 + .7, w0 + 1.3)
        scenes.append(f'''<section class="scene" data-show="{w0},{w1}">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 380px; left: 190px; width: 700px; height: 700px"><div class="wpush" style="position: absolute; inset: 0">{bowl('miel')}</div></div>
    <div style="position: absolute; top: 1200px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="wa1" style="display: block; {H}; font-size: 100px; font-weight: 200; line-height: 1.12; color: {INK}">יוגורט לבן.</span></span>
      <span class="mask"><span class="wa2" style="display: block; {H}; font-size: 100px; font-weight: 600; line-height: 1.12; color: {INK}">כל השאר פרי.</span></span>
      <div data-in="{w0 + 1.2}" style="margin-top: 18px; {H}; font-size: 36px; font-weight: 300; color: rgba(31,27,58,.66)">מסוננים כל לילה. פרי שנחתך הבוקר.</div>
    </div>
  </section>''')

    # ── LOGO + CTA (holds to the last frame) ──
    e0 = plan['cta']
    kf('ctl', f'0%,{p(e0 + .1)}{{opacity:0;transform:translateY(30px)}}{p(e0 + .7)},100%{{opacity:1;transform:none}}')
    scenes.append(f'''<section class="scene" data-show="{e0},{D}">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 330px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 22px">
      {logo_html(210)}
      <div style="{H}; font-size: 28px; font-weight: 600; letter-spacing: .34em; color: rgba(31,27,58,.55)" dir="ltr">BAR À YAOURT · TEL AVIV</div>
    </div>
    <div class="ctl" style="position: absolute; top: 760px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 46px" dir="rtl">
      <div style="{H}; font-size: 116px; line-height: 1.08; color: {INK}"><span style="font-weight: 200">בול</span><br><b style="font-weight: 600">מה שבחרת.</b></div>
      <div style="display: flex; flex-direction: column; align-items: center; gap: 22px">
        <div style="padding: 30px 74px; border-radius: 999px; background: {FRAMB}; color: #FFFFFF; {H}; font-size: 46px; font-weight: 600">להרכיב קערה</div>
        <div style="{H}; font-size: 34px; font-weight: 300; color: rgba(31,27,58,.7)">או להזמין מראש ולאסוף בלי תור</div>
      </div>
    </div>
    <div style="position: absolute; bottom: 150px; left: 0; right: 0; text-align: center; {FR}; font-style: italic; font-weight: 300; font-size: 40px; color: {FRAMB}" dir="ltr">Le blanc d'abord. La couleur, c'est vous.</div>
  </section>''')

    # ── assemble: template's film CSS + reel.js, nothing of the studio wrapper ──
    head = TPL.split('<style>')[0].replace("family=Cormorant+Garamond", "family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;1,9..144,300;1,9..144,400&amp;family=Cormorant+Garamond").replace('<title>Brand World Reel</title>', f'<title>BOL° ad {D}s</title>')
    base = f'''<style>
html,body{{margin:0;background:{BG}}}
body{{font-family:'Assistant',sans-serif;color:{INK}}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{BG}}}
.film *{{animation-duration:{D}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
.mask{{overflow:hidden;display:block}}
.scene{{position:absolute;inset:0;overflow:hidden}}
''' + '\n'.join(css) + '\n</style>\n</head>'
    script = '<script>' + TPL.split('<script>')[1]
    script = script.replace('<body data-duration="30">', '')
    html = head + base + f'\n<body data-duration="{D}">\n<div id="stage"><div class="film stack">\n  ' + '\n  '.join(scenes) + '\n</div></div>\n' + script
    return html

PLANS = {
    30: dict(hook=(0, 2.6), logo=(2.5, 4.1), carte=(4.0, 9.2, [5.3, 6.6, 7.9]), quart=(9.1, 16.1, 9.6, .95),
             glacerie=(16.0, 20.1, [17.0, 18.9]), hanoucca=(19.9, 24.1, 20.4), promise=(23.9, 27.2), cta=27.0),
    15: dict(hook=(0, 2.6), logo=(2.5, 3.9), quart=(3.8, 10.6, 4.3, .9), glacerie=(10.4, 12.7, [11.3]), cta=12.5),
}
for D, plan in PLANS.items():
    html = build(D, plan)
    open(os.path.join(HERE, f'ad-{D}.html'), 'w').write(html)
    print('ok', D, len(html))
