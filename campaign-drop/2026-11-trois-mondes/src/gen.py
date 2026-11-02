# TROIS MONDES — one serum, three brand worlds (ROSÉE° 15 · ELVÉA° 14 · ORÉVA° 24).
# Campaign film, 9:16, 30s. Hook → merge → three worlds through copper portals → "La Prisme" → triptych → outro.
# python3 gen.py  →  reel.html (next to ./a/ assets). Render: node <skill>/scripts/render.js reel.html 30 out.mp4
import os
HERE = os.path.dirname(os.path.abspath(__file__))
D = 30


def p(t):
    return '%.3f%%' % (max(0, min(D, t)) / D * 100)


CSS = []


def kf(cls, stops, tf=None, origin=None):
    """stops: [(t, 'decl'), ...] in seconds; the first value holds from 0, the last holds to the end."""
    name = 'k_' + cls.replace('-', '_')
    out = '0%%,%s{%s}' % (p(stops[0][0]), stops[0][1])
    for t, d in stops[1:-1]:
        out += '%s{%s}' % (p(t), d)
    out += '%s,100%%{%s}' % (p(stops[-1][0]), stops[-1][1])
    extra = ''
    if tf:
        extra += 'animation-timing-function:%s;' % tf
    if origin:
        extra += 'transform-origin:%s;' % origin
    CSS.append('.%s{animation-name:%s;%s}@keyframes %s{%s}' % (cls, name, extra, name, out))


def fade_in(cls, t, dur=.5, dy=30):
    kf(cls, [(t, 'opacity:0;transform:translateY(%dpx)' % dy), (t + dur, 'opacity:1;transform:none')])


def window(cls, a, b, f=.3):
    kf(cls, [(a - f, 'opacity:0'), (a, 'opacity:1'), (b, 'opacity:1'), (b + f, 'opacity:0')])


def portal(cls, t, cx, cy, dur=.9):
    kf(cls, [(t, 'clip-path:circle(0px at %dpx %dpx)' % (cx, cy)), (t + dur, 'clip-path:circle(2300px at %dpx %dpx)' % (cx, cy))],
       tf='cubic-bezier(.55,0,.25,1)')
    kf(cls + '-ring', [(t, 'r:40px;opacity:0'), (t + .05, 'r:40px;opacity:1'), (t + dur, 'r:1500px;opacity:.9'), (t + dur + .3, 'r:1700px;opacity:0')],
       tf='cubic-bezier(.55,0,.25,1)')


def ring_svg(cls, cx, cy):
    return ('<svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">'
            '<circle class="%s-ring" cx="%d" cy="%d" r="40" fill="none" stroke="#C4765A" stroke-width="6"></circle></svg>' % (cls, cx, cy))


# ── palette ──
S_BG, S_CREAM, S_INK, S_COP, S_DARK = '#FAF8F3', '#EEE6D8', '#6B563F', '#C4765A', '#3E2F25'
R = dict(bg='#F7F0E6', ink='#3B2E33', soft='#6E5A61', rose='#E8B4B8', deep='#C9878E')
E = dict(bg='#F0EADD', ink='#2E3526', soft='#5D6550', olive='#55613F', deep='#3E4930', sage='#DFE3CE', nectar='#E9DABC')
O = dict(bg='#F6EFE7', ink='#3A2E29', cop='#B87A57', deep='#8F5A3C', blush='#EFCDBF', light='#D9A88A')
CG = "font-family:'Cormorant Garamond',serif"
AS = "font-family:'Assistant',sans-serif"
FR = "font-family:'Frank Ruhl Libre',serif"
HB = "font-family:'Heebo',sans-serif"

