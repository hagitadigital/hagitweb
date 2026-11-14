# Generates reel.html: the studio's dessert-worlds reel, 22.5s, 1080x1920. One CSS timeline; times in seconds.
import pathlib
CREAM, DEEP, INK, SOFT, COPPER, CSOFT, CTEXT = '#F2EBDC', '#E7DEC9', '#15202E', '#3D4A5C', '#C28A5A', '#D9AE85', '#825630'
DISP = "'Cormorant Garamond','Frank Ruhl Libre',serif"
LAB = "'Plus Jakarta Sans','Heebo',sans-serif"

def an(k, t, d=.6, e='cubic-bezier(.2,.8,.2,1)'):
    return f'{k} {d}s {e} {t}s both'

def ball(t, frm, to, extra=''):
    # the copper ball on its line; rolls (in px from the right end) from `frm` to `to` starting at t
    return f'''<div style="position:relative;height:44px;{extra}">
<div style="position:absolute;left:0;right:0;top:20px;height:4px;border-radius:999px;background:{COPPER}"></div>
<div style="position:absolute;right:{to}px;top:0;width:44px;height:44px;border-radius:999px;background:{COPPER};box-shadow:0 0 0 10px {CSOFT},0 8px 18px rgba(20,30,45,.25);--x:{to-frm}px;animation:{an('roll', t, .9, 'cubic-bezier(.4,0,.2,1)')}"></div>
</div>'''

def world(a, no, inner, caption, bfrm, bto, bg, cut=False, shadow=.14):
    corners = ''.join(f'<div style="position:absolute;{h}:-24px;{v}:-24px;width:48px;height:48px;border-{h}:4px solid {COPPER};border-{v}:4px solid {COPPER};animation:{an("fade", a+.3, .3)}"></div>'
                      for h in ('left', 'right') for v in ('top', 'bottom'))
    return f'''<section class="scene" style="animation:fade {'.01' if cut else '.25'}s linear {a}s both;padding:170px 80px 330px;display:flex;flex-direction:column;gap:40px">
<div style="display:flex;justify-content:space-between;align-items:center;animation:{an('fade', a+.15, .35)}">
<div style="padding:10px 28px;border:2px solid {CSOFT};border-radius:999px;font-size:28px;line-height:1.4;color:{CTEXT}">עולם מותג קונספט · No.{no}</div>
<div dir="ltr" style="font-family:{LAB};font-size:22px;font-weight:500;letter-spacing:.22em;color:{CTEXT}">BRAND WORLDS STUDIO</div>
</div>
<div style="position:relative;flex:1 1 0;min-height:0">{corners}
<div style="position:absolute;inset:0;overflow:hidden;border-radius:20px;background:{bg};box-shadow:0 24px 60px rgba(20,30,45,{shadow});animation:{an('win', a, .5)}">{inner}</div>
</div>
<div style="display:flex;flex-direction:column;gap:16px">{caption}</div>
{ball(a+.15, bfrm, bto)}
</section>'''

def cap(a, h1, p, pre='', th=.6, tp=1.0):
    return f'''{pre}<h1 style="margin:0;font-size:64px;line-height:1.2;font-weight:600;animation:{an('rise', a+th, .5)}">{h1}</h1>
<p style="margin:0;font-size:40px;line-height:1.5;color:{SOFT};animation:{an('rise', a+tp, .5)}">{p}</p>'''

def name(a, txt, color=INK, ls='0', pos='top:48px'):
    return f'<div dir="ltr" style="position:absolute;left:0;right:0;{pos};text-align:center;font-family:{DISP};font-size:100px;line-height:1.05;letter-spacing:{ls};color:{color};animation:{an("rise", a+.3, .5)}">{txt}</div>'

def seq(folder, n, t, step):
    # a frame sequence: frames stack, each one switches on at its time
    return ''.join(f'<img src="assets/{folder}/f{i:02d}.webp" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover' + (f';animation:on .001s linear {t+(i-1)*step:.3f}s both' if i > 1 else '') + '">' for i in range(1, n+1))

# ── 1 · HOOK 0–2.4: the claim and its proof are on frame 0: five brands, five colour tiles ──
def htile(bg, img):
    return f'<div style="position:relative;overflow:hidden;border-radius:20px;background:{bg}">{img}</div>'
