# ORÉVA° (World 24) — "how the identity is built": a narrated case-study reel (voice-over + burned captions).
# Run: python3 gen.py  → writes reel.html next to this file (assets in ./a/).
# Every timing lives in CAPS (caption cards, following the voice-over) and in the scene starts T_* below:
# re-time here when the recording arrives.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OFF = 0.25       # the recording starts this long after frame 0
D = 55.0

# scene starts (seconds on the reel) — measured from the pauses in the Cartesia recording (audio time + OFF)
T_INTRO = 4.2    # "אז כשיצרתי את אורווה, קונספט למותג טיפוח, התחלתי משאלה אחרת:"
T_Q = 10.0       # "מה גורם לנו להרגיש שיש מישהו אמיתי מאחורי המוצר?"
T_IDEA = 14.1    # "מכאן נולד הרעיון שהוביל את כל העולם הזה:"
T_TOUCHW = 17.35 # "כל מוצר מתחיל במגע אנושי."
T_LINE = 19.9    # "תרגמתי אותו לקו נחושת עדין, שמתחיל בתנועת היד וממשיך אל הבקבוק."
T_PAL = 25.5     # "שלושה גוונים, לרגעים השונים של העור."
T_LANG = 28.9    # "אבן טבעית, וטיפוגרפיה שקטה."  (the board holds through "כל פרט מזכיר את אותה הבטחה:")
PROM = [34.4, 36.3, 37.35]          # "טיפוח שמתחיל בהקשבה," · "במגע" · "ובתשומת לב."
T_PROM = PROM[0]
TOUCH = [38.7, 39.9, 41.5, 44.0]    # "מהבקבוק," · "דרך האריזה," · "ועד החלל שבו פוגשים את המותג:" · "אותו סיפור בכל נקודת מפגש."
T_TOUCH = TOUCH[0]
T_OUT = 46.4     # "כי כשיש למותג זהות ברורה,"
T_NOT = 49.1     # "לא משווים אותו לאחרים."
T_CHOOSE = 50.9  # "בוחרים בו."

# caption cards: (start, end, text)
CAPS = [
    (0.3, 3.95, 'סרום שמבטיח זוהר לעור.<br>יש אינספור כאלה.'),
    (4.35, 9.8, 'אז כשיצרתי את ORÉVA, קונספט למותג טיפוח,<br>התחלתי משאלה אחרת:'),
    (10.2, 13.8, 'מה גורם לנו להרגיש<br>שיש מישהו אמיתי מאחורי המוצר?'),
    (14.25, 19.7, 'מכאן נולד הרעיון שהוביל את כל העולם הזה:<br>כל מוצר מתחיל במגע אנושי.'),
    (20.0, 25.25, 'תרגמתי אותו לקו נחושת עדין,<br>שמתחיל בתנועת היד וממשיך אל הבקבוק.'),
    (25.65, 28.6, 'שלושה גוונים,<br>לרגעים השונים של העור.'),
    (29.0, 31.65, 'אבן טבעית,<br>וטיפוגרפיה שקטה.'),
    (32.05, 34.25, 'כל פרט מזכיר את אותה הבטחה:'),
    (34.45, 38.45, 'טיפוח שמתחיל בהקשבה,<br>במגע ובתשומת לב.'),
    (38.8, 43.8, 'מהבקבוק, דרך האריזה,<br>ועד החלל שבו פוגשים את המותג:'),
    (44.1, 46.25, 'אותו סיפור בכל נקודת מפגש.'),
]

def P(t): return '%.3f%%' % (max(0, min(D, t)) / D * 100)
css = []; uid = [0]
def kf(body):
    uid[0] += 1; n = 'k%d' % uid[0]; css.append('@keyframes %s{%s}' % (n, body)); return n

CREAM, STONE, BLUSH, COPPER, DEEP, INK = '#F6EFE7', '#D9C7B3', '#EFCDBF', '#B87A57', '#8F5A3C', '#3A2E29'
SERIF = "'Frank Ruhl Libre',serif"; LAT = "'Cormorant Garamond',serif"; SANS = "'Plus Jakarta Sans',sans-serif"
FPS12 = 0.0833