# ════════ HOOK 0–4.2 ════════
Q_OUT, Q_IN = 2.5, 2.8
kf('hq1', [(Q_OUT, 'opacity:1;transform:none'), (Q_OUT + .4, 'opacity:0;transform:translateY(-60px)')])
kf('hq2', [(Q_IN, 'opacity:0;transform:translateY(50px)'), (Q_IN + .5, 'opacity:1;transform:none')])
kf('htag', [(2.5, 'opacity:1'), (2.8, 'opacity:0')])
kf('cardL', [(2.7, 'opacity:1;transform:none'), (3.4, 'opacity:0;transform:translateX(330px) scale(.85)')])
kf('cardR', [(2.7, 'opacity:1;transform:none'), (3.4, 'opacity:0;transform:translateX(-330px) scale(.85)')])
kf('cardC', [(3.0, 'transform:none'), (3.7, 'transform:scale(1.14)')], origin='50% 40%')
LINE = 'M1040 1480 H800 C640 1480 540 1300 540 1004'
kf('hline', [(.1, 'stroke-dashoffset:1'), (2.4, 'stroke-dashoffset:.5'), (3.3, 'stroke-dashoffset:.5'), (4.2, 'stroke-dashoffset:0')], tf='linear')
kf('hball', [(0, 'offset-distance:0%;opacity:1'), (2.4, 'offset-distance:50%;opacity:1'), (3.3, 'offset-distance:50%;opacity:1'),
             (4.2, 'offset-distance:100%;opacity:1'), (4.6, 'offset-distance:100%;opacity:0')], tf='linear')
kf('hroll', [(0, 'transform:rotate(0deg)'), (2.4, 'transform:rotate(-260deg)'), (3.3, 'transform:rotate(-260deg)'), (4.2, 'transform:rotate(-520deg)')], tf='linear')
kf('hbs', [(4.2, 'transform:scale(1)'), (4.6, 'transform:scale(1.6)')])

card = lambda cls, left: f'''
  <div class="{cls}" style="position:absolute;top:770px;left:{left}px;width:300px;box-sizing:border-box;padding:14px;background:#FFFFFF;border-radius:18px;box-shadow:0 22px 50px rgba(62,47,37,.13);display:flex;flex-direction:column;gap:12px" dir="rtl">
    <img src="a/generic-serum.jpg" alt="" style="width:100%;height:440px;object-fit:cover;border-radius:10px;display:block">
    <div style="display:flex;justify-content:space-between;align-items:baseline;padding:0 4px"><span style="font-size:23px;color:#6E6660">סרום פנים · 30ml</span><strong style="font-size:32px;color:#2E2A27">₪189</strong></div>
  </div>'''

HOOK = f'''
<div class="stack" style="background:{S_CREAM}">
  <div style="position:absolute;top:88px;right:80px;display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    <div style="{CG};font-style:italic;font-size:36px;color:{S_DARK}" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size:17px;letter-spacing:.3em;color:#8B7B6E">חגית אנטבי</div>
  </div>
  <div class="hq1" style="position:absolute;top:270px;left:70px;right:70px;text-align:right;font-size:88px;font-weight:600;line-height:1.14;color:{S_DARK}" dir="rtl">שלושה סרומים.<br>אותו מחיר.<br>למה בוחרים <span style="color:{S_COP}">רק אחד</span>?</div>
  <div class="hq2" style="position:absolute;top:330px;left:70px;right:70px;text-align:right;font-size:100px;font-weight:600;line-height:1.14;color:{S_DARK}" dir="rtl">אותו סרום.<br>שלושה <span style="color:{S_COP}">עולמות</span>.</div>
  <div class="htag" style="position:absolute;top:680px;left:0;right:0;margin:0 auto;width:max-content;padding:10px 26px;border-radius:999px;background:#2E2A27;color:#F4F2EF;font-size:26px" dir="rtl">ככה משווים</div>
  {card('cardL', 60)}{card('cardR', 720)}{card('cardC', 390)}
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line hline" pathLength="1" d="{LINE}"></path></svg>
  <div class="ball hball" style="offset-path:path('{LINE}')"><div class="hbs" style="position:absolute;inset:0"><div class="halo"></div><div class="sph"><div class="hroll" style="position:absolute;inset:0"><div style="position:absolute;left:13px;top:13px;width:52px;height:52px;border-radius:50%;border:1px solid rgba(250,228,200,.65)"></div><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{CG};font-size:21px;color:#F5DEC4" dir="ltr">BW</div><div style="position:absolute;left:12px;top:46px;width:14px;height:14px;border-radius:50%;background:#FFF7EC;box-shadow:0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div></div>
</div>'''

