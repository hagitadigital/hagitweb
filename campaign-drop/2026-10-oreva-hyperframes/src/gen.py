# ORÉVA° · World 24 — 30s studio reel, built for HyperFrames (GSAP timeline, 1080×1920).
# Run: python3 gen.py  → index.html.  All timing lives in T below (seconds).
# Hook: "חוזרות אלייך לטיפול שוב ושוב. והמוצר שלך בלי מיתוג?" · Signature: "שעון העור" (DEW → CALM → GLOW).
# Music: assets/audio/morning-light-ritual.mp3 (Suno, Hagit) — 0–30s of the track; the lift at ~10s lands on the dial.
import json, os, pathlib

HERE = pathlib.Path(__file__).parent

T = dict(                # snapped to the track's beats (beats/…json, 95 bpm; bars 2.60 5.12 7.63 10.19 12.70 15.23 17.75 20.29 22.80)
    hook_out=2.60,       # bar: hook fades, studio window takes over
    win_open=4.50,       # beat before the bar: the window opens…
    win_full=5.12,       # …and is full screen on the bar
    a_line1=5.75, a_pan=(5.75, 9.54), a_line2=7.63, a_sub=8.28,
    b_in=9.85,           # the dial is up on the lift at 10.19
    b_stops=[(10.19, 12.06), (12.70, 14.60), (15.23, 16.50)],   # DEW, CALM, GLOW: each turn starts a beat early and lands on a bar
    b_payoff=16.50,
    c_in=17.75, c_seq=17.95, c_step=0.05,
    d_in=20.29, d_shots=[20.29, 21.55, 22.80],
    e_in=24.07,
    outro=27.23,
)

# Dial stops, in the site's 28-day order (01–07 DEW · 08–14 CALM · 15–28 GLOW), clockwise.
STOPS = [
    dict(key="dew", name="DEW", line="לחות שנשארת עד הערב", when="בוקר, על עור נקי, לפני קרם",
         days="01–07 · העור שותה", bg="#F1E4CB", img="assets/p-dew.webp"),
    dict(key="calm", name="CALM", line="הרגעה לעור שמגיב", when="כשהעור מבקש. אחרי שמש, אחרי טיפול",
         days="08–14 · האדמומיות נרגעת", bg="#DFCFD8", img="assets/p-calm.webp"),
    dict(key="glow", name="GLOW", line="זוהר שרואים במראה", when="ערב, אחרי ניקוי, לפני COCOON",
         days="15–28 · הזוהר שרואים במראה", bg="#EDD2C5", img="assets/p-glow.webp"),
]

SHOTS = [
    dict(img="assets/lineup-full-line-boxes.webp", pos="50% 50%", text="שבעה מוצרים, לא שבעים."),
    dict(img="assets/packaging-set-ribbon.webp", pos="34% 50%", text="סרט נחושת אחד, חמישה קודים, שלושה גוונים."),
    dict(img="assets/founder-consultation-table.webp", pos="24% 50%", text="הפגישה הראשונה היא אבחון, לא מכירה."),
]

HUD = [
    (5.6, 10.19, "01 · The Core", "קודם הידיים. אחר כך הבקבוק."),
    (10.19, 17.75, "02 · The Visual World", "שעון העור · השלישייה לפי מה שהעור מבקש"),
    (17.75, 20.29, "03 · The Element", "הפריחה: הפרח נכנס לבקבוק"),
    (20.29, 24.07, "04 · Live Site", "הליין, האריזה, האבחון"),
    (24.07, 30, "05 · The Promise", "כל מוצר יצא קודם מהידיים שלה"),
]

R = 290          # dial radius
DIAL = (540, 905)

def slot_xy(i):
    import math
    a = math.radians(-i * 120)
    return DIAL[0] + R * math.sin(a), DIAL[1] - R * math.cos(a)

# Music: set MUSIC to the instrumental file (Hagit asked for no vocals); None renders silent.
MUSIC = "assets/audio/morning-light-ritual.mp3"
AUDIO = (f'<audio id="music" class="clip" data-start="0" data-duration="30" data-volume="0.9" data-fade-out="1.4" src="{MUSIC}"></audio>'
         if MUSIC else '<!-- music: set MUSIC in gen.py -->')

