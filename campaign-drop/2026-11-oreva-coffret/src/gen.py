#!/usr/bin/env python3
"""ORÉVA° · Le Coffret — studio-mode "live screen" reel (9:16, 30s).

Hook A: "שבעה מוצרים באתר, והיא יוצאת בלי כלום?" over a generic skincare shop.
Studio window → laptop on Or Éva's terrazzo counter: the real Le Coffret section, products dragged
from the shelf into their foam cuts, DEW ESSENCE refused. Signature scene: seven become four — the
copper ribbon threads the four, the other three step back, the four drop into a big kit and the ribbon
becomes the copper band of the sleeve. Checkout → the promise (her hands) → outro + "ערכה" CTA.
Render: node .claude/skills/brandos-brand-world-reel/scripts/render.js reel.html 30 <out>
"""
import os

D = 30.0
HERE = os.path.dirname(os.path.abspath(__file__))
css = []


def P(t):
    return f"{max(0.0, min(D, t)) / D * 100:.3f}%"


def kf(name, frames):
    fr = list(frames)
    if fr[0][0] > 0:
        fr.insert(0, (0, fr[0][1]))
    if fr[-1][0] < D:
        fr.append((D, fr[-1][1]))
    css.append("@keyframes %s{%s}" % (name, "".join("%s{%s}" % (P(t), c) for t, c in fr)))
    return name


def win(name, a, b, fade=.18):
    fr = [(max(0, a - fade), "opacity:0"), (a, "opacity:1")] if a > 0 else [(0, "opacity:1")]
    if b < D:
        fr += [(b, "opacity:1"), (min(D, b + fade), "opacity:0")]
    return kf(name, fr)


# products: original cut-out sizes (bbox of the site's photos) and the kit files
PR = {
    "cleanse": dict(n="SOFT CLEANSE", ow=430, oh=1306, p=140),
    "essence": dict(n="DEW ESSENCE", ow=386, oh=1370, p=180),
    "dew": dict(n="DEW", ow=423, oh=1260, p=240),
    "glow": dict(n="GLOW", ow=472, oh=1308, p=260),
    "calm": dict(n="CALM", ow=467, oh=1302, p=240),
    "eye": dict(n="EYE VEIL", ow=438, oh=1033, p=220),
    "cocoon": dict(n="COCOON CREAM", ow=851, oh=636, p=290),
}
SHELF = ["cleanse", "essence", "dew", "glow", "calm", "eye", "cocoon"]          # right → left
SLOTS = [("cleanse", "cleanse", "01 · ניקוי"), ("serum", "glow", "02 · סרום"), ("eye", "eye", "03 · עיניים"), ("cocoon", "cocoon", "04 · קרם")]
CHOSEN = {"cleanse": "cleanse", "serum": "calm", "eye": "eye", "cocoon": "cocoon"}


def row(ids, k, gap, cx, bottom):
    """lay out items right→left, centred on cx, standing on `bottom`; returns {id: (x, y, w, h)}"""
    ws = [PR[i]["ow"] * k for i in ids]
    tot = sum(ws) + gap * (len(ids) - 1)
    xr, out = cx + tot / 2, {}
    for i, w in zip(ids, ws):
        h = PR[i]["oh"] * k
        out[i] = (xr - w, bottom - h, w, h)
        xr -= w + gap
    return out


def slots_row(k, gap, cx, bottom):
    dims = [(s, PR[m]["ow"] * k, PR[m]["oh"] * k) for s, m, _ in SLOTS]
    tot = sum(w for _, w, _ in dims) + gap * 3
    xr, out = cx + tot / 2, {}
    for s, w, h in dims:
        out[s] = (xr - w, bottom - h, w, h)
        xr -= w + gap
    return out, tot


def box(r):
    return "left:%.1fpx;top:%.1fpx;width:%.1fpx;height:%.1fpx" % r


def hand(closed):
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
            '<g fill="#1d1d1f" stroke="#1d1d1f" stroke-width="2.6" stroke-linejoin="round">%s</g><g fill="#fff">%s</g></svg>') % (shapes, shapes)


# ── page (1280×800, shown at .75 in a 960×600 screen) ───────────────────────
SH = row(SHELF, .12, 28, 640, 300)
KS, KW = slots_row(.2, 46, 640, 690)
TL = {"dew": 0}

# ── timeline ────────────────────────────────────────────────────────────────
HOOK_OUT = 2.5
WORLD_OPEN, WORLD_FULL = 3.95, 4.55
WORLD_CLOSE, WORLD_SMALL = 27.2, 27.75
SIG_IN, SIG_OUT = 14.45, 20.35
ADD_CLICK = 21.3
PROMISE = 24.15


def ctr(r):
    return (r[0] + r[2] / 2, r[1] + r[3] / 2)


# drags on the screen: (id, slot or None, hover, grab, release)
DR = [("cleanse", "cleanse", 5.9, 6.1, 7.3), ("essence", None, 8.35, 8.5, 9.45), ("calm", "serum", 11.2, 11.3, 12.3), ("eye", "eye", 12.95, 13.05, 13.75)]
KIT_MID = (640, 560)
cur = [(4.7, (1360, 700))]
for pid, sl, hv, gr, rl in DR:
    s = ctr(SH[pid])
    tgt = ctr(KS[sl]) if sl else KIT_MID
    cur += [(hv, s), (gr, s), (rl, tgt), (rl + .15, tgt)]