# ════════ WORLD 1 · ROSÉE° 4.2–10 ════════
portal('w1', 4.2, 540, 1004)
fade_in('r-t1', 5.3); fade_in('r-t2', 5.6)
kf('r-a', [(7.3, 'opacity:0'), (7.8, 'opacity:1')])
kf('r-sky', [(7.6, f'background-color:#E3AEB2'), (8.6, 'background-color:#F0CFCB'), (9.6, 'background-color:#F7EBE3')])
kf('r-arch', [(7.5, 'transform:translateY(70px) scale(.94)'), (8.3, 'transform:none')])
kf('r-sun', [(7.7, 'offset-distance:0%'), (9.7, 'offset-distance:100%')], tf='cubic-bezier(.45,0,.4,1)')
kf('r-arc', [(7.7, 'stroke-dashoffset:1'), (9.7, 'stroke-dashoffset:0')], tf='cubic-bezier(.45,0,.4,1)')
window('r-h1', 7.7, 8.4, .15); window('r-h2', 8.55, 9.2, .15); kf('r-h3', [(9.2, 'opacity:0'), (9.35, 'opacity:1')])
fade_in('r-p1', 8.0); fade_in('r-p2', 8.6)
ARC = 'M210 800 A330 330 0 0 1 870 800'
W1 = f'''
<section class="w1 stack" style="background:{R['bg']}">
  <div class="stack" data-seq="a/rosee/f_%03d.webp" data-from="1" data-to="79" data-by="2" data-start="5.0" data-step="0.06" data-pos="50% 50%"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient({R['bg']} 35%,rgba(247,240,230,0))"></div>
  <div class="r-t1" style="position:absolute;top:190px;left:0;right:0;text-align:center;{CG};font-style:italic;font-weight:400;font-size:170px;line-height:1;color:{R['ink']}" dir="ltr">ROSÉE°</div>
  <div class="r-t2" style="position:absolute;top:390px;left:0;right:0;text-align:center;{AS};font-weight:300;font-size:52px;color:{R['soft']}" dir="rtl">נולד עם שחר</div>
  <div class="r-a stack">
    <div class="r-sky stack"></div>
    <div style="position:absolute;top:150px;left:0;right:0;text-align:center;{CG};font-style:italic;font-size:64px;color:{R['ink']}" dir="ltr">ROSÉE°</div>
    <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
      <path d="{ARC}" fill="none" stroke="rgba(59,46,51,.18)" stroke-width="2"></path>
      <path class="r-arc" d="{ARC}" pathLength="1" fill="none" stroke="{R['deep']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 1"></path>
    </svg>
    <div class="r-sun" style="position:absolute;left:0;top:0;width:44px;height:44px;border-radius:50%;offset-path:path('{ARC}');offset-rotate:0deg;background:radial-gradient(circle at 40% 35%,#FFF4E6,#F1B98F 60%,#D98C6E);box-shadow:0 0 30px 10px rgba(255,214,180,.7)"></div>
    <div class="r-arch" style="position:absolute;left:300px;top:560px;width:480px;height:680px;border-radius:240px 240px 24px 24px;overflow:hidden;box-shadow:0 40px 90px rgba(59,46,51,.22)">
      <img src="a/reveil.webp" alt="" class="cover" style="object-position:50% 60%;transform:scale(1.25);transform-origin:50% 62%">
    </div>
    <div style="position:absolute;top:1290px;left:0;right:0;height:110px;{CG};font-size:104px;line-height:1;color:{R['ink']}" dir="ltr">
      <div class="r-h1" style="position:absolute;inset:0;text-align:center">05:42</div>
      <div class="r-h2" style="position:absolute;inset:0;text-align:center">06:00</div>
      <div class="r-h3" style="position:absolute;inset:0;text-align:center">06:14</div>
    </div>
    <div class="r-p1" style="position:absolute;top:1440px;left:0;right:0;text-align:center;{AS};font-weight:400;font-size:56px;color:{R['ink']}" dir="rtl">טיפה אחת, כל בוקר.</div>
    <div class="r-p2" style="position:absolute;top:1530px;left:0;right:0;text-align:center;{AS};font-weight:300;font-size:36px;color:{R['soft']}" dir="rtl">הבוקר הוא מעגל.</div>
  </div>
</section>{ring_svg('w1', 540, 1004)}'''

