"""SIGNÉ° — world film, studio mode (World N°17). Fills the skill's reel template.
Hook A (hidden logo, the piped signature stays) · signature scene A (La Coupe as a dial → the sixth flavour drops in).
Run: python3 gen.py  →  reel.html next to this file; assets come from make_assets.sh (./a)."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '../../../../.claude/skills/brandos-brand-world-reel/')
s = open(SK + 'assets/reel-template.html').read()
def p(t): return '%.3f%%' % (max(0, min(30, t)) / 30 * 100)
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

NOIR, CREAM, DIM, GOLD = '#120E08', '#F0E3CE', '#BFAF95', '#C9A25E'
H = "font-family: 'Assistant', sans-serif"
CG = "font-family: 'Cormorant Garamond', serif"
SC = f"font-family: 'Italianno', cursive; color: {GOLD}"
LTR = lambda t: f'<span dir="ltr" style="unicode-bidi: isolate">\u2066{t}\u2069</span>'
SIG = 'SIGNÉ<sup style="font-size: .38em; vertical-align: .9em; color: ' + GOLD + '">°</sup>'

rep("--w-bg:#F7F0E6;", f"--w-bg:{NOIR};"); rep("--w-ink:#3B2E33;", f"--w-ink:{CREAM};"); rep("--w-accent:#C9878E;", f"--w-accent:{GOLD};")
rep('family=Assistant:wght@300;400;600;700', 'family=Assistant:wght@200;300;400;600;700&amp;family=Italianno')
s = s.replace('<title>Brand World Reel</title>', '<title>SIGNÉ° world film</title>')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">17</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', f'מזון קינוחים שבו כל קינוח נחתם ביד אחת, שאי אפשר לזייף.')
rep('BRAND° · עולם מותג NN', f'{LTR("SIGNÉ°")} · עולם מותג 17')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', f'את {LTR("SIGNÉ°")} מזהים<br>לפי החתימה.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>מה החתימה שלו?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 17')
s = s.replace('מזון קינוחים', 'בית קינוחים')

# ── hook: the hidden logo. A copper bar covers the name; the piped signature on the éclair stays. ──
rep('>EDIT: למה תמיד<br>משווים אותך <span style="color: var(--s-copper)">במחיר</span>?</div>',
    '>אם נסתיר את הלוגו,<br>עדיין <span style="color: var(--s-copper)">יזהו</span> אותך?</div>')
i = s.index('  <!-- proof mechanic 1'); j = s.index('  <!-- proof mechanic 2'); s = s[:i] + s[j:]
i = s.index('  <!-- proof mechanic 2'); j = s.index('-->', s.index('</div> -->', i)) + 3
s = s[:i] + f"""  <div class="hp" style="position: absolute; top: 600px; left: 190px; width: 700px; height: 824px; border-radius: 24px; overflow: hidden; box-shadow: 0 30px 70px rgba(62,47,37,.28)">
    <img class="cover" src="a/eclair.jpg" alt="The Le Noir éclair with its piped cream signature">
    <div style="position: absolute; top: 46px; left: 0; right: 0; text-align: center; {CG}; font-size: 76px; font-weight: 500; letter-spacing: .08em; color: {CREAM}" dir="ltr">{SIG}</div>
    <div class="hbar" style="position: absolute; left: 150px; right: 150px; top: 40px; height: 104px; background: var(--s-copper); border-radius: 8px"></div>
  </div>