# Hook variants (render-variants.sh renders each with --variables). The first is the default.
VARIANTS = {
    "h1": dict(hook="חוזרות אלייך לטיפול<br>שוב ושוב.<br>והמוצר שלך <em>בלי מיתוג</em>?",
               answer="ל-<bdi class='lat' dir='ltr' style='font-weight: 500'>Or Éva</bdi> יש ליין<br>מוצרים ממותג."),
    "h2": dict(hook="חוזרות אלייך לטיפול.<br>ואת הבקבוק קונות<br>אצל <em>מישהי אחרת</em>?",
               answer="קודם הידיים.<br>אחר כך הבקבוק. שלך."),
    "h3": dict(hook="הידיים שלך<br>כבר מותג.<br>למה <em>הבקבוק</em> עדיין לא?",
               answer="קודם הידיים.<br>אחר כך הבקבוק."),
    "h4": dict(hook="חוזרות אלייך שוב ושוב.<br>מה הן <em>לוקחות איתן</em><br>הביתה?",
               answer="ליין שנולד<br>מהידיים שלך."),
}
(HERE / "variants.json").write_text(json.dumps(VARIANTS, ensure_ascii=False, indent=2), encoding="utf-8")
DEF = VARIANTS[os.environ.get("VARIANT", "h1")]   # default copy baked into the HTML (VARIANT=h2 python3 gen.py for a check)
import html as _html
VARS_ATTR = _html.escape(json.dumps([
    dict(id="hook", type="string", label="Hook (HTML)", default=DEF["hook"]),
    dict(id="answer", type="string", label="Outro answer (HTML)", default=DEF["answer"]),
], ensure_ascii=False), quote=True)

bloom = "\n".join(
    f'<img class="bf" id="bf{k:02d}" src="assets/bloom/f{k:02d}.webp" alt="" style="object-fit: fill; opacity: {1 if k == 1 else 0}">'
    for k in range(1, 49))

slots = ""
for i, s in enumerate(STOPS):
    x, y = slot_xy(i)
    slots += f'''
    <div class="slot" style="left: {x - DIAL[0] - 100:.1f}px; top: {y - DIAL[1] - 100:.1f}px">
      <div class="medal" id="medal-{s['key']}"><img src="{s['img']}" alt=""></div>
    </div>'''

names = ""
for i, s in enumerate(STOPS):
    names += f'''
    <div class="dname" id="name-{s['key']}" style="opacity: {1 if i == 0 else 0}">
      <div class="dn" dir="ltr">{s['name']}</div>
      <div class="dl" dir="rtl">{s['line']}</div>
      <div class="dw" dir="rtl"><b>מתי:</b> {s['when']}</div>
      <div class="dd" dir="rtl">ימים {s['days']}</div>
    </div>'''

shots = ""
for i, s in enumerate(SHOTS):
    shots += f'''
    <div class="shot" id="shot{i}" style="opacity: {1 if i == 0 else 0}">
      <img class="cover push" id="push{i}" src="{s['img']}" alt="" style="object-position: {s['pos']}">
      <div class="shotband"></div>
      <div class="shottext" dir="rtl">{s['text']}</div>
    </div>'''

hud = ""
for i, (a, b, en, he) in enumerate(HUD):
    hud += f'''
      <div class="hudl" id="hud{i}" style="opacity: 0"><span class="hen" dir="ltr">{en}</span><span class="hhe">{he}</span></div>'''