# ════════ WORLD 2 · ELVÉA° 9.7–15 ════════
portal('w2', 9.7, 540, 1060)
fade_in('e-t1', 10.3); fade_in('e-t2', 10.6)
kf('e-ta', [(12.5, 'opacity:1;transform:none'), (12.9, 'opacity:0;transform:translateY(-40px)')])
fade_in('e-b1', 12.9); fade_in('e-b2', 13.3)
L1 = 'M-40 1560 C220 1480 300 1100 540 1060'
L2 = 'M1120 1330 C900 1300 760 1040 540 1060'
kf('e-l1', [(12.5, 'stroke-dashoffset:1'), (13.7, 'stroke-dashoffset:0')], tf='cubic-bezier(.5,0,.3,1)')
kf('e-l2', [(12.7, 'stroke-dashoffset:1'), (13.7, 'stroke-dashoffset:0')], tf='cubic-bezier(.5,0,.3,1)')
kf('e-glow', [(13.6, 'opacity:0;transform:scale(.3)'), (14.0, 'opacity:1;transform:scale(1)'), (14.8, 'opacity:.85;transform:scale(1.15)')])
W2 = f'''
<section class="w2 stack" style="background:{E['bg']}">
  <div style="position:absolute;left:0;right:0;top:288px;height:1632px" data-seq="a/elvea/f_%03d.webp" data-from="1" data-to="79" data-by="2" data-start="10.0" data-step="0.06" data-pos="77% 50%"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient({E['bg']} 62%,rgba(240,234,221,0))"></div>
  <div class="e-ta stack">
    <div class="e-t1" style="position:absolute;top:150px;left:0;right:0;text-align:center;{CG};font-weight:500;font-size:132px;letter-spacing:.12em;line-height:1;color:{E['deep']}" dir="ltr">ELVÉA°</div>
    <div class="e-t2" style="position:absolute;top:320px;left:0;right:0;text-align:center;{AS};font-weight:300;font-size:50px;color:{E['soft']}" dir="rtl">שני קווים. נקודת מפגש אחת.</div>
  </div>
  <div class="e-b1" style="position:absolute;top:150px;left:0;right:0;text-align:center;{AS};font-weight:400;font-size:60px;line-height:1.2;color:{E['deep']}" dir="rtl">הטבע מתחיל את הסיפור.</div>
  <div class="e-b2" style="position:absolute;top:240px;left:0;right:0;text-align:center;{AS};font-weight:300;font-size:60px;line-height:1.2;color:{E['olive']}" dir="rtl">הפורמולה משלימה אותו.</div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <path class="e-l1" d="{L1}" pathLength="1" fill="none" stroke="{E['olive']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 1"></path>
    <path class="e-l2" d="{L2}" pathLength="1" fill="none" stroke="{E['olive']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 1"></path>
  </svg>
  <div class="e-glow" style="position:absolute;left:470px;top:990px;width:140px;height:140px;border-radius:50%;background:radial-gradient(circle,rgba(255,250,232,.95) 0%,rgba(233,218,188,.55) 40%,rgba(233,218,188,0) 70%)"></div>
</section>{ring_svg('w2', 540, 1060)}'''

