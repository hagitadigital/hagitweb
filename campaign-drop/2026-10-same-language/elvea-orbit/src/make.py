# ELVÉA° · "אותה שפה" — 20s studio reel: hook → leaf portal → five cards orbiting the bottle → the line closes → outro.
# Writes orbit.html next to this file. Every time is in seconds; P() turns it into a keyframe percentage.
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
D = 20.0
def P(t): return '%.3f%%' % (max(0, min(D, t)) / D * 100)

# ELVÉA palette (elvea/index.html :root)
CREAM, LINEN, SAND, SAGE, OLIVE, OLIVE_D, INK, INK_S, NECTAR = '#F0EADD', '#F7F3E9', '#E5DBC8', '#B9C1A2', '#55613F', '#3E4930', '#2E3526', '#5D6550', '#E9DABC'
HE = "font-family: 'Heebo', sans-serif"
AS = "font-family: 'Assistant', sans-serif"
CG = "font-family: 'Cormorant Garamond', serif"

# ── orbit geometry ──
CX, CY = 540, 910          # centre of the world circle
RC = 220                   # circle radius
R, KY = 410, .95           # orbit radius, vertical squash (camera slightly above)
CW, CH = 300, 400          # card size
STOPS = [5.1, 7.1, 9.1, 11.1, 13.1]   # card k reaches the front at STOPS[k]; each turn takes TURN before it
TURN = .6
FIN = (14.9, 15.6)         # last turn: a full circle back to the site
OUT = 16.9                 # world shrinks into the studio window

