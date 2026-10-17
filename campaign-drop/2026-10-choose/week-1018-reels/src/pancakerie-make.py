# PANCAKERIE° · עולם מותג 26 — studio reel, Wednesday 21.10 (campaign "ככה בוחרים").
# Hook: "הלקוחה בוחרת בעיניים. מה היא רואה אצלך?" · frame 0 = the question + the four dishes on their four colours.
# Reuses the studio wrapper, CSS and reel.js from oreva-price.html (same template, design-system colours).
# Run: python3 pancakerie-make.py  →  pancakerie-eyes.html ; render with the skill's render.js.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'oreva-price.html')).read()
R = '../../../../pancakerie/assets/'
def p(t): return '%.3f%%' % (t / 30 * 100)

head = src[:src.index('<style>')]
head = head.replace('ORÉVA° · עולם מותג 24 — studio reel, Sunday 18.10', 'PANCAKERIE° · עולם מותג 26 — studio reel, Wednesday 21.10')
head = head.replace('<title>ORÉVA° · למה תמיד משווים אותך במחיר?</title>', '<title>PANCAKERIE° · הלקוחה בוחרת בעיניים</title>')
head = head.replace('family=Frank+Ruhl+Libre:wght@400;500&amp;', 'family=Fraunces:opsz,wght@9..144,500;9..144,600&amp;')
css = src[src.index('<style>'):src.index('/* B · ')]
css = css.replace('--w-bg:#F6EFE7; --w-ink:#3A2E29; --w-ink2:#6E5E55; --w-accent:#B87A57; --w-accent-text:#8F5A3C; --w-stone:#D9C7B3;',
                  '--w-bg:#EEE6DA; --w-ink:#402613; --w-ink2:#6B4E3A; --w-accent:#8C6A52; --w-accent-text:#6B4E3A; --w-stone:#E8D8C3;')
marks = src[src.index('<!-- STUDIO · crop marks -->'):src.index('<!-- WORLD -->')]
script = src[src.index('<script>'):]

# the four signatures, in the site's order, with the light tone (--wl) and the mid tone (--c)
D = [('pistache', 'PISTACHE', 'פיסטוק', 'ירוק רך, מלוח-מתוק, והקצפת מרגיעה את הכול.', '#D4CFBA', '#A5A57F', '#402613'),
     ('fraise', 'FRAISE', 'תות', 'הקלאסיקה של שבת בבוקר.', '#E5C9BC', '#D39483', '#402613'),
     ('noisette', 'NOISETTE', 'אגוזי לוז', 'הכי כהה בתפריט. חם, עמוק, ולא מתנצל.', '#523726', '#523726', '#EEE6DA'),
     ('citron', 'CITRON', 'לימון', 'חמוץ שמעיר, מתוק שמרגיע. הבוקר בצהוב.', '#EEDAB7', '#EEC376', '#402613')]
STEPS = [2.6, 6.6, 8.0, 9.4]   # the fan opens the film right after the hook; pistache holds through the studio window            # each colour takes the top of the fan; the ring turns 90° clockwise between them
FAN_CX, FAN_CY, FAN_R = 540, 1880, 330

def kf(name, prop, vals, times, ease=.45):
    out = '0%%,%s{%s:%s}' % (p(times[0]), prop, vals[0])
    for k in range(1, len(vals)):
        out += '%s,%s{%s:%s}' % (p(times[k]), p(times[k + 1] - ease) if k + 1 < len(times) else '100%', prop, vals[k])
    return '@keyframes %s{%s}' % (name, out)

# the fan: discs placed counter-clockwise, the ring rotates clockwise so the next colour arrives at the top
ring_t = [STEPS[0]] + [t - .45 for t in STEPS[1:]]
ring = '0%%,%s{transform:rotate(0deg)}' % p(STEPS[1] - .45)
for k in range(1, 4):
    ring += '%s,%s{transform:rotate(%ddeg)}' % (p(STEPS[k]), p(STEPS[k + 1] - .45) if k < 3 else '100%', 90 * k)
bg = '0%%,%s{background-color:%s}' % (p(STEPS[1] - .45), D[0][4])
fg = '0%%,%s{color:%s}' % (p(STEPS[1] - .45), D[0][6])
for k in range(1, 4):
    end = p(STEPS[k + 1] - .45) if k < 3 else '100%'
    bg += '%s,%s{background-color:%s}' % (p(STEPS[k]), end, D[k][4])
    fg += '%s,%s{color:%s}' % (p(STEPS[k]), end, D[k][6])

