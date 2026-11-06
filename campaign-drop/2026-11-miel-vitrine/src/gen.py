#!/usr/bin/env python3
"""MIEL° · La Vitrine — studio-mode "live screen" reel (9:16, 18s).

Hook A: "נכנסות לאתר שלך, ולא קונות?" over a generic cake shop that the cursor scrolls past.
Then the studio window opens on a laptop on MIEL's marble table: the real vitrine section, a hand drags
La Rose into the bag (the slice turns into the whole cake over the bag), four quick drags follow, and
every bag steps out of the screen onto the table — five bags, each side carrying its own cut.
Checkout: the flip clock turns to 10:30. Outro answers the hook + comment CTA.

All timing is in seconds on one CSS timeline; render with
  node .claude/skills/brandos-brand-world-reel/scripts/render.js reel.html 18 <out>
"""
import os

D = 18.0
HERE = os.path.dirname(os.path.abspath(__file__))
css = []


def P(t):
    return f"{max(0.0, min(D, t)) / D * 100:.3f}%"


def kf(name, frames):
    """frames: [(t, 'css decls')] in time order; holds the first/last state to 0%/100%."""
    fr = list(frames)
    if fr[0][0] > 0:
        fr.insert(0, (0, fr[0][1]))
    if fr[-1][0] < D:
        fr.append((D, fr[-1][1]))
    css.append("@keyframes %s{%s}" % (name, "".join("%s{%s}" % (P(t), c) for t, c in fr)))
    return name


def win(name, a, b, fade=.18):
    """opacity window a..b"""
    fr = []
    if a > 0:
        fr += [(max(0, a - fade), "opacity:0"), (a, "opacity:1")]
    else:
        fr += [(0, "opacity:1")]
    if b < D:
        fr += [(b, "opacity:1"), (min(D, b + fade), "opacity:0")]
    return kf(name, fr)


# ── MIEL data (same codes as the site's bagSVG) ─────────────────────────────
CAKES = {
    "rose":     dict(he="הוורודה",   fr="La Rose",     whole="sig-rose.webp",     code=("#EBCB9C", "#B8243F", "#EDBABD"), line="ביסקוויט וניל · לב פטל · רובּ ורוד־אומברה"),
    "cacao":    dict(he="השוקולדית", fr="Le Cacao",    whole="sig-chocolat.webp", code=("#6B4231", "#C98A4B", "#4A2C24"), line="ביסקוויט שוקולד · לב קרמל · רובּ שוקולד"),
    "citron":   dict(he="הלימונית",  fr="Le Citron",   whole="sig-citron.webp",   code=("#EBCB9C", "#EFD77A", "#F1E1A6"), line="ביסקוויט וניל · קרם לימון · רובּ לימון מסורק"),
    "pistache": dict(he="הפיסטוקית", fr="La Pistache", whole="sig-pistache.webp", code=("#EBCB9C", "#A3B06E", "#C9CCA3"), line="ביסקוויט וניל · קרם פיסטוק · רובּ פיסטוק"),
    "fleurs":   dict(he="הפרחונית",  fr="Les Fleurs",  whole="sig-fleurs.webp",   code=("#EBCB9C", "#F7EEDC", "#F2E7D8"), line="ביסקוויט וניל · לב קרם וניל · רובּ שמנת"),
}
uid = [0]


def bag_svg(cid, w):
    s, h, r = CAKES[cid]["code"]
    k = "c%d" % uid[0]; uid[0] += 1
    y, layers = 62, ""
    for kind, hh in [("s", 20), ("h", 5)] * 5 + [("s", 30)]:
        layers += '<rect x="138" y="%d" width="44" height="%.1f" fill="%s"/>' % (y, hh + .6, s if kind == "s" else h)
        y += hh
    return ('<svg viewBox="0 0 200 230" width="%d" height="%d" style="display:block;overflow:visible">'
            '<defs><clipPath id="%s"><path d="M140 62 L178 50 L178 208 L140 222z"/></clipPath></defs>'
            '<path d="M50 64c0-36 12-52 26-52s26 16 26 52" fill="none" stroke="#C8344F" stroke-width="6" stroke-linecap="round"/>'
            '<path d="M88 64c0-36 12-52 26-52s26 16 26 52" fill="none" stroke="#B02A44" stroke-width="6" stroke-linecap="round"/>'
            '<path d="M20 62h120v160H20z" fill="#F4ECE0" stroke="rgba(74,44,36,.10)"/>'
            '<g clip-path="url(#%s)"><rect x="138" y="46" width="44" height="180" fill="%s"/>%s<rect x="138" y="46" width="44" height="180" fill="rgba(0,0,0,.06)"/></g>'
            '<text x="80" y="148" text-anchor="middle" font-family="Cormorant Garamond,Georgia,serif" font-weight="600" font-size="19" letter-spacing="4" fill="#B8956A">MIEL°</text>'
            '</svg>') % (w, round(w * 230 / 200), k, k, r, layers)


