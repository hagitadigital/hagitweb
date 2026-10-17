import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '../../../../.claude/skills/brandos-brand-world-reel') + '/'
R = '../../../../'   # repo root, relative to this page
s = open(SK + 'assets/reel-template.html').read()
def p(t): return '%.3f%%' % (t / 30 * 100)
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

INK, MATCHA, BG = '#1F2A1F', '#4C6B33', '#F4E7D5'
H = "font-family: 'Heebo', sans-serif"
K = f"font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 44px; color: {MATCHA}"

rep("--w-bg:#F7F0E6;", f"--w-bg:{BG};"); rep("--w-ink:#3B2E33;", f"--w-ink:{INK};"); rep("--w-accent:#C9878E;", f"--w-accent:{MATCHA};")
s = s.replace('<title>Brand World Reel</title>', '<title>CHASEN reel</title>')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">22</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'בר מאצ\'ה שבו הכוס לא קיימת עד שהיא שלך.')
rep('BRAND° · עולם מותג NN', 'CHASEN° · עולם מותג 22')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'כשהלקוחה מכינה,<br>היא נשארת.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ומה הלקוחות שלך<br>עושות באתר שלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 22')

# hook (Tuesday, canvas frame 0): the question + the glass and its three steps on her copper line — no price card
i = s.index('  <!-- proof mechanic 1'); j = s.index('<svg class="stack"', i)
PROOF = f"""  <div style="position: absolute; top: 600px; left: 270px; width: 540px; height: 820px; box-sizing: border-box; padding: 20px">
    <div style="position: absolute; inset: 20px; border-radius: 20px; overflow: hidden; background: #F2E7D8; box-shadow: 0 24px 60px rgba(20,30,45,.14)"><img src="{R}chasen/img/glass_classic.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 60%"></div>
    <div style="position: absolute; top: 0; right: 0; width: 48px; height: 48px; border-top: 4px solid var(--s-copper); border-right: 4px solid var(--s-copper)"></div>
    <div style="position: absolute; top: 0; left: 0; width: 48px; height: 48px; border-top: 4px solid var(--s-copper); border-left: 4px solid var(--s-copper)"></div>
    <div style="position: absolute; bottom: 0; right: 0; width: 48px; height: 48px; border-bottom: 4px solid var(--s-copper); border-right: 4px solid var(--s-copper)"></div>
    <div style="position: absolute; bottom: 0; left: 0; width: 48px; height: 48px; border-bottom: 4px solid var(--s-copper); border-left: 4px solid var(--s-copper)"></div>
  </div>
  <div style="position: absolute; top: 1470px; left: 60px; right: 60px; height: 90px" dir="rtl">
    <div style="position: absolute; left: 60px; right: 60px; top: 43px; height: 4px; border-radius: 2px; background: var(--s-copper)"></div>
    <div style="position: relative; display: flex; justify-content: space-between">
      <span style="padding: 16px 30px; border-radius: 999px; border: 3px solid var(--s-copper); background: var(--s-cream); font-size: 32px; font-weight: 600; color: var(--s-ink)">1 · טעם</span>
      <span style="padding: 16px 30px; border-radius: 999px; border: 3px solid var(--s-copper); background: var(--s-cream); font-size: 32px; font-weight: 600; color: var(--s-ink)">2 · קצפת ושוקולד</span>
      <span style="padding: 16px 30px; border-radius: 999px; border: 3px solid var(--s-copper); background: var(--s-bg); font-size: 32px; font-weight: 600; color: var(--s-ink)">3 · שם משלה</span>
    </div>
  </div>
"""
s = s[:i] + PROOF + s[j:]
rep('<div class="hq" style="position: absolute; top: 250px;', '<div style="position: absolute; top: 240px;')
rep('>EDIT: למה תמיד<br>\nמשווים אותך <span style="color: var(--s-copper)">במחיר</span>?</div>'.replace('\\n',''), '>X</div>') if False else None
s = re.sub(r'>EDIT: למה תמיד<br>.*?</div>', '>המוצר מצוין.<br>למה הן לא <span style="color: var(--s-copper)">נשארות</span><br>באתר?</div>', s, count=1, flags=re.S)
rep('M1140 1690 H540', 'M1140 1640 H540'); rep("path('M1140 1690 H540')", "path('M1140 1640 H540')")