# builder (C): base → cream → fruit → cream on top, each falls onto the plate
LAY = [('layer-base', 10.6), ('layer-cream-pistache', 11.3), ('layer-fraises', 12.0), ('layer-chantilly', 12.7)]
drops = ''.join('.drop%d{animation-name:drop%d;animation-timing-function:cubic-bezier(.3,0,.25,1)}@keyframes drop%d{0%%,%s{opacity:0;transform:translateY(-220px)}%s{opacity:1}%s,100%%{opacity:1;transform:none}}'
                % (i, i, i, p(t), p(t + .15), p(t + .5)) for i, (n, t) in enumerate(LAY))

scss = f"""
/* B · La Carte: the fan turns, the plate swaps, the whole frame takes the colour */
.fbg{{animation-name:fbg}}@keyframes fbg{{{bg}}}
.ffg{{animation-name:ffg}}@keyframes ffg{{{fg}}}
.fring{{animation-name:fring;transform-origin:0 0}}@keyframes fring{{{ring}}}
{drops}
.cbg{{animation-name:cbg}}@keyframes cbg{{0%,{p(11.4)}{{background-color:#EEE6DA}}{p(11.8)},100%{{background-color:#D4CFBA}}}}
.kbD{{animation-name:kbD;animation-timing-function:linear}}@keyframes kbD{{0%,{p(18.3)}{{transform:scale(1.04)}}{p(24.3)},100%{{transform:scale(1.14) translateX(-30px)}}}}
.tileimg img{{border-radius:20px}}
.kbE{{animation-name:kbE;animation-timing-function:linear}}@keyframes kbE{{0%,{p(24.0)}{{transform:scale(1.02)}}100%{{transform:scale(1.14)}}}}
"""
css = css.replace('/* E · slow push-in on the hands */\n.kbE{animation-name:kbE;animation-timing-function:linear}\n@keyframes kbE{0%,75%{transform:scale(1.02)}100%{transform:scale(1.12)}}\n', '')
css += scss + '</style>\n</head>\n'

TILE = 'position: absolute; top: 210px; left: 40px; width: 1000px; height: 1260px; border-radius: 20px; overflow: hidden; box-shadow: 0 30px 70px rgba(20,30,45,.16)'
FR = "font-family: 'Fraunces', 'Cormorant Garamond', serif"

intro = f"""<!-- STUDIO · intro -->
<div class="intro stack" style="background: var(--s-bg)">
  <div style="position: absolute; top: 120px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px">
    <div class="i1" style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 500; letter-spacing: .32em; text-transform: uppercase; color: var(--s-copper-text)" dir="ltr">Brand Worlds Studio · Hagit Antebi</div>
    <div class="i2" style="font-size: 100px; font-weight: 500; line-height: 1.05; color: var(--s-ink)" dir="rtl">עולם מותג <em style="font-family: 'Cormorant Garamond', serif; font-weight: 400; color: var(--s-copper)">26</em></div>
  </div>
  <div class="i3" style="position: absolute; top: 1470px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center" dir="rtl">
    <div style="font-size: 64px; font-weight: 600; line-height: 1.15; color: var(--s-ink)">עולם מותג קונספט</div>
    <div style="font-size: 38px; line-height: 1.5; color: var(--s-ink-soft)">לפנקייקרי עם בנאי מנה.</div>
  </div>
</div>

<!-- STUDIO · outro -->
<div class="outro stack" style="background: var(--s-bg)">
  <div style="position: absolute; top: 100px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 16px; text-align: center">
    <div class="o1" style="font-size: 28px; font-weight: 500; letter-spacing: .06em; color: var(--s-copper-text)" dir="rtl">PANCAKERIE° · עולם מותג 26</div>
    <div class="o2" style="font-size: 64px; font-weight: 600; line-height: 1.2; color: var(--s-ink)" dir="rtl">כשרואים את הטעם,<br>בוחרים בך.</div>
  </div>
  <div class="o3" style="position: absolute; top: 1430px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 24px; text-align: center">
    <div style="font-size: 46px; font-weight: 500; line-height: 1.3; color: var(--s-copper-text)" dir="rtl">ומה רואים אצלך<br>לפני הטעימה?</div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 22px 56px; background: var(--s-ink); color: var(--s-bg); border-radius: 12px" dir="rtl"><span style="font-size: 38px; font-weight: 600">אבחון פער המותג</span><span style="font-size: 26px">30 דק׳ · בלי עלות</span></div>
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 500; letter-spacing: .3em; color: var(--s-ink-soft)" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</div>

"""