def hand(closed):
    """macOS-like grab cursor, white with a dark outline (shapes drawn twice: outline, then fill)."""
    if closed:
        shapes = ('<rect x="8" y="12" width="18" height="16" rx="6"/>'
                  '<rect x="9" y="9" width="4.2" height="8" rx="2.1"/><rect x="13" y="8" width="4.2" height="8" rx="2.1"/>'
                  '<rect x="17" y="8" width="4.2" height="8" rx="2.1"/><rect x="21" y="9.5" width="4.2" height="8" rx="2.1"/>'
                  '<rect x="4.5" y="15" width="8" height="4.4" rx="2.2" transform="rotate(25 8.5 17)"/>')
    else:
        shapes = ('<rect x="8" y="13" width="18" height="15" rx="6"/>'
                  '<rect x="9" y="5" width="4.2" height="13" rx="2.1"/><rect x="13" y="2.5" width="4.2" height="14" rx="2.1"/>'
                  '<rect x="17" y="3" width="4.2" height="14" rx="2.1"/><rect x="21" y="6" width="4.2" height="12" rx="2.1"/>'
                  '<rect x="2.5" y="14" width="10" height="4.4" rx="2.2" transform="rotate(35 7.5 16)"/>')
    return ('<svg viewBox="0 0 32 32" width="64" height="64" style="display:block;overflow:visible">'
            '<g fill="#1d1d1f" stroke="#1d1d1f" stroke-width="2.6" stroke-linejoin="round">%s</g>'
            '<g fill="#fff">%s</g></svg>') % (shapes, shapes)


# ── timeline ────────────────────────────────────────────────────────────────
HOOK_OUT = 2.5
WORLD_OPEN, WORLD_FULL = 3.95, 4.55
WORLD_CLOSE, WORLD_SMALL = 15.2, 15.75

# page coords (1280×800 page, shown at .75 inside a 960×600 screen)
SPOT = {"rose": (212, 335), "fleurs": (442, 330), "cacao": (682, 318), "citron": (879, 308), "pistache": (1082, 302)}
DROP = (640, 668)
# drags: (cake, hover, grab, release)
DRAGS = [("rose", 5.55, 5.85, 7.45), ("cacao", 8.25, 8.32, 8.78), ("citron", 9.1, 9.17, 9.63),
         ("pistache", 9.95, 10.02, 10.48), ("fleurs", 10.8, 10.87, 11.33)]
SLOT_X = [860, 700, 540, 380, 220]          # table, filled right → left
CART_CLICK, PLUS_CLICK, BTN_CLICK, BTN_DONE = 13.3, 14.0, 14.5, 14.85

# cursor path
cur = [(4.6, (1360, 760)), (5.55, SPOT["rose"]), (5.85, SPOT["rose"]), (6.7, (430, 625)), (7.45, DROP), (7.7, DROP)]
for cid, hv, gr, rl in DRAGS[1:]:
    cur += [(hv, SPOT[cid]), (gr, SPOT[cid]), (rl, DROP), (rl + .12, DROP)]
cur += [(12.3, (95, 765)), (CART_CLICK, (95, 765)), (13.85, (975, 366)), (PLUS_CLICK + .1, (975, 366)),
        (14.4, (806, 445)), (15.0, (806, 445))]
kf("cur", [(t, "transform:translate(%dpx,%dpx)" % (x - 22, y - 18)) for t, (x, y) in cur])
win("curop", 4.75, 15.05)
closed_windows = [(gr, rl) for _, _, gr, rl in DRAGS]
# closed hand also flashes on clicks
closed_windows += [(CART_CLICK - .05, CART_CLICK + .12), (PLUS_CLICK - .05, PLUS_CLICK + .12), (BTN_CLICK - .05, BTN_CLICK + .12)]
fr = [(0, "opacity:0")]
for a, b in closed_windows:
    fr += [(a - .01, "opacity:0"), (a, "opacity:1"), (b, "opacity:1"), (b + .01, "opacity:0")]
kf("closed", fr)
fr = [(0, "opacity:1")]
for a, b in closed_windows:
    fr += [(a - .01, "opacity:1"), (a, "opacity:0"), (b, "opacity:0"), (b + .01, "opacity:1")]
kf("open", fr)

# ghosts (one per drag) follow the cursor, the slice turns into the whole cake over the bag
ghost_html = ""
for i, (cid, hv, gr, rl) in enumerate(DRAGS):
    sx, sy = SPOT[cid]
    path = [(gr, (sx, sy))] + ([(6.7, (430, 625))] if i == 0 else []) + [(rl, DROP)]

    def tr(x, y, s):
        return "transform:translate(%dpx,%dpx) scale(%.2f)" % (x - 70, y - 80, s)
    fr = [(gr - .01, tr(sx, sy, .7) + ";opacity:0"), (gr, tr(sx, sy, .7) + ";opacity:1"), (gr + .14, tr(sx, sy - 14, 1.05) + ";opacity:1")]
    fr += [(t, tr(x, y, 1) + ";opacity:1") for t, (x, y) in path[1:]]
    fr += [(rl + .26, tr(DROP[0], DROP[1] + 6, .25) + ";opacity:0")]
    kf("gh%d" % i, fr)
    swap = rl - (.5 if i == 0 else .16)
    kf("gw%d" % i, [(swap, "opacity:0"), (swap + .14, "opacity:1")])
    c = CAKES[cid]
    ghost_html += ('<div class="ghost" style="animation-name:gh%d"><img class="gslice" src="assets/slice-%s.webp" alt="">'
                   '<img class="gwhole" style="animation-name:gw%d" src="assets/%s" alt=""></div>') % (i, cid, i, c["whole"])

# hover ring on the slice
ring_html = ""
for i, (cid, hv, gr, rl) in enumerate(DRAGS):
    x, y = SPOT[cid]
    win("rg%d" % i, hv - .12, gr + .25, .1)
    ring_html += '<div class="ring" style="left:%dpx;top:%dpx;animation-name:rg%d"></div>' % (x - 92, y - 175, i)

