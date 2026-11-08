"""UX reels · campaign "ככה בוחרים" (Oct 2026). Builds reel-desserts.html and reel-beauty.html (1080×1920, 25s).
Timing is in seconds; the page script turns data-* attributes into keyframes. Cue points come from ../audio/README.md.
Run: python3 gen.py  →  then  node <skill>/scripts/render.js reel-desserts.html 25 ../reel-desserts.mp4
"""
from pathlib import Path

D = 25
HERE = Path(__file__).parent

CSS = """
:root{--cream:#FAF8F3;--beige:#F5F1E8;--ink:#2A201A;--deep:#4F372C;--copper:#C4765A;--copper-text:#A45839;--copper-light:#E0A88E;--grey:#6F665C;--choc:#7A6349}
html,body{margin:0;background:var(--ink)}
body{font-family:'Heebo',sans-serif}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--ink)}
.film *{animation-duration:25s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}
.stack{position:absolute;inset:0}
.cover{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.scene{position:absolute;inset:0;overflow:hidden}
.disp{font-family:'Frank Ruhl Libre',serif;font-weight:500}
.lat{font-family:'Cormorant Garamond',serif}
.eyebrow{position:absolute;top:150px;right:80px;left:80px;display:flex;align-items:center;gap:22px;font-size:34px;font-weight:500}
.eyebrow .rule{width:90px;height:2px}
.box{position:absolute;top:270px;left:60px;width:960px;height:1080px;border-radius:28px;overflow:hidden;border:2px solid var(--copper);box-shadow:0 40px 90px rgba(20,14,10,.28)}
.pill{position:absolute;top:26px;right:26px;padding:10px 24px;border-radius:999px;font-size:28px;font-weight:500}
.lines{position:absolute;top:1420px;right:80px;left:80px;display:flex;flex-direction:column;gap:14px;text-align:right}
.l1{font-size:62px;line-height:1.2}
.l2{font-size:74px;line-height:1.15;font-style:italic}
.cap{position:absolute;top:1745px;right:80px;left:80px;font-size:28px;letter-spacing:.02em;text-align:right}
.mark{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:600;letter-spacing:.32em}
.phone{position:absolute;top:270px;left:250px;width:580px;height:1090px;box-sizing:border-box;border:16px solid #1A1410;border-radius:76px;overflow:hidden;box-shadow:0 40px 90px rgba(20,14,10,.3)}
.thumb{position:absolute;left:50%;margin-left:-44px;width:88px;height:88px;border-radius:50%;background:rgba(255,255,255,.42);border:3px solid rgba(255,255,255,.9)}
.progress{transform-origin:right;animation-name:prog;animation-timing-function:linear}
@keyframes prog{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
.line{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1}
.ball{position:absolute;left:0;top:0;width:96px;height:96px}
.halo{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.25);border:1.5px solid rgba(216,204,189,.7)}
.sph{position:absolute;left:12px;top:12px;width:72px;height:72px;border-radius:50%;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}
"""