BTN = (604, 770)
cur += [(14.3, (700, 600)), (20.4, (700, 600)), (ADD_CLICK, BTN), (23.9, BTN)]
kf("cur", [(t, "transform:translate(%dpx,%dpx)" % (x - 22, y - 18)) for t, (x, y) in cur])
win("curop", 4.85, 24.0)
clicks = [(ADD_CLICK - .05, ADD_CLICK + .12)]
cw = [(gr, rl) for _, _, _, gr, rl in DR] + clicks
fr_c, fr_o = [(0, "opacity:0")], [(0, "opacity:1")]
for a, b in cw:
    fr_c += [(a - .01, "opacity:0"), (a, "opacity:1"), (b, "opacity:1"), (b + .01, "opacity:0")]
    fr_o += [(a - .01, "opacity:1"), (a, "opacity:0"), (b, "opacity:0"), (b + .01, "opacity:1")]
kf("closed", fr_c)
kf("open", fr_o)

# ghosts follow the cursor; they grow toward the size of their cut
ghosts = ""
for i, (pid, sl, hv, gr, rl) in enumerate(DR):
    x, y, w, h = SH[pid]
    sx, sy = ctr(SH[pid])
    if sl:
        X, Y, W, Hh = KS[sl]
        s_end = Hh / h
        tx, ty = X + W / 2, Y + Hh / 2

        def T(cx, cy, s):
            return "transform:translate(%.1fpx,%.1fpx) scale(%.3f)" % (cx - w * s / 2, cy - h * s / 2, s)
        fr = [(gr - .01, T(sx, sy, 1) + ";opacity:0"), (gr, T(sx, sy, 1) + ";opacity:1"),
              ((gr + rl) / 2, T((sx + tx) / 2, (sy + ty) / 2 - 40, (1 + s_end) / 2) + ";opacity:1"),
              (rl, T(tx, ty, s_end) + ";opacity:1"), (rl + .01, T(tx, ty, s_end) + ";opacity:0")]
    else:
        tx, ty = KIT_MID

        def T(cx, cy, s):
            return "transform:translate(%.1fpx,%.1fpx) scale(%.3f)" % (cx - w * s / 2, cy - h * s / 2, s)
        fr = [(gr - .01, T(sx, sy, 1) + ";opacity:0"), (gr, T(sx, sy, 1) + ";opacity:1"), (rl, T(tx, ty, 1.25) + ";opacity:1"),
              (rl + .38, T(sx, sy, 1) + ";opacity:1"), (rl + .39, T(sx, sy, 1) + ";opacity:0")]
    kf("gh%d" % i, fr)
    ghosts += '<img class="ghost" src="assets/%s.webp" alt="" style="width:%.1fpx;height:%.1fpx;animation-name:gh%d">' % (pid, w, h, i)

# shelf items: hidden while in hand, dimmed once in the kit; the essence shakes
shelf_html = ""
for pid in SHELF:
    fr = [(0, "opacity:1;transform:none")]
    for i, (p2, sl, hv, gr, rl) in enumerate(DR):
        if p2 != pid:
            continue
        if sl:
            fr += [(gr - .01, "opacity:1;transform:none"), (gr, "opacity:0;transform:none"), (rl, "opacity:0;transform:none"), (rl + .15, "opacity:.28;transform:none")]
        else:
            fr += [(gr - .01, "opacity:1;transform:none"), (gr, "opacity:0;transform:none"), (rl + .38, "opacity:0;transform:none"), (rl + .39, "opacity:1;transform:none")]
            for j, dx in enumerate([-7, 7, -6, 6, 0]):
                fr.append((rl + .45 + j * .08, "opacity:1;transform:translateX(%dpx)" % dx))
    if pid == "cocoon":
        fr += [(SIG_OUT, "opacity:1;transform:none"), (SIG_OUT + .01, "opacity:.28;transform:none")]
    kf("sh_" + pid, fr)
    shelf_html += '<img class="sp" src="assets/%s.webp" alt="" style="%s;animation-name:sh_%s">' % (pid, box(SH[pid]), pid)
shelf_labels = "".join('<span class="spl" style="left:%.1fpx;top:308px;width:%.1fpx">%s</span>' % (SH[p][0] - 20, SH[p][2] + 40, PR[p]["n"].replace("SOFT ", "").replace(" CREAM", "")) for p in SHELF)

# kit slots: cut (mask), copper while its product is in hand, product appears on release
slot_html = ""
for s, mask, lab in SLOTS:
    r = KS[s]
    fr = [(0, "--cut:#BFAB95")]
    for pid, sl, hv, gr, rl in DR:
        if sl == s:
            fr += [(gr, "--cut:#BFAB95"), (gr + .15, "--cut:#C0855F"), (rl, "--cut:#C0855F"), (rl + .1, "--cut:#BFAB95")]
        else:
            fr += [(gr, "--cut:#BFAB95"), (gr + .15, "--cut:#D3C4B3"), (rl, "--cut:#D3C4B3"), (rl + .1, "--cut:#BFAB95")]
    kf("cut_" + s, fr)
    placed = [(pid, rl) for pid, sl, hv, gr, rl in DR if sl == s]
    t_in = placed[0][1] if placed else SIG_OUT
    win("in_" + s, t_in, D, .02)
    kf("land_" + s, [(t_in, "transform:translateY(-10px)"), (t_in + .3, "transform:none")])
    slot_html += ('<div class="slot" style="%s"><i class="cut" style="-webkit-mask-image:url(assets/%s.webp);mask-image:url(assets/%s.webp);animation-name:cut_%s"></i>'
                  '<img src="assets/%s.webp" alt="" style="animation-name:in_%s"><b class="sl" style="animation-name:none">%s</b></div>') % (
        box(r), mask, mask, s, CHOSEN[s], s, lab)

