# TROIS MONDES — one serum, three brand worlds (ROSÉE° 15 · ELVÉA° 14 · ORÉVA° 24).
# Campaign film, 9:16, 30s. Hook → ONE bottle dressed by each world (what it IS there + who chooses it, why) → La Prisme (same bottle, one word per face) → triptych → outro.
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

# ════════ THE BOTTLE — one shape for every world; only glass tint, rubber, collar and label change ════════
BX, BY = 360, 640           # bottle box on the stage (360×720); label centre on stage = (540, 1145)
_uid = [0]


def bottle_svg(glass, bulb, collar):
    _uid[0] += 1
    u = 'b%d' % _uid[0]
    return f'''<svg width="360" height="720" viewBox="0 0 360 720" style="position:absolute;left:0;top:0" aria-hidden="true"><defs>
<linearGradient id="{u}g" x1="0" x2="1"><stop offset="0" stop-color="{glass[0]}"/><stop offset=".45" stop-color="{glass[1]}"/><stop offset="1" stop-color="{glass[2]}"/></linearGradient>
<linearGradient id="{u}b" x1="0" x2="1"><stop offset="0" stop-color="{bulb[0]}"/><stop offset=".4" stop-color="{bulb[1]}"/><stop offset="1" stop-color="{bulb[2]}"/></linearGradient>
<linearGradient id="{u}c" x1="0" x2="1"><stop offset="0" stop-color="{collar[0]}"/><stop offset=".35" stop-color="{collar[1]}"/><stop offset=".7" stop-color="{collar[0]}"/><stop offset="1" stop-color="{collar[2]}"/></linearGradient></defs>
<path d="M142 150 V64 Q142 2 180 2 Q218 2 218 64 V150 Z" fill="url(#{u}b)"/>
<rect x="150" y="214" width="60" height="26" fill="{glass[2]}"/>
<path d="M40 334 Q40 238 140 238 H220 Q320 238 320 334 V680 Q320 716 284 716 H76 Q40 716 40 680 Z" fill="url(#{u}g)"/>
<rect x="118" y="140" width="124" height="82" rx="10" fill="url(#{u}c)"/>
<rect x="118" y="196" width="124" height="4" fill="rgba(0,0,0,.12)"/>
<rect x="64" y="300" width="22" height="380" rx="11" fill="rgba(255,255,255,.42)"/>
<rect x="292" y="320" width="12" height="360" rx="6" fill="rgba(0,0,0,.06)"/></svg>'''


def label_box(bg, inner, cls=''):
    return (f'<div class="{cls}" style="position:absolute;left:82px;top:380px;width:196px;height:250px;box-sizing:border-box;background:{bg};'
            f'border-radius:4px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;text-align:center;'
            f'box-shadow:inset 0 0 0 1px rgba(0,0,0,.04)">{inner}</div>')