hook = f'''<section class="scene" style="padding:40px;display:flex;flex-direction:column;gap:16px">
<div style="flex:1 1 0;min-height:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px">
{htile('#FFFFFF', '<img src="assets/bowl-foret.webp" style="position:absolute;width:440px;height:440px;left:26px;top:140px;animation:spin 2.8s linear 0s both;--r0:-30deg;--r1:10deg">')}
{htile('#D4CFBA', f'<img src="assets/dish-pistache.webp" style="position:absolute;width:560px;height:420px;left:-34px;top:150px;animation:{an("zoom", 0, 2.6, "ease-out")}">')}
</div>
<div style="padding:52px 24px 44px;border-radius:20px;background:{DEEP};display:flex;flex-direction:column;align-items:center;gap:36px">
<h1 style="margin:0;font-size:72px;line-height:1.2;font-weight:600;text-align:center;white-space:nowrap">אותו תחום. חמישה מותגים.<br><span style="color:{COPPER}">אף אחד לא נראה כמו השני.</span></h1>
{ball(.1, 0, 908, 'width:100%').replace(' .9s ', ' 2.1s ')}
</div>
<div style="flex:1 1 0;min-height:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px">
{htile('#E3AEB8', f'<img src="assets/miel-cake.webp" style="position:absolute;width:360px;height:453px;left:-19px;top:140px;animation:{an("zoom", 0, 2.6, "ease-out")}">')}
{htile('#0C0907', f'<img src="assets/chou/f40.webp" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:{an("zoom", 0, 2.6, "ease-out")}">')}
{htile('#F6E38F', '<img src="assets/mac-framboise.webp" style="position:absolute;width:290px;height:334px;left:16px;top:190px;animation:spin 2.8s linear 0s both;--r0:-10deg;--r1:12deg">')}
</div>
</section>'''

# ── 2 · BOL 2.4–5.6 ──
a = 2.4
bol = world(a, '09', name(a, 'BOL°') + f'''
<img src="assets/bowl-soleil.webp" style="position:absolute;width:440px;height:440px;right:-140px;top:150px;animation:{an('fromR', a+.35, .6)},spin 4s linear {a+.35}s both;--r0:-70deg;--r1:20deg">
<img src="assets/bowl-jardin.webp" style="position:absolute;width:440px;height:440px;left:-140px;top:250px;animation:{an('fromL', a+.55, .6)},spin 4s linear {a+.55}s both;--r0:60deg;--r1:-20deg">
<img src="assets/bowl-foret.webp" style="position:absolute;width:600px;height:600px;left:160px;bottom:40px;animation:{an('pop', a+.75, .6)},spin 4s linear {a+.75}s both;--r0:-70deg;--r1:10deg">''',
            cap(a, 'הדף לבן.<br>הצבע נכנס רק לקערה.', 'בר קערות יוגורט שמזהים מרחוק.', th=.7, tp=1.1), 60, 160, '#FFFFFF')

# ── 3 · PANCAKERIE 5.6–9.0: the site's fan. The hero dishes turn on an arc; the ground and the box follow the flavour ──
a = 5.6; t1 = a + 1.35; t2 = a + 2.3
dish = lambda f, k: f'<img src="assets/dish-{f}.webp" style="position:absolute;left:180px;top:60px;width:560px;height:420px;transform-origin:280px 910px;rotate:{k*34}deg">'
box = lambda f, extra='': f'<img src="assets/box-{f}.webp" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;{extra}">'
pan = world(a, '26', f'''<div style="position:absolute;inset:0;background:#E5C9BC;animation:{an('fade', t1, .3, 'linear')}"></div>
<div style="position:absolute;inset:0;background:#EEDAB7;animation:{an('fade', t2, .3, 'linear')}"></div>
<div style="position:absolute;inset:0;animation:{an('pop', a+.25, .6)}"><div style="position:absolute;inset:0;transform-origin:460px 970px;animation:fan 3.4s cubic-bezier(.4,0,.2,1) {a}s both">
{dish('noisette', -1)}{dish('pistache', 0)}{dish('fraise', 1)}{dish('citron', 2)}</div></div>
<div style="position:absolute;left:210px;bottom:36px;width:500px;height:375px;overflow:hidden;border-radius:20px;box-shadow:0 18px 40px rgba(20,30,45,.2);animation:{an('rise', a+.45, .5)}">
{box('pistache')}{box('fraise', f"animation:{an('fade', t1, .3, 'linear')}")}{box('citron', f"animation:{an('fade', t2, .3, 'linear')}")}</div>''',
            cap(a, 'פה הטעם הוא צבע.', 'בוחרים טעם, והעמוד והמארז מתחלפים איתו.',
                f'<div dir="ltr" style="text-align:right;font-family:{DISP};font-style:italic;font-size:44px;line-height:1.2;color:{CTEXT};animation:{an("rise", a+.45, .5)}">Pancakerie°</div>'),
            160, 330, '#D4CFBA')

