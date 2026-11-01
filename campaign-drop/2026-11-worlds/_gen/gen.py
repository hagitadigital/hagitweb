#!/usr/bin/env python3
"""Hidden-logo reels, Nov 2026 — ORÉVA°, ENCORE°, MIEL°.
Same skeleton as the ELVÉA° hidden-logo reel (26.5s): hook → 01 הסמל · 02 האתר · 03 המוצרים · 04 האריזה ·
05 החנות · 06 הפיד → outro with the answer and the CTA. Plus a 3s hook-only clip per world.

Usage (from the repo root):  python3 campaign-drop/2026-11-worlds/_gen/gen.py [world ...]
Writes campaign-drop/2026-11-worlds/<world>/src/{reel.html,hook.html,assets/…}. Render with the skill's render.js."""
import os, sys, shutil, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from film import Film

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'campaign-drop', '2026-11-worlds')

# Studio (Brand Worlds Studio design system · feed tokens)
CREAM, CREAM_DEEP, INK, INK_SOFT = '#F2EBDC', '#E7DEC9', '#15202E', '#3D4A5C'
COPPER, COPPER_SOFT, COPPER_TEXT = '#C28A5A', '#D9AE85', '#825630'
FONTS = ('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400'
         '&family=Plus+Jakarta+Sans:wght@500;600&display=swap')
DISPLAY = "'Cormorant Garamond','Frank Ruhl Libre',serif"
LABEL = "'Plus Jakarta Sans','Heebo',sans-serif"

D = 26.5
CH = [(2.6, 5.9), (5.9, 9.3), (9.3, 12.6), (12.6, 16.0), (16.0, 19.3), (19.3, 22.4)]
OUTRO = 22.3


# ───────────────────────── assets ─────────────────────────
class Assets:
    def __init__(self, world):
        self.dir = os.path.join(OUT, world, 'src', 'assets')
        os.makedirs(self.dir, exist_ok=True)

    def img(self, src, name=None, maxw=1280, q=82, trim=False):
        name = name or os.path.splitext(os.path.basename(src))[0] + '.webp'
        dst = os.path.join(self.dir, name)
        if not os.path.exists(dst):
            im = Image.open(os.path.join(ROOT, src))
            im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
            if trim:
                im = im.crop(im.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox())
            if im.width > maxw:
                im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
            im.save(dst, 'WEBP', quality=q)
        return 'assets/' + name

    def seq(self, srcs, sub, maxw=1000):
        os.makedirs(os.path.join(self.dir, sub), exist_ok=True)
        return [self.img(s, f'{sub}/f{i:03d}.webp', maxw, 78) for i, s in enumerate(srcs)]

    def video_seq(self, src, sub, fps, maxw=1000):
        d = os.path.join(self.dir, sub)
        if not os.path.isdir(d) or not os.listdir(d):
            os.makedirs(d, exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(ROOT, src), '-vf', f'fps={fps},scale={maxw}:-2',
                            '-c:v', 'libwebp', '-quality', '78', os.path.join(d, 'f%03d.webp')], check=True)
        return ['assets/%s/%s' % (sub, f) for f in sorted(os.listdir(d))]


# ───────────────────────── pieces ─────────────────────────
def kb_img(fm, src, a, b, pos='50% 50%', z0=1.08, z1=1.0, fit='cover', bg='transparent'):
    """an image shown a→b with a slow push (Ken Burns). Two elements: the wrapper fades, the img moves."""
    return (f'<div style="position:absolute;inset:0;background:{bg};{fm.show(a, b)}">'
            f'<img src="{src}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:{fit};object-position:{pos};'
            f'{fm.kf([(a - .3, f"transform:scale({z0})"), (b + .3, f"transform:scale({z1})")], "linear")}"></div>')