def seq(path, n, start, pos='50% 50%'):
    return f'<div class="stack" data-seq="a/{path}" data-from="1" data-to="{n}" data-by="1" data-start="{start:.2f}" data-step="{FPS12}" data-pos="{pos}"></div>'
def stagebar(stage):
    return f'<div style="position:absolute;top:54px;left:70px;right:70px;display:flex;justify-content:space-between;align-items:baseline;font-size:24px;font-weight:500;color:{COPPER}" dir="rtl"><span>{stage}</span><span style="font-family:{SANS};font-size:19px;letter-spacing:.24em" dir="ltr">BRAND WORLDS STUDIO · N°24</span></div>'
def title(stage, l1, l2, a, b, size=78):
    return f'''<div data-show="{a},{b}" style="position:absolute;top:0;left:0;right:0;height:310px">{stagebar(stage)}
  <div style="position:absolute;top:112px;left:70px;right:70px;text-align:right;font-family:{SERIF};font-weight:500;font-size:{size}px;line-height:1.14;color:{INK}" dir="rtl">{l1}<br><span style="color:{DEEP}">{l2}</span></div>
</div>'''
def zone(inner): return f'<div style="position:absolute;top:310px;left:0;width:1080px;height:1360px;overflow:hidden;background:{STONE}">{inner}</div>'

# ───────── HOOK · opens on the wow: the serum blooming, the question over it, the first colour chip already there ─────────
def chip0(name, hexv, t):
    an = '' if t <= 0 else 'animation-name:%s;' % kf('0%%,%s{opacity:0;transform:translateY(40px)}%s,100%%{opacity:1;transform:none}' % (P(t), P(t + .45)))
    return f'<div style="width:170px;{an}"><div style="height:160px;border-radius:22px;background:{hexv};border:3px solid rgba(255,255,255,.85);box-shadow:0 18px 40px rgba(143,90,60,.25)"></div><div style="margin-top:12px;display:flex;justify-content:space-between;align-items:baseline;font-family:{LAT};font-size:38px;color:{INK}" dir="ltr"><span>{name}</span><span style="font-family:{SANS};font-size:16px;letter-spacing:.1em;color:{DEEP}">{hexv}</span></div></div>'
PATH0 = 'M1140 1590 H540'
ln = kf('0%%,%s{stroke-dashoffset:1}%s,100%%{stroke-dashoffset:0}' % (P(.6), P(3.6)))
bl = kf('0%%,%s{offset-distance:0%%;opacity:0}%s{offset-distance:0%%;opacity:1}%s,100%%{offset-distance:100%%;opacity:1}' % (P(.5), P(.6), P(3.6)))
rl = kf('0%%,%s{transform:rotate(0deg)}%s,100%%{transform:rotate(-400deg)}' % (P(.6), P(3.6)))
hook = f'''<section class="scene" data-show="0,{T_INTRO}" style="background:{CREAM}">
  <div class="stack" data-seq="a/bloom/f%02d.webp" data-from="18" data-to="48" data-by="1" data-start="0.25" data-step="0.09" data-pos="66% 50%"></div>
  <div style="position:absolute;top:0;left:0;right:0;height:760px;background:linear-gradient(to bottom,rgba(246,239,231,.97) 0,rgba(246,239,231,.9) 55%,rgba(246,239,231,0))"></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:760px;background:linear-gradient(to top,rgba(246,239,231,.96) 0,rgba(246,239,231,.82) 50%,rgba(246,239,231,0))"></div>
  <div style="position:absolute;top:84px;right:70px;display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    <div style="font-family:{LAT};font-style:italic;font-size:36px;color:{INK}" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size:17px;letter-spacing:.3em;color:{DEEP}">חגית אנטבי</div>
  </div>
  <div style="position:absolute;top:226px;left:70px;right:70px;text-align:right;font-size:80px;font-weight:600;line-height:1.16;color:{INK}" dir="rtl">סרום כמו כל סרום.<br><span style="color:{DEEP}">איך הופכים אותו למותג?</span></div>
  <div style="position:absolute;top:1345px;left:70px;right:70px;display:flex;gap:30px;justify-content:flex-start" dir="rtl">{chip0('DEW', '#F1D3A6', 0)}{chip0('GLOW', '#F0BFB0', .7)}{chip0('CALM', '#D9B8C0', 1.3)}</div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path pathLength="1" d="{PATH0}" style="fill:none;stroke:{COPPER};stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1;animation-name:{ln};animation-timing-function:linear"></path></svg>
  <div style="position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg;offset-path:path('{PATH0}');animation-name:{bl};animation-timing-function:linear"><div style="position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)"></div><div style="position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)"><div style="position:absolute;inset:0;animation-name:{rl};animation-timing-function:linear"><div style="position:absolute;left:13px;top:13px;width:52px;height:52px;border-radius:50%;border:1px solid rgba(250,228,200,.65)"></div><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:{LAT};font-size:21px;color:#F5DEC4" dir="ltr">BW</div></div></div></div>
</section>'''