# A · De la poêle — Verser, Retourner, Napper (the site's scroll film, as three runs)
def run(letter, start, step, a, b, pos):
    return (f'<div class="stack" data-show="{a},{b}" data-fade="0.15"><div class="stack" data-seq="{R}poele/{letter}%02d.webp" data-from="1" data-to="40" data-by="2" '
            f'data-start="{start}" data-step="{step}" data-pos="{pos} 50%"></div></div>')
def cap(fr, he, a, b):
    return (f'<div class="stack" data-show="{a},{b}" data-fade="0.2" style="display: flex; flex-direction: column; align-items: center; gap: 10px; text-align: center">'
            f'<div style="font-family: \'Cormorant Garamond\', serif; font-style: italic; font-size: 64px; line-height: 1; color: var(--w-ink)" dir="ltr">{fr}</div>'
            f'<div style="font-size: 44px; font-weight: 500; color: var(--w-ink2)" dir="rtl">{he}</div></div>')
A = f"""  <section class="scene" data-show="14.3,18.6" style="background: var(--w-bg)">
    <div class="tileimg" style="position: absolute; top: 210px; left: 40px; width: 1000px; height: 1260px; border-radius: 20px; box-shadow: 0 30px 70px rgba(20,30,45,.16)">{run('a', 14.3, .07, 14.3, 15.75, '38%')}{run('b', 15.7, .07, 15.6, 17.15, '45%')}{run('c', 17.1, .07, 17.0, 18.6, '62%')}</div>
    <div style="position: absolute; top: 1530px; left: 80px; right: 80px; height: 180px">
      {cap('Verser', 'מוזגים. בצק אחד, מהכד למחבת.', 14.3, 15.6)}{cap('Retourner', 'הופכים. פעם אחת.', 15.75, 16.95)}{cap('Napper', 'מזלפים. מכאן מתחיל הצבע.', 17.15, 18.6)}
    </div>
  </section>
"""

# B · La Carte — the colour fan (signature)
discs = ''.join(f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-90 * i}deg) translateY(-{FAN_R}px) rotate({90 * i}deg)">'
                f'<div style="position: absolute; left: -92px; top: -92px; width: 184px; height: 184px; border-radius: 50%; background: {d[5]}; box-shadow: 0 0 0 6px #FFFFFF, 0 16px 34px rgba(20,30,45,.2)"></div></div>'
                for i, d in enumerate(D))
dishes = ''.join(f'<div class="stack" data-show="{STEPS[i] if i else 0},{STEPS[i + 1] if i < 3 else 10.6}" data-fade="0.3">'
                 f'<img src="{R}dish-{d[0]}.webp" alt="" style="position: absolute; left: 40px; top: 470px; width: 1000px; height: 750px; display: block"></div>'
                 for i, d in enumerate(D))
names = ''.join(f'<div class="stack" data-show="{STEPS[i] + .15 if i else 0},{STEPS[i + 1] - .35 if i < 3 else 10.6}" data-fade="0.2" style="display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center">'
                f'<div style="{FR}; font-size: 72px; font-weight: 600; letter-spacing: .08em; line-height: 1" dir="ltr">{d[1]}</div>'
                f'<div style="font-size: 36px" dir="rtl">{d[2]} · {d[3]}</div></div>'
                for i, d in enumerate(D))
B = f"""  <section class="scene" data-show="0,10.6">
    <div class="stack fbg"></div>
    <div class="ffg" style="position: absolute; top: 200px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center" dir="rtl">
      <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 44px" dir="ltr">Les Signatures</div>
      <div style="font-size: 68px; font-weight: 600; line-height: 1.15">ארבע מנות.<br>כל אחת בצבע שלה.</div>
    </div>
    {dishes}
    <div class="ffg" style="position: absolute; top: 1230px; left: 60px; right: 60px; height: 150px">{names}</div>
    <div class="fring" style="position: absolute; left: {FAN_CX}px; top: {FAN_CY}px; width: 0; height: 0">{discs}</div>
    <div style="position: absolute; left: 522px; top: {FAN_CY - FAN_R - 92 - 40}px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid #FFFFFF"></div>
  </section>
"""

