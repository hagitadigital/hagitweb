#!/usr/bin/env python3
"""ROSÉE° · Sept Matins — brand-mode reel (9:16, 30s). Builds reel.html next to this file.

Timeline (s): hook 0–2.5 · logo 2.4–4.1 · La Goutte 3.9–9.3 · La Semaine 9.0–16.3 (signature) ·
Le Rituel 16.0–20.8 · Le Rituel shop 20.5–24.3 · 08:00 24.0–27.2 · outro 27.0–30 (holds to the last frame).
"""
import pathlib, re

HERE = pathlib.Path(__file__).parent
TEMPLATE = HERE.parents[2] / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
P = lambda t: f"{max(0, min(D, t)) / D * 100:.3f}%"

css = []

# ── palette ────────────────────────────────────────────────────────────
PLUM, GLASS, ROSE, COPPER = '#E5C4CB', '#E8B4B8', '#C9878E', '#C28A5A'
CREAM, LINEN, INK, INK2, CTEXT = '#F7F0E6', '#FBF6EE', '#3B2E33', '#6E5A61', '#6E4A2A'


def kf(name, stops):
    """stops: list of (t, decl) — written as percentage keyframes; first at 0%, last held to 100%."""
    body = ''.join(f"{P(t)}{{{d}}}" for t, d in stops)
    css.append(f"@keyframes {name}{{0%{{{stops[0][1]}}}{body}100%{{{stops[-1][1]}}}}}")
    css.append(f".{name}{{animation-name:{name}}}")


def drop(size, fill, extra=''):
    # teardrop pointing up: square, sharp top-right corner, rotated −45°
    return (f'<div style="width: {size}px; height: {size}px; border-radius: 50% 0 50% 50%; transform: rotate(-45deg); '
            f'{fill}; {extra}"></div>')


# ── HOOK (0–2.5) ───────────────────────────────────────────────────────
kf('hk', [(0, 'opacity:1'), (2.5, 'opacity:1'), (2.8, 'opacity:0')])
kf('d14', [(0, 'opacity:1'), (0.95, 'opacity:1'), (1.1, 'opacity:0')])
kf('d15', [(0, 'opacity:0'), (0.95, 'opacity:0'), (1.1, 'opacity:1')])
kf('hlit', [(0, 'opacity:0'), (0.95, 'opacity:0'), (1.15, 'opacity:1')])
kf('hfall', [(0, 'transform:translateY(0);opacity:1'), (1.55, 'transform:translateY(0);opacity:1'),
             (2.05, 'transform:translateY(395px);opacity:1'), (2.1, 'transform:translateY(400px);opacity:0')])
kf('hrip', [(0, 'transform:scale(.3);opacity:0'), (2.05, 'transform:scale(.3);opacity:0'),
            (2.15, 'transform:scale(.5);opacity:1'), (2.7, 'transform:scale(1.5);opacity:0')])
kf('hhalo', [(0, 'transform:scale(.6);opacity:0'), (1.0, 'transform:scale(.6);opacity:0'),
             (1.15, 'transform:scale(1);opacity:.9'), (1.6, 'transform:scale(1.9);opacity:0')])

ticks = ''
for ang in (-75, -50, -25, 25, 50, 75):
    ticks += (f'<div style="position: absolute; left: 540px; top: 1300px; width: 0; height: 0; transform: rotate({ang}deg)">'
              f'<div style="position: absolute; left: -6px; top: -436px; width: 12px; height: 12px; border-radius: 999px; background: {COPPER}"></div></div>')

