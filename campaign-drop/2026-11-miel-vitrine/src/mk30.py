#!/usr/bin/env python3
"""Builds gen30.py (the 30s cut) from gen.py (the 18s cut): same hook, vitrine and checkout,
plus three scenes — the big cake out of the screen, the bags turning in 3D, the promise."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, "gen.py")).read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep('D = 18.0', 'D = 30.0')
rep('WORLD_CLOSE, WORLD_SMALL = 15.2, 15.75', 'WORLD_CLOSE, WORLD_SMALL = 27.2, 27.75')
rep('DRAGS = [("rose", 5.55, 5.85, 7.45), ("cacao", 8.25, 8.32, 8.78), ("citron", 9.1, 9.17, 9.63),\n         ("pistache", 9.95, 10.02, 10.48), ("fleurs", 10.8, 10.87, 11.33)]',
    'SH = 3.6\nDRAGS = [("rose", 5.55, 5.85, 7.45)] + [(c, a + SH, b + SH, r + SH) for c, a, b, r in [("cacao", 8.25, 8.32, 8.78), ("citron", 9.1, 9.17, 9.63),\n         ("pistache", 9.95, 10.02, 10.48), ("fleurs", 10.8, 10.87, 11.33)]]')
rep('CART_CLICK, PLUS_CLICK, BTN_CLICK, BTN_DONE = 13.3, 14.0, 14.5, 14.85', 'CART_CLICK, PLUS_CLICK, BTN_CLICK, BTN_DONE = 22.0, 22.7, 23.2, 23.55')
rep('(7.45, DROP), (7.7, DROP)]', '(7.45, DROP), (7.7, DROP), (11.3, DROP)]')
rep('cur += [(12.3, (95, 765)), (CART_CLICK, (95, 765)), (13.85, (975, 366)), (PLUS_CLICK + .1, (975, 366)),\n        (14.4, (806, 445)), (15.0, (806, 445))]',
    'cur += [(15.3, DROP), (21.5, (95, 765)), (CART_CLICK, (95, 765)), (22.55, (975, 366)), (PLUS_CLICK + .1, (975, 366)),\n        (23.1, (806, 445)), (24.0, (806, 445))]')
rep('win("curop", 4.75, 15.05)', 'win("curop", 4.75, 24.0)')
rep('(6.3, "transform:none"), (12.1, "transform:none"), (12.5, "transform:translateY(250px)")]',
    '(6.3, "transform:none"), (15.2, "transform:none"), (15.6, "transform:translateY(250px)")]')
rep('kf("cam", [(4.5, "transform:scale(1)"), (5.5, "transform:scale(1.28)"), (15.2, "transform:scale(1.31)")])',
    'kf("cam", [(4.5, "transform:scale(1)"), (5.5, "transform:scale(1.28)"), (24.2, "transform:scale(1.34)")])')
rep('for n, t in [("o1", 15.55), ("o2", 15.75), ("o3", 16.15)]:', 'for n, t in [("o1", 27.55), ("o2", 27.75), ("o3", 28.15)]:')
rep('kf("hud", [(4.6, "opacity:0;transform:translateY(-16px)"), (4.95, "opacity:1;transform:none"), (14.95, "opacity:1;transform:none"), (15.2, "opacity:0")])', '')
rep('kf("ov", [(4.7, "opacity:0;transform:translateY(30px)"), (5.15, "opacity:1;transform:none"), (14.95, "opacity:1;transform:none"), (15.2, "opacity:0")])',
    'kf("ov", [(4.7, "opacity:0;transform:translateY(30px)"), (5.15, "opacity:1;transform:none"), (7.95, "opacity:1;transform:none"), (8.2, "opacity:0"),'
    ' (11.4, "opacity:0"), (11.7, "opacity:1;transform:none"), (15.3, "opacity:1"), (15.55, "opacity:0"), (21.4, "opacity:0"), (21.7, "opacity:1"), (23.95, "opacity:1"), (24.2, "opacity:0")])')
rep('kf("ov2", [(11.9, "opacity:0;transform:translateY(24px)"), (12.3, "opacity:1;transform:none"), (14.95, "opacity:1;transform:none"), (15.2, "opacity:0")])',
    'kf("ov2", [(0, "opacity:0")])')

NEW = r'''
# ── 30s scenes ────────────────────────────────────────────────────────────
BC_IN, BC_OUT = 8.05, 11.3          # big cake out of the screen
R3_IN, R3_OUT = 15.55, 21.35        # bags in 3D
PR_IN = 24.15                       # the promise (stays into the outro window)
win("bcw", BC_IN + .25, BC_OUT, .3)
kf("bcake", [(BC_IN, "transform:translate(0px,243px) scale(.1);opacity:0"), (BC_IN + .05, "transform:translate(0px,243px) scale(.1);opacity:1"),
             (BC_IN + .75, "transform:none;opacity:1"), (BC_OUT - .35, "transform:scale(1.05);opacity:1"),
             (BC_OUT + .05, "transform:translate(320px,596px) scale(.08);opacity:0")])
kf("bct1", [(BC_IN + .7, "opacity:0;transform:translateY(26px)"), (BC_IN + 1.05, "opacity:1;transform:none")])
kf("bct2", [(BC_IN + 1.1, "opacity:0;transform:translateY(26px)"), (BC_IN + 1.45, "opacity:1;transform:none")])
kf("bcl", [(BC_IN + 1.5, "opacity:0;transform:scale(.6)"), (BC_IN + 1.8, "opacity:1;transform:scale(1.06)"), (BC_IN + 1.95, "opacity:1;transform:none")])
kf("bcn", [(BC_IN + 1.9, "opacity:0;transform:translateY(20px)"), (BC_IN + 2.25, "opacity:1;transform:none")])
kf("bcline", [(BC_IN + 1.7, "stroke-dashoffset:1"), (BC_IN + 2.2, "stroke-dashoffset:0")])

win("r3w", R3_IN, R3_OUT, .35)
kf("r3rise", [(R3_IN, "transform:translateY(120px) scale(.8)"), (R3_IN + .7, "transform:none")])
kf("r3ring", [(R3_IN, "transform:rotateY(60deg)"), (19.0, "transform:rotateY(-360deg)"), (19.5, "transform:rotateY(-360deg)"),
              (19.95, "transform:rotateY(-432deg)"), (20.45, "transform:rotateY(-432deg)"), (20.9, "transform:rotateY(-504deg)")])
kf("r3t1", [(R3_IN + .3, "opacity:0;transform:translateY(26px)"), (R3_IN + .65, "opacity:1;transform:none")])
kf("r3t2", [(R3_IN + .7, "opacity:0;transform:translateY(26px)"), (R3_IN + 1.05, "opacity:1;transform:none")])
R3_FRONT = [("rose", 0, 19.68), ("cacao", 19.68, 20.62), ("citron", 20.62, D)]
for cid, a, b in R3_FRONT:
    win("r3c_" + cid, a, b, .2)
for cid, a, b in [("rose", 18.85, 19.68), ("cacao", 19.88, 20.62), ("citron", 20.82, D)]:
    win("r3l_" + cid, a, b, .15)

win("prw", PR_IN, D, .4)
kf("prpush", [(PR_IN - .4, "transform:scale(1.12)"), (27.4, "transform:scale(1.02)")])
kf("prt1", [(PR_IN + .35, "opacity:0;transform:translateY(26px)"), (PR_IN + .75, "opacity:1;transform:none")])
kf("prt2", [(PR_IN + .85, "opacity:0;transform:translateY(26px)"), (PR_IN + 1.25, "opacity:1;transform:none")])

for i, (a, b) in enumerate([(4.95, 8.0), (11.6, 15.4), (15.9, 21.2), (21.6, 24.0), (24.5, 27.1)]):
    win("hud%d" % i, a, b, .25)


def stripes(cid):
    s_, h_, r_ = CAKES[cid]["code"]
    seq = [("r", 14)] + [("s", 20), ("h", 5)] * 5 + [("s", 30)]
    tot, y, st = sum(v for _, v in seq), 0, []
    col = {"r": r_, "s": s_, "h": h_}
    for k, v in seq:
        a, b = y / tot * 100, (y + v) / tot * 100
        st.append("%s %.2f%% %.2f%%" % (col[k], a, b)); y += v
    return "linear-gradient(180deg,%s)" % ",".join(st)


W3, H3, D3, R3 = 210, 240, 74, 300
HANDLES = ('<svg viewBox="0 0 210 90" width="210" height="90" style="display:block;overflow:visible">'
           '<path d="M58 92c0-50 18-78 40-78s40 28 40 78" fill="none" stroke="#C8344F" stroke-width="9" stroke-linecap="round"/>'
           '<path d="M74 92c0-50 18-78 40-78s40 28 40 78" fill="none" stroke="#B02A44" stroke-width="9" stroke-linecap="round"/></svg>')


def bag3d(cid, i):
    g = stripes(cid)
    f = "position:absolute;left:%dpx;top:%dpx;width:%dpx;height:%dpx;backface-visibility:hidden;"
    return ('<div class="slot3" style="transform:rotateY(%ddeg) translateZ(%dpx)"><div class="box3">'
            '<div style="%stransform:translateZ(%dpx);background:#F4ECE0" class="fr3"><span>MIEL°</span></div>'
            '<div style="%stransform:rotateY(180deg) translateZ(%dpx);background:#EFE6D8" class="bk3"><span>MAISON MIEL · PÂTISSERIE</span></div>'
            '<div style="%stransform:rotateY(90deg) translateZ(%dpx);background:%s"><i class="sh3"></i></div>'
            '<div style="%stransform:rotateY(-90deg) translateZ(%dpx);background:%s"><i class="sh3"></i></div>'
            '<div style="%stransform:rotateX(90deg) translateZ(%dpx);background:#D9CBB8"></div>'
            '<div style="position:absolute;left:%dpx;top:%dpx;transform:translateZ(%dpx)">%s</div>'
            '<div style="position:absolute;left:%dpx;top:%dpx;transform:translateZ(%dpx)">%s</div>'
            '</div></div>') % (
        i * 72, R3,
        f % (-W3 // 2, -H3 // 2, W3, H3), D3 // 2,
        f % (-W3 // 2, -H3 // 2, W3, H3), D3 // 2,
        f % (-D3 // 2, -H3 // 2, D3, H3), W3 // 2, g,
        f % (-D3 // 2, -H3 // 2, D3, H3), W3 // 2, g,
        f % (-W3 // 2, -D3 // 2, W3, D3), H3 // 2,
        -W3 // 2, -H3 // 2 - 88, D3 // 2 - 10, HANDLES,
        -W3 // 2, -H3 // 2 - 88, -(D3 // 2 - 10), HANDLES)


ORDER3 = ["rose", "cacao", "citron", "pistache", "fleurs"]
ring3 = "".join(bag3d(c, i) for i, c in enumerate(ORDER3))
cakes3 = "".join('<img src="assets/%s" alt="" class="c3" style="animation-name:r3c_%s">' % (CAKES[c]["whole"], c) for c, _, _ in R3_FRONT)
labels3 = "".join('<div class="l3" style="animation-name:r3l_%s"><b>%s</b> <bdi dir="ltr"><span>%s</span></bdi><small>%s</small></div>' % (c, CAKES[c]["he"], CAKES[c]["fr"], CAKES[c]["line"]) for c in ["rose", "cacao", "citron"])

SCENES = f"""
 <!-- 30s · the big cake comes out of the screen -->
 <div class="bcw stack" style="animation-name:bcw">
   <div class="stack" style="background:radial-gradient(ellipse at 50% 58%,rgba(253,246,242,.97),rgba(243,224,219,.96) 70%);backdrop-filter:blur(12px)"></div>
   <div class="bctxt" dir="rtl"><div style="animation-name:bct1">פרוסה אחת בוויטרינה.</div><div style="animation-name:bct2;color:#B8606A">עוגה שלמה בשקית.</div></div>
 </div>
 <img class="bcake" src="assets/sig-rose.webp" alt="">
 <div class="bcw stack" style="animation-name:bcw;pointer-events:none">
   <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920"><path class="bcline" pathLength="1" d="M330 1330 C400 1300 430 1270 470 1230" fill="none" stroke="#B8956A" stroke-width="3" stroke-dasharray="1 1" style="animation-name:bcline"/></svg>
   <div class="bcl" style="animation-name:bcl"><img src="assets/slice-rose.webp" alt=""><span>מה שבפנים</span></div>
   <div class="bcn" dir="rtl" style="animation-name:bcn"><b>הוורודה</b> <bdi dir="ltr"><span>La Rose</span></bdi><small>ביסקוויט וניל · לב פטל · רובּ ורוד־אומברה</small></div>
 </div>

 <!-- 30s · the bags turn in 3D around the cake -->
 <div class="r3w stack" style="animation-name:r3w">
   <img class="cover" src="assets/12-still-table-empty.webp" alt="" style="object-position:50% 50%">
   <div class="stack" style="background:linear-gradient(180deg,rgba(250,240,236,.75),rgba(250,240,236,0) 38%)"></div>
   <div class="r3txt" dir="rtl"><div style="animation-name:r3t1">חמש עוגות. חמש שקיות.</div><div style="animation-name:r3t2" class="sub">כל דופן היא החתך שלה.</div></div>
   <div class="r3floor"></div>
   <div class="r3rise" style="animation-name:r3rise">
     <div class="r3root"><div class="r3tilt">
       <div class="r3cake">{cakes3}</div>
       <div class="r3ring" style="animation-name:r3ring">{ring3}</div>
     </div></div>
   </div>
   <div class="r3lab" dir="rtl">{labels3}</div>
 </div>

 <!-- 30s · the promise -->
 <div class="prw stack" style="animation-name:prw;overflow:hidden">
   <div class="stack" style="animation-name:prpush"><img class="cover" src="assets/08-still-slice-pink-topper.webp" alt="" style="object-position:40% 50%"></div>
   <div class="stack" style="background:linear-gradient(180deg,rgba(250,240,236,.92) 0,rgba(250,240,236,.6) 26%,rgba(250,240,236,0) 46%)"></div>
   <div class="prtxt" dir="rtl"><div class="eb" style="animation-name:prt1" dir="ltr">MIEL° · ROMANTIQUE DE L'INTÉRIEUR</div><div style="animation-name:prt2">רומנטיקה<br>מתחילה מבפנים.</div></div>
 </div>
