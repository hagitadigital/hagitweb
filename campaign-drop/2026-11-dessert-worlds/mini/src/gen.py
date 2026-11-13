# Generates reel.html: "she walks into the dessert" studio reel, 15.5s, 1080x1920. One CSS timeline; times in seconds.
import pathlib
CREAM, DEEP, INK, SOFT, COPPER, CSOFT, CTEXT = '#F2EBDC', '#E7DEC9', '#15202E', '#3D4A5C', '#C28A5A', '#D9AE85', '#825630'
DISP = "'Cormorant Garamond','Frank Ruhl Libre',serif"
LAB = "'Plus Jakarta Sans','Heebo',sans-serif"
EASE = 'cubic-bezier(.2,.8,.2,1)'

def an(k, t, d=.6, e=EASE):
    return f'{k} {d}s {e} {t}s both'

BALL = f'width:44px;height:44px;border-radius:999px;background:{COPPER};box-shadow:0 0 0 10px {CSOFT},0 8px 18px rgba(20,30,45,.25)'

def seq(folder, n, t, fps=24):
    # a video clip as stacked frames; each frame switches on at its time. Frames come from character/clips/*.mp4:
    #   ffmpeg -i ../character/clips/walk.mp4 -vf colorchannelmixer=rr=1.0168:gg=1.0173:bb=1.0233 -q:v 2 src/assets/walk/f%03d.jpg
    #   ffmpeg -i ../character/clips/taste.mp4 -q:v 2 src/assets/taste/f%03d.jpg
    return ''.join(f'<img src="assets/{folder}/f{i:03d}.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover' + (f';animation:on .001s linear {t+(i-1)/fps:.3f}s both' if i > 1 else '') + '">' for i in range(1, n+1))

def world(a, dur, img, no, nm, line, origin, z0, z1, dark=False, cut=False, pill_bg='rgba(242,235,220,.86)', clip=None):
    fg = CREAM if dark else INK
    return f'''<section class="scene" style="animation:fade {'.01' if cut else '.3'}s linear {a}s both;overflow:hidden;background:{'#000' if dark else '#fff'}">
{f'<div style="position:absolute;inset:0;transform-origin:{origin};--z0:{z0};--z1:{z1};animation:push {dur+.4}s cubic-bezier(.3,0,.3,1) {a}s both">{clip}</div>' if clip else f'''<img src="assets/{img}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform-origin:{origin};--z0:{z0};--z1:{z1};animation:push {dur+.4}s cubic-bezier(.3,0,.3,1) {a}s both{',light 1s ease-out '+str(a+.15)+'s both' if dark else ''}">'''}
<div style="position:absolute;left:80px;right:80px;top:170px;display:flex;flex-direction:column;align-items:flex-start;gap:16px">
<div style="padding:10px 28px;border:2px solid {CSOFT};border-radius:999px;background:{'rgba(12,9,7,.55)' if dark else pill_bg};font-size:28px;line-height:1.4;color:{CSOFT if dark else CTEXT};animation:{an('fade', a+.3, .4)}">עולם מותג קונספט · No.{no}</div>
<div dir="ltr" style="align-self:flex-start;font-family:{DISP};font-size:100px;line-height:1.05;color:{fg};animation:{an('rise', a+.45)}">{nm}</div>
<div style="padding:10px 28px;margin-right:-28px;border-radius:12px;background:{'rgba(12,9,7,.6)' if dark else 'rgba(242,235,220,.9)'};font-size:64px;line-height:1.2;font-weight:600;color:{fg};animation:{an('rise', a+.9)}">{line}</div>
</div>
</section>'''

# ── 1 · HOOK 0–2.6: she is small, the dessert is huge; the question is on frame 0 ──
hook = f'''<section class="scene" style="overflow:hidden">
{seq('walk', 72, 0)}
<h1 style="position:absolute;left:80px;right:80px;top:250px;margin:0;font-size:76px;line-height:1.18;font-weight:600;text-align:right">הקינוח שלך כבר עולם.<br><span style="color:{COPPER}">נכנסת אליו פעם?</span></h1>
<div style="position:absolute;left:0;right:0;top:1157px;height:4px;background:{COPPER}"></div>
<div style="position:absolute;left:0;top:1137px;{BALL};animation:walk 3s linear 0s both;--x0:470px;--x1:960px"></div>
</section>'''

bol = world(2.6, 3.4, 'scene-bol.jpg', '09', 'BOL°', 'בול מה שבחרת.', '74% 36%', 1, 1.16, clip=seq('taste', 90, 2.6))
miel = world(6.0, 3.5, 'scene-miel.jpg', '27', 'MIEL°', 'רומנטיקה מתחילה מבפנים.', '53% 60%', 1, 1.32, pill_bg='rgba(242,235,220,.7)')
signe = world(9.5, 3.0, 'scene-signe.jpg', '17', 'SIGNÉ°', 'כל קינוח חתום.', '62% 58%', 1.12, 1, dark=True, cut=True)

# ── 5 · CTA 12.5–15.5: she sits on the button; everything has landed by 14, then it holds ──
a = 12.5
cta = f'''<section class="scene" style="animation:fade .3s linear {a}s both;padding:80px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:72px;text-align:center">
<div style="display:flex;flex-direction:column;gap:8px;animation:{an('rise', a+.15)}">
<div dir="ltr" style="font-family:{DISP};font-style:italic;font-size:64px;line-height:1.2">Brand Worlds Studio</div>
<div style="font-size:28px;line-height:1.4;letter-spacing:.3em;color:{SOFT}">חגית אנטבי</div>
</div>
<div style="display:flex;flex-direction:column;gap:24px">
<h1 style="margin:0;font-size:96px;line-height:1.1;font-weight:600;animation:{an('rise', a+.35)}">הקינוח שלך<br>כבר שווה <span style="color:{COPPER}">עולם.</span></h1>
<p style="margin:0;font-size:40px;line-height:1.5;color:{SOFT};animation:{an('rise', a+.6)}">בואי נראה מה חסר בין המוצר שלך<br>למותג שלך.</p>
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

html = f'''<!doctype html><html lang="he"><head><meta charset="utf-8"><title>Dessert worlds mini reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Heebo:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500&display=swap">
<style>
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
.scene{{position:absolute;inset:0;box-sizing:border-box;background:{CREAM};color:{INK};font-family:'Heebo',sans-serif;direction:rtl}}
img{{display:block}}
@keyframes on{{from{{visibility:hidden}}to{{visibility:visible}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes rise{{from{{opacity:0;translate:0 40px}}to{{opacity:1;translate:0 0}}}}
@keyframes pop{{0%{{opacity:0;scale:.55}}65%{{opacity:1;scale:1.05}}100%{{opacity:1;scale:1}}}}
@keyframes drop{{0%{{opacity:0;translate:0 -260px}}70%{{opacity:1;translate:0 10px}}100%{{opacity:1;translate:0 0}}}}
@keyframes spin{{from{{rotate:var(--r0)}}to{{rotate:var(--r1)}}}}
@keyframes walk{{from{{translate:var(--x0) 0}}to{{translate:var(--x1) 0}}}}
@keyframes bob{{from{{translate:0 0}}to{{translate:0 -10px}}}}
@keyframes push{{from{{scale:var(--z0)}}to{{scale:var(--z1)}}}}
@keyframes light{{from{{filter:brightness(.1)}}to{{filter:brightness(1)}}}}
</style></head><body>
{hook}{bol}{miel}{signe}{cta}
</body></html>'''
pathlib.Path(__file__).with_name('reel.html').write_text(html, encoding='utf-8')
