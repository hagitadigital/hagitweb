# VELUNE° · world orbit — 25s studio reel, rebuilt from the 20.10 canvas artboard (VE-Orbit.dc.html), same engine as PARDON ME°.
# hook ("היא לא קונה ריח. היא נכנסת למקום.", the red fruit under VELUNE's arch) → studio "עולם מותג 25" → four cards orbit the fruit
# (site · feed · ad · packaging), each plays the world's own mechanic at the front → the ring closes → outro.
# REEL=long builds the long cut (reel-long.html): at each stop the front card opens to a full window and the site itself plays
# (clips recorded by record-site.js, laid over the render by build-long.sh from the schedule in long-overlays.json).
# Writes reel.html next to this file. Every time is in seconds; P() turns it into a keyframe percentage.
import math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
LONG = os.environ.get('REEL') == 'long'
def P(t): return '%.3f%%' % (max(0, min(D, t)) / D * 100)

# VELUNE palette (velune/index.html :root)
MARBRE, POUDRE, INK, LITCHI, CHAIR, EAU, NUIT, MUTED, ARGENT = '#DCE3EB', '#C4D2E0', '#1E2A38', '#8E1E44', '#F1D9DC', '#8FA9C2', '#232A3F', '#6E8399', '#C9CFD6'
HE = "font-family: 'Heebo', sans-serif"
MA = "font-family: 'Marcellus', serif"
DV = "font-family: 'David Libre', serif"
AS = "font-family: 'Assistant', sans-serif"
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
FIN = (20.9, 21.7)         # last turn: back to the site
OUT = 22.0                 # world shrinks into the studio window
HOLD_END = [STOPS[1] - TURN, STOPS[2] - TURN, STOPS[3] - TURN, FIN[0]]
D = 25.0
# long cut: (clips, seconds in the full window) per card; a card opens .5s after it lands, .6s each way
CHAPTERS = [(['seuil', 'heures'], 10.6), ([], 4.2), (['fruit'], 6.2), (['ecrin'], 4.6)]
CLIP_LEN = {'seuil': 6.0, 'heures': 4.6, 'fruit': 6.2, 'ecrin': 4.6}
OPEN = []
if LONG:
    STOPS, HOLD_END = [5.4], []
    for k, (clips, L) in enumerate(CHAPTERS):
        o = STOPS[k] + .5
        OPEN.append((o, o + .6, o + .6 + L, o + 1.2 + L))   # opening, full, closing, closed
        HOLD_END.append(o + 1.2 + L + .2)
        if k < N - 1: STOPS.append(HOLD_END[-1] + TURN)
    FIN = (HOLD_END[-1], HOLD_END[-1] + .8)
    OUT = FIN[1] + .4
    D = round(OUT + 3.2, 1)

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
def windows(segs, f=.15):   # opacity on during each (a, b) segment, quick fades between
    pts = []
    for a, b in segs:
        pts += [(a - f, 0), (a, 1), (b, 1), (b + f, 0)]
    kf, last = '', None
    for t, o in sorted((max(0, min(D, t)), o) for t, o in pts):
        kf += '%s{opacity:%d}' % (P(t), o)
    first = 1 if segs[0][0] <= 0 else 0
    lastv = 1 if segs[-1][1] >= D else 0
    return anim('0%%{opacity:%d}%s100%%{opacity:%d}' % (first, kf, lastv))
def steps(prop, pts, extra=''):   # pts: [(t, value)], held between
    kf = '0%%{%s:%s}' % (prop, pts[0][1]) + ''.join('%s{%s:%s}' % (P(t), prop, v) for t, v in pts) + '100%%{%s:%s}' % (prop, pts[-1][1])
    return anim(kf, extra)

# the litchi line around the orbit draws a quarter per stop and closes on the last turn
ring = '0%%,%s{stroke-dashoffset:1}%s{stroke-dashoffset:.75}' % (P(4.8), P(STOPS[0]))
for k in range(1, N):
    ring += '%s{stroke-dashoffset:%.2f}%s{stroke-dashoffset:%.2f}' % (P(STOPS[k] - TURN), 1 - .25 * k, P(STOPS[k]), .75 - .25 * k)
ring += '%s,100%%{stroke-dashoffset:0}' % P(FIN[1])