# studio colours from the Brand Worlds Studio design system (cream, cream-deep, ink, copper, copper-text)
rep('--s-bg:#FAF8F3; --s-cream:#EEE6D8; --s-ink:#6B563F; --s-copper:#C4765A; --s-gold:#B8894A; --s-dark:#3E2F25;',
    '--s-bg:#F2EBDC; --s-cream:#E7DEC9; --s-ink:#15202E; --s-copper:#C28A5A; --s-gold:#C28A5A; --s-dark:#15202E; --s-ctext:#825630; --s-isoft:#3D4A5C;')
for a, b in [('letter-spacing: .32em; text-transform: uppercase; color: var(--s-copper)', 'letter-spacing: .32em; text-transform: uppercase; color: var(--s-ctext)'),
             ('font-size: 28px; font-weight: 500; letter-spacing: .06em; color: var(--s-copper)', 'font-size: 28px; font-weight: 500; letter-spacing: .06em; color: var(--s-ctext)'),
             ('font-size: 46px; font-weight: 500; line-height: 1.3; color: var(--s-copper)', 'font-size: 46px; font-weight: 500; line-height: 1.3; color: var(--s-ctext)'),
             ('font-size: 18px; font-weight: 500; letter-spacing: .04em; color: var(--s-copper)', 'font-size: 18px; font-weight: 500; letter-spacing: .04em; color: var(--s-ctext)'),
             ('color: #8B7355" dir="ltr">HAGITANTEBI', 'color: var(--s-isoft)" dir="ltr">HAGITANTEBI'),
             ('color: #8B7B6E">חגית אנטבי', 'color: var(--s-isoft)">חגית אנטבי'),
             ('stroke:#C4814F', 'stroke:#C28A5A'), ('background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)', 'background:rgba(217,174,133,.45);border:1.5px solid #D9AE85;box-shadow:0 10px 28px rgba(20,30,45,.22)'),
             ('background: rgba(250,248,243,.92); border: 1px solid #D4C9BC', 'background: rgba(242,235,220,.94); border: 1px solid #D9AE85'),
             ('rgba(196,118,90,.18)', 'rgba(194,138,90,.2)'), ('<span style="font-size: 22px; opacity: .8">30 דק׳', '<span style="font-size: 26px">30 דק׳')]:
    rep(a, b)
s = s.replace('2px solid var(--s-copper)', '4px solid var(--s-copper)')

# HUD
tags = [('01 · The Core', 'מאצ\'ה לא מזמינים. מרכיבים.'), ("02 · L'Atelier", 'חוגת הטעמים: כוס אחת, חמישה טעמים'),
        ('03 · Les Suppléments', 'קצפת עולה, שוקולד נוזל, שם משלה'), ('04 · La Métamorphose', 'אותה כוס, גם חמה'),
        ('05 · The Promise', 'המטרפה לא משתנה')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>'); s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i); e = s.index('</span>', k); s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,15.3"'), ('data-show="14.7,18.7"', 'data-show="15.3,19.5"'),
             ('data-show="18.7,22.7"', 'data-show="19.5,22.9"'), ('data-show="22.7,30"', 'data-show="22.9,30"')]:
    rep(a, b)

# ── the flavour dial ──
FL = [('classic', 'Matcha Classique', 'ירוק עמוק, מריר-מתוק', '#DDE5C7'), ('fraise', 'Matcha Fraise', 'הכוס הוורודה של הבר', '#F1D5D2'),
      ('hojicha', 'Hōjicha', 'קרמל, עשן קל, בלי מרירות', '#EAD7BF'), ('yuzu', 'Matcha Yuzu', 'הכוס של הבוקר החם', '#F2E5B4'),
      ('bleu', 'Matcha Bleu', 'צבע שמשנה את מצב הרוח', '#D5DCEF')]
STEPS = [10.6, 11.7, 12.8, 13.9]           # ring turns 72° clockwise at each; the arriving flavour pours 0.4s later
GX, GY, GW, GH, RR = 348, 690, 384, 820, 470  # glass box (852×1820 at .4505) and ring radius; centre (540,1100)
ring = '0%%,%s{transform:rotate(0deg)}' % p(STEPS[0])
cr = '0%%,%s{transform:rotate(0deg)}' % p(STEPS[0])
for k, t in enumerate(STEPS):
    nxt = p(STEPS[k + 1]) if k < 3 else '100%'
    ring += '%s,%s{transform:rotate(%ddeg)}' % (p(t + .5), nxt, 72 * (k + 1))
    cr += '%s,%s{transform:rotate(%ddeg)}' % (p(t + .5), nxt, -72 * (k + 1))
