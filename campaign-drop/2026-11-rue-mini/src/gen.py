# RUE° mini ad: "she walks into the project". 15.5s, 1080x1920, one CSS timeline (seconds). Opens on the site's hero lighting up.
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
def seq(folder, n, t, fps=24):
    # the clip of her walking the line, as stacked frames (from character/clips/walk.mp4, top 800px, see NOTES.md)
    return ''.join(f'<img src="assets/{folder}/f{i:03d}.jpg" style="position:absolute;left:0;top:0;width:1080px;height:1200px' + (f';animation:on .001s linear {t+(i-1)/fps:.3f}s both' if i > 1 else '') + '">' for i in range(1, n+1))
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

# ── 2 · 2.8–6.2: the street. Three addresses stand on one pavement line; she walks it ──
a = 2.8
lots = [('16-flagship.webp', 620, 840, '14', 'הדקל 14'), ('11-tower.webp', 520, 720, '3', 'החוף 3'), ('14-hotel.webp', 600, 600, '9', 'ביאליק 9')]
track = ''
for src, w, h, n, nm in lots:
    track += f'<div style="flex:none;width:{w}px;margin:0 16px"><div style="height:{h}px;border-radius:14px 14px 0 0;overflow:hidden"><img src="assets/{src}" style="width:100%;height:100%;object-fit:cover"></div><div style="display:flex;align-items:center;gap:18px;padding-top:26px;direction:ltr"><span style="font-family:{SERIF};font-weight:500;font-size:60px;line-height:1;color:{PEACH};border:3px solid {PEACH};border-radius:12px;padding:.14em .36em .06em;min-width:1.7em;text-align:center">{n}</span><span style="font-family:{SERIF};font-size:50px;color:{STONE};direction:rtl">{nm}</span></div></div>'
street = f'''<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:linear-gradient({NUIT},#1D1942);color:{STONE}">
<div style="position:absolute;left:0;top:1610px;transform:translateY(-100%);display:flex;align-items:flex-end;direction:ltr;animation:walk 3.9s linear {a}s both;--x0:120px;--x1:-760px"><div style="display:flex;align-items:flex-start">{track}</div></div>
<div style="position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient({NUIT} 55%,rgba(20,18,42,0))"></div>
<div style="position:absolute;left:0;right:0;top:1487px;height:3px;background:rgba(239,230,216,.55)"></div>
<img src="assets/sit.webp" style="position:absolute;left:150px;top:{1487-212}px;width:{round(370*988/2000)}px;height:370px;animation:{an('drop', a+.5, .6)};filter:drop-shadow(0 14px 18px rgba(10,8,25,.45))">
{head(a, 'לפרויקט אין שם. יש לו כתובת.')}
</section>'''
# the lots sit with their image bottom on the line: shift the track so that captions fall below it
street = street.replace('top:1610px;transform:translateY(-100%)', 'top:1487px;transform:translateY(calc(-100% + 113px))')

# ── 3 · 6.2–9.7: the plate stays; the building behind it changes. She sits on it ──
a = 6.2
PW, PH, PT = 800, 430, 930
plate = f'''<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:{NUIT};color:{STONE}">
<img src="assets/01-old.webp" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.6) saturate(.6)">
<div style="position:absolute;inset:0;animation:wipe .7s cubic-bezier(.6,0,.2,1) {a+1.5}s both"><img src="assets/16-flagship.webp" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%"></div>
<div style="position:absolute;inset:0;background:linear-gradient(rgba(20,18,42,.92) 0,rgba(20,18,42,.5) 36%,rgba(20,18,42,.25) 60%,rgba(20,18,42,.85))"></div>
<div style="position:absolute;left:{(1080-PW)//2}px;top:{PT}px;width:{PW}px;height:{PH}px;border-radius:70px;background:{STONE};box-shadow:0 40px 90px rgba(10,8,25,.6);animation:{an('pop', a+.25, .6)}">
<div style="position:absolute;left:70px;top:0;height:{PH}px;display:flex;align-items:center;font-family:{SERIF};font-weight:500;font-size:330px;line-height:1;color:{RINK};direction:ltr;padding-top:.06em">14</div>
<div style="position:absolute;inset:0;border-radius:70px;animation:ringon .6s ease-out {a+2.3}s both"></div>
</div>
<img src="assets/sit.webp" style="position:absolute;left:{(1080-PW)//2+PW-250}px;top:{PT-258}px;width:{round(450*988/2000)}px;height:450px;animation:{an('drop', a+.95, .6)};filter:drop-shadow(0 16px 20px rgba(10,8,25,.4))">
<div style="position:absolute;left:0;right:0;top:1500px;text-align:center;direction:ltr;font-family:{NUM};font-size:84px;color:{PEACH}"><span style="animation:fadeout .25s linear {a+1.5}s both">1964</span></div>
<div style="position:absolute;left:0;right:0;top:1500px;text-align:center;direction:ltr;font-family:{NUM};font-size:84px;color:{PEACH};animation:{an('fade', a+1.75, .3)}">2029</div>
{head(a, 'הבניין מתחלף. המספר נשאר.')}
</section>'''