# toast, kit sleeve on the screen, cart drawer
win("toast", 9.6, 11.5, .25)
win("slotsw", 0, SIG_OUT, .01)
kf("pslv", [(SIG_OUT, "transform:none")])                      # closed after the signature scene
win("pslvw", SIG_OUT, D, .01)
win("addon", SIG_OUT, D, .01)
kf("addbtn", [(ADD_CLICK - .06, "transform:none"), (ADD_CLICK, "transform:scale(.93)"), (ADD_CLICK + .14, "transform:none")])
kf("drawer", [(ADD_CLICK + .1, "transform:translateX(-105%)"), (ADD_CLICK + .55, "transform:none")])
win("dveil", ADD_CLICK + .1, D, .3)
win("badge", ADD_CLICK + .3, D, .1)
st_txt = [(0, 7.45, "הערכה ריקה. ארבעה מקומות בקצף מחכים."), (7.45, 12.45, "1/4 · חסר: סרום, עיניים, קרם"), (12.45, 13.9, "2/4 · חסר: עיניים, קרם"),
          (13.9, SIG_OUT, "3/4 · חסר: קרם")]
status_html = ""
for i, (a, b, t) in enumerate(st_txt):
    win("stt%d" % i, a, b, .05)
    status_html += '<span style="animation-name:stt%d">%s</span>' % (i, t)

# ── signature: seven become four ───────────────────────────────────────────
BR = row(SHELF, .27, 20, 540, 960)
BK, BKW = slots_row(.3, 50, 540, 1600)
order_pick = ["cleanse", "calm", "eye", "cocoon"]
pick_slot = {"cleanse": "cleanse", "calm": "serum", "eye": "eye", "cocoon": "cocoon"}
win("sig", SIG_IN, SIG_OUT, .4)
kf("st1", [(SIG_IN + .45, "opacity:0;transform:translateY(26px)"), (SIG_IN + .8, "opacity:1;transform:none")])
kf("st2", [(SIG_IN + .8, "opacity:0;transform:translateY(26px)"), (SIG_IN + 1.15, "opacity:1;transform:none")])
big_html = ""
RIB_T0, RIB_T1 = 15.8, 17.1
for j, pid in enumerate(SHELF):
    x, y, w, h = BR[pid]
    t0 = SIG_IN + .35 + j * .07
    if pid in pick_slot:
        X, Y, W, Hh = BK[pick_slot[pid]]
        s = Hh / h
        dx, dy = (X + W / 2) - (x + w / 2), (Y + Hh) - (y + h)
        tp = RIB_T0 + (RIB_T1 - RIB_T0) * (order_pick.index(pid) + .5) / 4
        tf = 17.55 + order_pick.index(pid) * .2
        fr = [(t0, "opacity:0;transform:translateY(40px)"), (t0 + .4, "opacity:1;transform:none"), (tp - .1, "opacity:1;transform:none"),
              (tp + .15, "opacity:1;transform:translateY(-22px)"), (tf, "opacity:1;transform:translateY(-22px)"),
              (tf + .5, "opacity:1;transform:translate(%.1fpx,%.1fpx) scale(%.3f)" % (dx, dy, s))]
    else:
        fr = [(t0, "opacity:0;transform:translateY(40px)"), (t0 + .4, "opacity:1;transform:none"), (16.4, "opacity:1;transform:none"),
              (16.9, "opacity:.22;transform:translateY(-30px) scale(.86)"), (17.4, "opacity:0;transform:translateY(-60px) scale(.8)")]
    kf("bp_" + pid, fr)
    big_html += '<img class="bp" src="assets/%s.webp" alt="" style="%s;animation-name:bp_%s">' % (pid, box(BR[pid]), pid)
# ribbon through the four (in front), as one path; a bead rides its tip
pts = [(1120, 760)]
for pid in order_pick:
    x, y, w, h = BR[pid]
    pts.append((x + w / 2, y + h * .55 - 22))
pts.append((-40, 700))
d = "M %.0f %.0f" % pts[0]
for i in range(len(pts) - 1):
    p0, p1, p2, p3 = pts[i - 1] if i else pts[i], pts[i], pts[i + 1], pts[i + 2] if i + 2 < len(pts) else pts[i + 1]
    c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6 + (60 if i % 2 else -60))
    c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6 + (60 if i % 2 else -60))
    d += " C %.0f %.0f %.0f %.0f %.0f %.0f" % (c1 + c2 + p2)
kf("rib", [(RIB_T0, "stroke-dashoffset:1"), (RIB_T1, "stroke-dashoffset:0"), (17.6, "stroke-dashoffset:0;opacity:1"), (18.3, "stroke-dashoffset:0;opacity:0")])
kf("bead", [(RIB_T0 - .05, "offset-distance:0%;opacity:0"), (RIB_T0, "offset-distance:0%;opacity:1"), (RIB_T1, "offset-distance:100%;opacity:1"), (RIB_T1 + .15, "offset-distance:100%;opacity:0")])
kf("bkit", [(17.0, "opacity:0;transform:translateY(120px)"), (17.5, "opacity:1;transform:none")])
kf("bslv", [(18.65, "transform:translateY(-104%)"), (19.35, "transform:none")])
kf("bcard", [(19.2, "opacity:0;transform:rotate(-2deg) translateY(16px)"), (19.5, "opacity:1;transform:rotate(-2deg)")])
bslots = ""
for s, mask, lab in SLOTS:
    bslots += ('<div class="bslot" style="%s"><i class="cut" style="-webkit-mask-image:url(assets/%s.webp);mask-image:url(assets/%s.webp)"></i></div>'
               '<b class="bsl" style="left:%.1fpx;top:%.1fpx;width:%.1fpx">%s</b>') % (box(BK[s]), mask, mask, BK[s][0] - 30, BK[s][1] + BK[s][3] + 14, BK[s][2] + 60, lab)
KX0 = 540 - BKW / 2 - 40