JS = """
(function(){
  const D = +document.body.dataset.duration, css = [];
  const P = t => (Math.max(0, Math.min(D, t)) / D * 100).toFixed(3) + '%';
  let n = 0;
  const name = el => { const k = 'k' + (n++); el.style.animationName = k; return k; };
  document.querySelectorAll('[data-show]').forEach(el => {
    const [a, b] = el.dataset.show.split(',').map(Number), f = +(el.dataset.fade || .3), k = name(el);
    const s = a <= 0 ? '0%{opacity:1}' : `0%,${P(a - f)}{opacity:0}${P(a)}{opacity:1}`;
    const e = b >= D ? '100%{opacity:1}' : `${P(b)}{opacity:1}${P(b + f)},100%{opacity:0}`;
    css.push(`@keyframes ${k}{${s}${e}}`);
  });
  document.querySelectorAll('[data-in]').forEach(el => {
    const t = +el.dataset.in, k = name(el);
    css.push(`@keyframes ${k}{0%,${P(t)}{opacity:0;transform:translateY(34px)}${P(t + .55)},100%{opacity:1;transform:none}}`);
  });
  /* data-wipe="t": reveal from the right edge leftwards over .55s (RTL reading direction) */
  document.querySelectorAll('[data-wipe]').forEach(el => {
    const t = +el.dataset.wipe, k = name(el);
    css.push(`@keyframes ${k}{0%,${P(t)}{clip-path:inset(0 0 0 100%)}${P(t + .55)},100%{clip-path:inset(0 0 0 0)}}`);
  });
  /* data-tf="a;b;from;to": one transform move between a and b seconds */
  document.querySelectorAll('[data-tf]').forEach(el => {
    const [a, b, f, t] = el.dataset.tf.split(';'), k = name(el);
    css.push(`@keyframes ${k}{0%,${P(+a)}{transform:${f}}${P(+b)},100%{transform:${t}}}`);
  });
  /* data-seq: each frame shows from its start until the next one starts; the last frame holds */
  document.querySelectorAll('[data-seq]').forEach(el => {
    const d = el.dataset, from = +d.from, to = +d.to, by = +(d.by || 1), start = +d.start, step = +d.step;
    const pad = (s, i) => s.replace(/%0(\\d)d/, (_, w) => String(i).padStart(+w, '0'));
    const st = `position:absolute;inset:0;width:100%;height:100%;object-fit:${d.fit || 'cover'};object-position:${d.pos || '50% 50%'};display:block;animation-timing-function:linear`;
    const frames = []; for (let f = from; f <= to; f += by) frames.push(f);
    frames.forEach((f, i) => {
      const im = document.createElement('img'); im.src = pad(d.seq, f); im.alt = ''; im.style.cssText = st;
      const k = 'k' + (n++); im.style.animationName = k;
      const a = start + i * step, b = start + (i + 1) * step + .02, first = i === 0, last = i === frames.length - 1;
      let kf;
      if (first && last) kf = '0%,100%{opacity:1}';
      else if (first) kf = `0%,${P(b)}{opacity:1}${P(b + .001)},100%{opacity:0}`;
      else if (last) kf = `0%,${P(a - .001)}{opacity:0}${P(a)},100%{opacity:1}`;
      else kf = `0%,${P(a - .001)}{opacity:0}${P(a)},${P(b)}{opacity:1}${P(b + .001)},100%{opacity:0}`;
      css.push(`@keyframes ${k}{${kf}}`);
      el.appendChild(im);
    });
  });
  const s = document.createElement('style'); s.textContent = css.join('\\n'); document.head.appendChild(s);
})();
"""


def page(title, body):
    return f"""<!doctype html>
<html lang="he">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;1,500&amp;family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Heebo:wght@400;500;600&amp;family=Plus+Jakarta+Sans:wght@500;600&amp;display=swap">
<style>{CSS}</style>
</head>
<body data-duration="{D}">
<div id="stage"><div class="film stack">
{body}
<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 8px; background: rgba(196,118,90,.22)"><div class="progress" style="height: 8px; background: var(--copper)"></div></div>
</div></div>
<script>{JS}</script>
</body>
</html>"""


def theme(dark):
    return dict(bg='#2A201A' if dark else '#F5F1E8', ink='#FAF8F3' if dark else '#2A201A',
                muted='#CFC3B5' if dark else '#6F665C', acc='#E0A88E' if dark else '#A45839',
                rule='#E0A88E' if dark else '#C4765A')


