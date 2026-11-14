# Generates reel.html (1080x1920): ELVÉA "if we hide the name" ad with the character, 15.5s.
# One CSS timeline; times in seconds. The name stays hidden until the reveal scene, so no ELVÉA text before it.
# Scenes are 720p clips shown as stacked frames. Rebuild the frames with:
#   ffmpeg -i character/clips/<name>.mp4 -q:v 2 src/assets/<name>/f%03d.jpg
import pathlib, os
CREAM, DEEP, INK, SOFT, COPPER, CSOFT, CTEXT = '#F2EBDC', '#E7DEC9', '#15202E', '#3D4A5C', '#C28A5A', '#D9AE85', '#825630'
DISP = "'Cormorant Garamond','Frank Ruhl Libre',serif"
LAB = "'Plus Jakarta Sans','Heebo',sans-serif"
EASE = 'cubic-bezier(.2,.8,.2,1)'
BALL = f'width:44px;height:44px;border-radius:999px;background:{COPPER};box-shadow:0 0 0 10px {CSOFT},0 8px 18px rgba(20,30,45,.25)'
here = pathlib.Path(__file__).parent
TOP = 180   # first text line, clear of the app's top bar

def an(k, t, d=.5, e=EASE):
    return f'{k} {d}s {e} {t}s both'

def stage(name, a, dur, origin, z0, z1, fps=24):
    # the scene's clip if its frames exist, else the still
    folder = here / 'assets' / name
    n = len(list(folder.glob('f*.jpg'))) if folder.is_dir() else 0
    if n:
        inner = ''.join(f'<img src="assets/{name}/f{i:03d}.jpg" style="position:absolute;left:0;top:0;width:1080px;height:1910px;object-fit:cover' + (f';animation:on .001s linear {a+(i-1)/fps:.3f}s both' if i > 1 else '') + '">' for i in range(1, n+1))
    else:
        inner = f'<img src="assets/scene-{name}.jpg" style="width:1080px;height:1910px">'
    return f'<div style="position:absolute;left:0;top:5px;width:1080px;height:1910px;transform-origin:{origin};--z0:{z0};--z1:{z1};animation:push {dur+.3}s cubic-bezier(.3,0,.3,1) {a}s both">{inner}</div>'

pill = lambda txt, t: f'<div style="padding:10px 28px;border:2px solid {CSOFT};border-radius:999px;background:rgba(242,235,220,.86);font-size:28px;line-height:1.4;color:{CTEXT};animation:{an("fade", t, .35)}">{txt}</div>'
plate = lambda txt, t, size=64: f'<div style="padding:10px 28px;margin-right:-28px;border-radius:12px;background:rgba(242,235,220,.92);font-size:{size}px;line-height:1.2;font-weight:600;animation:{an("rise", t)}">{txt}</div>'

def world(name, a, dur, origin, z0, z1, text, bg):
    return f'''<section class="scene" style="animation:fade .25s linear {a}s both;overflow:hidden;background:{bg}">
{stage(name, a, dur, origin, z0, z1)}
<div style="position:absolute;left:80px;right:80px;top:{TOP}px;display:flex;flex-direction:column;align-items:flex-start;gap:14px">{text}</div>
</section>'''

# ── 1 · HOOK 0–3.2: she covers the name herself; question and proof are on frame 0 ──
hook = f'''<section class="scene" style="overflow:hidden;background:#D8CCB8">
{stage('hook', 0, 3.2, '50% 62%', 1, 1.08)}
<div style="position:absolute;left:60px;right:60px;top:150px;padding:28px 32px 26px;border-radius:20px;background:{DEEP};display:flex;flex-direction:column;align-items:center;gap:22px">
<h1 style="margin:0;font-size:76px;line-height:1.18;font-weight:600;text-align:center">אם נסתיר את השם,<br><span style="color:{COPPER}">עדיין יזהו אותך?</span></h1>
<div style="position:relative;width:100%;height:44px"><div style="position:absolute;left:0;right:0;top:20px;height:4px;border-radius:999px;background:{COPPER}"></div>
<div style="position:absolute;right:0;top:0;{BALL};--x0:0px;--x1:-852px;animation:walk 2.8s cubic-bezier(.4,0,.2,1) .1s both"></div></div>
</div>
</section>'''

