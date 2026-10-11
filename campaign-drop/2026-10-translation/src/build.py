"""The Translation — a 30s studio reel (9:16) built from four live sections.
Hook: a saved trend. Then the same question four times: what does the effect say about the promise?
Run: python3 build.py  →  reel.html   (render with the skill's scripts/render.js)"""
import os
D = 30
def p(t): return '%.3f%%' % (max(0, min(D, t)) / D * 100)
CREAM, INK, COPPER, GOLD, DARK = '#FAF8F3', '#6B563F', '#C4765A', '#B8894A', '#3E2F25'
H = "font-family:'Heebo',sans-serif"
CG = "font-family:'Cormorant Garamond',serif"

# ── the four translations ──────────────────────────────────────────────
S = [  # key, start, world label, trend label, trend mini, promise (main, small), translation, seq, frames, size, tint
 dict(k='pm', t=5.0, name='PARDON ME° · עולם מותג 29', trend="גליץ' בניאון", mini='glitch',
      prom='Polite outside. Not sorry inside.', prom_he='מנומס מבחוץ. לא מתנצל מבפנים.',
      tr=('הגליץ\' הפך להדפסה', 'שיוצאת מהרישום כשגוללים.'), n=54, w=1260, h=820, bg='#F4E6EA'),
 dict(k='so', t=9.9, name='SONAIR° · עולם מותג 23', trend='מריחת תנועה', mini='smear',
      prom='A more human sound.', prom_he='צליל אנושי יותר.',
      tr=('המריחה הפכה לצליל', 'שיוצא ממנה. שלוש חתימות.'), n=60, w=1124, h=562, bg='#ECEEF1'),
 dict(k='sp', t=14.8, name='ספרי המותג · Les Livres', trend='ספירלה בתלת־ממד', mini='helix',
      prom='One decision holds a world.', prom_he='לכל עולם החלטה אחת שמחזיקה אותו.',
      tr=('הספירלה הפכה לשיטה:', 'החלטה, קודים, צבעים, נקודות מגע.'), n=60, w=1072, h=802, bg='#F3EEE6'),
 dict(k='rg', t=19.7, name='הגלריה · 29 עולמות', trend='טבעת תמונות', mini='ring',
      prom='Brand worlds. One signature.', prom_he='עולמות מותג. חתימה אחת.',
      tr=('הטבעת הפכה לארכיון:', 'העולם שבחזית גדל ומציג את עצמו.'), n=60, w=1040, h=1000, bg='#F5F0E8'),
]
LEN = 4.9

css = []
def kf(name, body): css.append('@keyframes %s{%s}' % (name, body))

# generic trend minis (no brand, no names) ------------------------------------------------
NEON = ['#FF2E88', '#2E5BFF', '#E8FF3A', '#2EFFC0', '#B04CFF', '#FF7A1A']
def glitch(big=False):
    s = 1.0 if big else .5
    cards = ''
    for i in range(6):
        x, y, r = 40 + i * 92, 30 + i * 70, [-12, 8, -6, 10, -9, 6][i]
        txt = ['NEW', 'DROP', '00', 'FLUX', 'NOW', 'V2'][i]
        cards += (f'<div style="position:absolute;left:{x*s}px;top:{y*s}px;width:{150*s}px;height:{190*s}px;transform:rotate({r}deg);'
                  f'background:linear-gradient(135deg,{NEON[i]},{NEON[(i+2)%6]});box-shadow:{8*s}px 0 0 rgba(255,0,80,.55),{-8*s}px 0 0 rgba(0,200,255,.55);'
                  f'display:flex;align-items:flex-end;padding:{10*s}px;box-sizing:border-box">'
                  f'<span class="gj" style="font-family:Arial Black,Heebo,sans-serif;font-weight:900;font-size:{38*s}px;color:#111;'
                  f'text-shadow:{4*s}px 0 #FF0050,{-4*s}px 0 #00C8FF">{txt}</span></div>')
    return f'<div style="position:relative;width:{640*s}px;height:{620*s}px">{cards}</div>'
def smear():
    streaks = ''.join(f'<div class="smx" style="position:absolute;right:150px;top:{40+i*16}px;height:12px;width:{120+((i*53)%90)}px;border-radius:6px;'
                      f'background:linear-gradient(to left,{NEON[i%6]},transparent);animation-delay:-{i*.13:.2f}s"></div>' for i in range(10))
    return (f'<div style="position:relative;width:320px;height:240px">{streaks}'
            f'<div style="position:absolute;right:70px;top:30px;width:110px;height:150px;border-radius:55px 55px 40px 40px;background:#9A9AA2"></div></div>')