# dock: rises with the first grab, bag code changes per drag, bounces on each drop
kf("dock", [(5.85, "transform:translateY(250px)"), (6.3, "transform:none"), (12.1, "transform:none"), (12.5, "transform:translateY(250px)")])
dock_bags = ""
for i, (cid, hv, gr, rl) in enumerate(DRAGS):
    a = 0 if i == 0 else gr
    b = DRAGS[i + 1][2] if i + 1 < len(DRAGS) else D
    win("db%d" % i, a, b, .06)
    dock_bags += '<div class="stack0" style="animation-name:db%d">%s</div>' % (i, bag_svg(cid, 120))
fr = [(0, "transform:none")]
for _, _, gr, rl in DRAGS:
    fr += [(rl + .2, "transform:none"), (rl + .32, "transform:translateY(6px) scaleY(.94)"), (rl + .46, "transform:translateY(-4px)"), (rl + .56, "transform:none")]
kf("dockb", fr)
kf("dockhot", [(0, "transform:none")] + sum([[(rl - .3, "transform:none"), (rl - .15, "transform:scale(1.12)"), (rl + .1, "transform:scale(1.12)"), (rl + .22, "transform:none")] for _, _, _, rl in DRAGS], []))

# counter info follows the grabbed cake
info_html = ""
for i, (cid, hv, gr, rl) in enumerate(DRAGS):
    a = 0 if i == 0 else gr
    b = DRAGS[i + 1][2] if i + 1 < len(DRAGS) else D
    win("ci%d" % i, a, b, .08)
    c = CAKES[cid]
    info_html += ('<div class="cinfo" style="animation-name:ci%d"><img class="loupe" src="assets/slice-%s.webp" alt="">'
                  '<span class="arrow">←</span><img class="whole" src="assets/%s" alt="">'
                  '<div class="ctext"><div class="cname">%s <small>%s</small></div><div class="cline">%s</div><div class="cprice">₪ 290 <small>עוגה שלמה</small></div></div></div>') % (
        i, cid, c["whole"], c["he"], c["fr"], c["line"])

# cart bar
win("cart", 7.75, D, .2)
cart_txt = ["עוגה אחת בשקית · ₪ 290", "2 עוגות בשקיות · ₪ 580", "3 עוגות בשקיות · ₪ 870", "4 עוגות בשקיות · ₪ 1,160", "5 עוגות בשקיות · ₪ 1,450"]
cart_html = ""
for i, (_, _, _, rl) in enumerate(DRAGS):
    a = rl + .3
    b = DRAGS[i + 1][3] + .3 if i + 1 < len(DRAGS) else D
    win("ct%d" % i, a, b, .05)
    cart_html += '<span class="ctx" style="animation-name:ct%d">%s</span>' % (i, cart_txt[i])
kf("cartbtn", [(CART_CLICK - .06, "transform:none"), (CART_CLICK, "transform:scale(.92)"), (CART_CLICK + .14, "transform:none")])

# checkout modal on the screen
kf("modal", [(CART_CLICK + .1, "opacity:0;transform:translateY(14px) scale(.97)"), (CART_CLICK + .4, "opacity:1;transform:none")])
win("veil", CART_CLICK + .4, D, .28)
win("t1015", 0, PLUS_CLICK + .05, .01)
win("t1030", PLUS_CLICK + .05, D, .01)
kf("flipd", [(PLUS_CLICK + .05, "transform:rotateX(90deg)"), (PLUS_CLICK + .35, "transform:none")])
win("bt0", 0, BTN_CLICK, .05)
win("bt1", BTN_CLICK, BTN_DONE, .05)
win("bt2", BTN_DONE, D, .08)

# bags step out of the screen onto the table (world coords; dock bag ≈ (540, 1281) on the stage)
table_html = ""
for i, (cid, hv, gr, rl) in enumerate(DRAGS):
    sx = SLOT_X[i]
    t0 = rl + .08
    dx, dy = 540 - sx, 1281 - 1634
    kf("tb%d" % i, [(t0 - .01, "opacity:0;transform:translate(%dpx,%dpx) scale(.6)" % (dx, dy)),
                    (t0, "opacity:1;transform:translate(%dpx,%dpx) scale(.6)" % (dx, dy)),
                    (t0 + .26, "opacity:1;transform:translate(%dpx,%dpx) scale(.86)" % (dx * .42, -330)),
                    (t0 + .52, "opacity:1;transform:none"),
                    (t0 + .62, "opacity:1;transform:scaleY(.95)"),
                    (t0 + .72, "opacity:1;transform:none")])
    win("ts%d" % i, t0 + .5, D, .12)
    table_html += ('<div class="tshadow" style="left:%dpx;animation-name:ts%d"></div>'
                   '<div class="tbag" style="left:%dpx;animation-name:tb%d">%s</div>') % (sx - 70, i, sx - 75, i, bag_svg(cid, 150))

# camera: push in on the first drag, back out for the table
kf("cam", [(4.5, "transform:scale(1)"), (5.5, "transform:scale(1.28)"), (15.2, "transform:scale(1.31)")])

