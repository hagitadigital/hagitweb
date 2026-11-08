"""Series "ככה בוחרים" (Oct 2026) — 15s episodes in the studio frame, with the copper thread and ball running through each one.
Builds ep01-pancakerie.html and ep02-chasen.html (1080×1920). Cue points come from ../audio/README.md.
Render: node <skill>/scripts/render.js ep01-pancakerie.html 15 ../ep01-silent.mp4
Every time is in seconds. anim() turns (t, css) stops into keyframes on the 15s timeline.
"""
import math
import sys

sys.dont_write_bytecode = True   # the reel engine is imported from ../ux-reels; keep no __pycache__ in the repo
from pathlib import Path

D = 15
HERE = Path(__file__).parent
_css = []
_n = [0]

BALL_BG = 'radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)'


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


def anim(stops):
    """stops: [(t, 'css decls'), …] → animation-name. Holds the first value before and the last value after."""
    _n[0] += 1
    k = f'a{_n[0]}'
    body = ''.join(f'{P(t)}{{{c}}}' for t, c in stops)
    _css.append(f'@keyframes {k}{{0%{{{stops[0][1]}}}{body}100%{{{stops[-1][1]}}}}}')
    return k


def show(a, b, f=.25):
    """visible between a and b (fade f)."""
    st = [(0, 'opacity:0')] if a > 0 else [(0, 'opacity:1')]
    if a > 0:
        st += [(a - f, 'opacity:0'), (a, 'opacity:1')]
    if b < D:
        st += [(b, 'opacity:1'), (b + f, 'opacity:0')]
    return anim(st)


def rise(t, d=.5, dy=34):
    return anim([(t, f'opacity:0;transform:translateY({dy}px)'), (t + d, 'opacity:1;transform:none')])


def ball(stops, size=96, z=30):
    """stops: [(t, x, y)] centre positions in stage px."""
    k = anim([(t, f'transform:translate({x}px,{y}px)') for t, x, y in stops])
    s = size
    return f"""<div style="position: absolute; left: {-s // 2}px; top: {-s // 2}px; width: {s}px; height: {s}px; z-index: {z}; animation-name: {k}">
  <div style="position: absolute; inset: 0; border-radius: 50%; background: rgba(246,239,229,.55); border: 1.5px solid #D8CCBD; box-shadow: 0 10px 26px rgba(62,40,24,.3)"></div>
  <div style="position: absolute; left: {s * .13:.0f}px; top: {s * .13:.0f}px; width: {s * .74:.0f}px; height: {s * .74:.0f}px; border-radius: 50%; background: {BALL_BG}"></div>
  <div style="position: absolute; left: {s * .26:.0f}px; top: {s * .44:.0f}px; width: {s * .13:.0f}px; height: {s * .13:.0f}px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div>
</div>"""


def thread(d, t0, t1, w=4, color='#C4765A', extra=''):
    k = anim([(t0, 'stroke-dashoffset:1'), (t1, 'stroke-dashoffset:0')])
    return f'<path d="{d}" pathLength="1" style="fill: none; stroke: {color}; stroke-width: {w}; stroke-linecap: round; stroke-dasharray: 1 1; animation-name: {k}; animation-timing-function: linear{extra}"></path>'


def svg(inner, z=20):
    return f'<svg width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true" style="position: absolute; inset: 0; z-index: {z}">{inner}</svg>'


def circle_open(t, x, y, d=.55, r=2300):
    return anim([(t, f'clip-path:circle(0px at {x}px {y}px)'), (t + d, f'clip-path:circle({r}px at {x}px {y}px)')])


EPISODES = ['הצבע', 'הבחירה', 'מבפנים', 'הסיפור', 'האופי', 'הידיים']
BEAD_X = [920 - i * 152 for i in range(6)]   # RTL: episode 01 on the right


def series_thread(ep, y, t_roll, labels=True, small=False):
    """The series line: six beads, past episodes filled, the ball arrives on this episode's bead."""
    beads = ''
    for i, x in enumerate(BEAD_X):
        done = i < ep - 1
        r = 9 if small else 12
        fill = '#C4765A' if done else '#FAF8F3'
        beads += f'<div style="position: absolute; left: {x - r}px; top: {y - r}px; width: {2 * r}px; height: {2 * r}px; box-sizing: border-box; border-radius: 50%; background: {fill}; border: 3px solid #C4765A"></div>'
        if labels:
            col = '#C4765A' if i == ep - 1 else '#8B7355'
            beads += f'<div style="position: absolute; left: {x - 80}px; top: {y + 26}px; width: 160px; text-align: center; font-size: 24px; color: {col}" dir="rtl">{i + 1:02d} {EPISODES[i]}</div>'
    start_x = BEAD_X[ep - 2] if ep > 1 else 1140
    bx = BEAD_X[ep - 1]
    return (f'<div style="position: absolute; left: {BEAD_X[-1]}px; top: {y - 1}px; width: {BEAD_X[0] - BEAD_X[-1]}px; height: 3px; background: #C4765A"></div>'
            + beads + ball([(t_roll, start_x, y), (t_roll + .7, bx, y)], size=56 if small else 72))


def hook(ep, world_no, generic_html, world_img):
    """0–2s. Frame 0 = feed thumbnail: question + both screens are already on screen."""
    return f"""
<section class="stack" style="background: #EEE6D8; animation-name: {show(0, 2.05, .2)}" dir="rtl">
  <div style="position: absolute; top: 84px; right: 80px; left: 80px; display: flex; justify-content: space-between; align-items: baseline">
    <span dir="ltr" style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 40px; color: #3E2F25">Brand Worlds Studio</span>
    <span style="font-size: 26px; letter-spacing: .14em; color: #8B7B6E">ככה בוחרים · פרק {ep:02d}</span>
  </div>
  <div class="disp" style="position: absolute; top: 190px; right: 80px; left: 80px; font-size: 92px; line-height: 1.12; color: #3E2F25">למה מוצר אחד <span style="color: #C4765A">משווים,</span><br>ואת השני בוחרים?</div>
  <div style="position: absolute; top: 470px; left: 110px; width: 860px; height: 400px; box-sizing: border-box; border-radius: 18px; overflow: hidden; box-shadow: 0 24px 60px rgba(62,47,37,.16)">{generic_html}
    <span class="pill" style="background: #2E2A27; color: #F4F2EF">ככה משווים</span></div>
  <div style="position: absolute; top: 960px; left: 110px; width: 860px; box-sizing: border-box; padding: 14px 14px 26px; background: #120D0A; border-radius: 20px; box-shadow: 0 30px 70px rgba(62,47,37,.24)">
    <div style="position: relative; height: 452px; overflow: hidden; border-radius: 4px"><img class="cover" src="{world_img}" alt="">
    <span class="pill" style="background: #C4765A; color: #FAF8F3">ככה בוחרים</span></div>
  </div>
  <div style="position: absolute; top: 1470px; left: 486px; width: 108px; height: 44px; background: #4F372C; clip-path: polygon(18% 0, 82% 0, 100% 100%, 0 100%)"></div>
  {svg(thread('M1140 915 H60', .1, 1.6, 4), 25)}
  {ball([(.1, 1140, 915), (1.6, 540, 915)], 84)}
  <div style="position: absolute; top: 1600px; left: 0; right: 0; text-align: center; font-size: 30px; color: #8B7355">עולם מותג {world_no}</div>
</section>"""


def studio_window(a, b, world_no, inner, name):
    """The studio presents the world: header + crop marks + the world inside the window."""
    marks = ''
    for (x, y, bt, bl) in [(240, 412, 'top', 'left'), (796, 412, 'top', 'right'), (240, 1387, 'bottom', 'left'), (796, 1387, 'bottom', 'right')]:
        marks += f'<div style="position: absolute; left: {x}px; top: {y}px; width: 44px; height: 44px; border-{bt}: 3px solid #C4765A; border-{bl}: 3px solid #C4765A"></div>'
    return f"""
<section class="stack" style="background: #FAF8F3; animation-name: {show(a, b, .2)}" dir="rtl">
  <div style="position: absolute; top: 120px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 16px">
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; font-weight: 500; letter-spacing: .32em; color: #C4765A" dir="ltr">BRAND WORLDS STUDIO · HAGIT ANTEBI</div>
    <div style="font-size: 100px; font-weight: 500; line-height: 1.05; color: #6B563F">עולם מותג <em style="font-family: 'Cormorant Garamond', serif; font-weight: 400; color: #B8894A">{world_no}</em></div>
  </div>
  {marks}
  <div style="position: absolute; left: 270px; top: 442px; width: 540px; height: 960px; overflow: hidden; box-shadow: 0 50px 120px rgba(59,46,51,.26)">{inner}</div>
  <div style="position: absolute; top: 1500px; left: 0; right: 0; text-align: center; font-size: 40px; color: #6B563F" dir="ltr">{name}</div>
</section>"""