html = f'''<!doctype html>
<!-- generated by gen.py — edit there, not here -->
<html lang="he" data-composition-variables="{VARS_ATTR}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1080, height=1920">
<title>ORÉVA° · עולם מותג 24 · reel</title>
<script src="assets/lib/gsap.min.js"></script>
<style>
@font-face{{font-family:'Heebo';font-weight:300;src:url('assets/fonts/heebo-hebrew-300-normal.woff2') format('woff2');unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}}
@font-face{{font-family:'Heebo';font-weight:400;src:url('assets/fonts/heebo-hebrew-400-normal.woff2') format('woff2');unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}}
@font-face{{font-family:'Heebo';font-weight:500;src:url('assets/fonts/heebo-hebrew-500-normal.woff2') format('woff2');unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}}
@font-face{{font-family:'Heebo';font-weight:600;src:url('assets/fonts/heebo-hebrew-600-normal.woff2') format('woff2');unicode-range:U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}}
@font-face{{font-family:'Heebo';font-weight:400;src:url('assets/fonts/heebo-latin-400-normal.woff2') format('woff2');unicode-range:U+0000-00FF,U+2013-2014,U+2019-201D,U+2026}}
@font-face{{font-family:'Heebo';font-weight:500;src:url('assets/fonts/heebo-latin-500-normal.woff2') format('woff2');unicode-range:U+0000-00FF,U+2013-2014,U+2019-201D,U+2026}}
@font-face{{font-family:'Heebo';font-weight:600;src:url('assets/fonts/heebo-latin-600-normal.woff2') format('woff2');unicode-range:U+0000-00FF,U+2013-2014,U+2019-201D,U+2026}}
@font-face{{font-family:'Cormorant Garamond';font-weight:400;src:url('assets/fonts/cormorant-garamond-latin-400-normal.woff2') format('woff2')}}
@font-face{{font-family:'Cormorant Garamond';font-weight:500;src:url('assets/fonts/cormorant-garamond-latin-500-normal.woff2') format('woff2')}}
@font-face{{font-family:'Cormorant Garamond';font-weight:400;font-style:italic;src:url('assets/fonts/cormorant-garamond-latin-400-italic.woff2') format('woff2')}}
@font-face{{font-family:'Cormorant Garamond';font-weight:500;font-style:italic;src:url('assets/fonts/cormorant-garamond-latin-500-italic.woff2') format('woff2')}}
@font-face{{font-family:'Plus Jakarta Sans';font-weight:400;src:url('assets/fonts/plus-jakarta-sans-latin-400-normal.woff2') format('woff2')}}
@font-face{{font-family:'Plus Jakarta Sans';font-weight:500;src:url('assets/fonts/plus-jakarta-sans-latin-500-normal.woff2') format('woff2')}}
:root{{
  --w-bg:#F6EDE6; --w-ink:#4A3530; --w-accent:#B97A63;
  --s-bg:#FAF8F3; --s-cream:#EEE6D8; --s-ink:#6B563F; --s-copper:#C4765A; --s-gold:#B8894A; --s-dark:#3E2F25;
}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--s-bg)}}
body{{font-family:'Heebo',sans-serif;color:var(--w-ink)}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;background:var(--s-bg)}}
.stack{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.cover{{position:absolute;left:0;top:0;width:100%;height:100%;object-fit:cover;display:block}}
.lat{{font-family:'Cormorant Garamond',serif}}
.jak{{font-family:'Plus Jakarta Sans',sans-serif}}
.mask{{display:block;overflow:hidden;padding-bottom:.08em}}
.mask>span{{display:block}}

/* hook */
#hook{{background:var(--s-cream);z-index:50}}
.hq{{position:absolute;top:230px;left:80px;right:80px;text-align:right;font-size:76px;font-weight:600;line-height:1.16;color:var(--s-dark)}}
.hq em{{font-style:normal;color:var(--s-copper)}}
#hTreat{{position:absolute;left:430px;top:600px;width:570px;height:740px;border-radius:26px;overflow:hidden;box-shadow:0 30px 70px rgba(62,47,37,.22)}}
.chip{{position:absolute;padding:10px 22px;border-radius:999px;font-size:26px;font-weight:500;white-space:nowrap}}
#hGeneric{{position:absolute;left:80px;top:930px;width:420px;padding:18px;background:#fff;border-radius:22px;box-shadow:0 26px 60px rgba(62,47,37,.18)}}
.line{{fill:none;stroke:#C4814F;stroke-width:4;stroke-linecap:round}}
.ball{{position:absolute;left:-52px;top:-52px;width:104px;height:104px}}
.halo{{position:absolute;inset:0;border-radius:50%;background:rgba(246,239,229,.6);border:1.5px solid #D8CCBD;box-shadow:0 10px 28px rgba(62,40,24,.28)}}
.sph{{position:absolute;left:13px;top:13px;width:78px;height:78px;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 38% 30%,#F2C9A0 0%,#C98552 32%,#8A4F28 68%,#4E2A14 100%)}}

/* studio */
#intro{{background:var(--s-bg);z-index:10}}
#outro{{background:var(--s-bg);z-index:9;opacity:0}}
.mark{{position:absolute;width:44px;height:44px;border-color:var(--s-copper);border-style:solid;border-width:0}}
#marks{{z-index:12;opacity:0}}
#world{{z-index:20;overflow:hidden;background:var(--w-bg);box-shadow:0 50px 140px rgba(59,46,51,.26);opacity:0}}
#hud{{position:absolute;top:40px;right:40px;width:540px;height:132px;padding:18px 26px;background:rgba(250,248,243,.92);border:1px solid #D4C9BC;z-index:40;opacity:0}}
.hudl{{position:absolute;left:26px;right:26px;top:46px;display:flex;flex-direction:column;gap:4px;align-items:flex-start}}
.hen{{font-family:'Cormorant Garamond',serif;font-size:34px;line-height:1;color:var(--s-ink)}}
.hhe{{font-size:22px;color:var(--s-ink)}}
#progress{{position:absolute;left:0;right:0;bottom:0;height:6px;background:rgba(196,118,90,.18);z-index:60}}

/* world scenes */
.scene{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden}}
.topfade{{position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(180deg,rgba(246,237,230,.96) 0%,rgba(246,237,230,.86) 45%,rgba(246,237,230,0) 100%)}}
.wtitle{{position:absolute;top:230px;left:80px;right:80px;text-align:right;font-size:92px;font-weight:500;line-height:1.1;color:var(--w-ink)}}
.wsub{{position:absolute;top:470px;left:80px;right:80px;text-align:right;font-size:36px;line-height:1.45;color:var(--w-ink)}}

/* dial */
#bBg{{background:#F1E4CB}}
.bglow{{position:absolute;left:90px;top:455px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(255,250,242,.85) 0%,rgba(255,250,242,0) 70%)}}
.bhead{{position:absolute;top:220px;left:70px;right:70px;text-align:center}}
.bh1{{font-size:62px;font-weight:600;line-height:1.15;color:var(--w-ink)}}
.bh2{{font-size:40px;font-weight:400;line-height:1.35;color:var(--w-ink);margin-top:8px}}
#ring{{position:absolute;left:{DIAL[0]}px;top:{DIAL[1]}px;width:0;height:0}}
.slot{{position:absolute;width:200px;height:200px}}
.medal{{width:200px;height:200px;border-radius:50%;background:radial-gradient(circle at 50% 40%,#FFFDF9 0%,#F6EEE6 100%);border:1.5px solid rgba(196,118,90,.45);box-shadow:0 18px 40px rgba(74,53,48,.18);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.medal img{{height:176px;width:auto;display:block}}
#dialsvg{{position:absolute;left:0;top:0}}
#disk{{position:absolute;left:{DIAL[0]-170}px;top:{DIAL[1]-170}px;width:340px;height:340px;border-radius:50%;overflow:hidden;border:3px solid #FBF6F0;box-shadow:0 20px 50px rgba(74,53,48,.25)}}
#disk img{{object-position:64% 52%}}
.dname{{position:absolute;top:1235px;left:60px;right:60px;display:flex;flex-direction:column;align-items:center;gap:6px;text-align:center}}
.dn{{font-family:'Cormorant Garamond',serif;font-size:104px;font-weight:500;line-height:.95;letter-spacing:.08em;color:var(--w-ink)}}
.dl{{font-size:40px;font-weight:500;color:var(--w-ink)}}
.dw{{font-size:28px;color:var(--w-ink);opacity:.85}}
.dd{{margin-top:8px;padding:8px 22px;border-radius:999px;border:1.5px solid var(--s-copper);font-size:26px;color:#8A4F33}}
#bpay{{position:absolute;top:220px;left:70px;right:70px;text-align:center;opacity:0}}

/* bloom + shots */
.bf{{position:absolute;left:0;top:0;width:3404px;height:1920px;display:block}}
.shot{{position:absolute;inset:0;overflow:hidden}}
.shotband{{position:absolute;left:0;right:0;top:0;height:700px;background:linear-gradient(180deg,rgba(246,237,230,.95) 0%,rgba(246,237,230,.8) 50%,rgba(246,237,230,0) 100%)}}
.shottext{{position:absolute;top:240px;left:80px;right:80px;text-align:right;font-size:70px;font-weight:600;line-height:1.15;color:var(--w-ink)}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1080" data-height="1920">

{AUDIO}

<!-- STUDIO · intro -->
<div id="intro" class="stack">
  <div style="position: absolute; top: 175px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 14px">
    <div id="i1" class="jak" style="font-size: 22px; font-weight: 500; letter-spacing: .32em; text-transform: uppercase; color: var(--s-copper); opacity: 0" dir="ltr">Brand Worlds Studio · Hagit Antebi</div>
    <div id="i2" style="font-size: 100px; font-weight: 500; line-height: 1.05; color: var(--s-ink); opacity: 0" dir="rtl">עולם מותג <em class="lat" style="font-weight: 400; color: var(--s-gold)">24</em></div>
  </div>
  <div id="i3" style="position: absolute; top: 1470px; left: 90px; right: 90px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center; opacity: 0" dir="rtl">
    <div style="font-size: 62px; font-weight: 600; line-height: 1.15; color: var(--s-ink)">עולם מותג קונספט</div>
    <div style="font-size: 34px; line-height: 1.45; color: var(--s-ink)">קוסמטיקאית בפרונט,<br>ואחריה ליין של שבעה מוצרים.</div>
  </div>
</div>

<!-- STUDIO · outro (answers the hook) -->
<div id="outro" class="stack">
  <div style="position: absolute; top: 175px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
    <div id="o1" style="font-size: 28px; font-weight: 500; letter-spacing: .06em; color: var(--s-copper)" dir="rtl"><bdi class="lat" dir="ltr" style="font-size: 34px">ORÉVA°</bdi> · עולם מותג 24</div>
    <div id="o2" style="font-size: 64px; font-weight: 600; line-height: 1.15; color: var(--s-ink)" dir="rtl">{DEF["answer"]}</div>
  </div>
  <div id="o3" style="position: absolute; top: 1450px; left: 70px; right: 70px; display: flex; flex-direction: column; align-items: center; gap: 24px; text-align: center">
    <div style="font-size: 54px; font-weight: 600; line-height: 1.2; color: var(--s-copper)" dir="rtl">ומה עם העסק שלך?</div>
    <div style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 22px 56px; background: var(--s-ink); color: var(--s-bg); border-radius: 12px" dir="rtl"><span style="font-size: 36px; font-weight: 500">אבחון פער המותג</span><span style="font-size: 22px; opacity: .8">30 דק׳ · בלי עלות</span></div>
    <div class="jak" style="font-size: 22px; letter-spacing: .3em; color: #8B7355" dir="ltr">HAGITANTEBI.CO.IL</div>
  </div>
</div>

<!-- STUDIO · crop marks -->
<div id="marks" class="stack">
  <div class="mark" style="top: 412px; left: 240px; border-top-width: 2px; border-left-width: 2px"></div>
  <div class="mark" style="top: 412px; left: 796px; border-top-width: 2px; border-right-width: 2px"></div>
  <div class="mark" style="top: 1387px; left: 240px; border-bottom-width: 2px; border-left-width: 2px"></div>
  <div class="mark" style="top: 1387px; left: 796px; border-bottom-width: 2px; border-right-width: 2px"></div>
</div>

<!-- WORLD -->
<div id="world" class="stack">

  <!-- A · The Core: her hands first, then the bottle (pan across the site's hands film) -->
  <section class="scene" id="sA">
    <div id="aPan" style="position: absolute; left: 0; top: 0; width: 3413px; height: 1920px">
      <video id="vHands" class="clip" data-start="2.3" data-duration="7.9" muted playsinline src="assets/hands-loop.mp4" style="position: absolute; left: 0; top: 0; width: 3413px; height: 1920px; object-fit: fill"></video>
      <svg width="3413" height="1920" viewBox="0 0 3413 1920" style="position: absolute; left: 0; top: 0" aria-hidden="true">
        <path id="aLine" class="line" style="stroke-width: 6" d="M905 1395 C1100 1600 1430 1560 1590 1260"></path>
      </svg>
      <div id="aBead" style="position: absolute; left: -17px; top: -17px; width: 34px; height: 34px; border-radius: 50%; background: radial-gradient(circle at 38% 30%,#F6D3AE 0%,#C98552 40%,#7A4220 100%); box-shadow: 0 0 18px 6px rgba(255,226,190,.7)"></div>
    </div>
    <div class="topfade"></div>
    <div class="wtitle" dir="rtl"><span class="mask"><span id="aT1">קודם הידיים.</span></span><span class="mask"><span id="aT2" style="color: var(--w-accent)">אחר כך הבקבוק.</span></span></div>
    <div class="wsub" id="aSub" dir="rtl" style="opacity: 0"><bdi class="lat" dir="ltr" style="font-size: 42px">Or Éva</bdi>, קוסמטיקאית.<br>ארבע עשרה שנה בחדר הטיפולים.</div>
  </section>

  <!-- B · signature: שעון העור -->
  <section class="scene" id="sB" style="opacity: 0">
    <div class="stack" id="bBg"></div>
    <div class="bglow"></div>
    <svg id="dialsvg" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
      <circle cx="{DIAL[0]}" cy="{DIAL[1]}" r="{R}" fill="none" stroke="#C4765A" stroke-width="2" stroke-opacity=".55"></circle>
      <circle cx="{DIAL[0]}" cy="{DIAL[1]}" r="{R + 26}" fill="none" stroke="#C4765A" stroke-width="1" stroke-opacity=".3" stroke-dasharray="2 14"></circle>
      <line x1="{DIAL[0]}" y1="{DIAL[1] - R - 150}" x2="{DIAL[0]}" y2="{DIAL[1] - R - 112}" stroke="#C4765A" stroke-width="3"></line>
    </svg>
    <div style="position: absolute; left: {DIAL[0] - 16}px; top: {DIAL[1] - R - 186}px; width: 32px; height: 32px; border-radius: 50%; background: radial-gradient(circle at 38% 30%,#F6D3AE 0%,#C98552 40%,#7A4220 100%); box-shadow: 0 0 16px 5px rgba(255,226,190,.7)"></div>
    <div id="ring">{slots}
    </div>
    <div id="disk">
      <img class="cover" src="assets/skin-before.webp" alt="">
      <img class="cover" id="skinMid" src="assets/skin-after.webp" alt="" style="opacity: 0">
    </div>
    <div class="bhead" id="bhead" dir="rtl" style="opacity: 0">
      <div class="bh1">לא בוחרים אחד לתמיד.</div>
      <div class="bh2">בוחרים לפי מה שהעור מבקש הבוקר.</div>
    </div>
    <div class="bhead" id="bpay" dir="rtl">
      <div class="bh1" style="font-size: 72px">28 ימים עם השלישייה.</div>
      <div class="bh2">אותה לחי, אותו אור. העור מספר.</div>
    </div>
    {names}
  </section>

  <!-- C · the bloom: 48 frames from the site, flower → serum -->
  <section class="scene" id="sC" style="opacity: 0">
    <div id="cPan" style="position: absolute; left: 0; top: 0; width: 3404px; height: 1920px">
    {bloom}
    </div>
    <div class="topfade"></div>
    <div class="wtitle" style="font-size: 76px" dir="rtl"><span class="mask"><span id="cT1">הפרח נכנס לבקבוק</span></span><span class="mask"><span id="cT2" style="color: var(--w-accent)">רק אחרי שהיה על העור.</span></span></div>
  </section>

  <!-- D · touchpoints -->
  <section class="scene" id="sD" style="opacity: 0">{shots}
  </section>

  <!-- E · the promise -->
  <section class="scene" id="sE" style="opacity: 0; background: radial-gradient(circle at 50% 52%,#FBF3EC 0%,#F3E2D8 60%,#EBD3C6 100%)">
    <div style="position: absolute; left: 290px; top: 1390px; width: 500px; height: 70px; border-radius: 50%; background: radial-gradient(ellipse,rgba(122,74,52,.28) 0%,rgba(122,74,52,0) 70%)"></div>
    <img id="eBottle" src="assets/p-glow.webp" alt="" style="position: absolute; left: 335px; top: 480px; width: 410px; height: auto">
    <div style="position: absolute; top: 230px; left: 70px; right: 70px; text-align: center" dir="rtl">
      <div id="eT" style="font-size: 60px; font-weight: 600; line-height: 1.18; color: var(--w-ink); opacity: 0">כל מוצר בליין<br>יצא קודם מהידיים שלי.</div>
    </div>
    <div id="eSig" class="lat" style="position: absolute; top: 1490px; left: 0; right: 0; text-align: center; font-style: italic; font-size: 52px; color: var(--w-accent); opacity: 0" dir="ltr">— Or Éva</div>
  </section>
</div>

<!-- HOOK -->
<div id="hook" class="stack">
  <div style="position: absolute; top: 110px; right: 80px; display: flex; flex-direction: column; align-items: flex-end; gap: 4px">
    <div class="lat" style="font-style: italic; font-size: 36px; color: var(--s-dark)" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size: 17px; letter-spacing: .3em; color: #8B7B6E">חגית אנטבי</div>
  </div>
  <div class="hq" id="hq" dir="rtl">{DEF["hook"]}</div>
  <div id="hTreat">
    <video id="vTreat" class="clip" data-start="0" data-duration="3.1" muted playsinline src="assets/treatment-loop.mp4" style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; object-fit: cover; object-position: 24% 50%"></video>
    <div class="chip" style="right: 20px; bottom: 22px; background: rgba(250,248,243,.94); color: var(--s-dark)" dir="rtl">הידיים שלך · כל שלושה שבועות</div>
  </div>
  <div id="hGeneric" dir="rtl">
    <div style="position: relative"><img src="assets/generic-serum.jpg" alt="" style="width: 100%; height: 400px; object-fit: cover; border-radius: 12px; display: block">
      <span class="chip" id="hChip" style="top: 14px; right: 14px; background: #2E2A27; color: #F4F2EF; font-size: 24px">בלי שם. בלי סיפור.</span></div>
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 16px; font-size: 26px; color: #6E6660"><span>המוצר שלך</span><span class="jak" style="font-size: 22px" dir="ltr">30 ml</span></div>
  </div>
  <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true">
    <path id="hLine" class="line" d="M700 1350 C690 1560 470 1600 290 1420"></path>
  </svg>
  <div class="ball" id="hBall"><div class="halo"></div><div class="sph"><div id="hRoll" style="position: absolute; inset: 0"><div style="position: absolute; left: 13px; top: 13px; width: 52px; height: 52px; border-radius: 50%; border: 1px solid rgba(250,228,200,.65)"></div><div class="lat" style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 21px; color: #F5DEC4" dir="ltr">BW</div><div style="position: absolute; left: 12px; top: 46px; width: 14px; height: 14px; border-radius: 50%; background: #FFF7EC; box-shadow: 0 0 12px 4px rgba(255,240,215,.8)"></div></div></div></div>
</div>

<!-- STUDIO · layer tag -->
<div id="hud" dir="rtl">
  <div style="font-size: 18px; font-weight: 500; letter-spacing: .04em; color: var(--s-copper)">Brand Worlds Studio · עולם מותג 24</div>{hud}
</div>

<div id="progress"><div id="progbar" style="height: 6px; background: var(--s-copper)"></div></div>

<script>
const V = (window.__hyperframes && window.__hyperframes.getVariables) ? window.__hyperframes.getVariables() : {{}};
if (V.hook) document.getElementById("hq").innerHTML = V.hook;
if (V.answer) document.getElementById("o2").innerHTML = V.answer;
const T = {json.dumps(T)};
const STOPS = {json.dumps([s["key"] for s in STOPS])};
const BG = {json.dumps([s["bg"] for s in STOPS])};
const HUD = {json.dumps([[a, b] for a, b, _, _ in HUD])};
const tl = gsap.timeline({{ paused: true, defaults: {{ ease: "power2.inOut" }} }});
const $ = id => document.getElementById(id);
const fadeIn = (el, t, d = 0.35) => tl.to(el, {{ opacity: 1, duration: d, ease: "none" }}, t);
const fadeOut = (el, t, d = 0.35) => tl.to(el, {{ opacity: 0, duration: d, ease: "none" }}, t);
const rise = (el, t, d = 0.6) => tl.fromTo(el, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: d, ease: "power3.out", immediateRender: false }}, t);
const maskIn = (el, t) => {{ gsap.set(el, {{ yPercent: 110 }}); tl.to(el, {{ yPercent: 0, duration: 0.7, ease: "power3.out" }}, t); }};

// a line drawn by a proxy, with something riding its tip (deterministic: a pure function of timeline time)
function ride(pathId, riderId, t, d, spin) {{
  const p = $(pathId), L = p.getTotalLength(), r = riderId && $(riderId), o = {{ k: 0 }};
  p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
  const draw = () => {{
    p.style.strokeDashoffset = L * (1 - o.k);
    if (r) {{ const q = p.getPointAtLength(L * o.k); r.style.transform = `translate(${{q.x}}px, ${{q.y}}px)`; }}
    if (spin) $(spin).style.transform = `rotate(${{-400 * o.k}}deg)`;
  }};
  draw();
  tl.to(o, {{ k: 1, duration: d, ease: "none", onUpdate: draw }}, t);
}}

// ── HOOK (frame 0 already shows the question + both cards) ──
ride("hLine", "hBall", 0.25, 2.1, "hRoll");
tl.fromTo("#hGeneric", {{ y: 0 }}, {{ y: -14, duration: 1.2, ease: "sine.inOut", immediateRender: false }}, 0.4);
tl.fromTo("#hChip", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }}, 2.05);
fadeOut("#hook", T.hook_out, 0.32);

// ── STUDIO window ──
gsap.set("#world", {{ scale: 0.5, y: 60, transformOrigin: "50% 46%" }});
tl.to("#world", {{ opacity: 1, y: 0, duration: 0.36, ease: "power2.out" }}, 2.52);
tl.to("#world", {{ scale: 1, duration: T.win_full - T.win_open }}, T.win_open);
tl.to("#world", {{ scale: 0.5, duration: 0.9 }}, T.outro);
fadeIn("#marks", 2.75, 0.4); fadeOut("#marks", T.win_open, 0.3); fadeIn("#marks", T.outro + 0.6, 0.5);
rise("#i1", 2.75); rise("#i2", 2.9); rise("#i3", 3.25);
fadeOut("#intro", T.win_full, 0.3);
fadeIn("#outro", T.outro + 0.25, 0.4);
rise("#o1", T.outro + 0.45); rise("#o2", T.outro + 0.75); rise("#o3", T.outro + 1.35);
fadeIn("#hud", T.win_full + 0.25, 0.4); fadeOut("#hud", T.outro, 0.3);
HUD.forEach(([a, b], i) => {{ fadeIn("#hud" + i, a, 0.2); if (b < 30) fadeOut("#hud" + i, b, 0.2); }});
gsap.set("#progbar", {{ scaleX: 0, transformOrigin: "100% 50%" }});
tl.to("#progbar", {{ scaleX: 1, duration: 30, ease: "none" }}, 0);

// ── A · hands → bottle ──
gsap.set("#aPan", {{ x: -380 }});
tl.to("#aPan", {{ x: -1064, duration: T.a_pan[1] - T.a_pan[0], ease: "sine.inOut" }}, T.a_pan[0]);
ride("aLine", "aBead", T.a_pan[0] + 0.3, T.a_pan[1] - T.a_pan[0] - 0.4);
maskIn("#aT1", T.a_line1); maskIn("#aT2", T.a_line2);
fadeIn("#aSub", T.a_sub, 0.5);

// ── B · שעון העור ──
fadeIn("#sB", T.b_in, 0.4);
fadeIn("#bhead", T.b_in + 0.35, 0.5);
const medals = STOPS.map(k => $("medal-" + k));
gsap.set(medals[0], {{ scale: 1.22 }});
T.b_stops.forEach(([a, b], i) => {{
  if (i === 0) return;
  const [pa, pb] = T.b_stops[i - 1];
  const move = a - pb;                                   // the ring turns between two holds
  tl.to("#ring", {{ rotation: 120 * i, duration: move, ease: "power3.inOut" }}, pb);
  medals.forEach(m => tl.to(m, {{ rotation: -120 * i, duration: move, ease: "power3.inOut" }}, pb));
  tl.to(medals[i - 1], {{ scale: 1, duration: move }}, pb);
  tl.to(medals[i], {{ scale: 1.22, duration: move }}, pb);
  tl.to("#bBg", {{ backgroundColor: BG[i], duration: move, ease: "none" }}, pb);
  fadeOut("#name-" + STOPS[i - 1], pb, 0.3);
  rise("#name-" + STOPS[i], a - 0.25, 0.5);
  tl.to("#skinMid", {{ opacity: i === 1 ? 0.5 : 1, duration: move, ease: "none" }}, pb);
}});
// payoff: the three serums, the skin after 28 days
fadeOut("#bhead", T.b_payoff, 0.3);
rise("#bpay", T.b_payoff + 0.2, 0.6);
tl.to("#disk", {{ scale: 1.3, duration: 0.8 }}, T.b_payoff);
medals.forEach(m => tl.to(m, {{ scale: 0.86, duration: 0.8 }}, T.b_payoff));
fadeOut("#name-" + STOPS[2], T.b_payoff + 0.1, 0.3);

// ── C · bloom ──
fadeIn("#sC", T.c_in, 0.4);
for (let k = 2; k <= 48; k++) {{
  const t = T.c_seq + (k - 2) * T.c_step, id = "#bf" + String(k).padStart(2, "0"), prev = "#bf" + String(k - 1).padStart(2, "0");
  tl.set(id, {{ opacity: 1 }}, t); tl.set(prev, {{ opacity: 0 }}, t + 0.001);
}}
gsap.set("#cPan", {{ x: -(0.64 * 3404 - 540) }});
// the bottle forms left of centre, then the site's camera settles it in the middle: follow it
tl.to("#cPan", {{ x: -(0.56 * 3404 - 540), duration: 1.15, ease: "sine.inOut" }}, T.c_seq);
tl.to("#cPan", {{ x: -(0.66 * 3404 - 540), duration: 47 * T.c_step - 0.9, ease: "sine.inOut" }}, T.c_seq + 1.15);
maskIn("#cT1", T.c_in + 0.3); maskIn("#cT2", T.c_in + 1.1);

// ── D · touchpoints ──
fadeIn("#sD", T.d_in, 0.4);
T.d_shots.forEach((t, i) => {{
  if (i > 0) fadeIn("#shot" + i, t, 0.45);
  const end = i < T.d_shots.length - 1 ? T.d_shots[i + 1] + 0.45 : T.e_in + 0.4;
  tl.fromTo("#push" + i, {{ scale: 1.08 }}, {{ scale: 1, duration: end - t + (i === 0 ? 0.4 : 0), ease: "none", immediateRender: i === 0 }}, i === 0 ? t - 0.4 : t);
}});

// ── E · the promise (calm; it stays inside the window in the outro) ──
fadeIn("#sE", T.e_in, 0.5);
tl.fromTo("#eBottle", {{ y: 26, scale: 1.04 }}, {{ y: 0, scale: 1, duration: 2.6, ease: "power2.out", immediateRender: false }}, T.e_in);
fadeIn("#eT", T.e_in + 0.5, 0.6);
fadeIn("#eSig", T.e_in + 1.4, 0.6);

tl.seek(0);
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</div>
</body>
</html>
'''

(HERE / "index.html").write_text(html, encoding="utf-8")
print("index.html written")