face = "position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: 22px; overflow: hidden; box-shadow: 0 26px 60px rgba(30,42,56,.26)" % (-CW // 2, -CH // 2, CW, CH)

ARCH = 'border-radius: 999px 999px 0 0'          # VELUNE's arch: the door, the box, the boutique

# 01 · the site: a phone scrolling the real site (the door, the garden, the fruit)
h0, h1 = STOPS[0], HOLD_END[0]
site_scroll = anim('0%%,%s{transform:translateY(0)}%s,%s{transform:translateY(-356px)}%s,%s{transform:translateY(-711px)}%s,100%%{transform:translateY(0)}'
                   % (P(h0 + .3), P(h0 + .9), P(h0 + .3 + (h1 - h0 - .6) / 2), P(h0 + .9 + (h1 - h0 - .6) / 2), P(h1 + .4), P(h1 + 1.0)), 'animation-timing-function:cubic-bezier(.7,0,.2,1)')
F_SITE = f'''<div style="{face}; background: {POUDRE}">
  <div style="position: absolute; top: 14px; left: 0; right: 0; display: flex; justify-content: center"><span style="padding: 4px 14px; border-radius: 999px; background: {MARBRE}; {JK}; font-size: 13px; font-weight: 500; color: {NUIT}" dir="ltr">hagitantebi.co.il/velune</span></div>
  <div style="position: absolute; left: 60px; top: 50px; width: 220px; height: 376px; box-sizing: border-box; border: 10px solid {NUIT}; border-radius: 34px; overflow: hidden; background: {MARBRE}">
    <img src="media/site-scroll.jpg" alt="" style="width: 200px; height: 1066px; display: block; {site_scroll}"></div></div>'''

# 02 · the feed: a 3×3 grid in one light; tiles pop on the stop
tiles = ['02-porte-closed-wall', '06-fruit-closed', '10-bottle-aube-day', '17-muse-touching-fruit', '05-allee-garden-water',
         '20-ecrin-box-open', '11-bottle-floraison-blush', '08-drop-alone', '22-boutique-counter-three']
h0 = STOPS[1]
pops = [h0]
def pop(j):
    kf = '0%{transform:none;opacity:1}'
    for t0 in pops:
        kf += '%s{transform:none;opacity:1}%s{transform:scale(.55);opacity:.2}%s{transform:none;opacity:1}' % (P(t0 - .1 + j * .09), P(t0 + j * .09), P(t0 + .45 + j * .09))
    return anim(kf + '100%{transform:none;opacity:1}', 'animation-timing-function:cubic-bezier(.2,.9,.3,1.3)')
def avatar(size):
    return f'<span style="width: {size}px; height: {size}px; flex: none; border-radius: 50%; background: {MARBRE}; border: {max(2, size // 18)}px solid {LITCHI}; display: flex; align-items: flex-end; justify-content: center; overflow: hidden"><i style="width: {size * .42:.0f}px; height: {size * .6:.0f}px; background: {POUDRE}; border: {max(1, size // 30)}px solid {NUIT}; border-bottom: 0; {ARCH}"></i></span>'
grid = ''.join(f'''<div style="width: 104px; height: 104px; overflow: hidden; {pop(j)}"><img src="media/{f}.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>''' for j, f in enumerate(tiles))
F_FEED = f'''<div style="{face}; background: #FFFFFF; display: flex; flex-direction: column">
  <div style="height: 62px; display: flex; align-items: center; gap: 10px; padding: 0 14px" dir="ltr">{avatar(36)}<span style="display: flex; flex-direction: column"><b style="{JK}; font-size: 16px; color: {INK}">velune.maison</b><span style="{JK}; font-size: 12px; color: {MUTED}">Maison de Parfum</span></span></div>
  <div style="display: grid; grid-template-columns: repeat(3, 104px); gap: 4px; justify-content: center">{grid}</div>
  <div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; gap: 30px; {JK}; font-size: 13px; color: {MUTED}" dir="ltr"><span><b style="color: {INK}">36</b> posts</span><span><b style="color: {INK}">1</b> garden</span></div></div>'''

# 03 · the ad: a sponsored post; on the stop the image walks in and the CTA is pressed
h0, h1 = STOPS[2], HOLD_END[2]
push = anim('0%%,%s{transform:scale(1)}%s{transform:scale(1.12)}%s,100%%{transform:scale(1)}' % (P(h0), P(h1), P(h1 + .6)), 'animation-timing-function:linear')
press = anim('0%%,%s{transform:none;background:%s}%s{transform:scale(.94);background:#A8285A}%s,100%%{transform:none;background:%s}' % (P(h1 - 1.0), LITCHI, P(h1 - .8), P(h1 - .5), LITCHI))
F_ADS = f'''<div style="{face}; background: #FFFFFF; display: flex; flex-direction: column">
  <div style="height: 50px; display: flex; align-items: center; gap: 8px; padding: 0 12px" dir="ltr">{avatar(30)}<span style="display: flex; flex-direction: column"><b style="{JK}; font-size: 14px; color: {INK}">velune.maison</b><span style="{JK}; font-size: 11px; color: {MUTED}">Sponsored · ממומן</span></span></div>
  <div style="position: relative; height: 250px; overflow: hidden"><img src="media/17-muse-touching-fruit.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; object-position: 50% 35%; display: block; {push}"></div>
  <div style="height: 40px; margin: 0; display: flex; align-items: center; justify-content: space-between; padding: 0 14px; color: #FFFFFF; {HE}; font-size: 15px; font-weight: 500; {press}" dir="rtl"><span>להיכנס לגן</span><span>‹</span></div>
  <div style="flex-grow: 1; display: flex; align-items: center; padding: 0 14px; {DV}; font-size: 19px; line-height: 1.25; color: {INK}" dir="rtl">היא לא מתיזה בושם.<br>היא נכנסת אליו.</div></div>'''

# 04 · the packaging: L'Écrin — the box's two doors open on the stop, like the site's
h0, h1 = STOPS[3], HOLD_END[3]
def leaf(side):
    sgn = -1 if side == 'l' else 1
    kf = '0%%,%s{transform:rotateY(0deg)}%s,%s{transform:rotateY(%ddeg)}%s,100%%{transform:rotateY(0deg)}' % (P(h0 + .3), P(h0 + 1.3), P(h1 + .1), sgn * 100, P(h1 + .8))
    pos = 'left: 0' if side == 'l' else 'right: 0'
    return f'''<div style="position: absolute; top: 0; bottom: 0; {pos}; width: 50%; overflow: hidden; transform-origin: {'left' if side == 'l' else 'right'} center; backface-visibility: hidden; {anim(kf, 'animation-timing-function:cubic-bezier(.6,0,.25,1)')}"><img src="media/19-ecrin-box-closed.webp" alt="" style="position: absolute; top: 0; {pos}; width: 220px; height: 275px; display: block"></div>'''
F_PACK = f'''<div style="{face}; background: {POUDRE}">
  <div style="position: absolute; left: 60px; top: 34px; width: 220px; height: 275px; overflow: hidden; border-radius: 6px; perspective: 700px; box-shadow: 0 16px 30px rgba(30,42,56,.22)">
    <img src="media/20-ecrin-box-open.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; display: block">
    {leaf('l')}{leaf('r')}</div>
  <div style="position: absolute; left: 22px; right: 22px; bottom: 20px; padding: 10px 14px; background: {MARBRE}; border-radius: 8px; display: flex; flex-direction: column; gap: 2px; text-align: right">
    <div style="{MA}; font-size: 20px; letter-spacing: .12em; color: {NUIT}" dir="ltr">L'ÉCRIN</div>
    <div style="{HE}; font-size: 15px; color: {MUTED}" dir="rtl">קופסת אבן כחולה, קשת מוטבעת, קטיפה בצבע הפרי.</div></div></div>'''
FACES = [F_SITE, F_FEED, F_ADS, F_PACK]

LABELS = [('01', 'האתר', 'הגלילה פותחת את הדלת.'),
          ('02', 'הפיד', 'דלת, פרי, בקבוק. אותו גן.'),
          ('03', 'המודעה', 'היא לא מתיזה בושם. היא נכנסת אליו.'),
          ('04', 'האריזה', 'הדלת חוזרת. הפעם בקופסה.')]
lab_win = [(STOPS[0] - .3, HOLD_END[0])] + [(STOPS[k], HOLD_END[k]) for k in range(1, N)]
cards = ''.join(f'<div class="card{i}" style="position: absolute; left: 0; top: 0; width: 0; height: 0"><div class="dim{i}">{FACES[i]}</div></div>' for i in range(N))
labels = ''.join(f'''<div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; gap: 6px; {anim(show(a, b, .25))}">
      <div style="{HE}; font-size: 60px; font-weight: 700; line-height: 1.1; color: {INK}" dir="rtl"><span style="{HE}; font-weight: 300; color: {LITCHI}">{n}</span> · {h}</div>
      <div style="{HE}; font-size: 33px; font-weight: 300; color: {MUTED}" dir="rtl">{s}</div></div>''' for (n, h, s), (a, b) in zip(LABELS, lab_win))

# the centre: the fruit under the arch; with each stop it moves one step along its story (fruit → opened → drop → bottle → fruit)
STORY = ['06-fruit-closed', '07-fruit-open-drop', '08-drop-alone', '09-bottle-blush-garden']
pwin = [(0, STOPS[1] - TURN / 2), (STOPS[1] - TURN / 2, STOPS[2] - TURN / 2), (STOPS[2] - TURN / 2, STOPS[3] - TURN / 2), (STOPS[3] - TURN / 2, FIN[0] + .4)]
story = ''.join(f'<img src="media/{p}.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; {anim(show(a, b, .35))}">' for p, (a, b) in zip(STORY, pwin))
story += f'<img src="media/06-fruit-closed.webp" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; {anim(show(FIN[0] + .4, D, .35))}">'
AW, AH = 200, 290
CENTRE = f'''<div style="position: absolute; left: {CX - RC}px; top: {CY - RC}px; width: {2 * RC}px; height: {2 * RC}px; z-index: 50; {anim('0%,' + P(3.45) + '{clip-path:circle(0 at 50% 50%)}' + P(4.15) + ',100%{clip-path:circle(50% at 50% 50%)}', 'animation-timing-function:cubic-bezier(.3,0,.2,1)')}">
    <div style="position: absolute; inset: 0; border-radius: 50%; overflow: hidden; background: {MARBRE}; box-shadow: inset 0 0 0 1px rgba(30,42,56,.15)">
      <div style="position: absolute; left: {RC - AW // 2}px; top: 92px; width: {AW}px; height: {AH}px; overflow: hidden; {ARCH}; box-shadow: 0 0 0 2px {NUIT}">{story}</div>
      <div style="position: absolute; top: 40px; left: 0; right: 0; text-align: center; {MA}; font-size: 22px; letter-spacing: .32em; color: {NUIT}" dir="ltr">VELUNE°</div>
    </div>
    <div style="position: absolute; inset: -10px; border-radius: 50%; border: 3px solid {LITCHI}; {anim(show(4.1, D, .4))}"></div>
  </div>'''

# ── long cut: the front card opens to a full window. Site clips are laid over the render by ffmpeg while the window is full;
# the opening and closing moves show the clip's first and last frame, so the cut into the video is seamless.
FRONT = (CY + R * KY, 1.3)
fy, fs = FRONT
fw, fh = CW * fs / 2, CH * fs / 2
card_rect = 'inset(%.0fpx %.0fpx %.0fpx %.0fpx round 29px)' % (fy - fh, 540 - fw, 1920 - fy - fh, 540 - fw)
feed_tiles = ['02-porte-closed-wall', '06-fruit-closed', '10-bottle-aube-day', '17-muse-touching-fruit', '05-allee-garden-water', '20-ecrin-box-open',
              '11-bottle-floraison-blush', '08-drop-alone', '22-boutique-counter-three', '16-muse-holding-bottle', '04-porte-open-garden', '12-bottle-crepuscule-dusk',
              '07-fruit-open-drop', '19-ecrin-box-closed', '14-notes-floraison-rose-peony', '18-muse-spray', '01-lineup-three-editions-arch', '21-boutique-interior']
def full_feed(a, b):
    scroll = anim('0%%,%s{transform:translateY(0)}%s,100%%{transform:translateY(-760px)}' % (P(a + .4), P(b - .3)), 'animation-timing-function:cubic-bezier(.45,0,.3,1)')
    tiles = ''.join(f'<div style="aspect-ratio: 1; overflow: hidden"><img src="media/{t}.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block"></div>' for t in feed_tiles)
    return f'''<div style="position: absolute; inset: 0; background: #FFFFFF">
      <div style="height: 120px; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 18px; box-sizing: border-box; {JK}; font-size: 34px; font-weight: 700; color: {INK}" dir="ltr">velune.maison</div>
      <div style="position: absolute; top: 120px; left: 0; right: 0; bottom: 0; overflow: hidden"><div style="{scroll}">
        <div style="display: flex; align-items: center; gap: 44px; padding: 26px 44px" dir="ltr">{avatar(170)}
          <span style="display: flex; gap: 60px; {JK}; font-size: 26px; color: {MUTED}; text-align: center"><span><b style="display: block; font-size: 38px; color: {INK}">36</b>posts</span><span><b style="display: block; font-size: 38px; color: {INK}">18.2k</b>followers</span><span><b style="display: block; font-size: 38px; color: {INK}">1</b>garden</span></span></div>
        <div style="padding: 0 44px 26px" dir="ltr"><div style="{MA}; font-size: 32px; letter-spacing: .1em; color: {INK}">VELUNE° · Maison de Parfum</div><div style="margin-top: 6px; {DV}; font-size: 30px; color: {NUIT}" dir="rtl">בושם הוא לא ריח. הוא מקום.</div><div style="margin-top: 4px; {HE}; font-size: 25px; color: {MUTED}" dir="rtl">גן אחד מאחורי דלת אחת · שלוש שעות ביום</div></div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px">{tiles}</div></div></div></div>'''
AD_MEDIA = (0, 330, 1080, 1350, 285)    # x, y, w, h of the ad's media box, and the crop offset into the 1080×1920 clip
def full_ad(clip):
    x, y, w, h, cy = AD_MEDIA
    return f'''<div style="position: absolute; inset: 0; background: #FFFFFF">
      <div style="position: absolute; top: 210px; left: 0; right: 0; height: 110px; display: flex; align-items: center; gap: 22px; padding: 0 40px" dir="ltr">{avatar(78)}<span style="display: flex; flex-direction: column"><b style="{JK}; font-size: 32px; color: {INK}">velune.maison</b><span style="{JK}; font-size: 24px; color: {MUTED}">Sponsored · ממומן</span></span><span style="margin-left: auto; {JK}; font-size: 40px; color: {INK}">···</span></div>
      <div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {h}px; overflow: hidden; background: {MARBRE}"><img src="media/clips/{clip}-first.jpg" alt="" style="position: absolute; left: 0; top: -{cy}px; width: 1080px; height: 1920px; display: block"></div>
      <div style="position: absolute; left: 0; right: 0; top: {y + h}px; height: 96px; display: flex; align-items: center; justify-content: space-between; padding: 0 40px; background: {LITCHI}; color: #FFFFFF; {HE}; font-size: 36px; font-weight: 500" dir="rtl"><span>להיכנס לגן</span><span>‹</span></div>
      <div style="position: absolute; left: 40px; right: 40px; top: {y + h + 112}px; {DV}; font-size: 40px; line-height: 1.25; color: {INK}; text-align: right" dir="rtl"><b>velune.maison</b> היא לא מתיזה בושם. היא נכנסת אליו.</div></div>'''
def chip(k, top=330):   # the site clips keep the site's own logo clear; the feed puts its label at the bottom, the ad above its header
    CHIP_CSS = f"position: absolute; top: {top}px; left: 0; right: 0; display: flex; justify-content: center"
    n, h, sub = LABELS[k]
    return f'''<div style="{CHIP_CSS}"><div style="display: flex; flex-direction: column; align-items: center; gap: 2px; padding: 14px 40px 16px; border-radius: 22px; background: rgba(30,42,56,.84); color: {MARBRE}" dir="rtl"><span style="{HE}; font-size: 46px; font-weight: 700; line-height: 1.1"><span style="font-weight: 300; color: {CHAIR}">{n}</span> · {h}</span><span style="{HE}; font-size: 24px; font-weight: 300; opacity: .9">{sub}</span></div></div>'''
WINDOWS, OVERLAYS = '', []
for k, (clips, L) in enumerate(CHAPTERS if LONG else []):
    o0, o1, o2, o3 = OPEN[k]
    clip_kf = '0%%,%s{clip-path:%s}%s,%s{clip-path:inset(0px 0px 0px 0px round 0px)}%s,100%%{clip-path:%s}' % (P(o0), card_rect, P(o1), P(o2), P(o3), card_rect)
    chip_top = 330      # below the site's own logo bar
    if k == 2:            # the ad: the fruit film plays inside a sponsored post
        inner, chip_top = full_ad(clips[0]), 60
        x, y, w, h, cy = AD_MEDIA
        OVERLAYS.append({'clip': clips[0], 'start': round(o1, 3), 'dur': CLIP_LEN[clips[0]], 'chip': None, 'crop': [w, h, 0, cy], 'at': [x, y]})
    elif clips:
        inner = (f'<img src="media/clips/{clips[-1]}-last.jpg" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block">'
                 f'<img src="media/clips/{clips[0]}-first.jpg" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; {windows([(0, o1 + .2)], .01)}">')
        t = o1
        for c in clips:
            OVERLAYS.append({'clip': c, 'start': round(t, 3), 'dur': CLIP_LEN[c], 'chip': k})
            t += CLIP_LEN[c]
    else:
        inner, chip_top = full_feed(o1, o2), 1660
    WINDOWS += f'''<div style="position: absolute; inset: 0; z-index: 120; {windows([(o0, o3)], .01)}"><div style="position: absolute; inset: 0; {anim(clip_kf, 'animation-timing-function:cubic-bezier(.7,0,.2,1)')}">{inner}
    <div style="position: absolute; inset: 0; {anim(show(o1 - .1, o2, .2))}">{chip(k, chip_top)}</div></div></div>'''

WORLD = f'''<div style="position: absolute; inset: 0; overflow: hidden; background: radial-gradient(ellipse 70% 45% at 50% 46%, #E9EEF3 0%, {MARBRE} 75%); box-shadow: 0 50px 140px rgba(30,42,56,.26)">
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <ellipse cx="{CX}" cy="{CY}" rx="{R}" ry="{R * KY:.0f}" fill="none" stroke="{EAU}" stroke-width="2" stroke-dasharray="3 10" style="{anim(show(4.9, D, .5))}"/>
    <path d="M{CX} {CY + R * KY:.0f} A{R} {R * KY:.0f} 0 0 1 {CX} {CY - R * KY:.0f} A{R} {R * KY:.0f} 0 0 1 {CX} {CY + R * KY:.0f}" pathLength="1" fill="none" stroke="{LITCHI}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 1" style="{anim(ring, 'animation-timing-function:linear')}"/>
  </svg>
  {CENTRE}
  {WINDOWS}
  <div style="position: absolute; left: 0; top: 0; z-index: 60; {anim(show(4.3, D, .2))}">{cards}</div>
  <div style="position: absolute; top: 120px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; z-index: 95; {anim(rise(4.4))}">
    <div style="{MA}; font-size: 30px; letter-spacing: .3em; color: {NUIT}" dir="ltr">VELUNE° · MAISON DE PARFUM</div>
    <div style="margin-top: 10px; {DV}; font-size: 46px; color: {INK}" dir="rtl">בושם הוא לא ריח. <span style="color: {LITCHI}">הוא מקום.</span></div>
  </div>
  <div style="position: absolute; top: 1660px; left: 40px; right: 40px; height: 150px; z-index: 95">{labels}
    <div style="position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; gap: 8px; {anim(show(FIN[0] + .4, D, .3))}">
      <div style="{HE}; font-size: 54px; font-weight: 700; color: {INK}" dir="rtl">אתר · פיד · מודעה · אריזה</div>
      <div style="{HE}; font-size: 36px; font-weight: 300; color: {MUTED}" dir="rtl">הכל מסתובב סביב דבר אחד.</div></div>
  </div>
</div>'''

# ── the copper ball (Brand Worlds Studio) ──
def ball(path, a, b):
    k1 = anim('0%%,%s{offset-distance:0%%;opacity:%s}%s{offset-distance:0%%;opacity:1}%s{offset-distance:100%%;opacity:1}%s,100%%{offset-distance:100%%;opacity:0}' % (P(a - .01), '1' if a <= .2 else '0', P(a), P(b), P(b + .25)), 'animation-timing-function:cubic-bezier(.45,0,.4,1)')
    k2 = anim('0%%,%s{transform:rotate(0deg)}%s,100%%{transform:rotate(-400deg)}' % (P(a), P(b)), 'animation-timing-function:cubic-bezier(.45,0,.4,1)')
    return f'''<div class="ball" style="offset-path: path('{path}'); {k1}"><div class="halo"></div><div class="sph"><div style="position: absolute; inset: 0; {k2}"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>'''

# ── HOOK (0–2.6s): her line, and the red fruit under the arch already on screen in frame 0 ──
HOOK_LINE = 'M1140 1700 C900 1720 760 1640 540 1660'
HOOK = f'''<div style="position: absolute; inset: 0; background: #EEE6D8; z-index: 200; {anim('0%,' + P(2.45) + '{opacity:1}' + P(2.85) + ',100%{opacity:0}')}">
  <div style="position: absolute; top: 88px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 36px; color: #3E2F25" dir="ltr">Brand Worlds Studio</div>
    <div style="{HE}; font-size: 17px; letter-spacing: .3em; color: #8B7B6E">חגית אנטבי</div></div>
  <div style="position: absolute; top: 250px; left: 70px; right: 70px; text-align: right; {HE}; font-size: 88px; font-weight: 700; line-height: 1.14; color: {INK}" dir="rtl">היא לא קונה ריח.<br>היא נכנסת <span style="color: {LITCHI}">למקום</span>.</div>
  <div style="position: absolute; left: 290px; top: 600px; width: 500px; height: 760px; {anim('0%{transform:none}' + P(2.5) + '{transform:scale(1.04)}100%{transform:scale(1.04)}', 'animation-timing-function:linear')}">
    <div style="position: absolute; inset: 0; overflow: hidden; border-radius: 6px; background: {POUDRE}; box-shadow: 0 34px 70px rgba(30,42,56,.24)">
      <div style="position: absolute; left: 70px; top: 120px; width: 360px; height: 520px; overflow: hidden; {ARCH}; box-shadow: 0 0 0 3px {NUIT}">
        <img src="media/06-fruit-closed.webp" alt="" style="width: 100%; height: 100%; object-fit: cover; display: block; {anim('0%{transform:scale(1.12)}' + P(2.6) + ',100%{transform:scale(1)}', 'animation-timing-function:linear')}"></div>
      <div style="position: absolute; top: 46px; left: 0; right: 0; text-align: center; {MA}; font-size: 34px; letter-spacing: .34em; color: {NUIT}" dir="ltr">VELUNE°</div>
      <div style="position: absolute; bottom: 44px; left: 0; right: 0; text-align: center; {MA}; font-size: 22px; letter-spacing: .3em; color: {NUIT}" dir="ltr">MAISON DE PARFUM</div></div>
  </div>
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line" pathLength="1" d="{HOOK_LINE}" style="{anim('0%,' + P(.2) + '{stroke-dashoffset:1}' + P(2.2) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:linear')}"/></svg>
  {ball(HOOK_LINE, .2, 2.2)}
  <div style="position: absolute; top: 1760px; left: 0; right: 0; text-align: center; {HE}; font-size: 34px; font-weight: 300; color: #6B563F; {anim('0%,' + P(.9) + '{opacity:0}' + P(1.3) + ',100%{opacity:1}')}" dir="rtl">מאחורי הדלת יש גן. בגן פרי אחד.</div>
</div>'''

# ── studio intro (2.6–4.3): the copper line runs into the centre and opens the circle ──
INTRO_LINE = f'M1140 1690 C1000 1500 900 1050 {CX} {CY}'
INTRO = f'''<div style="position: absolute; inset: 0; z-index: 150; pointer-events: none">
  <div style="position: absolute; inset: 0; background: {MARBRE}; {anim('0%,' + P(3.9) + '{opacity:1}' + P(4.5) + ',100%{opacity:0}')}"></div>
  <div style="position: absolute; top: 120px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px; {anim(show(2.65, 4.05, .3))}">
    <div style="{JK}; font-size: 22px; font-weight: 500; letter-spacing: .32em; color: #C4765A" dir="ltr">BRAND WORLDS STUDIO · HAGIT ANTEBI</div>
    <div style="{HE}; font-size: 96px; font-weight: 500; line-height: 1.05; color: #6B563F" dir="rtl">עולם מותג <em style="font-family: 'Cormorant Garamond', serif; font-weight: 400; color: #B8894A">25</em></div></div>
  <div style="position: absolute; top: 1480px; left: 80px; right: 80px; text-align: center; {HE}; font-size: 44px; line-height: 1.35; color: #6B563F; {anim(show(2.8, 4.05, .3))}" dir="rtl">בית בושם.<br>גן אחד מאחורי דלת אחת.</div>
  <svg style="position: absolute; inset: 0" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <g style="{anim(show(2.6, 4.0, .3))}"><path class="line" pathLength="1" d="{INTRO_LINE}" style="{anim('0%,' + P(2.75) + '{stroke-dashoffset:1}' + P(3.55) + ',100%{stroke-dashoffset:0}', 'animation-timing-function:cubic-bezier(.4,0,.3,1)')}"/></g>
    <circle cx="{CX}" cy="{CY}" r="40" fill="none" stroke="#C4765A" stroke-width="3" style="transform-origin: {CX}px {CY}px; {anim('0%,' + P(3.5) + '{opacity:0;transform:scale(1)}' + P(3.6) + '{opacity:1}' + P(4.3) + ',100%{opacity:0;transform:scale(7)}')}"/>
  </svg>
  {ball(INTRO_LINE, 2.75, 3.55)}
</div>'''

# ── outro: her closing line in the studio window, then the CTA; holds to the last frame ──
OUTRO = f'''<div style="position: absolute; inset: 0; z-index: 150; pointer-events: none">
  <div style="position: absolute; top: 100px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
    <div style="{HE}; font-size: 28px; font-weight: 500; letter-spacing: .06em; color: #C4765A; {anim(rise(OUT + .3, 20))}" dir="rtl"><span dir="ltr">VELUNE°</span> · עולם מותג 25</div>
    <div style="{HE}; font-size: 64px; font-weight: 700; line-height: 1.18; color: {INK}; {anim(rise(OUT + .5))}" dir="rtl">עולם מותג אחד.<br><span style="color: {LITCHI}">כל נקודות המגע.</span></div></div>
  <div style="position: absolute; top: 1470px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center; {anim(rise(OUT + 1.0))}">
    <div style="{HE}; font-size: 44px; font-weight: 500; line-height: 1.3; color: #C4765A" dir="rtl">ואצלך, קונים ריח<br>או נכנסים למקום?</div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 20px 56px; background: #6B563F; color: #FAF8F3; border-radius: 12px" dir="rtl"><span style="{HE}; font-size: 36px; font-weight: 500">אבחון פער המותג</span><span style="{HE}; font-size: 22px; opacity: .85">30 דק׳ · בלי עלות</span></div>
    <div style="{JK}; font-size: 22px; letter-spacing: .3em; color: #8B7355" dir="ltr">HAGITANTEBI.CO.IL</div></div>
</div>'''

world_kf = '0%%,%s{transform:scale(1)}%s,100%%{transform:scale(.5)}' % (P(OUT), P(OUT + .8))
html = f'''<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>VELUNE orbit reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&amp;family=David+Libre:wght@400;500;700&amp;family=Assistant:wght@300;400;600&amp;family=Heebo:wght@300;400;500;700&amp;family=Cormorant+Garamond:ital,wght@0,400;1,400&amp;family=Plus+Jakarta+Sans:wght@400;500;700&amp;display=swap">
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
open(os.path.join(HERE, 'reel-long.html' if LONG else 'reel.html'), 'w').write(html)
if LONG:   # the schedule build-long.sh lays the site clips by, and one transparent chip page per card
    import json
    json.dump({'duration': D, 'overlays': OVERLAYS}, open(os.path.join(HERE, 'long-overlays.json'), 'w'), indent=1)
    for k in range(N):
        open(os.path.join(HERE, 'f', 'chip-%d.html' % k), 'w').write(f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@300;700&amp;display=swap"><style>html,body{{margin:0;background:transparent}}</style></head><body><div style="position: relative; width: 1080px; height: 1920px">{chip(k)}</div></body></html>''')
print('ok', len(html))