hook = f'''
<div class="hk stack" style="background: linear-gradient(180deg, {PLUM} 0%, {CREAM} 88%)">
  <div style="position: absolute; top: 96px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 34px; letter-spacing: .42em; color: {INK}" dir="ltr">ROSÉE°</div>
  <div style="position: absolute; top: 250px; left: 80px; right: 80px; text-align: center; font-family: 'Assistant', 'Heebo', sans-serif; font-size: 92px; line-height: 1.16; font-weight: 200; color: {INK}" dir="rtl">מה את עושה<br><span style="font-weight: 600">בדקות</span> שלפני<br>הקפה?</div>
  <div style="position: absolute; left: 110px; top: 870px; width: 860px; height: 430px; overflow: hidden">
    <div style="position: absolute; left: 0; top: 0; width: 860px; height: 860px; box-sizing: border-box; border-radius: 999px; border: 3px solid {COPPER}"></div>
  </div>
  {ticks}
  <div style="position: absolute; left: 80px; right: 80px; top: 1299px; height: 3px; background: {COPPER}; border-radius: 999px"></div>
  <div style="position: absolute; top: 1080px; left: 0; right: 0; height: 170px; font-family: 'Cormorant Garamond', serif; font-size: 170px; line-height: 1; color: {INK}; text-align: center" dir="ltr">
    <div class="d14 stack">06:14</div><div class="d15 stack">06:15</div>
  </div>
  <div style="position: absolute; left: 540px; top: 870px; width: 0; height: 0">
    <div class="hhalo" style="position: absolute; left: -60px; top: -60px; width: 120px; height: 120px; border-radius: 999px; background: rgba(232,180,184,.7)"></div>
    <div class="hfall" style="position: absolute; left: -26px; top: -30px">
      {drop(52, f'border: 3px solid {ROSE}; box-sizing: border-box; background: rgba(251,246,238,.6)')}
      <div class="hlit" style="position: absolute; inset: 0">{drop(52, f'background: {ROSE}', 'box-shadow: 0 6px 18px rgba(59,46,51,.18)')}</div>
    </div>
  </div>
  <div class="hrip" style="position: absolute; left: 400px; top: 1270px; width: 280px; height: 60px; box-sizing: border-box; border-radius: 50%; border: 3px solid {ROSE}"></div>
  <div style="position: absolute; top: 1400px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 54px; color: {INK}" dir="ltr">Sept Matins · Matin 01</div>
    <div style="font-family: 'Assistant', 'Heebo', sans-serif; font-size: 40px; font-weight: 300; color: {INK2}" dir="rtl">שבעה בקרים. טיפה אחת בכל אחד.</div>
  </div>
</div>'''

# ── LOGO (2.4–4.1) ─────────────────────────────────────────────────────
kf('lgline', [(0, 'transform:scaleX(0)'), (2.7, 'transform:scaleX(0)'), (3.4, 'transform:scaleX(1)')])
logo = f'''
<section class="scene" data-show="2.4,4.1" style="background: {PLUM}">
  <div style="position: absolute; top: 760px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 30px">
    <div data-in="2.5" style="font-family: 'Cormorant Garamond', serif; font-size: 132px; letter-spacing: .42em; padding-left: .42em; color: {INK}" dir="ltr">ROSÉE°</div>
    <div class="lgline" style="width: 420px; height: 3px; background: {COPPER}; border-radius: 999px"></div>
    <div data-in="2.9" style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 60px; color: {CTEXT}" dir="ltr">Née à l'aube</div>
  </div>
</section>'''

# ── LA GOUTTE (3.9–9.3) — the site's sequence ─────────────────────────
goutte = f'''
<section class="scene" data-show="3.9,9.3">
  <div class="stack" data-seq="assets/seq/f_%03d.webp" data-from="1" data-to="79" data-by="2" data-start="4.2" data-step="0.085" data-fit="cover" data-pos="50% 50%"></div>
  <div class="stack" style="background: linear-gradient(180deg, rgba(247,240,230,.95) 0px, rgba(247,240,230,.75) 560px, rgba(247,240,230,0) 820px)"></div>
  <div style="position: absolute; top: 170px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: center; gap: 18px; text-align: center; font-family: 'Assistant', 'Heebo', sans-serif; color: {INK}" dir="rtl">
    <div data-in="4.2" style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 56px; color: {CTEXT}" dir="ltr">La Goutte</div>
    <div data-in="4.7" style="font-size: 76px; font-weight: 200; line-height: 1.15">הטל נוצר <span style="font-weight: 600">בלילה</span>.</div>
    <div data-in="5.7" style="font-size: 76px; font-weight: 200; line-height: 1.15">זוהר עם <span style="font-weight: 600">שחר</span>.</div>
    <div data-in="7.0" style="font-size: 48px; font-weight: 300; line-height: 1.3; color: {INK2}">ונעלם עד הצהריים, אלא אם עוצרים אותו.</div>
  </div>
</section>'''

# ── LA SEMAINE (9.0–16.3) — signature: the week dial ──────────────────
N, R, CX, CY = 7, 330, 540, 1010
A = 360 / N
T0, STEP, MOVE = 9.6, 0.8, 0.35
arr = [T0 + k * STEP for k in range(N)]          # arrival of morning k under the pointer
skies = ['#D9A8B3', '#DFB5BE', '#E5C2C7', '#EBCFCF', '#F0DBD7', '#F4E6DF', CREAM]