def chapter(num, name, a, b, dark, media, l1, l2, cap, t1, t2):
    c = theme(dark)
    return f"""
<section class="scene" data-show="{a},{b}" style="background: {c['bg']}" dir="rtl">
  <div class="eyebrow" data-in="{a + .05}" style="color: {c['acc']}"><span class="lat" style="font-size: 44px">{num}</span><span class="rule" style="background: {c['rule']}"></span><span style="color: {c['ink']}">{name}</span></div>
  {media}
  <div class="lines">
    <div class="l1 disp" data-in="{t1}" style="color: {c['muted']}">{l1}</div>
    <div class="l2 disp" data-in="{t2}" style="color: {c['acc']}">{l2}</div>
  </div>
  <div class="cap" data-in="{t2 + .2}" style="color: {c['muted']}">{cap}</div>
</section>"""


def generic_card(img, label, price, a, b, dark=False):
    return f"""<div class="stack" data-show="{a},{b}" data-fade="0.25" style="background: #FFFFFF">
      <img class="cover" src="{img}" alt="" style="object-fit: contain; filter: grayscale(.35); padding: 90px 120px 200px; box-sizing: border-box">
      <span class="pill" style="background: #2E2A27; color: #F4F2EF">ככה משווים</span>
      <div style="position: absolute; left: 60px; right: 60px; bottom: 60px; display: flex; justify-content: space-between; font-size: 40px; color: #6E6660" dir="rtl"><span>{label}</span><b style="color: #2E2A27">{price}</b></div>
    </div>"""


def ball(y, t0, t1):
    d = f"M1160 {y} H540"
    p0, p1 = t0 / D * 100, t1 / D * 100
    return f"""<style>
.bl{{animation-name:bl;animation-timing-function:linear}}
@keyframes bl{{0%,{p0:.2f}%{{offset-distance:0%;opacity:0}}{p0 + .4:.2f}%{{opacity:1}}{p1:.2f}%,100%{{offset-distance:100%;opacity:1}}}}
.ln{{animation-name:ln;animation-timing-function:linear}}
@keyframes ln{{0%,{p0:.2f}%{{stroke-dashoffset:1}}{p1:.2f}%,100%{{stroke-dashoffset:0}}}}
.rl{{position:absolute;inset:0;animation-name:rl;animation-timing-function:linear}}
@keyframes rl{{0%,{p0:.2f}%{{transform:rotate(0)}}{p1:.2f}%,100%{{transform:rotate(-400deg)}}}}
</style>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line ln" pathLength="1" d="{d}"></path></svg>
  <div class="ball bl" style="offset-path: path('{d}')"><div class="halo"></div><div class="sph"><div class="rl"><div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-family: 'Cormorant Garamond', serif; font-size: 20px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 10px; top: 42px; width: 13px; height: 13px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>"""


def hook(end, g_img, g_name, g_price, w_img, w_pos, w_word):
    """Frame 0 already shows the question and the proof pair (it is the feed thumbnail)."""
    return f"""
<section class="scene" data-show="0,{end}" style="background: #2A201A" dir="rtl">
  <div style="position: absolute; top: 96px; right: 80px; left: 80px; display: flex; justify-content: space-between; align-items: baseline">
    <span class="lat" style="font-style: italic; font-size: 38px; color: #E0A88E" dir="ltr">Brand Worlds Studio</span>
    <span style="font-size: 24px; letter-spacing: .3em; color: #CFC3B5">חגית אנטבי</span>
  </div>
  <div class="disp" style="position: absolute; top: 230px; right: 80px; left: 80px; font-size: 98px; line-height: 1.14; color: #FAF8F3">למה מוצר אחד <span style="color: #E0A88E">משווים,</span><br>ואת השני <em style="color: #E0A88E">בוחרים?</em></div>
  <div style="position: absolute; top: 560px; right: 80px; left: 80px; height: 900px; display: flex; gap: 28px">
    <div style="flex: 1; background: #FFFFFF; border-radius: 22px; padding: 18px; box-sizing: border-box; display: flex; flex-direction: column; gap: 14px">
      <div style="position: relative; flex-grow: 1; min-height: 0"><img class="cover" src="{g_img}" alt="" style="object-fit: cover; border-radius: 12px"><span class="pill" style="top: 14px; right: 14px; background: #2E2A27; color: #F4F2EF; font-size: 26px">ככה משווים</span></div>
      <div style="display: flex; justify-content: space-between; font-size: 32px; color: #6E6660"><span>{g_name}</span><b style="color: #2E2A27">{g_price}</b></div>
    </div>
    <div style="flex: 1; position: relative; border-radius: 22px; overflow: hidden; border: 2px solid #C4765A">
      <img class="cover" src="{w_img}" alt="" style="object-position: {w_pos}">
      <span class="pill" style="top: 14px; right: 14px; background: #A45839; color: #FAF8F3; font-size: 26px">ככה בוחרים</span>
      <span class="disp" style="position: absolute; bottom: 22px; right: 18px; left: 18px; padding: 12px 10px; background: rgba(250,248,243,.9); color: #2A201A; font-size: 44px; text-align: center">{w_word}</span>
    </div>
  </div>
  {ball(1600, .25, end - .5)}
  <div class="mark" style="position: absolute; top: 1760px; left: 0; right: 0; text-align: center; color: #E0A88E" dir="ltr">BRAND · WORLDS · STUDIO</div>
</section>"""


