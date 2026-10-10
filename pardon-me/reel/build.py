#!/usr/bin/env python3
"""PARDON ME° · World 29 — studio reel that opens with the tear.

Fills the brandos-brand-world-reel template. Every timing lives here, in seconds.
    python3 pardon-me/reel/build.py            -> pardon-me/reel/reel.html
Render (from the repo root):
    node .claude/skills/brandos-brand-world-reel/scripts/render.js pardon-me/reel/reel.html 30 pardon-me/reel/out/PARDON-ME-29.mp4
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TPL = ROOT / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


css = []      # world-specific keyframes
A = '../assets/'

# ── palette ────────────────────────────────────────────────────────────
PORC, GARDEN, LIME, BLUE, PETAL, BERRY, INK = '#F3EDE2', '#1E3A2B', '#CFE06A', '#B9D3E8', '#F2C4CE', '#9B1B47', '#1B1F1C'
FONTS = ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500'
         '&amp;family=Heebo:wght@300;400;500;600;700;900&amp;family=Assistant:wght@300;400;600;700'
         '&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;family=Bodoni+Moda:ital,opsz,wght@0,6..96,400;1,6..96,400'
         '&amp;family=Frank+Ruhl+Libre:wght@400;500&amp;family=Archivo+Narrow:wght@700&amp;display=swap')

BASE_CSS = f'''
.bod{{font-family:'Bodoni Moda','Cormorant Garamond',serif}}
.frl{{font-family:'Frank Ruhl Libre','Heebo',serif}}
.loud{{font-family:'Archivo Narrow','Heebo',sans-serif;font-weight:700;text-transform:uppercase;letter-spacing:-.005em}}
.wm{{font-family:'Bodoni Moda',serif;letter-spacing:.28em;display:inline-flex;align-items:center;white-space:nowrap;color:{GARDEN};direction:ltr}}
.wm .o{{display:inline-block;width:.62em;height:.86em;border-radius:50%;border:.06em solid currentColor;background:url({A}print-bad-influence.webp) center/cover;margin:0 .02em}}
.ctr{{position:absolute;left:0;right:0;text-align:center}}
.pill{{display:inline-block;background:{PORC};color:{GARDEN};padding:14px 30px;border-radius:999px}}
'''


def kf(name, frames):
    """frames: list of (seconds, css-body). Writes @keyframes with held values."""
    body = ''.join(f'{P(t)}{{{v}}}' for t, v in frames)
    css.append(f'.{name}{{animation-name:{name}}}@keyframes {name}{{0%{{{frames[0][1]}}}{body}100%{{{frames[-1][1]}}}}}')
    return name


# ── HOOK (0–2.8s): the polite sleeve, the cut, the tear ───────────────
T0, T1 = 1.15, 1.75          # tear starts / ends
CUT0 = 0.55                  # scissors start along the perforation
zig_top = ','.join(['0% 0%', '100% 0%'] + [f'{k / 48 * 100:.2f}% calc(100% - {0 if k % 2 else 16}px)' for k in range(48, -1, -1)])
zig_bot = ','.join(['0% 100%', '100% 100%'] + [f'{k / 48 * 100:.2f}% {0 if k % 2 else 16}px' for k in range(48, -1, -1)])
kf('tTop', [(T0, 'transform:none'), (T1, 'transform:translateY(-1180px) rotate(-7deg)')])
kf('tBot', [(T0, 'transform:none'), (T1, 'transform:translateY(1180px) rotate(6deg)')])
kf('scis', [(CUT0 - .05, 'offset-distance:0%;opacity:0'), (CUT0, 'offset-distance:0%;opacity:1'), (T0, 'offset-distance:100%;opacity:1'), (T0 + .15, 'offset-distance:100%;opacity:0')])
kf('cutLine', [(CUT0, 'stroke-dashoffset:1'), (T0, 'stroke-dashoffset:0')])
kf('perf', [(T0, 'opacity:1'), (T0 + .2, 'opacity:0')])
kf('tearPill', [(0.0, 'opacity:1;transform:none'), (0.3, 'opacity:1;transform:rotate(-4deg)'), (0.45, 'opacity:1;transform:rotate(4deg)'), (CUT0, 'opacity:1;transform:none'), (CUT0 + .15, 'opacity:0;transform:none')])
kf('burst', [(T1 - .2, 'opacity:0;transform:scale(1.3)'), (T1 + .2, 'opacity:1;transform:none')])
kf('burstSub', [(T1 + .1, 'opacity:0;transform:translateY(20px)'), (T1 + .45, 'opacity:1;transform:none')])
kf('burstImg', [(0, 'transform:scale(1.14)'), (3.0, 'transform:scale(1)')])

HOOK = f'''<!-- HOOK (0–2.8s): the polite sleeve gets cut and torn; NOT SORRY. bursts out. Frame 0 = question + sleeve + "Tear here". -->
<div class="hook stack" style="background:{BERRY}">
  <div class="stack" style="overflow:hidden"><img class="cover burstImg" src="{A}ad-bad-decisions.webp" alt=""></div>
  <div class="stack" style="background:linear-gradient(180deg,rgba(27,31,28,.0) 30%,rgba(155,27,71,.55) 100%)"></div>
  <div class="ctr burst" style="top:1150px;direction:ltr"><span class="loud" style="display:inline-block;font-size:200px;line-height:.86;white-space:nowrap;color:{PORC};background:{BERRY};padding:12px 34px 4px">Not sorry.</span></div>
  <div class="ctr burstSub" style="top:1400px;direction:ltr"><span class="bod" style="display:inline-block;font-style:italic;font-size:46px;color:{GARDEN};background:{LIME};padding:6px 26px">Smells like bad decisions. The good kind.</span></div>

  <div class="stack tTop" style="background:{PORC};height:976px;bottom:auto;clip-path:polygon({zig_top})">
    <div class="ctr" style="top:640px"><span class="wm" style="font-size:34px">PARD<span class="o"></span>N ME</span></div>
    <div class="ctr bod" style="top:710px;font-style:italic;font-size:92px;line-height:1;color:{GARDEN};direction:ltr">Pardon the interruption.</div>
  </div>
  <div class="stack tBot" style="background:{PORC};top:944px;clip-path:polygon({zig_bot})">
    <div class="ctr frl" style="top:110px;font-size:44px;color:{GARDEN}" dir="rtl">סליחה על ההפרעה.</div>
    <div class="ctr" style="top:780px;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:34px;color:#6B563F;direction:ltr">Brand Worlds Studio · Hagit Antebi</div>
  </div>
  <svg class="stack perf" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <line x1="0" y1="960" x2="1080" y2="960" stroke="{GARDEN}" stroke-opacity=".45" stroke-width="3" stroke-dasharray="14 12"/>
    <path class="cutLine" d="M1040 960 H40" pathLength="1" stroke="{BERRY}" stroke-width="5" fill="none" stroke-dasharray="1 1"/>
  </svg>
  <div class="ctr tearPill" style="top:922px"><span class="loud" style="display:inline-block;background:{GARDEN};color:{PORC};font-size:34px;letter-spacing:.18em;padding:18px 40px;border-radius:999px;direction:ltr">✂ Tear here</span></div>
  <div class="scis" style="position:absolute;left:0;top:0;offset-path:path('M1040 960 H40');offset-rotate:0deg;font-size:76px;color:{BERRY};line-height:1;transform:scaleX(-1)">✂</div>

  <!-- the question: sits on the sleeve at frame 0, stays on its own card after the tear -->
  <div class="ctr" style="top:150px">
    <div style="display:inline-block;background:{PORC};padding:34px 60px 40px;border-radius:28px;box-shadow:0 24px 60px rgba(27,31,28,.18)" dir="rtl">
      <div class="frl" style="font-size:96px;line-height:1.1;color:{GARDEN};font-weight:500">המותג שלך<br><span style="color:{BERRY}">מנומס</span> מדי?</div>
    </div>
  </div>
</div>
'''

# ── A · The Core (0–10.1s): the window on the sleeve grows to the print ─
G0, G1 = 6.8, 8.4
kf('grow', [(G0, 'clip-path:ellipse(150px 225px at 540px 1090px)'), (G1, 'clip-path:ellipse(1500px 2100px at 540px 1090px)')])
kf('ringA', [(G0, 'opacity:1'), (G0 + .4, 'opacity:0')])
kf('notA', [(G1 - .1, 'opacity:0;transform:scale(1.15)'), (G1 + .35, 'opacity:1;transform:none')])
prints = ['print-well-hello', 'print-none-of-your-business', 'print-high-maintenance', 'print-bad-influence']
cyc = [(0, 3.7), (3.7, 4.9), (4.9, 6.1), (6.1, 10.2)]
pr_html = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.3" style="background:url({A}{p}.webp) center/cover"></div>' for p, (a, b) in zip(prints, cyc))
SCENE_A = f'''  <section class="scene" data-show="0,10.1">
    <div class="stack" style="background:{PORC}"></div>
    <div class="ctr" style="top:330px"><span class="wm" style="font-size:44px">PARD<span class="o"></span>N ME</span></div>
    <div class="ctr bod" style="top:420px;font-style:italic;font-size:104px;line-height:1;color:{GARDEN};direction:ltr">Nice on the outside.</div>
    <div class="ctr frl" style="top:1400px;font-size:46px;line-height:1.4;color:{GARDEN}" dir="rtl">מותג עם נימוסים מצוינים<br>וכוונות לא כל כך תמימות.</div>
    <div class="stack grow">{pr_html}</div>
    <div class="ringA" style="position:absolute;left:390px;top:865px;width:300px;height:450px;border:2px solid {GARDEN};border-radius:50%;box-sizing:border-box"></div>
    <div class="ctr notA" style="top:760px;direction:ltr"><span class="loud" style="display:inline-block;font-size:150px;line-height:.9;color:{PORC};background:{BERRY};padding:10px 30px 2px">Not sorry<br>inside.</span></div>
    <div class="ctr notA" style="top:1120px"><span class="frl" style="display:inline-block;font-size:50px;color:{GARDEN};background:{LIME};padding:8px 30px" dir="rtl">מנומס מבחוץ. לא מתנצל מבפנים.</span></div>
  </section>'''

# ── B · The Visual World (9.7–16.2s): written twice — the window reveals the truth ─
STOPS = [
    (10.0, 'ad-bad-decisions', 'A lovely candle<br>for a calm evening.', 'Smells like<br>bad decisions.', 'The good kind.'),
    (12.05, 'ad-touch-yourself', 'A nourishing<br>hand cream.', 'Touch<br>yourself.', "It's skincare."),
    (14.1, 'ad-i-kept-it', 'A thoughtful gift<br>for someone special.', 'I bought you<br>something.', 'I kept it.'),
]
CW, CH, CX, CY = 760, 950, 160, 470          # the ad card
kf('bgB', [(11.95, f'background-color:{BERRY}'), (12.15, f'background-color:{LIME}'), (14.0, f'background-color:{LIME}'), (14.2, f'background-color:{PETAL}')])
stops_html = ''
for i, (s, img, polite, truth, sub) in enumerate(STOPS):
    e = 16.25 if i == 2 else s + 2.05
    kf(f'lens{i}', [(s + .15, 'clip-path:ellipse(0px 0px at 22% 82%)'), (s + .35, 'clip-path:ellipse(115px 165px at 26% 80%)'),
                    (s + .8, 'clip-path:ellipse(115px 165px at 50% 62%)'), (s + 1.0, 'clip-path:ellipse(115px 165px at 50% 62%)'),
                    (s + 1.4, 'clip-path:ellipse(900px 1250px at 50% 55%)')])
    kf(f'lring{i}', [(s + .15, 'opacity:0;transform:translate(-30px,190px) scale(.2)'), (s + .35, 'opacity:1;transform:translate(-182px,171px)'),
                     (s + .8, 'opacity:1;transform:translate(0px,0px)'), (s + 1.0, 'opacity:1;transform:translate(0px,0px)'),
                     (s + 1.25, 'opacity:0;transform:translate(0px,0px) scale(2.2)')])
    kf(f'strike{i}', [(s + .55, 'transform:scaleX(0)'), (s + .85, 'transform:scaleX(1)')])
    kf(f'truthT{i}', [(s + 1.25, 'opacity:0;transform:translateY(24px)'), (s + 1.55, 'opacity:1;transform:none')])
    stops_html += f'''
    <div class="stack" data-show="{s},{e}" data-fade="0.2">
      <div style="position:absolute;left:{CX}px;top:{CY}px;width:{CW}px;height:{CH}px;background:{PORC};border-radius:22px;overflow:hidden;box-shadow:0 40px 90px rgba(27,31,28,.28)">
        <div class="ctr" style="top:90px"><span class="wm" style="font-size:26px">PARD<span class="o"></span>N ME</span></div>
        <div class="ctr" style="top:170px"><span class="bod" style="position:relative;display:inline-block;font-style:italic;font-size:62px;line-height:1.12;color:{GARDEN};direction:ltr">{polite}<span class="strike{i}" style="position:absolute;left:-12px;right:-12px;top:50%;height:7px;background:{BERRY};transform-origin:left"></span></span></div>
        <div class="stack lens{i}"><img class="cover" src="{A}{img}.webp" alt="">
          <div class="ctr truthT{i}" style="top:70px;direction:ltr;padding:0 40px"><span class="loud" style="font-size:96px;line-height:1.02;color:{PORC};background:{BERRY};padding:0 14px;-webkit-box-decoration-break:clone;box-decoration-break:clone">{truth}</span><br><span class="bod" style="display:inline-block;margin-top:18px;font-style:italic;font-size:46px;color:{GARDEN};background:{LIME};padding:4px 22px">{sub}</span></div>
        </div>
        <div class="lring{i}" style="position:absolute;left:{CW // 2 - 115}px;top:{int(CH * .62) - 165}px;width:230px;height:330px;border:3px solid {PORC};border-radius:50%;box-sizing:border-box;box-shadow:0 0 0 2px rgba(30,58,43,.35)"></div>
      </div>
      <div class="ctr" style="top:{CY + CH + 46}px"><span class="pill frl" style="font-size:40px" dir="rtl">כתוב פעמיים · {i + 1}/3</span></div>
    </div>'''
SCENE_B = f'''  <section class="scene" data-show="9.7,16.3">
    <div class="stack bgB"></div>
    <div class="ctr" style="top:236px;direction:ltr"><span class="loud" style="display:inline-block;font-size:104px;line-height:.92;color:{PORC};background:{GARDEN};padding:8px 22px 2px">Good manners.</span><br><span class="loud" style="display:inline-block;font-size:104px;line-height:.92;color:{BERRY};background:{PORC};padding:8px 22px 2px">Bad habits.</span></div>{stops_html}
  </section>'''

# ── C · The Element (15.95–20.9s): four collections, each takes off its sleeve ─
COLLS = [(16.2, 'well-hello', 'print-well-hello', 'Well, Hello.', 'Citrus · Blossom · Green Leaves', BLUE),
         (17.35, 'none-of-your-business', 'print-none-of-your-business', 'None of Your Business.', 'Fig · Amber · Wood', GARDEN),
         (18.5, 'high-maintenance', 'print-high-maintenance', 'High Maintenance.', 'Rose · Musk · Vanilla', PETAL),
         (19.65, 'bad-influence', 'print-bad-influence', 'Bad Influence.', 'Berry · Pink Pepper · Blossom', LIME)]
bgC = []
for k, (t, *_r, col) in enumerate(COLLS):
    bgC += [(t - .1 if k else 0, f'background-color:{col}'), ((COLLS[k + 1][0] - .15) if k < 3 else 21, f'background-color:{col}')]
kf('bgC', bgC)
NW, NH, NX, NY = 700, 875, 190, 430           # the arched niche
coll_html = ''
for k, (t, img, pr, name, notes, col) in enumerate(COLLS):
    e = 20.95 if k == 3 else COLLS[k + 1][0] + .25
    kf(f'slv{k}', [(t + .3, 'transform:none'), (t + .75, f'transform:translateY(-{NH + 40}px)')])
    coll_html += f'''
    <div class="stack" data-show="{t - .05},{e}" data-fade="0.25">
      <div style="position:absolute;left:{NX}px;top:{NY}px;width:{NW}px;height:{NH}px;border-radius:{NW // 2}px {NW // 2}px 26px 26px;overflow:hidden;box-shadow:0 40px 90px rgba(27,31,28,.25)">
        <img class="cover" src="{A}{img}.webp" alt="">
        <div class="stack slv{k}" style="background:url({A}{pr}.webp) center/cover">
          <div class="stack" style="background:{PORC};-webkit-mask-image:radial-gradient(130px 190px at 50% 60%,transparent 98%,#000 100%);mask-image:radial-gradient(130px 190px at 50% 60%,transparent 98%,#000 100%)">
            <div class="ctr" style="top:150px"><span class="wm" style="font-size:28px">PARD<span class="o"></span>N ME</span></div>
            <div class="ctr bod" style="top:205px;font-style:italic;font-size:48px;color:{GARDEN};direction:ltr">{name}</div>
          </div>
        </div>
      </div>
      <div class="ctr" style="top:{NY + NH + 40}px"><div style="display:inline-block;background:{PORC};padding:22px 46px;border-radius:18px"><div class="bod" style="font-style:italic;font-size:66px;line-height:1.1;color:{GARDEN};direction:ltr">{name}</div><div style="margin-top:10px;font-size:24px;letter-spacing:.24em;text-transform:uppercase;color:{BERRY};direction:ltr">{notes}</div></div></div>
    </div>'''
SCENE_C = f'''  <section class="scene" data-show="15.95,20.95">
    <div class="stack bgC"></div>
    <div class="ctr" style="top:236px"><span class="frl" style="display:inline-block;background:{PORC};color:{GARDEN};font-size:66px;line-height:1.2;padding:12px 34px;border-radius:16px" dir="rtl">ארבעה ריחות. אותו חוץ מנומס.</span></div>{coll_html}
  </section>'''

# ── D · Touchpoints (20.6–24.4s): the sleeve comes off, the poster, the bag ─
kf('pushD', [(22.3, 'transform:scale(1.08)'), (24.4, 'transform:scale(1)')])
SCENE_D = f'''  <section class="scene" data-show="20.6,24.45">
    <div class="stack" style="background:{PETAL}"></div>
    <div class="stack" data-seq="seq/rv_%03d.jpg" data-from="1" data-to="33" data-by="1" data-start="20.75" data-step="0.05" data-fit="cover" data-pos="50% 50%"></div>
    <div class="stack" data-show="22.35,23.75" data-fade="0.4" style="overflow:hidden"><img class="cover pushD" src="{A}poster.webp" alt="" style="object-position:50% 45%"></div>
    <div class="stack" data-show="23.45,24.45" data-fade="0.4" style="overflow:hidden"><img class="cover" src="{A}bag.webp" alt="" style="object-position:50% 50%"></div>
    <div class="stack" style="background:linear-gradient(180deg,transparent 70%,rgba(27,31,28,.35) 100%)"></div>
    <div class="ctr" style="top:1660px"><span class="frl pill" style="font-size:50px" dir="rtl">חלון אחד, בכל מקום.</span></div>
  </section>'''

# ── E · The Promise (24.1–30s): calm and centred; stays inside the window for the outro ─
SCENE_E = f'''  <section class="scene" data-show="24.1,30">
    <div class="stack" style="background:{PORC}"></div>
    <div class="ctr" style="top:700px" data-in="23.85"><span class="wm" style="font-size:76px">PARD<span class="o"></span>N ME</span></div>
    <div class="ctr bod" style="top:840px;font-style:italic;font-size:84px;line-height:1;color:{GARDEN};direction:ltr" data-in="24.15">Nice on the outside.</div>
    <div class="ctr" style="top:960px;direction:ltr" data-in="24.45"><span class="loud" style="display:inline-block;font-size:110px;line-height:.9;color:{PORC};background:{BERRY};padding:8px 24px 2px">Not sorry inside.</span></div>
    <div class="ctr frl" style="top:1110px;font-size:46px;color:{GARDEN}" dir="rtl" data-in="24.75">I'm Not Sorry. מנומס מבחוץ, לא מתנצל מבפנים.</div>
  </section>'''

WORLD = '\n'.join([SCENE_A, SCENE_B, SCENE_C, SCENE_D, SCENE_E])

HUD_TAGS = [((5.6, 9.9), '01 · The Core', 'מנומס מבחוץ, לא מתנצל מבפנים'),
            ((9.9, 16.2), '02 · The Visual World', 'כתוב פעמיים: בנימוס, ובאמת'),
            ((16.2, 20.8), '03 · The Element', 'השרוול יורד. לכל קולקציה סוד'),
            ((20.8, 24.1), '04 · Touchpoints', 'חלון אחד, בכל מקום'),
            ((24.1, 30), '05 · The Promise', "I'm Not Sorry.")]

# ── assemble from the template ─────────────────────────────────────────
t = TPL.read_text(encoding='utf-8')
t = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^"]*">', f'<link rel="stylesheet" href="{FONTS}">', t)
t = t.replace("--w-bg:#F7F0E6;", f"--w-bg:{PORC};").replace("--w-ink:#3B2E33;", f"--w-ink:{GARDEN};").replace("--w-accent:#C9878E;", f"--w-accent:{BERRY};")
t = t.replace("--w-display:'Cormorant Garamond',serif;", "--w-display:'Bodoni Moda','Cormorant Garamond',serif;")
t = t.replace('<title>Brand World Reel</title>', '<title>PARDON ME° · Brand World Reel · World 29</title>')
t = t.replace('/* ── WORLD scenes: EDIT — add each scene\'s own motion here (percent = s/30*100) ── */',
              '/* ── WORLD scenes (generated by build.py) ── */\n' + BASE_CSS + '\n'.join(css))
# studio intro + outro copy
t = t.replace('עולם מותג <em style="font-family: \'Cormorant Garamond\', serif; font-weight: 400; color: var(--s-gold)">NN</em>',
              'עולם מותג <em style="font-family: \'Cormorant Garamond\', serif; font-weight: 400; color: var(--s-gold)">29</em>')
t = t.replace('EDIT: משפט אחד על העולם, מתוך האתר.', 'מנומס מבחוץ, לא מתנצל מבפנים.<br>שרוול שמנת אחד, חלון אחד, ומסיבה מאחוריו.')
t = t.replace('BRAND° · עולם מותג NN', '<span dir="ltr">PARDON ME°</span> · עולם מותג 29')
t = t.replace('EDIT: התשובה להוק.<br>שורה שנייה.', 'את <span dir="ltr">PARDON ME°</span><br>לא שוכחים.')
t = t.replace('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ומה המותג שלך מסתיר<br>מאחורי החזית המנומסת?')
# world scenes
t = re.sub(r'(<div class="world stack"[^>]*>\n).*?(\n</div>\n\n<!-- HOOK)', lambda m: m.group(1) + WORLD + m.group(2), t, flags=re.S)
# hook
t = re.sub(r'<!-- HOOK \(0–2\.8s\)\. EDIT.*?(\n<!-- STUDIO · layer tag)', lambda m: HOOK + m.group(1), t, flags=re.S)
# HUD
t = t.replace('Brand Worlds Studio · עולם מותג NN</div>', 'Brand Worlds Studio · עולם מותג 29</div>')
hud = re.search(r'(<div style="position: relative; flex-grow: 1">\n)(.*?)(\n  </div>\n</div>)', t, flags=re.S)
tags = '\n'.join(f'    <div class="stack" data-show="{a},{b}" data-fade="0.2" style="display: flex; flex-direction: column; gap: 2px"><span style="font-family: \'Cormorant Garamond\', serif; font-size: 34px; line-height: 1; color: var(--s-ink)" dir="ltr">{h}</span><span style="font-size: 22px; color: var(--s-ink)">{s}</span></div>'
                 for (a, b), h, s in HUD_TAGS)
t = t[:hud.start(2)] + tags + t[hud.end(2):]
t = re.sub(r'<!--([^>]*?)EDIT[^>]*?-->', lambda m: '<!--' + m.group(1).rstrip(' (') + ' -->', t)
left = [l.strip()[:80] for l in t.split('<body')[1].split('\n') if 'EDIT' in l]
assert not left, left
(HERE / 'reel.html').write_text(t, encoding='utf-8')
print('wrote', HERE / 'reel.html')