LEAF = '<svg width="74" height="74" viewBox="0 0 100 100" aria-hidden="true"><path d="M18 86 C30 60 46 40 80 16 M34 64 C40 48 38 34 30 22 C46 30 50 46 44 60 M50 46 C62 44 74 48 84 58 C68 62 56 58 50 46" fill="none" stroke="#55613F" stroke-width="2.4" stroke-linecap="round"/></svg>'
DRESS = {
    'g': dict(glass=('#FFFFFF', '#F1F1EE', '#D6D6D1'), bulb=('#3A3A3A', '#1C1C1C', '#0E0E0E'), collar=('#2E2E2E', '#4A4A4A', '#161616'),
              label=label_box('#FFFFFF', '')),
    'r': dict(glass=('#FCE7E3', '#F2C6C3', '#D99A9F'), bulb=('#E7AEB2', '#D3949A', '#A96C74'), collar=('#B9774D', '#F0C39C', '#7E4A2C'),
              label=label_box('#FBF1EC', f'<div style="{CG};font-style:italic;font-size:46px;line-height:1;color:{R["ink"]}" dir="ltr">ROSÉE°</div>'
                              f'<div style="width:60px;height:1px;background:{R["deep"]}"></div>'
                              f'<div style="{CG};font-size:19px;letter-spacing:.24em;color:{R["soft"]}" dir="ltr">SÉRUM DE L’AUBE</div>'
                              f'<div style="{CG};font-size:22px;color:{R["deep"]}" dir="ltr">06:14</div>')),
    'e': dict(glass=('#FBF6EA', '#EDE2C8', '#CDBF9E'), bulb=('#66724F', '#4A5638', '#2F3824'), collar=('#4A5638', '#5E6A48', '#2F3824'),
              label=label_box('#F6F0E2', LEAF + f'<div style="{CG};font-weight:500;font-size:28px;letter-spacing:.16em;color:{E["deep"]}" dir="ltr">ELVÉA°</div>'
                              f'<div style="{CG};font-size:16px;letter-spacing:.2em;color:{E["soft"]}" dir="ltr">BOTANICAL SERUM</div>')),
    'o': dict(glass=('#FCEBE2', '#F1C7B4', '#D69C84'), bulb=('#C98A63', '#B87A57', '#7E4A2C'), collar=('#A86A43', '#EDB990', '#6E3F24'),
              label=label_box('#FBF3EC', f'<div style="{CG};font-size:31px;letter-spacing:.24em;color:{O["ink"]}" dir="ltr">ORÉVA</div>'
                              f'<div style="{CG};font-size:12px;letter-spacing:.3em;color:{O["cop"]}" dir="ltr">SKIN STUDIO</div>'
                              f'<div style="width:40px;height:1px;background:{O["cop"]};margin:6px 0"></div>'
                              f'<div style="{CG};font-size:30px;letter-spacing:.1em;color:{O["deep"]}" dir="ltr">GLOW</div>'
                              f'<div style="{CG};font-size:14px;letter-spacing:.2em;color:{O["ink"]}" dir="ltr">DAILY SERUM</div>')),
}


def bottle(k, dress_t=None, left=BX, top=BY, scale=1, rise=None):
    """The same bottle. With dress_t it starts generic and gets dressed in world k: glass/rubber fade, then the label wipes down."""
    g, d = DRESS['g'], DRESS[k]
    shadow = '<div style="position:absolute;left:40px;top:690px;width:280px;height:50px;border-radius:50%;background:radial-gradient(rgba(60,40,30,.28),rgba(60,40,30,0) 70%)"></div>'
    if dress_t is None:
        body = shadow + bottle_svg(d['glass'], d['bulb'], d['collar']) + d['label']
    else:
        c = 'dr-' + k
        kf(c + '-glass', [(dress_t, 'opacity:0'), (dress_t + .7, 'opacity:1')])
        kf(c + '-lab', [(dress_t + .45, 'clip-path:inset(0 0 100% 0)'), (dress_t + 1.05, 'clip-path:inset(0 0 0% 0)')], tf='cubic-bezier(.6,0,.3,1)')
        kf(c + '-flash', [(dress_t + .4, 'opacity:0;transform:translateY(-200px)'), (dress_t + .7, 'opacity:.9'), (dress_t + 1.1, 'opacity:0;transform:translateY(220px)')])
        body = (shadow + bottle_svg(g['glass'], g['bulb'], g['collar']) + g['label'] +
                f'<div class="{c}-glass" style="position:absolute;inset:0">' + bottle_svg(d['glass'], d['bulb'], d['collar']) + '</div>' +
                f'<div class="{c}-lab" style="position:absolute;inset:0">' + d['label'] + '</div>' +
                f'<div style="position:absolute;left:40px;top:238px;width:280px;height:478px;overflow:hidden;border-radius:60px 60px 36px 36px">'
                f'<div class="{c}-flash" style="position:absolute;left:0;right:0;top:200px;height:90px;background:linear-gradient(rgba(255,255,255,0),rgba(255,255,255,.75),rgba(255,255,255,0))"></div></div>')
    inner = f'<div style="position:absolute;left:0;top:0;width:360px;height:720px;transform:scale({scale});transform-origin:0 0">{body}</div>'
    cls = f' class="{rise}"' if rise else ''
    return f'<div{cls} style="position:absolute;left:{left}px;top:{top}px;width:{int(360 * scale)}px;height:{int(720 * scale)}px">{inner}</div>'