# ── 4 · 9.7–12.6: inside. The rooms open as a fan over the sun; she stands on the horizon ──
a = 9.7
CX, CY, R, R0, W = 540, 1330, 500, 112, 36.0
pt = lambda r, g: (R + r*math.cos(math.radians(g)), R - r*math.sin(math.radians(g)))
sector = 'polygon(50% 50%,' + ','.join('%.2f%% %.2f%%' % (pt(R, .7 + k*(W-1.4)/12)[0]/10, pt(R, .7 + k*(W-1.4)/12)[1]/10) for k in range(13)) + ')'
fan = ''
for i, src in enumerate(['16-flagship.webp', '22-lobby.webp', '20-kitchen.webp', '23-living.webp', '21-balcony.webp']):
    g = W*i
    pts = [pt(R0, g), pt(R, g), pt(R, g+W), pt(R0, g+W)] + [pt(R, q) for q in (90,) if g < q < g+W]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ko = kf('fo%d' % i, 'from{rotate:0deg}to{rotate:-%.1fdeg}' % g); ki = kf('fi%d' % i, 'from{rotate:0deg}to{rotate:%.1fdeg}' % g)
    fan += f'<div style="position:absolute;inset:0;clip-path:{sector};animation:{ko} 1.3s cubic-bezier(.4,0,.2,1) {a+.35}s both"><div style="position:absolute;inset:0;animation:{ki} 1.3s cubic-bezier(.4,0,.2,1) {a+.35}s both"><img src="assets/{src}" style="position:absolute;left:{min(xs):.0f}px;top:{min(ys):.0f}px;width:{max(xs)-min(xs):.0f}px;height:{max(ys)-min(ys):.0f}px;object-fit:cover"></div></div>'
inside = f'''<section class="scene" style="animation:fade .3s linear {a}s both;overflow:hidden;background:linear-gradient(#2F2659,#493873);color:{STONE}">
<div style="position:absolute;left:{CX-R}px;top:{CY-R}px;width:{2*R}px;height:{R}px;overflow:hidden"><div style="position:absolute;left:0;top:0;width:{2*R}px;height:{2*R}px">{fan}
<div style="position:absolute;left:{R-R0}px;top:{R-R0}px;width:{2*R0}px;height:{2*R0}px;border-radius:50%;background:#3F3270"></div>
<div style="position:absolute;left:{R-R0+22}px;top:{R-R0+22}px;width:{2*R0-44}px;height:{2*R0-44}px;border-radius:50%;background:radial-gradient(circle,#F7C9A3 0,#F2A977 70%,#A8718F 100%)"></div></div></div>
<div style="position:absolute;left:40px;right:40px;top:{CY}px;height:3px;background:rgba(239,230,216,.5)"></div>
<div style="position:absolute;left:0;right:0;top:{CY+70}px;text-align:center;font-size:40px;color:rgba(239,230,216,.8);animation:{an('fade', a+1.5, .4)}">הרחוב · הלובי · המטבח · הסלון · המרפסת</div>
{head(a, 'סטנדרט אחר מתחיל בפנים.')}
</section>'''

# ── 5 · CTA 12.6–15.5: she sits on the button; everything has landed by 14.2, then it holds ──
a = 12.6
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
@keyframes on{{from{{visibility:hidden}}to{{visibility:visible}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes fadeout{{from{{opacity:1}}to{{opacity:0}}}}
@keyframes rise{{from{{opacity:0;translate:0 40px}}to{{opacity:1;translate:0 0}}}}
@keyframes pop{{0%{{opacity:0;scale:.55}}65%{{opacity:1;scale:1.05}}100%{{opacity:1;scale:1}}}}
@keyframes drop{{0%{{opacity:0;translate:0 -260px}}70%{{opacity:1;translate:0 10px}}100%{{opacity:1;translate:0 0}}}}
@keyframes walk{{from{{translate:var(--x0) 0}}to{{translate:var(--x1) 0}}}}
@keyframes bob{{from{{translate:0 0}}to{{translate:0 -7px}}}}
@keyframes lamp{{0%{{opacity:0}}16%{{opacity:.7}}30%{{opacity:.3}}100%{{opacity:1}}}}
@keyframes wipe{{from{{clip-path:inset(100% 0 0 0)}}to{{clip-path:inset(0 0 0 0)}}}}
@keyframes ringon{{from{{box-shadow:0 0 0 0 rgba(242,169,119,0)}}to{{box-shadow:0 0 0 14px rgba(242,169,119,.95),0 0 120px 30px rgba(242,169,119,.5)}}}}
{chr(10).join(kfs)}
</style></head><body>
{hook}{street}{plate}{inside}{cta}
</body></html>'''
pathlib.Path(__file__).with_name('reel.html').write_text(html, encoding='utf-8')
