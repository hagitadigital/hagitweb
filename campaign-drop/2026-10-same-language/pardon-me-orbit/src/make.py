# PARDON ME° · world orbit — 25s studio reel, rebuilt from the 20.10 canvas artboard (PM-Orbit.dc.html).
# hook (her line, the sleeve with its oval window) → studio "עולם מותג 29" → four cards orbit the window
# (site · feed · ads · packaging), each plays the world's own mechanic at the front → the ring closes → outro.
# Writes reel.html next to this file. Every time is in seconds; P() turns it into a keyframe percentage.
import math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
D = 25.0
def P(t): return '%.3f%%' % (max(0, min(D, t)) / D * 100)

# PARDON ME palette (pardon-me/index.html :root)
PORC, PORC2, GARDEN, LIME, BLUE, PETAL, BERRY, INK, MUTED = '#F3EDE2', '#EAE2D3', '#1E3A2B', '#CFE06A', '#B9D3E8', '#F2C4CE', '#9B1B47', '#1B1F1C', '#5A6359'
HE = "font-family: 'Heebo', sans-serif"
BO = "font-family: 'Bodoni Moda', 'Frank Ruhl Libre', serif"
LOUD = "font-family: 'Archivo Narrow', sans-serif; font-weight: 700; text-transform: uppercase"
JK = "font-family: 'Plus Jakarta Sans', sans-serif"

# ── orbit geometry ──
CX, CY = 540, 890
RC = 215                    # the centre circle
R, KY = 380, 1.08           # orbit radius, vertical stretch (front card sits low, clear of the window)
CW, CH = 340, 450           # card size
N = 4
STEP = 360 / N
STOPS = [5.4, 9.4, 13.4, 17.4]   # card k reaches the front at STOPS[k]
TURN = .7
FIN = (20.9, 21.7)          # last turn: back to the site
OUT = 22.0                  # world shrinks into the studio window
HOLD_END = [STOPS[1] - TURN, STOPS[2] - TURN, STOPS[3] - TURN, FIN[0]]

