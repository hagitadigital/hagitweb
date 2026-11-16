# RUE° mini ad: "she walks into the project". 20.5s, 1080x1920, one CSS timeline (seconds). Opens on the site's hero lighting up.
# First cut built from the character's existing cut-outs (walk, sit); no generated scenes.
import pathlib, math
CREAM, INK, SOFT, COPPER, CSOFT = '#F2EBDC', '#15202E', '#3D4A5C', '#C28A5A', '#D9AE85'
NUIT, STONE, PEACH, APR, RINK = '#14122A', '#EFE6D8', '#F7C9A3', '#F2A977', '#1A1730'
DISP = "'Cormorant Garamond','Frank Ruhl Libre',serif"; SERIF = "'Frank Ruhl Libre',serif"; NUM = "'Bodoni Moda',serif"
LAB = "'Plus Jakarta Sans','Heebo',sans-serif"; EASE = 'cubic-bezier(.2,.8,.2,1)'
def an(k, t, d=.6, e=EASE): return f'{k} {d}s {e} {t}s both'
BALL = f'width:44px;height:44px;border-radius:999px;background:{COPPER};box-shadow:0 0 0 10px rgba(217,174,133,.45),0 8px 18px rgba(20,30,45,.35)'
kfs = []
def kf(name, body): kfs.append('@keyframes %s{%s}' % (name, body)); return name

def she(h, left, top, t, walk=None, extra=''):
    # the guide, cut out. walk=(x0,x1,dur): she crosses; a small bob keeps the step alive
    w = round(h * 290 / 760)
    mv = f'animation:walk {walk[2]}s linear {t}s both;--x0:{walk[0]}px;--x1:{walk[1]}px;' if walk else ''
    return f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;{mv}{extra}"><img src="assets/walk.webp" style="width:100%;height:100%;animation:bob .42s ease-in-out {t}s infinite alternate;filter:drop-shadow(0 14px 18px rgba(10,8,25,.45))"></div>'

def head(a, line, top=170):
    return f'''<div style="position:absolute;left:80px;right:80px;top:{top}px;display:flex;flex-direction:column;align-items:flex-start;gap:16px">
<div style="padding:10px 28px;border:2px solid {CSOFT};border-radius:999px;background:rgba(12,9,7,.55);font-size:28px;line-height:1.4;color:{CSOFT};animation:{an('fade', a+.3, .4)}">עולם מותג קונספט · No.07</div>
<div dir="ltr" style="font-family:{NUM};font-weight:500;font-size:88px;line-height:1;letter-spacing:.12em;color:{STONE};border:3px solid {STONE};border-radius:24px;padding:.28em .46em .2em .56em;animation:{an('rise', a+.45)}">RUE<span style="color:{APR}">°</span></div>
<div style="padding:10px 28px;margin-right:-28px;border-radius:12px;background:rgba(12,9,7,.6);font-size:60px;line-height:1.2;font-weight:600;color:{STONE};animation:{an('rise', a+.9)}">{line}</div>
</div>'''

# ── 1 · HOOK 0–2.8: the site's hero. The building lights up window by window; she walks the copper line in front of it ──
COMMON = [[27,80,10,14],[5,90,7,7],[42,91,6,6]]
HOMES = [[16.5,57,5.5,6.5],[28.5,48.5,3.2,5.5],[32.5,39,3.2,5.5],[19.5,44.5,4.2,5],[28.5,62,3.2,5.5],[31.5,26.5,3.2,5],[19,29.5,3.6,4.6],[32.5,51,3.2,5.5],[19.5,15,3.6,5.5],[32.5,64,3.2,5.5],[28.5,36,3.2,5.5],[28,23.5,3.2,5]]
def glow(g, t):
    m = 'radial-gradient(ellipse %s%% %s%% at %s%% %s%%,#000 0,#000 52%%,transparent 100%%)' % (g[2], g[3], g[0], g[1])
    a = '' if t <= 0 else f'animation:lamp .45s linear {t:.2f}s both;'
    return f'<div style="position:absolute;inset:0;background:url(assets/10-hero.webp) 0 0/100% 100%;-webkit-mask-image:{m};mask-image:{m};{a}"></div>'
def seq(folder, n, t, fps=24, h=1200):
    # a clip as stacked frames; each frame is visible only in its own 1/fps window, the last one holds
    out = ''
    for i in range(1, n+1):
        d = 30 if i == n else 1/fps
        out += f'<img src="assets/{folder}/f{i:03d}.jpg" style="position:absolute;left:0;top:0;width:1080px;height:{h}px;visibility:hidden;animation:win {d:.4f}s linear {t+(i-1)/fps:.3f}s forwards">'
    return out