bg = '0%%,%s{background-color:%s}' % (p(STEPS[0] + .4), FL[0][3])
for k, t in enumerate(STEPS):
    bg += '%s{background-color:%s}' % (p(t + .9), FL[k + 1][3])
bg += '100%%{background-color:%s}' % FL[4][3]
pours = ''.join('.pour%d{animation-name:pour%d;animation-timing-function:cubic-bezier(.5,0,.3,1)}@keyframes pour%d{0%%,%s{clip-path:inset(100%% 0 0 0)}%s,100%%{clip-path:inset(0 0 0 0)}}'
                % (k + 1, k + 1, k + 1, p(t + .4), p(t + .95)) for k, t in enumerate(STEPS))
names = []
wins = [(10.0, STEPS[0] + .5)] + [(t + .5, (STEPS[k + 1] + .5) if k < 3 else 15.6) for k, t in enumerate(STEPS)]

css = f"""
.core-ttl{{animation-name:corettl}}@keyframes corettl{{0%,{p(5.8)}{{opacity:0;letter-spacing:.5em}}{p(6.8)},100%{{opacity:1;letter-spacing:.18em}}}}
.c-l1{{animation-name:cl1}}@keyframes cl1{{0%,{p(6.0)}{{transform:translateY(110%)}}{p(6.6)},100%{{transform:none}}}}
.c-l2{{animation-name:cl2}}@keyframes cl2{{0%,{p(6.5)}{{transform:translateY(110%)}}{p(7.1)},100%{{transform:none}}}}
.d-bg{{animation-name:dbg}}@keyframes dbg{{{bg}}}
.d-ring{{animation-name:dring;transform-origin:0 0}}@keyframes dring{{{ring}}}
.d-cr{{animation-name:dcr}}@keyframes dcr{{{cr}}}
{pours}
.d-l1{{animation-name:dl1}}@keyframes dl1{{0%,{p(9.9)}{{transform:translateY(110%)}}{p(10.4)},100%{{transform:none}}}}
.d-l2{{animation-name:dl2}}@keyframes dl2{{0%,{p(10.2)}{{transform:translateY(110%)}}{p(10.7)},100%{{transform:none}}}}
.cream{{animation-name:cream;animation-timing-function:cubic-bezier(.4,0,.2,1)}}@keyframes cream{{0%,{p(15.7)}{{clip-path:inset(100% 0 0 0)}}{p(16.5)},100%{{clip-path:inset(0 0 0 0)}}}}
.choco{{animation-name:choco;animation-timing-function:cubic-bezier(.5,0,.6,1)}}@keyframes choco{{0%,{p(16.5)}{{clip-path:inset(0 0 100% 0)}}{p(17.4)},100%{{clip-path:inset(0 0 0 0)}}}}
.card{{animation-name:card}}@keyframes card{{0%,{p(17.3)}{{opacity:0;transform:translateY(60px) rotate(-3deg)}}{p(17.9)},100%{{opacity:1;transform:rotate(-2deg)}}}}
.s-l1{{animation-name:sl1}}@keyframes sl1{{0%,{p(15.4)}{{transform:translateY(110%)}}{p(15.9)},100%{{transform:none}}}}
.s-l2{{animation-name:sl2}}@keyframes sl2{{0%,{p(15.7)}{{transform:translateY(110%)}}{p(16.2)},100%{{transform:none}}}}
{''.join('.lift%d{{animation-name:lift%d}}@keyframes lift%d{{0%,{a}{{transform:none}}{b}{{transform:translateY(-34px)}}{c},100%{{transform:none}}}}'.format(i, i, i, a=p(20.6 + i * .5), b=p(20.9 + i * .5), c=p(21.3 + i * .5)) for i in range(5))}
.ntile img{{border-radius:20px}}
.w-push{{animation-name:wpush}}@keyframes wpush{{0%,{p(22.7)}{{transform:scale(1.1) rotate(-4deg)}}100%{{transform:none}}}}
.w-l1{{animation-name:wl1}}@keyframes wl1{{0%,{p(23.3)}{{transform:translateY(110%)}}{p(23.9)},100%{{transform:none}}}}
.w-l2{{animation-name:wl2}}@keyframes wl2{{0%,{p(23.7)}{{transform:translateY(110%)}}{p(24.3)},100%{{transform:none}}}}
"""
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · CHASEN ── */' + css)

def seq(prefix, n, start, step, a, b):
    return (f'<div class="stack" data-show="{a},{b}" data-fade="0.12"><div class="stack" data-seq="f/{prefix}_%03d.jpg" data-from="1" data-to="{n}" '
            f'data-start="{start}" data-step="{step}" data-pos="50% 50%"></div></div>')