def ball(fm, x0, x1, y, t0, t1, size=96):
    """the studio's copper ball rolling on its copper line, right to left."""
    line = (f'<div style="position:absolute;top:{y + size // 2 - 2}px;left:{x1 + size // 2}px;right:0;height:4px;border-radius:999px;background:{COPPER};'
            f'transform-origin:right;{fm.kf([(t0, "transform:scaleX(0)"), (t1, "transform:scaleX(1)")])}"></div>')
    rot = -(x0 - x1) / (3.1416 * size) * 360
    b = (f'<div style="position:absolute;top:{y}px;left:0;width:{size}px;height:{size}px;'
         f'{fm.kf([(t0, f"transform:translateX({x0}px)"), (t1, f"transform:translateX({x1}px)")])}">'
         f'<div style="position:absolute;inset:-12px;border-radius:999px;background:{COPPER_SOFT};opacity:.45"></div>'
         f'<div style="position:absolute;inset:0;border-radius:999px;overflow:hidden;box-shadow:0 10px 24px rgba(20,30,45,.28);'
         f'background:radial-gradient(circle at 36% 30%,#F4D3B0 0%,{COPPER} 36%,#8A5530 72%,#4E2D16 100%);'
         f'{fm.kf([(t0, "transform:rotate(0deg)"), (t1, f"transform:rotate({rot:.0f}deg)")])}">'
         f'<div style="position:absolute;left:22%;top:16%;width:22%;height:14%;border-radius:999px;background:rgba(255,255,255,.55)"></div></div></div>')
    return line + b


def signature(color=INK_SOFT):
    return (f'<div style="position:absolute;top:64px;left:64px;display:flex;flex-direction:column;gap:2px">'
            f'<span style="font-family:{DISPLAY};font-style:italic;font-size:32px;color:{color}" dir="ltr">Brand Worlds Studio</span>'
            f'<span style="font-size:15px;letter-spacing:.32em;color:{color}">חגית אנטבי</span></div>')


def question(lines, hi, top=190, color=INK):
    html = '<br>'.join(lines).replace(hi, f'<span style="color:{COPPER_TEXT}">{hi}</span>')
    return (f'<div dir="rtl" style="position:absolute;top:{top}px;left:64px;right:64px;text-align:right;font-size:86px;'
            f'font-weight:700;line-height:1.14;color:{color}">{html}</div>')


def price_hook(fm, w, end):
    """'ככה משווים': a no-name product card, never the world's product."""
    g = w['generic']
    t_st = 1.0
    card = (
        f'<div style="position:absolute;top:610px;left:220px;width:640px;height:820px;border-radius:22px;background:#F6F1E7;'
        f'border:1px solid #DCCFB8;transform:rotate(-5deg) translate(-40px,26px)"></div>'
        f'<div style="position:absolute;top:610px;left:220px;width:640px;height:820px;border-radius:22px;background:#FBF8F2;'
        f'border:1px solid #DCCFB8;transform:rotate(3.5deg) translate(30px,14px)"></div>'
        f'<div style="position:absolute;top:600px;left:220px;width:640px;height:820px;'
        f'{fm.kf([(0, "transform:translateY(0)"), (end, "transform:translateY(-14px)")], "linear")}">'
        f'<div style="position:absolute;inset:0;border-radius:22px;background:#FFFFFF;box-shadow:0 30px 70px rgba(20,30,45,.18);overflow:hidden">'
        f'<img src="{g["img"]}" alt="" style="position:absolute;top:20px;left:20px;width:600px;height:650px;object-fit:cover;border-radius:12px;background:#F2F2F2">'
        f'<div dir="rtl" style="position:absolute;bottom:0;left:0;right:0;height:150px;padding:0 34px;display:flex;align-items:center;justify-content:space-between">'
        f'<span style="font-size:32px;color:{INK_SOFT}">{g["name"]}</span>'
        f'<span dir="ltr" style="display:flex;align-items:baseline;gap:14px"><b style="font-size:50px;color:{INK}">{g["price"]}</b>'
        f'<s style="font-size:28px;color:#8A93A0">{g["was"]}</s></span></div>'
        f'<div style="position:absolute;top:44px;right:44px;padding:10px 22px;border-radius:999px;background:{INK};color:{CREAM};font-size:26px;font-weight:500">ככה משווים</div>'
        f'</div>'
        f'<div style="position:absolute;top:-56px;left:-56px;width:170px;height:170px;border-radius:999px;background:{INK};color:{CREAM};'
        f'display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 14px 30px rgba(20,30,45,.3)">'
        f'<span style="font-size:58px;font-weight:700;line-height:1" dir="ltr">30%</span><span style="font-size:24px">הנחה</span></div>'
        f'<div style="position:absolute;bottom:190px;left:-40px;{fm.kf([(t_st - .01, "opacity:0;transform:scale(.4) rotate(-6deg)"), (t_st, "opacity:1;transform:scale(.4) rotate(-6deg)"), (t_st + .22, "opacity:1;transform:scale(1.08) rotate(-6deg)"), (t_st + .36, "opacity:1;transform:scale(1) rotate(-6deg)")])}">'
        f'<div style="padding:16px 28px;border-radius:12px;background:#F7EDC9;color:{INK};font-size:32px;font-weight:600;box-shadow:0 10px 24px rgba(20,30,45,.18)">+ משלוח חינם?</div></div>'
        f'</div>')
    return (f'<div style="position:absolute;inset:0;background:{CREAM_DEEP}">{signature()}'
            f'{question(w["hook"]["lines"], w["hook"]["hi"])}{card}{ball(fm, 1180, 840, 1660, .2, 1.7)}</div>')