# the site, as the huge thing under the line: its hero at desktop proportions, lighting up
SW, SH = 1010, 690
site = f'<div style="position:absolute;left:{(1080-SW)//2}px;top:1238px;width:{SW}px;height:{SH}px;border-radius:26px 26px 0 0;overflow:hidden;background:{NUIT};box-shadow:0 -10px 60px rgba(20,30,45,.28)">'
site += f'<div style="position:absolute;left:0;top:0;width:{round(SH*2400/1357)}px;height:{SH}px"><img src="assets/10-hero.webp" style="position:absolute;inset:0;width:100%;height:100%;filter:brightness(.46) saturate(.42) contrast(1.06) hue-rotate(-8deg)">'
site += ''.join(glow(g, 0) for g in COMMON) + ''.join(glow(g, -.42 + i*.21) for i, g in enumerate(HOMES))
site += f'<img src="assets/10-hero.webp" style="position:absolute;inset:0;width:100%;height:100%;animation:fade .7s linear 2.15s both"></div>'
site += f'<div style="position:absolute;left:0;right:0;top:0;height:90px;background:linear-gradient(rgba(20,18,42,.75),rgba(20,18,42,0))"></div>'
site += f'<div style="position:absolute;right:34px;top:26px;font-family:{NUM};font-weight:500;font-size:30px;letter-spacing:.12em;color:{STONE};border:2px solid {STONE};border-radius:9px;padding:.28em .5em .2em .58em" dir="ltr">RUE<span style="color:{APR}">°</span></div>'
site += f'<div style="position:absolute;left:36px;top:40px;display:flex;gap:26px;font-size:17px;color:rgba(239,230,216,.75);direction:rtl"><span>הכתובות</span><span>הדרך הביתה</span><span>השכונה</span><span>בפנים</span></div>'
site += f'<div style="position:absolute;right:40px;top:250px;text-align:right;font-family:{SERIF};font-size:78px;line-height:1.04;color:{STONE}">אותה כתובת.<br><span style="color:{PEACH}">סטנדרט אחר.</span></div></div>'
hook = f"""<section class="scene" style="overflow:hidden">
{seq('walk', 72, 0)}
<h1 style="position:absolute;left:80px;right:80px;top:250px;margin:0;font-size:76px;line-height:1.18;font-weight:600;text-align:right">הפרויקט שלך כבר עולם.<br><span style="color:{COPPER}">נכנסת אליו פעם?</span></h1>
<div style="position:absolute;left:0;right:0;top:1157px;height:4px;background:{COPPER}"></div>
<div style="position:absolute;left:0;top:1137px;{BALL};animation:walk 3s linear 0s both;--x0:470px;--x1:960px"></div>
{site}
</section>"""

# ── 2–4 · three Kling clips of her inside the world (stills by Hagit, GPT Image 2.6; clips kling-video-v3_0_turbo, 5s, 1080p) ──
def clip(a, folder, n, line):
    return f"""<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:{NUIT};color:{STONE}">
{seq(folder, n, a, h=1920)}
<div style="position:absolute;left:0;right:0;top:0;height:640px;background:linear-gradient(rgba(20,18,42,.72),rgba(20,18,42,0))"></div>
{head(a, line)}
</section>"""
model = clip(2.8, 'model', 63, 'אותה כתובת. סטנדרט אחר.')
plate = clip(5.4, 'plate', 63, 'הבניין מתחלף. המספר נשאר.')

