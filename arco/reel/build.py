#!/usr/bin/env python3
"""ARCO° · World 13 — the world's 30s studio film.

Hook: a feed of generic, interchangeable room photos scrolls by ("הלקוחה גוללת עוד גלריית עבודות").
Signature scene: קופסת החומרים — the empty room stands in an arched niche; the four materials from the
site's material box (linen, oak, travertine, lime plaster) ride a clockwise dial whose upper half is
the arch itself. Each material that reaches the copper pointer furnishes the room one stage further
(the site's own home film, played in four parts), and the room around the niche takes its colour.
Around it: the sketch that becomes the empty room, the garden, the arched door, six touchpoints, the promise.

Fills the brandos-brand-world-reel template. Every timing lives here, in seconds.
    python3 arco/reel/build.py            -> arco/reel/reel.html
Render (from the repo root):
    node .claude/skills/brandos-brand-world-reel/scripts/render.js arco/reel/reel.html 30 arco/reel/out/ARCO-13.mp4
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TPL = ROOT / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


s = TPL.read_text()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# ── palette, from arco/index.html :root ───────────────────────────────
SAND, INK, BRONZE, OLIVE = '#EFE7DA', '#33302B', '#A87E52', '#6F6D4F'
AS = "font-family: 'Assistant', 'Heebo', sans-serif"
CG = "font-family: 'Cormorant Garamond', serif"
KICK = f"{AS}; font-size: 22px; font-weight: 700; letter-spacing: .4em; color: {BRONZE}"

rep('--w-bg:#F7F0E6;', f'--w-bg:{SAND};')
rep('--w-ink:#3B2E33;', f'--w-ink:{INK};')
rep('--w-accent:#C9878E;', f'--w-accent:{BRONZE};')
rep('Assistant:wght@300;400;600;700', 'Assistant:wght@200;300;400;600;700')
rep('<title>Brand World Reel</title>', '<title>ARCO reel</title>')

# ── studio wrapper ────────────────────────────────────────────────────
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">13</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'סטודיו לעיצוב פנים וחוץ.<br>הגלילה ממלאת את החלל, מחדר ריק לבית.')
rep('BRAND° · עולם מותג NN', '<span dir="ltr">ARCO°</span> · עולם מותג 13')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'את <span dir="ltr">ARCO°</span> מרגישים<br>עוד לפני הפגישה הראשונה.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>מה מרגישים אצלך לפני הפגישה?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 13')

tags = [('01 · The Core', 'כל בית מתחיל בקו.'),
        ('02 · The Visual World', 'קופסת החומרים: כל חומר מוסיף לבית'),
        ('03 · The Narrative', 'הבית ממשיך החוצה'),
        ('04 · Touchpoints', 'כל קשת היא דלת'),
        ('05 · The Promise', 'מחלל. לבית.')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>'); s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i); e = s.index('</span>', k); s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,16.2"'), ('data-show="14.7,18.7"', 'data-show="16.2,19.6"'),
             ('data-show="18.7,22.7"', 'data-show="19.6,24.0"'), ('data-show="22.7,30"', 'data-show="24.0,30"')]:
    rep(a, b)

# ── HOOK: the generic feed (frame 0 already shows the question and the feed) ──
i = s.index('  <div class="hq"'); j = s.index('  <svg class="stack"', i)
tiles = ''.join(f'<img src="img/g{(k % 9) + 1}.jpg" alt="" style="width: 244px; height: 244px; object-fit: cover; display: block; border-radius: 4px">'
                for k in range(18))
HOOK = f"""  <div style="position: absolute; top: 250px; left: 80px; right: 80px; text-align: right; font-size: 76px; font-weight: 600; line-height: 1.18; color: var(--s-dark)" dir="rtl">הלקוחה גוללת עוד<br>גלריית עבודות.<br>למה שתעצור <span style="color: var(--s-copper)">אצלך</span>?</div>
  <div style="position: absolute; top: 610px; left: 150px; width: 780px; height: 900px; box-sizing: border-box; padding: 16px; background: #FFFFFF; border-radius: 24px; box-shadow: 0 24px 60px rgba(62,47,37,.14); display: flex; flex-direction: column; gap: 16px">
    <div style="height: 56px; display: flex; align-items: center; gap: 14px; padding: 0 6px" dir="rtl"><span style="width: 52px; height: 52px; border-radius: 50%; background: #D9D9D9"></span><span style="display: flex; flex-direction: column"><b style="font-size: 24px; color: #2E2A27">עיצוב פנים · פרויקטים</b><span style="font-size: 19px; color: #8E8A86">128 פוסטים</span></span></div>
    <div style="position: relative; flex-grow: 1; overflow: hidden; border-radius: 8px">
      <div class="feed" style="display: grid; grid-template-columns: repeat(3, 244px); gap: 8px">{tiles}</div>
      <span style="position: absolute; top: 14px; right: 14px; padding: 8px 18px; border-radius: 999px; background: #2E2A27; color: #F4F2EF; font-size: 22px" dir="rtl">ככה משווים</span>
    </div>
  </div>