# ── 4 · MIEL 9.0–12.0: the promise is what is inside, so the scene is the cut itself ──
a = 9.0
miel = world(a, '27', seq('coupe', 61, a+.3, .04) + name(a, 'MIEL°', INK, '.12em', 'bottom:36px'),
             cap(a, 'רומנטיקה מתחילה<br>מבפנים.', 'קודם רואים מה שבפנים. מזה נגזר כל המותג.'), 330, 500, '#E3AEB8')

# ── 5 · SIGNÉ 12.0–14.6: hard cut to black; the dessert jumps out of the menu ──
a = 12.0
signe = world(a, '17', seq('chou', 60, a+.1, .04) + name(a, 'SIGNÉ°', '#2A1C12', '.14em', 'bottom:36px'),
              cap(a, 'תפריט שהקינוחים<br>קופצים ממנו.', 'בית קינוחים בשחור. כל קינוח חתום.', th=.5, tp=.9),
              500, 640, '#0C0907', cut=True, shadow=.28)

# ── 6 · PÉTALE 14.6–16.6 ──
a = 14.6
pet = world(a, '18', name(a, 'Pétale°') + f'''
<img src="assets/mac-pistache.webp" style="position:absolute;width:420px;height:330px;right:-80px;top:190px;rotate:16deg;animation:{an('drop', a+.25, .5)}">
<img src="assets/mac-framboise.webp" style="position:absolute;width:520px;height:600px;left:190px;bottom:50px;animation:{an('drop', a+.4, .6)},spin 2s ease-out {a+.4}s both;--r0:-40deg;--r1:-6deg">
<img src="assets/mac-pistache.webp" style="position:absolute;width:300px;height:236px;left:-90px;bottom:-30px;rotate:-24deg;animation:{an('drop', a+.55, .5)}">''',
            cap(a, 'שבעה טעמים,<br>קופסה אחת.', 'מקרונים שיורדים לקופסה ונקשרים בסרט.', th=.45, tp=.8),
            640, 760, '#F6E38F')

# ── 7 · THE BRIDGE 16.6–19.2: from pretty desserts to what the studio builds ──
a = 16.6
tiles = [('#FFFFFF', '<img src="assets/bowl-foret.webp" style="position:absolute;width:190px;height:190px;left:-11px;top:35px">'),
         ('#D4CFBA', '<img src="assets/dish-pistache.webp" style="position:absolute;width:240px;height:180px;left:-36px;top:46px">'),
         ('#E3AEB8', '<img src="assets/miel-cake.webp" style="position:absolute;width:190px;height:239px;left:-11px;top:18px">'),
         ('#0C0907', '<img src="assets/chou/f40.webp" style="position:absolute;width:100%;height:100%;left:0;top:0;object-fit:cover">'),
         ('#F6E38F', '<img src="assets/mac-framboise.webp" style="position:absolute;width:150px;height:173px;left:9px;top:44px">')]
turn = f'''<section class="scene" style="animation:fade .25s linear {a}s both;padding:80px;display:flex;flex-direction:column;justify-content:center;gap:72px">
<div style="display:flex;flex-direction:column;gap:28px">
<h1 style="margin:0;font-size:72px;line-height:1.18;font-weight:600"><span style="display:block;animation:{an('rise', a+.15, .5)}">לא עוד מותג שנראה טוב.</span><span style="display:block;color:{COPPER};animation:{an('rise', a+.5, .5)}">מותג שאי אפשר<br>לטעות בזיהוי שלו.</span></h1>
<p style="margin:0;font-size:40px;line-height:1.5;color:{SOFT};animation:{an('rise', a+1.0, .5)}">עולם מותג שלם: שפה, נראות ואתר.</p>
</div>
<div style="display:flex;flex-direction:column;gap:40px">
<div dir="ltr" style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px">
{''.join(f'<div style="position:relative;overflow:hidden;height:260px;border-radius:20px;background:{bg};box-shadow:0 12px 30px rgba(20,30,45,.12);animation:{an("pop", a+.2+i*.08, .45)}">{im}</div>' for i, (bg, im) in enumerate(tiles))}
</div>
<div dir="ltr" style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px;text-align:center;font-family:{DISP};font-style:italic;font-size:32px;line-height:1.2;color:{CTEXT};animation:{an('fade', a+.6, .4)}">
<div>BOL°</div><div>Pancakerie°</div><div>MIEL°</div><div>SIGNÉ°</div><div>Pétale°</div></div>
{ball(a+.2, 0, 876).replace(' .9s ', ' 1.8s ')}
</div>
</section>'''