# ── the site's own sections, between the clips ──
# the neighbourhood: the plate she just polished is the pin; the walking routes draw out of it
a = 8.0
routes = ['M330,310 H400', 'M330,310 H220 V268', 'M330,310 H400 V190', 'M330,310 H560 V364', 'M330,310 H220 V430 H124', 'M330,310 H560 V190']
spots = [(400,310,2), (220,268,3), (400,190,4), (560,364,6), (124,430,7), (560,190,8)]
rs = ''.join(f'<path pathLength="1" d="{d}" fill="none" stroke="{APR}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" style="animation:draw .7s cubic-bezier(.4,0,.2,1) {a+.35+i*.13:.2f}s both"/>' for i, d in enumerate(routes))
ss = ''.join(f'<g style="animation:fade .25s linear {a+.85+i*.13:.2f}s both"><circle cx="{x}" cy="{y}" r="19" fill="#15122D" stroke="{APR}" stroke-width="3"/><text x="{x}" y="{y+7}" text-anchor="middle" font-family="Bodoni Moda" font-size="20" fill="{STONE}">{n}</text></g>' for i, (x, y, n) in enumerate(spots))
places = ''.join(f'<div style="display:flex;align-items:baseline;gap:14px;padding:16px 0;border-bottom:1.5px solid rgba(239,230,216,.2);font-size:40px;animation:{an("rise", a+.9+i*.18, .5)}"><span>{nm}</span><span style="flex:1;border-bottom:2px dotted rgba(239,230,216,.4);transform:translateY(-8px)"></span><b style="font-family:{NUM};font-weight:500;font-size:60px;line-height:1;color:{PEACH}">{m}</b><span style="font-size:26px;color:rgba(239,230,216,.6)">דק׳</span></div>' for i, (nm, m) in enumerate([('המכולת בפינה', 2), ('גן הילדים', 4), ('הרכבת הקלה', 7)]))
carte = f"""<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:linear-gradient(#1D1942,#221C4A);color:{STONE}">
<svg viewBox="0 0 800 620" style="position:absolute;left:40px;top:560px;width:1000px;height:775px;border-radius:18px;background:#15122D">
<rect x="98" y="204" width="106" height="92" rx="10" fill="rgba(90,68,128,.4)"/>
<g fill="none" stroke="rgba(239,230,216,.08)" stroke-width="8" stroke-linecap="round"><path d="M0,92 C200,40 500,112 800,62"/><path d="M0,550 H800"/><path d="M80,0 V620"/><path d="M720,0 V620"/><path d="M540,620 L800,392"/></g>
<g fill="none" stroke="rgba(239,230,216,.12)" stroke-width="16" stroke-linecap="round"><path d="M0,190 H800"/><path d="M0,430 H800"/><path d="M220,0 V620"/><path d="M400,0 V620"/><path d="M560,0 V620"/><path d="M0,310 H800" stroke="rgba(239,230,216,.2)"/></g>
<circle cx="330" cy="310" r="150" fill="none" stroke="rgba(247,201,163,.3)" stroke-dasharray="3 8"/><circle cx="330" cy="310" r="292" fill="none" stroke="rgba(247,201,163,.3)" stroke-dasharray="3 8"/>
{rs}{ss}
<g transform="translate(330 310)"><g style="transform-box:fill-box;transform-origin:50% 100%;animation:pop .5s {EASE} {a+.1}s both"><path d="M0,0 L-11,-20 H11 Z" fill="{STONE}"/><rect x="-46" y="-80" width="92" height="62" rx="12" fill="{STONE}"/><text x="0" y="-35" text-anchor="middle" font-family="Frank Ruhl Libre" font-weight="500" font-size="40" fill="{RINK}">14</text></g></g>
</svg>
<div style="position:absolute;left:90px;right:90px;top:1390px">{places}</div>
{head(a, 'הבניין חדש. השכונה נשארת.')}
</section>"""

# the way home: five stairs rise, the last one lights
a = 10.2
steps = [('01-old.webp', 'הסכמות', '8', 'חודשים'), ('17-model.webp', 'היתר', '14', 'חודשים'), ('18-boxes.webp', 'דיור חלופי', '1', 'מעבר'), ('19-site.webp', 'בנייה', '30', 'חודשים'), ('16-flagship.webp', 'חוזרים הביתה', '14', 'אותו מספר')]
PWD, PHT, RISE, BASE = 188, 820, 80, 1740
stairs_h = ''
for i, (src, nm, num, unit) in enumerate(steps):
    x = 1080 - 50 - (i+1)*PWD - i*10; top = BASE - PHT - i*RISE; last = i == 4
    lit = f'animation:lit .5s linear {a+1.55}s both;' if last else 'filter:brightness(.62) saturate(.5);'
    stairs_h += f"""<div style="position:absolute;left:{x}px;top:{top}px;width:{PWD}px;height:{PHT}px;border-radius:14px 14px 0 0;overflow:hidden;background:#382C66;animation:{an('climb', a+.2+i*.2, .7)}{';box-shadow:0 0 0 3px '+APR if last else ''}">
<img src="assets/{src}" style="width:100%;height:100%;object-fit:cover;{lit}">
<div style="position:absolute;inset:0;background:linear-gradient(rgba(20,18,42,.94) 0,rgba(20,18,42,.5) 42%,rgba(20,18,42,0) 62%)"></div>
<div style="position:absolute;left:12px;right:12px;top:16px;text-align:right"><div style="font-size:22px;color:{PEACH}">מדרגה {i+1}</div><div style="font-family:{SERIF};font-size:{30 if len(nm)>8 else 36}px;line-height:1.1">{nm}</div><div style="margin-top:10px;padding-top:8px;border-top:1.5px dashed rgba(239,230,216,.45);display:flex;align-items:baseline;gap:8px;justify-content:flex-start"><b style="font-family:{SERIF};font-weight:500;font-size:64px;line-height:.9;color:{PEACH}">{num}</b><span style="font-size:20px;color:rgba(239,230,216,.75)">{unit}</span></div></div>
</div>"""
chemin = f"""<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:linear-gradient(#1A1639,#1D1942);color:{STONE}">
{stairs_h}
<div style="position:absolute;left:0;right:0;top:{BASE}px;bottom:0;background:#1D1942"></div>
<div style="position:absolute;left:50px;right:50px;top:{BASE}px;height:3px;background:rgba(239,230,216,.5)"></div>
{head(a, 'חמש מדרגות, ואז מפתח.')}
</section>"""