# C · L'Atelier — choose the colour, get the dish
chips = ''.join(f'<span data-in="{t:.1f}" style="padding: 14px 26px; border-radius: 999px; border: 3px solid var(--w-accent); background: #FFFFFF; font-size: 30px; font-weight: 600; color: var(--w-ink)">{lab}</span>'
                for lab, (n, t) in zip(['01 · הבסיס', '02 · הקרם', '03 · הפרי', '04 · התוספות'], LAY))
layers = ''.join(f'<img class="drop{i}" src="{R}{n}.webp" alt="" style="position: absolute; left: 0; top: 0; width: 1000px; height: 750px; display: block">'
                 for i, (n, t) in enumerate(LAY))
C = f"""  <section class="scene" data-show="10.3,14.6">
    <div class="stack cbg"></div>
    <div style="position: absolute; top: 200px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 6px; text-align: center" dir="rtl">
      <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 44px; color: var(--w-accent-text)" dir="ltr">L'Atelier</div>
      <div style="font-size: 72px; font-weight: 600; line-height: 1.15; color: var(--w-ink)">בוחרים צבע.<br>מקבלים מנה.</div>
    </div>
    <div style="position: absolute; left: 40px; top: 560px; width: 1000px; height: 750px">{layers}</div>
    <div style="position: absolute; top: 1420px; left: 50px; right: 50px; display: flex; justify-content: space-between" dir="rtl">{chips}</div>
    <div data-in="13.0" style="position: absolute; top: 1580px; left: 70px; right: 70px; text-align: center; font-size: 40px; color: var(--w-ink2)" dir="rtl">הצבע של הקרם הוא הצבע של המנה.</div>
  </section>
"""

# D · La Boîte — one box takes the colour of each signature, in the fan's order (box images: Kling, 17.10)
BOX = [('pistache', 18.3, 19.6), ('fraise', 19.6, 20.9), ('noisette', 20.9, 22.2), ('citron', 22.2, 24.3)]
boxes = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.3"><img src="kling-out/box-{n}.jpg" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; border-radius: 20px; display: block"></div>'
                for n, a, b in BOX)
pills = ''.join(f'<div class="stack" data-show="{a + .1:.1f},{b - .15:.2f}" data-fade="0.2" style="display: flex; justify-content: center"><span style="padding: 14px 34px; border-radius: 999px; background: {d[5]}; color: {"#EEE6DA" if d[0] == "noisette" else "#402613"}; font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 26px; font-weight: 500; letter-spacing: .28em" dir="ltr">{d[1]}</span></div>'
                for (n, a, b), d in zip(BOX, D))
Dsc = f"""  <section class="scene" data-show="18.3,24.3" style="background: var(--w-bg)">
    <div style="position: absolute; top: 220px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center" dir="rtl">
      <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 44px; color: var(--w-accent-text)" dir="ltr">La Boîte</div>
      <div style="font-size: 72px; font-weight: 600; line-height: 1.15; color: var(--w-ink)">הצבע יוצא איתך.</div>
    </div>
    <div style="position: absolute; top: 470px; left: 40px; width: 1000px; height: 750px; border-radius: 20px; box-shadow: 0 30px 70px rgba(20,30,45,.16)">{boxes}</div>
    <div style="position: absolute; top: 1270px; left: 0; right: 0; height: 80px">{pills}</div>
    <div style="position: absolute; top: 1400px; left: 70px; right: 70px; text-align: center; font-size: 38px; line-height: 1.4; color: var(--w-ink2)" dir="rtl">הקופסה, הכוס והשקית<br>יוצאים בצבע של המנה שבחרת.</div>
  </section>
"""

# E · Le Moment — the promise
E = f"""  <section class="scene" data-show="24.0,30" style="background: var(--w-bg)">
    <div style="{TILE}"><img class="kbE" src="{R}moment.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: 48% 50%; display: block"></div>
    <div style="position: absolute; top: 1540px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center" dir="rtl">
      <div style="font-size: 72px; font-weight: 600; line-height: 1.2; color: var(--w-ink)">טעם שרואים<br>לפני שטועמים.</div>
      <div style="{FR}; font-size: 40px; font-weight: 500; letter-spacing: .06em; color: var(--w-accent-text)" dir="ltr">PANCAKERIE° · Morning Patisserie</div>
    </div>
  </section>
"""