def say(prefix, t, eyebrow, l1, l2, proof, chooser, fx):
    """The fixed frame every world answers in: what the serum IS here (l1/l2) and who chooses it, and why."""
    fade_in(prefix + '-eb', t, .5, 16); fade_in(prefix + '-l1', t + .2); fade_in(prefix + '-l2', t + .45, .55, 40)
    fade_in(prefix + '-pf', t + 1.2); fade_in(prefix + '-ch', t + 1.7)
    return f'''
  <div class="{prefix}-eb" style="position:absolute;top:150px;left:0;right:0;text-align:center;{fx['eb']}" dir="ltr">{eyebrow}</div>
  <div class="{prefix}-l1" style="position:absolute;top:212px;left:0;right:0;text-align:center;{fx['l1']}" dir="rtl">{l1}</div>
  <div class="{prefix}-l2" style="position:absolute;top:296px;left:0;right:0;text-align:center;line-height:1.05;{fx['l2']}" dir="rtl">{l2}</div>
  <div class="{prefix}-pf" style="position:absolute;top:1400px;left:0;right:0;height:90px;text-align:center">{proof}</div>
  <div class="{prefix}-ch" style="position:absolute;top:1510px;left:110px;right:110px;text-align:center;line-height:1.3;{fx['ch']}" dir="rtl">{chooser}</div>'''


def nm(n):
    return f'<bdi dir="ltr" style="unicode-bidi:isolate">{n}</bdi>'


# ════════ WORLD 1 · ROSÉE° — "הבוקר שלה" (4.2–10.2) ════════
T1 = 4.2
portal('w1', T1, 540, 1004)
kf('r-sky', [(T1 + .9, 'background-color:#EBCFD3'), (T1 + 2.4, 'background-color:#F0C9C3'), (T1 + 3.9, 'background-color:#F8E7D9')])
kf('r-sun', [(T1 + 1.2, 'offset-distance:0%'), (T1 + 5.2, 'offset-distance:100%')], tf='cubic-bezier(.45,0,.4,1)')
kf('r-arc', [(T1 + 1.2, 'stroke-dashoffset:1'), (T1 + 5.2, 'stroke-dashoffset:0')], tf='cubic-bezier(.45,0,.4,1)')
window('r-h1', T1 + 1.2, T1 + 2.3, .12); window('r-h2', T1 + 2.45, T1 + 3.6, .12); kf('r-h3', [(T1 + 3.6, 'opacity:0'), (T1 + 3.72, 'opacity:1')])
ARC = 'M110 1000 A430 430 0 0 1 970 1000'
FX_R = dict(eb=f"{CG};font-style:italic;font-size:38px;color:{R['soft']}", l1=f"{AS};font-weight:400;font-size:60px;color:{R['ink']}",
            l2=f"{AS};font-weight:300;font-size:120px;color:{R['deep']}", ch=f"{AS};font-weight:400;font-size:42px;color:{R['ink']}")
W1 = f'''
<section class="w1 stack">
  <div class="r-sky stack"></div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <path d="{ARC}" fill="none" stroke="rgba(59,46,51,.16)" stroke-width="2"></path>
    <path class="r-arc" d="{ARC}" pathLength="1" fill="none" stroke="{R['deep']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 1"></path>
  </svg>
  <div class="r-sun" style="position:absolute;left:0;top:0;width:46px;height:46px;border-radius:50%;offset-path:path('{ARC}');offset-rotate:0deg;background:radial-gradient(circle at 40% 35%,#FFF4E6,#F1B98F 60%,#D98C6E);box-shadow:0 0 34px 12px rgba(255,214,180,.75)"></div>
  {bottle('r', T1 + .8)}
  {say('r', T1 + .9, 'ROSÉE° · née à l’aube', 'ב־' + nm('ROSÉE°') + ' הוא', 'הבוקר שלה.',
       f'<div style="position:relative;height:90px;{CG};font-size:84px;line-height:1;color:{R["ink"]}" dir="ltr"><div class="r-h1" style="position:absolute;inset:0">05:42</div><div class="r-h2" style="position:absolute;inset:0">06:00</div><div class="r-h3" style="position:absolute;inset:0">06:14</div></div>',
       'בוחרת בו מי שהבוקר הוא<br>הרגע היחיד שלה, לפני כולם.', FX_R)}
</section>{ring_svg('w1', 540, 1004)}'''