ring, sky = [(0, 'transform:rotate(0deg)')], [(0, f'background-color:{skies[0]}')]
for k in range(N):
    if k:
        ring.append((arr[k] - MOVE, f'transform:rotate({(k - 1) * A:.3f}deg)'))
        ring.append((arr[k], f'transform:rotate({k * A:.3f}deg)'))
        sky.append((arr[k] - MOVE, f'background-color:{skies[k - 1]}'))
        sky.append((arr[k], f'background-color:{skies[k]}'))
kf('ring', ring)
kf('cring', [(t, d.replace('rotate(', 'rotate(-')) for t, d in ring])
kf('sky', sky)
kf('dialin', [(0, 'transform:scale(.85);opacity:0'), (9.1, 'transform:scale(.85);opacity:0'), (9.6, 'transform:scale(1);opacity:1')])

slots = ''
for i in range(N):
    kf(f'lit{i}', [(0, 'opacity:0'), (arr[i] - .02, 'opacity:0'), (arr[i] + .15, 'opacity:1')])
    slots += f'''
    <div style="position: absolute; left: 0; top: 0; width: 0; height: 0; transform: rotate({-i * A:.3f}deg) translateY(-{R}px) rotate({i * A:.3f}deg)">
      <div class="cring" style="position: absolute; left: 0; top: 0; width: 0; height: 0">
        <div style="position: absolute; left: -26px; top: -30px">
          {drop(52, f'border: 3px solid {COPPER}; box-sizing: border-box; background: rgba(251,246,238,.55)')}
          <div class="lit{i}" style="position: absolute; inset: 0">{drop(52, f'background: {ROSE}', 'box-shadow: 0 6px 16px rgba(59,46,51,.2)')}</div>
        </div>
        <div style="position: absolute; left: -40px; top: 34px; width: 80px; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 30px; color: {CTEXT}" dir="ltr">0{i + 1}</div>
      </div>
    </div>'''

falls = ''
for k in range(N):
    t = arr[k]
    kf(f'fall{k}', [(0, 'transform:translateY(0);opacity:0'), (t - .01, 'transform:translateY(0);opacity:0'), (t + .05, 'transform:translateY(0);opacity:1'),
                    (t + .4, 'transform:translateY(160px);opacity:1'), (t + .45, 'transform:translateY(170px);opacity:0')])
    kf(f'rip{k}', [(0, 'transform:scale(1);opacity:0'), (t + .38, 'transform:scale(1);opacity:0'), (t + .45, 'transform:scale(1.02);opacity:.9'),
                   (t + 1.0, 'transform:scale(1.32);opacity:0')])
    falls += f'''
    <div class="fall{k}" style="position: absolute; left: -16px; top: {-R + 40}px">{drop(32, f'background: {ROSE}')}</div>
    <div class="rip{k}" style="position: absolute; left: -200px; top: -200px; width: 400px; height: 400px; box-sizing: border-box; border-radius: 999px; border: 3px solid {ROSE}"></div>'''

lines = [
    'טיפה <b>אחת</b>, לפני הקפה.',
    'העור מתעורר <b>לפנייך</b>.',
    'הסרום נכנס כשהעור עוד <b>לח</b>.',
    'בוקר רביעי. <b>כבר</b> הרגל.',
    'עשר דקות שהן <b>שלך</b>.',
    'הטל נשאר <b>בפנים</b>.',
]
centre, under = '', ''
for k in range(N):
    end = arr[k + 1] if k + 1 < N else 16.3
    centre += (f'<div class="stack" data-show="{arr[k] - .05:.2f},{end - .05:.2f}" data-fade="0.18" style="display: flex; align-items: center; justify-content: center; '
               f"font-family: 'Cormorant Garamond', serif; font-size: 74px; color: {INK}\" dir=\"ltr\">Matin 0{k + 1}</div>")
    if k < N - 1:
        under += (f'<div class="stack" data-show="{arr[k]:.2f},{end - .05:.2f}" data-fade="0.18" style="display: flex; justify-content: center; '
                  f"font-size: 62px; font-weight: 300\" dir=\"rtl\"><span>{lines[k].replace('<b>', '<span style=\"font-weight: 600\">').replace('</b>', '</span>')}</span></div>")