"""
s = s[:i] + HOOK + s[j:]

# ── the materials dial ────────────────────────────────────────────────
MAT = [('linen', 'פשתן', 'LINEN', 'הספה והשטיח', '#DCD2C0'),
       ('oak', 'אלון', 'OAK', 'הכורסה', '#D3B68F'),
       ('trav', 'טרוורטין', 'TRAVERTINE', 'שולחן הסלון', '#E5D3B1'),
       ('plaster', 'טיח', 'LIME PLASTER', 'הקיר, האור והתמונה', '#F3EEE5')]
STEPS = [10.9, 12.0, 13.1, 14.2]       # the ring turns 40° clockwise at each; the room grows 0.4s later
RANGES = [(1, 10), (10, 16), (16, 22), (22, 40)]   # frames of arco/home-m per material
CX, CY, RR, A = 540, 1180, 470, 40      # ring centre, radius, angle between materials
NX, NY, NW, NH = 290, 830, 500, 700     # the arched niche
END_B = 16.4

ang = [-A] + [A * k for k in range(4)]  # -40 → 0 → 40 → 80 → 120: material k under the pointer after step k
ring = f'0%,{P(STEPS[0])}{{transform:rotate({ang[0]}deg)}}'
cr = f'0%,{P(STEPS[0])}{{transform:rotate({-ang[0]}deg)}}'
for k, t in enumerate(STEPS):
    nxt = P(STEPS[k + 1]) if k < 3 else '100%'
    ring += f'{P(t + .5)},{nxt}{{transform:rotate({ang[k + 1]}deg)}}'
    cr += f'{P(t + .5)},{nxt}{{transform:rotate({-ang[k + 1]}deg)}}'
cols = [SAND] + [m[4] for m in MAT]
bg = f'0%,{P(STEPS[0] + .4)}{{background-color:{cols[0]}}}'
for k, t in enumerate(STEPS):
    nxt = P(STEPS[k + 1] + .4) if k < 3 else '100%'
    bg += f'{P(t + .9)},{nxt}{{background-color:{cols[k + 1]}}}'
# the medal under the pointer lights up while it is there
glow = ''
for k, t in enumerate(STEPS):
    out = STEPS[k + 1] if k < 3 else 30
    glow += (f'.mg{k}{{animation-name:mg{k}}}@keyframes mg{k}{{0%,{P(t + .3)}{{transform:scale(1)}}{P(t + .55)},{P(out)}{{transform:scale(1.22)}}'
             f'{P(out + .4)},100%{{transform:scale(1)}}}}')

css = f"""
/* hook: the feed scrolls, then stops */
.feed{{animation-name:feed;animation-timing-function:cubic-bezier(.25,.6,.3,1)}}
@keyframes feed{{0%,{P(.15)}{{transform:translateY(0)}}{P(1.75)},100%{{transform:translateY(-756px)}}}}
/* A · the line, the sketch, the empty room */
.arch{{fill:none;stroke:{BRONZE};stroke-width:5;stroke-linecap:round;stroke-dasharray:1 1;animation-name:arch;animation-timing-function:cubic-bezier(.5,0,.3,1)}}
@keyframes arch{{0%,{P(5.6)}{{stroke-dashoffset:1;opacity:1}}{P(6.9)},{P(7.3)}{{stroke-dashoffset:0;opacity:1}}{P(8.0)},100%{{stroke-dashoffset:0;opacity:0}}}}
.wm{{animation-name:wm}}@keyframes wm{{0%,{P(5.6)}{{opacity:0;letter-spacing:.8em}}{P(6.6)},100%{{opacity:1;letter-spacing:.42em}}}}
.a-l1{{animation-name:al1}}@keyframes al1{{0%,{P(6.0)}{{transform:translateY(110%)}}{P(6.6)},100%{{transform:none}}}}
.a-l2{{animation-name:al2}}@keyframes al2{{0%,{P(7.6)}{{transform:translateY(110%)}}{P(8.2)},100%{{transform:none}}}}
/* B · the dial */
.d-bg{{animation-name:dbg}}@keyframes dbg{{{bg}}}
.d-ring{{animation-name:dring;transform-origin:0 0}}@keyframes dring{{{ring}}}
.d-cr{{animation-name:dcr}}@keyframes dcr{{{cr}}}
{glow}
.b-l1{{animation-name:bl1}}@keyframes bl1{{0%,{P(9.9)}{{transform:translateY(110%)}}{P(10.4)},100%{{transform:none}}}}
.b-l2{{animation-name:bl2}}@keyframes bl2{{0%,{P(10.2)}{{transform:translateY(110%)}}{P(10.7)},100%{{transform:none}}}}
/* C · garden */
.c-l1{{animation-name:cl1}}@keyframes cl1{{0%,{P(16.4)}{{transform:translateY(110%)}}{P(17.0)},100%{{transform:none}}}}
.c-l2{{animation-name:cl2}}@keyframes cl2{{0%,{P(16.9)}{{transform:translateY(110%)}}{P(17.5)},100%{{transform:none}}}}
/* D · the arched door opens */
.leaf{{animation-name:leaf;transform-origin:0 50%;animation-timing-function:cubic-bezier(.55,0,.25,1)}}
@keyframes leaf{{0%,{P(19.75)}{{transform:rotateY(0deg)}}{P(20.45)},100%{{transform:rotateY(-104deg)}}}}
.dpush{{animation-name:dpush}}@keyframes dpush{{0%,{P(19.75)}{{transform:scale(1.1)}}{P(21.3)},100%{{transform:scale(1)}}}}
.dshade{{animation-name:dshade}}@keyframes dshade{{0%,{P(19.75)}{{opacity:1}}{P(20.6)},100%{{opacity:0}}}}
/* E · the promise */
.epush{{animation-name:epush;animation-timing-function:linear}}@keyframes epush{{0%,{P(23.75)}{{transform:scale(1.1)}}100%{{transform:scale(1)}}}}
.e-l1{{animation-name:el1}}@keyframes el1{{0%,{P(24.1)}{{transform:translateY(110%)}}{P(24.7)},100%{{transform:none}}}}
.e-l2{{animation-name:el2}}@keyframes el2{{0%,{P(24.6)}{{transform:translateY(110%)}}{P(25.2)},100%{{transform:none}}}}
"""
rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · ARCO ── */' + css)

GT = lambda h=560: f'<div style="position: absolute; left: 0; right: 0; top: 0; height: {h}px; background: linear-gradient(to bottom, rgba(239,231,218,.96) 40%, rgba(239,231,218,0))"></div>'
GB = lambda h=760: f'<div style="position: absolute; left: 0; right: 0; bottom: 0; height: {h}px; background: linear-gradient(to top, rgba(239,231,218,.96) 42%, rgba(239,231,218,0))"></div>'
IMG = 'position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block'

# A · The Core — the sketch, a line draws the arch, the empty room appears
A_ = f"""<section class="scene" data-show="0,10.1">
    <img src="../sketch-m.webp" alt="" style="{IMG}">
    <div class="stack" data-show="7.2,30" data-fade="0.8"><img src="../home-m/f_001.webp" alt="" style="{IMG}"></div>
    <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="arch" pathLength="1" d="M300 1330 V880 A240 240 0 0 1 780 880 V1330"></path></svg>
    {GT(520)}{GB(700)}
    <div class="wm" style="position: absolute; top: 230px; left: 0; right: 0; text-align: center; {AS}; font-size: 64px; font-weight: 600; letter-spacing: .42em; color: {INK}" dir="ltr">ARCO<span style="color: {BRONZE}">°</span></div>
    <div data-in="6.2" style="position: absolute; top: 330px; left: 0; right: 0; text-align: center; {KICK}" dir="rtl">מחלל. לבית.</div>
    <div style="position: absolute; bottom: 230px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="a-l1" style="display: block; {AS}; font-size: 92px; font-weight: 200; line-height: 1.15; color: {INK}">כל בית מתחיל בקו.</span></span>
      <span class="mask"><span class="a-l2" style="display: block; {AS}; font-size: 58px; font-weight: 300; line-height: 1.3; color: {OLIVE}">ואז בחלל ריק שמקשיבים לו.</span></span>
    </div>
  </section>"""

# B · the materials dial
stages = f'<div class="stack" data-show="9.7,{STEPS[0] + .45:.2f}" data-fade="0.08"><img src="../home-m/f_001.webp" alt="" style="{IMG}"></div>'
for k, ((a, b), t) in enumerate(zip(RANGES, STEPS)):
    end = (STEPS[k + 1] + .45) if k < 3 else END_B
    stages += (f'<div class="stack" data-show="{t + .38:.2f},{end:.2f}" data-fade="0.08"><div class="stack" data-seq="../home-m/f_%03d.webp" '
               f'data-from="{a}" data-to="{b}" data-start="{t + .4:.2f}" data-step="0.055" data-pos="50% 55%"></div></div>')
medals = ''.join(f"""<div style="position: absolute; left: 0; top: 0; transform: rotate({-A * i}deg) translateY(-{RR}px) rotate({A * i}deg)"><div class="d-cr" style="position: absolute; left: -66px; top: -66px; width: 132px; height: 132px"><div class="mg{i}" style="width: 132px; height: 132px; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 4px #FBF8F2, 0 0 0 6px {BRONZE}, 0 14px 30px rgba(51,48,43,.22)"><img src="img/m_{f}.jpg" alt="{he}" style="width: 100%; height: 100%; display: block"></div></div></div>"""
                 for i, (f, he, en, what, c) in enumerate(MAT))
wins = [(9.9, STEPS[0] + .5)] + [(t + .5, (STEPS[k + 1] + .5) if k < 3 else 15.1) for k, t in enumerate(STEPS)]
LBL = 'display: flex; flex-direction: column; align-items: center; gap: 8px; text-align: center'
labels = (f'<div class="stack" data-show="{wins[0][0]},{wins[0][1]}" data-fade="0.18" style="{LBL}"><span style="{KICK}" dir="rtl">קופסת החומרים</span>'
          f'<span style="{AS}; font-size: 36px; font-weight: 300; line-height: 1.3; color: {INK}" dir="rtl">טיח, אלון, טרוורטין ופשתן.<br>כל חומר מוסיף לחדר.</span></div>')
for (f, he, en, what, c), (a, b) in zip(MAT, wins[1:]):
    labels += (f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.18" style="{LBL}"><span style="{AS}; font-size: 20px; font-weight: 700; letter-spacing: .4em; color: {BRONZE}" dir="ltr">{en}</span>'
               f'<span style="{AS}; font-size: 72px; font-weight: 300; line-height: 1; color: {INK}" dir="rtl">{he} <span style="color: {BRONZE}">←</span> {what}</span></div>')
labels += (f'<div class="stack" data-show="15.1,30" data-fade="0.25" style="{LBL}"><span style="{AS}; font-size: 20px; font-weight: 700; letter-spacing: .4em; color: {BRONZE}" dir="ltr">A R C O °</span>'
           f'<span style="{AS}; font-size: 84px; font-weight: 600; line-height: 1; color: {INK}" dir="rtl">מחלל. לבית.</span></div>')
B_ = f"""<section class="scene" data-show="9.7,{END_B}">
    <div class="stack d-bg" style="background-color: {SAND}"></div>
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="b-l1" style="display: block; {AS}; font-size: 70px; font-weight: 200; line-height: 1.15; color: {INK}">חדר אחרי חדר,</span></span>
      <span class="mask"><span class="b-l2" style="display: block; {AS}; font-size: 70px; font-weight: 600; line-height: 1.15; color: {INK}">פרט אחרי פרט.</span></span>
    </div>
    <div style="position: absolute; left: {CX - RR}px; top: {CY - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(168,126,82,.5); box-sizing: border-box"></div>
    <div style="position: absolute; left: {NX}px; top: {NY}px; width: {NW}px; height: {NH}px; border-radius: {NW // 2}px {NW // 2}px 18px 18px; overflow: hidden; background: {SAND}; box-shadow: 0 0 0 10px #FBF8F2, 0 0 0 12px {BRONZE}, 0 36px 80px rgba(51,48,43,.24)">
      {stages}
    </div>
    <div class="d-ring" style="position: absolute; left: {CX}px; top: {CY}px; width: 0; height: 0">{medals}</div>
    <div style="position: absolute; top: {CY - RR - 66 - 48}px; left: {CX - 18}px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 28px solid var(--s-copper)"></div>
    <div style="position: absolute; top: 1716px; left: 40px; right: 40px; height: 150px">{labels}</div>
  </section>"""

# C · the garden
C_ = f"""<section class="scene" data-show="16.1,19.8">
    <div class="stack" data-seq="../garden-m/f_%03d.webp" data-from="1" data-to="61" data-by="2" data-start="16.3" data-step="0.06" data-pos="50% 50%"></div>
    {GT(620)}{GB(520)}
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="c-l1" style="display: block; {AS}; font-size: 62px; font-weight: 200; line-height: 1.2; color: {INK}">והבית לא נגמר בקיר האחרון —</span></span>
      <span class="mask"><span class="c-l2" style="display: block; {AS}; font-size: 84px; font-weight: 600; line-height: 1.15; color: {INK}">הוא ממשיך החוצה.</span></span>
    </div>
    <div data-in="17.6" style="position: absolute; bottom: 220px; left: 0; right: 0; text-align: center; {AS}; font-size: 44px; font-weight: 300; color: {INK}" dir="rtl">הגינה היא עוד מרחב לאירוח.</div>
  </section>"""

# D · the arched door, then six touchpoints
ARCH = 'border-radius: 50% 50% 8px 8px / 34% 34% 3% 3%'
names = ['המצגת', 'קופסת החומרים', 'הגדר באתר', 'הכרטיס', 'הפיד', 'מסירת המפתח']
grid = ''.join(f"""<div data-in="{21.45 + i * .12:.2f}" style="display: flex; flex-direction: column; align-items: center; gap: 12px; width: 290px"><div style="width: 290px; height: 380px; {ARCH}; overflow: hidden; box-shadow: 0 18px 40px rgba(51,48,43,.18)"><img src="../touch/0{i + 1}.webp" alt="{n}" style="width: 100%; height: 100%; object-fit: cover; display: block"></div><div style="{AS}; font-size: 28px; color: {INK}" dir="rtl"><span style="color: {BRONZE}; font-weight: 700" dir="ltr">N°0{i + 1}</span> · {n}</div></div>"""
               for i, n in enumerate(names))
D_ = f"""<section class="scene" data-show="19.4,24.1">
    <div class="stack" style="background: {SAND}"></div>
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 14px" dir="rtl">
      <div data-in="19.5" style="{AS}; font-size: 84px; font-weight: 600; line-height: 1.1; color: {INK}">כל קשת היא דלת.</div>
      <div data-in="19.8" style="{AS}; font-size: 40px; font-weight: 300; line-height: 1.35; color: {OLIVE}">מאחורי כל אחת — בית שכבר הקשבנו לו.</div>
    </div>
    <div style="position: absolute; left: 250px; top: 560px; width: 580px; height: 920px; perspective: 1800px">
      <div style="position: absolute; inset: 0; {ARCH}; overflow: hidden; background: #8D7B63; box-shadow: inset 0 8px 30px rgba(0,0,0,.42)">
        <img class="dpush" src="../projects/01.webp" alt="" style="{IMG}; object-position: 50% 50%">
        <div class="dshade" style="position: absolute; inset: 0; background: linear-gradient(255deg, rgba(0,0,0,.45), rgba(0,0,0,0) 60%)"></div>
      </div>
      <div class="leaf" style="position: absolute; inset: 0; {ARCH}; overflow: hidden; background: linear-gradient(100deg, #E6DBC8, #D3C3AA); box-shadow: inset 0 0 0 1px rgba(51,48,43,.12)">
        <div style="position: absolute; left: 38px; right: 38px; top: 38px; bottom: 38px; border: 2px solid rgba(168,126,82,.55); {ARCH}"></div>
        <div style="position: absolute; right: 70px; top: 520px; width: 16px; height: 16px; border-radius: 50%; background: {BRONZE}"></div>
      </div>
      <div style="position: absolute; left: 8%; right: 8%; bottom: -28px; height: 28px; background: radial-gradient(60% 100% at 50% 0, rgba(51,48,43,.24), transparent 72%)"></div>
    </div>
    <div class="stack" data-show="21.35,30" data-fade="0.3" style="background: {SAND}">
      <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center; gap: 6px" dir="rtl">
        <div style="{AS}; font-size: 70px; font-weight: 200; line-height: 1.15; color: {INK}">שישה רגעים, שפה אחת:</div>
        <div style="{AS}; font-size: 70px; font-weight: 600; line-height: 1.15; color: {INK}">קשת, טיח ואלון.</div>
      </div>
      <div style="position: absolute; top: 520px; left: 80px; width: 920px; display: flex; flex-wrap: wrap; justify-content: space-between; row-gap: 46px" dir="rtl">{grid}</div>
      <div data-in="22.3" style="position: absolute; top: 1600px; left: 0; right: 0; text-align: center; {AS}; font-size: 36px; font-weight: 300; color: {OLIVE}" dir="rtl">מהמצגת הראשונה ועד מסירת המפתח.</div>
    </div>
  </section>"""

# E · the promise
E_ = f"""<section class="scene" data-show="23.75,30">
    <div class="stack" style="overflow: hidden"><img class="epush" src="../home-m/f_040.webp" alt="" style="{IMG}"></div>
    {GT(640)}{GB(620)}
    <div style="position: absolute; top: 230px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center" dir="rtl">
      <span class="mask"><span class="e-l1" style="display: block; {AS}; font-size: 76px; font-weight: 200; line-height: 1.18; color: {INK}">אנחנו לא ממלאים חדרים.</span></span>
      <span class="mask"><span class="e-l2" style="display: block; {AS}; font-size: 84px; font-weight: 600; line-height: 1.18; color: {INK}">אנחנו מעירים אותם.</span></span>
    </div>
    <div data-in="25.3" style="position: absolute; bottom: 230px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 12px">
      <div style="{AS}; font-size: 60px; font-weight: 600; letter-spacing: .42em; color: {INK}" dir="ltr">ARCO<span style="color: {BRONZE}">°</span></div>
      <div style="{KICK}" dir="rtl">עיצוב פנים וחוץ · מחלל. לבית.</div>
    </div>
  </section>"""

i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A_, B_, C_, D_, E_]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
(HERE / 'reel.html').write_text(s)
print('ok', len(s))
