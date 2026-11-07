# La Leçon (CHASEN°, World 22) — studio-mode reel for workshop builders.
# Hook: "why are there empty chairs at your workshop?" · signature scene: "the table fills up".
# Run: python3 gen.py  → reel.html next to this file (assets in a/ and f/).
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '../../../.claude/skills/brandos-brand-world-reel/')
s = open(SK + 'assets/reel-template.html').read()
def p(t): return '%.3f%%' % (max(0, min(30, t)) / 30 * 100)
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b, 1)

INK, MATCHA, DEEP, BG = '#1F2A1F', '#4C6B33', '#22301F', '#F4E7D5'
H = "font-family: 'Heebo', sans-serif"
K = f"font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 46px; color: {MATCHA}"
NO = '22'

rep("--w-bg:#F7F0E6;", f"--w-bg:{BG};"); rep("--w-ink:#3B2E33;", f"--w-ink:{INK};"); rep("--w-accent:#C9878E;", f"--w-accent:{MATCHA};")
s = s.replace('<title>Brand World Reel</title>', '<title>La Leçon reel</title>')
rep('color: var(--s-gold)">NN</em>', f'color: var(--s-gold)">{NO}</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'סדנת מאצ\'ה של תשעים דקות סביב שולחן אחד, בעולם של <span dir="ltr">CHASEN°</span>.')
rep('BRAND° · עולם מותג NN', f'CHASEN° · La Leçon · עולם מותג {NO}')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'ב־<bdi dir="ltr">La Leçon</bdi> השולחן מתמלא,<br>כי נרשמים לחוויה.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'והסדנה שלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', f'Brand Worlds Studio · עולם מותג {NO}')

# ── HOOK: a generic no-name workshop flyer (not CHASEN), five empty chairs ──
rep('>EDIT: למה תמיד<br>משווים אותך <span style="color: var(--s-copper)">במחיר</span>?</div>',
    '>למה בסדנה שלך<br>נשארים כיסאות <span style="color: var(--s-copper)">ריקים</span>?</div>')
i = s.index('<!-- proof mechanic 1'); j = s.index('-->', s.index('<!-- proof mechanic 2')) + 3
chairs = ''.join(f'<span style="width: 62px; height: 62px; border-radius: 50%; box-sizing: border-box; {"background: #8E8A86" if k == 0 else "border: 3px dashed #C9C4BE"}"></span>' for k in range(6))
flyer = f"""<div class="hp" style="position: absolute; top: 640px; left: 190px; width: 700px; box-sizing: border-box; padding: 54px 50px 46px; background: #FFFFFF; border-radius: 20px; box-shadow: 0 24px 60px rgba(62,47,37,.14); display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; font-family: Arial, sans-serif; color: #3A3A3A" dir="rtl">
    <span style="position: absolute; top: 18px; right: 18px; padding: 8px 18px; border-radius: 999px; background: #2E2A27; color: #F4F2EF; font-family: 'Heebo', sans-serif; font-size: 22px">ככה מפרסמים</span>
    <div style="margin-top: 26px; font-size: 76px; font-weight: 700; color: #6E8F4E">סדנת מאצ'ה</div>
    <div style="font-size: 34px">שבת הקרובה · 10:00</div>
    <div style="font-size: 34px">₪240 למשתתפת</div>
    <div style="font-size: 28px; color: #8A8A8A">להרשמה שלחו הודעה בפרטי</div>
    <div style="margin-top: 26px; display: flex; gap: 22px">{chairs}</div>
    <div style="font-family: 'Heebo', sans-serif; font-size: 30px; color: #8A8A8A">נרשמה אחת. נשארו 5.</div>
  </div>"""
s = s[:i] + flyer + s[j:]