def logo_hook(fm, w, end):
    """hidden logo: the world's own product, a copper bar already over the logo at frame 0."""
    h = w['hidden']
    return (f'<div style="position:absolute;inset:0;background:{CREAM}">'
            f'<div style="position:absolute;inset:0;transform-origin:{h["origin"]};{fm.kf([(0, "transform:scale(1.0)"), (end, "transform:scale(1.04)")], "linear")}">'
            f'<img src="{h["img"]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{h["pos"]}">'
            f'<div style="position:absolute;{h["bar"]};border-radius:8px;background:linear-gradient(90deg,#B07848,{COPPER},#B07848);box-shadow:0 6px 16px rgba(20,30,45,.25)"></div></div>'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,{CREAM} 0%,rgba(242,235,220,.92) 17%,rgba(242,235,220,0) 36%)"></div>'
            f'{signature()}{question(w["hook"]["lines"], w["hook"]["hi"])}'
            f'</div>')


def header(fm, w):
    labels = ''.join(
        f'<div style="position:absolute;top:0;right:0;display:flex;align-items:baseline;gap:16px;white-space:nowrap;{fm.show(a, b, .25)}">'
        f'<span style="font-family:{DISPLAY};font-size:46px;line-height:1;opacity:.75">0{i + 1}</span>'
        f'<span style="font-size:36px;font-weight:600">{name}</span></div>'
        for i, ((a, b), name) in enumerate(zip(CH, w['chapters'])))
    return (f'<div dir="rtl" style="position:absolute;top:92px;left:64px;right:64px;height:60px">'
            f'<div style="position:relative;height:60px">{labels}</div>'
            f'<div dir="ltr" style="position:absolute;top:18px;left:0;font-family:{LABEL};font-size:21px;letter-spacing:.14em;opacity:.72">'
            f'{w["no"]} · עולם מותג קונספט · {w["name"]}</div></div>'
            f'<div style="position:absolute;top:172px;left:64px;right:64px;height:1px;background:currentColor;opacity:.22"></div>')


def chapter_text(fm, i, head, sub):
    a, b = CH[i]
    return (f'<div dir="rtl" style="position:absolute;top:1262px;left:64px;right:64px;text-align:right;{fm.window_rise(a + .15, b - .1)}">'
            f'<div style="font-size:68px;font-weight:600;line-height:1.18">{head}</div>'
            f'<div style="margin-top:20px;font-size:33px;line-height:1.45;opacity:.8">{sub}</div></div>')


def browser(fm, w, frames, start, step, url, pos='50% 50%'):
    a, b = CH[1]
    return (f'<div style="position:absolute;inset:0;background:#FBF8F2;{fm.show(a, b)}">'
            f'<div style="position:absolute;top:0;left:0;right:0;height:62px;display:flex;align-items:center;gap:12px;padding:0 26px;border-bottom:1px solid #E4DCCB">'
            f'<i style="width:14px;height:14px;border-radius:99px;background:#D9CFBF"></i><i style="width:14px;height:14px;border-radius:99px;background:#D9CFBF"></i>'
            f'<i style="width:14px;height:14px;border-radius:99px;background:#D9CFBF"></i>'
            f'<span style="margin-left:18px;padding:6px 22px;border-radius:999px;background:#EFE8DA;font-family:{LABEL};font-size:19px;color:{INK_SOFT}">{url}</span></div>'
            f'<div style="position:absolute;top:62px;left:0;right:0;bottom:0;overflow:hidden">{fm.seq(frames, start, step, pos=pos)}</div></div>')