def close(a, words, last, last_t, cta_t, ask):
    beats = ''.join(f'<span data-in="{t}" style="display: inline-block; margin-left: 22px">{w}</span>' for w, t in words)
    return f"""
<section class="scene" data-show="{a},{D}" style="background: #2A201A" dir="rtl">
  <div class="disp" style="position: absolute; top: 420px; right: 80px; left: 80px; font-size: 92px; line-height: 1.2; color: #FAF8F3">{beats}</div>
  <div class="disp" data-in="{last_t}" style="position: absolute; top: 560px; right: 80px; left: 80px; font-size: 92px; line-height: 1.18; font-style: italic; color: #E0A88E">{last}</div>
  <div data-in="{cta_t}" style="position: absolute; top: 1020px; right: 80px; left: 80px; display: flex; flex-direction: column; align-items: center; gap: 34px; text-align: center">
    <div style="font-size: 44px; line-height: 1.35; color: #E8DDD0">{ask}</div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 26px 64px; background: #C4765A; color: #2A201A; border-radius: 4px"><span style="font-size: 42px; font-weight: 600">אבחון פער המותג</span><span style="font-size: 26px">30 דק׳ · בלי עלות</span></div>
    <div class="mark" style="color: #E0A88E" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</section>"""


def phone_grid(img, a, b):
    tiles = ''.join(f'<div style="height: 300px; background: #FFFFFF; border-radius: 8px; overflow: hidden"><img src="{img}" alt="" style="width: 100%; height: 100%; object-fit: cover; filter: grayscale(.4)"></div>' for _ in range(10))
    return f"""<div class="phone" data-show="{a},{b}" data-fade="0.25" style="background: #EFEFEF">
      <div data-tf="{a};{b};translateY(0);translateY(-620px)" style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; padding: 90px 18px">{tiles}</div>
      <span class="pill" style="background: #2E2A27; color: #F4F2EF">ככה משווים</span>
    </div>"""


def thumb(a, b, y1=760, y2=300):
    return f"""<div class="stack" data-show="{a},{b}" style="pointer-events: none"><div data-tf="{a};{b};translateY({y1}px);translateY({y2}px)" style="position: absolute; top: 270px; left: 0; right: 0"><div class="thumb"></div></div></div>"""