# ───────── the concept: the studio space, the name ─────────
push0 = kf('0%%,%s{transform:scale(1.14)}%s,100%%{transform:scale(1)}' % (P(T_INTRO - .4), P(T_Q + .3)))
intro = f'''<section class="scene" data-show="{T_INTRO},{T_Q}" style="background:{CREAM}">
  {zone(f'<img class="cover" src="a/studio-interior-reception.webp" alt="" style="object-position:50% 50%;animation-name:{push0};animation-timing-function:linear">')}
  {title('ORÉVA° · עולם מותג 24', 'קונספט למותג טיפוח.', 'התחלתי משאלה אחרת.', T_INTRO, T_Q)}
</section>'''

# ───────── 01 the question: her hands on a face ─────────
question = f'''<section class="scene" data-show="{T_Q},{T_IDEA}" style="background:{CREAM}">
  {zone(seq('treatq/q_%03d.webp', 60, T_Q - .35, '36% 50%'))}
  {title('01 · השאלה', 'מה גורם לנו להרגיש', 'שיש מישהו אמיתי מאחורי המוצר?', T_Q, T_IDEA, 66)}
</section>'''

# ───────── 02 the idea → 03 the line: the hands film, then it freezes and the ribbon is drawn from the finger to the pump ─────────
IW, IH = 2418, 1360   # the 16:9 film at the picture zone's height
def cam(s, cx, cy): return 'transform:translate(%.1fpx,%.1fpx) scale(%.3f)' % (540 - s * cx * IW, 680 - s * cy * IH, s)
pan = kf('0%%,%s{%s}%s{%s}%s,100%%{%s}' % (P(T_IDEA), cam(1.42, .30, .52), P(T_LINE - .2), cam(1.22, .325, .6), P(T_LINE + .9), cam(1.0, .365, .5)))
RIB = 'M372 540 C 420 600 500 640 540 580 C 580 520 520 450 560 420 C 580 406 596 410 600 422'
t0, t1 = T_LINE + .9, T_LINE + 4.6
draw = kf('0%%,%s{stroke-dashoffset:1}%s,100%%{stroke-dashoffset:0}' % (P(t0), P(t1)))
bead = kf('0%%,%s{opacity:0;transform:scale(.2)}%s{opacity:1;transform:scale(1.7)}%s,100%%{opacity:1;transform:scale(1)}' % (P(t1 - .1), P(t1 + .15), P(t1 + .45)))
dot0 = kf('0%%,%s{opacity:0}%s,100%%{opacity:1}' % (P(t0 - .3), P(t0)))
EASE = 'cubic-bezier(.4,0,.3,1)'
story = f'''<section class="scene" data-show="{T_IDEA},{T_PAL}" style="background:{CREAM}">
  {zone(f"""<div style="position:absolute;left:0;top:0;width:{IW}px;height:{IH}px;transform-origin:0 0;animation-name:{pan};animation-timing-function:cubic-bezier(.45,0,.2,1)">
      {seq('hands/h_%03d.webp', 81, T_IDEA - .35)}
      <svg viewBox="0 0 1280 720" style="position:absolute;inset:0;width:100%;height:100%;overflow:visible" aria-hidden="true">
        <defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E6B899"/><stop offset=".5" stop-color="#B87A57"/><stop offset="1" stop-color="#8F5A3C"/></linearGradient>
        <radialGradient id="bg" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#F6DCC9"/><stop offset=".55" stop-color="#B87A57"/><stop offset="1" stop-color="#6E4128"/></radialGradient></defs>
        <path pathLength="1" d="{RIB}" style="fill:none;stroke:rgba(110,65,40,.28);stroke-width:5.6;stroke-linecap:round;stroke-dasharray:1 1;animation-name:{draw};animation-timing-function:{EASE}" transform="translate(0,3)"></path>
        <path pathLength="1" d="{RIB}" style="fill:none;stroke:url(#rg);stroke-width:4.4;stroke-linecap:round;stroke-dasharray:1 1;animation-name:{draw};animation-timing-function:{EASE}"></path>
        <path pathLength="1" d="{RIB}" style="fill:none;stroke:rgba(255,255,255,.6);stroke-width:1.1;stroke-linecap:round;stroke-dasharray:1 1;animation-name:{draw};animation-timing-function:{EASE}"></path>
        <circle cx="372" cy="540" r="5" fill="url(#bg)" style="animation-name:{dot0}"></circle>
        <g transform="translate(600 422)"><circle r="9" fill="url(#bg)" style="animation-name:{bead}"></circle></g>
      </svg>
    </div>
    <div data-in="{t0 + .5}" style="position:absolute;left:44px;bottom:44px;padding:16px 26px;background:rgba(246,239,231,.94);border:1px solid {STONE};border-radius:14px;font-size:27px;color:{INK}" dir="rtl"><b style="color:{DEEP};font-weight:600">סרט הנחושת</b><br>קו אחד, רציף. אף פעם לא קשת.</div>""")}
  <div data-show="{T_IDEA},{T_TOUCHW - .1}" style="position:absolute;top:0;left:0;right:0">{stagebar('02 · הרעיון')}</div>
  {title('02 · הרעיון', 'כל מוצר מתחיל', 'במגע אנושי.', T_TOUCHW, T_LINE - .1)}
  {title('03 · האלמנט', 'קו נחושת עדין,', 'מהיד אל הבקבוק.', T_LINE + .25, T_PAL)}
</section>'''