# studio wrapper
kf("hook", [(HOOK_OUT - .05, "opacity:1"), (HOOK_OUT + .15, "opacity:0")])
kf("scroll", [(.35, "transform:none"), (1.15, "transform:translateY(-250px)"), (1.35, "transform:translateY(-250px)"), (2.1, "transform:translateY(-470px)")])
kf("hcur", [(0, "transform:translate(520px,560px)"), (.35, "transform:translate(520px,560px)"), (1.15, "transform:translate(540px,470px)"),
            (1.35, "transform:translate(540px,470px)"), (2.1, "transform:translate(560px,380px)"), (2.45, "transform:translate(860px,180px)")])
kf("ln0", [(.3, "stroke-dashoffset:1"), (2.3, "stroke-dashoffset:0")])
kf("bl0", [(.25, "offset-distance:0%;opacity:0"), (.3, "offset-distance:0%;opacity:1"), (2.3, "offset-distance:100%;opacity:1"), (2.45, "offset-distance:100%;opacity:0")])
kf("rl0", [(.3, "transform:rotate(0deg)"), (2.3, "transform:rotate(-400deg)")])
kf("world", [(2.45, "opacity:0;transform:translateY(60px) scale(.5)"), (2.8, "opacity:1;transform:scale(.5)"), (WORLD_OPEN, "opacity:1;transform:scale(.5)"),
             (WORLD_FULL, "opacity:1;transform:scale(1)"), (WORLD_CLOSE, "opacity:1;transform:scale(1)"), (WORLD_SMALL, "opacity:1;transform:scale(.5)")])
kf("marks", [(2.65, "opacity:0"), (2.9, "opacity:1"), (WORLD_OPEN, "opacity:1"), (4.2, "opacity:0"), (WORLD_SMALL - .15, "opacity:0"), (WORLD_SMALL + .1, "opacity:1")])
kf("intro", [(2.5, "opacity:0"), (2.75, "opacity:1"), (WORLD_OPEN, "opacity:1"), (4.25, "opacity:0")])
for n, t in [("i1", 2.6), ("i2", 2.75), ("i3", 2.95)]:
    kf(n, [(t, "opacity:0;transform:translateY(24px)"), (t + .35, "opacity:1;transform:none")])
kf("outro", [(WORLD_CLOSE + .2, "opacity:0"), (WORLD_SMALL, "opacity:1")])
for n, t in [("o1", 15.55), ("o2", 15.75), ("o3", 16.15)]:
    kf(n, [(t, "opacity:0;transform:translateY(26px)"), (t + .4, "opacity:1;transform:none")])
kf("hud", [(4.6, "opacity:0;transform:translateY(-16px)"), (4.95, "opacity:1;transform:none"), (14.95, "opacity:1;transform:none"), (15.2, "opacity:0")])
kf("ov", [(4.7, "opacity:0;transform:translateY(30px)"), (5.15, "opacity:1;transform:none"), (14.95, "opacity:1;transform:none"), (15.2, "opacity:0")])
kf("ov2", [(11.9, "opacity:0;transform:translateY(24px)"), (12.3, "opacity:1;transform:none"), (14.95, "opacity:1;transform:none"), (15.2, "opacity:0")])

# ── generic shop for the hook (frame 0 shows it complete) ───────────────────
names = ["עוגת וניל", "עוגת שמנת", "עוגה לבנה", "עוגת יום הולדת", "עוגת קרם", "עוגת פירות", "עוגת וניל גדולה", "עוגה קלאסית"]
cards = "".join('<div class="gcard"><img src="assets/generic-cake.jpg" alt=""><div class="gn">%s</div>'
                '<div class="gp"><span>₪ 290</span><button>הוספה לסל</button></div></div>' % n for n in names)

ARROW = ('<svg viewBox="0 0 20 28" width="44" height="62" style="display:block;overflow:visible">'
         '<path d="M1 1 L1 22 L6.5 16.8 L10.5 26 L14 24.6 L10.2 15.6 L17.5 15.6 Z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>')

BALL = ('<div class="ball" style="offset-path:path(\'M1140 1700 H540\');animation-name:bl0"><div class="halo"></div><div class="sph">'
        '<div class="rl" style="animation-name:rl0"><div style="position:absolute;left:13px;top:13px;width:52px;height:52px;border-radius:50%;border:1px solid rgba(250,228,200,.65)"></div>'
        '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:\'Cormorant Garamond\',serif;font-size:21px;color:#F5DEC4" dir="ltr">BW</div>'
        '<div style="position:absolute;left:12px;top:46px;width:14px;height:14px;border-radius:50%;background:#FFF7EC;box-shadow:0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>')