def helix():
    pan = ''.join(f'<div style="position:absolute;left:-40px;top:{-70+i*24}px;width:80px;height:56px;background:{NEON[i%6]};'
                  f'transform:rotateY({i*55}deg) translateZ(110px);backface-visibility:hidden"></div>' for i in range(7))
    return (f'<div style="position:relative;width:320px;height:240px;perspective:600px">'
            f'<div class="hx" style="position:absolute;left:160px;top:120px;transform-style:preserve-3d">{pan}</div></div>')
def ring():
    sq = ''.join(f'<div style="position:absolute;left:-{12+6*(i%3)}px;top:-{12+6*(i%3)}px;width:{24+12*(i%3)}px;height:{24+12*(i%3)}px;background:{NEON[i%6]};'
                 f'transform:rotate({i*30}deg) translateY(-95px) rotate(-{i*30}deg)"></div>' for i in range(12))
    return (f'<div style="position:relative;width:320px;height:240px"><div class="rgx" style="position:absolute;left:160px;top:120px">{sq}</div></div>')
MINI = dict(glitch=lambda: glitch(False), smear=smear, helix=helix, ring=ring)
css.append('.film *{animation-duration:30s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}')
# small loops for the generic minis run on their own short durations
css.append('.film .gj{animation:gj .18s steps(2) infinite!important}@keyframes gj{0%{transform:translate(0,0)}50%{transform:translate(3px,-2px)}}')
css.append('.film .smx{animation:smx 1.1s ease-in-out infinite!important}@keyframes smx{0%,100%{transform:translateX(0)}50%{transform:translateX(-26px)}}')
css.append('.film .hx{animation:hx 3s linear infinite!important}@keyframes hx{to{transform:rotateY(360deg)}}')
css.append('.film .rgx{animation:rgx 4s linear infinite!important}@keyframes rgx{to{transform:rotate(360deg)}}')

# ── HOOK 0–2.8 (frame 0 already shows the question and its proof) ─────────────────────
kf('hook', f'0%,{p(2.7)}{{opacity:1}}{p(3.0)},100%{{opacity:0}}')
hook = f"""
<div class="stack" style="animation-name:hook;background:#EEE6D8">
  <div style="position:absolute;top:84px;right:80px;display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    <div style="{CG};font-style:italic;font-size:36px;color:{DARK}" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size:17px;letter-spacing:.3em;color:#8B7B6E">חגית אנטבי</div>
  </div>
  <div style="position:absolute;top:230px;left:80px;right:80px;text-align:right;{H};font-size:78px;font-weight:600;line-height:1.16;color:{DARK}" dir="rtl">
    ראית אפקט מהמם<br>אצל מישהו אחר.<br>לשים אותו גם <span style="color:{COPPER}">אצלך</span>?</div>
  <div style="position:absolute;top:760px;left:190px;width:700px;height:860px;border-radius:44px;background:#0E0E12;box-shadow:0 40px 90px rgba(40,26,18,.35);overflow:hidden">
    <div style="position:absolute;inset:26px;border-radius:26px;overflow:hidden;background:#F2F2F4">
      <div style="position:absolute;left:30px;top:90px">{glitch(True)}</div>
      <div style="position:absolute;top:22px;left:22px;right:22px;display:flex;justify-content:space-between;align-items:center" dir="rtl">
        <span style="padding:8px 18px;border-radius:999px;background:#111;color:#fff;font-size:22px;{H}">נשמר ✓</span>
        <span style="{H};font-size:22px;color:#555">השראה · אפקטים</span>
      </div>
    </div>
  </div>
</div>"""