# ───────── 04 the palette: three chips land, each with its bottle and its moment of the skin ─────────
PAL = [('DEW', '#F1D3A6', 'p-dew.webp', 'בוקר', 'לחות שנשארת<br>עד הערב', 205),
       ('GLOW', '#F0BFB0', 'p-glow.webp', 'ערב', 'זוהר שרואים<br>במראה', 262),
       ('CALM', '#D9B8C0', 'p-calm.webp', 'כשהעור מבקש', 'הרגעה לעור<br>שמגיב', 296)]
chips = ''
for i, (nm, hx, img, mom, mean, bw) in enumerate(PAL):
    t = T_PAL + .15 + i * .4; tm = t + .7
    land = kf('0%%,%s{opacity:0;transform:translateY(90px)}%s,100%%{opacity:1;transform:none}' % (P(t), P(t + .5)))
    rise = kf('0%%,%s{opacity:0;transform:translateY(50px) scale(.94)}%s,100%%{opacity:1;transform:none}' % (P(t + .2), P(t + .7)))
    lit = kf('0%%,%s{opacity:.0;transform:translateY(16px)}%s,100%%{opacity:1;transform:none}' % (P(tm - .1), P(tm + .3)))
    x = 730 - i * 340
    chips += f'''<div style="position:absolute;left:{x}px;top:350px;width:300px;height:1010px;animation-name:{land}">
  <div style="position:absolute;inset:0;border-radius:30px;background:{hx};box-shadow:0 20px 50px rgba(143,90,60,.14)"></div>
  <div style="position:absolute;top:34px;left:0;right:0;text-align:center;font-family:{LAT};font-size:66px;line-height:1;letter-spacing:.08em;color:{INK}" dir="ltr">{nm}</div>
  <div style="position:absolute;top:112px;left:0;right:0;text-align:center;font-family:{SANS};font-size:18px;letter-spacing:.22em;color:{DEEP}" dir="ltr">{hx}</div>
  <div style="position:absolute;top:170px;left:0;right:0;height:600px;display:flex;align-items:flex-end;justify-content:center;animation-name:{rise}"><img src="a/{img}" alt="" style="width:{bw}px;height:auto;display:block;filter:drop-shadow(0 18px 22px rgba(110,65,40,.25))"></div>
  <div style="position:absolute;top:800px;left:14px;right:14px;text-align:center;animation-name:{lit}" dir="rtl"><div style="font-family:{SERIF};font-weight:500;font-size:{40 if i == 2 else 50}px;line-height:1.1;color:{INK}">{mom}</div><div style="margin-top:12px;font-size:25px;line-height:1.35;color:{DEEP}">{mean}</div></div>
</div>'''
BASE = [('קרם', '#F6EFE7'), ('טרוורטין', '#D9C7B3'), ('סומק', '#EFCDBF'), ('נחושת', '#B87A57'), ('נחושת עמוקה', '#8F5A3C'), ('דיו', '#3A2E29')]
base = ''.join(f'<div data-in="{T_PAL + 1.5 + i * .07:.2f}" style="width:136px;display:flex;flex-direction:column;align-items:center;gap:10px"><span style="width:92px;height:92px;border-radius:50%;background:{h};border:2px solid #fff;box-shadow:0 8px 20px rgba(143,90,60,.2)"></span><span style="font-size:21px;color:{INK};white-space:nowrap">{n}</span></div>' for i, (n, h) in enumerate(BASE))
palette = f'''<section class="scene" data-show="{T_PAL},{T_LANG}" style="background:{CREAM}">
  {title('04 · הצבעים', 'שלושה גוונים,', 'לרגעים השונים של העור.', T_PAL, T_LANG)}
  {chips}
  <div style="position:absolute;top:1420px;left:50px;right:50px;display:flex;justify-content:space-between" dir="rtl">{base}</div>
</section>'''