GT = f'<div style="position: absolute; left: 0; right: 0; top: 0; height: 520px; background: linear-gradient(to bottom, rgba(244,231,213,.95) 38%, rgba(244,231,213,0))"></div>'
GB = f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 760px; background: linear-gradient(to top, rgba(244,231,213,.96) 45%, rgba(244,231,213,0))"></div>'
A = f"""<section class="scene" data-show="0,10.1">
    {seq('p', 24, 5.4, 0.06, 0, 6.9)}{seq('c', 28, 6.9, 0.06, 6.85, 8.6)}{seq('v', 24, 8.6, 0.06, 8.55, 10.2)}
    {GT}{GB}
    <div style="position: absolute; top: 200px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 12px">
      <div class="core-ttl" style="font-family: 'Cormorant Garamond', serif; font-size: 112px; font-weight: 500; line-height: 1; color: {INK}" dir="ltr">CHASEN°</div>
      <div data-in="6.4" style="font-family: 'Assistant', sans-serif; font-size: 24px; font-weight: 600; letter-spacing: .34em; color: {MATCHA}" dir="ltr">BAR À MATCHA</div>
    </div>
    <div style="position: absolute; bottom: 210px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="c-l1" style="display: block; {H}; font-size: 100px; font-weight: 300; line-height: 1.12; color: {INK}">מאצ'ה לא מזמינים.</span></span>
      <span class="mask"><span class="c-l2" style="display: block; {H}; font-size: 100px; font-weight: 600; line-height: 1.12; color: {MATCHA}">מרכיבים.</span></span>
      <div data-in="7.6" style="margin-top: 18px; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 40px; color: #5C6B52" dir="ltr">Le matcha ne se commande pas. Il se compose.</div>
    </div>
  </section>"""

glass = lambda f, cls='', extra='': f'<img class="{cls}" src="{R}chasen/img/glass_{f}.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block{extra}">'
medals = ''.join(f"""<div style="position: absolute; left: 0; top: 0; transform: rotate({-72 * i}deg) translateY(-{RR}px) rotate({72 * i}deg)"><div class="d-cr" style="position: absolute; left: -64px; top: -64px; width: 128px; height: 128px; border-radius: 50%; overflow: hidden; background: {BG}; box-shadow: 0 0 0 3px #FFFFFF, 0 0 0 5px {MATCHA}, 0 14px 30px rgba(31,42,31,.18)"><img src="{R}chasen/img/glass_{f}.webp" alt="{n}" style="position: absolute; left: -6px; top: -50px; width: 140px; height: 300px"></div></div>"""
                 for i, (f, n, d, c) in enumerate(FL))
labels = ''.join(f"""<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.18" style="display: flex; flex-direction: column; align-items: center; gap: 4px"><span style="font-family: 'Cormorant Garamond', serif; font-size: 64px; line-height: 1; color: {INK}" dir="ltr">{n}</span><span style="{H}; font-size: 32px; font-weight: 300; color: #4A5642" dir="rtl">{d}</span></div>"""
                 for (f, n, d, c), (a, b) in zip(FL, wins))
B = f"""<section class="scene" data-show="9.7,15.6">
    <div class="stack d-bg" style="background-color: {FL[0][3]}"></div>
    <div style="position: absolute; top: 200px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="9.8" style="{K}; margin-bottom: 8px" dir="ltr">L'Atelier</div>
      <span class="mask"><span class="d-l1" style="display: block; {H}; font-size: 72px; font-weight: 300; line-height: 1.15; color: {INK}">הכוס הזאת עוד לא קיימת.</span></span>
      <span class="mask"><span class="d-l2" style="display: block; {H}; font-size: 72px; font-weight: 600; line-height: 1.15; color: {MATCHA}">עד שאת מכינה אותה.</span></span>
    </div>
    <div style="position: absolute; left: {540 - RR}px; top: {1100 - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(76,107,51,.45); box-sizing: border-box"></div>
    <div style="position: absolute; left: {GX}px; top: {GY}px; width: {GW}px; height: {GH}px; border-radius: {GW // 2}px {GW // 2}px 26px 26px; overflow: hidden; background: {BG}; box-shadow: 0 30px 70px rgba(31,42,31,.18)">
      {glass('classic')}{glass('fraise', 'pour1')}{glass('hojicha', 'pour2')}{glass('yuzu', 'pour3')}{glass('bleu', 'pour4')}
    </div>
    <div class="d-ring" style="position: absolute; left: 540px; top: 1100px; width: 0; height: 0">{medals}</div>
    <div style="position: absolute; top: {1100 - RR - 64 - 46}px; left: 522px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {MATCHA}"></div>
    <div style="position: absolute; top: 1680px; left: 40px; right: 40px; height: 120px">{labels}</div>
  </section>"""