key = clip(12.5, 'key', 63, 'חוזרים הביתה.')

# inside: the rooms open as a fan over the sun
a = 15.1
CX, CY, R, R0, W = 540, 1330, 500, 112, 36.0
pt = lambda r, g: (R + r*math.cos(math.radians(g)), R - r*math.sin(math.radians(g)))
sector = 'polygon(50% 50%,' + ','.join('%.2f%% %.2f%%' % (pt(R, .7 + k*(W-1.4)/12)[0]/10, pt(R, .7 + k*(W-1.4)/12)[1]/10) for k in range(13)) + ')'
fan = ''
for i, src in enumerate(['16-flagship.webp', '22-lobby.webp', '20-kitchen.webp', '23-living.webp', '21-balcony.webp']):
    g = W*i
    pts = [pt(R0, g), pt(R, g), pt(R, g+W), pt(R0, g+W)] + [pt(R, q) for q in (90,) if g < q < g+W]
    xs = [q[0] for q in pts]; ys = [q[1] for q in pts]
    ko = kf('fo%d' % i, 'from{rotate:0deg}to{rotate:-%.1fdeg}' % g); ki = kf('fi%d' % i, 'from{rotate:0deg}to{rotate:%.1fdeg}' % g)
    fan += f'<div style="position:absolute;inset:0;clip-path:{sector};animation:{ko} 1.2s cubic-bezier(.4,0,.2,1) {a+.3}s both"><div style="position:absolute;inset:0;animation:{ki} 1.2s cubic-bezier(.4,0,.2,1) {a+.3}s both"><img src="assets/{src}" style="position:absolute;left:{min(xs):.0f}px;top:{min(ys):.0f}px;width:{max(xs)-min(xs):.0f}px;height:{max(ys)-min(ys):.0f}px;object-fit:cover"></div></div>'
inside = f"""<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:linear-gradient(#2F2659,#493873);color:{STONE}">
<div style="position:absolute;left:{CX-R}px;top:{CY-R}px;width:{2*R}px;height:{R}px;overflow:hidden"><div style="position:absolute;left:0;top:0;width:{2*R}px;height:{2*R}px">{fan}
<div style="position:absolute;left:{R-R0}px;top:{R-R0}px;width:{2*R0}px;height:{2*R0}px;border-radius:50%;background:#3F3270"></div>
<div style="position:absolute;left:{R-R0+22}px;top:{R-R0+22}px;width:{2*R0-44}px;height:{2*R0-44}px;border-radius:50%;background:radial-gradient(circle,#F7C9A3 0,#F2A977 70%,#A8718F 100%)"></div></div></div>
<div style="position:absolute;left:40px;right:40px;top:{CY}px;height:3px;background:rgba(239,230,216,.5)"></div>
<div style="position:absolute;left:0;right:0;top:{CY+70}px;text-align:center;font-size:40px;color:rgba(239,230,216,.85);animation:{an('fade', a+1.3, .4)}">הרחוב · הלובי · המטבח · הסלון · המרפסת</div>
{head(a, 'סטנדרט אחר מתחיל בפנים.')}
</section>"""