kf('pay', [(0, 'opacity:0;transform:translateY(30px)'), (arr[-1] + .1, 'opacity:0;transform:translateY(30px)'), (arr[-1] + .6, 'opacity:1;transform:none')])
semaine = f'''
<section class="scene" data-show="9.0,16.3">
  <div class="sky stack"></div>
  <div style="position: absolute; top: 180px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 8px; color: {INK}">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 78px" dir="ltr">Sept Matins</div>
    <div style="font-family: 'Assistant', 'Heebo', sans-serif; font-size: 44px; font-weight: 300; letter-spacing: .04em" dir="rtl">שבעה בקרים · 06:15</div>
  </div>
  <div class="dialin" style="position: absolute; left: {CX}px; top: {CY}px; width: 0; height: 0">
    <div style="position: absolute; left: -{R}px; top: -{R}px; width: {2 * R}px; height: {2 * R}px; box-sizing: border-box; border-radius: 999px; border: 2px solid {COPPER}"></div>
    <div style="position: absolute; left: -2px; top: -{R + 92}px; width: 4px; height: 38px; border-radius: 999px; background: {COPPER}"></div>
    <div style="position: absolute; left: -190px; top: -190px; width: 380px; height: 380px; border-radius: 999px; background: {LINEN}; box-shadow: 0 24px 60px rgba(59,46,51,.12)"></div>
    {falls}
    <div style="position: absolute; left: -190px; top: -80px; width: 380px; height: 110px">{centre}</div>
    <div style="position: absolute; left: -190px; top: 34px; width: 380px; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 52px; color: {CTEXT}" dir="ltr">06:15</div>
    <div class="ring" style="position: absolute; left: 0; top: 0; width: 0; height: 0">{slots}
    </div>
  </div>
  <div style="position: absolute; top: 1470px; left: 60px; right: 60px; height: 90px; font-family: 'Assistant', 'Heebo', sans-serif; color: {INK}">{under}</div>
  <div class="pay" style="position: absolute; top: 1450px; left: 60px; right: 60px; text-align: center; font-family: 'Assistant', 'Heebo', sans-serif; font-size: 92px; font-weight: 200; color: {INK}" dir="rtl">הבוקר כבר <span style="font-weight: 600">שלך</span>.</div>
</section>'''

# ── LE RITUEL (16.0–20.8) ──────────────────────────────────────────────
steps = [('05:30', 'La Brume', 'brume', 'מעירים את העור', 'ענן של מי טל על פנים נקיות.'),
         ('06:15', 'Le Réveil', 'reveil', 'טיפה אחת', 'הסרום נכנס כשהעור עוד לח.'),
         ('07:45', 'La Lumière', 'lumiere', 'חותמים באור', 'מה שנכנס בבוקר נשאר עד הערב.')]
kf('axis', [(0, 'transform:scaleY(0)'), (16.4, 'transform:scaleY(0)'), (18.6, 'transform:scaleY(1)')])
rows = ''
for j, (tm, fr, img, he, line) in enumerate(steps):
    rows += f'''
    <div data-in="{16.5 + j * .8:.1f}" style="display: flex; align-items: center; gap: 44px; height: 300px" dir="rtl">
      <img src="assets/p/{img}.webp" alt="" style="width: 280px; height: 280px; border-radius: 999px; object-fit: cover; border: 3px solid {COPPER}; flex-shrink: 0; position: relative; z-index: 1">
      <div style="display: flex; flex-direction: column; gap: 4px">
        <div style="display: flex; gap: 20px; align-items: baseline" dir="ltr"><span style="font-family: 'Cormorant Garamond', serif; font-size: 66px; color: {INK}">{tm}</span><span style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 50px; color: {CTEXT}">{fr}</span></div>
        <div style="font-size: 46px; font-weight: 600; color: {INK}">{he}</div>
        <div style="font-size: 38px; font-weight: 300; color: {INK2}">{line}</div>
      </div>
    </div>'''
rituel = f'''
<section class="scene" data-show="16.0,20.8" style="background: {CREAM}">
  <div style="position: absolute; top: 170px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 10px; color: {INK}">
    <div style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 78px" dir="ltr">Le Rituel</div>
    <div style="font-family: 'Assistant', 'Heebo', sans-serif; font-size: 64px; font-weight: 200" dir="rtl">שלושה צעדים. <span style="font-weight: 600">לפני</span> הקפה.</div>
  </div>
  <div class="axis" style="position: absolute; top: 640px; right: 228px; width: 3px; height: 760px; background: {COPPER}; transform-origin: top"></div>
  <div style="position: absolute; top: 500px; right: 90px; left: 60px; display: flex; flex-direction: column; gap: 60px; font-family: 'Assistant', 'Heebo', sans-serif">{rows}
  </div>
</section>'''