def close(ep, a, world_no, world_name, inner, world_line, nxt):
    return f"""
<section class="stack" style="background: #FAF8F3; animation-name: {show(a, D, .3)}" dir="rtl">
  <div style="position: absolute; left: 240px; top: 110px; width: 44px; height: 44px; border-top: 3px solid #C4765A; border-left: 3px solid #C4765A"></div>
  <div style="position: absolute; left: 796px; top: 110px; width: 44px; height: 44px; border-top: 3px solid #C4765A; border-right: 3px solid #C4765A"></div>
  <div style="position: absolute; left: 240px; top: 790px; width: 44px; height: 44px; border-bottom: 3px solid #C4765A; border-left: 3px solid #C4765A"></div>
  <div style="position: absolute; left: 796px; top: 790px; width: 44px; height: 44px; border-bottom: 3px solid #C4765A; border-right: 3px solid #C4765A"></div>
  <div style="position: absolute; left: 270px; top: 140px; width: 540px; height: 664px; overflow: hidden; box-shadow: 0 40px 100px rgba(59,46,51,.22)">{inner}</div>
  <div style="position: absolute; top: 880px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
    <div style="font-size: 30px; color: #C4765A; animation-name: {rise(a + .2)}">{world_name} · עולם מותג {world_no}</div>
    <div class="disp" style="font-size: 50px; line-height: 1.25; color: #6B563F; animation-name: {rise(a + .4)}">{world_line}</div>
    <div class="disp" style="font-size: 120px; line-height: 1.05; font-style: italic; color: #C4765A; animation-name: {rise(a + .9)}">ככה בוחרים.</div>
  </div>
  {series_thread(ep, 1360, a + 1.2)}
  <div style="position: absolute; top: 1460px; left: 80px; right: 80px; text-align: center; font-size: 30px; color: #8B7355; animation-name: {rise(a + 1.8)}">{nxt}</div>
  <div style="position: absolute; top: 1560px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 18px; animation-name: {rise(a + 1.9)}">
    <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 22px 60px; background: #6B563F; color: #FAF8F3; border-radius: 12px"><span style="font-size: 38px; font-weight: 500">אבחון פער המותג</span><span style="font-size: 24px; opacity: .85">30 דק׳ · בלי עלות</span></div>
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; letter-spacing: .3em; color: #8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</section>"""


def page(title, body):
    import importlib.util
    spec = importlib.util.spec_from_file_location('uxgen', HERE.parent.parent / 'ux-reels' / 'src' / 'gen.py')
    ux = importlib.util.module_from_spec(spec); spec.loader.exec_module(ux)
    js = ux.JS
    return f"""<!doctype html>
<html lang="he">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Heebo:wght@300;400;500;600;800&amp;family=Plus+Jakarta+Sans:wght@500;600&amp;display=swap">
<style>
html,body{{margin:0;background:#FAF8F3}}
body{{font-family:'Heebo',sans-serif}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#FAF8F3}}
.film *{{animation-duration:{D}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.disp{{font-family:'Frank Ruhl Libre',serif;font-weight:500}}
.lat{{font-family:'Cormorant Garamond',serif}}
.pill{{position:absolute;top:22px;right:22px;padding:9px 22px;border-radius:999px;font-size:26px;font-weight:500;z-index:5}}
{chr(10).join(_css)}
</style>
</head>
<body data-duration="{D}">
<div id="stage"><div class="film stack">
{body}
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 8px; background: rgba(196,118,90,.2); z-index: 50"><div style="height: 8px; background: #C4765A; transform-origin: right; animation-name: {anim([(0, 'transform:scaleX(0)'), (D, 'transform:scaleX(1)')])}; animation-timing-function: linear"></div></div>
</div></div>
<script>{js}</script>
</body>
</html>"""


def stacks(n=1, scale=1.0):
    """A generic no-name pancake stack, drawn (no photo of any world)."""
    w = [70, 78, 86]
    return ''.join(f'<div style="width: {x * scale:.0f}px; height: {16 * scale:.0f}px; margin-top: {-6 * scale if i else 0:.0f}px; border-radius: 50%; background: #E9D6B4; border: 2px solid #C9B48F"></div>' for i, x in enumerate(w))


# ─────────────────────────── EPISODE 01 · PANCAKERIE · הצבע ───────────────────────────
# music ep01-15s.mp3: quiet to 3.3 · chorus hits 3.3 · beats 4.48 / 5.50 / 6.48 / 7.48 · music drops at 15.
def ep01():
    _css.clear()
    rows = [('פנקייק פיסטוק', '₪42'), ('פנקייק תות', '₪39'), ('פנקייק נוטלה', '₪44'), ('פנקייק לימון', '₪39')]
    small = ''.join(f'<div style="display: flex; align-items: center; gap: 22px; padding: 14px 0; border-bottom: 1px solid #EEEEEE"><div style="width: 90px; display: flex; flex-direction: column; align-items: center">{stacks(scale=.9)}</div><span style="flex-grow: 1; font-size: 32px; color: #444444">{n}</span><b style="font-size: 34px; color: #222222">{p}</b></div>' for n, p in rows[:3])
    generic_small = f'<div class="stack" style="background: #FFFFFF; padding: 70px 40px 0; box-sizing: border-box">{small}</div>'

    # full-screen app 2.0–3.4: rows at fixed y so the ball can ring each price
    ys = [700, 900, 1100, 1300]
    big = ''
    for i, ((n, p), y) in enumerate(zip(rows, ys)):
        ring = anim([(2.35 + i * .25, 'opacity:0;transform:scale(1.5)'), (2.55 + i * .25, 'opacity:1;transform:scale(1)')])
        big += f"""<div style="position: absolute; top: {y - 80}px; left: 90px; right: 90px; height: 160px; display: flex; align-items: center; gap: 34px; border-bottom: 2px solid #EEEEEE" dir="rtl">
      <div style="width: 130px; display: flex; flex-direction: column; align-items: center">{stacks(scale=1.4)}</div>
      <span style="flex-grow: 1; font-size: 46px; color: #444444">{n}</span>
      <b style="position: relative; font-size: 54px; color: #222222">{p}<span style="position: absolute; inset: -14px -24px; border: 4px solid #C4765A; border-radius: 999px; animation-name: {ring}"></span></b></div>"""
    compare = f"""
<section class="stack" style="background: #FFFFFF; animation-name: {show(2.0, 3.45, .15)}" dir="rtl">
  <div style="position: absolute; top: 150px; right: 90px; left: 90px; display: flex; justify-content: space-between; align-items: center; font-size: 30px; color: #777777"><span style="padding: 10px 26px; border-radius: 999px; background: #2E2A27; color: #F4F2EF">ככה משווים</span><span>משלוחים · קינוחים</span></div>
  <div class="disp" style="position: absolute; top: 300px; right: 90px; left: 90px; font-size: 64px; line-height: 1.2; color: #2E2A27; animation-name: {rise(2.15, .35)}">ארבע שורות. ההבדל היחיד הוא המחיר.</div>
  {big}
  {ball([(2.0, 1140, 1500), (2.35, 220, ys[0]), (2.6, 220, ys[1]), (2.85, 220, ys[2]), (3.1, 220, ys[3])], 84)}
</section>"""

    colors = [('#A5A57F', '#402613', 'PISTACHE', 'פיסטוק', 'dish-pistache'), ('#D39483', '#402613', 'FRAISE', 'תות', 'dish-fraise'),
              ('#523726', '#EEE6DA', 'NOISETTE', 'אגוזי לוז', 'dish-noisette'), ('#EEC376', '#402613', 'CITRON', 'לימון', 'dish-citron')]
    swaps = [4.0, 5.5, 6.48, 7.48]
    arc_y = 1420
    beads_x = [880, 653, 427, 200]  # RTL: first bead on the right
    arc = 'M960 1330 Q540 1560 120 1330'

    def arc_point(x):
        # quadratic through (960,1330) (540,1560 ctrl) (120,1330): y as function of x
        u = (960 - x) / 840
        return round((1 - u) ** 2 * 1330 + 2 * (1 - u) * u * 1560 + u ** 2 * 1330)

    layers = ''
    for i, ((bg, ink, fr, he, img), t) in enumerate(zip(colors, swaps)):
        bx = beads_x[i]
        by = arc_point(bx)
        end = swaps[i + 1] + .5 if i < 3 else 9.0
        layers += f"""
  <div class="stack" style="background: {bg}; animation-name: {circle_open(t, bx, by, .5)}; z-index: {i + 1}">
    <div class="stack" style="animation-name: {show(t + .05, end, .12)}">
      <div style="position: absolute; top: 250px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 150px; letter-spacing: .08em; line-height: 1; color: {ink}" dir="ltr">{fr}</div>
      <div class="disp" style="position: absolute; top: 420px; left: 0; right: 0; text-align: center; font-size: 60px; color: {ink}">{he}</div>
      <img src="assets/{img}.webp" alt="" style="position: absolute; top: 560px; left: 60px; width: 960px; height: 720px; object-fit: contain; animation-name: {anim([(t, 'transform:scale(.86) translateY(30px)'), (t + .45, 'transform:none')])}">
    </div>
  </div>"""
    bstops = [(3.75, 540, 920), (4.25, beads_x[0], arc_point(beads_x[0]))]
    for i in range(1, 4):
        bstops += [(swaps[i] - .25, beads_x[i - 1], arc_point(beads_x[i - 1])), (swaps[i], beads_x[i], arc_point(beads_x[i]))]
    bead_html = ''.join(f'<div style="position: absolute; left: {x - 16}px; top: {arc_point(x) - 16}px; width: 32px; height: 32px; box-sizing: border-box; border-radius: 50%; background: {c[0]}; border: 4px solid #FAF8F3; z-index: 21"></div>' for x, c in zip(beads_x, colors))
    swap = f"""
<section class="stack" style="animation-name: {show(4.0, 9.1, .2)}; clip-path: none" dir="rtl">
  <div class="stack" style="background: #A5A57F; animation-name: {circle_open(3.75, 540, 920, .55)}">
    {layers}
    {svg(thread(arc, 4.2, 4.7, 5, '#FAF8F3'), 20)}
    <div class="stack" style="z-index: 21; animation-name: {show(4.6, 9.1, .2)}">{bead_html}</div>
    <div class="disp" style="position: absolute; bottom: 150px; left: 0; right: 0; text-align: center; z-index: 22">
      <span style="display: inline-block; padding: 16px 40px; background: rgba(250,248,243,.92); border-radius: 999px; font-size: 52px; color: #402613; animation-name: {rise(5.0)}">ארבע מנות. כל אחת בצבע שלה.</span></div>
    {ball(bstops, 80)}
  </div>
</section>"""

    # colour travels down the thread to the box (8.9–11.6)
    chips = [('רקע', '#A5A57F', '#402613', 10.2), ('כפתור', '#402613', '#EEE6DA', 10.45), ('מארז', '#D39483', '#402613', 10.7)]
    chip_html = ''.join(f'<span style="flex: 1; padding: 22px 0; border-radius: 10px; text-align: center; font-size: 40px; color: {fg}; background: {bg}; animation-name: {anim([(t, "opacity:0;transform:scale(.8)"), (t + .3, "opacity:1;transform:none")])}">{n}</span>' for n, bg, fg, t in chips)
    travel = f"""
<section class="stack" style="background: #EEC376; animation-name: {show(8.9, 11.75, .2)}" dir="rtl">
  <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 76px; line-height: 1.15; color: #402613; animation-name: {rise(9.0)}">הצבע לא נשאר<br>על הצלחת.</div>
  <img src="assets/dish-citron.webp" alt="" style="position: absolute; top: 380px; left: 300px; width: 480px; height: 360px; object-fit: contain">
  {svg(thread('M540 700 C 540 840, 300 820, 330 980', 9.2, 9.9, 5), 20)}
  {ball([(9.2, 540, 700), (9.55, 470, 830), (9.9, 330, 980)], 72)}
  <div style="position: absolute; top: 980px; left: 80px; width: 920px; height: 520px; border-radius: 24px; overflow: hidden; border: 3px solid #C4765A; animation-name: {anim([(9.85, 'clip-path:circle(0px at 250px 0px)'), (10.4, 'clip-path:circle(1200px at 250px 0px)')])}"><img class="cover" src="assets/brand-takeaway-m.webp" alt=""></div>
  <div style="position: absolute; top: 1540px; left: 80px; right: 80px; display: flex; gap: 20px">{chip_html}</div>
  <div class="disp" style="position: absolute; top: 1680px; right: 80px; left: 80px; font-size: 50px; line-height: 1.2; color: #402613; animation-name: {rise(10.4)}">הוא עובר לרקע, לכפתור, <em>ולמארז שלך.</em></div>
</section>"""

    window_inner = '<div class="stack" style="background: #A5A57F"><img src="assets/dish-pistache.webp" alt="" style="position: absolute; top: 300px; left: -60px; width: 660px; height: 495px; object-fit: contain"></div>'
    window = studio_window(3.3, 4.4, 26, window_inner, 'Pancakerie° · Morning Patisserie') + f'<div class="stack" style="z-index: 9; animation-name: {show(3.3, 4.1, .1)}">{svg(thread("M1140 1700 H780 C 620 1700, 560 1300, 540 920", 3.3, 3.75, 5), 1)}{ball([(3.3, 1140, 1700), (3.5, 780, 1700), (3.75, 540, 920)], 84)}</div>'

    close_inner = '<div class="stack" style="background: #EEC376"><img class="cover" src="assets/brand-takeaway-m.webp" alt="" style="object-position: 40% 50%"></div>'
    body = (hook(1, 26, generic_small, 'assets/pancakerie.webp') + compare + window + swap + travel
            + close(1, 11.6, 26, 'Pancakerie°', close_inner, 'טעם שרואים לפני שטועמים.', 'בפרק הבא: הבחירה · CHASEN°'))
    return page('ככה בוחרים · פרק 01 · הצבע', body)