def feed(fm, w, slides, line_color):
    """06 · the feed: a carousel advancing right to left with one continuous line through every slide."""
    a, b = CH[5]
    sw, gap = 600, 40
    n = len(slides)
    total = n * sw + (n - 1) * gap
    items = ''.join(f'<div style="position:absolute;top:0;right:{i * (sw + gap)}px;width:{sw}px;height:760px;border-radius:18px;overflow:hidden;'
                    f'box-shadow:0 18px 40px rgba(0,0,0,.25)"><img src="{s}" alt="" style="width:100%;height:100%;object-fit:cover;display:block"></div>'
                    for i, s in enumerate(slides))
    # one wave through all slides
    pts = []
    for i in range(n * 2 + 1):
        x = total - i * (total / (n * 2))
        y = 560 + (60 if i % 2 else -40)
        pts.append((x, y))
    d = f'M{pts[0][0]:.0f},{pts[0][1]}' + ''.join(
        f' Q{(pts[i - 1][0] + pts[i][0]) / 2:.0f},{pts[i - 1][1] + (90 if i % 2 else -90)} {pts[i][0]:.0f},{pts[i][1]}' for i in range(1, len(pts)))
    svg = (f'<svg width="{total}" height="760" viewBox="0 0 {total} 760" style="position:absolute;top:0;right:0;overflow:visible" aria-hidden="true">'
           f'<path d="{d}" fill="none" stroke="{line_color}" stroke-width="5" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" '
           f'style="{fm.kf([(a, "stroke-dashoffset:-1"), (b - .3, "stroke-dashoffset:0")], "linear")}"/></svg>')
    # first slide centred, then the strip slides right (RTL carousel advancing) by ~2.6 slides
    x0 = -(1080 - sw) // 2 + 64 - 64
    shift = 2.6 * (sw + gap)
    strip = (f'<div style="position:absolute;top:120px;right:{(952 - sw) // 2}px;width:{total}px;height:760px;'
             f'{fm.kf([(a, "transform:translateX(0)"), (b, f"transform:translateX({shift:.0f}px)")], "cubic-bezier(.45,.05,.4,1)")}">'
             f'<div style="position:absolute;top:0;right:0;width:{total}px;height:760px">{items}</div>{svg}</div>')
    return f'<div style="position:absolute;inset:0;{fm.show(a, b)}">{strip}</div>'


def outro(fm, w, start):
    o = w['outro']
    name = w['name']
    if o.get('logo'):  # hidden-logo world: the same picture as the hook, the bar slides off
        h = w['hidden']
        img = (f'<img src="{h["img"]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{h["pos"]}">'
               f'<div style="position:absolute;{h["bar"]}"><div style="position:absolute;inset:0;border-radius:8px;transform-origin:right;'
               f'background:linear-gradient(90deg,#B07848,{COPPER},#B07848);{fm.kf([(start + .6, "transform:scaleX(1)"), (start + 1.2, "transform:scaleX(0)")])}"></div></div>')
    else:
        img = (f'<img src="{o["img"]}" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{o["pos"]};'
               f'{fm.kf([(start, "transform:scale(1.06)"), (D, "transform:scale(1)")], "linear")}">')
    head = ''.join(f'<div>{l}</div>' for l in o['head'])
    if o.get('hi'):
        head += f'<div style="color:{COPPER};font-size:104px;line-height:1.05">{o["hi"]}</div>'
    return (f'<div style="position:absolute;inset:0;background:{CREAM};{fm.show(start, D, .35)}">'
            f'<div style="position:absolute;inset:0;overflow:hidden">{img}</div>'
            f'<div style="position:absolute;top:0;left:0;right:0;height:900px;background:linear-gradient(180deg,{CREAM} 0%,rgba(242,235,220,.92) 45%,rgba(242,235,220,0) 100%)"></div>'
            f'<div dir="rtl" style="position:absolute;top:150px;left:64px;right:64px;text-align:right;color:{INK}">'
            f'<div style="font-size:86px;font-weight:700;line-height:1.14;{fm.rise(start + .3)}">{head}</div>'
            f'<div style="margin-top:22px;font-size:42px;line-height:1.35;color:{COPPER_TEXT};{fm.rise(start + .8)}">{o["sub"]}</div></div>'
            f'<div style="position:absolute;left:0;right:0;bottom:0;height:470px;background:{CREAM};{fm.kf([(start + 1.5, "transform:translateY(470px)"), (start + 2.1, "transform:none")])}">'
            f'<div dir="rtl" style="position:absolute;top:56px;left:64px;right:64px;display:flex;flex-direction:column;align-items:center;gap:28px;text-align:center">'
            f'<div style="font-size:44px;font-weight:500;color:{INK}"><span dir="ltr">{name}</span> לא קיים. העסק שלך כן.</div>'
            f'<div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:24px 64px;border-radius:12px;background:{INK};color:{CREAM}">'
            f'<span style="font-size:40px;font-weight:600">אבחון פער המותג</span><span style="font-size:24px;opacity:.85">30 דק׳ · בלי עלות</span></div>'
            f'<div dir="ltr" style="font-family:{LABEL};font-size:22px;letter-spacing:.32em;color:{INK_SOFT}">HAGITANTEBI.CO.IL</div></div></div>'
            f'</div>')