# ───────── 05 the language: stone, pump, wordmark, the two-line headline — the board completes and holds ─────────
tl = T_LANG
def tile(x, t, inner, tag):
    return f'''<div data-in="{t}" style="position:absolute;left:{x}px;top:340px;width:470px;height:520px;border-radius:24px;overflow:hidden;box-shadow:0 18px 44px rgba(143,90,60,.16)">{inner}
  <span style="position:absolute;right:16px;bottom:16px;padding:9px 18px;border-radius:999px;background:rgba(246,239,231,.94);font-size:24px;color:{INK}" dir="rtl">{tag}</span></div>'''
track = kf('0%%,%s{letter-spacing:.02em;opacity:0}%s{opacity:1}%s,100%%{letter-spacing:.3em;opacity:1}' % (P(tl + 1.0), P(tl + 1.25), P(tl + 2.0)))
line2 = kf('0%%,%s{transform:translateY(110%%)}%s,100%%{transform:none}' % (P(tl + 2.2), P(tl + 2.7)))
strip = ''.join(f'<span style="flex:1;background:{h}"></span>' for h in ['#F1D3A6', '#F0BFB0', '#D9B8C0', '#F6EFE7', '#D9C7B3', '#EFCDBF', '#B87A57', '#8F5A3C', '#3A2E29'])
lang = f'''<section class="scene" data-show="{T_LANG},{T_PROM}" style="background:{CREAM}">
  {title('05 · השפה', 'אבן טבעית.', 'וטיפוגרפיה שקטה.', T_LANG, T_PROM)}
  {tile(560, tl + .15, '<img src="a/packaging-set-ribbon.webp" alt="" style="position:absolute;left:-150px;top:-360px;width:1320px;height:880px;display:block">', 'אבן הטרוורטין')}
  {tile(50, tl + .45, f'<div style="position:absolute;inset:0;background:{BLUSH}"></div><img src="a/p-glow.webp" alt="" style="position:absolute;left:-55px;top:40px;width:580px;height:auto;display:block">', 'משאבת הנחושת')}
  <div style="position:absolute;top:900px;left:50px;right:50px;height:250px;border-radius:24px;background:#FBF7F1;border:1px solid {STONE};display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px" data-in="{tl + .85}">
    <div style="font-family:{LAT};font-weight:400;font-size:118px;line-height:1;color:{INK};padding-left:.3em;animation-name:{track};animation-timing-function:cubic-bezier(.2,.7,.2,1)" dir="ltr">ORÉVA</div>
    <div style="font-family:{SANS};font-size:25px;letter-spacing:.42em;padding-left:.42em;color:{COPPER}" dir="ltr">SKIN STUDIO</div>
  </div>
  <div style="position:absolute;top:1180px;left:50px;right:50px;height:330px;border-radius:24px;background:#FBF7F1;border:1px solid {STONE}" data-in="{tl + 1.5}">
    <div style="position:absolute;top:26px;left:36px;right:36px;display:flex;justify-content:space-between;font-family:{SANS};font-size:18px;letter-spacing:.2em;color:{COPPER}" dir="ltr"><span>FRANK RUHL LIBRE</span><span dir="rtl" style="font-family:'Heebo',sans-serif;letter-spacing:.04em;font-size:22px">השורה השנייה</span></div>
    <div style="position:absolute;top:84px;left:36px;right:36px;text-align:right;font-family:{SERIF};font-weight:500;font-size:92px;line-height:1.14;color:{INK}" dir="rtl">קודם הידיים.<br><span style="display:inline-block;overflow:hidden;vertical-align:top"><span style="display:inline-block;color:{DEEP};animation-name:{line2}">אחר כך הבקבוק.</span></span></div>
  </div>
  <div data-in="{tl + 2.8}" style="position:absolute;top:1545px;left:50px;right:50px;height:96px;border-radius:18px;overflow:hidden;display:flex;border:1px solid {STONE}" dir="ltr">{strip}</div>
</section>'''

