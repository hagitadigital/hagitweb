import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'   # the skill folder
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
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">19</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'בר מאצ\'ה שבו הכוס לא קיימת עד שהיא שלך.')
rep('BRAND° · עולם מותג NN', 'CHASEN° · עולם מותג 19')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'את <span dir="ltr">CHASEN°</span> לא משווים.<br>מרכיבים.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ללקוחות שלך יש מה לבחור.<br>יש להן למה לבחור בך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 19')

# hook: price card (mechanic 1), drop mechanic 2
rep('EDIT-product.jpg', 'chasen/img/glass_classic.webp')
rep('alt="" style="width: 100%; height: 470px; object-fit: cover; border-radius: 12px; display: block">',
    'alt="A matcha latte" style="width: 100%; height: 470px; object-fit: cover; object-position: 50% 42%; border-radius: 12px; display: block">')
rep('>EDIT: למה תמיד<br>', '>למה תמיד<br>')
rep('EDIT: שם גנרי · 30ml', 'מאצ\'ה לאטה קרה · 350ml'); rep('₪000', '₪24')
i = s.index('<!-- proof mechanic 2'); j = s.index('-->', i) + 3; s = s[:i] + s[j:]

# HUD
tags = [('01 · The Core', 'מאצ\'ה לא מזמינים. מרכיבים.'), ("02 · L'Atelier", 'חוגת הטעמים: כוס אחת, חמישה טעמים'),
        ('03 · Les Suppléments', 'קצפת עולה, שוקולד נוזל, שם משלו'), ('04 · La Carte', 'חמישה טעמים, אינסוף כוסות'),
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

glass = lambda f, cls='', extra='': f'<img class="{cls}" src="chasen/img/glass_{f}.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block{extra}">'
medals = ''.join(f"""<div style="position: absolute; left: 0; top: 0; transform: rotate({-72 * i}deg) translateY(-{RR}px) rotate({72 * i}deg)"><div class="d-cr" style="position: absolute; left: -64px; top: -64px; width: 128px; height: 128px; border-radius: 50%; overflow: hidden; background: {BG}; box-shadow: 0 0 0 3px #FFFFFF, 0 0 0 5px {MATCHA}, 0 14px 30px rgba(31,42,31,.18)"><img src="chasen/img/glass_{f}.webp" alt="{n}" style="position: absolute; left: -6px; top: -50px; width: 140px; height: 300px"></div></div>"""
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
    <div class="stack" style="background-color: {FL[4][3]}"></div>
    <div style="position: absolute; top: 200px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="15.3" style="{K}; margin-bottom: 8px" dir="ltr">Les suppléments</div>
      <span class="mask"><span class="s-l1" style="display: block; {H}; font-size: 72px; font-weight: 300; line-height: 1.15; color: {INK}">אותה כוס.</span></span>
      <span class="mask"><span class="s-l2" style="display: block; {H}; font-size: 72px; font-weight: 600; line-height: 1.15; color: {MATCHA}">שם משלו.</span></span>
    </div>
    <div style="position: absolute; left: {GX}px; top: {GY}px; width: {GW}px; height: {GH}px; border-radius: {GW // 2}px {GW // 2}px 26px 26px; overflow: hidden; background: {BG}; box-shadow: 0 30px 70px rgba(31,42,31,.18)">
      {glass('bleu')}
      <img class="choco" src="chasen/img/layer_choco.webp" alt="" style="position: absolute; left: {178 * CR:.1f}px; top: {532 * CR:.1f}px; width: {512 * CR:.1f}px; height: {1169 * CR:.1f}px">
      <img class="cream" src="chasen/img/layer_cream.webp" alt="" style="position: absolute; left: {149 * CR:.1f}px; top: {159 * CR:.1f}px; width: {552 * CR:.1f}px; height: {719 * CR:.1f}px">
    </div>
    <div class="card" style="position: absolute; left: 250px; top: 1560px; width: 580px; box-sizing: border-box; padding: 26px 34px; background: #FBF6EC; border: 2px solid {MATCHA}; border-radius: 18px; box-shadow: 0 24px 50px rgba(31,42,31,.2); display: flex; flex-direction: column; align-items: center; gap: 6px">
      <div style="font-family: 'Assistant', sans-serif; font-size: 18px; font-weight: 600; letter-spacing: .3em; color: {MATCHA}" dir="ltr">CHASEN° · N°19</div>
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 58px; line-height: 1; color: {INK}" dir="ltr">Bleu · Crème · Cacao</div>
      <div style="{H}; font-size: 28px; font-weight: 300; color: #4A5642" dir="rtl">זה הכרטיס שהמשקה שלך מקבל בבר.</div>
    </div>
  </section>"""

cards = ''.join(f"""<div data-in="{19.6 + i * .22:.2f}" style="display: flex; flex-direction: column; align-items: center; width: 196px"><div class="lift{i}" style="width: 196px; height: 419px"><img src="chasen/img/glass_{f}.webp" alt="{n}" style="width: 100%; height: 100%; display: block"></div>
      <div style="margin-top: 14px; font-family: 'Cormorant Garamond', serif; font-size: 34px; line-height: 1.05; color: {INK}; text-align: center" dir="ltr">{n.replace('Matcha ', '')}</div>
      <div style="margin-top: 6px; {H}; font-size: 22px; font-weight: 300; color: #4A5642; text-align: center; padding: 0 6px" dir="rtl">{d}</div></div>"""
                for i, (f, n, d, c) in enumerate(FL))
D = f"""<section class="scene" data-show="19.3,23.2">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 210px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px; text-align: center">
      <div data-in="19.4" style="{K}" dir="ltr">La Carte.</div>
      <div data-in="19.6" style="{H}; font-size: 76px; font-weight: 300; line-height: 1.15; color: {INK}" dir="rtl">חמישה טעמים,<br><b style="font-weight: 600; color: {MATCHA}">אינסוף כוסות.</b></div>
    </div>
    <div style="position: absolute; top: 700px; left: 50px; right: 50px; display: flex; justify-content: space-between" dir="ltr">{cards}</div>
    <div data-in="21.0" style="position: absolute; top: 1420px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 46px; color: {MATCHA}" dir="ltr">Glacé · Crème · Cacao</div>
  </section>"""

E = f"""<section class="scene" data-show="22.7,30">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; left: 60px; top: 520px; width: 960px; height: 720px; overflow: hidden; -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 62%, transparent 100%); mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 62%, transparent 100%)">
      <img class="w-push" src="chasen/assets/chasen.webp" alt="The chasen whisk resting in the bowl" style="width: 100%; height: 100%; object-fit: cover; display: block">
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
open(os.path.join(HERE, 'reel.html'), 'w').write(s)
print('ok', len(s))