""" + s[j:]

# ── HUD ──
tags = [('01 · The Core', 'יש קינוחים שמוגשים. ויש שנחתמים.'), ('02 · La Coupe', 'חמישה טעמים. השישי בדרך אלייך.'),
        ('03 · La Promesse', 'פס קרם אחד, ביד חופשית'), ('04 · La Carte Vivante', 'התפריט לא מודפס. הוא חי.'),
        ('05 · The Promise', 'ארבע מהדורות. חתימה אחת.')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>'); s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i); e = s.index('</span>', k); s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,16.3"'), ('data-show="14.7,18.7"', 'data-show="16.3,19.7"'),
             ('data-show="18.7,22.7"', 'data-show="19.7,23.4"'), ('data-show="22.7,30"', 'data-show="23.4,30"')]:
    rep(a, b)

# ── the coupe dial ──
# scoop angles on the plate (clockwise from the top): vanilla 352°, pistachio 53°, chocolate 108°, caramel 181°, raspberry 275°.
# The plate turns clockwise; the scoop that arrives under the pointer is the one counter-clockwise of it.
FL = [(8, 'Vanille', 'וניל', '#EFE3CB'), (85, 'Framboise', 'פטל', '#8A2E45'), (179, 'Caramel', 'קרמל', '#C98F45'),
      (252, 'Chocolat', 'שוקולד', '#7A5034'), (307, 'Pistache', 'פיסטוק', '#97A96B')]
STEPS = [10.6, 11.45, 12.3, 13.15]          # the plate moves 0.4s from each of these
END = 14.0                                  # last move: pistachio → the empty well (360°), then the sixth drops in
DROP, DSTEP, DN = 14.45, 0.04, 52
PX, PY, PW = 90, 560, 900                   # the plate box (centre 540,1010)
rot = '0%%,%s{transform:rotate(%ddeg)}' % (p(STEPS[0]), FL[0][0])
for k, t in enumerate(STEPS):
    rot += '%s,%s{transform:rotate(%ddeg)}' % (p(t + .4), p(STEPS[k + 1] if k < 3 else END), FL[k + 1][0])
rot += '%s,100%%{transform:rotate(360deg)}' % p(END + .4)
glow = '0%%,%s{--g:%s}' % (p(STEPS[0] + .2), FL[0][3])
for k, t in enumerate(STEPS):
    glow += '%s,%s{--g:%s}' % (p(t + .4), p(STEPS[k + 1] + .2 if k < 3 else END + .2), FL[k + 1][3])
glow += '%s,100%%{--g:%s}' % (p(END + .5), GOLD)
wins = [(9.8, STEPS[0] + .25)] + [(t + .3, (STEPS[k + 1] + .25) if k < 3 else END + .25) for k, t in enumerate(STEPS)]

css = f"""
@property --g{{syntax:"<color>";inherits:true;initial-value:#EFE3CB}}
.core-ttl{{animation-name:corettl}}@keyframes corettl{{0%,{p(5.7)}{{opacity:0;letter-spacing:.3em}}{p(6.7)},100%{{opacity:1;letter-spacing:.08em}}}}
.c-sig{{animation-name:csig;animation-timing-function:cubic-bezier(.6,.05,.25,1)}}@keyframes csig{{0%,{p(6.4)}{{clip-path:inset(0 100% 0 0)}}{p(7.9)},100%{{clip-path:inset(0 0 0 0)}}}}
.c-l1{{animation-name:cl1}}@keyframes cl1{{0%,{p(7.2)}{{transform:translateY(110%)}}{p(7.8)},100%{{transform:none}}}}
.c-l2{{animation-name:cl2}}@keyframes cl2{{0%,{p(7.8)}{{transform:translateY(110%)}}{p(8.4)},100%{{transform:none}}}}
.d-glow{{animation-name:dglow;background:radial-gradient(circle at 50% 52.6%, var(--g) 0%, transparent 58%)}}@keyframes dglow{{{glow}}}
.d-rot{{animation-name:drot;animation-timing-function:cubic-bezier(.55,0,.25,1)}}@keyframes drot{{{rot}}}
.d-l1{{animation-name:dl1}}@keyframes dl1{{0%,{p(9.9)}{{transform:translateY(110%)}}{p(10.4)},100%{{transform:none}}}}
.d-l2{{animation-name:dl2}}@keyframes dl2{{0%,{p(END + .2)}{{transform:translateY(110%)}}{p(END + .8)},100%{{transform:none}}}}
.e-pan{{animation-name:epan;animation-timing-function:cubic-bezier(.45,0,.35,1)}}@keyframes epan{{0%,{p(16.2)}{{transform:translateX(-430px)}}{p(19.8)},100%{{transform:translateX(-1500px)}}}}
.e-line{{animation-name:eline;animation-timing-function:cubic-bezier(.5,0,.4,1)}}@keyframes eline{{0%,{p(16.7)}{{stroke-dashoffset:1}}{p(18.9)},100%{{stroke-dashoffset:0}}}}
.e-l1{{animation-name:el1}}@keyframes el1{{0%,{p(16.4)}{{transform:translateY(110%)}}{p(17.0)},100%{{transform:none}}}}
.e-l2{{animation-name:el2}}@keyframes el2{{0%,{p(16.8)}{{transform:translateY(110%)}}{p(17.4)},100%{{transform:none}}}}
.f-push{{animation-name:fpush}}@keyframes fpush{{0%,{p(22.1)}{{transform:scale(1.1)}}{p(23.6)},100%{{transform:none}}}}
.g-sig{{animation-name:gsig;animation-timing-function:cubic-bezier(.6,.05,.25,1)}}@keyframes gsig{{0%,{p(25.4)}{{clip-path:inset(0 100% 0 0)}}{p(27.0)},100%{{clip-path:inset(0 0 0 0)}}}}
.g-l1{{animation-name:gl1}}@keyframes gl1{{0%,{p(23.5)}{{transform:translateY(110%)}}{p(24.1)},100%{{transform:none}}}}
.g-l2{{animation-name:gl2}}@keyframes gl2{{0%,{p(23.9)}{{transform:translateY(110%)}}{p(24.5)},100%{{transform:none}}}}
"""
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · SIGNÉ° ── */' + css)

GT = lambda h=560: f'<div style="position: absolute; left: 0; right: 0; top: 0; height: {h}px; background: linear-gradient(to bottom, rgba(18,14,8,.96) 40%, rgba(18,14,8,0))"></div>'
GB = lambda h=780: f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: {h}px; background: linear-gradient(to top, rgba(18,14,8,.97) 45%, rgba(18,14,8,0))"></div>'
def head(tag, l1, l2, c1, c2, t, top=190):
    return f"""<div style="position: absolute; top: {top}px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="{t}" style="{CG}; font-style: italic; font-size: 44px; color: {GOLD}; margin-bottom: 10px" dir="ltr">{tag}</div>
      <span class="mask"><span class="{c1}" style="display: block; {H}; font-size: 74px; font-weight: 200; line-height: 1.18; color: {CREAM}">{l1}</span></span>
      <span class="mask"><span class="{c2}" style="display: block; {H}; font-size: 74px; font-weight: 600; line-height: 1.18; color: {CREAM}">{l2}</span></span>
    </div>"""

A = f"""<section class="scene" data-show="0,10.1">
    <div class="stack" style="background: {NOIR}"></div>
    <div class="stack" data-seq="a/pour/f_%03d.jpg" data-from="1" data-to="41" data-start="5.4" data-step="0.06"></div>
    {GT(620)}{GB(820)}
    <div style="position: absolute; top: 190px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 0">
      <div class="core-ttl" style="{CG}; font-size: 150px; font-weight: 500; line-height: 1; color: {CREAM}" dir="ltr">{SIG}</div>
      <div data-in="6.0" style="font-family: 'Assistant', sans-serif; font-size: 22px; font-weight: 400; letter-spacing: .34em; color: {GOLD}; margin-top: 14px" dir="ltr">MAISON DE DESSERTS</div>
    </div>
    <div style="position: absolute; bottom: 200px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div class="c-sig" style="{SC}; font-size: 104px; line-height: 1; margin-bottom: 26px" dir="ltr">Chaque dessert est signé.</div>
      <span class="mask"><span class="c-l1" style="display: block; {H}; font-size: 76px; font-weight: 200; line-height: 1.2; color: {CREAM}">יש קינוחים שמוגשים.</span></span>
      <span class="mask"><span class="c-l2" style="display: block; {H}; font-size: 76px; font-weight: 600; line-height: 1.2; color: {CREAM}">ויש קינוחים <span style="color: {GOLD}">שנחתמים.</span></span></span>
    </div>
  </section>"""

labels = ''.join(f"""<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.18" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{CG}; font-size: 72px; line-height: 1; color: {CREAM}" dir="ltr">{fr}</span><span style="{H}; font-size: 40px; font-weight: 300; color: {DIM}" dir="rtl">{he}</span></div>"""
                 for (ang, fr, he, c), (a, b) in zip(FL, wins))
labels += f"""<div class="stack" data-show="{END + .3:.2f},16.6" data-fade="0.2" style="display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{CG}; font-size: 72px; line-height: 1; color: {GOLD}" dir="ltr">Le Sixième</span><span style="{H}; font-size: 34px; font-weight: 300; color: {DIM}" dir="rtl">ישר מהמזיגה אל הקערה</span></div>"""
plate_mask = 'clip-path: circle(46.2% at 50% 50%)'
drop_mask = '-webkit-mask-image: radial-gradient(circle at 50% 50%, #000 58%, transparent 70%); mask-image: radial-gradient(circle at 50% 50%, #000 58%, transparent 70%)'
B = f"""<section class="scene" data-show="9.7,16.6">
    <div class="stack" style="background: {NOIR}"></div>
    <div class="stack d-glow" style="opacity: .5"></div>
    {head('La Coupe', 'חמישה טעמים בקערה.', 'השישי — בדרך אלייך.', 'd-l1', 'd-l2', 9.8)}
    <div class="stack" data-show="9.7,{END + .5:.2f}" data-fade="0.25">
      <div style="position: absolute; left: {PX}px; top: {PY}px; width: {PW}px; height: {PW}px; filter: drop-shadow(0 40px 60px rgba(0,0,0,.55))">
        <div class="d-rot" style="position: absolute; inset: 0; {plate_mask}"><img src="a/plate.jpg" alt="The SIGNÉ° flavour plate from above: five gelato scoops around an empty well" style="width: 100%; height: 100%; display: block"></div>
      </div>
    </div>
    <div class="stack" data-show="{END + .45:.2f},16.6" data-fade="0.08">
      <div style="position: absolute; left: {PX - 50}px; top: {PY - 50}px; width: {PW + 100}px; height: {PW + 100}px; {drop_mask}">
        <div class="stack" data-seq="a/drop/f_%03d.jpg" data-from="1" data-to="{DN}" data-start="{DROP}" data-step="{DSTEP}"></div>
      </div>
    </div>
    <div style="position: absolute; top: {PY - 14}px; left: 522px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 28px solid {GOLD}"></div>
    <div style="position: absolute; top: 1540px; left: 40px; right: 40px; height: 140px">{labels}</div>
  </section>"""

LINE = 'M -40 1360 C 120 1300, 200 1420, 330 1350 S 520 1270, 600 1345 S 760 1430, 880 1340 S 1040 1300, 1130 1350'
C = f"""<section class="scene" data-show="16.3,19.9">
    <div class="stack" style="background: {NOIR}"></div>
    <div style="position: absolute; left: 0; top: 0; height: 1920px; width: 2879px"><img class="e-pan" src="a/piping.jpg" alt="A hand pipes one continuous line of cream on dark slate" style="height: 1920px; width: 2879px; display: block"></div>
    {GT(640)}{GB(560)}
    {head('La Promesse', 'קינוח לא יוצא מהמטבח', 'בלי חתימה ביד.', 'e-l1', 'e-l2', 16.4)}
    <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="e-line" pathLength="1" d="{LINE}" style="fill: none; stroke: {CREAM}; stroke-width: 11; stroke-linecap: round; stroke-dasharray: 1 1; filter: drop-shadow(0 2px 8px rgba(240,227,206,.45))"></path></svg>
    <div data-in="17.6" style="position: absolute; bottom: 230px; left: 80px; right: 80px; text-align: center; {H}; font-size: 38px; font-weight: 300; line-height: 1.5; color: {DIM}" dir="rtl">פס קרם אחד רציף, מזולף ביד חופשית.<br>אין שניים זהים.</div>
  </section>"""

CARTE = [('noir', 'Le Noir', 'אקלר שוקולד 70% · עלי זהב'), ('framboise', 'La Tarte Framboise', 'פטל טרי על קרם פטיסייר'),
         ('pistache', 'Le Dôme Pistache', 'מוס פיסטוק · גלזורת מראה')]
CW = [(19.5, 20.6), (20.55, 21.6), (21.55, 22.35)]
holos = ''
for (n, fr, he), (a, b) in zip(CARTE, CW):
    holos += f"""<div class="stack" data-show="{a},{b}" data-fade="0.1">
      <div style="position: absolute; left: 0; top: 400px; width: 1080px; height: 1280px"><div class="stack" data-seq="a/{n}/f_%03d.jpg" data-from="4" data-to="36" data-by="3" data-start="{a}" data-step="0.09"></div>
        <div style="position: absolute; left: 0; right: 0; top: 0; height: 300px; background: linear-gradient(to bottom, {NOIR}, rgba(18,14,8,0))"></div>
        <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 320px; background: linear-gradient(to top, {NOIR}, rgba(18,14,8,0))"></div></div>
      <div style="position: absolute; top: 1560px; left: 40px; right: 40px; display: flex; flex-direction: column; align-items: center; gap: 6px"><span style="{CG}; font-size: 66px; line-height: 1; color: {CREAM}" dir="ltr">{fr}</span><span style="{H}; font-size: 32px; font-weight: 300; color: {DIM}" dir="rtl">{he}</span></div>
    </div>"""
D = f"""<section class="scene" data-show="19.5,23.5">
    <div class="stack" style="background: {NOIR}"></div>
    <div class="stack" data-show="19.5,22.3" data-fade="0.15">
      {holos}
      {head('La Carte Vivante', 'התפריט לא מודפס.', 'הוא חי.', 'h-l1', 'h-l2', 19.6)}
    </div>
    <div class="stack" data-show="22.2,23.5" data-fade="0.2">
      {head('La Maison', 'דלפק אחד מואר.', 'שורה אחת של קינוחים.', 'm-l1', 'm-l2', 22.2)}
      <div style="position: absolute; left: 0; top: 760px; width: 1080px; height: 720px; overflow: hidden; -webkit-mask-image: radial-gradient(ellipse 60% 56% at 50% 50%, #000 66%, transparent 100%); mask-image: radial-gradient(ellipse 60% 56% at 50% 50%, #000 66%, transparent 100%)">
        <img class="f-push" src="a/boutique.jpg" alt="The SIGNÉ° counter at night: one lit case with one row of the desserts" style="width: 100%; height: 100%; object-fit: cover; display: block">
      </div>
      <div data-in="22.6" style="position: absolute; top: 1560px; left: 0; right: 0; text-align: center; {CG}; font-style: italic; font-size: 44px; color: {GOLD}" dir="ltr">— fermé quand c'est fini.</div>
    </div>
  </section>"""
for c in ['h-l1', 'h-l2', 'm-l1', 'm-l2']:
    t = {'h-l1': 19.6, 'h-l2': 19.95, 'm-l1': 22.25, 'm-l2': 22.55}[c]
    rep('/* ── WORLD scenes · SIGNÉ° ── */', '/* ── WORLD scenes · SIGNÉ° ── */\n.%s{animation-name:%s}@keyframes %s{0%%,%s{transform:translateY(110%%)}%s,100%%{transform:none}}' % (c, c.replace('-', ''), c.replace('-', ''), p(t), p(t + .5)))

EDS = [('noir', 'Le Noir'), ('pistache', 'La Pistache'), ('framboise', 'La Framboise'), ('vanille', 'La Vanille')]
eds = ''.join(f"""<div data-in="{23.7 + i * .25:.2f}" style="position: absolute; left: {[555, 165, 555, 165][i]}px; top: {[560, 560, 1050, 1050][i]}px; width: 360px; display: flex; flex-direction: column; align-items: center; gap: 10px">
      <img src="a/ed-{n}.jpg" alt="{fr} éclair" style="width: 360px; height: 420px; object-fit: cover; border-radius: 6px; display: block; box-shadow: 0 24px 50px rgba(0,0,0,.5)">
      <span style="{CG}; font-size: 38px; line-height: 1; color: {CREAM}" dir="ltr">{fr}</span></div>""" for i, (n, fr) in enumerate(EDS))
E = f"""<section class="scene" data-show="23.2,30">
    <div class="stack" style="background: {NOIR}"></div>
    {head('Les Éditions Signées', 'ארבע מהדורות אקלר.', 'חתימה אחת.', 'g-l1', 'g-l2', 23.3)}
    {eds}
    <div class="g-sig" style="position: absolute; top: 1600px; left: 0; right: 0; text-align: center; {SC}; font-size: 112px; line-height: 1" dir="ltr">Chaque dessert est signé.</div>
  </section>"""

i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D, E]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
open(os.path.join(HERE, 'reel.html'), 'w').write(s)
print('ok', len(s))