# shared: full-bleed runs with a light top for the title
TOPGRAD = '<div style="position:absolute;top:0;left:0;right:0;height:560px;background:linear-gradient(to bottom,rgba(246,239,231,.97) 0,rgba(246,239,231,.9) 52%,rgba(246,239,231,0))"></div>'
def run(items, starts, last_holds_to):
    T = starts[0]
    out = ''
    for i, (src, n, pos) in enumerate(items):
        a = starts[i]
        op = '' if i == 0 else f' data-show="{a:.2f},{D}" data-fade="0.4"'
        inner = seq(src, n, a - .45, pos) if n else f'<img class="cover" src="a/{src}" alt="" style="object-position:{pos}">'
        out += f'<div class="stack"{op}>{inner}</div>'
    push = kf('0%%,%s{transform:scale(1.08)}%s,100%%{transform:scale(1)}' % (P(T), P(last_holds_to)))
    return f'<div class="stack" style="animation-name:{push};animation-timing-function:linear">{out}</div>'

# ───────── 06 the promise: listening · touch · attention — one film per word ─────────
WORDS = ['בהקשבה.', 'במגע.', 'ובתשומת לב.']
words = ''.join(f'<span data-show="{PROM[i] + .1:.2f},{(PROM[i + 1] - .15) if i < 2 else D:.2f}" data-fade="0.15" style="position:absolute;top:0;right:0;white-space:nowrap">{w}</span>' for i, w in enumerate(WORDS))
promise = f'''<section class="scene" data-show="{T_PROM},{T_TOUCH}" style="background:{STONE}">
  {run([('diag/d_%03d.webp', 18, '25% 50%'), ('treat/t_%03d.webp', 18, '35% 50%'), ('consult/c_%03d.webp', 20, '25% 50%')], PROM, T_TOUCH + .4)}
  {TOPGRAD}
  <div style="position:absolute;top:0;left:0;right:0;height:310px">{stagebar('06 · ההבטחה')}
    <div style="position:absolute;top:112px;left:70px;right:70px;text-align:right;font-family:{SERIF};font-weight:500;font-size:78px;line-height:1.14;color:{INK}" dir="rtl">טיפוח שמתחיל<div style="position:relative;height:90px;color:{DEEP}">{words}</div></div>
  </div>
</section>'''

# ───────── 07 the identity: from the bottle, through the packaging, to the space ─────────
TP = [('lineup-three-serums-podiums.webp', 0, '50% 50%', 'הבקבוק', 'משאבת הנחושת · סרט הנחושת'),
      ('kit/k_%03d.webp', 20, '24% 50%', 'האריזה', 'סרט הנחושת · סומק'),
      ('studio-interior-reception.webp', 0, '50% 50%', 'החלל', 'אבן הטרוורטין · נחושת'),
      ('founder-counter-full-line.webp', 0, '58% 50%', 'הדלפק', 'סרט הנחושת · משאבת הנחושת · אבן הטרוורטין')]