# ════════ WORLD 2 · ELVÉA° — "הוכחה" (9.9–15.4) ════════
T2 = 9.9
portal('w2', T2, 540, 1145)
L1 = 'M-40 560 C220 640 300 1080 540 1145'
L2 = 'M1120 760 C880 820 760 1110 540 1145'
kf('e-l1', [(T2 + 1.1, 'stroke-dashoffset:1'), (T2 + 2.3, 'stroke-dashoffset:0')], tf='cubic-bezier(.5,0,.3,1)')
kf('e-l2', [(T2 + 1.3, 'stroke-dashoffset:1'), (T2 + 2.3, 'stroke-dashoffset:0')], tf='cubic-bezier(.5,0,.3,1)')
kf('e-glow', [(T2 + 2.2, 'opacity:0;transform:scale(.3)'), (T2 + 2.6, 'opacity:1;transform:scale(1)'), (T2 + 3.4, 'opacity:.7;transform:scale(1.2)')])
FX_E = dict(eb=f"{CG};font-weight:500;font-size:34px;letter-spacing:.16em;color:{E['soft']}", l1=f"{AS};font-weight:400;font-size:60px;color:{E['ink']}",
            l2=f"{AS};font-weight:600;font-size:120px;color:{E['olive']}", ch=f"{AS};font-weight:400;font-size:42px;color:{E['ink']}")
W2 = f'''
<section class="w2 stack" style="background:radial-gradient(circle at 12% 18%,#C9D1B0 0,rgba(201,209,176,0) 48%),radial-gradient(circle at 92% 70%,#E3E5D0 0,rgba(227,229,208,0) 40%),{E['bg']}">
  {bottle('e', T2 + .6)}
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <path class="e-l1" d="{L1}" pathLength="1" fill="none" stroke="{E['olive']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 1"></path>
    <path class="e-l2" d="{L2}" pathLength="1" fill="none" stroke="{E['olive']}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 1"></path>
  </svg>
  <div class="e-glow" style="position:absolute;left:460px;top:1065px;width:160px;height:160px;border-radius:50%;background:radial-gradient(circle,rgba(255,250,232,.9) 0%,rgba(233,218,188,.45) 40%,rgba(233,218,188,0) 70%)"></div>
  {say('e', T2 + .7, 'ELVÉA° · BOTANICAL SKIN SCIENCE', 'ב־' + nm('ELVÉA°') + ' הוא', 'הוכחה.',
       f'<div style="{AS};font-weight:300;font-size:44px;line-height:90px;color:{E["olive"]}" dir="rtl">טבע ומדע. נקודת מפגש אחת.</div>',
       'בוחרת בו מי שרוצה טבע,<br>רק כשהמדע חתום עליו.', FX_E)}
</section>{ring_svg('w2', 540, 1145)}'''

# ════════ WORLD 3 · ORÉVA° — "הידיים שלה" (15.1–20.5) ════════
T3 = 15.1
portal('w3', T3, 540, 1145)
kf('o-pan', [(T3, 'transform:translateX(-200px) scale(1.06)'), (T3 + 1.6, 'transform:translateX(-330px) scale(1)')], tf='linear', origin='0 60%')
fade_in('o-first', T3 + .5)
kf('o-hands', [(T3 + 1.5, 'opacity:1'), (T3 + 1.9, 'opacity:0')])
kf('o-rise', [(T3 + 1.6, 'opacity:0;transform:translateY(140px)'), (T3 + 2.2, 'opacity:1;transform:none')], tf='cubic-bezier(.2,.7,.2,1)')
kf('o-rib', [(T3 + 1.8, 'stroke-dashoffset:1'), (T3 + 3.2, 'stroke-dashoffset:0')], tf='cubic-bezier(.5,0,.3,1)')
RIB = 'M-60 940 C200 1140 360 720 520 820 C700 930 840 660 1140 740'
FX_O = dict(eb=f"{CG};font-size:34px;letter-spacing:.3em;color:{O['cop']}", l1=f"{FR};font-weight:400;font-size:58px;color:{O['ink']}",
            l2=f"{FR};font-weight:500;font-size:112px;color:{O['deep']}", ch=f"{HB};font-weight:300;font-size:42px;color:{O['ink']}")