# ─────────────────────────── EPISODE 02 · CHASEN · הבחירה ───────────────────────────
# music ep02-15s.mp3: quiet to 3.8 · chorus 3.84 · beats 4.53 / 5.53 / 6.53 / 7.55 / 8.55 · winds down from 10.6.
def ep02():
    _css.clear()
    rows = [('מאצ\'ה לאטה', '₪22'), ('מאצ\'ה תות', '₪24'), ('הוג\'יצ\'ה', '₪24'), ('מאצ\'ה יוזו', '₪26'), ('מאצ\'ה כחולה', '₪26')]
    small = ''.join(f'<div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 2px dashed #555555; font-size: 34px; color: #DDDDDD"><span>{n}</span><b>{p}</b></div>' for n, p in rows[:4])
    generic_small = f'<div class="stack" style="background: #222222; padding: 80px 50px 0; box-sizing: border-box">{small}</div>'

    ys = [640, 810, 980, 1150, 1320]
    big = ''
    for i, ((n, p), y) in enumerate(zip(rows, ys)):
        ring = anim([(2.25 + i * .22, 'opacity:0;transform:scale(1.5)'), (2.45 + i * .22, 'opacity:1;transform:scale(1)')])
        big += f"""<div style="position: absolute; top: {y - 70}px; left: 90px; right: 90px; height: 140px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px dashed #555555" dir="rtl">
      <span style="font-size: 56px; color: #E8E8E8">{n}</span>
      <b style="position: relative; font-size: 58px; color: #FFFFFF">{p}<span style="position: absolute; inset: -14px -24px; border: 4px solid #C4765A; border-radius: 999px; animation-name: {ring}"></span></b></div>"""
    compare = f"""
<section class="stack" style="background: #222222; animation-name: {show(2.0, 3.35, .15)}" dir="rtl">
  <div style="position: absolute; top: 150px; right: 90px; left: 90px; display: flex; justify-content: space-between; align-items: center; font-size: 30px; color: #999999"><span style="padding: 10px 26px; border-radius: 999px; background: #F4F2EF; color: #2E2A27">ככה משווים</span><span>תפריט · משקאות קרים</span></div>
  <div class="disp" style="position: absolute; top: 290px; right: 90px; left: 90px; font-size: 64px; line-height: 1.2; color: #F4F2EF; animation-name: {rise(2.1, .35)}">חמישה טעמים. חמש שורות, ומחיר.</div>
  {big}
  <div style="position: absolute; top: 1450px; right: 90px; left: 90px; display: flex; justify-content: space-between; font-size: 40px; color: #999999"><span>תוספת קצפת / שוקולד</span><b>₪4</b></div>
  {ball([(2.0, 1140, 1600), (2.25, 220, ys[0]), (2.47, 220, ys[1]), (2.69, 220, ys[2]), (2.91, 220, ys[3]), (3.13, 220, ys[4])], 84)}
</section>"""

    flavours = [('Matcha Classique', 'glass_classic', '#C9D1A8'), ('Matcha Fraise', 'glass_fraise', '#E6BFB4'),
                ('Hōjicha', 'glass_hojicha', '#D8BC98'), ('Matcha Yuzu', 'glass_yuzu', '#EDD68E'), ('Matcha Bleu', 'glass_bleu', '#B4C4E2')]
    stops = [4.53, 5.53, 6.53, 7.55, 8.55]
    cx, cy, R = 540, 960, 440
    niche_l, niche_t, niche_w, niche_h = 335, 560, 410, 800
    gw, gh = 372, 795        # glass image displayed size (852×1820 · 0.4366)
    gx, gy = 19, 6           # glass inside the niche
    s = gw / 852

    def on_ring(k):          # bead k clockwise from the top
        a = math.radians(k * 72)
        return round(cx + R * math.sin(a)), round(cy - R * math.cos(a))

    tints = ''.join(f'<div class="stack" style="background: {c}; animation-name: {show(t - .1 if i else 3.8, (stops[i + 1] + .1) if i < 4 else 12.5, .3)}"></div>' for i, ((_, _, c), t) in enumerate(zip(flavours, stops)))
    pours = ''
    for i, ((name, img, _), t) in enumerate(zip(flavours, stops)):
        clip = anim([(t, 'clip-path:inset(100% 0 0 0)'), (t + .55, 'clip-path:inset(0 0 0 0)')]) if i else None
        pours += f'<img src="assets/{img}.webp" alt="" style="position: absolute; left: {gx}px; top: {gy}px; width: {gw}px; height: {gh}px{"; animation-name: " + clip if clip else ""}">'
    names = ''.join(f'<div class="stack" style="animation-name: {show(t + .05 if i else 4.3, (stops[i + 1]) if i < 4 else 12.5, .15)}"><div style="position: absolute; top: 1500px; left: 0; right: 0; text-align: center; font-family: \'Cormorant Garamond\', serif; font-size: 84px; color: #22301f" dir="ltr">{n}</div></div>' for i, ((n, _, _), t) in enumerate(zip(flavours, stops)))
    ring_d = f'M{cx} {cy - R} A{R} {R} 0 0 1 {cx} {cy + R} A{R} {R} 0 0 1 {cx} {cy - R}'
    beads = ''.join(f'<div style="position: absolute; left: {on_ring(k)[0] - 20}px; top: {on_ring(k)[1] - 20}px; width: 40px; height: 40px; box-sizing: border-box; border-radius: 50%; background: {c}; border: 5px solid #FAF8F3; z-index: 21"></div>'
                    for k, c in enumerate(['#4c6b33', '#C77B6E', '#8A5A2B', '#D9B23A', '#4A6BC4']))
    # ball walks clockwise bead to bead along the ring (sub-steps so it follows the circle)
    bstops = [(3.84, cx, 1700), (4.3, *on_ring(0))]
    for k in range(1, 5):
        t0, t1 = stops[k] - .32, stops[k]
        bstops.append((t0, *on_ring(k - 1)))
        for j in range(1, 6):
            a = math.radians((k - 1 + j / 6) * 72)
            bstops.append((t0 + (t1 - t0) * j / 6, round(cx + R * math.sin(a)), round(cy - R * math.cos(a))))
        bstops.append((t1, *on_ring(k)))
    cream_clip = anim([(9.35, 'clip-path:inset(100% 0 0 0)'), (9.9, 'clip-path:inset(0 0 0 0)')])
    choco_clip = anim([(9.85, 'clip-path:inset(0 0 100% 0)'), (10.45, 'clip-path:inset(0 0 0 0)')])
    dial = f"""
<section class="stack" style="animation-name: {show(3.84, 12.2, .2)}" dir="rtl">
  <div class="stack" style="animation-name: {circle_open(3.84, 540, 960, .55)}">
    {tints}
    <div class="disp" style="position: absolute; top: 210px; left: 0; right: 0; text-align: center; font-size: 62px; color: #22301f; animation-name: {rise(4.3)}">הכוס הזאת עוד לא קיימת.</div>
    {svg(f'<circle cx="{cx}" cy="{cy}" r="{R}" style="fill: none; stroke: rgba(250,248,243,.0)"></circle>' + thread(ring_d, 4.0, 4.5, 5, '#C4765A'), 6)}
    <div class="stack" style="z-index: 21; animation-name: {show(4.4, 12.2, .2)}">{beads}</div>
    <div style="position: absolute; left: {niche_l}px; top: {niche_t}px; width: {niche_w}px; height: {niche_h}px; border-radius: {niche_w // 2}px {niche_w // 2}px 34px 34px; overflow: hidden; background: #F2E8D5; z-index: 10; box-shadow: 0 30px 70px rgba(34,48,31,.18)">
      {pours}
      <img src="assets/layer_cream.webp" alt="" style="position: absolute; left: {gx + 149 * s:.0f}px; top: {gy + 159 * s:.0f}px; width: {552 * s:.0f}px; height: {719 * s:.0f}px; animation-name: {cream_clip}">
      <img src="assets/layer_choco.webp" alt="" style="position: absolute; left: {gx + 178 * s:.0f}px; top: {gy + 532 * s:.0f}px; width: {512 * s:.0f}px; height: {1169 * s:.0f}px; animation-name: {choco_clip}">
    </div>
    <div class="stack" style="z-index: 22; animation-name: {show(4.3, 9.3, .2)}">{names}</div>
    <div class="disp" style="position: absolute; top: 1640px; left: 0; right: 0; text-align: center; font-size: 56px; color: #22301f; z-index: 22; animation-name: {anim([(5.0, 'opacity:0;transform:translateY(34px)'), (5.5, 'opacity:1;transform:none'), (9.1, 'opacity:1;transform:none'), (9.3, 'opacity:0;transform:none')])}">עד שאת מכינה אותה.</div>
    <div style="position: absolute; top: 1640px; left: 0; right: 0; text-align: center; z-index: 22; animation-name: {anim([(9.35, 'opacity:0'), (9.55, 'opacity:1'), (10.6, 'opacity:1'), (10.8, 'opacity:0')])}"><span style="font-size: 50px; color: #15202E">+ קצפת · + שוקולד על הדפנות</span></div>
    {ball(bstops + [(9.0, *on_ring(4)), (9.35, 540, 1405)], 80)}
  </div>
</section>"""

    card = f"""
<section class="stack" style="background: #B4C4E2; animation-name: {show(10.6, 12.6, .2)}; z-index: 1" dir="rtl">
  <div style="position: absolute; left: 370px; top: 150px; width: 340px; height: 663px; border-radius: 170px 170px 30px 30px; overflow: hidden; background: #F2E8D5">
    <img src="assets/glass_bleu.webp" alt="" style="position: absolute; left: 16px; top: 5px; width: 310px; height: 662px">
    <img src="assets/layer_cream.webp" alt="" style="position: absolute; left: {16 + 149 * 310 / 852:.0f}px; top: {5 + 159 * 310 / 852:.0f}px; width: {552 * 310 / 852:.0f}px; height: {719 * 310 / 852:.0f}px">
    <img src="assets/layer_choco.webp" alt="" style="position: absolute; left: {16 + 178 * 310 / 852:.0f}px; top: {5 + 532 * 310 / 852:.0f}px; width: {512 * 310 / 852:.0f}px; height: {1169 * 310 / 852:.0f}px">
  </div>
  {svg(thread('M540 813 C 540 900, 700 900, 640 1010', 10.65, 10.95, 5), 6)}
  {ball([(10.65, 540, 813), (10.95, 640, 1010)], 64)}
  <div style="position: absolute; top: 1010px; left: 150px; right: 150px; padding: 46px 30px; box-sizing: border-box; background: #FAF8F3; border: 3px solid #C4765A; border-radius: 22px; text-align: center; box-shadow: 0 30px 70px rgba(21,32,46,.25); animation-name: {anim([(10.8, 'opacity:0;transform:translateY(80px) rotate(-3deg)'), (11.2, 'opacity:1;transform:none')])}">
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 22px; letter-spacing: .3em; color: #C4765A" dir="ltr">CHASEN° · LA CARTE</div>
    <div style="font-family: 'Cormorant Garamond', serif; font-size: 84px; line-height: 1.1; color: #15202E" dir="ltr">Matcha Bleu</div>
    <div style="font-size: 34px; color: #4F372C">קצפת · שוקולד על הדפנות</div>
    <div style="font-size: 32px; color: #7A6349; margin-top: 10px">המשקה שלך.</div>
  </div>
  <div class="disp" style="position: absolute; top: 1560px; left: 0; right: 0; text-align: center; font-size: 66px; line-height: 1.2; color: #15202E; animation-name: {rise(11.1)}">אותה כוס. <em>שם משלה.</em></div>
</section>"""

    window_inner = '<div class="stack" style="background: #C9D1A8"><div style="position: absolute; left: 95px; top: 120px; width: 350px; height: 690px; border-radius: 175px 175px 30px 30px; overflow: hidden; background: #F2E8D5"><img src="assets/glass_classic.webp" alt="" style="position: absolute; left: 16px; top: 4px; width: 318px; height: 680px"></div></div>'
    window = studio_window(3.25, 4.2, 22, window_inner, 'CHASEN° · Bar à Matcha') + f'<div class="stack" style="z-index: 9; animation-name: {show(3.25, 4.05, .1)}">{svg(thread("M1140 1700 H780 C 620 1700, 560 1300, 540 960", 3.3, 3.84, 5), 1)}{ball([(3.3, 1140, 1700), (3.5, 780, 1700), (3.84, 540, 960)], 84)}</div>'

    close_inner = '<div class="stack" style="background: #B4C4E2"><div style="position: absolute; left: 115px; top: 40px; width: 310px; height: 600px; border-radius: 155px 155px 26px 26px; overflow: hidden; background: #F2E8D5"><img src="assets/glass_bleu.webp" alt="" style="position: absolute; left: 14px; top: -20px; width: 282px; height: 602px"></div></div>'
    body = (hook(2, 22, generic_small, 'assets/chasen.webp') + compare + window + dial + card
            + close(2, 12.45, 22, 'CHASEN°', close_inner, 'מאצ\'ה לא מזמינים. מרכיבים.', 'בפרק הבא: מבפנים · MIEL°'))
    return page('ככה בוחרים · פרק 02 · הבחירה', body)