def ease(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
def theta(t):
    if t < 4.3: return -135
    if t < STOPS[0]: return -135 + 135 * ease((t - 4.3) / (STOPS[0] - 4.3))
    a = 0
    for k in range(1, N):
        a -= STEP * ease((t - (STOPS[k] - TURN)) / TURN)
    a -= STEP * ease((t - FIN[0]) / (FIN[1] - FIN[0]))
    if t > OUT: a -= 20 * (t - OUT) / (D - OUT)
    return a
def radius(t): return R * ease((t - 4.3) / (STOPS[0] - 4.4))
def active(i, t):
    a = STOPS[i] - (.2 if i == 0 else 0)
    return min(ease((t - a + .25) / .35), 1 - ease((t - HOLD_END[i]) / .3))

CSS = []
for i in range(N):
    kf, op = [], []
    for f in range(int(D * 15) + 1):
        t = f / 15
        ph = math.radians(theta(t) + STEP * i)
        r = radius(t)
        x, y = CX - r * math.sin(ph), CY + r * KY * math.cos(ph)
        d = math.cos(ph)
        s = (.58 + .42 * (d + 1) / 2) * (1 + .3 * active(i, t)) * (min(1, r / R) * .9 + .1)
        z = int(round(50 + 40 * d)) if r > 10 else 40
        kf.append('%.3f%%{transform:translate(%.1fpx,%.1fpx) scale(%.4f);z-index:%d}' % (t / D * 100, x, y, s, z))
        op.append('%.3f%%{opacity:%.3f}' % (t / D * 100, .6 + .4 * (d + 1) / 2))
    CSS.append('.card%d{animation-name:card%d;animation-timing-function:linear}@keyframes card%d{%s}' % (i, i, i, ''.join(kf)))
    CSS.append('.dim%d{animation-name:dim%d;animation-timing-function:linear}@keyframes dim%d{%s}' % (i, i, i, ''.join(op)))

NK = [0]
def anim(kf, extra=''):
    NK[0] += 1; k = 'k%d' % NK[0]
    CSS.append('@keyframes %s{%s}' % (k, kf)); return 'animation-name:%s;%s' % (k, extra)
def show(a, b, f=.3):
    s = '0%{opacity:1}' if a <= 0 else '0%%,%s{opacity:0}%s{opacity:1}' % (P(a - f), P(a))
    e = '100%{opacity:1}' if b >= D else '%s{opacity:1}%s,100%%{opacity:0}' % (P(b), P(b + f))
    return s + e
def rise(t, dy=30): return '0%%,%s{opacity:0;transform:translateY(%dpx)}%s,100%%{opacity:1;transform:none}' % (P(t), dy, P(t + .5))
def steps(prop, pts, extra=''):   # pts: [(t, value)], held between
    kf = '0%%{%s:%s}' % (prop, pts[0][1]) + ''.join('%s{%s:%s}' % (P(t), prop, v) for t, v in pts) + '100%%{%s:%s}' % (prop, pts[-1][1])
    return anim(kf, extra)

# the berry line around the orbit draws a quarter per stop and closes on the last turn
ring = '0%%,%s{stroke-dashoffset:1}%s{stroke-dashoffset:.75}' % (P(4.8), P(STOPS[0]))
for k in range(1, N):
    ring += '%s{stroke-dashoffset:%.2f}%s{stroke-dashoffset:%.2f}' % (P(STOPS[k] - TURN), 1 - .25 * k, P(STOPS[k]), .75 - .25 * k)
ring += '%s,100%%{stroke-dashoffset:0}' % P(FIN[1])

face = "position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: 22px; overflow: hidden; box-shadow: 0 26px 60px rgba(27,31,28,.24)" % (-CW // 2, -CH // 2, CW, CH)
def oval_hole(rx, ry, cy='50%'):   # a porcelain sleeve with PARDON ME's oval window cut out of it
    m = f'radial-gradient(ellipse {rx}px {ry}px at 50% {cy}, transparent 98%, #000 100%)'
    return f'-webkit-mask-image: {m}; mask-image: {m}'

# 01 · the site: a phone scrolling the real site (hero window → NOT SORRY → the collections)
h0, h1 = STOPS[0], HOLD_END[0]
site_scroll = anim('0%%,%s{transform:translateY(0)}%s,%s{transform:translateY(-433px)}%s,%s{transform:translateY(-866px)}%s,100%%{transform:translateY(0)}'
                   % (P(h0 + .3), P(h0 + .9), P(h0 + 1.7), P(h0 + 2.3), P(h1 + .4), P(h1 + 1.0)), 'animation-timing-function:cubic-bezier(.7,0,.2,1)')
F_SITE = f'''<div style="{face}; background: {PORC2}">
  <div style="position: absolute; top: 12px; left: 0; right: 0; display: flex; justify-content: center"><span style="padding: 4px 14px; border-radius: 999px; background: {PORC}; {JK}; font-size: 13px; font-weight: 500; color: {GARDEN}" dir="ltr">hagitantebi.co.il/pardon-me</span></div>
  <div style="position: absolute; left: 60px; top: 42px; width: 220px; height: 400px; box-sizing: border-box; border: 10px solid {GARDEN}; border-radius: 34px; overflow: hidden; background: {PORC}">
    <img src="media/site-scroll.jpg" alt="" style="width: 200px; height: 1299px; display: block; {site_scroll}"></div></div>'''

# 02 · the feed: a 3×3 grid, every tile in the same language; tiles pop on the stop
tiles = ['print-high-maintenance.webp', 'ad-touch-yourself.webp', 'well-hello.webp', 'stationery.webp', 'print-none-of-your-business.webp',
         'ad-bad-decisions.webp', 'bag.webp', 'ad-i-kept-it.webp', 'print-bad-influence.webp']
h0 = STOPS[1]
grid = ''.join(f'''<div style="width: 104px; height: 104px; overflow: hidden; {anim('0%%,%s{transform:none}%s{transform:scale(.55);opacity:.2}%s,100%%{transform:none;opacity:1}' % (P(h0 - .1 + j * .09), P(h0 + j * .09), P(h0 + .45 + j * .09)), 'animation-timing-function:cubic-bezier(.2,.9,.3,1.3)')}"><img src="media/{f}" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>''' for j, f in enumerate(tiles))
F_FEED = f'''<div style="{face}; background: #FFFFFF; display: flex; flex-direction: column">
  <div style="height: 62px; display: flex; align-items: center; gap: 10px; padding: 0 14px" dir="ltr"><span style="width: 36px; height: 36px; border-radius: 50%; background: {PORC}; border: 2px solid {BERRY}; display: flex; align-items: center; justify-content: center"><i style="width: 10px; height: 17px; border-radius: 50%; background: {BERRY}"></i></span><span style="display: flex; flex-direction: column"><b style="{JK}; font-size: 16px; color: {INK}">pardonme.studio</b><span style="{JK}; font-size: 12px; color: {MUTED}">Nice on the outside.</span></span></div>
  <div style="display: grid; grid-template-columns: repeat(3, 104px); gap: 4px; justify-content: center">{grid}</div>
  <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; gap: 30px; {JK}; font-size: 13px; color: {MUTED}" dir="ltr"><span><b style="color: {INK}">48</b> posts</span><span><b style="color: {INK}">1</b> window</span></div></div>'''

# 03 · the ads: the polite card, and the oval lens that opens on the truth
h0 = STOPS[2]
lens = anim('0%%,%s{clip-path:ellipse(26px 42px at 50%% 56%%)}%s,%s{clip-path:ellipse(260px 330px at 50%% 52%%)}%s,100%%{clip-path:ellipse(26px 42px at 50%% 56%%)}'
            % (P(h0 + .25), P(h0 + 1.05), P(HOLD_END[2] + .2), P(HOLD_END[2] + .8)), 'animation-timing-function:cubic-bezier(.7,0,.2,1)')
F_ADS = f'''<div style="{face}; background: {BERRY}">
  <div style="position: absolute; left: 22px; top: 22px; width: 296px; height: 360px; background: {PORC}; overflow: hidden">
    <div style="position: absolute; top: 34px; left: 0; right: 0; text-align: center; {BO}; font-size: 15px; letter-spacing: .34em; color: {GARDEN}" dir="ltr">PARDON ME</div>
    <div style="position: absolute; top: 74px; left: 0; right: 0; text-align: center; {BO}; font-style: italic; font-size: 26px; line-height: 1.2; color: {GARDEN}" dir="ltr">A lovely candle<br>for a calm evening.</div>
    <div style="position: absolute; bottom: 22px; left: 0; right: 0; text-align: center; {HE}; font-size: 15px; color: {MUTED}" dir="rtl">נר נעים לערב רגוע.</div>
    <div style="position: absolute; inset: 0; {lens}"><img src="media/ad-bad-decisions.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block">
      <div style="position: absolute; left: 14px; top: 16px; display: flex; flex-direction: column; align-items: flex-start; gap: 4px; {anim(show(h0 + .9, HOLD_END[2], .2))}" dir="ltr"><span style="padding: 2px 8px; background: {BERRY}; color: #FFFFFF; {LOUD}; font-size: 26px; line-height: 1.05">Smells like<br>bad decisions.</span><span style="padding: 2px 8px; background: {LIME}; color: {GARDEN}; {BO}; font-style: italic; font-size: 15px">The good kind.</span></div></div>
  </div>
  <div style="position: absolute; bottom: 22px; left: 0; right: 0; text-align: center; {HE}; font-size: 16px; color: {PORC}" dir="rtl">פעם בשביל מי שמסתכלת מהר. ופעם בשביל מי שמציצה.</div></div>'''

# 04 · the packaging: "Take it off." — the sleeve slides up off the printed box
h0 = STOPS[3]
sleeve = anim('0%%,%s{transform:none}%s,%s{transform:translateY(-104%%)}%s,100%%{transform:none}' % (P(h0 + .35), P(h0 + 1.2), P(HOLD_END[3] + .1), P(HOLD_END[3] + .8)), 'animation-timing-function:cubic-bezier(.7,0,.2,1)')
F_PACK = f'''<div style="{face}; background: {PETAL}">
  <div style="position: absolute; left: 60px; top: 30px; width: 220px; height: 330px; overflow: hidden; border-radius: 4px; box-shadow: 0 16px 30px rgba(27,31,28,.22)">
    <img src="media/print-high-maintenance.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block">
    <div style="position: absolute; inset: 0; {sleeve}"><div style="position: absolute; inset: 0; background: {PORC}; {oval_hole(52, 92, '52%')}"></div>
      <div style="position: absolute; inset: 0; box-shadow: inset 0 0 0 1px rgba(30,58,43,.12)"></div>
      <div style="position: absolute; top: 22px; left: 0; right: 0; text-align: center; {BO}; font-size: 14px; letter-spacing: .32em; color: {GARDEN}" dir="ltr">PARDON ME</div>
      <div style="position: absolute; bottom: 20px; left: 0; right: 0; text-align: center; {BO}; font-style: italic; font-size: 17px; color: {GARDEN}" dir="ltr">High Maintenance</div></div></div>
  <div style="position: absolute; left: 22px; right: 22px; bottom: 20px; padding: 10px 14px; background: {PORC}; border-radius: 8px; display: flex; flex-direction: column; gap: 2px; text-align: right">
    <div style="{BO}; font-style: italic; font-size: 22px; color: {GARDEN}" dir="ltr">Take it off.</div>
    <div style="{HE}; font-size: 14px; color: {MUTED}" dir="rtl">ארבע קופסאות, אותו שרוול. כל אחת מספרת סוד אחר.</div></div></div>'''
FACES = [F_SITE, F_FEED, F_ADS, F_PACK]

LABELS = [('01', 'האתר', 'הגלילה הראשונה מגדילה את החלון.'),
          ('02', 'הפיד', 'פרינט, מודעה, ניירת. אותה שפה.'),
          ('03', 'המודעות', 'מבחוץ נר נעים. החלון חושף את האמת.'),
          ('04', 'האריזה', 'אותו שרוול, ובפנים פרינט אחר.')]
lab_win = [(STOPS[0] - .3, HOLD_END[0])] + [(STOPS[k], HOLD_END[k]) for k in range(1, N)]
cards = ''.join(f'<div class="card{i}" style="position: absolute; left: 0; top: 0; width: 0; height: 0"><div class="dim{i}">{FACES[i]}</div></div>' for i in range(N))
labels = ''.join(f'''<div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; gap: 6px; {anim(show(a, b, .25))}">
      <div style="{HE}; font-size: 60px; font-weight: 700; line-height: 1.1; color: {INK}" dir="rtl"><span style="{HE}; font-weight: 300; color: {BERRY}">{n}</span> · {h}</div>
      <div style="{HE}; font-size: 33px; font-weight: 300; color: {MUTED}" dir="rtl">{s}</div></div>''' for (n, h, s), (a, b) in zip(LABELS, lab_win))

# the centre: the sleeve's oval window; the print inside changes with each stop (roses → figs → berries → lemons → roses)
PRINTS = ['print-high-maintenance', 'print-none-of-your-business', 'print-bad-influence', 'print-well-hello']
pwin = [(0, STOPS[1] - TURN / 2), (STOPS[1] - TURN / 2, STOPS[2] - TURN / 2), (STOPS[2] - TURN / 2, STOPS[3] - TURN / 2), (STOPS[3] - TURN / 2, FIN[0] + .4)]
prints = ''.join(f'<img src="media/{p}.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; {anim(show(a, b, .35))}">' for p, (a, b) in zip(PRINTS, pwin))
prints += f'<img src="media/print-high-maintenance.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; {anim(show(FIN[0] + .4, D, .35))}">'
CENTRE = f'''<div style="position: absolute; left: {CX - RC}px; top: {CY - RC}px; width: {2 * RC}px; height: {2 * RC}px; z-index: 50; {anim('0%,' + P(3.45) + '{clip-path:circle(0 at 50% 50%)}' + P(4.15) + ',100%{clip-path:circle(50% at 50% 50%)}', 'animation-timing-function:cubic-bezier(.3,0,.2,1)')}">
    <div style="position: absolute; inset: 0; border-radius: 50%; overflow: hidden; background: {PORC}; box-shadow: inset 0 0 0 1px rgba(30,58,43,.15)">
      <div style="position: absolute; inset: 0">{prints}</div>
      <div style="position: absolute; inset: 0; background: {PORC}; {oval_hole(92, 150, '54%')}"></div>
      <div style="position: absolute; left: {RC - 92}px; top: {RC * 2 * .54 - 150:.0f}px; width: 184px; height: 300px; border-radius: 50%; box-shadow: inset 0 0 0 2px {GARDEN}"></div>
      <div style="position: absolute; top: 38px; left: 0; right: 0; text-align: center; {BO}; font-size: 20px; letter-spacing: .36em; color: {GARDEN}" dir="ltr">PARDON ME</div>
    </div>
    <div style="position: absolute; inset: -10px; border-radius: 50%; border: 3px solid {BERRY}; {anim(show(4.1, D, .4))}"></div>
  </div>'''

WORLD = f'''<div style="position: absolute; inset: 0; overflow: hidden; background: radial-gradient(ellipse 70% 45% at 50% 46%, {PORC} 0%, #EFE6D6 75%); box-shadow: 0 50px 140px rgba(27,31,28,.26)">
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <ellipse cx="{CX}" cy="{CY}" rx="{R}" ry="{R * KY:.0f}" fill="none" stroke="#D9AE85" stroke-width="2" stroke-dasharray="3 10" style="{anim(show(4.9, D, .5))}"/>
    <path d="M{CX} {CY + R * KY:.0f} A{R} {R * KY:.0f} 0 0 1 {CX} {CY - R * KY:.0f} A{R} {R * KY:.0f} 0 0 1 {CX} {CY + R * KY:.0f}" pathLength="1" fill="none" stroke="{BERRY}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 1" style="{anim(ring, 'animation-timing-function:linear')}"/>
  </svg>
  {CENTRE}
  <div style="position: absolute; left: 0; top: 0; z-index: 60; {anim(show(4.3, D, .2))}">{cards}</div>
  <div style="position: absolute; top: 120px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; z-index: 95; {anim(rise(4.4))}">
    <div style="{BO}; font-style: italic; font-size: 40px; color: {GARDEN}" dir="ltr">Nice on the outside. <span style="color: {BERRY}">Not sorry inside.</span></div>
    <div style="margin-top: 8px; {HE}; font-size: 34px; font-weight: 400; color: {MUTED}" dir="rtl">מנומס מבחוץ. לא מתנצל מבפנים.</div>
  </div>
  <div style="position: absolute; top: 1660px; left: 40px; right: 40px; height: 150px; z-index: 95">{labels}
    <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; gap: 8px; {anim(show(FIN[0] + .4, D, .3))}">
      <div style="{HE}; font-size: 54px; font-weight: 700; color: {INK}" dir="rtl">אתר · פיד · מודעות · אריזה</div>
      <div style="{HE}; font-size: 36px; font-weight: 300; color: {MUTED}" dir="rtl">חלון אחד, בכל מקום.</div></div>
  </div>
</div>'''

# ── the copper ball (Brand Worlds Studio) ──
def ball(path, a, b):
    k1 = anim('0%%,%s{offset-distance:0%%;opacity:%s}%s{offset-distance:0%%;opacity:1}%s{offset-distance:100%%;opacity:1}%s,100%%{offset-distance:100%%;opacity:0}' % (P(a - .01), '1' if a <= .2 else '0', P(a), P(b), P(b + .25)), 'animation-timing-function:cubic-bezier(.45,0,.4,1)')
    k2 = anim('0%%,%s{transform:rotate(0deg)}%s,100%%{transform:rotate(-400deg)}' % (P(a), P(b)), 'animation-timing-function:cubic-bezier(.45,0,.4,1)')
    return f'''<div class="ball" style="offset-path: path('{path}'); {k1}"><div class="halo"></div><div class="sph"><div style="position: absolute; inset: 0; {k2}"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>'''

# ── HOOK (0–2.6s): her line, and the sleeve with its oval window already on screen in frame 0 ──
HOOK_LINE = 'M1140 1700 C900 1720 760 1640 540 1660'
HOOK = f'''<div style="position: absolute; inset: 0; background: #EEE6D8; z-index: 200; {anim('0%,' + P(2.45) + '{opacity:1}' + P(2.85) + ',100%{opacity:0}')}">
  <div style="position: absolute; top: 88px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 36px; color: #3E2F25" dir="ltr">Brand Worlds Studio</div>
    <div style="{HE}; font-size: 17px; letter-spacing: .3em; color: #8B7B6E">חגית אנטבי</div></div>
  <div style="position: absolute; top: 250px; left: 70px; right: 70px; text-align: right; {HE}; font-size: 92px; font-weight: 700; line-height: 1.14; color: {INK}" dir="rtl">היא לא קונה נר.<br>היא בוחרת <span style="color: {BERRY}">עולם</span>.</div>
  <div style="position: absolute; left: 300px; top: 620px; width: 480px; height: 700px; {anim('0%{transform:none}' + P(2.5) + '{transform:scale(1.04)}100%{transform:scale(1.04)}', 'animation-timing-function:linear')}">
    <div style="position: absolute; inset: 0; overflow: hidden; border-radius: 6px; box-shadow: 0 34px 70px rgba(27,31,28,.24)">
      <img src="media/print-high-maintenance.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; {anim('0%{transform:scale(1.15)}' + P(2.6) + ',100%{transform:scale(1)}', 'animation-timing-function:linear')}">
      <div style="position: absolute; inset: 0; background: {PORC}; {oval_hole(110, 190, '54%')}"></div>
      <div style="position: absolute; left: 130px; top: {700 * .54 - 190:.0f}px; width: 220px; height: 380px; border-radius: 50%; box-shadow: inset 0 0 0 2px {GARDEN}"></div>
      <div style="position: absolute; top: 46px; left: 0; right: 0; text-align: center; {BO}; font-size: 30px; letter-spacing: .34em; color: {GARDEN}" dir="ltr">PARDON ME</div>
      <div style="position: absolute; bottom: 40px; left: 0; right: 0; text-align: center; {BO}; font-style: italic; font-size: 30px; color: {GARDEN}" dir="ltr">Nice on the outside.</div></div>
  </div>
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line" pathLength="1" d="{HOOK_LINE}" style="{anim('0%,' + P(.2) + '{stroke-dashoffset:1}' + P(2.2) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:linear')}"/></svg>
  {ball(HOOK_LINE, .2, 2.2)}
  <div style="position: absolute; top: 1760px; left: 0; right: 0; text-align: center; {HE}; font-size: 34px; font-weight: 300; color: #6B563F; {anim('0%,' + P(.9) + '{opacity:0}' + P(1.3) + ',100%{opacity:1}')}" dir="rtl">מאחורי החלון יש עולם שלם.</div>
</div>'''

# ── studio intro (2.6–4.3): the copper line runs into the centre and opens the window ──
INTRO_LINE = f'M1140 1690 C1000 1500 900 1050 {CX} {CY}'
INTRO = f'''<div style="position: absolute; inset: 0; z-index: 150; pointer-events: none">
  <div style="position: absolute; inset: 0; background: #EFE6D6; {anim('0%,' + P(3.9) + '{opacity:1}' + P(4.5) + ',100%{opacity:0}')}"></div>
  <div style="position: absolute; top: 120px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px; {anim(show(2.65, 4.05, .3))}">
    <div style="{JK}; font-size: 22px; font-weight: 500; letter-spacing: .32em; color: #C4765A" dir="ltr">BRAND WORLDS STUDIO · HAGIT ANTEBI</div>
    <div style="{HE}; font-size: 96px; font-weight: 500; line-height: 1.05; color: #6B563F" dir="rtl">עולם מותג <em style="font-family: 'Cormorant Garamond', serif; font-weight: 400; color: #B8894A">29</em></div></div>
  <div style="position: absolute; top: 1480px; left: 80px; right: 80px; text-align: center; {HE}; font-size: 44px; line-height: 1.35; color: #6B563F; {anim(show(2.8, 4.05, .3))}" dir="rtl">נרות, ריח לבית וטיפוח.<br>שרוול מנומס עם חלון אחד.</div>
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <g style="{anim(show(2.6, 4.0, .3))}"><path class="line" pathLength="1" d="{INTRO_LINE}" style="{anim('0%,' + P(2.75) + '{stroke-dashoffset:1}' + P(3.55) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:cubic-bezier(.4,0,.3,1)')}"/></g>
    <circle cx="{CX}" cy="{CY}" r="40" fill="none" stroke="#C4765A" stroke-width="3" style="transform-origin: {CX}px {CY}px; {anim('0%,' + P(3.5) + '{opacity:0;transform:scale(1)}' + P(3.6) + '{opacity:1}' + P(4.3) + ',100%{opacity:0;transform:scale(7)}')}"/>
  </svg>
  {ball(INTRO_LINE, 2.75, 3.55)}
</div>'''

# ── outro (22–25): her closing line in the studio window, then the CTA; holds to the last frame ──
OUTRO = f'''<div style="position: absolute; inset: 0; z-index: 150; pointer-events: none">
  <div style="position: absolute; top: 100px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
    <div style="{HE}; font-size: 28px; font-weight: 500; letter-spacing: .06em; color: #C4765A; {anim(rise(OUT + .3, 20))}" dir="rtl"><span dir="ltr">PARDON ME°</span> · עולם מותג 29</div>
    <div style="{HE}; font-size: 64px; font-weight: 700; line-height: 1.18; color: {INK}; {anim(rise(OUT + .5))}" dir="rtl">עולם שבוחרים בו.<br><span style="color: {BERRY}">בכל נקודת מגע.</span></div></div>
  <div style="position: absolute; top: 1470px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center; {anim(rise(OUT + 1.0))}">
    <div style="{HE}; font-size: 44px; font-weight: 500; line-height: 1.3; color: #C4765A" dir="rtl">ואצלך, בוחרים מוצר<br>או בוחרים עולם?</div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 20px 56px; background: #6B563F; color: #FAF8F3; border-radius: 12px" dir="rtl"><span style="{HE}; font-size: 36px; font-weight: 500">אבחון פער המותג</span><span style="{HE}; font-size: 22px; opacity: .85">30 דק׳ · בלי עלות</span></div>
    <div style="{JK}; font-size: 22px; letter-spacing: .3em; color: #8B7355" dir="ltr">HAGITANTEBI.CO.IL</div></div>
</div>'''

world_kf = '0%%,%s{transform:scale(1)}%s,100%%{transform:scale(.5)}' % (P(OUT), P(OUT + .8))
html = f'''<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>PARDON ME orbit reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;0,6..96,500;1,6..96,400&amp;family=Frank+Ruhl+Libre:wght@400;500&amp;family=Heebo:wght@300;400;500;700&amp;family=Archivo+Narrow:wght@700&amp;family=Cormorant+Garamond:ital,wght@0,400;1,400&amp;family=Plus+Jakarta+Sans:wght@400;500;700&amp;display=swap">
<style>
html,body{{margin:0;background:#FAF8F3}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#FAF8F3}}
.film *{{animation-duration:{D:g}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}
</style><style>{{CSS}}</style></head>
<body><div id="stage"><div class="film" style="position: absolute; inset: 0">
<div style="position: absolute; inset: 0; transform-origin: 50% 50%; {anim(world_kf)}">{WORLD}</div>
{INTRO}
{OUTRO}
{HOOK}
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 6px; background: rgba(196,118,90,.18); z-index: 300"><div style="height: 6px; background: #C4765A; transform-origin: right; {anim('0%{transform:scaleX(0)}100%{transform:scaleX(1)}', 'animation-timing-function:linear')}"></div></div>
</div></div></body></html>'''
html = html.replace('{CSS}', '\n'.join(CSS))
open(os.path.join(HERE, 'reel.html'), 'w').write(html)
print('ok', len(html))