PAGE = """<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="{fonts}">
<style>
html,body{{margin:0;background:{cream}}}
body{{font-family:'Heebo',sans-serif}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.film *{{animation-duration:{dur}s;animation-iteration-count:1;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
i{{display:block}}
{css}
</style></head>
<body><div id="stage" class="film">{body}</div></body></html>"""


def page(title, dur, fm, body):
    return PAGE.format(title=title, fonts=FONTS.replace('&', '&amp;'), cream=CREAM, dur=dur, css=fm.style(), body=body)


def build(world, cfg_fn):
    A = Assets(world)
    w = cfg_fn(A)
    src = os.path.join(OUT, world, 'src')

    # ── the full reel ──
    fm = Film(D)
    hook = price_hook if w['hook']['type'] == 'price' else logo_hook
    body = []
    # world plane (chapters)
    c = w['color']
    plane = [header(fm, w)]
    card = [f'<div style="position:absolute;inset:0;background:{c["card"]}"></div>']
    card += w['scenes'](fm, A)
    plane.append(f'<div style="position:absolute;top:212px;left:64px;width:952px;height:1000px;border-radius:24px;overflow:hidden;'
                 f'box-shadow:0 24px 60px rgba(0,0,0,.22)">{"".join(card)}</div>')
    plane += [chapter_text(fm, i, h, s) for i, (h, s) in enumerate(w['texts'])]
    plane.append(f'<div dir="ltr" style="position:absolute;top:1600px;left:-40px;right:-40px;text-align:center;font-family:{DISPLAY};font-size:330px;'
                 f'line-height:1;letter-spacing:.05em;white-space:nowrap;opacity:.08">{w["ghost"]}</div>')
    body.append(f'<div style="position:absolute;inset:0;background:{c["plane"]};color:{c["text"]};{fm.show(2.45, OUTRO + .5, .2)}">{"".join(plane)}</div>')
    body.append(f'<div style="position:absolute;inset:0;{fm.show(0, 2.6, .3)}">{hook(fm, w, 2.9)}</div>')
    body.append(outro(fm, w, OUTRO))
    open(os.path.join(src, 'reel.html'), 'w', encoding='utf-8').write(page(f'{w["name"]} · hidden logo reel', D, fm, ''.join(body)))

    # ── the 3s hook clip ──
    fh = Film(3.0)
    open(os.path.join(src, 'hook.html'), 'w', encoding='utf-8').write(
        page(f'{w["name"]} · hook', 3.0, fh, f'<div style="position:absolute;inset:0">{hook(fh, w, 3.0)}</div>'))
    print('built', world)


if __name__ == '__main__':
    from worlds import WORLDS
    names = sys.argv[1:] or list(WORLDS)
    for n in names:
        build(n, WORLDS[n])