def ease(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
def theta(t):              # ring angle in degrees; card i sits at theta + 72 i, 0 = front
    if t < 4.2: return -150
    if t < STOPS[0]: return -150 + 150 * ease((t - 4.2) / (STOPS[0] - 4.2))
    a = 0
    for k in range(1, 5):
        a -= 72 * ease((t - (STOPS[k] - TURN)) / TURN)
    a -= 72 * ease((t - FIN[0]) / (FIN[1] - FIN[0]))
    if t > OUT: a -= 24 * (t - OUT) / (D - OUT)       # slow drift in the outro
    return a
def radius(t): return R * ease((t - 4.2) / (STOPS[0] - 4.2 - .1))
def active(i, t):          # 0..1 emphasis of card i while it holds the front
    if i == 0: a, b = STOPS[0] - .2, STOPS[1] - TURN
    else: a, b = STOPS[i], (STOPS[i + 1] - TURN) if i < 4 else FIN[0]
    return min(ease((t - a + .25) / .35), 1 - ease((t - b) / .3))

cards_css = []
for i in range(5):
    kf = []
    n = int(D * 15)
    for f in range(n + 1):
        t = f / 15
        ph = math.radians(theta(t) + 72 * i)
        r = radius(t)
        x, y = CX - r * math.sin(ph), CY + r * KY * math.cos(ph)
        d = math.cos(ph)
        s = (.6 + .4 * (d + 1) / 2) * (1 + .15 * active(i, t)) * (min(1, r / R) * .9 + .1)
        z = int(round(50 + 40 * d)) if r > 10 else 40
        kf.append('%.3f%%{transform:translate(%.1fpx,%.1fpx) scale(%.4f);z-index:%d}' % (t / D * 100, x, y, s, z))
    cards_css.append('.card%d{animation-name:card%d;animation-timing-function:linear}@keyframes card%d{%s}' % (i, i, i, ''.join(kf)))
dim = []
for i in range(5):        # cards that are not in front sit back a little
    kf = []
    for f in range(int(D * 15) + 1):
        t = f / 15
        d = math.cos(math.radians(theta(t) + 72 * i))
        o = .55 + .45 * (d + 1) / 2
        kf.append('%.3f%%{opacity:%.3f}' % (t / D * 100, o))
    dim.append('.dim%d{animation-name:dim%d;animation-timing-function:linear}@keyframes dim%d{%s}' % (i, i, i, ''.join(kf)))

# the green line around the orbit draws one fifth per stop and closes on the last turn
ring_kf = '0%%,%s{stroke-dashoffset:1}%s{stroke-dashoffset:.8}' % (P(4.6), P(STOPS[0]))
for k in range(1, 5):
    ring_kf += '%s{stroke-dashoffset:%.2f}%s{stroke-dashoffset:%.2f}' % (P(STOPS[k] - TURN), .8 - .2 * (k - 1), P(STOPS[k]), .8 - .2 * k)
ring_kf += '%s{stroke-dashoffset:0}100%%{stroke-dashoffset:0}' % P(FIN[1])

def show(a, b, f=.3):     # opacity window
    s = '0%{opacity:1}' if a <= 0 else '0%%,%s{opacity:0}%s{opacity:1}' % (P(a - f), P(a))
    e = '100%{opacity:1}' if b >= D else '%s{opacity:1}%s,100%%{opacity:0}' % (P(b), P(b + f))
    return s + e
def rise(t, dy=30): return '0%%,%s{opacity:0;transform:translateY(%dpx)}%s,100%%{opacity:1;transform:none}' % (P(t), dy, P(t + .5))
NK = [0]
def anim(kf, extra=''):
    NK[0] += 1; k = 'k%d' % NK[0]
    CSS.append('@keyframes %s{%s}' % (k, kf)); return 'animation-name:%s;%s' % (k, extra)
CSS = []

# ── leaf portal (recipe 6), ending at the circle's centre ──
LEAF_A = 'M1140 1690 L1000 1560 C1050 1330 900 1030 540 910'
LEAF_B = 'M1140 1690 L1000 1560 C760 1520 560 1250 540 910'

# ── card faces (300×400) ──
face = "position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: 22px; overflow: hidden; box-shadow: 0 26px 60px rgba(46,53,38,.22)" % (-CW // 2, -CH // 2, CW, CH)
SYM = f'''<svg viewBox="30 20 260 380" width="96" height="140" aria-hidden="true" style="display: block"><g fill="none" stroke="{OLIVE}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
<path d="M62,58 C152,50 196,118 201,198 C120,196 68,140 62,58 Z M74,70 C122,108 166,150 194,188"/><path d="M212,212 C244,252 266,282 266,312 A55,55 0 1 1 156,312 C156,282 178,252 212,212 Z"/></g><circle cx="206" cy="205" r="9" fill="#C4765A"/></svg>'''
FACES = [
    # 01 · the site (a real mobile screenshot of elvea/)
    f'''<div style="{face}; background: #FFFFFF; padding: 10px; box-sizing: border-box">
      <div style="position: relative; width: 100%; height: 100%; border-radius: 14px; overflow: hidden"><img src="media/site.jpg" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 78%; display: block"></div></div>''',
    # 02 · the feed (Le Fil Vert, first slide)
    f'''<div style="{face}; background: #FFFFFF; display: flex; flex-direction: column">
      <div style="height: 50px; display: flex; align-items: center; gap: 10px; padding: 0 14px" dir="ltr"><span style="width: 30px; height: 30px; border-radius: 50%; background: {OLIVE}; color: {LINEN}; display: flex; align-items: center; justify-content: center; {CG}; font-size: 18px">E</span><span style="{AS}; font-size: 17px; font-weight: 600; color: {INK}">elvea.skin</span><span style="margin-left: auto; {AS}; font-size: 20px; color: {INK_S}">···</span></div>
      <div style="position: relative; flex-grow: 1; overflow: hidden"><img src="media/fil-01.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 40%; display: block"><span style="position: absolute; top: 10px; right: 10px; padding: 3px 10px; border-radius: 999px; background: rgba(46,53,38,.6); color: #FFFFFF; {AS}; font-size: 14px" dir="ltr">1/5</span></div>
      <div style="height: 46px; display: flex; align-items: center; padding: 0 14px; gap: 14px" dir="ltr"><svg width="22" height="20" viewBox="0 0 24 22"><path d="M12 20 C4 14 1 10 1 6.5 A5.5 5.5 0 0 1 12 4 A5.5 5.5 0 0 1 23 6.5 C23 10 20 14 12 20Z" fill="#C4765A"/></svg><svg width="22" height="22" viewBox="0 0 24 24"><path d="M21 12a9 9 0 1 1-4-7.5L21 3l-1 4.5A9 9 0 0 1 21 12z" fill="none" stroke="{INK}" stroke-width="1.8"/></svg>
        <span style="margin-left: auto; margin-right: auto; display: flex; gap: 5px"><i style="width: 7px; height: 7px; border-radius: 50%; background: {OLIVE}"></i><i style="width: 7px; height: 7px; border-radius: 50%; background: {SAGE}"></i><i style="width: 7px; height: 7px; border-radius: 50%; background: {SAGE}"></i><i style="width: 7px; height: 7px; border-radius: 50%; background: {SAGE}"></i><i style="width: 7px; height: 7px; border-radius: 50%; background: {SAGE}"></i></span><span style="width: 36px"></span></div></div>''',
    # 03 · the language: the symbol and the sentence
    f'''<div style="{face}; background: {LINEN}; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; border: 1.5px solid {SAGE}; box-sizing: border-box">
      {SYM}
      <div style="{CG}; font-size: 40px; letter-spacing: .12em; color: {INK}" dir="ltr">ELVÉA°</div>
      <div style="{AS}; font-size: 25px; line-height: 1.35; color: {INK}; text-align: center; padding: 0 20px" dir="rtl">הטבע מתחיל את הסיפור.<br><b style="font-weight: 600; color: {OLIVE}">הפורמולה משלימה אותו.</b></div></div>''',
    # 04 · the colours
    f'''<div style="{face}; display: flex; flex-direction: column">''' + ''.join(
        f'<div style="flex: 1; background: {c}; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; {AS}; font-size: 17px; letter-spacing: .08em; color: {fg}" dir="ltr"><span>{n}</span><span>{c}</span></div>'
        for n, c, fg in [('OLIVE DEEP', OLIVE_D, LINEN), ('OLIVE', OLIVE, LINEN), ('SAGE', SAGE, INK), ('NECTAR', NECTAR, INK), ('CREAM', CREAM, INK)]) + '</div>',
    # 05 · the packaging
    f'''<div style="{face}; background: {CREAM}"><img src="media/gift-set.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 50%; display: block"></div>''',
]
LABELS = [('01', 'האתר', 'הפרח והטיפה נפגשים בגלילה.'),
          ('02', 'הפיד', 'חמישה שקפים. קו אחד רציף.'),
          ('03', 'השפה', 'עלה, טיפה, ונקודת המפגש ביניהם.'),
          ('04', 'הצבעים', 'זית, מרווה, נקטר ושמנת.'),
          ('05', 'האריזה', 'אותו קו על המארז, על התווית ועל השקית.')]
lab_win = [(STOPS[0] - .3, STOPS[1] - TURN)] + [(STOPS[k], (STOPS[k + 1] - TURN) if k < 4 else FIN[0]) for k in range(1, 5)]

cards = ''.join(f'<div class="card{i}" style="position: absolute; left: 0; top: 0; width: 0; height: 0"><div class="dim{i}">{FACES[i]}</div></div>' for i in range(5))
labels = ''.join(f'''<div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; gap: 6px; {anim(show(a, b, .25))}">
      <div style="{HE}; font-size: 60px; font-weight: 600; line-height: 1.1; color: {OLIVE_D}" dir="rtl"><span style="{CG}; font-weight: 500; color: #C4765A">{n}</span> · {h}</div>
      <div style="{HE}; font-size: 34px; font-weight: 300; color: {INK_S}" dir="rtl">{s}</div></div>''' for (n, h, s), (a, b) in zip(LABELS, lab_win))

WORLD = f'''<div class="world" style="position: absolute; inset: 0; overflow: hidden; background: radial-gradient(ellipse 70% 45% at 50% 50%, {LINEN} 0%, {CREAM} 70%); box-shadow: 0 50px 140px rgba(46,53,38,.26)">
  <div style="position: absolute; inset: 0; background: {CREAM}; {anim('0%,' + P(3.9) + '{opacity:1}' + P(4.5) + ',100%{opacity:0}')}"></div>
  <!-- the orbit line, behind everything -->
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <ellipse cx="{CX}" cy="{CY}" rx="{R}" ry="{R * KY:.0f}" fill="none" stroke="{SAGE}" stroke-width="2" stroke-dasharray="3 10" style="{anim(show(4.8, D, .5))}"/>
    <path d="M{CX} {CY + R * KY:.0f} A{R} {R * KY:.0f} 0 0 1 {CX} {CY - R * KY:.0f} A{R} {R * KY:.0f} 0 0 1 {CX} {CY + R * KY:.0f}" pathLength="1" fill="none" stroke="{OLIVE}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 1" style="{anim(ring_kf, 'animation-timing-function:linear')}"/>
  </svg>
  <!-- the circle: ELVÉA's bottle -->
  <div style="position: absolute; left: {CX - RC}px; top: {CY - RC}px; width: {2 * RC}px; height: {2 * RC}px; z-index: 50; {anim('0%,' + P(3.45) + '{clip-path:circle(0 at 50% 50%)}' + P(4.15) + ',100%{clip-path:circle(50% at 50% 50%)}', 'animation-timing-function:cubic-bezier(.3,0,.2,1)')}">
    <div style="position: absolute; inset: 0; border-radius: 50%; overflow: hidden; background: {CREAM}; box-shadow: inset 0 0 0 4px {LINEN}">
      <img src="media/hero-7-bottle.webp" alt="ELVÉA° bottle" style="position: absolute; left: -335px; top: -12px; width: 830px; height: 467px; display: block; {anim('0%,' + P(3.5) + '{transform:scale(1.25)}' + P(5) + ',100%{transform:none}')}">
    </div>
    <div style="position: absolute; inset: -10px; border-radius: 50%; border: 3px solid {OLIVE}; {anim(show(4.1, D, .4))}"></div>
  </div>
  <div style="position: absolute; left: 0; top: 0; z-index: 60; {anim(show(4.2, D, .2))}">{cards}</div>
  <!-- header: the site's own line -->
  <div style="position: absolute; top: 150px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; z-index: 95; {anim(rise(4.3))}">
    <div style="{CG}; font-size: 30px; font-weight: 500; letter-spacing: .3em; color: {OLIVE}" dir="ltr">ELVÉA° · BOTANICAL SKIN SCIENCE</div>
    <div style="margin-top: 14px; {HE}; font-size: 66px; font-weight: 300; line-height: 1.15; color: {INK}" dir="rtl">עולם שלם,<br><b style="font-weight: 600; color: {OLIVE}">באותו קו ובאותם צבעים.</b></div>
  </div>
  <div style="position: absolute; top: 1610px; left: 40px; right: 40px; height: 160px; z-index: 95">{labels}
    <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; gap: 8px; {anim(show(FIN[0] + .35, D, .3))}">
      <div style="{HE}; font-size: 54px; font-weight: 600; color: {OLIVE_D}" dir="rtl">אתר · פיד · שפה · צבעים · אריזה</div>
      <div style="{HE}; font-size: 36px; font-weight: 300; color: {INK_S}" dir="rtl">קו אחד עובר דרך כולם.</div></div>
  </div>
</div>'''

# ── HOOK (0–2.6s): frame 0 already shows the question and the three mismatched generic pieces ──
GEN_SITE = f'''<div style="position: absolute; left: 70px; top: 700px; width: 470px; height: 380px; transform: rotate(-6deg); background: #FFFFFF; border-radius: 10px; overflow: hidden; box-shadow: 0 24px 50px rgba(62,47,37,.18); font-family: Arial, sans-serif">
    <div style="height: 34px; background: #E4E7EB; display: flex; align-items: center; gap: 7px; padding: 0 12px"><i style="width: 10px; height: 10px; border-radius: 50%; background: #F26B5B"></i><i style="width: 10px; height: 10px; border-radius: 50%; background: #F6BE3B"></i><i style="width: 10px; height: 10px; border-radius: 50%; background: #3FC25B"></i><span style="margin-left: 10px; flex-grow: 1; height: 16px; border-radius: 8px; background: #FFFFFF"></span></div>
    <div style="height: 54px; background: #1F6FB2; display: flex; align-items: center; justify-content: space-between; padding: 0 18px" dir="rtl"><span style="padding: 4px 14px; border: 2px solid #FFFFFF; color: #FFFFFF; font-weight: 700; font-size: 18px">LOGO</span><span style="display: flex; gap: 12px"><i style="width: 40px; height: 8px; background: rgba(255,255,255,.7)"></i><i style="width: 40px; height: 8px; background: rgba(255,255,255,.7)"></i><i style="width: 40px; height: 8px; background: rgba(255,255,255,.7)"></i></span></div>
    <div style="display: flex; height: 292px" dir="rtl"><div style="width: 50%; padding: 26px 20px; box-sizing: border-box; display: flex; flex-direction: column; gap: 12px"><b style="font-size: 30px; line-height: 1.1; color: #1B1B1B">טיפוח מקצועי לעור שלך!</b><i style="height: 8px; background: #D7DADF"></i><i style="height: 8px; width: 80%; background: #D7DADF"></i><span style="align-self: flex-start; margin-top: 8px; padding: 10px 18px; background: #F39C12; color: #FFFFFF; font-weight: 700; font-size: 17px; border-radius: 4px">קני עכשיו</span></div>
      <img src="media/generic-serum.jpg" alt="" style="width: 50%; height: 100%; object-fit: cover; display: block"></div></div>'''
GEN_POST = f'''<div style="position: absolute; left: 600px; top: 640px; width: 400px; height: 470px; transform: rotate(5deg); background: #FFFFFF; border-radius: 14px; overflow: hidden; box-shadow: 0 24px 50px rgba(62,47,37,.18)">
    <div style="height: 50px; display: flex; align-items: center; gap: 10px; padding: 0 14px; font-family: Arial, sans-serif" dir="ltr"><span style="width: 30px; height: 30px; border-radius: 50%; background: #D7DADF"></span><b style="font-size: 16px; color: #222">your.business</b></div>
    <div style="position: relative; height: 420px; background: #F7C6D9; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px">
      <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 76px; line-height: .95; color: #D6246E; text-align: center">MEGA<br>SALE</div>
      <div style="font-family: Arial, sans-serif; font-weight: 700; font-size: 36px; color: #FFFFFF; background: #222; padding: 4px 16px; transform: rotate(-3deg)">-20% 🔥</div>
      <div style="font-family: Arial, sans-serif; font-size: 22px; color: #6B2847" dir="rtl">על כל מוצרי הטיפוח</div></div></div>'''
GEN_BOX = f'''<div style="position: absolute; left: 300px; top: 1170px; width: 480px; height: 300px; transform: rotate(-2deg)">
    <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 230px; background: linear-gradient(160deg, #C9A57A, #B08A5E); border-radius: 6px; box-shadow: 0 24px 50px rgba(62,47,37,.22)"></div>
    <div style="position: absolute; left: 0; right: 0; top: 20px; height: 70px; background: linear-gradient(180deg, #D8B78C, #C29C70); border-radius: 6px 6px 0 0; transform: skewX(-8deg)"></div>
    <div style="position: absolute; left: 150px; top: 135px; width: 180px; height: 96px; background: #FFFFFF; border: 3px solid #222; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: Georgia, serif; font-weight: 700; color: #222"><span style="font-size: 28px; letter-spacing: .1em">LOGO</span><span style="font-family: Arial, sans-serif; font-size: 13px; font-weight: 400">Thank you for your order!</span></div></div>'''
def tag(x, y, txt): return f'<span style="position: absolute; left: {x}px; top: {y}px; padding: 8px 20px; border-radius: 999px; background: #3E2F25; color: #FAF8F3; {HE}; font-size: 26px; font-weight: 500" dir="rtl">{txt}</span>'
HOOK = f'''<div style="position: absolute; inset: 0; background: #EEE6D8; z-index: 200; {anim('0%,' + P(2.45) + '{opacity:1}' + P(2.85) + ',100%{opacity:0}')}">
  <div style="position: absolute; top: 88px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div style="{CG}; font-style: italic; font-size: 36px; color: #3E2F25" dir="ltr">Brand Worlds Studio</div>
    <div style="{HE}; font-size: 17px; letter-spacing: .3em; color: #8B7B6E">חגית אנטבי</div></div>
  <div style="position: absolute; top: 250px; left: 70px; right: 70px; text-align: right; {HE}; font-size: 80px; font-weight: 600; line-height: 1.16; color: #3E2F25" dir="rtl">האתר, הפוסט והאריזה שלך<br>נראים כמו <span style="color: #C4765A">אותו מותג</span>?</div>
  <div style="position: absolute; inset: 0; {anim('0%{transform:none}' + P(2.5) + '{transform:scale(1.03)}100%{transform:scale(1.03)}', 'animation-timing-function:linear')}">
    {GEN_SITE}{GEN_POST}{GEN_BOX}
    {tag(110, 650, 'האתר')}{tag(840, 590, 'הפוסט')}{tag(640, 1440, 'האריזה')}
  </div>
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line" pathLength="1" d="M1140 1690 C900 1700 760 1600 540 1640" style="{anim('0%,' + P(.2) + '{stroke-dashoffset:1}' + P(2.2) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:linear')}"/></svg>
  {{BALL:M1140 1690 C900 1700 760 1600 540 1640:0.2:2.2}}
  <div style="position: absolute; top: 1730px; left: 0; right: 0; text-align: center; {HE}; font-size: 34px; font-weight: 300; color: #6B563F; {anim('0%,' + P(.9) + '{opacity:0}' + P(1.3) + ',100%{opacity:1}')}" dir="rtl">שלושה מקומות. שלוש שפות.</div>
</div>'''

def ball(path, a, b):
    k1 = anim('0%%,%s{offset-distance:0%%;opacity:%s}%s{offset-distance:0%%;opacity:1}%s{offset-distance:100%%;opacity:1}%s,100%%{offset-distance:100%%;opacity:0}' % (P(a - .01), '1' if a <= .2 else '0', P(a), P(b), P(b + .25)), 'animation-timing-function:cubic-bezier(.45,0,.4,1)')
    k2 = anim('0%%,%s{transform:rotate(0deg)}%s,100%%{transform:rotate(-400deg)}' % (P(a), P(b)), 'animation-timing-function:cubic-bezier(.45,0,.4,1)')
    return f'''<div class="ball" style="offset-path: path('{path}'); {k1}"><div class="halo"></div><div class="sph"><div style="position: absolute; inset: 0; {k2}"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; {CG}; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>'''
import re
def fill_balls(s):
    return re.sub(r'\{BALL:([^:]+):([\d.]+):([\d.]+)\}', lambda m: ball(m.group(1), float(m.group(2)), float(m.group(3))), s)
HOOK = fill_balls(HOOK)

# ── studio intro (2.6–4.3): the leaf lines meet in the centre and open the circle ──
INTRO = f'''<div style="position: absolute; inset: 0; z-index: 150; pointer-events: none">
  <div style="position: absolute; top: 120px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px; {anim(show(2.65, 4.05, .3))}">
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 500; letter-spacing: .32em; color: #C4765A" dir="ltr">BRAND WORLDS STUDIO · HAGIT ANTEBI</div>
    <div style="{HE}; font-size: 96px; font-weight: 500; line-height: 1.05; color: #6B563F" dir="rtl">עולם מותג <em style="{CG}; font-weight: 400; color: #B8894A">14</em></div></div>
  <div style="position: absolute; top: 1480px; left: 80px; right: 80px; text-align: center; {HE}; font-size: 44px; font-weight: 400; line-height: 1.35; color: #6B563F; {anim(show(2.8, 4.05, .3))}" dir="rtl">טיפוח בוטני־מדעי.<br>עלה וטיפה שנפגשים בעור.</div>
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <g style="{anim(show(2.6, 4.0, .3))}">
    <path class="line" pathLength="1" d="{LEAF_A}" style="{anim('0%,' + P(2.75) + '{stroke-dashoffset:1}' + P(3.55) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:cubic-bezier(.4,0,.3,1)')}"/>
    <path class="line" pathLength="1" d="{LEAF_B}" style="stroke: {OLIVE}; {anim('0%,' + P(2.75) + '{stroke-dashoffset:1}' + P(3.55) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:cubic-bezier(.4,0,.3,1)')}"/>
    </g>
    <circle cx="{CX}" cy="{CY}" r="40" fill="none" stroke="#C4765A" stroke-width="3" style="transform-origin: {CX}px {CY}px; {anim('0%,' + P(3.5) + '{opacity:0;transform:scale(1)}' + P(3.6) + '{opacity:1}' + P(4.3) + '{opacity:.0;transform:scale(7)}100%{opacity:0;transform:scale(7)}')}"/>
  </svg>
  {{BALL:{LEAF_A}:2.75:3.55}}
  <div style="position: absolute; left: 0; top: 0; width: 34px; height: 34px; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #E6EDD6, {OLIVE} 70%); offset-path: path('{LEAF_B}'); offset-rotate: 0deg; {anim('0%,' + P(2.74) + '{offset-distance:0%;opacity:0}' + P(2.75) + '{opacity:1;offset-distance:0%}' + P(3.55) + '{offset-distance:100%;opacity:1}' + P(3.75) + ',100%{offset-distance:100%;opacity:0}', 'animation-timing-function:cubic-bezier(.4,0,.3,1)')}"></div>
</div>'''
INTRO = fill_balls(INTRO)

# ── outro (16.9–20): the world sits in the studio window; the answer + CTA; holds to the last frame ──
OUTRO = f'''<div style="position: absolute; inset: 0; z-index: 150; pointer-events: none">
  <div style="position: absolute; top: 100px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
    <div style="{HE}; font-size: 28px; font-weight: 500; letter-spacing: .06em; color: #C4765A; {anim(rise(OUT + .3, 20))}" dir="rtl"><span dir="ltr">ELVÉA°</span> · עולם מותג 14</div>
    <div style="{HE}; font-size: 62px; font-weight: 600; line-height: 1.18; color: #6B563F; {anim(rise(OUT + .5))}" dir="rtl">מהאתר ועד האריזה,<br>אותה שפה.</div></div>
  <div style="position: absolute; top: 1470px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center; {anim(rise(OUT + 1.0))}">
    <div style="{HE}; font-size: 44px; font-weight: 500; line-height: 1.3; color: #C4765A" dir="rtl">ואצלך, כל חלק מספר<br>את אותו סיפור?</div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 20px 56px; background: #6B563F; color: #FAF8F3; border-radius: 12px" dir="rtl"><span style="{HE}; font-size: 36px; font-weight: 500">אבחון פער המותג</span><span style="{HE}; font-size: 22px; opacity: .85">30 דק׳ · בלי עלות</span></div>
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; letter-spacing: .3em; color: #8B7355" dir="ltr">HAGITANTEBI.CO.IL</div></div>
</div>'''

world_kf = '0%%,%s{transform:scale(1)}%s,100%%{transform:scale(.5)}' % (P(OUT), P(OUT + .8))
html = f'''<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>ELVÉA orbit reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Heebo:wght@300;400;500;600&amp;family=Assistant:wght@300;400;600;700&amp;family=Plus+Jakarta+Sans:wght@400;500;800&amp;display=swap">
<style>
html,body{{margin:0;background:#FAF8F3}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#FAF8F3}}
.film *{{animation-duration:{D:g}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.world{{transform-origin:50% 50%}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}
{''.join(cards_css)}
{''.join(dim)}
</style><style>{{CSS}}</style></head>
<body><div id="stage"><div class="film" style="position: absolute; inset: 0">
<div style="position: absolute; inset: 0; {anim(world_kf)}">{WORLD}</div>
{INTRO}
{OUTRO}
{HOOK}
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: rgba(196,118,90,.18); z-index: 300"><div style="height: 6px; background: #C4765A; transform-origin: right; {anim('0%{transform:scaleX(0)}100%{transform:scaleX(1)}', 'animation-timing-function:linear')}"></div></div>
</div></div></body></html>'''
html = html.replace('{CSS}', '\n'.join(CSS))
open(os.path.join(HERE, 'orbit.html'), 'w').write(html)
print('ok', len(html))