# ── DESSERTS · music cut desserts-25s.mp3: drop 3.7, return 6.45, chapters 10.1 / 13.9 / 17.6, silence 21.7 ──
def desserts():
    slices = [('assets/41-slice-vanille-framboise-m.webp', 'ביסקוויט וניל · לב פטל'),
              ('assets/39-slice-chocolat-caramel-m.webp', 'ביסקוויט שוקולד · לב קרמל'),
              ('assets/36-slice-vanille-caramel-m.webp', 'ביסקוויט וניל · לב קרמל'),
              ('assets/38-slice-chocolat-framboise-m.webp', 'ביסקוויט שוקולד · לב פטל')]
    cuts = [10.35, 11.28, 12.21, 13.14]
    run = ''.join(f"""<div class="stack" data-show="{t},{(cuts[i + 1] if i + 1 < len(cuts) else 14.2)}" data-fade="0.12"><img class="cover" src="{s}" alt="" style="object-position: 46% 55%">
        <div style="position: absolute; left: 0; right: 0; bottom: 0; padding: 26px 30px; background: rgba(42,32,26,.72); color: #FAF8F3; font-size: 40px; text-align: center" dir="rtl">{l}</div></div>""" for i, (t, (s, l)) in enumerate(zip(cuts, slices)))
    ch1 = chapter('01', 'המוצר', 3.7, 10.1, False, f"""
  <div class="box">
    {generic_card('assets/generic-cake.jpg', 'עוגת קרם וניל', '₪159', 3.7, 4.7)}
    <div class="stack" data-wipe="4.55">
      <div class="stack" data-show="4.55,6.5" data-fade="0.1" data-seq="assets/coupe/c_%03d.jpg" data-from="1" data-to="14" data-start="4.55" data-step="0.135" data-pos="55% 40%"></div>
      <div class="stack" data-show="6.45,10.4" data-fade="0.05" data-seq="assets/coupe/c_%03d.jpg" data-from="18" data-to="41" data-start="6.45" data-step="0.08" data-pos="62% 45%"></div>
      <span class="pill" style="background: #A45839; color: #FAF8F3">ככה בוחרים</span>
    </div>
  </div>""", 'כל בייקרי מראה עוגה מבחוץ.', 'כאן חותכים.', 'MIEL° · רומנטיקה מתחילה מבפנים', 4.0, 6.5)
    chips = ''.join(f'<span style="padding: 12px 30px; border-radius: 999px; border: 2px solid #E0A88E; color: #FAF8F3">{c}</span>' for c in ['ביסקוויט', 'לב', 'רובּ', 'זר'])
    ch2 = chapter('02', 'רגע הבחירה', 10.1, 13.9, True, f"""
  <div style="position: absolute; top: 262px; right: 60px; left: 60px; display: flex; gap: 16px; align-items: center; font-size: 32px" dir="rtl">
    <span style="position: relative; padding: 12px 26px; background: #FFFFFF; color: #6E6660; border-radius: 6px">גודל: 20 ס״מ ▾<span data-tf="10.5;10.9;scaleX(0);scaleX(1)" style="position: absolute; left: 10px; right: 10px; top: 50%; height: 4px; background: #C4765A; transform-origin: right"></span></span>
    {chips}
  </div>
  <div class="box" style="top: 360px; height: 990px">{run}</div>""", 'לא בוחרים גודל.', 'בוחרים מה יהיה בפנים.', 'MIEL° · ארבע בחירות, 72 עוגות, טאפ אחד חותך', 10.3, 11.1)
    ch3 = chapter('03', 'הגלילה', 13.9, 17.6, False, f"""
  {phone_grid('assets/generic-cake.jpg', 13.9, 14.85)}
  <div class="phone" data-wipe="14.7" style="background: #120D0A">
    <div class="stack" data-seq="assets/signe/f%02d.webp" data-from="1" data-to="41" data-start="14.75" data-step="0.058" data-pos="49% 50%"></div>
    <div style="position: absolute; top: 70px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 58px; letter-spacing: .14em; color: #F1E6D8" dir="ltr">SIGNÉ°</div>
  </div>
  {thumb(14.8, 17.3)}""", 'שם גוללים תפריט.', 'כאן הגלילה מוזגת שוקולד.', 'SIGNÉ° · כל קינוח חתום', 14.1, 15.2)
    ch4 = chapter('04', 'האריזה', 17.6, 21.7, True, f"""
  <div class="box" style="background: #FFFFFF">
    <div class="stack" data-show="17.6,18.4" data-fade="0.25" style="display: flex; align-items: center; justify-content: center; background: #FFFFFF">
      <div style="width: 520px; height: 380px; background: #F2F2F2; border: 2px solid #DDDDDD; display: flex; align-items: center; justify-content: center"><span style="padding: 18px 30px; background: #FFFFFF; border: 1px solid #CCCCCC; font-size: 34px; color: #6E6660">מקרונים · 7 יח׳ · ₪89</span></div>
      <span class="pill" style="background: #2E2A27; color: #F4F2EF">ככה משווים</span>
    </div>
    <div class="stack" data-wipe="18.25">
      <div class="stack" data-show="18.25,20.2" data-fade="0.08" data-seq="assets/pet1/p_%03d.jpg" data-from="1" data-to="41" data-start="18.25" data-step="0.045"></div>
      <div class="stack" data-show="20.1,21.9" data-fade="0.08" data-seq="assets/pet2/p_%03d.jpg" data-from="1" data-to="41" data-start="20.1" data-step="0.038"></div>
      <span class="pill" style="background: #A45839; color: #FAF8F3">ככה בוחרים</span>
    </div>
  </div>""", 'שם קופסה עם מדבקה.', 'כאן שבעה צבעים נקשרים בסרט.', 'PÉTALE° · Pétale in colour', 17.8, 18.8)
    body = (hook(3.7, 'assets/generic-cake.jpg', 'עוגת קרם, מבחוץ', '₪159', 'assets/41-slice-vanille-framboise-m.webp', '42% 50%', 'מה שבפנים.')
            + ch1 + ch2 + ch3 + ch4
            + close(21.7, [('בחתך.', 21.75), ('בגלילה.', 22.2), ('בקופסה.', 22.65)], 'מה שבפנים<br>זה מה שבוחרים.', 23.1, 23.6,
                    'מה ההבטחה שלך<br>מראה מבפנים?'))
    return page('ריל קינוחים · מבפנים', body)