# ─────────────────────────── EPISODE 03 · MIEL · מבפנים ───────────────────────────
# music ep03-15s.mp3 (0:04.95–0:19.95): quiet to 3.25 · chorus hits 3.25 · beats every 0.51s (6.47, 8.49, 9.0, 9.49, 10.0, 10.49, 11.49).
# The thread is a straight line this time: the ball goes down through the cake and the line it leaves is the cut.
def ep03():
    _css.clear()
    cakes = [('עוגת קרם וניל', '₪159'), ('עוגת פירות יער', '₪169'), ('עוגת שוקולד', '₪179'), ('עוגת יום הולדת', '₪189')]
    cards = ''.join(f'<div style="flex: 1; display: flex; flex-direction: column; gap: 8px"><img src="assets/generic-cake.jpg" alt="" style="width: 100%; height: 230px; object-fit: cover; border-radius: 8px"><span style="font-size: 24px; color: #444444">{n}</span><b style="font-size: 30px; color: #222222">{p}</b></div>' for n, p in cakes[:3])
    generic_small = f'<div class="stack" style="background: #FFFFFF; padding: 76px 30px 0; box-sizing: border-box; display: flex; gap: 22px">{cards}</div>'

    ys = [640, 880, 1120, 1360]
    rows = ''
    for i, ((n, p), y) in enumerate(zip(cakes, ys)):
        ring = anim([(2.25 + i * .25, 'opacity:0;transform:scale(1.5)'), (2.45 + i * .25, 'opacity:1;transform:scale(1)')])
        rows += f"""<div style="position: absolute; top: {y - 100}px; left: 90px; right: 90px; height: 200px; display: flex; align-items: center; gap: 34px; border-bottom: 2px solid #EEEEEE" dir="rtl">
      <img src="assets/generic-cake.jpg" alt="" style="width: 200px; height: 160px; object-fit: cover; border-radius: 10px">
      <span style="flex-grow: 1; font-size: 44px; color: #444444">{n}</span>
      <b style="position: relative; font-size: 54px; color: #222222">{p}<span style="position: absolute; inset: -14px -24px; border: 4px solid #C4765A; border-radius: 999px; animation-name: {ring}"></span></b></div>"""
    compare = f"""
<section class="stack" style="background: #FFFFFF; animation-name: {show(2.0, 3.4, .15)}" dir="rtl">
  <div style="position: absolute; top: 150px; right: 90px; left: 90px; display: flex; justify-content: space-between; align-items: center; font-size: 30px; color: #777777"><span style="padding: 10px 26px; border-radius: 999px; background: #2E2A27; color: #F4F2EF">ככה משווים</span><span>עוגות · משלוח עד הבית</span></div>
  <div class="disp" style="position: absolute; top: 290px; right: 90px; left: 90px; font-size: 64px; line-height: 1.2; color: #2E2A27; animation-name: {rise(2.1, .35)}">מבחוץ, כל העוגות נראות אותו דבר.</div>
  {rows}
  {ball([(2.0, 1140, 1600), (2.25, 220, ys[0]), (2.5, 220, ys[1]), (2.75, 220, ys[2]), (3.0, 220, ys[3])], 84)}
</section>"""

    # studio window: the site's hero plays inside it, the empty table fills with five slices
    window_inner = ('<div class="stack" data-seq="assets/hero/f%03d.webp" data-from="1" data-to="41" data-start="3.3" data-step="0.028"></div>')
    window = studio_window(3.2, 4.65, 27, window_inner, 'MIEL° · Maison Miel Pâtisserie') + \
        f'<div class="stack" style="z-index: 9; animation-name: {show(3.2, 4.5, .1)}">{svg(thread("M1140 1700 H780 C 620 1700, 560 1200, 540 880", 3.25, 4.25, 5), 1)}{ball([(3.25, 1140, 1700), (3.55, 780, 1700), (4.25, 540, 880)], 84)}</div>'

    # the cut: the ball goes down where the knife enters, the film follows its line
    kx = 695
    cut = f"""
<section class="stack" style="background: #F3E3DE; animation-name: {show(4.45, 8.55, .2)}" dir="rtl">
  <div class="stack" style="animation-name: {show(4.45, 6.5, .06)}"><div class="stack" data-seq="assets/coupe/c_%03d.jpg" data-from="1" data-to="14" data-start="4.5" data-step="0.14" data-pos="62% 40%"></div></div>
  <div class="stack" style="animation-name: {show(6.45, 8.6, .05)}"><div class="stack" data-seq="assets/coupe/c_%03d.jpg" data-from="18" data-to="41" data-start="6.47" data-step="0.07" data-pos="62% 40%"></div></div>
  <div class="stack" style="background: linear-gradient(180deg, rgba(250,248,243,.92) 0%, rgba(250,248,243,0) 26%, rgba(250,248,243,0) 64%, rgba(250,248,243,.94) 86%)"></div>
  <div class="stack" style="animation-name: {show(4.45, 6.55, .15)}">{svg(thread(f'M{kx} 470 V1310', 4.55, 6.4, 6), 20)}{ball([(4.5, kx, 470), (6.4, kx, 1310)], 80)}</div>
  <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 68px; line-height: 1.15; color: #4F372C; animation-name: {rise(4.7)}">כל בייקרי מראה<br>עוגה מבחוץ.</div>
  <div class="disp" style="position: absolute; top: 1590px; right: 80px; left: 80px; font-size: 120px; line-height: 1; font-style: italic; color: #A45839; animation-name: {rise(6.5, .4)}">כאן חותכים.</div>
</section>"""

    # what's inside: the thread runs down the slice's face, the ball counts the layers, then the slice swaps on the beat
    top = 420
    lay = [('ביסקוויט', .40, False, 8.49), ('לב', .485, True, 9.0), ('ביסקוויט', .57, False, 9.49), ('לב', .65, True, 10.0)]
    lx = 432
    labels = ''
    for n, fy, heart, t in lay:
        y = round(top + fy * 810)
        bg = '#A45839;color:#FAF8F3' if heart else 'rgba(250,248,243,.94);color:#4F372C'
        labels += f'<div style="position: absolute; top: {y - 30}px; right: {1080 - lx + 70}px; padding: 8px 22px; border-radius: 8px; font-size: 36px; font-weight: 500; background: {bg}; animation-name: {anim([(t - .05, "opacity:0;transform:translateX(30px)"), (t + .2, "opacity:1;transform:none"), (10.4, "opacity:1;transform:none"), (10.55, "opacity:0;transform:none")])}">{n}</div>'
    bst = [(8.4, lx, top + 230)]
    for n, fy, heart, t in lay:
        bst += [(t - .12, *bst[-1][1:]), (t, lx, round(top + fy * 810))]
    swaps = [('41-slice-vanille-framboise-m', 8.4, 10.5), ('39-slice-chocolat-caramel-m', 10.49, 11.5), ('36-slice-vanille-caramel-m', 11.49, 11.8)]
    slices = ''.join(f'<div class="stack" style="animation-name: {show(a, b, .1)}"><img src="assets/{img}.webp" alt="" style="position: absolute; top: {top}px; left: 0; width: 1080px; height: 810px; object-fit: cover"></div>' for img, a, b in swaps)
    inside = f"""
<section class="stack" style="background: #F3E3DE; animation-name: {show(8.4, 11.8, .2)}" dir="rtl">
  {slices}
  <div class="stack" style="background: linear-gradient(180deg, #F3E3DE 0%, #F3E3DE 21%, rgba(243,227,222,0) 24%, rgba(243,227,222,0) 60%, #F3E3DE 64%)"></div>
  <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 72px; line-height: 1.15; color: #4F372C; animation-name: {anim([(8.5, 'opacity:0;transform:translateY(30px)'), (8.9, 'opacity:1;transform:none'), (10.3, 'opacity:1;transform:none'), (10.5, 'opacity:0;transform:none')])}">שכבה. לב. שכבה. לב.</div>
  <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 72px; line-height: 1.15; color: #4F372C; animation-name: {rise(10.5, .35)}">72 עוגות. טאפ אחד חותך.</div>
  <div class="stack" style="animation-name: {show(8.4, 10.55, .15)}">{svg(thread(f'M{lx} {top + 200} V{top + 600}', 8.4, 8.6, 5), 20)}{labels}{ball(bst, 64)}</div>
  <div class="disp" style="position: absolute; top: 1330px; right: 80px; left: 80px; font-size: 64px; line-height: 1.2; color: #4F372C; animation-name: {rise(9.3)}">לא בוחרים גודל.</div>
  <div class="disp" style="position: absolute; top: 1420px; right: 80px; left: 80px; font-size: 84px; line-height: 1.15; font-style: italic; color: #A45839; animation-name: {rise(10.0)}">בוחרים מה יהיה בפנים.</div>
</section>"""

    close_inner = '<img class="cover" src="assets/miel-box.webp" alt="" style="object-position: 50% 40%">'
    body = (hook(3, 27, generic_small, 'assets/hero/f041.webp') + compare + window + cut + inside
            + close(3, 11.6, 27, 'MIEL°', close_inner, 'רומנטיקה מתחילה מבפנים.', 'בפרק הבא: הסיפור · VELUNE°'))
    return page('ככה בוחרים · פרק 03 · מבפנים', body)