tags = ''
for i, (src, n, pos, nm, codes) in enumerate(TP):
    a = TOUCH[i] - (.2 if i else -.1); b = D if i == 3 else TOUCH[i + 1] - .4
    tags += f'<div data-show="{a:.2f},{b:.2f}" data-fade="0.2" style="position:absolute;left:60px;top:1470px;padding:16px 28px;background:rgba(246,239,231,.94);border-radius:14px;text-align:right" dir="rtl"><div style="font-family:{SERIF};font-weight:500;font-size:46px;line-height:1.1;color:{INK}">{nm}</div><div style="margin-top:4px;font-size:23px;color:{DEEP}">{codes}</div></div>'
touch = f'''<section class="scene" data-show="{T_TOUCH},{D}" style="background:{STONE}">
  {run([(s, n, p) for s, n, p, _, _ in TP], TOUCH, T_OUT + .4)}
  {TOPGRAD}
  {title('07 · הזהות', 'אותו סיפור', 'בכל נקודת מפגש.', T_TOUCH, D)}
  {tags}
</section>'''

# ───────── outro (studio): the answer to the hook + CTA; holds to the last frame ─────────
def oin(t): return 'animation-name:%s;' % kf('0%%,%s{opacity:0;transform:translateY(28px)}%s,100%%{opacity:1;transform:none}' % (P(t), P(t + .55)))
win = kf('0%%,%s{opacity:0;transform:scale(1.9)}%s,100%%{opacity:1;transform:scale(1)}' % (P(T_OUT - .1), P(T_OUT + .8)))
S_BG, S_INK, S_COP = '#FAF8F3', '#6B563F', '#C4765A'
outro = f'''<section class="scene" data-show="{T_OUT},{D}" style="background:{S_BG}">
  <div style="position:absolute;top:84px;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center">
    <div style="font-size:28px;font-weight:500;letter-spacing:.06em;color:{S_COP};{oin(T_OUT + .1)}" dir="rtl">ORÉVA° · עולם מותג 24</div>
    <div style="font-size:62px;font-weight:600;line-height:1.2;color:{S_INK};" dir="rtl"><div style="{oin(T_OUT + .2)}">כשיש למותג זהות ברורה,</div><div style="{oin(T_NOT)}">לא משווים אותו לאחרים.</div></div>
    <div style="font-size:78px;font-weight:600;line-height:1.1;color:{S_COP};{oin(T_CHOOSE)}" dir="rtl">בוחרים בו.</div>
  </div>
  <div style="position:absolute;left:290px;top:520px;width:500px;height:800px;animation-name:{win};transform-origin:50% 50%">
    <div style="position:absolute;inset:0;overflow:hidden;box-shadow:0 40px 110px rgba(59,46,51,.26)"><img class="cover" src="a/founder-counter-full-line.webp" alt="" style="object-position:58% 50%"></div>
    <i style="position:absolute;left:-26px;top:-26px;width:40px;height:40px;border-top:2px solid {S_COP};border-left:2px solid {S_COP}"></i><i style="position:absolute;right:-26px;top:-26px;width:40px;height:40px;border-top:2px solid {S_COP};border-right:2px solid {S_COP}"></i>
    <i style="position:absolute;left:-26px;bottom:-26px;width:40px;height:40px;border-bottom:2px solid {S_COP};border-left:2px solid {S_COP}"></i><i style="position:absolute;right:-26px;bottom:-26px;width:40px;height:40px;border-bottom:2px solid {S_COP};border-right:2px solid {S_COP}"></i>
  </div>
  <div style="position:absolute;top:1410px;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;gap:24px;text-align:center;{oin(T_CHOOSE + 1.0)}">
    <div style="font-size:54px;font-weight:500;line-height:1.25;color:{S_COP}" dir="rtl">ואת העסק שלך?</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:22px 56px;background:{S_INK};color:{S_BG};border-radius:12px" dir="rtl"><span style="font-size:38px;font-weight:500">אבחון פער המותג</span><span style="font-size:23px;opacity:.8">30 דק׳ · בלי עלות</span></div>
    <div style="font-family:{SANS};font-size:22px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</section>'''