# ════════ WORLD 3 · ORÉVA° 14.7–20 ════════
portal('w3', 14.7, 540, 960)
kf('o-pan', [(15.4, 'transform:translateX(-300px)'), (17.2, 'transform:translateX(-1040px)')], tf='cubic-bezier(.5,0,.3,1)')
fade_in('o-t1', 15.3); fade_in('o-t2', 15.6); fade_in('o-t3', 16.7)
kf('o-b', [(17.4, 'opacity:0'), (17.8, 'opacity:1')])
kf('o-bottle', [(17.6, 'opacity:0;transform:translateY(160px)'), (18.5, 'opacity:1;transform:none')], tf='cubic-bezier(.2,.7,.2,1)')
kf('o-rib', [(17.7, 'stroke-dashoffset:1'), (19.0, 'stroke-dashoffset:0')], tf='cubic-bezier(.5,0,.3,1)')
fade_in('o-p0', 18.0); fade_in('o-p1', 18.3); fade_in('o-p2', 18.7)
RIB = 'M-60 1500 C200 1700 420 1180 560 1260 C720 1350 860 1080 1140 1120'
W3 = f'''
<section class="w3 stack" style="background:{O['bg']}">
  <div class="o-pan" style="position:absolute;left:0;top:0;width:3413px;height:1920px"><img src="a/founder-cream-on-hand.webp" alt="" style="width:100%;height:100%;display:block"></div>
  <div style="position:absolute;left:0;right:0;top:0;height:620px;background:linear-gradient(rgba(246,239,231,.96) 30%,rgba(246,239,231,0))"></div>
  <div class="o-t1" style="position:absolute;top:150px;left:0;right:0;text-align:center;{CG};font-weight:400;font-size:104px;letter-spacing:.22em;line-height:1;color:{O['ink']}" dir="ltr">ORÉVA°</div>
  <div class="o-t2" style="position:absolute;top:290px;right:110px;{FR};font-weight:500;font-size:76px;color:{O['ink']}" dir="rtl">קודם הידיים.</div>
  <div class="o-t3" style="position:absolute;top:390px;left:110px;{FR};font-weight:500;font-size:76px;color:{O['deep']}" dir="rtl">אחר כך הבקבוק.</div>
  <div class="o-b stack" style="background:radial-gradient(ellipse at 50% 58%,#FBF3EC 0%,{O['blush']} 62%,#E2B6A2 100%)">
    <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="o-rib" d="{RIB}" pathLength="1" fill="none" stroke="{O['cop']}" stroke-width="14" stroke-linecap="round" stroke-dasharray="1 1" opacity=".75"></path></svg>
    <div style="position:absolute;left:340px;top:1530px;width:400px;height:60px;border-radius:50%;background:radial-gradient(rgba(143,90,60,.35),rgba(143,90,60,0) 70%)"></div>
    <div class="o-bottle" style="position:absolute;left:311px;top:540px;width:458px;height:1003px"><img src="a/p-glow.webp" alt="" style="width:100%;height:100%;display:block"></div>
    <div class="o-p0" style="position:absolute;top:150px;left:0;right:0;text-align:center;{CG};font-size:40px;letter-spacing:.3em;color:{O['cop']}" dir="ltr">ORÉVA° · SKIN STUDIO</div>
    <div class="o-p1" style="position:absolute;top:230px;left:0;right:0;text-align:center;{FR};font-weight:500;font-size:66px;line-height:1.25;color:{O['ink']}" dir="rtl">מה שקורה בחדר הטיפולים,</div>
    <div class="o-p2" style="position:absolute;top:320px;left:0;right:0;text-align:center;{FR};font-weight:500;font-size:66px;line-height:1.25;color:{O['deep']}" dir="rtl">קורה בבקבוק.</div>
  </div>
</section>{ring_svg('w3', 540, 960)}'''