# ─────────────────────────── shared for 04–06 ───────────────────────────
def compare_rows(rows, ys, icon, t0, title, tag, theme='light', a=2.0, b=3.4):
    """Generic no-name list: name · sub · price, the ball rings each price. rows: [(name, sub, price)]."""
    dark = theme == 'dark'
    bg, line, name_c, sub_c, price_c = ('#222222', '#555555', '#E8E8E8', '#999999', '#FFFFFF') if dark else ('#FFFFFF', '#EEEEEE', '#444444', '#999999', '#222222')
    pill = 'background: #F4F2EF; color: #2E2A27' if dark else 'background: #2E2A27; color: #F4F2EF'
    big = ''
    for i, ((n, sub, p), y) in enumerate(zip(rows, ys)):
        ring = anim([(t0 + i * .25, 'opacity:0;transform:scale(1.5)'), (t0 + .2 + i * .25, 'opacity:1;transform:scale(1)')])
        big += f"""<div style="position: absolute; top: {y - 90}px; left: 90px; right: 90px; height: 180px; display: flex; align-items: center; gap: 34px; border-bottom: 2px solid {line}" dir="rtl">
      <div style="width: 120px; display: flex; justify-content: center">{icon(1.3)}</div>
      <div style="flex-grow: 1; display: flex; flex-direction: column; gap: 4px"><span style="font-size: 44px; color: {name_c}">{n}</span><span style="font-size: 30px; color: {sub_c}">{sub}</span></div>
      <b style="position: relative; font-size: 54px; color: {price_c}">{p}<span style="position: absolute; inset: -14px -24px; border: 4px solid #C4765A; border-radius: 999px; animation-name: {ring}"></span></b></div>"""
    return f"""
<section class="stack" style="background: {bg}; animation-name: {show(a, b, .15)}" dir="rtl">
  <div style="position: absolute; top: 150px; right: 90px; left: 90px; display: flex; justify-content: space-between; align-items: center; font-size: 30px; color: {sub_c}"><span style="padding: 10px 26px; border-radius: 999px; {pill}">ככה משווים</span><span>{tag}</span></div>
  <div class="disp" style="position: absolute; top: 290px; right: 90px; left: 90px; font-size: 64px; line-height: 1.2; color: {'#F4F2EF' if dark else '#2E2A27'}; animation-name: {rise(a + .1, .35)}">{title}</div>
  {big}
  {ball([(a, 1140, 1600)] + [(t0 + i * .25, 220, y) for i, y in enumerate(ys)], 84)}
</section>"""