W3 = f'''
<section class="w3 stack" style="background:radial-gradient(ellipse at 50% 60%,#FBF3EC 0%,{O['blush']} 62%,#E2B6A2 100%)">
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="o-rib" d="{RIB}" pathLength="1" fill="none" stroke="{O['cop']}" stroke-width="12" stroke-linecap="round" stroke-dasharray="1 1" opacity=".7"></path></svg>
  {bottle('o', T3 + 2.3, rise='o-rise')}
  {say('o', T3 + 2.3, 'ORÉVA° · SKIN STUDIO', 'ב־' + nm('ORÉVA°') + ' הוא', 'הידיים שלה.',
       f'<div style="{FR};font-weight:400;font-size:44px;line-height:90px;color:{O["cop"]}" dir="rtl">קודם הידיים. אחר כך הבקבוק.</div>',
       'בוחרת בו מי שסומכת על הקוסמטיקאית שלה,<br>גם כשהיא בבית.', FX_O)}
  <div class="o-hands stack">
    <div class="o-pan" style="position:absolute;left:0;top:0;width:3413px;height:1920px"><img src="a/founder-cream-on-hand.webp" alt="" style="width:100%;height:100%;display:block"></div>
    <div style="position:absolute;left:0;right:0;top:0;height:560px;background:linear-gradient(rgba(246,239,231,.95) 35%,rgba(246,239,231,0))"></div>
    <div class="o-first" style="position:absolute;top:200px;left:0;right:0;text-align:center;{FR};font-weight:500;font-size:96px;color:{O['ink']}" dir="rtl">קודם הידיים.</div>
  </div>
</section>{ring_svg('w3', 540, 1145)}'''