# ── MON RITUEL — the cart sorted by morning (20.5–24.3) ───────────────
items = [('05:30', 'La Brume', 'brume', 'מי טל'), ('06:15', 'Le Réveil', 'reveil', 'סרום בוקר'),
         ('07:00', 'Le Voile', 'voile', 'קרם עיניים'), ('07:45', 'La Lumière', 'lumiere', 'קרם יום')]
cart = ''
for j, (tm, fr, img, he) in enumerate(items):
    cart += f'''
      <div data-in="{21.0 + j * .45:.2f}" style="display: flex; align-items: center; gap: 30px; padding: 22px 26px; background: {CREAM}; border-radius: 22px" dir="rtl">
        <img src="assets/p/{img}.webp" alt="" style="width: 150px; height: 150px; border-radius: 18px; object-fit: cover; flex-shrink: 0">
        <div style="display: flex; flex-direction: column; gap: 2px; flex-grow: 1">
          <div style="display: flex; gap: 16px; align-items: baseline" dir="ltr"><span style="font-family: 'Cormorant Garamond', serif; font-size: 54px; color: {INK}">{tm}</span><span style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 44px; color: {CTEXT}">{fr}</span></div>
          <div style="font-size: 36px; font-weight: 300; color: {INK2}">{he}</div>
        </div>
      </div>'''
shop = f'''
<section class="scene" data-show="20.5,24.3" style="background: linear-gradient(180deg, {PLUM} 0%, {CREAM} 70%)">
  <div style="position: absolute; top: 170px; left: 70px; right: 70px; text-align: center; font-family: 'Assistant', 'Heebo', sans-serif; font-size: 64px; font-weight: 200; line-height: 1.2; color: {INK}" dir="rtl">כל מוצר נכנס<br>עם השעה <span style="font-weight: 600">שלו</span>.</div>
  <div style="position: absolute; top: 470px; left: 90px; right: 90px; box-sizing: border-box; padding: 44px 40px; background: {LINEN}; border-radius: 36px; box-shadow: 0 40px 100px rgba(59,46,51,.16); display: flex; flex-direction: column; gap: 22px; font-family: 'Assistant', 'Heebo', sans-serif">
    <div style="display: flex; justify-content: space-between; align-items: baseline" dir="rtl">
      <span style="font-size: 54px; font-weight: 600; color: {INK}">הריטואל שלי</span>
      <span style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 40px; color: {CTEXT}" dir="ltr">Matin 04</span>
    </div>
    <div style="height: 2px; background: {COPPER}"></div>{cart}
    <div data-in="22.9" style="margin-top: 10px; padding: 28px; border-radius: 16px; background: {INK}; color: {LINEN}; text-align: center; font-size: 42px; font-weight: 600" dir="rtl">להמשיך את הבוקר</div>
  </div>
</section>'''