def small_rows(rows, icon, theme='light'):
    dark = theme == 'dark'
    bg, line, c1, c2 = ('#222222', '#555555', '#DDDDDD', '#FFFFFF') if dark else ('#FFFFFF', '#EEEEEE', '#444444', '#222222')
    inner = ''.join(f'<div style="display: flex; align-items: center; gap: 22px; padding: 12px 0; border-bottom: 1px solid {line}"><div style="width: 80px; display: flex; justify-content: center">{icon(.8)}</div><span style="flex-grow: 1; font-size: 30px; color: {c1}">{n} · {sub}</span><b style="font-size: 34px; color: {c2}">{p}</b></div>' for n, sub, p in rows[:3])
    return f'<div class="stack" style="background: {bg}; padding: 70px 40px 0; box-sizing: border-box">{inner}</div>'


def seq(path, a, b, start, step, frm, to, pos='50% 50%'):
    """A frame sequence that is only on screen between a and b (so its held first/last frame never leaks)."""
    return f'<div class="stack" style="animation-name: {show(a, b, .05)}"><div class="stack" data-seq="{path}" data-from="{frm}" data-to="{to}" data-start="{start}" data-step="{step}" data-pos="{pos}"></div></div>'


def into_window(a, b, t_in, t_land, x=540, y=960):
    """The ball and the thread that carry the viewer from the studio window into the world."""
    return f'<div class="stack" style="z-index: 9; animation-name: {show(a, b, .1)}">{svg(thread(f"M1140 1700 H780 C 620 1700, 560 1300, {x} {y}", t_in, t_land, 5), 1)}{ball([(t_in, 1140, 1700), (t_in + .2, 780, 1700), (t_land, x, y)], 84)}</div>'


def fade_band(color, top=True, h=30):
    rgba = color
    if top:
        return f'<div class="stack" style="background: linear-gradient(180deg, {rgba} 0%, transparent {h}%)"></div>'
    return f'<div class="stack" style="background: linear-gradient(0deg, {rgba} 0%, transparent {h}%)"></div>'


def icon_perfume(k=1.0):
    return f'<div style="position: relative; width: {52 * k:.0f}px; height: {70 * k:.0f}px; margin-top: {16 * k:.0f}px; border-radius: {10 * k:.0f}px; background: #ECE8E2; border: 2px solid #C9C2B8"><div style="position: absolute; top: {-16 * k:.0f}px; left: {16 * k:.0f}px; width: {20 * k:.0f}px; height: {14 * k:.0f}px; border-radius: 3px; background: #BDB5AA"></div></div>'


def icon_chain(k=1.0):
    return f'<div style="width: {64 * k:.0f}px; height: {64 * k:.0f}px; box-sizing: border-box; border-radius: 50%; border: {5 * k:.0f}px dotted #BCA878"></div>'


def icon_serum(k=1.0):
    return f'<div style="position: relative; width: {40 * k:.0f}px; height: {64 * k:.0f}px; margin-top: {22 * k:.0f}px; border-radius: {6 * k:.0f}px; background: #EFE9E1; border: 2px solid #C9C2B8"><div style="position: absolute; top: {-24 * k:.0f}px; left: {9 * k:.0f}px; width: {18 * k:.0f}px; height: {22 * k:.0f}px; border-radius: {9 * k:.0f}px {9 * k:.0f}px 2px 2px; background: #B7AEA3"></div></div>'


# ─────────────────────────── EPISODE 04 · VELUNE · הסיפור ───────────────────────────
# music ep04-15s.mp3 (0:32.94–0:47.94): quiet to 3.3 · chorus hits 3.3 · beats every 0.511s (6.37, 9.95, 10.46, 10.97).
# The thread is the path: it waits on the closed door, walks down the garden alley, runs beside the drop, then turns into the sun arc.
def ep04():
    _css.clear()
    rows = [('בושם פרחוני', 'ורד, יסמין · 50 מ״ל', '₪480'), ('בושם עצי', 'ארז, וטיבר · 50 מ״ל', '₪520'),
            ('בושם הדרים', 'ברגמוט, לימון · 50 מ״ל', '₪450'), ('בושם מאסק', 'מאסק, ענבר · 50 מ״ל', '₪560')]
    generic_small = small_rows(rows, icon_perfume)
    compare = compare_rows(rows, [700, 920, 1140, 1360], icon_perfume, 2.25, 'תווים, מ״ל ומחיר.', 'בשמים · 50 מ״ל')

    window = studio_window(3.3, 4.4, 25, '<img class="cover" src="assets/velune/02-porte-closed-wall-m.webp" alt="">', 'VELUNE° · Maison de Parfum') + into_window(3.3, 4.1, 3.3, 3.75, 540, 965)

    ink = '#1E2A38'
    door = f"""
<section class="stack" style="animation-name: {show(4.0, 7.5, .2)}" dir="rtl">
  <div class="stack" style="background: #DCE3EB; animation-name: {circle_open(3.75, 540, 965, .55)}">
    {seq('assets/velune/porte/d%02d.webp', 3.75, 6.15, 4.4, .043, 1, 40)}
    {seq('assets/velune/porte/e%02d.webp', 6.1, 7.6, 6.12, .033, 1, 40)}
    {fade_band('rgba(220,227,235,.95)', True, 24)}{fade_band('rgba(220,227,235,.95)', False, 24)}
    <div class="stack" style="animation-name: {show(6.1, 7.6, .1)}">{svg(thread('M540 1720 V1080', 6.15, 7.2, 5), 20)}</div>
    {ball([(3.75, 540, 965), (6.1, 540, 965), (6.4, 540, 1500), (7.25, 540, 1080)], 80)}
    <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 80px; line-height: 1.15; color: {ink}; animation-name: {rise(4.6)}">בושם הוא לא ריח.</div>
    <div class="disp" style="position: absolute; top: 1600px; right: 80px; left: 80px; font-size: 130px; line-height: 1; font-style: italic; color: #8E1E44; animation-name: {rise(6.37, .4)}">הוא מקום.</div>
  </div>
</section>"""

    fx = 790
    fruit = f"""
<section class="stack" style="background: #DCE3EB; animation-name: {show(7.35, 10.0, .2)}" dir="rtl">
  {seq('assets/velune/fruit/a%02d.webp', 7.3, 8.55, 7.4, .028, 1, 40)}
  {seq('assets/velune/fruit/b%02d.webp', 8.5, 10.1, 8.52, .03, 1, 40)}
  {fade_band('rgba(220,227,235,.95)', True, 26)}{fade_band('rgba(220,227,235,.95)', False, 22)}
  {svg(thread(f'M{fx} 700 V1460', 7.45, 9.6, 5), 20)}
  {ball([(7.35, 540, 1080), (7.6, fx, 700), (9.6, fx, 1460)], 64)}
  <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 66px; line-height: 1.2; color: {ink}; animation-name: {rise(7.5)}">גן אחד. פרי אחד.<br>טיפה אחת.</div>
  <div class="disp" style="position: absolute; top: 1620px; right: 80px; left: 80px; font-size: 92px; line-height: 1.1; font-style: italic; color: #8E1E44; animation-name: {rise(9.2, .4)}">והיא כבר בקבוק.</div>
</section>"""

    hours = [('AUBE', 'שחר', '10-bottle-aube-day-m', '#DCE3EB', ink), ('FLORAISON', 'פריחה', '11-bottle-floraison-blush-m', '#F1D9DC', ink),
             ('CRÉPUSCULE', 'דמדומים', '12-bottle-crepuscule-dusk-m', '#9A7E99', '#F4EEF2')]
    swaps = [9.95, 10.46, 10.97]
    bx = [880, 540, 200]

    def arc_y(x):
        u = (960 - x) / 840
        return round((1 - u) ** 2 * 420 + 2 * (1 - u) * u * 260 + u ** 2 * 420)
    layers = ''
    for i, ((fr, he, img, bg, fg), t) in enumerate(zip(hours, swaps)):
        end = swaps[i + 1] + .45 if i < 2 else 11.8
        layers += f"""
  <div class="stack" style="background: {bg}; animation-name: {circle_open(t, bx[i], arc_y(bx[i]), .45)}; z-index: {i + 1}">
    <img src="assets/velune/{img}.webp" alt="" style="position: absolute; top: 200px; left: 0; width: 1080px; height: 1720px; object-fit: cover">
    <div class="stack" style="background: linear-gradient(180deg, {bg} 0, {bg} 210px, transparent 340px)"></div>{fade_band(bg, False, 22)}
    <div class="stack" style="animation-name: {show(t + .05, end, .1)}">
      <div style="position: absolute; top: 90px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 84px; letter-spacing: .12em; line-height: 1; color: {fg}" dir="ltr">{fr}</div>
      <div class="disp" style="position: absolute; top: 186px; left: 0; right: 0; text-align: center; font-size: 42px; color: {fg}">{he}</div>
    </div>
  </div>"""
    beads = ''.join(f'<div style="position: absolute; left: {x - 16}px; top: {arc_y(x) - 16}px; width: 32px; height: 32px; box-sizing: border-box; border-radius: 50%; background: {h[3]}; border: 4px solid #C4765A; z-index: 21"></div>' for x, h in zip(bx, hours))
    bst = [(9.6, fx, 1460), (9.95, bx[0], arc_y(bx[0]))]
    for i in (1, 2):
        bst += [(swaps[i] - .25, bx[i - 1], arc_y(bx[i - 1])), (swaps[i], bx[i], arc_y(bx[i]))]
    sun = f"""
<section class="stack" style="animation-name: {show(9.9, 11.85, .15)}" dir="rtl">
  {layers}
  {svg(thread('M960 420 Q540 260 120 420', 9.95, 10.4, 5), 20)}
  <div class="stack" style="z-index: 21; animation-name: {show(10.1, 11.85, .15)}">{beads}</div>
  <div class="disp" style="position: absolute; bottom: 110px; left: 0; right: 0; text-align: center; z-index: 22">
    <span style="display: inline-block; padding: 16px 40px; background: rgba(250,248,243,.92); border-radius: 999px; font-size: 48px; color: {ink}; animation-name: {rise(10.2)}">לא שלושה ניחוחות. שלוש שעות.</span></div>
  {ball(bst, 72, 23)}
</section>"""

    close_inner = '<img class="cover" src="assets/velune/04-porte-open-garden-m.webp" alt="">'
    body = (hook(4, 25, generic_small, 'assets/velune/porte/d40.webp') + compare + window + door + fruit + sun
            + close(4, 11.65, 25, 'VELUNE°', close_inner, 'בושם הוא לא ריח. הוא מקום.', 'בפרק הבא: האופי · ENCORE°'))
    return page('ככה בוחרים · פרק 04 · הסיפור', body)