# HUD over the three worlds
window('hud', 5.2, 19.7, .35)
HUD = f'''
<div class="hud-wrap hud stack" style="pointer-events:none">
  <div style="position:absolute;top:44px;right:44px;height:64px;padding:0 26px;box-sizing:border-box;background:rgba(250,248,243,.9);border:1px solid #D4C9BC;border-radius:999px;display:flex;align-items:center;gap:14px" dir="rtl">
    <span style="font-size:22px;font-weight:500;color:{S_COP}">עולם</span>
    <span style="position:relative;width:420px;height:40px;display:block">
      <span class="hu1" style="position:absolute;inset:0;display:flex;align-items:center;gap:12px;font-size:24px;color:{S_INK}"><b style="font-weight:600">1/3</b> · <span dir="ltr">ROSÉE°</span> · עולם מותג 15</span>
      <span class="hu2" style="position:absolute;inset:0;display:flex;align-items:center;gap:12px;font-size:24px;color:{S_INK}"><b style="font-weight:600">2/3</b> · <span dir="ltr">ELVÉA°</span> · עולם מותג 14</span>
      <span class="hu3" style="position:absolute;inset:0;display:flex;align-items:center;gap:12px;font-size:24px;color:{S_INK}"><b style="font-weight:600">3/3</b> · <span dir="ltr">ORÉVA°</span> · עולם מותג 24</span>
    </span>
  </div>
  <div style="position:absolute;bottom:64px;left:0;right:0;margin:0 auto;width:max-content;padding:16px 34px;background:rgba(250,248,243,.92);border:1px solid #D4C9BC;border-radius:999px;font-size:28px;color:{S_INK}" dir="rtl">אותו סרום · 30ml · <b style="color:{S_DARK}">₪189</b></div>
</div>'''
window('hu1', 5.2, 9.9, .2); window('hu2', 10.1, 14.9, .2); window('hu3', 15.1, 20, .2)

# ════════ LA PRISME 20–25.6 → triptych → outro ════════
FACES = [  # front order: ORÉVA → ROSÉE → ELVÉA
    dict(k='o', name='ORÉVA°', nst=f"{CG};font-size:66px;letter-spacing:.22em", panel=O['cop'], ink='#FBF1E8', sub='#F6DCCB',
         line='קודם הידיים. אחר כך הבקבוק.', lst=f"{FR};font-weight:500;font-size:34px",
         photo=f'<div class="stack" style="background:radial-gradient(ellipse at 50% 60%,#FBF3EC,{O["blush"]} 70%)"></div><img src="a/p-glow.webp" alt="" style="position:absolute;left:186px;top:40px;width:268px;height:587px">'),
    dict(k='r', name='ROSÉE°', nst=f"{CG};font-style:italic;font-size:84px", panel=R['ink'], ink='#F7E3E1', sub=R['rose'],
         line='טיפה אחת, כל בוקר.', lst=f"{AS};font-weight:300;font-size:38px",
         photo='<img src="a/reveil.webp" alt="" class="cover" style="object-position:50% 60%">'),
    dict(k='e', name='ELVÉA°', nst=f"{CG};font-weight:500;font-size:74px;letter-spacing:.12em", panel=E['deep'], ink=E['nectar'], sub=E['sage'],
         line='הטבע מתחיל. הפורמולה משלימה.', lst=f"{AS};font-weight:300;font-size:34px",
         photo='<img src="a/hero-5-bottle.webp" alt="" class="cover" style="object-position:83% 50%">'),
]


def face(f):
    return f'''<div style="position:absolute;inset:0;border-radius:6px;overflow:hidden;background:{f['panel']}">
      <div style="position:absolute;left:0;top:0;width:640px;height:700px;overflow:hidden">{f['photo']}</div>
      <div style="position:absolute;left:0;right:0;top:700px;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;text-align:center">
        <div style="{f['nst']};line-height:1;color:{f['ink']}" dir="ltr">{f['name']}</div>
        <div style="{f['lst']};color:{f['sub']}" dir="rtl">{f['line']}</div>
        <div style="{HB};font-size:24px;letter-spacing:.14em;color:{f['ink']};opacity:.75" dir="rtl">30ml · ₪189</div>
      </div></div>'''