caps = ''.join(f'<div data-show="{a},{b}" data-fade="0.18" style="position:absolute;left:0;right:0;bottom:104px;display:flex;justify-content:center"><span style="max-width:960px;padding:16px 34px;border-radius:16px;background:rgba(58,46,41,.9);color:#FBF6EE;font-size:39px;font-weight:500;line-height:1.32;text-align:center" dir="rtl">{c}</span></div>' for a, b, c in CAPS)

RUNTIME = r'''(function(){
  const D=+document.body.dataset.duration,css=[];const P=t=>(Math.max(0,Math.min(D,t))/D*100).toFixed(3)+'%';let n=0;
  document.querySelectorAll('[data-show]').forEach(el=>{const [a,b]=el.dataset.show.split(',').map(Number),f=+(el.dataset.fade||.35),k='show'+(n++);
    const s=a<=0?'0%{opacity:1}':`0%,${P(a-f)}{opacity:0}${P(a)}{opacity:1}`;const e=b>=D?'100%{opacity:1}':`${P(b)}{opacity:1}${P(b+f)},100%{opacity:0}`;
    css.push(`@keyframes ${k}{${s}${e}}`);el.style.animationName=k;});
  document.querySelectorAll('[data-in]').forEach(el=>{const t=+el.dataset.in,k='in'+(n++);
    css.push(`@keyframes ${k}{0%,${P(t)}{opacity:0;transform:translateY(30px)}${P(t+.6)},100%{opacity:1;transform:none}}`);el.style.animationName=k;});
  document.querySelectorAll('[data-seq]').forEach(el=>{const d=el.dataset,from=+d.from,to=+d.to,by=+(d.by||1),start=+d.start,step=+d.step;
    const pad=(s,i)=>s.replace(/%0(\d)d/,(_,w)=>String(i).padStart(+w,'0'));
    const st=`position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:${d.pos||'50% 50%'};display:block`;
    const base=document.createElement('img');base.src=pad(d.seq,from);base.alt='';base.style.cssText=st;el.appendChild(base);
    let i=0,last=from;for(let f=from;f<=to;f+=by,i++){const im=document.createElement('img');im.src=pad(d.seq,f);im.alt='';im.className='bf';im.style.cssText=st+`;animation-delay:${(start+i*step).toFixed(3)}s`;el.appendChild(im);last=f;}
    const hold=document.createElement('img'),k='hold'+(n++),th=start+i*step;hold.src=pad(d.seq,last);hold.alt='';hold.style.cssText=st+`;animation-name:${k};animation-timing-function:linear`;
    css.push(`@keyframes ${k}{0%,${P(th-.05)}{opacity:0}${P(th)},100%{opacity:1}}`);el.appendChild(hold);});
  const s=document.createElement('style');s.textContent=css.join('\n');document.head.appendChild(s);
})();'''
prog = kf('0%{transform:scaleX(0)}100%{transform:scaleX(1)}')
BFW = 0.105 / D * 100   # each sequence frame stays visible ~0.105s
html = f'''<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>ORÉVA° — how the identity is built</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&amp;family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Heebo:wght@300;400;500;600&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">
<style>
html,body{{margin:0;background:{CREAM}}}
body{{font-family:'Heebo',sans-serif;color:{INK}}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
.film *{{animation-duration:{D:g}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
.scene{{position:absolute;inset:0;overflow:hidden}}
.bf{{animation-name:bf;animation-timing-function:linear}}
@keyframes bf{{0%{{opacity:0}}.005%{{opacity:1}}{BFW:.3f}%{{opacity:1}}{BFW + .005:.3f}%,100%{{opacity:0}}}}
{chr(10).join(css)}
</style></head>
<body data-duration="{D:g}"><div id="stage"><div class="film stack">
{hook}
{intro}
{question}
{story}
{palette}
{lang}
{promise}
{touch}
{outro}
{caps}
<div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18)"><div style="height:6px;background:#C4765A;transform-origin:right;animation-name:{prog};animation-timing-function:linear"></div></div>
</div></div>
<script>{RUNTIME}</script></body></html>'''
open(os.path.join(HERE, 'reel.html'), 'w', encoding='utf-8').write(html)
print('wrote reel.html', len(html))