# ─────────────────────────── EPISODE 05 · ENCORE · האופי ───────────────────────────
# music ep05-15s.mp3 = the ep01 cut (0:54.94–1:09.94): quiet to 3.3 · chorus 3.3 · two-beat steps 6.48 / 7.48 / 8.50 / 9.52 · drops at 15.
# The thread is the day: the pendant lands, then the ball walks the half sun through four hours and rolls into the box.
def ep05():
    _css.clear()
    rows = [('שרשרת זהב 18K', '3.1 גרם', '₪2,450'), ('שרשרת זהב 18K', '4.6 גרם', '₪3,590'),
            ('צמיד זהב 18K', '5.2 גרם', '₪4,100'), ('טבעת זהב 18K', '2.8 גרם', '₪2,190')]
    generic_small = small_rows(rows, icon_chain)
    compare = compare_rows(rows, [700, 920, 1140, 1360], icon_chain, 2.25, 'זהב 18K. גרם, ומחיר.', 'תכשיטים · לפי משקל')

    gold, cream, bg = '#D9B26A', '#F6EEE4', '#6E4E4A'
    window = studio_window(3.3, 4.4, 28, '<img class="cover" src="assets/encore/landed.webp" alt="" style="object-position: 50% 60%">', 'ENCORE° · Maison de Bijoux') + into_window(3.3, 4.1, 3.3, 3.75, 540, 960)

    land = f"""
<section class="stack" style="animation-name: {show(4.0, 6.75, .2)}" dir="rtl">
  <div class="stack" style="background: {bg}; animation-name: {circle_open(3.75, 540, 960, .55)}">
    {seq('assets/encore/land/l%02d.webp', 3.75, 6.9, 4.1, .03, 1, 72)}
    {fade_band('rgba(70,46,40,.9)', True, 26)}{fade_band('rgba(70,46,40,.9)', False, 24)}
    {ball([(3.75, 540, 960), (4.48, 540, 960), (6.0, 760, 1440)], 64)}
    <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 76px; line-height: 1.15; color: {cream}; animation-name: {rise(4.48)}">מכאן, הוא כבר לא יורד.</div>
    <div class="disp" style="position: absolute; top: 1610px; right: 80px; left: 80px; font-size: 96px; line-height: 1.1; font-style: italic; color: {gold}; animation-name: {rise(5.5, .4)}">לא שוקלים אותו.</div>
  </div>
</section>"""

    hours = [('06:00', 'Aube', 'הדבר הראשון שאת עונדת בבוקר.', 'rings-1', '#B38A7F'), ('12:00', 'Midi', 'באמצע היום, היא עדיין שם.', 'pendants-1', '#7F93C4'),
             ('18:00', 'Lave', 'צמיד שזוכר איפה היית.', 'bracelets-1', '#D27A52'), ('00:00', 'Minuit', 'כשהיום נגמר, את נשארת.', 'earrings-1', '#B9A6D6')]
    swaps = [6.48, 7.48, 8.50, 9.52]
    cx, cy, R = 540, 1720, 380
    angs = [15, 65, 115, 165]

    def on_sun(a):
        r = math.radians(a)
        return round(cx + R * math.cos(r)), round(cy - R * math.sin(r))
    layers = ''
    for i, ((hh, fr, line, img, col), t) in enumerate(zip(hours, swaps)):
        x, y = on_sun(angs[i])
        end = swaps[i + 1] + .45 if i < 3 else 10.75
        layers += f"""
  <div class="stack" style="background: {col}; animation-name: {circle_open(t, x, y, .5)}; z-index: {i + 1}">
    <div class="stack" style="animation-name: {show(t + .05, end, .12)}">
      <div style="position: absolute; top: 140px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 170px; line-height: 1; color: {cream}" dir="ltr">{hh}</div>
      <div style="position: absolute; top: 320px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 48px; letter-spacing: .1em; color: {cream}" dir="ltr">{fr}</div>
      <div class="disp" style="position: absolute; top: 410px; right: 80px; left: 80px; text-align: center; font-size: 58px; line-height: 1.2; color: {cream}">{line}</div>
      <img src="assets/encore/{img}.webp" alt="" style="position: absolute; top: 600px; left: 290px; width: 500px; height: 640px; object-fit: contain; filter: drop-shadow(0 30px 40px rgba(40,24,20,.35)); animation-name: {anim([(t, 'transform:scale(.84) translateY(30px)'), (t + .45, 'transform:none')])}">
    </div>
  </div>"""
    beads = ''.join(f'<div style="position: absolute; left: {on_sun(a)[0] - 18}px; top: {on_sun(a)[1] - 18}px; width: 36px; height: 36px; box-sizing: border-box; border-radius: 50%; background: {h[4]}; border: 4px solid {cream}; z-index: 21"></div>' for a, h in zip(angs, hours))
    bst = [(6.0, 760, 1440), (6.48, *on_sun(angs[0]))]
    for k in range(1, 4):
        t0, t1 = swaps[k] - .3, swaps[k]
        bst.append((t0, *on_sun(angs[k - 1])))
        for j in range(1, 5):
            bst.append((t0 + (t1 - t0) * j / 5, *on_sun(angs[k - 1] + 50 * j / 5)))
        bst.append((t1, *on_sun(angs[k])))
    sun = f"""
<section class="stack" style="animation-name: {show(6.4, 10.8, .15)}" dir="rtl">
  {layers}
  {svg(thread(f'M{cx + R} {cy} A{R} {R} 0 0 0 {cx - R} {cy}', 6.48, 7.0, 5, cream), 20)}
  <div class="stack" style="z-index: 21; animation-name: {show(6.7, 10.8, .15)}">{beads}</div>
  {ball(bst + [(10.3, *on_sun(165)), (10.75, 540, 1000)], 72, 23)}
</section>"""

    box = f"""
<section class="stack" style="background: {bg}; animation-name: {show(10.6, 12.15, .2)}" dir="rtl">
  <div class="stack" style="animation-name: {circle_open(10.6, 540, 1000, .4)}">
    <img class="cover" src="assets/encore/box-open.webp" alt="" style="object-position: 50% 40%">
    {fade_band('rgba(70,46,40,.97)', False, 48)}
    <div class="disp" style="position: absolute; top: 1420px; right: 80px; left: 80px; font-size: 54px; line-height: 1.2; color: {cream}; animation-name: {rise(10.7, .4)}">שנה אחרי, הקופסה עוד זוכרת.</div>
    <div class="disp" style="position: absolute; top: 1540px; right: 80px; left: 80px; font-size: 84px; line-height: 1.12; font-style: italic; color: {gold}; animation-name: {rise(10.95, .4)}">״הוא לא ירד ממני<br>יום אחד.״</div>
  </div>
</section>"""

    close_inner = f'<div class="stack" style="background: {bg}"><img class="cover" src="assets/encore/landed.webp" alt="" style="object-position: 50% 50%"></div>'
    body = (hook(5, 28, generic_small, 'assets/encore/landed.webp') + compare + window + land + sun + box
            + close(5, 12.0, 28, 'ENCORE°', close_inner, 'תכשיט אחד. שנים עלייך.', 'בפרק הבא, האחרון: הידיים · ORÉVA°'))
    return page('ככה בוחרים · פרק 05 · האופי', body)