# ── HUD ──
tags = [("01 · La Leçon", 'את המטרפה לא קונים'), ('02 · La Table', 'שישה כיסאות, שולחן אחד'),
        ('03 · Les Gestes', 'לנפות, להקציף, למזוג'), ('04 · Réserver', 'ההרשמה נגמרת בכרטיס מקום'),
        ('05 · The Promise', 'יוצאות הביתה עם המטרפה')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>'); s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i); e = s.index('</span>', k); s = s[:k] + line + s[e:]
for a, b in [('data-show="5.6,9.9"', 'data-show="5.6,9.7"'), ('data-show="9.9,14.7"', 'data-show="9.7,19.2"'), ('data-show="14.7,18.7"', 'data-show="19.2,22.5"'),
             ('data-show="18.7,22.7"', 'data-show="22.5,25.9"'), ('data-show="22.7,30"', 'data-show="25.9,30"')]:
    rep(a, b)

# ── B · the table fills up ──
STEPS = [10.3, 11.7, 13.1, 14.5, 15.9, 17.1]           # chair k lights at STEPS[k]
ORDER = [0, 3, 1, 4, 2, 5]                              # like guests arriving: across the table, as on the site
MOM = [('couvert', '10:00 · המקום מחכה', None), ('t', '10:05 · השולחן', 'seq'), ('m', '10:40 · היד', 'seq'),
       ('glass_classic', '11:10 · הכוס', None), ('cadeau', '11:30 · המתנה', None)]
TINT = ['#F4E7D5', '#F1E3CF', '#EDDDC5', '#E8D6BA', '#E3CFAF', '#DCE3C5', '#D4DEB9']
bg = '0%%,%s{background-color:%s}' % (p(STEPS[0]), TINT[0])
for k, t in enumerate(STEPS):
    nxt = p(STEPS[k + 1]) if k < 5 else '100%'
    bg += '%s,%s{background-color:%s}' % (p(t + .4), nxt, TINT[k + 1])
seat_css = ''.join(
    '.seat%d{animation-name:seat%d}@keyframes seat%d{0%%,%s{background-color:rgba(31,42,31,0);border-color:rgba(31,42,31,.38);transform:scale(1)}%s{background-color:%s;border-color:%s;transform:scale(1.18)}%s,100%%{background-color:%s;border-color:%s;transform:scale(1)}}'
    % (k, k, k, p(t), p(t + .25), MATCHA, MATCHA, p(t + .5), MATCHA, MATCHA) for k, t in enumerate(STEPS))
ring_css = ''.join(
    '.pulse%d{animation-name:pulse%d;animation-timing-function:ease-out}@keyframes pulse%d{0%%,%s{opacity:0;transform:scale(1)}%s{opacity:.8;transform:scale(1)}%s,100%%{opacity:0;transform:scale(2.4)}}'
    % (k, k, k, p(t), p(t + .05), p(t + .8)) for k, t in enumerate(STEPS))
# the portal: each moment opens as a circle from the centre
port_css = ''.join(
    '.mo%d{animation-name:mo%d}@keyframes mo%d{0%%,%s{opacity:0;transform:scale(1.08)}%s{opacity:1}%s,100%%{opacity:1;transform:none}}'
    % (k, k, k, p(t + .05), p(t + .5), p(t + 1.3)) for k, t in enumerate(STEPS[:5]))

css = f"""
.a-push{{animation-name:apush;animation-timing-function:linear}}@keyframes apush{{0%{{transform:scale(1.12)}}{p(9.8)},100%{{transform:scale(1)}}}}
.a-l1{{animation-name:al1}}@keyframes al1{{0%,{p(6.0)}{{transform:translateY(110%)}}{p(6.6)},100%{{transform:none}}}}
.a-l2{{animation-name:al2}}@keyframes al2{{0%,{p(6.5)}{{transform:translateY(110%)}}{p(7.1)},100%{{transform:none}}}}
.b-bg{{animation-name:bbg}}@keyframes bbg{{{bg}}}
{seat_css}{ring_css}{port_css}
.b-l1{{animation-name:bl1}}@keyframes bl1{{0%,{p(9.8)}{{transform:translateY(110%)}}{p(10.3)},100%{{transform:none}}}}
.b-port{{animation-name:bport}}@keyframes bport{{0%,{p(9.9)}{{opacity:0;transform:scale(.6)}}{p(10.4)},{p(17.2)}{{opacity:1;transform:none}}{p(17.6)},100%{{opacity:0;transform:scale(.9)}}}}
.b-card{{animation-name:bcard}}@keyframes bcard{{0%,{p(17.3)}{{opacity:0;transform:perspective(1400px) translateY(80px) rotateX(55deg)}}{p(18.0)},100%{{opacity:1;transform:none}}}}
.c-l1{{animation-name:cl1}}@keyframes cl1{{0%,{p(19.3)}{{transform:translateY(110%)}}{p(19.8)},100%{{transform:none}}}}
{''.join('.g%d{{animation-name:g%d}}@keyframes g%d{{0%,{a}{{opacity:0;transform:translateX(-60px)}}{b},100%{{opacity:1;transform:none}}}}'.format(i, i, i, a=p(19.6 + i * .7), b=p(20.2 + i * .7)) for i in range(3))}
.d-l1{{animation-name:dl1}}@keyframes dl1{{0%,{p(22.6)}{{transform:translateY(110%)}}{p(23.1)},100%{{transform:none}}}}
.d-tap{{animation-name:dtap}}@keyframes dtap{{0%,{p(23.9)}{{opacity:0;transform:scale(1.6)}}{p(24.1)}{{opacity:.9;transform:scale(1)}}{p(24.4)},100%{{opacity:0;transform:scale(.8)}}}}
.d-form{{animation-name:dform}}@keyframes dform{{0%,{p(24.3)}{{opacity:1;transform:none}}{p(24.7)},100%{{opacity:.0;transform:translateY(40px) scale(.96)}}}}
.d-card{{animation-name:dcard}}@keyframes dcard{{0%,{p(24.4)}{{opacity:0;transform:perspective(1400px) translateY(90px) rotateX(55deg)}}{p(25.1)},100%{{opacity:1;transform:none}}}}
.e-push{{animation-name:epush;animation-timing-function:linear}}@keyframes epush{{0%,{p(25.9)}{{transform:scale(1.1)}}100%{{transform:none}}}}
.e-l1{{animation-name:el1}}@keyframes el1{{0%,{p(26.2)}{{transform:translateY(110%)}}{p(26.7)},100%{{transform:none}}}}
.e-l2{{animation-name:el2}}@keyframes el2{{0%,{p(26.5)}{{transform:translateY(110%)}}{p(27.0)},100%{{transform:none}}}}
"""
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · La Leçon ── */' + css)

GT = f'<div style="position: absolute; left: 0; right: 0; top: 0; height: 560px; background: linear-gradient(to bottom, rgba(244,231,213,.96) 40%, rgba(244,231,213,0))"></div>'
GB = f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 780px; background: linear-gradient(to top, rgba(244,231,213,.97) 46%, rgba(244,231,213,0))"></div>'

A = f"""<section class="scene" data-show="0,10">
    <div class="stack" style="overflow: hidden"><img class="cover a-push" src="a/hote.webp" alt="Maya, the host, with a matcha bowl and a bamboo whisk" style="object-position: 46% 30%"></div>
    {GT}{GB}
    <div style="position: absolute; top: 205px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px">
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 108px; font-weight: 500; line-height: 1; color: {INK}" dir="ltr">La Leçon</div>
      <div style="font-family: 'Assistant', sans-serif; font-size: 24px; font-weight: 600; letter-spacing: .34em; color: {MATCHA}" dir="ltr">CHASEN° · SAMEDI MATIN</div>
    </div>
    <div style="position: absolute; bottom: 200px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="a-l1" style="display: block; {H}; font-size: 92px; font-weight: 300; line-height: 1.12; color: {INK}">את המטרפה לא קונים.</span></span>
      <span class="mask"><span class="a-l2" style="display: block; {H}; font-size: 92px; font-weight: 600; line-height: 1.12; color: {MATCHA}">לומדים להחזיק אותה.</span></span>
      <div data-in="7.6" style="margin-top: 18px; {H}; font-size: 34px; font-weight: 300; color: #4A5642">מאיה, המארחת · תשעים דקות · שש משתתפות</div>
    </div>
  </section>"""

# portal (centre 540,800, r 330) + table (bar at y 1330) + seats in two rows
PX, PY, PR = 540, 800, 330
moments = ''
for k, (src, lab, kind) in enumerate(MOM):
    t = STEPS[k]
    if kind == 'seq':
        inner = (f'<div class="stack" data-seq="f/{src}_%03d.jpg" data-from="1" data-to="27" data-start="{t + .05:.2f}" data-step="0.05" '
                 f'data-pos="{"50% 45%" if src == "t" else "62% 55%"}"></div>')
    else:
        pos = {'couvert': '50% 55%', 'glass_classic': '50% 40%', 'cadeau': '50% 45%'}[src]
        inner = f'<img class="cover" src="a/{src}.webp" alt="" style="object-position: {pos}">'
    moments += f'<div class="stack mo{k}">{inner}</div>'
labels = ''.join(f'<div class="stack" data-show="{STEPS[k] + .1:.2f},{(STEPS[k + 1] + .1) if k < 4 else 17.2:.2f}" data-fade="0.15" style="display: flex; justify-content: center"><span style="font-family: \'Heebo\', sans-serif; font-size: 34px; font-weight: 500; color: {DEEP}; background: rgba(251,246,236,.92); padding: 6px 22px; border-radius: 999px" dir="rtl">{lab}</span></div>'
                 for k, (src, lab, kind) in enumerate(MOM))
SEATX = [300, 540, 780]
seats = ''
for j in range(6):
    k = ORDER.index(j)                                   # the step at which chair j fills
    x = SEATX[j % 3]; y = 1225 if j < 3 else 1435
    seats += (f'<div class="pulse{k}" style="position: absolute; left: {x - 46}px; top: {y - 46}px; width: 92px; height: 92px; border-radius: 50%; border: 3px solid {MATCHA}; box-sizing: border-box"></div>'
              f'<div class="seat{k}" style="position: absolute; left: {x - 46}px; top: {y - 46}px; width: 92px; height: 92px; border-radius: 50%; border: 3px dashed rgba(31,42,31,.38); box-sizing: border-box; display: grid; place-items: center; font-family: \'Assistant\', sans-serif; font-size: 30px; font-weight: 600; color: #F4E7D5">{k + 1}</div>')
left_txt = ['נשארו 6 מקומות', 'נשארו 5 מקומות', 'נשארו 4 מקומות', 'נשארו 3 מקומות', 'נשארו 2 מקומות', 'נשאר מקום אחד']
wins = [(9.7, STEPS[0] + .2)] + [(STEPS[k] + .2, STEPS[k + 1] + .2) for k in range(5)]
counter = ''.join(f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.12" style="text-align: center; {H}; font-size: 40px; font-weight: 400; color: {INK}" dir="rtl">{tx}</div>' for tx, (a, b) in zip(left_txt, wins))
counter += f'<div class="stack" data-show="{STEPS[5] + .2:.2f},19.4" data-fade="0.12" style="text-align: center; {H}; font-size: 44px; font-weight: 700; color: {MATCHA}" dir="rtl">השולחן מלא.</div>'

B = f"""<section class="scene" data-show="9.6,19.4">
    <div class="stack b-bg" style="background-color: {TINT[0]}"></div>
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="9.7" style="{K}; margin-bottom: 6px" dir="ltr">La table · 6</div>
      <span class="mask"><span class="b-l1" style="display: block; {H}; font-size: 66px; font-weight: 300; line-height: 1.15; color: {INK}">כל כיסא <b style="font-weight: 600; color: {MATCHA}">פותח רגע.</b></span></span>
    </div>
    <div class="b-port" style="position: absolute; left: {PX - PR}px; top: {PY - PR}px; width: {2 * PR}px; height: {2 * PR}px">
      <div style="position: absolute; inset: 0; border-radius: 50%; overflow: hidden; background: {BG}; box-shadow: 0 0 0 6px #FBF6EC, 0 0 0 8px #C4765A, 0 30px 70px rgba(31,42,31,.25)">{moments}</div>
      <div style="position: absolute; left: -40px; right: -40px; bottom: -34px; height: 60px">{labels}</div>
    </div>
    <div style="position: absolute; left: 190px; top: 1290px; width: 700px; height: 80px; border-radius: 14px; background: linear-gradient(90deg,#D7BF98,#E6D3B2 50%,#D7BF98); box-shadow: 0 16px 34px rgba(31,42,31,.15); display: grid; place-items: center; font-family: 'Cormorant Garamond', serif; font-size: 30px; letter-spacing: .16em; color: rgba(31,42,31,.55)" dir="ltr">La table</div>
    {seats}
    <div style="position: absolute; top: 1545px; left: 60px; right: 60px; height: 70px">{counter}</div>
    <div class="b-card" style="position: absolute; left: 230px; top: 440px; width: 620px; box-sizing: border-box; padding: 40px 40px 44px; background: #FBF6EC; border-radius: 10px; box-shadow: 0 40px 80px rgba(31,42,31,.3); display: flex; flex-direction: column; align-items: center; gap: 8px; border-top: 12px solid {MATCHA}">
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 36px; letter-spacing: .22em; color: {INK}" dir="ltr">CHASEN°</div>
      <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 30px; letter-spacing: .2em; color: #4A5642" dir="ltr">La Leçon</div>
      <div style="{H}; font-size: 110px; font-weight: 200; line-height: 1.2; color: {DEEP}" dir="rtl">דנה</div>
      <div style="width: 100%; border-top: 1px solid rgba(31,42,31,.15); border-bottom: 1px solid rgba(31,42,31,.15); padding: 18px 0; display: flex; justify-content: space-around; {H}; font-size: 30px; color: {INK}" dir="rtl"><span>שבת · 10:00</span><span>הכיסא האחרון</span></div>
      <div style="{H}; font-size: 30px; font-weight: 300; color: #4A5642; margin-top: 6px" dir="rtl">המטרפה כבר מחכה על השולחן.</div>
    </div>
  </section>"""

G = [('poudre', '01 · La Poudre', 'לנפות.'), ('chasen', '02 · Le Chasen', 'להקציף.'), ('verre', '03 · Le Verre', 'למזוג.')]
rows = ''.join(f"""<div class="g{i}" style="position: relative; width: 960px; height: 380px; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 44px rgba(31,42,31,.16)">
      <img class="cover" src="a/{f}.webp" alt="">
      <div style="position: absolute; inset: 0; background: linear-gradient(to left, rgba(244,231,213,.95) 30%, rgba(244,231,213,0) 62%)"></div>
      <div style="position: absolute; top: 0; bottom: 0; right: 50px; display: flex; flex-direction: column; justify-content: center; align-items: flex-start; gap: 6px" dir="rtl">
        <span style="font-family: 'Cormorant Garamond', serif; font-size: 34px; color: {MATCHA}" dir="ltr">{fr}</span>
        <span style="{H}; font-size: 78px; font-weight: 600; line-height: 1; color: {INK}">{he}</span></div></div>""" for i, (f, fr, he) in enumerate(G))
C = f"""<section class="scene" data-show="19.2,22.6">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="19.2" style="{K}; margin-bottom: 6px" dir="ltr">Les gestes</div>
      <span class="mask"><span class="c-l1" style="display: block; {H}; font-size: 66px; font-weight: 300; line-height: 1.15; color: {INK}">תשעים דקות. <b style="font-weight: 600; color: {MATCHA}">שלושה מהלכים.</b></span></span>
    </div>
    <div style="position: absolute; top: 480px; left: 60px; display: flex; flex-direction: column; gap: 34px">{rows}</div>
  </section>"""

chip = lambda d, s_, on=False, off=False: (f'<div style="padding: 16px 22px; border-radius: 14px; border: 2px solid {INK if on else "rgba(31,42,31,.16)"}; background: {"#FFFDF8" if on else "transparent"}; opacity: {.45 if off else 1}; display: flex; flex-direction: column; gap: 2px" dir="rtl">'
                                           f'<span style="{H}; font-size: 32px; font-weight: 600; color: {INK}">{d}</span><span style="{H}; font-size: 24px; color: #4A5642; {"text-decoration: line-through" if off else ""}">{s_}</span></div>')
D = f"""<section class="scene" data-show="22.4,26.0">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; top: 205px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <div data-in="22.4" style="{K}; margin-bottom: 6px" dir="ltr">Réserver une place</div>
      <span class="mask"><span class="d-l1" style="display: block; {H}; font-size: 66px; font-weight: 300; line-height: 1.15; color: {INK}">שמרי לך מקום <b style="font-weight: 600; color: {MATCHA}">ליד השולחן.</b></span></span>
    </div>
    <div class="d-form" style="position: absolute; left: 150px; top: 520px; width: 780px; box-sizing: border-box; padding: 44px; border-radius: 22px; background: rgba(255,252,246,.8); border: 2px solid rgba(31,42,31,.12); display: flex; flex-direction: column; gap: 26px" dir="rtl">
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px">{chip('שבת 14.11', 'נשארו 2 מקומות', True)}{chip('שבת 21.11', 'נשארו 4 מקומות')}{chip('שבת 28.11', 'השולחן מלא', off=True)}{chip('שבת 5.12', 'נשארו 5 מקומות')}</div>
      <div style="padding: 20px 24px; border-radius: 14px; border: 2px solid rgba(31,42,31,.14); background: #FFFDF8; {H}; font-size: 32px; color: {INK}">נועה</div>
      <div style="padding: 20px 24px; border-radius: 14px; border: 2px solid rgba(31,42,31,.14); background: #FFFDF8; {H}; font-size: 32px; color: {INK}; text-align: right" dir="ltr">052-1234567</div>
      <div style="display: flex; justify-content: space-between; align-items: baseline; border-top: 2px solid rgba(31,42,31,.12); padding-top: 18px; {H}; font-size: 30px; color: #4A5642"><span>סה״כ</span><b style="font-size: 44px; color: {INK}">₪240</b></div>
      <div style="position: relative; padding: 26px; border-radius: 999px; background: {DEEP}; color: #F4E7D5; text-align: center; {H}; font-size: 36px; font-weight: 600">לשמור את המקום
        <div class="d-tap" style="position: absolute; left: 50%; top: 50%; margin: -45px 0 0 -45px; width: 90px; height: 90px; border-radius: 50%; background: rgba(255,255,255,.45); border: 3px solid #FFFFFF"></div></div>
    </div>
    <div class="d-card" style="position: absolute; left: 190px; top: 640px; width: 700px; box-sizing: border-box; padding: 46px 46px 52px; background: #FBF6EC; border-radius: 10px; box-shadow: 0 40px 80px rgba(31,42,31,.3); display: flex; flex-direction: column; align-items: center; gap: 10px; border-top: 12px solid {MATCHA}">
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 40px; letter-spacing: .22em; color: {INK}" dir="ltr">CHASEN°</div>
      <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 32px; letter-spacing: .2em; color: #4A5642" dir="ltr">La Leçon</div>
      <div style="{H}; font-size: 120px; font-weight: 200; line-height: 1.2; color: {DEEP}" dir="rtl">נועה</div>
      <div style="width: 100%; border-top: 1px solid rgba(31,42,31,.15); border-bottom: 1px solid rgba(31,42,31,.15); padding: 20px 0; display: grid; grid-template-columns: 1fr 1fr; gap: 16px; {H}; font-size: 30px; color: {INK}; text-align: center" dir="rtl"><span>שבת 14.11</span><span>10:00–11:30</span><span>מקום אחד</span><span>כיסא 5</span></div>
      <div style="{H}; font-size: 32px; font-weight: 300; color: #4A5642; margin-top: 8px" dir="rtl">המטרפה כבר מחכה על השולחן.</div>
    </div>
  </section>"""

E = f"""<section class="scene" data-show="25.8,30">
    <div class="stack" style="background: {BG}"></div>
    <div style="position: absolute; left: 190px; top: 470px; width: 700px; height: 880px; border-radius: 350px 350px 30px 30px; overflow: hidden; box-shadow: 0 30px 70px rgba(31,42,31,.2)">
      <img class="cover e-push" src="a/cadeau.webp" alt="The host hands a gift box with a bamboo whisk to a guest" style="object-position: 40% 50%"></div>
    <div data-in="25.9" style="position: absolute; top: 205px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 8px">
      <div style="font-family: 'Cormorant Garamond', serif; font-size: 96px; font-weight: 500; line-height: 1; color: {INK}" dir="ltr">La Leçon</div>
      <div style="{K}; font-size: 36px" dir="ltr">CHASEN° · Bar à Matcha</div>
    </div>
    <div style="position: absolute; bottom: 220px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="e-l1" style="display: block; {H}; font-size: 76px; font-weight: 300; line-height: 1.15; color: {INK}">יוצאות הביתה</span></span>
      <span class="mask"><span class="e-l2" style="display: block; {H}; font-size: 76px; font-weight: 600; line-height: 1.15; color: {MATCHA}">עם המטרפה שהקצפתן בה.</span></span>
    </div>
  </section>"""

i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D, E]) + '\n' + s[j:]
# frame 0 is the feed thumbnail: the question and the flyer are already there
s = s.replace('</style>', '.hq,.hp{animation-name:none!important;opacity:1}\n</style>', 1)
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
open(os.path.join(HERE, 'reel.html'), 'w').write(s)
print('ok', len(s))