# ── RULE 2.8–5.0: the copper ball draws the line ─────────────────────────────────
kf('rule', f'0%,{p(2.7)}{{opacity:0}}{p(3.0)},{p(4.8)}{{opacity:1}}{p(5.1)},100%{{opacity:0}}')
kf('r1', f'0%,{p(3.0)}{{transform:translateY(110%)}}{p(3.5)},100%{{transform:none}}')
kf('r2', f'0%,{p(3.4)}{{transform:translateY(110%)}}{p(3.9)},100%{{transform:none}}')
kf('ln0', f'0%,{p(3.0)}{{stroke-dashoffset:1}}{p(4.6)},100%{{stroke-dashoffset:0}}')
kf('bl0', f'0%,{p(2.95)}{{offset-distance:0%;opacity:0}}{p(3.0)}{{offset-distance:0%;opacity:1}}{p(4.6)},{p(4.8)}{{offset-distance:100%;opacity:1}}{p(5.0)},100%{{offset-distance:100%;opacity:0}}')
kf('rl0', f'0%,{p(3.0)}{{transform:rotate(0)}}{p(4.6)},100%{{transform:rotate(-400deg)}}')
BALL = ('<div class="halo"></div><div class="sph"><div class="rl" style="animation-name:{rl}"><div style="position:absolute;left:13px;top:13px;width:52px;height:52px;border-radius:50%;border:1px solid rgba(250,228,200,.65)"></div>'
        '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:\'Cormorant Garamond\',serif;font-size:21px;color:#F5DEC4" dir="ltr">BW</div>'
        '<div style="position:absolute;left:12px;top:46px;width:14px;height:14px;border-radius:50%;background:#FFF7EC;box-shadow:0 0 12px 4px rgba(255,240,215,.8)"></div></div></div>')
RULE_D = 'M1140 1180 C 860 1180 760 1000 540 1000'
rule = f"""
<div class="stack" style="animation-name:rule;background:{CREAM}">
  <div style="position:absolute;top:560px;left:80px;right:80px;text-align:center" dir="rtl">
    <span class="mask"><span style="display:block;animation-name:r1;{H};font-size:96px;font-weight:300;line-height:1.15;color:{INK}">קודם ההבטחה.</span></span>
    <span class="mask"><span style="display:block;animation-name:r2;{H};font-size:96px;font-weight:600;line-height:1.15;color:{COPPER}">אחר כך האפקט.</span></span>
  </div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920"><path class="line" style="animation-name:ln0" pathLength="1" d="{RULE_D}"/></svg>
  <div class="ball" style="animation-name:bl0;offset-path:path('{RULE_D}')">{BALL.format(rl='rl0')}</div>
  <div style="position:absolute;top:1360px;left:80px;right:80px;text-align:center;{H};font-size:38px;line-height:1.5;color:{INK}" dir="rtl">
    ארבעה אפקטים מהרשת. ארבעה עולמות.<br>ככה כל אחד <b style="font-weight:600">תורגם</b>.</div>
</div>"""