FW, FH = 640, 1080
APO = round(FW / (2 * 3 ** .5))  # 185
STOPS = [(20.0, 0), (21.4, 0), (22.0, -120), (22.8, -120), (23.4, -240), (24.0, -240), (25.0, -960)]
kf('pr-ring', [(t, 'transform:rotateY(%ddeg)' % a) for t, a in STOPS])
kf('pr-in', [(20.0, 'transform:scale(1.3)'), (20.7, 'transform:scale(1)')])
kf('pr-fade', [(24.9, 'opacity:1'), (25.25, 'opacity:0')])
BGS = [(20.0, '#EED3C2'), (21.4, '#EED3C2'), (22.0, '#EAD3D2'), (22.8, '#EAD3D2'), (23.4, '#DCE1CB'), (24.0, '#DCE1CB'), (25.1, S_BG)]
kf('pr-bg', [(t, 'background-color:' + c) for t, c in BGS])
kf('pr-scene', [(19.8, 'opacity:0'), (20.15, 'opacity:1')])
window('pl0', 20.4, 21.5, .2); window('pl1', 21.9, 22.9, .2); window('pl2', 23.3, 24.1, .2)
kf('ph1', [(24.9, 'opacity:1;transform:none'), (25.2, 'opacity:0;transform:translateY(-40px)')])
kf('ph2', [(25.2, 'opacity:0;transform:translateY(40px)'), (25.7, 'opacity:1;transform:none')])
# triptych: three faces at half size, flying out from the centre
TX = [(40, 'e'), (380, 'r'), (720, 'o')]  # RTL reading: ORÉVA right, ROSÉE middle, ELVÉA left
for i, (x, k) in enumerate(TX):
    dx = 380 - x
    kf('tc' + k, [(25.0 + i * .05, f'opacity:0;transform:translateX({dx}px) scale(.7)'), (25.65 + i * .05, 'opacity:1;transform:none')],
       tf='cubic-bezier(.2,.8,.2,1)')
fade_in('ot1', 25.8, .5, 16)
fade_in('oq', 27.0); fade_in('octa', 27.5); fade_in('ourl', 27.9)

prism_faces = ''.join(
    f'<div style="position:absolute;left:{-FW // 2}px;top:{-FH // 2}px;width:{FW}px;height:{FH}px;backface-visibility:hidden;transform:rotateY({i * 120}deg) translateZ({APO}px)">{face(f)}</div>'
    for i, f in enumerate(FACES))
byk = {f['k']: f for f in FACES}
trip = ''.join(
    f'<div class="tc{k}" style="position:absolute;left:{x}px;top:0;width:320px;height:540px;box-shadow:0 26px 60px rgba(62,47,37,.2);border-radius:6px"><div style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;transform:scale(.5);transform-origin:0 0">{face(byk[k])}</div></div>'
    for x, k in TX)
labels = ['<span dir="ltr">ORÉVA°</span> · הידיים', '<span dir="ltr">ROSÉE°</span> · השחר', '<span dir="ltr">ELVÉA°</span> · המפגש']

PRISM = f'''
<section class="pr-scene stack">
  <div class="pr-bg stack"></div>
  <div class="ph1" style="position:absolute;top:150px;left:0;right:0;text-align:center;font-size:64px;font-weight:600;color:{S_DARK}" dir="rtl">אותו סרום. אותו מחיר.</div>
  <div class="pr-fade stack">
    <div style="position:absolute;left:540px;top:1000px;width:0;height:0;perspective:2400px;perspective-origin:0 0">
      <div class="pr-in" style="position:absolute;left:0;top:0;transform-style:preserve-3d">
        <div class="pr-ring" style="position:absolute;left:0;top:0;transform-style:preserve-3d">{prism_faces}</div>
      </div>
    </div>
    <div style="position:absolute;top:1640px;left:0;right:0;height:70px;font-size:44px;font-weight:500;color:{S_INK}" dir="rtl">
      {''.join(f'<div class="pl{i}" style="position:absolute;inset:0;text-align:center">{l}</div>' for i, l in enumerate(labels))}
    </div>
  </div>
  <div class="ot1" style="position:absolute;top:140px;left:0;right:0;text-align:center;font-size:24px;font-weight:500;letter-spacing:.06em;color:{S_COP}" dir="rtl">Brand Worlds Studio · עולמות מותג 15 · 14 · 24</div>
  <div class="ph2" style="position:absolute;top:220px;left:0;right:0;text-align:center;font-size:84px;font-weight:600;line-height:1.15;color:{S_DARK}" dir="rtl">אותו סרום.<br><span style="color:{S_COP}">שלושה עולמות.</span></div>
  <div style="position:absolute;left:0;top:560px;width:1080px;height:540px">{trip}</div>
  <div class="oq" style="position:absolute;top:1220px;left:70px;right:70px;text-align:center;font-size:58px;font-weight:600;line-height:1.25;color:{S_INK}" dir="rtl">ההבדל הוא לא בבקבוק.<br><span style="color:{S_COP}">ואת העסק שלך?</span></div>
  <div class="octa" style="position:absolute;top:1470px;left:0;right:0;margin:0 auto;width:max-content;display:flex;flex-direction:column;align-items:center;gap:4px;padding:24px 60px;background:{S_INK};color:{S_BG};border-radius:12px" dir="rtl"><span style="font-size:40px;font-weight:500">אבחון פער המותג</span><span style="font-size:24px;opacity:.8">30 דק׳ · בלי עלות</span></div>
  <div class="ourl" style="position:absolute;top:1690px;left:0;right:0;text-align:center;font-family:'Plus Jakarta Sans',sans-serif;font-size:24px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
</section>'''