# ── 5 · CTA 12.6–15.5: she sits on the button; everything has landed by 14.2, then it holds ──
a = 17.6
cta = f'''<section class="scene" style="animation:fade .3s linear {a}s both;padding:80px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:72px;text-align:center">
<div style="display:flex;flex-direction:column;gap:8px;animation:{an('rise', a+.15)}">
<div dir="ltr" style="font-family:{DISP};font-style:italic;font-size:64px;line-height:1.2">Brand Worlds Studio</div>
<div style="font-size:28px;line-height:1.4;letter-spacing:.3em;color:{SOFT}">חגית אנטבי</div>
</div>
<div style="display:flex;flex-direction:column;gap:24px">
<h1 style="margin:0;font-size:96px;line-height:1.1;font-weight:600;animation:{an('rise', a+.35)}">הפרויקט שלך<br>כבר שווה <span style="color:{COPPER}">עולם.</span></h1>
<p style="margin:0;font-size:40px;line-height:1.5;color:{SOFT};animation:{an('rise', a+.6)}">בואי נראה מה חסר בין הפרויקט שלך<br>למותג שלך.</p>
</div>
<div style="position:relative;width:100%;height:44px">
<div style="position:absolute;left:0;right:0;top:20px;height:4px;border-radius:999px;background:{COPPER}"></div>
<div style="position:absolute;left:0;top:0;{BALL};animation:walk 1.2s cubic-bezier(.4,0,.2,1) {a+.2}s both;--x0:0px;--x1:438px"></div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:24px;margin-top:150px">
<div style="position:relative;width:760px;box-sizing:border-box;padding:36px 60px 36px 220px;border-radius:12px;background:{INK};color:{CREAM};font-size:56px;line-height:1.2;font-weight:600;box-shadow:0 18px 40px rgba(20,30,45,.22);animation:{an('pop', a+.9, .6)}">אבחון פער המותג
<img src="assets/sit.webp" style="position:absolute;left:24px;top:-196px;width:178px;height:360px;animation:{an('drop', a+1.3, .6)}">
</div>
<div style="font-size:40px;line-height:1.5;animation:{an('fade', a+1.2, .4)}">30 דק׳ · בלי עלות</div>
<div dir="ltr" style="font-family:{LAB};font-size:22px;font-weight:500;letter-spacing:.3em;color:{SOFT};animation:{an('fade', a+1.3, .4)}">HAGITANTEBI.CO.IL</div>
</div>
</section>'''

html = f'''<!doctype html><html lang="he"><head><meta charset="utf-8"><title>RUE mini ad</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Heebo:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500&family=Bodoni+Moda:opsz,wght@6..96,400..600&family=Frank+Ruhl+Libre:wght@300..700&display=swap">
<style>
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
.scene{{position:absolute;inset:0;box-sizing:border-box;background:{CREAM};color:{INK};font-family:'Heebo',sans-serif;direction:rtl}}
img{{display:block}}
@keyframes win{{0%,99.9%{{visibility:visible}}100%{{visibility:hidden}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes fadeout{{from{{opacity:1}}to{{opacity:0}}}}
@keyframes rise{{from{{opacity:0;translate:0 40px}}to{{opacity:1;translate:0 0}}}}
@keyframes pop{{0%{{opacity:0;scale:.55}}65%{{opacity:1;scale:1.05}}100%{{opacity:1;scale:1}}}}
@keyframes drop{{0%{{opacity:0;translate:0 -260px}}70%{{opacity:1;translate:0 10px}}100%{{opacity:1;translate:0 0}}}}
@keyframes walk{{from{{translate:var(--x0) 0}}to{{translate:var(--x1) 0}}}}
@keyframes bob{{from{{translate:0 0}}to{{translate:0 -7px}}}}
@keyframes lamp{{0%{{opacity:0}}16%{{opacity:.7}}30%{{opacity:.3}}100%{{opacity:1}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes climb{{from{{opacity:0;translate:0 140px}}to{{opacity:1;translate:0 0}}}}
@keyframes lit{{from{{filter:brightness(.62) saturate(.5)}}to{{filter:none}}}}
@keyframes wipe{{from{{clip-path:inset(100% 0 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes ringon{{from{{box-shadow:0 0 0 0 rgba(242,169,119,0)}}to{{box-shadow:0 0 0 14px rgba(242,169,119,.95),0 0 120px 30px rgba(242,169,119,.5)}}}}
{chr(10).join(kfs)}
</style></head><body>
{hook}{model}{plate}{carte}{chemin}{key}{inside}{cta}
</body></html>'''
pathlib.Path(__file__).with_name('reel.html').write_text(html, encoding='utf-8')