# ── the four translations ───────────────────────────────────────────────────────
scenes = ''
for i, sc in enumerate(S):
    t, k = sc['t'], sc['k']
    cw = 1000; chh = round(cw * sc['h'] / sc['w']); top = 760 if chh < 900 else 700
    cap_top = top + chh + 44
    a, b = t, t + LEN
    kf(f'sc{k}', f'0%,{p(a-.25)}{{opacity:0}}{p(a)},{p(b-.05)}{{opacity:1}}{p(b+.25)},100%{{opacity:0}}')
    # the trend comes in big, gets crossed out, then stays as a small 'before' stamp at the top right
    kf(f'tr{k}', f'0%,{p(a+.1)}{{opacity:0;transform:translateY(30px)}}{p(a+.5)},{p(a+1.5)}{{opacity:1;transform:none}}{p(a+2.2)},100%{{opacity:.9;transform:translate(290px,-40px) scale(.55)}}')
    kf(f'st{k}', f'0%,{p(a+1.05)}{{transform:scaleX(0)}}{p(a+1.35)},100%{{transform:scaleX(1)}}')
    kf(f'pr{k}', f'0%,{p(a+.7)}{{transform:translateY(110%)}}{p(a+1.2)},100%{{transform:none}}')
    kf(f'ph{k}', f'0%,{p(a+.95)}{{opacity:0}}{p(a+1.4)},100%{{opacity:1}}')
    kf(f'pt{k}', f'0%,{p(a+1.8)}{{clip-path:circle(0px at 50% 50%)}}{p(a+2.6)},100%{{clip-path:circle(120% at 50% 50%)}}')
    kf(f'rg{k}', f'0%,{p(a+1.8)}{{transform:scale(0);opacity:0}}{p(a+1.85)}{{opacity:1}}{p(a+2.6)}{{transform:scale(1);opacity:1}}{p(a+2.9)},100%{{transform:scale(1.05);opacity:0}}')
    kf(f'c1{k}', f'0%,{p(a+2.3)}{{transform:translateY(110%)}}{p(a+2.8)},100%{{transform:none}}')
    kf(f'c2{k}', f'0%,{p(a+2.6)}{{transform:translateY(110%)}}{p(a+3.1)},100%{{transform:none}}')
    D2 = f'M540 640 C 540 680 540 {top - 40} 540 {top + chh // 2}'
    kf(f'ln{k}', f'0%,{p(a+1.2)}{{stroke-dashoffset:1}}{p(a+1.85)},100%{{stroke-dashoffset:0}}')
    kf(f'bl{k}', f'0%,{p(a+1.15)}{{offset-distance:0%;opacity:0}}{p(a+1.2)}{{offset-distance:0%;opacity:1}}{p(a+1.85)}{{offset-distance:100%;opacity:1;transform:scale(1)}}{p(a+2.2)},100%{{offset-distance:100%;opacity:0;transform:scale(1.5)}}')
    kf(f'rl{k}', f'0%,{p(a+1.2)}{{transform:rotate(0)}}{p(a+1.85)},100%{{transform:rotate(-300deg)}}')
    step = 3.0 / sc['n']
    scenes += f"""
<div class="stack" style="animation-name:sc{k};background:{sc['bg']}">
  <div style="position:absolute;top:70px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:baseline" dir="rtl">
    <span style="{H};font-size:34px;font-weight:500;color:{INK}">{sc['name']}</span>
    <span style="{CG};font-size:34px;color:{COPPER}" dir="ltr">0{i+1} / 04</span>
  </div>
  <div style="position:absolute;top:150px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:14px;animation-name:tr{k}">
    <div style="position:relative;padding:6px 22px;border-radius:999px;background:#1B1B1F;color:#fff;{H};font-size:26px" dir="rtl">הטרנד: {sc['trend']}
      <span style="position:absolute;left:10px;right:10px;top:50%;height:4px;background:{COPPER};transform-origin:right;animation-name:st{k}"></span></div>
    <div style="transform:scale({1 if sc['mini']=='glitch' else 1.3});transform-origin:50% 0">{MINI[sc['mini']]()}</div>
  </div>
  <div style="position:absolute;top:470px;left:60px;right:60px;text-align:center">
    <span class="mask"><span style="display:block;animation-name:pr{k};{CG};font-style:italic;font-size:64px;line-height:1.1;color:{DARK}" dir="ltr">{sc['prom']}</span></span>
    <div style="animation-name:ph{k};margin-top:10px;{H};font-size:32px;color:{INK}" dir="rtl"><span style="color:{COPPER}">נגזר מ־</span>{sc['prom_he']}</div>
  </div>
  <div style="position:absolute;left:40px;top:{top}px;width:{cw}px;height:{chh}px;border-radius:24px;overflow:hidden;box-shadow:0 40px 90px rgba(40,26,18,.28);animation-name:pt{k}">
    <div class="stack" data-seq="seq/{k}_%03d.jpg" data-from="1" data-to="{sc['n']}" data-start="{a+1.9:.2f}" data-step="{step:.4f}" data-fit="cover"></div>
  </div>
  <div style="position:absolute;left:{540 - 60}px;top:{top + chh // 2 - 60}px;width:120px;height:120px;border-radius:50%;border:3px solid {COPPER};animation-name:rg{k}"></div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920"><path class="line" style="animation-name:ln{k}" pathLength="1" d="{D2}"/></svg>
  <div class="ball" style="animation-name:bl{k};offset-path:path('{D2}')">{BALL.format(rl='rl'+k)}</div>
  <div style="position:absolute;top:{cap_top}px;left:70px;right:70px;text-align:center" dir="rtl">
    <span class="mask"><span style="display:block;animation-name:c1{k};{H};font-size:52px;font-weight:300;line-height:1.2;color:{INK}">{sc['tr'][0]}</span></span>
    <span class="mask"><span style="display:block;animation-name:c2{k};{H};font-size:52px;font-weight:600;line-height:1.2;color:{COPPER}">{sc['tr'][1]}</span></span>
  </div>
</div>"""

# ── ANSWER 24.6–27.4 · OUTRO 27.4–30 ───────────────────────────────────────────
kf('ans', f'0%,{p(24.5)}{{opacity:0}}{p(24.8)},{p(27.3)}{{opacity:1}}{p(27.6)},100%{{opacity:0}}')
for n, t0 in [('a1', 24.9), ('a2', 25.3), ('a3', 25.9), ('a4', 26.3)]:
    kf(n, f'0%,{p(t0)}{{transform:translateY(110%)}}{p(t0+.5)},100%{{transform:none}}')