# ── 8 · CTA 19.2–22.5: the question first, then the button; everything has landed by 20.8, then it holds ──
a = 19.2
cta = f'''<section class="scene" style="animation:fade .25s linear {a}s both;overflow:hidden;padding:80px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:80px;text-align:center">
<img src="assets/bowl-soleil.webp" style="position:absolute;width:520px;height:520px;right:-200px;top:-170px;animation:spin 1.8s ease-out {a}s both;--r0:-40deg;--r1:20deg">
<img src="assets/mac-framboise.webp" style="position:absolute;width:330px;height:380px;left:-110px;bottom:-90px;animation:spin 1.8s ease-out {a}s both;--r0:10deg;--r1:-18deg">
<div style="display:flex;flex-direction:column;gap:8px;animation:{an('rise', a+.1, .5)}">
<div dir="ltr" style="font-family:{DISP};font-style:italic;font-size:64px;line-height:1.2">Brand Worlds Studio</div>
<div style="font-size:28px;line-height:1.4;letter-spacing:.3em;color:{SOFT}">חגית אנטבי</div>
</div>
<h1 style="margin:0;font-size:76px;line-height:1.18;font-weight:600;animation:{an('rise', a+.25, .5)}">המותג שלך נראה כמו כולם,<br><span style="color:{COPPER}">או שיש לו עולם משלו?</span></h1>
{ball(a+.2, 0, 438, 'width:100%').replace(' .9s ', ' 1.1s ')}
<div style="display:flex;flex-direction:column;align-items:center;gap:24px">
<div style="padding:36px 96px;border-radius:12px;background:{INK};color:{CREAM};font-size:56px;line-height:1.2;font-weight:600;box-shadow:0 18px 40px rgba(20,30,45,.22);animation:{an('pop', a+1.0, .5)}">אבחון פער המותג</div>
<div style="font-size:40px;line-height:1.5;animation:{an('fade', a+1.25, .35)}">30 דק׳ · בלי עלות</div>
<div dir="ltr" style="font-family:{LAB};font-size:22px;font-weight:500;letter-spacing:.3em;color:{SOFT};animation:{an('fade', a+1.35, .35)}">HAGITANTEBI.CO.IL</div>
</div>
</section>'''

html = f'''<!doctype html><html lang="he"><head><meta charset="utf-8"><title>Dessert worlds reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Heebo:wght@400;500;600&family=Plus+Jakarta+Sans:wght@500&display=swap">
<style>
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:{CREAM}}}
.scene img:not([style*=animation]){{}}
.scene{{position:absolute;inset:0;box-sizing:border-box;background:{CREAM};color:{INK};font-family:'Heebo',sans-serif;direction:rtl}}
img{{display:block}}
@keyframes on{{from{{visibility:hidden}}to{{visibility:visible}}}}
@keyframes fan{{0%,38%{{rotate:0deg}}46%,66%{{rotate:-34deg}}74%,100%{{rotate:-68deg}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes out{{to{{opacity:0;scale:.8}}}}
@keyframes rise{{from{{opacity:0;translate:0 40px}}to{{opacity:1;translate:0 0}}}}
@keyframes riseBig{{from{{opacity:0;translate:0 300px;scale:.8}}to{{opacity:1;translate:0 0;scale:1}}}}
@keyframes pop{{0%{{opacity:0;scale:.55}}65%{{opacity:1;scale:1.05}}100%{{opacity:1;scale:1}}}}
@keyframes win{{from{{scale:.82;opacity:0}}to{{scale:1;opacity:1}}}}
@keyframes fromR{{from{{opacity:0;translate:420px 0}}to{{opacity:1;translate:0 0}}}}
@keyframes fromL{{from{{opacity:0;translate:-420px 0}}to{{opacity:1;translate:0 0}}}}
@keyframes drop{{0%{{opacity:0;translate:0 -800px}}70%{{opacity:1;translate:0 24px}}100%{{opacity:1;translate:0 0}}}}
@keyframes spin{{from{{rotate:var(--r0)}}to{{rotate:var(--r1)}}}}
@keyframes zoom{{from{{scale:1.18}}to{{scale:1}}}}
@keyframes zoomIn{{from{{scale:1}}to{{scale:1.08}}}}
@keyframes roll{{from{{translate:var(--x) 0}}to{{translate:0 0}}}}
@keyframes ring{{0%{{opacity:0;scale:.3}}30%{{opacity:1}}100%{{opacity:0;scale:2.4}}}}
@keyframes light{{from{{filter:brightness(.12)}}to{{filter:brightness(1)}}}}
</style></head><body>
{hook}{bol}{pan}{miel}{signe}{pet}{turn}{cta}
</body></html>'''
pathlib.Path(__file__).with_name('reel.html').write_text(html, encoding='utf-8')