# ── studio wrapper, overlay, hud, promise ───────────────────────────────────
kf("cam", [(4.5, "transform:scale(1)"), (5.5, "transform:scale(1.28)"), (24.2, "transform:scale(1.33)")])
kf("hook", [(HOOK_OUT - .05, "opacity:1"), (HOOK_OUT + .15, "opacity:0")])
kf("hcur", [(0, "transform:translate(470px,500px)"), (.5, "transform:translate(470px,500px)"), (.95, "transform:translate(200px,560px)"),
            (1.4, "transform:translate(500px,860px)"), (1.85, "transform:translate(210px,860px)"), (2.45, "transform:translate(760px,1100px)")])
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
for n, t in [("o1", 27.55), ("o2", 27.75), ("o3", 28.15)]:
    kf(n, [(t, "opacity:0;transform:translateY(26px)"), (t + .4, "opacity:1;transform:none")])
kf("ov", [(4.7, "opacity:0;transform:translateY(30px)"), (5.15, "opacity:1;transform:none"), (14.25, "opacity:1;transform:none"), (14.5, "opacity:0"),
          (20.3, "opacity:0"), (20.6, "opacity:1;transform:none"), (23.95, "opacity:1"), (24.2, "opacity:0")])
HUDS = [(4.95, 14.3, "04 · Live Site", "הערכה: גוררים מהמדף לקצף"), (14.8, 20.2, "02 · The Visual World", "סרט הנחושת בוחר ארבעה"),
        (20.55, 24.0, "04 · Live Site", "הערכה לסל"), (24.5, 27.1, "05 · The Promise", "קודם הידיים")]
for i, (a, b, _, _) in enumerate(HUDS):
    win("hud%d" % i, a, b, .25)
win("prw", PROMISE, D, .4)
kf("prpush", [(PROMISE - .4, "transform:scale(1.1)"), (27.4, "transform:scale(1.0)")])
kf("prt1", [(PROMISE + .35, "opacity:0;transform:translateY(26px)"), (PROMISE + .75, "opacity:1;transform:none")])
kf("prt2", [(PROMISE + .85, "opacity:0;transform:translateY(26px)"), (PROMISE + 1.25, "opacity:1;transform:none")])

ARROW = ('<svg viewBox="0 0 20 28" width="44" height="62" style="display:block;overflow:visible">'
         '<path d="M1 1 L1 22 L6.5 16.8 L10.5 26 L14 24.6 L10.2 15.6 L17.5 15.6 Z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>')
BALL = ('<div class="ball" style="offset-path:path(\'M1140 1700 H540\');animation-name:bl0"><div class="halo"></div><div class="sph">'
        '<div class="rl" style="animation-name:rl0"><div style="position:absolute;left:13px;top:13px;width:52px;height:52px;border-radius:50%;border:1px solid rgba(250,228,200,.65)"></div>'
        '<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:\'Cormorant Garamond\',serif;font-size:21px;color:#F5DEC4" dir="ltr">BW</div>'
        '<div style="position:absolute;left:12px;top:46px;width:14px;height:14px;border-radius:50%;background:#FFF7EC;box-shadow:0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>')
gnames = ["סרום פנים", "סרום לחות", "קרם יום", "סרום ויטמין", "תחליב ניקוי", "סרום לילה", "קרם עיניים", "טונר"]
gcards = "".join('<div class="gcard"><img src="assets/generic-serum.jpg" alt=""><div class="gn">%s</div><div class="gp"><span>₪ 189</span><button>הוספה לסל</button></div></div>' % n for n in gnames)
hud_html = "".join(('<div class="hud" style="animation-name:hud%d" dir="rtl"><div class="h1">Brand Worlds Studio · עולם מותג No.24</div>'
                    '<div class="h2"><span dir="ltr">%s</span><span>%s</span></div></div>') % (i, t, s) for i, (_, _, t, s) in enumerate(HUDS))
drawer_rows = "".join('<div class="drow"><img src="assets/%s.webp" alt=""><div><b>%s</b><small>1 ×</small></div><span>₪ %d</span></div>' % (pid, PR[pid]["n"], PR[pid]["p"]) for pid in order_pick)
kit_total = sum(PR[p]["p"] for p in order_pick)
BIDI = '<bdi dir="ltr">ORÉVA°</bdi>'