kf('out', f'0%,{p(27.3)}{{opacity:0}}{p(27.6)},100%{{opacity:1}}')
for n, t0 in [('o1', 27.6), ('o2', 27.9), ('o3', 28.4)]:
    kf(n, f'0%,{p(t0)}{{opacity:0;transform:translateY(30px)}}{p(t0+.5)},100%{{opacity:1;transform:none}}')
strip = ''.join(f'<img src="seq/{s["k"]}_{s["n"]:03d}.jpg" alt="" style="width:240px;height:240px;object-fit:cover;border-radius:16px;box-shadow:0 16px 30px rgba(40,26,18,.2)">' for s in S)
end = f"""
<div class="stack" style="animation-name:ans;background:{CREAM}">
  <div style="position:absolute;top:300px;left:30px;right:30px;display:flex;justify-content:center;gap:16px">{strip}</div>
  <div style="position:absolute;top:720px;left:70px;right:70px;text-align:center" dir="rtl">
    <span class="mask"><span style="display:block;animation-name:a1;{H};font-size:66px;font-weight:300;line-height:1.2;color:{INK}">אפקט שלא נגזר מההבטחה</span></span>
    <span class="mask"><span style="display:block;animation-name:a2;{H};font-size:66px;font-weight:600;line-height:1.2;color:{INK}">הוא קישוט.</span></span>
    <div style="height:46px"></div>
    <span class="mask"><span style="display:block;animation-name:a3;{H};font-size:66px;font-weight:300;line-height:1.2;color:{INK}">אפקט שנגזר ממנה</span></span>
    <span class="mask"><span style="display:block;animation-name:a4;{H};font-size:86px;font-weight:600;line-height:1.2;color:{COPPER}">הוא מותג.</span></span>
  </div>
</div>
<div class="stack" style="animation-name:out;background:{CREAM}">
  <div style="position:absolute;top:120px;left:0;right:0;text-align:center;{CG};font-style:italic;font-size:40px;color:{DARK}" dir="ltr">Brand Worlds Studio</div>
  <div style="position:absolute;top:470px;left:70px;right:70px;text-align:center;animation-name:o1" dir="rtl">
    <div style="{H};font-size:52px;font-weight:300;line-height:1.3;color:{INK}">לפני שאת שומרת עוד אפקט,</div>
    <div style="{H};font-size:84px;font-weight:600;line-height:1.2;color:{COPPER};margin-top:10px">מה ההבטחה שלך?</div>
  </div>
  <div style="position:absolute;top:1080px;left:0;right:0;display:flex;justify-content:center;animation-name:o2">
    <div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:26px 64px;background:{INK};color:{CREAM};border-radius:14px" dir="rtl">
      <span style="{H};font-size:42px;font-weight:500">אבחון פער המותג</span><span style="{H};font-size:26px;opacity:.85">30 דק׳ · בלי עלות</span></div>
  </div>
  <div style="position:absolute;top:1320px;left:0;right:0;text-align:center;animation-name:o3;font-family:'Plus Jakarta Sans',sans-serif;font-size:24px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
</div>"""

kf('prog', '0%{transform:scaleX(0)}100%{transform:scaleX(1)}')
tpl = open(os.path.join(os.path.dirname(__file__), 'reel-js.html')).read()
html = f"""<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>The Translation</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&amp;family=Heebo:wght@300;400;500;600&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">
<style>
html,body{{margin:0;background:{CREAM}}} body{{{H}}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
.stack{{position:absolute;inset:0}} .mask{{overflow:hidden;display:block}}
.bf{{animation-name:bf;animation-timing-function:linear}}
@keyframes bf{{0%{{opacity:0}}.01%{{opacity:1}}.36%{{opacity:1}}.37%,100%{{opacity:0}}}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1;stroke-dashoffset:1;animation-timing-function:linear}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg;animation-timing-function:linear}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}
.rl{{position:absolute;inset:0;animation-timing-function:linear}}
{chr(10).join(css)}
</style></head>
<body data-duration="30"><div id="stage"><div class="film stack">
{rule}{scenes}{end}{hook}
<div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18)"><div style="height:6px;background:{COPPER};transform-origin:right;animation-name:prog;animation-timing-function:linear"></div></div>
</div></div>
{tpl}
</body></html>"""
open(os.path.join(os.path.dirname(__file__), 'reel.html'), 'w').write(html)
print('reel.html written')