"""

CSS30 = """
.bctxt{position:absolute;top:250px;left:60px;right:60px;text-align:center;font-size:84px;font-weight:700;line-height:1.12;color:#3E2F25}
.bctxt div{animation-fill-mode:both}
.bcake{position:absolute;left:160px;top:560px;width:760px;height:957px;object-fit:contain;animation-name:bcake;filter:drop-shadow(0 40px 40px rgba(74,44,36,.28))}
.bcl{position:absolute;left:50px;top:1220px;width:290px;text-align:center;transform-origin:50% 50%}
.bcl img{width:290px;height:290px;object-fit:cover;border-radius:50%;border:6px solid #fff;box-shadow:0 0 0 1px rgba(184,149,106,.5),0 24px 40px -20px rgba(74,44,36,.5)}
.bcl span{display:block;margin-top:12px;font-size:28px;font-weight:600;color:#B8956A}
.bcn{position:absolute;left:380px;right:60px;top:1560px;text-align:center;color:#3E2F25}
.bcn b{font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:70px}
.bcn span{margin-right:16px;font-family:'Cormorant Garamond',serif;font-size:42px;color:#B8956A}
.bcn small{display:block;font-size:28px;opacity:.8;margin-top:6px}
.r3txt{position:absolute;top:240px;left:60px;right:60px;text-align:center;font-size:86px;font-weight:700;line-height:1.1;color:#3E2F25}
.r3txt .sub{font-size:48px;font-weight:500;margin-top:14px;color:#6B3A36}
.r3floor{position:absolute;left:110px;top:1515px;width:860px;height:140px;border-radius:50%;background:radial-gradient(closest-side,rgba(74,44,36,.30),transparent)}
.r3rise{position:absolute;left:0;top:0;width:1080px;height:1920px}
.r3root{position:absolute;left:540px;top:1265px;width:0;height:0;perspective:1700px;perspective-origin:0 -200px}
.r3tilt{position:absolute;left:0;top:0;transform-style:preserve-3d;transform:rotateX(-11deg)}
.r3ring{position:absolute;left:0;top:0;transform-style:preserve-3d}
.slot3{position:absolute;left:0;top:0;transform-style:preserve-3d}
.box3{position:absolute;left:0;top:0;transform-style:preserve-3d}
.fr3 span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-weight:600;font-size:34px;letter-spacing:.2em;color:#B8956A}
.bk3 span{position:absolute;left:0;right:0;bottom:22px;text-align:center;font-family:'Cormorant Garamond',serif;font-size:12px;letter-spacing:.24em;color:#B8956A}
.sh3{position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.10),rgba(0,0,0,0) 60%)}
.r3cake{position:absolute;left:-230px;top:-330px;width:460px;height:579px;transform:rotateX(11deg) translateZ(0)}
.c3{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 30px 30px rgba(74,44,36,.25))}
.r3lab{position:absolute;left:60px;right:60px;top:1680px;height:160px;text-align:center;color:#3E2F25}
.l3{position:absolute;inset:0}
.l3 b{font-family:'Frank Ruhl Libre',serif;font-weight:500;font-size:62px}
.l3 span{margin-right:16px;font-family:'Cormorant Garamond',serif;font-size:38px;color:#9A6A3E}
.l3 small{display:block;font-size:28px;margin-top:6px}
.prtxt{position:absolute;top:230px;left:60px;right:60px;text-align:center;font-size:96px;font-weight:700;line-height:1.08;color:#3E2F25}
.prtxt .eb{font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:500;letter-spacing:.28em;color:#9A4E35;margin-bottom:22px}
"""
'''
rep('# ── generic shop for the hook', NEW + '\n# ── generic shop for the hook')
rep('  {table_html}\n </div>\n', '  {table_html}\n </div>\n{SCENES}\n')
rep('{chr(10).join(css)}\n</style>', '{chr(10).join(css)}\n{CSS30}\n</style>')

HUDS = r'''{"".join('<div class="hud" style="animation-name:hud%d;position:absolute;top:40px;right:40px;width:540px;height:120px;box-sizing:border-box;padding:16px 26px;background:rgba(250,248,243,.92);border:1px solid #D4C9BC;display:flex;flex-direction:column;gap:6px" dir="rtl"><div style="font-size:18px;font-weight:500;letter-spacing:.04em;color:var(--s-copper)">Brand Worlds Studio · עולם מותג No.27</div><div style="display:flex;flex-direction:column;gap:2px"><span style="font-family:\'Cormorant Garamond\',serif;font-size:32px;line-height:1;color:var(--s-ink)" dir="ltr">%s</span><span style="font-size:21px;color:var(--s-ink)">%s</span></div></div>' % (i, a, b) for i, (a, b) in enumerate([("04 · Live Site", "הוויטרינה: גוררים פרוסה, מקבלים עוגה"), ("04 · Live Site", "חמש פרוסות, חמש שקיות"), ("02 · The Visual World", "השקית: הדופן היא החתך"), ("04 · Live Site", "הקופה: מתי הרגע המתוק?"), ("05 · The Promise", "רומנטיקה מתחילה מבפנים")]))}'''
i = s.index('<div class="hud" style="position:absolute;top:40px;right:40px;width:520px')
j = s.index('</div>\n</div>\n', i) + len('</div>\n</div>\n')
s = s[:i] + HUDS + '\n' + s[j:]
rep('open(os.path.join(HERE, "reel.html"), "w").write(html)', 'open(os.path.join(HERE, "reel30.html"), "w").write(html)')
open(os.path.join(HERE, "gen30.py"), "w").write(s)
print("wrote gen30.py")