kf('progress', [(0, 'transform:scaleX(0)'), (30, 'transform:scaleX(1)')], tf='linear', origin='right')

html = f'''<!doctype html>
<html lang="he">
<head>
<meta charset="utf-8">
<title>TROIS MONDES reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400;1,500&amp;family=Heebo:wght@300;400;500;600;700&amp;family=Assistant:wght@200;300;400;600&amp;family=Frank+Ruhl+Libre:wght@400;500&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">
<style>
html,body{{margin:0;background:{S_BG}}}
body{{{HB};color:{S_DARK}}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{S_BG}}}
.film *{{animation-duration:30s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.bf{{animation-name:bf;animation-timing-function:linear}}
@keyframes bf{{0%{{opacity:0}}.01%{{opacity:1}}.36%{{opacity:1}}.37%,100%{{opacity:0}}}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}
{chr(10).join(CSS)}
</style>
</head>
<body data-duration="30">
<div id="stage">
<div class="film stack">
{HOOK}
{W1}
{W2}
{W3}
{HUD}
{PRISM}
<div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18)"><div class="progress" style="height:6px;background:{S_COP}"></div></div>
</div>
</div>
<script>
(function(){{
  const D = 30, css = [];
  const P = t => (Math.max(0, Math.min(D, t)) / D * 100).toFixed(3) + '%';
  let n = 0;
  document.querySelectorAll('[data-seq]').forEach(el => {{
    const d = el.dataset, from = +d.from, to = +d.to, by = +(d.by || 1), start = +d.start, step = +d.step;
    const pad = (s, i) => s.replace(/%0(\\d)d/, (_, w) => String(i).padStart(+w, '0'));
    const style = `position:absolute;inset:0;width:100%;height:100%;object-fit:${{d.fit || 'cover'}};object-position:${{d.pos || '50% 50%'}};display:block`;
    const base = document.createElement('img'); base.src = pad(d.seq, from); base.alt = ''; base.style.cssText = style; el.appendChild(base);
    let i = 0, last = from;
    for (let f = from; f <= to; f += by, i++) {{
      const im = document.createElement('img'); im.src = pad(d.seq, f); im.alt = ''; im.className = 'bf';
      im.style.cssText = style + `;animation-delay:${{(start + i * step).toFixed(3)}}s`; el.appendChild(im); last = f;
    }}
    const hold = document.createElement('img'), k = 'hold' + (n++), th = start + i * step;
    hold.src = pad(d.seq, last); hold.alt = ''; hold.style.cssText = style + `;animation-name:${{k}};animation-timing-function:linear`;
    css.push(`@keyframes ${{k}}{{0%,${{P(th - .05)}}{{opacity:0}}${{P(th)}},100%{{opacity:1}}}}`); el.appendChild(hold);
  }});
  const s = document.createElement('style'); s.textContent = css.join('\\n'); document.head.appendChild(s);
}})();
</script>
</body>
</html>
'''
open(os.path.join(HERE, 'reel.html'), 'w').write(html)
print('wrote reel.html')