html = f"""<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>MIEL° La Vitrine — reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&amp;family=Heebo:wght@300;400;500;600;700;800&amp;family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Assistant:wght@400;600;700&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">
<style>
:root{{--s-bg:#FAF8F3;--s-cream:#EEE6D8;--s-ink:#6B563F;--s-copper:#C4765A;--s-gold:#B8894A;--s-dark:#3E2F25;
  --poudre:#F3E4DF;--creme:#F6EADF;--rose:#C98989;--cacao:#4A2C24;--or:#B8956A;--or-soft:rgba(184,149,106,.45);--line:rgba(74,44,36,.14)}}
html,body{{margin:0;background:var(--s-bg)}}
body{{font-family:'Heebo',sans-serif;color:var(--s-dark)}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--s-bg)}}
.film *{{animation-duration:{D:g}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
.stack0{{position:absolute;left:0;top:0}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}}
img{{display:block}}

/* studio wrapper */
.world{{animation-name:world;transform-origin:50% 46%}}
.marks{{animation-name:marks}} .intro{{animation-name:intro}} .outro{{animation-name:outro}}
.i1{{animation-name:i1}}.i2{{animation-name:i2}}.i3{{animation-name:i3}}.o1{{animation-name:o1}}.o2{{animation-name:o2}}.o3{{animation-name:o3}}
.hud{{animation-name:hud}}
.progress{{animation-name:prog;animation-timing-function:linear;transform-origin:right}}
@keyframes prog{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}

/* hook */
.hook{{animation-name:hook}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round;stroke-dasharray:1 1;animation-name:ln0;animation-timing-function:linear}}
.ball{{position:absolute;left:0;top:0;width:104px;height:104px;offset-rotate:0deg;animation-timing-function:linear}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}
.rl{{position:absolute;inset:0;animation-timing-function:linear}}
.shop{{position:absolute;top:610px;left:150px;width:780px;height:960px;background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(62,47,37,.18)}}
.sbar{{height:58px;background:#EFEDEA;display:flex;align-items:center;gap:10px;padding:0 22px;direction:ltr}}
.sbar i{{width:14px;height:14px;border-radius:50%;background:#D5D1CC}}
.sbar span{{margin-left:18px;flex:1;height:32px;border-radius:16px;background:#fff;font:400 18px 'Heebo';color:#8a8580;display:flex;align-items:center;padding:0 16px}}
.shead{{height:86px;display:flex;align-items:center;justify-content:space-between;padding:0 30px;border-bottom:1px solid #eee;font-size:30px;font-weight:600;color:#2E2A27}}
.shead small{{font-size:22px;font-weight:400;color:#6E6660;border:1px solid #ddd;border-radius:999px;padding:4px 16px}}
.sgrid{{position:absolute;top:144px;left:0;right:0;bottom:0;overflow:hidden}}
.sgrid .in{{animation-name:scroll;display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:24px 30px}}
.gcard{{border:1px solid #eee;border-radius:14px;overflow:hidden;background:#fff}}
.gcard img{{width:100%;height:250px;object-fit:cover}}
.gn{{font-size:24px;color:#2E2A27;padding:12px 16px 2px}}
.gp{{display:flex;justify-content:space-between;align-items:center;padding:6px 16px 16px;font-size:22px;color:#2E2A27;font-weight:600}}
.gp button{{font:400 18px 'Heebo';border:1px solid #ccc;background:#fafafa;border-radius:8px;padding:6px 12px;color:#555}}
.hcur{{position:absolute;left:150px;top:610px;animation-name:hcur}}

/* world: MIEL table + laptop */
.cam{{position:absolute;inset:0;animation-name:cam;transform-origin:540px 1150px}}
.lid{{position:absolute;left:40px;top:760px;width:1000px;height:640px;box-sizing:border-box;padding:20px;background:#1b1b1d;border-radius:30px 30px 8px 8px;
  box-shadow:0 0 0 2px #3a3a3e inset,0 40px 60px -20px rgba(60,30,30,.45)}}
.lid::before{{content:"";position:absolute;top:8px;left:50%;width:8px;height:8px;margin-left:-4px;border-radius:50%;background:#333}}
.base{{position:absolute;left:-10px;top:1396px;width:1100px;height:34px;background:linear-gradient(180deg,#e9e7ea,#bdbbc0 70%,#8d8b90);border-radius:4px 4px 30px 30px;box-shadow:0 26px 30px -12px rgba(60,30,30,.4)}}
.base::before{{content:"";position:absolute;top:0;left:50%;width:180px;margin-left:-90px;height:12px;border-radius:0 0 12px 12px;background:#a9a7ac}}
.scr{{position:relative;width:960px;height:600px;overflow:hidden;border-radius:6px;background:var(--creme)}}
.page{{position:absolute;left:0;top:0;width:1280px;height:800px;transform:scale(.75);transform-origin:0 0;background:linear-gradient(180deg,var(--creme),var(--poudre));font-family:'Assistant',sans-serif;color:var(--cacao)}}
.pnav{{height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;background:rgba(247,238,234,.95);border-bottom:1px solid var(--line);direction:rtl}}
.plogo{{font-family:'Cormorant Garamond',serif;font-weight:600;letter-spacing:.22em;font-size:19px;direction:ltr}}
.plogo b{{color:var(--or)}}
.pmenu{{display:flex;gap:26px;font-size:16px;opacity:.8}}
.ppill{{background:var(--cacao);color:var(--creme);border-radius:999px;padding:8px 18px;font-size:15px;font-weight:600}}
.phead{{position:absolute;top:70px;right:40px;left:40px;direction:rtl}}
.peb{{font-size:12px;letter-spacing:.2em;font-weight:600;color:var(--or)}}
.ph2{{font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:36px;line-height:1.1;margin-top:4px}}
.ph2 b{{font-weight:500;color:var(--rose)}}
.pvit{{position:absolute;left:40px;top:160px;width:1200px;height:447px;border-radius:18px;overflow:hidden;border:2px solid var(--or-soft);box-shadow:0 24px 40px -26px rgba(74,44,36,.45)}}
.pvit img{{width:100%;height:100%}}
.tag{{position:absolute;transform:translateX(-50%);background:rgba(251,244,238,.94);border:1px solid var(--or-soft);border-radius:8px;padding:2px 10px 3px;font-size:12px;line-height:1.2;text-align:center;white-space:nowrap}}
.tag b{{display:block;font-family:'Cormorant Garamond',serif;font-weight:600;font-size:14px}}
.dot{{position:absolute;width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:#fff;box-shadow:0 0 0 6px rgba(255,255,255,.35)}}
.ring{{position:absolute;width:184px;height:290px;border-radius:16px;box-shadow:0 0 0 3px var(--or) inset;background:rgba(255,255,255,.16)}}
.pnote{{position:absolute;top:618px;left:0;right:0;text-align:center;font-size:13px;opacity:.72;direction:rtl}}
.pcount{{position:absolute;left:40px;right:40px;top:646px;height:200px;background:#FBF4EE;border:1px solid var(--or-soft);border-radius:22px}}
.cinfo{{position:absolute;inset:0;direction:rtl;display:flex;align-items:center;gap:22px;padding:0 28px}}
.loupe{{width:118px;height:118px;object-fit:cover;border-radius:50%;border:3px solid #fff;box-shadow:0 0 0 1px var(--or-soft)}}
.arrow{{font-family:'Cormorant Garamond',serif;font-size:30px;color:var(--or)}}
.whole{{height:130px;width:auto}}
.ctext{{flex:1}}
.cname{{font-family:'Frank Ruhl Libre',serif;font-size:30px;line-height:1.1}}
.cname small{{font-family:'Cormorant Garamond',serif;font-size:18px;color:var(--or)}}
.cline{{font-size:14px;opacity:.85;margin-top:4px}}
.cprice{{font-family:'Cormorant Garamond',serif;font-size:24px;font-weight:600;margin-top:4px}}
.cprice small{{font-family:'Assistant';font-size:12px;font-weight:400;opacity:.7}}
.dock{{position:absolute;left:530px;top:566px;width:220px;height:240px;box-sizing:border-box;padding:14px 0 0;background:rgba(251,244,238,.97);border:1px solid var(--or-soft);border-bottom:0;border-radius:24px 24px 0 0;box-shadow:0 -20px 40px -24px rgba(74,44,36,.45);animation-name:dock;text-align:center}}
.dockhot{{position:relative;width:120px;height:138px;margin:0 auto;animation-name:dockhot}}
.dockb{{position:absolute;inset:0;animation-name:dockb;transform-origin:50% 100%}}
.dock span{{display:block;font-size:13px;font-weight:600;color:var(--or);margin-top:6px;direction:rtl}}
.cartbar{{position:absolute;left:40px;top:740px;width:400px;height:50px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;background:#fff;border:1px solid var(--line);border-radius:999px;padding:0 6px 0 0;padding-inline-start:18px;direction:rtl;font-size:15px;box-shadow:0 16px 30px -18px rgba(74,44,36,.45);animation-name:cart}}
.ctxw{{position:relative;flex:1;height:22px}}
.ctx{{position:absolute;right:0;top:0;white-space:nowrap}}
.cbtn{{background:var(--cacao);color:var(--creme);border-radius:999px;padding:9px 20px;font-weight:600;animation-name:cartbtn;margin-left:-0px}}
.ghost{{position:absolute;left:0;top:0;width:140px;height:160px}}
.ghost img{{position:absolute;inset:0;width:100%;height:100%}}
.gslice{{object-fit:cover;border:3px solid #fff;border-radius:18px;box-sizing:border-box;box-shadow:0 18px 26px -8px rgba(74,44,36,.4)}}
.gwhole{{object-fit:contain;filter:drop-shadow(0 18px 18px rgba(74,44,36,.35))}}
.pcur{{position:absolute;left:0;top:0;animation-name:cur}}
.curop{{animation-name:curop}}
.hopen{{animation-name:open}} .hclosed{{position:absolute;left:0;top:0;animation-name:closed}}
.veil{{position:absolute;inset:0;background:rgba(243,228,223,.6);backdrop-filter:blur(6px);animation-name:veil}}
.modal{{position:absolute;left:250px;top:110px;width:780px;height:560px;background:#FFFBF7;border-radius:26px;box-shadow:0 40px 90px -30px rgba(74,44,36,.55);display:grid;grid-template-columns:1.15fr .85fr;overflow:hidden;animation-name:modal;direction:rtl}}
.mbody{{padding:34px 36px}}
.meb{{font-size:12px;letter-spacing:.2em;font-weight:600;color:var(--or)}}
.mh{{font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:34px;margin-top:6px}}
.mh b{{font-weight:500;color:var(--rose)}}
.mtot{{display:flex;justify-content:space-between;align-items:baseline;margin-top:16px;padding:10px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-weight:600;font-size:16px}}
.mtot b{{font-family:'Cormorant Garamond',serif;font-size:28px}}
.mq{{font-family:'Frank Ruhl Libre',serif;font-size:20px;margin:18px 0 10px}}
.clock{{display:flex;align-items:center;gap:12px}}
.step{{width:38px;height:38px;border-radius:50%;border:1px solid var(--cacao);display:flex;align-items:center;justify-content:center;font-size:20px}}
.flip{{display:flex;gap:4px;align-items:center;background:#E7BDB8;padding:8px;border-radius:12px;direction:ltr}}
.d{{position:relative;width:34px;height:46px;border-radius:6px;background:var(--cacao);color:var(--creme);font-family:'Cormorant Garamond',serif;font-weight:600;font-size:34px;line-height:46px;text-align:center;overflow:hidden;font-variant-numeric:lining-nums}}
.d::after{{content:"";position:absolute;inset:50% 0 auto;height:1px;background:rgba(0,0,0,.45)}}
.dd{{position:relative;width:34px;height:46px}}
.dd .d{{position:absolute;inset:0}}
.c{{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:600}}
.flipd{{animation-name:flipd}}
.mbtn{{position:relative;margin-top:22px;height:52px}}
.mbtn div{{position:absolute;inset:0;border-radius:999px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:16px}}
.mbags{{background:linear-gradient(180deg,#F7E3DE,#F0D5D0);display:flex;align-items:center;justify-content:center;padding:20px;direction:ltr;flex-wrap:wrap;gap:0 4px;align-content:center}}
.mbags svg{{margin:-6px -10px}}
.tbag{{position:absolute;top:1547px;width:150px;height:173px;transform-origin:50% 100%}}
.tshadow{{position:absolute;top:1704px;width:140px;height:26px;border-radius:50%;background:radial-gradient(closest-side,rgba(74,44,36,.32),transparent)}}

/* overlay copy */
.ov{{position:absolute;left:60px;right:60px;top:250px;text-align:center;animation-name:ov}}
.ov .l{{font-size:96px;white-space:nowrap;font-weight:700;line-height:1.05;color:var(--s-dark);letter-spacing:-.01em;text-shadow:0 2px 24px rgba(250,240,236,.6)}}
.ov .s{{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;letter-spacing:.3em;font-weight:500;color:#9A4E35;margin-bottom:18px}}
.ov2{{position:absolute;left:60px;right:60px;top:500px;text-align:center;font-size:44px;font-weight:500;line-height:1.3;color:var(--s-dark);animation-name:ov2}}
{chr(10).join(css)}
</style></head>
<body><div id="stage"><div class="film stack">

<!-- STUDIO · intro -->
<div class="intro stack" style="background:var(--s-bg)">
  <div style="position:absolute;top:120px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:18px">
    <div class="i1" style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:500;letter-spacing:.32em;text-transform:uppercase;color:var(--s-copper)" dir="ltr">Brand Worlds Studio · Hagit Antebi</div>
    <div class="i2" style="font-size:100px;font-weight:500;line-height:1.05;color:var(--s-ink)" dir="rtl">עולם מותג <em style="font-family:'Cormorant Garamond',serif;font-weight:400;color:var(--s-gold)">No.27</em></div>
  </div>
  <div class="i3" style="position:absolute;top:1470px;left:90px;right:90px;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center" dir="rtl">
    <div style="font-size:64px;font-weight:600;line-height:1.15;color:var(--s-ink)"><bdi dir="ltr">MIEL°</bdi> · הוויטרינה</div>
    <div style="font-size:34px;line-height:1.5;color:var(--s-ink)">בוחרים לפי הפרוסה. לוקחים את השלמה.</div>
  </div>
</div>

<!-- STUDIO · outro -->
<div class="outro stack" style="background:var(--s-bg)">
  <div style="position:absolute;top:110px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center">
    <div class="o1" style="font-size:28px;font-weight:500;letter-spacing:.06em;color:var(--s-copper)" dir="rtl"><bdi dir="ltr">MIEL°</bdi> · עולם מותג No.27</div>
    <div class="o2" style="font-size:66px;font-weight:600;line-height:1.2;color:var(--s-ink)" dir="rtl">מהוויטרינה של <bdi dir="ltr">MIEL°</bdi><br>ישר לשקית.</div>
  </div>
  <div class="o3" style="position:absolute;top:1430px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center">
    <div style="font-size:50px;font-weight:500;line-height:1.3;color:var(--s-copper)" dir="rtl">בואי לחוות בעצמך.</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:22px 56px;background:var(--s-ink);color:var(--s-bg);border-radius:12px" dir="rtl"><span style="font-size:38px;font-weight:500">כתבי <b style="font-weight:700">ויטרינה</b> בתגובות</span><span style="font-size:24px;opacity:.85">ואשלח לך את הקישור לעולם</span></div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</div>

<!-- STUDIO · crop marks -->
<div class="marks stack">
  <div style="position:absolute;top:412px;left:240px;width:44px;height:44px;border-top:2px solid var(--s-copper);border-left:2px solid var(--s-copper)"></div>
  <div style="position:absolute;top:412px;left:796px;width:44px;height:44px;border-top:2px solid var(--s-copper);border-right:2px solid var(--s-copper)"></div>
  <div style="position:absolute;top:1387px;left:240px;width:44px;height:44px;border-bottom:2px solid var(--s-copper);border-left:2px solid var(--s-copper)"></div>
  <div style="position:absolute;top:1387px;left:796px;width:44px;height:44px;border-bottom:2px solid var(--s-copper);border-right:2px solid var(--s-copper)"></div>
</div>

<!-- WORLD -->
<div class="world stack" style="overflow:hidden;background:#E9C9C6;box-shadow:0 50px 140px rgba(59,46,51,.26)">
 <div class="cam">
  <img class="cover" src="assets/12-still-table-empty.webp" alt="" style="object-position:50% 50%">
  <div class="stack" style="background:linear-gradient(180deg,rgba(250,240,236,.55),rgba(250,240,236,0) 34%)"></div>
  <div class="base"></div>
  <div class="lid"><div class="scr"><div class="page">
    <div class="pnav"><div class="plogo">MAISON MIEL<b>°</b></div><div class="pmenu"><span>הבנייה</span><span>האטלייה</span><span>החתך</span><span>החתימות</span><span>הוויטרינה</span><span>הבית</span></div><div class="ppill">לבנות את שלי</div></div>
    <div class="phead"><div class="peb">LA VITRINE · הוויטרינה</div><div class="ph2">בוחרים לפי הפרוסה. <b>לוקחים את השלמה.</b></div></div>
    <div class="pvit"><img src="assets/vitrine-slices.webp" alt=""></div>
    {"".join('<div class="dot" style="left:%dpx;top:%dpx"></div>' % (x, 160 + int((t + 0.08) * 447)) for x, t in [(212, .176), (442, .167), (682, .148), (879, .13), (1082, .139)])}
    {"".join('<div class="tag" style="left:%dpx;top:%dpx"><b>%s</b>%s</div>' % (x, y, CAKES[c]["fr"], CAKES[c]["he"]) for c, x, y in [("rose", 212, 500), ("fleurs", 442, 486), ("cacao", 682, 468), ("citron", 879, 453), ("pistache", 1082, 437)])}
    {ring_html}
    <div class="pnote">גררי פרוסה אל השקית, והעוגה השלמה נכנסת · או לחצי עליה</div>
    <div class="pcount">{info_html}</div>
    <div class="cartbar"><div class="ctxw">{cart_html}</div><div class="cbtn">לקופה</div></div>
    <div class="dock"><div class="dockhot"><div class="dockb">{dock_bags}</div></div><span>שחררי לתוך השקית</span></div>
    {ghost_html}
    <div class="veil"></div>
    <div class="modal">
      <div class="mbody">
        <div class="meb">LE COMPTOIR · בקופה</div>
        <div class="mh">רומנטיקה <b>יוצאת בשקית.</b></div>
        <div class="mtot"><span>5 עוגות שלמות</span><b>₪ 1,450</b></div>
        <div class="mq">מתי הרגע המתוק?</div>
        <div class="clock"><div class="step">+</div>
          <div class="flip"><div class="d">1</div><div class="d">0</div><span class="c">:</span>
            <div class="dd"><div class="d" style="animation-name:t1015">1</div><div class="d flipd" style="animation-name:t1030"><span style="display:block" class="flipd">3</span></div></div>
            <div class="dd"><div class="d" style="animation-name:t1015">5</div><div class="d" style="animation-name:t1030"><span style="display:block" class="flipd">0</span></div></div>
          </div><div class="step">−</div></div>
        <div class="mbtn">
          <div style="background:var(--cacao);color:var(--creme);animation-name:bt0">לשמור לאיסוף</div>
          <div style="background:var(--rose);color:#fff;animation-name:bt1">אורזות את השלמה…</div>
          <div style="background:var(--or);color:#fff;animation-name:bt2">השקיות מחכות לך ב-10:30</div>
        </div>
      </div>
      <div class="mbags">{"".join(bag_svg(c, 96) for c in ["rose", "cacao", "citron", "pistache", "fleurs"])}</div>
    </div>
    <div class="pcur"><div class="curop"><div class="hopen">{hand(False)}</div><div class="hclosed">{hand(True)}</div></div></div>
  </div></div></div>
  {table_html}
 </div>
</div>

<!-- overlay copy (like the reference's single big line) -->
<div class="ov" dir="rtl"><div class="s" dir="ltr">MIEL° · LA VITRINE</div><div class="l">חוויית גרירה באתר.</div></div>
<div class="ov2" dir="rtl">חמש עוגות. חמש שקיות.<br>כל דופן היא החתך שלה.</div>

<!-- HOOK (frame 0 already shows the question and the generic shop) -->
<div class="hook stack" style="background:var(--s-cream)">
  <div style="position:absolute;top:88px;right:80px;display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:36px;color:var(--s-dark)" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size:17px;letter-spacing:.3em;color:#8B7B6E">חגית אנטבי</div>
  </div>
  <div style="position:absolute;top:240px;left:80px;right:80px;text-align:right;font-size:84px;font-weight:600;line-height:1.16;color:var(--s-dark)" dir="rtl">נכנסות לאתר שלך,<br>ולא <span style="color:var(--s-copper)">קונות</span>?</div>
  <div class="shop" dir="rtl">
    <div class="sbar"><i></i><i></i><i></i><span>www.cakes-shop.co.il</span></div>
    <div class="shead"><span>העוגות שלנו</span><small>סל (0)</small></div>
    <div class="sgrid"><div class="in">{cards}</div></div>
  </div>
  <div class="hcur">{ARROW}</div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line" pathLength="1" d="M1140 1700 H540"></path></svg>
  {BALL}
</div>

<!-- STUDIO · layer tag -->
<div class="hud" style="position:absolute;top:40px;right:40px;width:520px;height:120px;box-sizing:border-box;padding:16px 26px;background:rgba(250,248,243,.92);border:1px solid #D4C9BC;display:flex;flex-direction:column;gap:6px" dir="rtl">
  <div style="font-size:18px;font-weight:500;letter-spacing:.04em;color:var(--s-copper)">Brand Worlds Studio · עולם מותג No.27</div>
  <div style="display:flex;flex-direction:column;gap:2px"><span style="font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--s-ink)" dir="ltr">04 · Live Site</span><span style="font-size:21px;color:var(--s-ink)">הוויטרינה: גוררים פרוסה, מקבלים עוגה</span></div>
</div>

<div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18)"><div class="progress" style="height:6px;background:var(--s-copper)"></div></div>
</div></div></body></html>
"""
open(os.path.join(HERE, "reel.html"), "w").write(html)
print("wrote reel.html", len(html), "bytes,", len(css), "keyframes")