# ── BEAUTY · music cut beauty-25s.mp3: bars of 2.51s, chapters 2.5 / 7.5 / 12.6 / 17.6, silence 21.5, return 23.4 ──
def beauty():
    ch1 = chapter('01', 'המוצר', 2.5, 7.5, False, f"""
  <div class="box">
    {generic_card('assets/generic-serum.jpg', 'סרום פנים · 30 מ״ל', '₪89', 2.5, 3.4)}
    <div class="stack" data-wipe="3.25">
      <div class="stack" data-show="3.25,5.75" data-fade="0.1"><div class="stack" data-tf="3.25;5.9;scale(1.14);scale(1.0)"><img class="cover" src="assets/founder-cream-on-hand.webp" alt="" style="object-position: 34% 60%"></div></div>
      <div class="stack" data-show="5.6,7.9" data-fade="0.4"><div class="stack" data-tf="5.6;7.6;scale(1.0);scale(1.07)"><img class="cover" src="assets/founder-client-bottle.webp" alt="" style="object-position: 46% 50%"></div></div>
      <span class="pill" style="background: #A45839; color: #FAF8F3">ככה בוחרים</span>
    </div>
  </div>""", 'שם הבקבוק בפרונט.', 'כאן קודם הידיים.', '<span dir="ltr">ORÉVA° · Les mains d\'abord. Le flacon ensuite.</span>', 2.8, 4.0)
    ch2 = chapter('02', 'הגלילה', 7.5, 12.6, True, f"""
  {phone_grid('assets/generic-serum.jpg', 7.5, 8.45)}
  <div class="phone" data-wipe="8.3" style="background: #F3E6E1">
    <div class="stack" data-seq="assets/rosee/f_%03d.webp" data-from="1" data-to="80" data-by="2" data-start="8.35" data-step="0.088" data-pos="52% 50%"></div>
    <div style="position: absolute; top: 70px; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', serif; font-size: 56px; letter-spacing: .14em; color: #6B3F3A" dir="ltr">ROSÉE°</div>
  </div>
  {thumb(8.4, 12.0)}""", 'שם גוללים עוד ריבועים.', 'כאן הטיפה נופלת ונפתחת.', '<span dir="ltr">ROSÉE° · Née à l\'aube</span>', 7.7, 8.9)
    W = round(1080 * 880 / 496)   # the 16:9 sequence at the box height
    x1, x2 = -(0.45 * W - 480), -(0.635 * W - 480)
    ch3 = chapter('03', 'העיצוב', 12.6, 17.6, False, f"""
  <div class="box" style="background: #EEEBE1">
    {generic_card('assets/generic-serum.jpg', 'תווית לבנה · מחיר', '₪89', 12.6, 13.45)}
    <div class="stack" data-wipe="13.3" style="overflow: hidden">
      <div data-tf="13.3;16.8;translateX({x1:.0f}px);translateX({x2:.0f}px)" style="position: absolute; top: 0; left: 0; width: {W}px; height: 1080px">
        <div class="stack" data-seq="assets/elvea/f_%03d.webp" data-from="1" data-to="80" data-by="2" data-start="13.35" data-step="0.085"></div>
      </div>
      <span class="pill" style="background: #A45839; color: #FAF8F3">ככה בוחרים</span>
    </div>
  </div>""", 'שם תווית ומחיר.', 'כאן פרח, טיפה, ואז בקבוק.', 'ELVÉA° · הטבע מתחיל את הסיפור. הפורמולה מסיימת אותו.', 12.8, 14.0)
    ch4 = chapter('04', 'נקודות המגע', 17.6, 21.5, True, f"""
  <div style="position: absolute; top: 280px; left: 60px; width: 960px; box-sizing: border-box; padding: 14px 14px 26px; background: #120D0A; border-radius: 22px">
    <div style="position: relative; height: 504px; overflow: hidden; border-radius: 6px">
      <img class="cover" src="assets/elvea.webp" alt="">
      <div data-tf="18.3;18.75;scaleX(0);scaleX(1)" style="position: absolute; left: 15.5%; width: 27%; top: 31%; height: 21%; background: #C4765A; border-radius: 6px; transform-origin: right"></div>
    </div>
  </div>
  <div style="position: absolute; top: 880px; left: 60px; width: 960px; height: 470px; border-radius: 22px; overflow: hidden; border: 2px solid #C4765A">
    <img class="cover" src="assets/boutique-bags-m.webp" alt="" style="object-position: 78% 60%">
    <span class="pill" data-in="19.0" style="background: #A45839; color: #FAF8F3">גם על השקית אין שם</span>
  </div>""", 'הסתרנו את הלוגו.', 'עדיין יודעים של מי זה.', 'ELVÉA° · אתר, בוטיק, שקית', 18.0, 18.9)
    body = (hook(2.5, 'assets/generic-serum.jpg', 'סרום 30 מ״ל', '₪89', 'assets/founder-cream-on-hand.webp', '34% 60%', 'קודם הידיים.')
            + ch1 + ch2 + ch3 + ch4
            + close(21.5, [('בידיים.', 21.6), ('בטיפה.', 22.1), ('בשפה.', 22.6)], 'הבקבוק הוא רק<br>השכבה האחרונה.', 23.4, 23.7,
                    'מה קורה סביב<br>הבקבוק שלך?'))
    return page('ריל ביוטי · קודם הידיים', body)


if __name__ == '__main__':
    (HERE / 'reel-desserts.html').write_text(desserts(), encoding='utf8')
    (HERE / 'reel-beauty.html').write_text(beauty(), encoding='utf8')
    print('ok')