world = ('<!-- WORLD -->\n<div class="world stack" style="overflow: hidden; background: var(--w-bg); box-shadow: 0 50px 140px rgba(20,30,45,.22)">\n'
         + A + B + C + Dsc + E + '</div>\n\n')

# HOOK — frame 0 already shows the question and the four dishes on their four colours
tiles = ''.join(f'<div style="position: relative; height: 400px; border-radius: 20px; background: {d[5]}; overflow: hidden; box-shadow: 0 18px 40px rgba(20,30,45,.14)">'
                f'<img src="{R}dish-{d[0]}.webp" alt="" style="position: absolute; left: -10px; top: 10px; width: 460px; height: 345px">'
                f'<div style="position: absolute; bottom: 18px; left: 0; right: 0; text-align: center; font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 22px; font-weight: 500; letter-spacing: .3em; color: {d[6]}" dir="ltr">{d[1]}</div></div>'
                for d in [D[1], D[0], D[3], D[2]])
hook = f"""<!-- HOOK (0–2.8) -->
<div class="hook stack" style="background: var(--s-cream)">
  <div style="position: absolute; top: 88px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 36px; color: var(--s-ink)" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size: 18px; letter-spacing: .3em; color: var(--s-ink-soft)">חגית אנטבי</div>
  </div>
  <div style="position: absolute; top: 240px; left: 80px; right: 80px; text-align: right; font-size: 84px; font-weight: 600; line-height: 1.16; color: var(--s-ink)" dir="rtl">הלקוחה בוחרת<br>בעיניים. מה היא<br><span style="color: var(--s-copper)">רואה</span> אצלך?</div>
  <div style="position: absolute; top: 640px; left: 80px; right: 80px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px">{tiles}</div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line ln0" pathLength="1" d="M1140 1610 H540"></path></svg>
  <div class="ball bl0" style="offset-path: path('M1140 1610 H540')"><div class="halo"></div><div class="sph"><div class="rl0"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>
  <div style="position: absolute; bottom: 110px; left: 0; right: 0; text-align: center; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 500; letter-spacing: .3em; color: var(--s-ink-soft)" dir="ltr">HAGITANTEBI.CO.IL</div>
</div>

"""

hudrows = [('01 · La Carte', 'ארבע מנות, ארבעה צבעים.', 5.6, 10.4), ("02 · L'Atelier", 'בוחרים צבע. מקבלים מנה.', 10.4, 14.4),
           ('03 · De la poêle', 'מוזגים, הופכים, מזלפים.', 14.4, 18.4), ('04 · La Boîte', 'הצבע יוצא איתך.', 18.4, 24.1), ('05 · The Promise', 'טעם שרואים לפני שטועמים.', 24.1, 30)]
hud = ('<!-- STUDIO · layer tag -->\n<div class="hud" style="position: absolute; top: 40px; right: 40px; width: 540px; height: 132px; box-sizing: border-box; padding: 18px 26px; background: rgba(242,235,220,.94); border: 1px solid var(--s-copper-soft); display: flex; flex-direction: column; gap: 6px" dir="rtl">\n'
       '  <div style="font-size: 18px; font-weight: 500; letter-spacing: .04em; color: var(--s-copper-text)">Brand Worlds Studio · עולם מותג 26</div>\n  <div style="position: relative; flex-grow: 1">\n'
       + ''.join(f'    <div class="stack" data-show="{a},{b}" data-fade="0.2" style="display: flex; flex-direction: column; gap: 2px"><span style="font-family: \'Cormorant Garamond\', serif; font-size: 34px; line-height: 1; color: var(--s-ink)" dir="ltr">{n}</span><span style="font-size: 22px; color: var(--s-ink)">{l}</span></div>\n' for n, l, a, b in hudrows)
       + '  </div>\n</div>\n\n<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: rgba(194,138,90,.2)"><div class="progress" style="height: 6px; background: var(--s-copper)"></div></div>\n</div>\n</div>\n\n')

page = head + css + '<body data-duration="30">\n<div id="stage">\n<div class="film stack">\n\n' + intro + marks + world + hook + hud + script
open(os.path.join(HERE, 'pancakerie-eyes.html'), 'w').write(page)
print('ok', len(page))