html = f"""<!doctype html>
<html lang="he"><head><meta charset="utf-8"><title>ORÉVA° Le Coffret — reel</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&amp;family=Heebo:wght@300;400;500;600;700;800&amp;family=Frank+Ruhl+Libre:wght@400;500;700&amp;family=Plus+Jakarta+Sans:wght@400;500&amp;display=swap">
<style>
:root{{--s-bg:#FAF8F3;--s-cream:#EEE6D8;--s-ink:#6B563F;--s-copper:#C4765A;--s-gold:#B8894A;--s-dark:#3E2F25;
  --cream:#F6EFE7;--cream-2:#FBF7F1;--blush:#EFCDBF;--blush-2:#F5DED3;--stone:#D9C7B3;--copper:#B87A57;--copper-deep:#8F5A3C;--copper-light:#D9A88A;--ink:#3A2E29;--ink-2:#6E5E55;--ink-3:#9A8A80}}
@property --cut{{syntax:"<color>";inherits:true;initial-value:#BFAB95}}
html,body{{margin:0;background:var(--s-bg)}}
body{{font-family:'Heebo',sans-serif;color:var(--s-dark)}}
#stage{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--s-bg)}}
.film *{{animation-duration:{D:g}s;animation-iteration-count:infinite;animation-timing-function:cubic-bezier(.4,0,.2,1);animation-fill-mode:both}}
.stack{{position:absolute;inset:0}}
img{{display:block}}
.cover{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.world{{animation-name:world;transform-origin:50% 46%}} .marks{{animation-name:marks}} .intro{{animation-name:intro}} .outro{{animation-name:outro}}
.i1{{animation-name:i1}}.i2{{animation-name:i2}}.i3{{animation-name:i3}}.o1{{animation-name:o1}}.o2{{animation-name:o2}}.o3{{animation-name:o3}}
.progress{{animation-name:prog;animation-timing-function:linear;transform-origin:right}}
@keyframes prog{{0%{{transform:scaleX(0)}}100%{{transform:scaleX(1)}}}}
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
.sgrid{{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:24px 30px}}
.gcard{{border:1px solid #eee;border-radius:14px;overflow:hidden;background:#fff}}
.gcard img{{width:100%;height:250px;object-fit:cover}}
.gn{{font-size:24px;color:#2E2A27;padding:12px 16px 2px}}
.gp{{display:flex;justify-content:space-between;align-items:center;padding:6px 16px 16px;font-size:22px;color:#2E2A27;font-weight:600}}
.gp button{{font:400 18px 'Heebo';border:1px solid #ccc;background:#fafafa;border-radius:8px;padding:6px 12px;color:#555}}
.hcur{{position:absolute;left:150px;top:610px;animation-name:hcur}}

.cam{{position:absolute;inset:0;animation-name:cam;transform-origin:540px 1150px}}
.bg{{position:absolute;height:2000px;width:3556px;top:-170px;left:-2280px;max-width:none}}
.lid{{position:absolute;left:40px;top:760px;width:1000px;height:640px;box-sizing:border-box;padding:20px;background:#1b1b1d;border-radius:30px 30px 8px 8px;box-shadow:0 0 0 2px #3a3a3e inset,0 40px 60px -20px rgba(60,40,30,.45)}}
.base{{position:absolute;left:-10px;top:1396px;width:1100px;height:34px;background:linear-gradient(180deg,#e9e7ea,#bdbbc0 70%,#8d8b90);border-radius:4px 4px 30px 30px;box-shadow:0 26px 30px -12px rgba(60,40,30,.4)}}
.scr{{position:relative;width:960px;height:600px;overflow:hidden;border-radius:6px;background:var(--cream)}}
.page{{position:absolute;left:0;top:0;width:1280px;height:800px;transform:scale(.75);transform-origin:0 0;background:linear-gradient(180deg,var(--cream),var(--blush-2) 160%);font-family:'Heebo',sans-serif;color:var(--ink);overflow:hidden}}
.pnav{{position:absolute;left:0;right:0;top:0;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;background:rgba(246,239,231,.95);border-bottom:1px solid rgba(58,46,41,.1);direction:rtl}}
.plogo{{font-family:'Cormorant Garamond',serif;font-size:22px;letter-spacing:.3em;direction:ltr;line-height:1}}
.plogo small{{display:block;font-size:8px;letter-spacing:.4em;color:var(--copper)}}
.pmenu{{display:flex;gap:24px;font-size:15px;color:var(--ink-2)}}
.pact{{display:flex;gap:12px;align-items:center}}
.pbtn{{background:var(--copper);color:#fff;border-radius:999px;padding:8px 18px;font-size:14px;font-weight:500}}
.pcart{{position:relative;width:34px;height:34px;border-radius:50%;border:1px solid var(--stone);display:flex;align-items:center;justify-content:center}}
.pcart i{{position:absolute;top:-6px;left:-6px;min-width:18px;height:18px;border-radius:9px;background:var(--copper-deep);color:#fff;font:600 11px/18px 'Heebo';text-align:center;font-style:normal;animation-name:badge}}
.phead{{position:absolute;top:72px;left:0;right:0;text-align:center}}
.peb{{font-family:'Cormorant Garamond',serif;font-size:12px;letter-spacing:.3em;color:var(--copper);direction:ltr}}
.ph2{{font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:34px;line-height:1.15;margin-top:2px}}
.ph2 b{{font-weight:700;color:var(--copper-deep)}}
.sp{{position:absolute;filter:drop-shadow(0 6px 6px rgba(58,46,41,.18))}}
.spl{{position:absolute;text-align:center;font-family:'Cormorant Garamond',serif;font-size:10px;letter-spacing:.12em;color:var(--ink-2)}}
.shelfline{{position:absolute;left:310px;width:660px;top:300px;height:7px;background:linear-gradient(180deg,#E7DACB,#D3C0AC)}}
.phint{{position:absolute;top:330px;left:0;right:0;text-align:center;font-size:12.5px;color:var(--ink-3);direction:rtl}}
.klid{{position:absolute;left:{640 - KW / 2 - 10:.0f}px;width:{KW + 20:.0f}px;top:350px;height:48px;border-radius:12px 12px 2px 2px;background:linear-gradient(180deg,#F3DCD0,#EBCBBB);box-shadow:inset 0 0 0 1px rgba(184,122,87,.35);transform:perspective(700px) rotateX(38deg);transform-origin:50% 100%;text-align:center;font-family:'Cormorant Garamond',serif;font-size:10px;letter-spacing:.3em;color:var(--copper-deep);padding-top:10px;box-sizing:border-box}}
.kbox{{position:absolute;left:{640 - KW / 2 - 50:.0f}px;width:{KW + 100:.0f}px;top:396px;height:338px;border-radius:8px 8px 14px 14px;background:linear-gradient(180deg,#F5E2D8,#EDCFC1);box-shadow:inset 0 0 0 1px rgba(184,122,87,.4),0 30px 40px -26px rgba(58,46,41,.45);overflow:hidden}}
.kins{{position:absolute;inset:10px;border-radius:5px;background:radial-gradient(120% 90% at 50% 0%,#EADFD2,#DCCBB8);box-shadow:inset 0 3px 10px rgba(58,46,41,.14)}}
.slot{{position:absolute}}
.slot img,.bslot img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:50% 100%;filter:drop-shadow(0 3px 3px rgba(58,46,41,.2))}}
.cut{{position:absolute;inset:0;-webkit-mask-size:100% 100%;mask-size:100% 100%;-webkit-mask-repeat:no-repeat;mask-repeat:no-repeat;background:linear-gradient(180deg,rgba(58,46,41,.22),rgba(58,46,41,0) 22%),var(--cut)}}
.sl{{position:absolute;top:100%;left:-30px;right:-30px;text-align:center;margin-top:8px;font-size:11.5px;font-weight:500;color:var(--ink-2);direction:rtl;white-space:nowrap}}
.psleeve{{position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,#F5E2D8,#EDCDBF);box-shadow:inset 0 0 0 1px rgba(184,122,87,.45);display:flex;align-items:center;justify-content:center;animation-name:pslvw}}
.band{{position:absolute;top:0;bottom:0;left:50%;width:30px;margin-left:-15px;background:linear-gradient(90deg,var(--copper-deep),var(--copper-light) 45%,var(--copper) 60%,var(--copper-deep))}}
.card{{position:relative;background:var(--cream-2);border:1px solid rgba(184,122,87,.45);border-radius:6px;padding:12px 22px;text-align:center;box-shadow:0 14px 26px -16px rgba(58,46,41,.5);transform:rotate(-2deg);direction:rtl}}
.card b{{display:block;font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:19px;color:var(--ink)}}
.card small{{display:block;font-size:11.5px;color:var(--ink-2);margin-top:2px;direction:ltr}}
.pstatus{{position:absolute;top:744px;left:0;right:0;height:20px;text-align:center;font-size:13px;color:var(--ink-2);direction:rtl}}
.pstatus span{{position:absolute;left:0;right:0}}
.pbar{{position:absolute;top:748px;left:0;right:0;display:flex;justify-content:center;gap:12px;align-items:center;direction:rtl;animation-name:addon}}
.pbar b{{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:600;font-variant-numeric:lining-nums}}
.addb{{background:var(--copper);color:#fff;border-radius:999px;padding:9px 22px;font-size:14px;font-weight:500;animation-name:addbtn}}
.toast{{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);background:var(--ink);color:var(--cream);border-radius:999px;padding:9px 20px;font-size:13.5px;white-space:nowrap;direction:rtl;animation-name:toast}}
.ghost{{position:absolute;left:0;top:0;transform-origin:0 0;filter:drop-shadow(0 14px 14px rgba(58,46,41,.3))}}
.pcur{{position:absolute;left:0;top:0;animation-name:cur}} .curop{{animation-name:curop}} .hopen{{animation-name:open}} .hclosed{{position:absolute;left:0;top:0;animation-name:closed}}
.dveil{{position:absolute;inset:0;background:rgba(58,46,41,.28);animation-name:dveil}}
.drawer{{position:absolute;left:0;top:0;bottom:0;width:430px;background:var(--cream-2);box-shadow:20px 0 40px -20px rgba(58,46,41,.4);padding:26px 28px;box-sizing:border-box;direction:rtl;animation-name:drawer}}
.drawer h4{{margin:0 0 14px;font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:24px}}
.drow{{display:grid;grid-template-columns:54px 1fr auto;gap:12px;align-items:center;border-bottom:1px solid rgba(58,46,41,.1);padding:8px 0}}
.drow img{{width:54px;height:64px;object-fit:contain}}
.drow b{{display:block;font-family:'Cormorant Garamond',serif;font-size:16px;letter-spacing:.08em;direction:ltr;text-align:right}}
.drow small{{font-size:12px;color:var(--ink-3)}}
.drow span,.dtot b{{font-family:'Cormorant Garamond',serif;font-size:18px;font-weight:600;font-variant-numeric:lining-nums}}
.dtot{{display:flex;justify-content:space-between;align-items:baseline;margin-top:14px;font-size:15px}}
.dtot b{{font-size:26px}}
.dpay{{margin-top:16px;background:var(--copper);color:#fff;border-radius:999px;text-align:center;padding:11px;font-weight:500}}

.sig{{animation-name:sig;background:radial-gradient(ellipse at 50% 55%,#FBF4EE,#F2DDD2 75%)}}
.stxt{{position:absolute;top:250px;left:60px;right:60px;text-align:center;font-size:92px;font-weight:700;line-height:1.08;color:#3A2E29}}
.stxt b{{color:#8F5A3C;font-weight:700}}
.bp{{position:absolute;transform-origin:50% 100%;filter:drop-shadow(0 18px 18px rgba(58,46,41,.22))}}
.rib{{fill:none;stroke:url(#cg);stroke-width:7;stroke-linecap:round;stroke-dasharray:1 1;animation-name:rib;filter:drop-shadow(0 2px 2px rgba(143,90,60,.3))}}
.bead{{position:absolute;left:0;top:0;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#F5D2B5,#C0855F 50%,#7E4A2E);offset-rotate:0deg;animation-name:bead;animation-timing-function:linear;box-shadow:0 4px 8px rgba(120,70,40,.4)}}
.bkit{{position:absolute;inset:0;animation-name:bkit}}
.bklid{{position:absolute;left:{KX0 + 20:.0f}px;width:{BKW + 40:.0f}px;top:1040px;height:96px;border-radius:18px 18px 4px 4px;background:linear-gradient(180deg,#F3DCD0,#EBCBBB);box-shadow:inset 0 0 0 1px rgba(184,122,87,.35);transform:perspective(900px) rotateX(38deg);transform-origin:50% 100%;text-align:center;font-family:'Cormorant Garamond',serif;font-size:16px;letter-spacing:.32em;color:#8F5A3C;padding-top:18px;box-sizing:border-box}}
.bkbox{{position:absolute;left:{KX0 - 20:.0f}px;width:{BKW + 120:.0f}px;top:1130px;height:560px;border-radius:12px 12px 22px 22px;background:linear-gradient(180deg,#F5E2D8,#EDCFC1);box-shadow:inset 0 0 0 1px rgba(184,122,87,.4),0 40px 60px -30px rgba(58,46,41,.45);overflow:hidden}}
.bkins{{position:absolute;inset:16px;border-radius:8px;background:radial-gradient(120% 90% at 50% 0%,#EADFD2,#DCCBB8);box-shadow:inset 0 4px 12px rgba(58,46,41,.14)}}
.bslot{{position:absolute}} .bslot .cut{{--cut:#BFAB95}}
.bsl{{position:absolute;text-align:center;font-size:24px;font-weight:500;color:#6E5E55;direction:rtl}}
.bslv{{position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,#F5E2D8,#EDCDBF);box-shadow:inset 0 0 0 1px rgba(184,122,87,.45);display:flex;align-items:center;justify-content:center;animation-name:bslv}}
.bslv .band{{width:58px;margin-left:-29px}}
.bcard{{position:relative;background:#FBF7F1;border:1px solid rgba(184,122,87,.45);border-radius:10px;padding:24px 40px;text-align:center;box-shadow:0 20px 34px -18px rgba(58,46,41,.5);direction:rtl;animation-name:bcard}}
.bcard b{{display:block;font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:44px;color:#3A2E29}}
.bcard small{{display:block;font-size:24px;color:#6E5E55;margin-top:6px;direction:ltr;letter-spacing:.04em}}

.prw{{animation-name:prw;overflow:hidden}}
.prtxt{{position:absolute;top:240px;left:60px;right:60px;text-align:center;font-size:100px;font-weight:700;line-height:1.08;color:#3A2E29}}
.prtxt b{{color:#8F5A3C}}
.prtxt .eb{{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:500;letter-spacing:.28em;color:#8F5A3C;margin-bottom:22px}}

.ov{{position:absolute;left:40px;right:40px;top:250px;text-align:center;animation-name:ov}}
.ov .l{{font-size:96px;font-weight:700;line-height:1.05;color:var(--s-dark);white-space:nowrap;text-shadow:0 2px 24px rgba(250,244,238,.7)}}
.ov .s{{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;letter-spacing:.3em;font-weight:500;color:#8F5A3C;margin-bottom:18px}}
.hud{{position:absolute;top:40px;right:40px;width:540px;height:120px;box-sizing:border-box;padding:16px 26px;background:rgba(250,248,243,.92);border:1px solid #D4C9BC;display:flex;flex-direction:column;gap:6px}}
.hud .h1{{font-size:18px;font-weight:500;letter-spacing:.04em;color:var(--s-copper)}}
.hud .h2{{display:flex;flex-direction:column;gap:2px}}
.hud .h2 span:first-child{{font-family:'Cormorant Garamond',serif;font-size:32px;line-height:1;color:var(--s-ink)}}
.hud .h2 span:last-child{{font-size:21px;color:var(--s-ink)}}
{chr(10).join(css)}
</style></head>
<body><div id="stage"><div class="film stack">

<div class="intro stack" style="background:var(--s-bg)">
  <div style="position:absolute;top:120px;left:0;right:0;display:flex;flex-direction:column;align-items:center;gap:18px">
    <div class="i1" style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:500;letter-spacing:.32em;text-transform:uppercase;color:var(--s-copper)" dir="ltr">Brand Worlds Studio · Hagit Antebi</div>
    <div class="i2" style="font-size:100px;font-weight:500;line-height:1.05;color:var(--s-ink)" dir="rtl">עולם מותג <em style="font-family:'Cormorant Garamond',serif;font-weight:400;color:var(--s-gold)">No.24</em></div>
  </div>
  <div class="i3" style="position:absolute;top:1470px;left:90px;right:90px;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center" dir="rtl">
    <div style="font-size:64px;font-weight:600;line-height:1.15;color:var(--s-ink)">{BIDI} · הערכה</div>
    <div style="font-size:34px;line-height:1.5;color:var(--s-ink)">גוררים מהמדף. כל מוצר נכנס רק לצורה שלו.</div>
  </div>
</div>

<div class="outro stack" style="background:var(--s-bg)">
  <div style="position:absolute;top:110px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center">
    <div class="o1" style="font-size:28px;font-weight:500;letter-spacing:.06em;color:var(--s-copper)" dir="rtl">{BIDI} · עולם מותג No.24</div>
    <div class="o2" style="font-size:66px;font-weight:600;line-height:1.2;color:var(--s-ink)" dir="rtl">ב-{BIDI} יוצאים<br>עם ארבעה. בדיוק.</div>
  </div>
  <div class="o3" style="position:absolute;top:1430px;left:70px;right:70px;display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center">
    <div style="font-size:50px;font-weight:500;line-height:1.3;color:var(--s-copper)" dir="rtl">בואי לחוות בעצמך.</div>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;padding:22px 56px;background:var(--s-ink);color:var(--s-bg);border-radius:12px" dir="rtl"><span style="font-size:38px;font-weight:500">כתבי <b style="font-weight:700">ערכה</b> בתגובות</span><span style="font-size:24px;opacity:.85">ואשלח לך את הקישור לעולם</span></div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;letter-spacing:.3em;color:#8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</div>

<div class="marks stack">
  <div style="position:absolute;top:412px;left:240px;width:44px;height:44px;border-top:2px solid var(--s-copper);border-left:2px solid var(--s-copper)"></div>
  <div style="position:absolute;top:412px;left:796px;width:44px;height:44px;border-top:2px solid var(--s-copper);border-right:2px solid var(--s-copper)"></div>
  <div style="position:absolute;top:1387px;left:240px;width:44px;height:44px;border-bottom:2px solid var(--s-copper);border-left:2px solid var(--s-copper)"></div>
  <div style="position:absolute;top:1387px;left:796px;width:44px;height:44px;border-bottom:2px solid var(--s-copper);border-right:2px solid var(--s-copper)"></div>
</div>

<div class="world stack" style="overflow:hidden;background:#EFE4D8;box-shadow:0 50px 140px rgba(59,46,51,.26)">
 <div class="cam">
  <img class="bg" src="assets/founder-counter-full-line.webp" alt="">
  <div class="stack" style="background:linear-gradient(180deg,rgba(250,244,238,.6),rgba(250,244,238,0) 34%)"></div>
  <div class="base"></div>
  <div class="lid"><div class="scr"><div class="page">
    <div class="pnav"><div class="plogo">ORÉVA°<small>SKIN STUDIO</small></div><div class="pmenu"><span>הסיפור</span><span>הליין</span><span>לפני · אחרי</span><span>הטיפול</span><span>הערכה</span><span>הסטודיו</span></div>
      <div class="pact"><span class="pbtn">לקבוע אבחון עור</span><span class="pcart"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3A2E29" stroke-width="1.6"><path d="M6 8h12l-1 12H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg><i>4</i></span></div></div>
    <div class="phead"><div class="peb">LE COFFRET · הערכה</div><div class="ph2">ארבעה מוצרים, <b>לא שבעה.</b></div></div>
    <div class="shelfline"></div>
    {shelf_html}
    {shelf_labels}
    <div class="phint">גררי מוצר אל הערכה · או לחצי עליו</div>
    <div class="klid">ORÉVA° · LE RITUEL DU MATIN</div>
    <div class="kbox"><div class="kins"></div><div class="psleeve"><i class="band"></i><span class="card"><b>הפרוטוקול שלך</b><small>SOFT CLEANSE · CALM · EYE VEIL · COCOON CREAM</small></span></div></div>
    <div style="position:absolute;inset:0;animation-name:slotsw" class="slots">{slot_html.replace('class="slot" style="', 'class="slot" style="')}</div>
    <div class="pstatus">{status_html}</div>
    <div class="pbar"><b>₪ {kit_total}</b><span class="addb">הערכה לסל</span></div>
    <div class="toast">DEW ESSENCE לא בערכה של הבוקר. ארבעה מוצרים, לא שבעה.</div>
    {ghosts}
    <div class="dveil"></div>
    <div class="drawer"><h4>הסל שלי</h4>{drawer_rows}<div class="dtot"><span>סה״כ</span><b>₪ {kit_total}</b></div><div class="dpay">לתשלום</div></div>
    <div class="pcur"><div class="curop"><div class="hopen">{hand(False)}</div><div class="hclosed">{hand(True)}</div></div></div>
  </div></div></div>
 </div>

 <!-- signature: seven become four -->
 <div class="sig stack">
   <div class="stxt" dir="rtl"><div style="animation-name:st1">ארבעה מוצרים,</div><div style="animation-name:st2"><b>לא שבעה.</b></div></div>
   <div class="bkit"><div class="bklid">ORÉVA° · LE RITUEL DU MATIN</div><div class="bkbox"><div class="bkins"></div></div>{bslots}</div>
   {big_html}
   <div class="bkit" style="pointer-events:none"><div class="bkbox" style="background:none;box-shadow:none"><div class="bslv"><i class="band"></i><span class="bcard"><b>הפרוטוקול שלך</b><small>SOFT CLEANSE · CALM · EYE VEIL · COCOON</small></span></div></div></div>
   <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" style="overflow:visible"><defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="#8F5A3C"/><stop offset=".45" stop-color="#E2B394"/><stop offset=".6" stop-color="#B87A57"/><stop offset="1" stop-color="#8F5A3C"/></linearGradient></defs>
     <path class="rib" pathLength="1" d="{d}"/></svg>
   <div class="bead" style="offset-path:path('{d}')"></div>
 </div>

 <!-- the promise -->
 <div class="prw stack">
   <div class="stack" style="animation-name:prpush"><img class="cover" src="assets/founder-cream-on-hand.webp" alt="" style="object-position:53% 50%"></div>
   <div class="stack" style="background:linear-gradient(180deg,rgba(250,244,238,.95) 0,rgba(250,244,238,.65) 27%,rgba(250,244,238,0) 46%)"></div>
   <div class="prtxt" dir="rtl"><div class="eb" style="animation-name:prt1" dir="ltr">OR ÉVA · SKIN STUDIO</div><div style="animation-name:prt2">קודם הידיים.<br><b>אחר כך הבקבוק.</b></div></div>
 </div>
</div>

<div class="ov" dir="rtl"><div class="s" dir="ltr">ORÉVA° · LE COFFRET</div><div class="l">ערכה שבונים בגרירה.</div></div>

<div class="hook stack" style="background:var(--s-cream)">
  <div style="position:absolute;top:88px;right:80px;display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:36px;color:var(--s-dark)" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size:17px;letter-spacing:.3em;color:#8B7B6E">חגית אנטבי</div>
  </div>
  <div style="position:absolute;top:230px;left:70px;right:70px;text-align:right;font-size:80px;font-weight:600;line-height:1.16;color:var(--s-dark)" dir="rtl">שבעה מוצרים באתר,<br>והיא יוצאת <span style="color:var(--s-copper)">בלי כלום</span>?</div>
  <div class="shop" dir="rtl">
    <div class="sbar"><i></i><i></i><i></i><span>www.skincare-shop.co.il</span></div>
    <div class="shead"><span>כל המוצרים (7)</span><small>סל (0)</small></div>
    <div class="sgrid">{gcards}</div>
  </div>
  <div class="hcur">{ARROW}</div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><path class="line" pathLength="1" d="M1140 1700 H540"></path></svg>
  {BALL}
</div>

{hud_html}
<div style="position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18)"><div class="progress" style="height:6px;background:var(--s-copper)"></div></div>
</div></div></body></html>
"""
open(os.path.join(HERE, "reel.html"), "w").write(html)
print("wrote reel.html", len(html), "bytes,", len(css), "keyframes")
