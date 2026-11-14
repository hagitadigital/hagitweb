# Generates reel-4x5.html (1080x1350) and reel-9x16.html (1080x1920): "same product, same price" MIEL ad, 14s.
# One CSS timeline; times in seconds. Scene images are 1080x1910 and sit centred, so 4:5 shows their middle band.
import pathlib
CREAM, DEEP, INK, SOFT, COPPER, CSOFT, CTEXT = '#F2EBDC', '#E7DEC9', '#15202E', '#3D4A5C', '#C28A5A', '#D9AE85', '#825630'
DISP = "'Cormorant Garamond','Frank Ruhl Libre',serif"
LAB = "'Plus Jakarta Sans','Heebo',sans-serif"
EASE = 'cubic-bezier(.2,.8,.2,1)'
BALL = f'width:44px;height:44px;border-radius:999px;background:{COPPER};box-shadow:0 0 0 10px {CSOFT},0 8px 18px rgba(20,30,45,.25)'

def an(k, t, d=.5, e=EASE):
    return f'{k} {d}s {e} {t}s both'

def build(H):
    top = 60 if H == 1350 else 180          # first text line; 9:16 keeps clear of the app's top bar
    ioff = (H - 1910) // 2                   # the 1080x1910 image, centred

    def frames(folder, t, n=97, fps=24):
        # a 720p clip as stacked frames, each switching on at its time. Rebuild with:
        #   ffmpeg -i character/clips/<folder>.mp4 -q:v 2 src/assets/<folder>/f%03d.jpg
        return ''.join(f'<img src="assets/{folder}/f{i:03d}.jpg" style="position:absolute;left:0;top:0;width:1080px;height:1910px;object-fit:cover' + (f';animation:on .001s linear {t+(i-1)/fps:.3f}s both' if i > 1 else '') + '">' for i in range(1, n+1))

    def stage(img, a, dur, origin, z0, z1, overlays=''):
        return f'''<div style="position:absolute;left:0;top:{ioff}px;width:1080px;height:1910px;transform-origin:{origin};--z0:{z0};--z1:{z1};animation:push {dur+.3}s cubic-bezier(.3,0,.3,1) {a}s both">
{frames(img, a) if '.' not in img else f'<img src="assets/{img}" style="width:1080px;height:1910px">'}{overlays}</div>'''

    def price(x, y, t=None):
        anim = f';animation:{an("pop", t, .4)}' if t is not None else ''
        return f'<div style="position:absolute;left:{x}%;top:{y}%;translate:-50% -50%;padding:8px 26px;border-radius:999px;background:{INK};color:{CREAM};font-size:38px;font-weight:600;line-height:1.3;direction:ltr{anim}">₪290</div>'

    pill = lambda txt, t: f'<div style="padding:10px 28px;border:2px solid {CSOFT};border-radius:999px;background:rgba(242,235,220,.86);font-size:28px;line-height:1.4;color:{CTEXT};animation:{an("fade", t, .35)}">{txt}</div>'
    plate = lambda txt, t, size=64: f'<div style="padding:10px 28px;margin-right:-28px;border-radius:12px;background:rgba(242,235,220,.92);font-size:{size}px;line-height:1.2;font-weight:600;animation:{an("rise", t)}">{txt}</div>'

    # ── 1 · HOOK 0–3: two identical no-name slices, the same price; she cannot decide. All of it is on frame 0 ──
    hook = f'''<section class="scene" style="overflow:hidden;background:#C9C4BE">
{stage('scene-compare.jpg', 0, 3.0, '50% 58%', 1, 1.1,
       f'<div style="position:absolute;left:50%;top:40.5%;translate:-50% -50%;padding:8px 26px;border-radius:999px;background:#2E2A27;color:#F4F2EF;font-size:30px;line-height:1.4">ככה משווים</div>' + price(24, 69.5) + price(77, 69.5))}
<div style="position:absolute;left:60px;right:60px;top:{top}px;padding:28px 32px 26px;border-radius:20px;background:{DEEP};display:flex;flex-direction:column;align-items:center;gap:22px">
<h1 style="margin:0;font-size:76px;line-height:1.18;font-weight:600;text-align:center">אותו מוצר. אותו מחיר.<br><span style="color:{COPPER}">למה שיבחרו דווקא בך?</span></h1>
<div style="position:relative;width:100%;height:44px"><div style="position:absolute;left:0;right:0;top:20px;height:4px;border-radius:999px;background:{COPPER}"></div>
<div style="position:absolute;right:0;top:0;{BALL};--x0:0px;--x1:-852px;animation:walk 2.6s cubic-bezier(.4,0,.2,1) .1s both"></div></div>
</div>
</section>'''

    # ── 2 · MIEL 3–7: the same price, inside a world; she pulls her slice out of the vitrine ──
    a = 3.0
    vit = f'''<section class="scene" style="animation:fade .25s linear {a}s both;overflow:hidden;background:#E3AEB8">
{stage('vitrine', a, 4.0, '18% 56%', 1, 1.3, price(27, 68.5, a+1.2))}
<div style="position:absolute;left:80px;right:80px;top:{top}px;display:flex;flex-direction:column;align-items:flex-start;gap:14px">
{pill('MIEL° · עולם מותג קונספט · No.27', a+.2)}
{plate(f'אותו מחיר. <span style="color:{CTEXT}">עולם אחר.</span>', a+.5)}
</div>
</section>'''

    # ── 3 · THE BAG 7–10: the answer to the hook ──
    a = 7.0
    bag = f'''<section class="scene" style="animation:fade .25s linear {a}s both;overflow:hidden;background:#D9A7AB">
{stage('bag', a, 3.0, '70% 55%', 1.12, 1)}
<div style="position:absolute;right:60px;top:{top}px;width:400px;display:flex;flex-direction:column;align-items:flex-start;gap:14px">
{plate('עכשיו יש סיבה לבחור<br>דווקא בך.', a+.4, 58)}
</div>
</section>'''

    # ── 4 · CTA 10–14: the question, what the studio builds, then the button she sits on. Lands by 11.6, then holds ──
    a = 10.0
    gap = 34 if H == 1350 else 60
    cta = f'''<section class="scene" style="animation:fade .25s linear {a}s both;padding:70px 80px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:{gap}px;text-align:center">
<div style="display:flex;flex-direction:column;gap:6px;animation:{an('rise', a+.1)}">
<div dir="ltr" style="font-family:{DISP};font-style:italic;font-size:52px;line-height:1.2">Brand Worlds Studio</div>
<div style="font-size:34px;line-height:1.4;color:{SOFT}">MIEL° לא קיימת. העסק שלך כן.</div>
</div>
<h1 style="margin:0;font-size:76px;line-height:1.18;font-weight:600;animation:{an('rise', a+.3)}">איפה משווים אותך,<br><span style="color:{COPPER}">ואיך יוצאים מזה?</span></h1>
<p style="margin:0;font-size:40px;line-height:1.5;color:{SOFT};animation:{an('rise', a+.6)}">עולם מותג שלם: שפה, נראות ואתר.</p>
<div style="position:relative;width:100%;height:44px">
<div style="position:absolute;left:0;right:0;top:20px;height:4px;border-radius:999px;background:{COPPER}"></div>
<div style="position:absolute;left:0;top:0;{BALL};animation:walk 1.1s cubic-bezier(.4,0,.2,1) {a+.2}s both;--x0:0px;--x1:438px"></div>
</div>
<div style="display:flex;flex-direction:column;align-items:center;gap:18px;margin-top:{150 if H == 1350 else 170}px">
<div style="position:relative;width:760px;box-sizing:border-box;padding:36px 60px 36px 220px;border-radius:12px;background:{INK};color:{CREAM};font-size:56px;line-height:1.2;font-weight:600;box-shadow:0 18px 40px rgba(20,30,45,.22);animation:{an('pop', a+1.0)}">אבחון פער המותג
<img src="assets/sit.webp" style="position:absolute;left:24px;top:-196px;width:178px;height:360px;animation:{an('drop', a+1.3)}">
</div>
<div style="font-size:40px;line-height:1.5;animation:{an('fade', a+1.3, .35)}">30 דק׳ · בלי עלות</div>
<div dir="ltr" style="font-family:{LAB};font-size:22px;font-weight:500;letter-spacing:.3em;color:{SOFT};animation:{an('fade', a+1.4, .35)}">HAGITANTEBI.CO.IL</div>
</div>
</section>'''

    return f'''<!doctype html><html lang="he"><head><meta charset="utf-8"><title>MIEL · same product, same price</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Heebo:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500&display=swap">
<style>
html,body{{margin:0;width:1080px;height:{H}px;overflow:hidden;background:{CREAM}}}
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
{hook}{vit}{bag}{cta}
</body></html>'''

here = pathlib.Path(__file__).parent
(here / 'reel-4x5.html').write_text(build(1350), encoding='utf-8')
(here / 'reel-9x16.html').write_text(build(1920), encoding='utf-8')