# HUD over the three worlds
window('hud', 5.2, 20.0, .35)
HUD = f'''
<div class="hud stack">
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
window('hu1', 5.2, 9.9 + .6, .2); window('hu2', 10.7, 15.1 + .6, .2); window('hu3', 15.9, 20.3, .2)

# ════════ LA PRISME 20.3–25.6: the same bottle on every face, one word under it ════════
FACES = [  # front order: ORÉVA → ROSÉE → ELVÉA
    dict(k='o', word='הידיים', wst=f"{FR};font-weight:500;font-size:104px", name='ORÉVA°', nst=f"{CG};font-size:40px;letter-spacing:.24em",
         top=f"radial-gradient(ellipse at 50% 60%,#FBF3EC,{O['blush']} 75%)", panel=O['cop'], ink='#FBF1E8', sub='#F6DCCB'),
    dict(k='r', word='הבוקר', wst=f"{AS};font-weight:300;font-size:112px", name='ROSÉE°', nst=f"{CG};font-style:italic;font-size:48px",
         top='linear-gradient(#EBCFD3,#F8E7D9)', panel=R['ink'], ink='#F7E3E1', sub=R['rose']),
    dict(k='e', word='ההוכחה', wst=f"{AS};font-weight:600;font-size:100px", name='ELVÉA°', nst=f"{CG};font-weight:500;font-size:42px;letter-spacing:.16em",
         top=f"radial-gradient(circle at 15% 15%,#C9D1B0 0,rgba(201,209,176,0) 55%),{E['bg']}", panel=E['deep'], ink=E['nectar'], sub=E['sage']),
]


def face(f):
    return f'''<div style="position:absolute;inset:0;border-radius:6px;overflow:hidden;background:{f['panel']}">
      <div style="position:absolute;left:0;top:0;width:640px;height:720px;background:{f['top']}">{bottle(f['k'], None, left=185, top=60, scale=.75)}</div>
      <div style="position:absolute;left:0;right:0;top:720px;bottom:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;text-align:center">
        <div style="{f['wst']};line-height:1;color:{f['sub']}" dir="rtl">{f['word']}</div>
        <div style="{f['nst']};line-height:1;color:{f['ink']}" dir="ltr">{f['name']}</div>
        <div style="{HB};font-size:24px;letter-spacing:.14em;color:{f['ink']};opacity:.7" dir="rtl">30ml · ₪189</div>
      </div></div>'''


FW, FH = 640, 1080
APO = round(FW / (2 * 3 ** .5))
STOPS = [(20.3, 0), (21.5, 0), (22.1, -120), (22.9, -120), (23.5, -240), (24.1, -240), (25.0, -960)]
kf('pr-ring', [(t, 'transform:rotateY(%ddeg)' % a) for t, a in STOPS])
kf('pr-in', [(20.3, 'transform:scale(1.3)'), (21.0, 'transform:scale(1)')])
kf('pr-fade', [(24.9, 'opacity:1'), (25.25, 'opacity:0')])
BGS = [(20.3, '#EED3C2'), (21.5, '#EED3C2'), (22.1, '#EAD3D2'), (22.9, '#EAD3D2'), (23.5, '#DCE1CB'), (24.1, '#DCE1CB'), (25.1, S_BG)]
kf('pr-bg', [(t, 'background-color:' + c) for t, c in BGS])
kf('pr-scene', [(20.1, 'opacity:0'), (20.45, 'opacity:1')])
fade_in('pl', 24.0, .4, 20)
kf('ph1', [(24.9, 'opacity:1;transform:none'), (25.2, 'opacity:0;transform:translateY(-40px)')])
kf('ph2', [(25.2, 'opacity:0;transform:translateY(40px)'), (25.7, 'opacity:1;transform:none')])
TX = [(40, 'e'), (380, 'r'), (720, 'o')]
for i, (x, k) in enumerate(TX):
    kf('tc' + k, [(25.0 + i * .05, f'opacity:0;transform:translateX({380 - x}px) scale(.7)'), (25.65 + i * .05, 'opacity:1;transform:none')],
       tf='cubic-bezier(.2,.8,.2,1)')
fade_in('ot1', 25.8, .5, 16)
fade_in('oln', 26.5); fade_in('oq', 27.2); fade_in('octa', 27.7); fade_in('ourl', 28.0)

prism_faces = ''.join(
    f'<div style="position:absolute;left:{-FW // 2}px;top:{-FH // 2}px;width:{FW}px;height:{FH}px;backface-visibility:hidden;transform:rotateY({i * 120}deg) translateZ({APO}px)">{face(f)}</div>'
    for i, f in enumerate(FACES))
byk = {f['k']: f for f in FACES}
trip = ''.join(
    f'<div class="tc{k}" style="position:absolute;left:{x}px;top:0;width:320px;height:540px;box-shadow:0 26px 60px rgba(62,47,37,.2);border-radius:6px"><div style="position:absolute;left:0;top:0;width:{FW}px;height:{FH}px;transform:scale(.5);transform-origin:0 0">{face(byk[k])}</div></div>'
    for x, k in TX)

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
    <div class="pl" style="position:absolute;top:1650px;left:0;right:0;text-align:center;font-size:54px;font-weight:600;color:{S_COP}" dir="rtl">שלוש סיבות לבחור.</div>
  </div>
  <div class="ot1" style="position:absolute;top:140px;left:0;right:0;text-align:center;font-size:24px;font-weight:500;letter-spacing:.06em;color:{S_COP}" dir="rtl">Brand Worlds Studio · עולמות מותג 15 · 14 · 24</div>
  <div class="ph2" style="position:absolute;top:220px;left:0;right:0;text-align:center;font-size:84px;font-weight:600;line-height:1.15;color:{S_DARK}" dir="rtl">אותו סרום.<br><span style="color:{S_COP}">שלוש סיבות לבחור.</span></div>
  <div style="position:absolute;left:0;top:540px;width:1080px;height:540px">{trip}</div>
  <div class="oln" style="position:absolute;top:1150px;left:60px;right:60px;text-align:center;font-size:56px;font-weight:500;color:{S_INK}" dir="rtl">המוצר לא השתנה. המשמעות כן.</div>
  <div class="oq" style="position:absolute;top:1250px;left:60px;right:60px;text-align:center;font-size:60px;font-weight:600;color:{S_COP}" dir="rtl">מה הסיבה לבחור דווקא בך?</div>
  <div class="octa" style="position:absolute;top:1400px;left:0;right:0;margin:0 auto;width:max-content;display:flex;flex-direction:column;align-items:center;gap:4px;padding:24px 60px;background:{S_INK};color:{S_BG};border-radius:12px" dir="rtl"><span style="font-size:40px;font-weight:500">אבחון פער המותג</span><span style="font-size:24px;opacity:.8">30 דק׳ · בלי עלות</span></div>
  <div class="ourl" style="position:absolute;top:1610px;left:0;right:0;text-align:center;font-family:'Plus Jakarta Sans',sans-serif;font-size:24px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
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