# ── 2 · THE BOX 3.2–6.0 and 3 · THE BAGS 6.0–8.8: no name anywhere, only the line ──
box = world('box', 3.2, 2.8, '40% 55%', 1, 1.12,
            pill('עולם מותג קונספט · No.14', 3.4) + plate('אותו קו. גם על הקופסה.', 3.7), '#D6CDB6')
bags = world('bags', 6.0, 2.8, '55% 60%', 1, 1.1, plate('גם על השקית. גם בחנות.', 6.4), '#DCD2BF')

# ── 4 · THE REVEAL 8.8–11.8: the sticker is off, the name is there; it answers the hook ──
reveal = world('reveal', 8.8, 3.0, '48% 60%', 1, 1.14,
               pill('ELVÉA° · עולם מותג קונספט', 9.4) + plate(f'<span style="color:{CTEXT}">יזהו אותך.</span>', 9.1, 84), '#D8CCB8')

# ── 5 · CTA 11.8–15.5: the question to her, what the studio builds, the button she sits on. Lands by 13.5, then holds ──
a = 11.8
cta = f'''<section class="scene" style="animation:fade .25s linear {a}s both;padding:70px 80px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:60px;text-align:center">
<div style="display:flex;flex-direction:column;gap:6px;animation:{an('rise', a+.1)}">
<div dir="ltr" style="font-family:{DISP};font-style:italic;font-size:52px;line-height:1.2">Brand Worlds Studio</div>
<div style="font-size:34px;line-height:1.4;color:{SOFT}">ELVÉA° לא קיים. העסק שלך כן.</div>
</div>
<h1 style="margin:0;font-size:76px;line-height:1.18;font-weight:600;animation:{an('rise', a+.3)}">אם נסתיר את השם שלך,<br><span style="color:{COPPER}">מה יישאר?</span></h1>
<p style="margin:0;font-size:40px;line-height:1.5;color:{SOFT};animation:{an('rise', a+.6)}">עולם מותג שלם: שפה, נראות ואתר.</p>
<div style="position:relative;width:100%;height:44px">
<div style="position:absolute;left:0;right:0;top:20px;height:4px;border-radius:999px;background:{COPPER}"></div>
<div style="position:absolute;left:0;top:0;{BALL};animation:walk 1.1s cubic-bezier(.4,0,.2,1) {a+.2}s both;--x0:0px;--x1:438px"></div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:18px;margin-top:170px">
<div style="position:relative;width:760px;box-sizing:border-box;padding:36px 60px 36px 220px;border-radius:12px;background:{INK};color:{CREAM};font-size:56px;line-height:1.2;font-weight:600;box-shadow:0 18px 40px rgba(20,30,45,.22);animation:{an('pop', a+1.0)}">אבחון פער המותג
<img src="assets/sit.webp" style="position:absolute;left:24px;top:-196px;width:178px;height:360px;animation:{an('drop', a+1.3)}">
</div>
<div style="font-size:40px;line-height:1.5;animation:{an('fade', a+1.3, .35)}">30 דק׳ · בלי עלות</div>
<div dir="ltr" style="font-family:{LAB};font-size:22px;font-weight:500;letter-spacing:.3em;color:{SOFT};animation:{an('fade', a+1.4, .35)}">HAGITANTEBI.CO.IL</div>
</div>
</section>'''

html = f'''<!doctype html><html lang="he"><head><meta charset="utf-8"><title>ELVÉA · if we hide the name</title>
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
@keyframes walk{{from{{translate:var(--x0) 0}}to{{translate:var(--x1) 0}}}}
@keyframes push{{from{{scale:var(--z0)}}to{{scale:var(--z1)}}}}
</style></head><body>
{hook}{box}{bags}{reveal}{cta}
</body></html>'''
(here / 'reel.html').write_text(html, encoding='utf-8')