# ── 08:00 — the dew is gone (24.0–27.2) ───────────────────────────────
kf('noon', [(0, f'background-color:{PLUM}'), (24.3, f'background-color:{PLUM}'), (25.6, f'background-color:{CREAM}')])
kf('t745', [(0, 'opacity:1'), (24.75, 'opacity:1'), (24.95, 'opacity:0')])
kf('t800', [(0, 'opacity:0'), (24.75, 'opacity:0'), (24.95, 'opacity:1')])
kf('evap', [(0, 'transform:scale(1);opacity:1'), (25.0, 'transform:scale(1);opacity:1'), (25.9, 'transform:scale(.2) translateY(-40px);opacity:0')])
kf('evhalo', [(0, 'transform:scale(1);opacity:.8'), (25.0, 'transform:scale(1);opacity:.8'), (25.9, 'transform:scale(2.2);opacity:0')])
ticks2 = ticks.replace('top: 1300px', 'top: 1250px')
eight = f'''
<section class="scene" data-show="24.0,27.2">
  <div class="noon stack"></div>
  <div style="position: absolute; left: 110px; top: 820px; width: 860px; height: 430px; overflow: hidden">
    <div style="position: absolute; left: 0; top: 0; width: 860px; height: 860px; box-sizing: border-box; border-radius: 999px; border: 3px solid {COPPER}"></div>
  </div>
  {ticks2}
  <div style="position: absolute; left: 80px; right: 80px; top: 1249px; height: 3px; background: {COPPER}; border-radius: 999px"></div>
  <div style="position: absolute; top: 1030px; left: 0; right: 0; height: 170px; font-family: 'Cormorant Garamond', serif; font-size: 170px; line-height: 1; color: {INK}; text-align: center" dir="ltr">
    <div class="t745 stack">07:45</div><div class="t800 stack">08:00</div>
  </div>
  <div style="position: absolute; left: 540px; top: 820px; width: 0; height: 0">
    <div class="evhalo" style="position: absolute; left: -60px; top: -60px; width: 120px; height: 120px; border-radius: 999px; background: rgba(232,180,184,.7)"></div>
    <div class="evap" style="position: absolute; left: -26px; top: -30px">{drop(52, f'background: {ROSE}')}</div>
  </div>
  <div style="position: absolute; top: 230px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 22px; text-align: center; font-family: 'Assistant', 'Heebo', sans-serif; color: {INK}" dir="rtl">
    <div data-in="24.3" style="font-size: 80px; font-weight: 200; line-height: 1.15">נעלם עד <span style="font-weight: 600">הצהריים</span>.</div>
    <div data-in="25.6" style="font-size: 60px; font-weight: 300; line-height: 1.2; color: {INK2}">מחר ב־06:15 הוא חוזר.</div>
  </div>
  <div data-in="25.0" style="position: absolute; top: 1380px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 50px; color: {CTEXT}" dir="ltr">avant 08:00 · chaque matin</div>
</section>'''

# ── OUTRO (27.0–30, holds) ─────────────────────────────────────────────
outro = f'''
<section class="scene" data-show="27.0,30" style="background: linear-gradient(180deg, {PLUM} 0%, {CREAM} 62%)">
  <div style="position: absolute; top: 300px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 26px">
    <div data-in="27.0">{drop(64, f'background: {ROSE}', 'box-shadow: 0 0 0 16px rgba(232,180,184,.5)')}</div>
    <div data-in="27.1" style="margin-top: 26px; font-family: 'Cormorant Garamond', serif; font-size: 120px; letter-spacing: .42em; padding-left: .42em; color: {INK}" dir="ltr">ROSÉE°</div>
    <div data-in="27.2" style="font-family: 'Cormorant Garamond', serif; font-style: italic; font-size: 52px; color: {CTEXT}" dir="ltr">Née à l'aube</div>
  </div>
  <div data-in="27.6" style="position: absolute; top: 880px; left: 60px; right: 60px; text-align: center; font-family: 'Assistant', 'Heebo', sans-serif; font-size: 96px; font-weight: 200; line-height: 1.16; color: {INK}" dir="rtl">שבעה בקרים.<br>טיפה <span style="font-weight: 600">אחת</span> בכל אחד.</div>
  <div data-in="28.1" style="position: absolute; top: 1330px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 24px; font-family: 'Assistant', 'Heebo', sans-serif">
    <div style="padding: 30px 64px; border-radius: 14px; background: {INK}; color: {LINEN}; font-size: 46px; font-weight: 600" dir="rtl">להתחיל את הבוקר הראשון</div>
    <div style="font-family: 'Cormorant Garamond', serif; font-size: 44px; letter-spacing: .12em; color: {CTEXT}" dir="ltr">Sept Matins · 06:15</div>
  </div>
</section>'''

# ── assemble from the skill template (keeps reel.js and the base CSS) ─
t = TEMPLATE.read_text(encoding='utf8')
head = t.split('/* ── STUDIO wrapper')[0]
head = head.replace('<title>Brand World Reel</title>', '<title>ROSÉE° · Sept Matins</title>')
script = '<script>' + t.split('<script>', 1)[1]
html = (head + '\n'.join(css) + f'''
#stage{{background:{CREAM}}}
</style>
</head>
<body data-duration="30">
<div id="stage">
<div class="film stack">
{goutte}
{semaine}
{rituel}
{shop}
{eight}
{outro}
{logo}
{hook}
</div>
</div>
''' + script)
(HERE / 'reel.html').write_text(html, encoding='utf8')
print('wrote', HERE / 'reel.html', len(html), 'bytes')