# ─────────────────────────── EPISODE 06 · ORÉVA · הידיים ───────────────────────────
# music ep06-15s.mp3 = the ep02 cut (1:18.41–1:33.41), the end of the track: quiet to 3.8 · chorus 3.84 · beats 4.53 / 5.53 / 6.53 / 7.55 / 8.55 · winds down from 10.6.
# The thread goes from her hands to the bottle, then becomes the before/after line that the ball drags across the cheek.
def ep06():
    _css.clear()
    rows = [('סרום ויטמין C', '15% · 30 מ״ל', '₪189'), ('סרום היאלורוני', '2% · 30 מ״ל', '₪159'),
            ('סרום ניאצינמיד', '10% · 30 מ״ל', '₪149'), ('סרום רטינול', '0.3% · 30 מ״ל', '₪219')]
    generic_small = small_rows(rows, icon_serum)
    compare = compare_rows(rows, [700, 920, 1140, 1360], icon_serum, 2.25, 'אחוזים, מ״ל ומחיר.', 'טיפוח · סרומים', b=3.35)

    ink, copper, cream = '#3A2E29', '#8F5A3C', '#F6EFE7'
    window = studio_window(3.25, 4.2, 24, '<img class="cover" src="assets/oreva/founder-facial-treatment.webp" alt="" style="object-position: 30% 50%">', 'ORÉVA° · Skin Studio') + into_window(3.25, 4.05, 3.3, 3.84, 540, 960)

    hx, hy = 712, 1330
    hands = f"""
<section class="stack" style="animation-name: {show(3.84, 6.75, .2)}" dir="rtl">
  <div class="stack" style="background: {cream}; animation-name: {circle_open(3.84, 540, 960, .55)}">
    <img src="assets/oreva/founder-facial-treatment.webp" alt="" style="position: absolute; top: 380px; left: 0; width: 1080px; height: 1540px; object-fit: cover; object-position: 28% 50%; transform-origin: {hx}px {hy - 380}px; animation-name: {anim([(3.84, 'transform:scale(1)'), (6.75, 'transform:scale(1.07)')])}">
    <div class="stack" style="background: linear-gradient(180deg, {cream} 0, {cream} 390px, transparent 520px)"></div>
    {ball([(3.84, 540, 960), (4.53, hx, hy)], 64)}
    <div class="disp" style="position: absolute; top: 110px; right: 80px; left: 80px; font-size: 130px; line-height: 1; font-style: italic; color: {copper}; animation-name: {rise(4.53, .4)}">קודם הידיים.</div>
    <div class="disp" style="position: absolute; top: 280px; right: 80px; left: 80px; font-size: 50px; line-height: 1.25; color: {ink}; animation-name: {rise(5.53)}">ארבע עשרה שנה בחדר הטיפולים.</div>
  </div>
</section>"""

    bottle = f"""
<section class="stack" style="animation-name: {show(6.5, 8.75, .2)}" dir="rtl">
  <div class="stack" style="background: {cream}; animation-name: {circle_open(6.53, hx, hy, .5)}">
    <img class="cover" src="assets/oreva/lineup-three-serums-podiums.webp" alt="" style="object-position: 50% 60%">
    {fade_band('rgba(246,239,231,.97)', True, 26)}{fade_band('rgba(246,239,231,.97)', False, 30)}
    {svg(thread(f'M{hx} {hy} C {hx} 1260, 540 1260, 540 1200', 6.55, 7.05, 5), 20)}
    {ball([(6.53, hx, hy), (7.05, 540, 1200)], 64)}
    <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 104px; line-height: 1.05; font-style: italic; color: {copper}; animation-name: {rise(6.6, .4)}">אחר כך הבקבוק.</div>
    <div class="disp" style="position: absolute; top: 1520px; right: 80px; left: 80px; font-size: 54px; line-height: 1.25; color: {ink}; animation-name: {rise(7.55)}">שבעה מוצרים. כל אחד היה קודם<br>על העור של הלקוחות שלה.</div>
  </div>
</section>"""

    # before/after: the ball drags the line from right to left, "after" is revealed behind it (RTL)
    t0, t1, y = 8.75, 10.5, 1000
    line_k = anim([(t0, 'transform:translateX(1040px)'), (t1, 'transform:translateX(40px)')])
    reveal = anim([(t0, 'clip-path:inset(0 0 0 1040px)'), (t1, 'clip-path:inset(0 0 0 40px)')])
    bloom = f"""
<section class="stack" style="background: {cream}; animation-name: {show(8.55, 12.25, .2)}" dir="rtl">
  <div class="stack" style="animation-name: {circle_open(8.55, 540, 1200, .45)}">
    <img class="cover" src="assets/oreva/skin-before.webp" alt="" style="object-position: 72% 50%">
    <img class="cover" src="assets/oreva/skin-after.webp" alt="" style="object-position: 72% 50%; animation-name: {reveal}; animation-timing-function: linear">
    {fade_band('rgba(246,239,231,.97)', True, 22)}{fade_band('rgba(246,239,231,.97)', False, 28)}
    <div style="position: absolute; top: 0; bottom: 0; left: 0; width: 4px; margin-left: -2px; background: #C4765A; animation-name: {line_k}; animation-timing-function: linear"></div>
    <span class="pill" style="top: 360px; right: 60px; left: auto; background: #C4765A; color: #FAF8F3; animation-name: {show(9.2, 12.25, .2)}">אחרי</span>
    <span class="pill" style="top: 360px; left: 60px; right: auto; background: #2E2A27; color: #F4F2EF; animation-name: {show(8.8, 12.25, .2)}">לפני</span>
    <div class="disp" style="position: absolute; top: 150px; right: 80px; left: 80px; font-size: 66px; line-height: 1.2; color: {ink}; animation-name: {rise(8.7)}">28 ימים עם השלישייה.</div>
    <div class="disp" style="position: absolute; top: 1540px; right: 80px; left: 80px; font-size: 64px; line-height: 1.2; color: {ink}; animation-name: {rise(10.6)}">וכשהבקבוק נפתח,<br><em style="color: {copper}">הידיים שלה ממשיכות בבית.</em></div>
  </div>
  {ball([(8.55, 540, 1200), (t0, 1040, y), (t1, 40, y)], 72, 23)}
</section>"""

    close_inner = '<img class="cover" src="assets/oreva/founder-cream-on-hand.webp" alt="" style="object-position: 30% 50%">'
    body = (hook(6, 24, generic_small, 'assets/oreva/founder-cream-on-hand.webp') + compare + window + hands + bottle + bloom
            + close(6, 12.05, 24, 'ORÉVA°', close_inner, 'קודם הידיים. אחר כך הבקבוק.', 'זה הפרק האחרון. שש שכבות, ובכולן אותה החלטה:<br>לתת ללקוחה סיבה לבחור שהיא לא המחיר.'))
    return page('ככה בוחרים · פרק 06 · הידיים', body)


if __name__ == '__main__':
    (HERE / 'ep01-pancakerie.html').write_text(ep01(), encoding='utf8')
    (HERE / 'ep02-chasen.html').write_text(ep02(), encoding='utf8')
    (HERE / 'ep03-miel.html').write_text(ep03(), encoding='utf8')
    (HERE / 'ep04-velune.html').write_text(ep04(), encoding='utf8')
    (HERE / 'ep05-encore.html').write_text(ep05(), encoding='utf8')
    (HERE / 'ep06-oreva.html').write_text(ep06(), encoding='utf8')
    print('ok')