CR = .4505
C = f"""<section class="scene" data-show="15.3,19.6">
    <div class="stack" style="background: #F3E6D3"></div>
    <div class="ntile" style="position: absolute; left: 215px; top: 470px; width: 650px; height: 1156px; border-radius: 20px; box-shadow: 0 30px 70px rgba(31,42,31,.18)"><div class="stack" data-seq="f/n_%03d.jpg" data-from="1" data-to="51" data-start="15.4" data-step="0.078" data-pos="50% 50%"></div></div>
    <div style="position: absolute; top: 200px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="15.3" style="{K}; margin-bottom: 8px" dir="ltr">Les suppléments</div>
      <span class="mask"><span class="s-l1" style="display: block; {H}; font-size: 72px; font-weight: 300; line-height: 1.15; color: {INK}">אותה כוס.</span></span>
      <span class="mask"><span class="s-l2" style="display: block; {H}; font-size: 72px; font-weight: 600; line-height: 1.15; color: {MATCHA}">שם משלה.</span></span>
    </div>
    <div class="card" style="position: absolute; left: 220px; top: 1580px; width: 640px; box-sizing: border-box; padding: 26px 34px; background: #FBF6EC; border: 2px solid {MATCHA}; border-radius: 18px; box-shadow: 0 24px 50px rgba(31,42,31,.2); display: flex; flex-direction: column; align-items: center; gap: 6px">
      <div style="font-family: 'Assistant', sans-serif; font-size: 18px; font-weight: 600; letter-spacing: .3em; color: {MATCHA}" dir="ltr">CHASEN° · N°22</div>
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 46px; line-height: 1; color: {INK}" dir="ltr">Classique · Crème · Cacao</div>
      <div style="{H}; font-size: 28px; font-weight: 300; color: #4A5642" dir="rtl">זה הכרטיס שהמשקה שלך מקבל בבר.</div>
    </div>
  </section>"""

D = f"""<section class="scene" data-show="19.3,23.2">
    <div class="stack" style="background: #F3E6D3"></div>
    <div class="stack" data-seq="f/m_%03d.jpg" data-from="1" data-to="60" data-start="19.3" data-step="0.062" data-pos="50% 40%"></div>
    {GB}
    <div style="position: absolute; bottom: 230px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="19.6" style="{K}; margin-bottom: 8px" dir="ltr">La Métamorphose</div>
      <div data-in="19.9" style="{H}; font-size: 76px; font-weight: 300; line-height: 1.15; color: {INK}">אותה כוס.<br><b style="font-weight: 600; color: {MATCHA}">גם חמה.</b></div>
    </div>
  </section>"""

E = f"""<section class="scene" data-show="22.7,30">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; left: 60px; top: 520px; width: 960px; height: 720px; overflow: hidden; -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 62%, transparent 100%); mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 62%, transparent 100%)">
      <img class="w-push" src="{R}chasen/assets/chasen.webp" alt="The chasen whisk resting in the bowl" style="width: 100%; height: 100%; object-fit: cover; display: block">
    </div>
    <div data-in="23.0" style="position: absolute; top: 210px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px">
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 96px; font-weight: 500; line-height: 1; color: {INK}" dir="ltr">CHASEN°</div>
      <div style="{K}; font-size: 36px" dir="ltr">Le Chasen · la promesse</div>
    </div>
    <div style="position: absolute; bottom: 260px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="w-l1" style="display: block; {H}; font-size: 80px; font-weight: 300; line-height: 1.15; color: {INK}">המטרפה היא הדבר היחיד</span></span>
      <span class="mask"><span class="w-l2" style="display: block; {H}; font-size: 80px; font-weight: 600; line-height: 1.15; color: {MATCHA}">שלא משתנה.</span></span>
      <div data-in="24.8" style="margin-top: 18px; {H}; font-size: 34px; font-weight: 300; color: #4A5642">כל השאר נבחר בכל פעם מחדש.</div>
    </div>
  </section>"""

i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D, E]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
open(os.path.join(HERE, 'chasen-stay.html'), 'w').write(s)
print('ok', len(s))
