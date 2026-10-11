# ORÉVA° Backstage reel (studio mode, World 24 · Backstage) — fills the skill's reel template.
# Run: python3 gen.py  → reel.html next to this file. Render with the skill's scripts/render.js.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, '../../../../.claude/skills/brandos-brand-world-reel') + '/'
s = open(SK + 'assets/reel-template.html').read()

def p(t): return '%.3f%%' % (max(0, min(30, t)) / 30 * 100)
def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

CREAM, CREAM2, STONE, BLUSH = '#F6EFE7', '#FBF7F1', '#EADFD1', '#F5DED3'
COPPER, DEEP, LIGHT, INK, INK2 = '#B87A57', '#8F5A3C', '#D9A88A', '#3A2E29', '#6E5E55'
DEW, GLOW, CALM = '#F1D3A6', '#F0BFB0', '#D9B8C0'
FR = "font-family: 'Frank Ruhl Libre', serif"
CG = "font-family: 'Cormorant Garamond', serif"

# ── palette, fonts, titles ───────────────────────────────────────────
rep("--w-bg:#F7F0E6;", f"--w-bg:{CREAM};"); rep("--w-ink:#3B2E33;", f"--w-ink:{INK};"); rep("--w-accent:#C9878E;", f"--w-accent:{COPPER};")
rep("family=Heebo:wght@300;400;500;600", "family=Heebo:wght@300;400;500;600&amp;family=Frank+Ruhl+Libre:wght@400;500;700")
s = s.replace('<title>Brand World Reel</title>', '<title>ORÉVA Backstage reel</title>')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">24</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'עכשיו רואים מה קורה בו אחרי שהוא נבנה: טופס, לידים, הודעות, סוכנת ודשבורד.')
rep('<div style="font-size: 64px; font-weight: 600; line-height: 1.15; color: var(--s-ink)">עולם מותג קונספט</div>',
    '<div style="font-size: 64px; font-weight: 600; line-height: 1.15; color: var(--s-ink)" dir="ltr">ORÉVA° Backstage</div>')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 24 · Backstage')

# outro: the answer to the hook + the Backstage CTA
rep('BRAND° · עולם מותג NN', '<span dir="ltr">ORÉVA°</span> · עולם מותג 24 · Backstage')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'היא קיבלה תשובה תוך דקה.<br>בקול של <span dir="ltr">Or Éva</span>.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?')
rep('<span style="font-size: 36px; font-weight: 500">אבחון פער המותג</span><span style="font-size: 22px; opacity: .8">30 דק׳ · בלי עלות</span>',
    '<span style="font-size: 36px; font-weight: 500">לעבור את המסע כלקוחה</span><span style="font-size: 22px; opacity: .8" dir="ltr">hagitantebi.co.il/oreva/backstage</span>')

# ── HOOK: a generic phone, a lead at 22:14 that nobody answers ──────
rep('EDIT: למה תמיד<br>משווים אותך <span style="color: var(--s-copper)">במחיר</span>?',
    'לקוחה השאירה פרטים<br>בעשר בלילה.<br>מי <span style="color: var(--s-copper)">עונה לה</span>?')
i = s.index('<!-- proof mechanic 1'); j = s.index('<svg class="stack" width="1080"', i)
CLOCK = [('22:14', 0, .95), ('23:40', .95, 1.45), ('01:15', 1.45, 1.95), ('08:30', 1.95, 3.0)]
clock = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.05" style="display: flex; justify-content: center">{t}</div>' for t, a, b in CLOCK)
PHONE = f'''
  <!-- proof: a generic lock screen (no brand) — the lead arrives at 22:14 and is still unanswered in the morning -->
  <div style="position: absolute; top: 690px; left: 250px; width: 580px; height: 930px; box-sizing: border-box; padding: 18px; background: #2A2624; border-radius: 64px; box-shadow: 0 40px 90px rgba(42,38,36,.35)">
    <div style="position: relative; width: 100%; height: 100%; border-radius: 48px; overflow: hidden; background: linear-gradient(170deg,#5D5A60 0%,#3C3A40 55%,#2B292E 100%)">
      <div style="position: absolute; top: 70px; left: 0; right: 0; text-align: center; font-size: 26px; color: rgba(255,255,255,.75)">יום שלישי</div>
      <div style="position: absolute; top: 110px; left: 0; right: 0; height: 150px; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 132px; font-weight: 400; color: #FFFFFF; line-height: 150px" dir="ltr">{clock}</div>
      <div style="position: absolute; top: 330px; left: 26px; right: 26px; padding: 22px 24px; background: rgba(255,255,255,.88); border-radius: 26px; display: flex; flex-direction: column; gap: 6px" dir="rtl">
        <div style="display: flex; justify-content: space-between; font-size: 21px; color: #6E6A66"><span>טופס באתר · ליד חדש</span><span dir="ltr">22:14</span></div>
        <div style="font-size: 27px; font-weight: 600; color: #2A2624">נועה</div>
        <div style="font-size: 25px; line-height: 1.4; color: #2A2624">היי, רציתי לשאול על טיפול לעור רגיש. אפשר לקבוע?</div>
      </div>
      <div class="stack" data-show="1.0,3.0" data-fade="0.15" style="top: 560px; height: 60px; display: flex; justify-content: center"><span style="padding: 10px 26px; border-radius: 999px; background: rgba(196,118,90,.95); color: #FFFFFF; font-size: 24px; font-weight: 500" dir="rtl">עדיין בלי תשובה</span></div>
    </div>
  </div>
'''
s = s[:i] + PHONE + '\n  ' + s[j:]
# frame 0 is the thumbnail: question and proof are already there
rep('@keyframes hq{0%,.5%{opacity:0;transform:translateY(24px)}2.5%,100%{opacity:1;transform:none}}', '@keyframes hq{0%,100%{opacity:1}}')
rep('@keyframes hp{0%,1.5%{opacity:0;transform:scale(.94)}3.5%,100%{opacity:1;transform:none}}', '@keyframes hp{0%,100%{opacity:1}}')
rep('top: 250px; left: 80px; right: 80px; text-align: right; font-size: 76px;', 'top: 230px; left: 80px; right: 80px; text-align: right; font-size: 80px;')

# ── HUD ──────────────────────────────────────────────────────────────
TAGS = [('01 · Le formulaire', 'השאלות שלה, בקול שלה', '5.6,9.9'),
        ('02 · Les messages', 'היא בחדר הטיפולים, ההודעות יוצאות', '9.9,16.3'),
        ('03 · Le carnet', 'ליד נסגר כשהלקוחה חוזרת', '16.3,19.7'),
        ('04 · Le studio', 'הבוקר של Or Éva במסך אחד', '19.7,23.0'),
        ('05 · The Promise', 'קודם הידיים. אחר כך הבקבוק.', '23.0,30')]
OLD = [('01 · The Core', '5.6,9.9'), ('02 · The Visual World', '9.9,14.7'), ('03 · The Narrative', '14.7,18.7'),
       ('04 · Live Site', '18.7,22.7'), ('05 · The Promise', '22.7,30')]
for (name, line, win), (o, ow) in zip(TAGS, OLD):
    rep(f'data-show="{ow}"', f'data-show="{win}"')
    k = s.index('>' + o + '</span>'); s = s[:k + 1] + name + s[k + 1 + len(o):]
    e = s.index('EDIT', k); f = s.index('</span>', e); s = s[:e] + line + s[f:]

# ── WORLD SCENES ─────────────────────────────────────────────────────
css = []
def head(l1, l2, top=230, cls1='', cls2=''):
    return (f'<div style="position: absolute; top: {top}px; left: 80px; right: 80px; text-align: right; {FR}; line-height: 1.16" dir="rtl">'
            f'<div class="{cls1}" style="font-size: 84px; font-weight: 500; color: {INK}">{l1}</div>'
            f'<div class="{cls2}" style="font-size: 84px; font-weight: 700; color: {DEEP}">{l2}</div></div>')

# A · hero of the page (what shows in the studio window) → the form
HERO = f'''
  <section class="scene" data-show="0,5.9">
    <img class="cover" src="assets/founder-counter-full-line.webp" alt="" style="object-position: 34% 50%">
    <div class="stack" style="background: linear-gradient(to top, {CREAM} 0%, rgba(246,239,231,.94) 30%, rgba(246,239,231,0) 55%)"></div>
    <div style="position: absolute; top: 1230px; left: 80px; right: 80px; display: flex; flex-direction: column; align-items: flex-start; gap: 18px" dir="rtl">
      <div style="{CG}; font-size: 30px; letter-spacing: .3em; color: {COPPER}" dir="ltr">LES COULISSES · BACKSTAGE</div>
      <div style="{FR}; font-size: 118px; font-weight: 500; line-height: 1.1; color: {INK}">העולם נבנה.<br><b style="font-weight: 700; color: {DEEP}">עכשיו הוא עובד.</b></div>
    </div>
  </section>'''

def chip(txt, on=False):
    st = f'background: {COPPER}; color: #FFFFFF; border-color: {COPPER}' if on else f'background: {CREAM2}; color: {INK}; border-color: #D9C7B3'
    return f'<span style="display: inline-block; padding: 14px 28px; border: 1.5px solid; border-radius: 999px; font-size: 32px; {st}">{txt}</span>'
def chips(items, on_idx=None, on_at=None):
    base = ''.join(chip(t) for t in items)
    over = ''
    if on_idx is not None:
        over = ('<div class="stack" data-show="%s,30" data-fade="0.2" style="display: flex; flex-wrap: wrap; gap: 14px; align-content: flex-start">' % on_at +
                ''.join(chip(t, k == on_idx) if k == on_idx else f'<span style="visibility: hidden; display: inline-block; padding: 14px 28px; border: 1.5px solid; font-size: 32px">{t}</span>' for k, t in enumerate(items)) + '</div>')
    return f'<div style="position: relative; display: flex; flex-wrap: wrap; gap: 14px">{base}{over}</div>'

def bar(show):
    return f'<span style="flex: 1; height: 6px; border-radius: 6px; background: {STONE}; position: relative; overflow: hidden"><span class="stack" data-show="{show},30" data-fade="0.25" style="background: {COPPER}"></span></span>'

def toast(icon_bg, icon, head_, body, top, at):
    return (f'<div style="position: absolute; top: {top}px; left: 90px; right: 90px" data-in="{at}">'
            f'<div style="display: flex; gap: 20px; align-items: flex-start; padding: 22px 26px; background: #FFFFFF; border-radius: 26px; box-shadow: 0 24px 50px -20px rgba(58,46,41,.45)" dir="rtl">'
            f'<span style="flex: 0 0 64px; height: 64px; border-radius: 16px; background: {icon_bg}; color: #FFFFFF; display: grid; place-items: center; font-size: 30px">{icon}</span>'
            f'<div style="display: flex; flex-direction: column; gap: 4px"><span style="font-size: 23px; color: #9A8A80">{head_}</span><span style="font-size: 29px; line-height: 1.4; color: {INK}">{body}</span></div></div></div>')

FORM = f'''
  <section class="scene" data-show="5.6,10.1">
    <div class="stack" style="background: {CREAM}"></div>
    {head('השאלות שלה.', 'בקול שלה.')}
    <div style="position: absolute; top: 560px; left: 80px; right: 80px; height: 900px; box-sizing: border-box; padding: 50px 50px; background: #FFFFFF; border: 1px solid {STONE}; border-radius: 18px; box-shadow: 0 30px 70px -40px rgba(58,46,41,.4)" dir="rtl">
      <div style="display: flex; gap: 12px; margin-bottom: 44px">{bar(0)}{bar(7.0)}{bar(7.8)}</div>
      <div style="position: relative; height: 640px">
        <div class="stack" data-show="5.6,7.0" data-fade="0.2" style="display: flex; flex-direction: column; gap: 26px">
          <div style="font-size: 38px; font-weight: 500; color: {INK}">מה מעסיק אותך בעור</div>
          {chips(['יובש', 'עור עייף', 'רגישות ואדמומיות', 'סימני גיל', 'לא בטוחה, בשביל זה אני באה'], 2, 6.2)}
        </div>
        <div class="stack" data-show="7.0,7.8" data-fade="0.2" style="display: flex; flex-direction: column; gap: 26px">
          <div style="font-size: 38px; font-weight: 500; color: {INK}">מתי נוח לך</div>
          {chips(['בוקר', 'צהריים', 'אחר הצהריים', 'שישי'], 0, 7.3)}
        </div>
        <div class="stack" data-show="7.8,8.75" data-fade="0.2" style="display: flex; flex-direction: column; gap: 22px">
          <div style="font-size: 30px; font-weight: 500; color: {INK}">שם</div>
          <div style="position: relative; height: 92px; border: 1.5px solid #D9C7B3; border-radius: 10px; background: {CREAM2}"><span class="type1" style="position: absolute; right: 24px; top: 18px; font-size: 38px; color: {INK}">נועה</span></div>
          <div style="font-size: 30px; font-weight: 500; color: {INK}">טלפון</div>
          <div style="height: 92px; border: 1.5px solid #D9C7B3; border-radius: 10px; background: {CREAM2}; display: flex; align-items: center; justify-content: flex-end; padding: 0 24px; font-size: 36px; color: {INK}" dir="ltr">054-0000000</div>
          <div class="press" style="margin-top: 22px; align-self: flex-start; padding: 22px 52px; border-radius: 999px; background: {COPPER}; color: #FFFFFF; font-size: 34px; font-weight: 500">לקבוע אבחון עור</div>
        </div>
        <div class="stack" data-show="8.75,30" data-fade="0.25" style="display: flex; flex-direction: column; gap: 20px; padding-top: 40px">
          <div style="{CG}; font-size: 30px; letter-spacing: .3em; color: {COPPER}" dir="ltr">MERCI</div>
          <div style="{FR}; font-size: 74px; font-weight: 500; color: {INK}">תודה, נועה.</div>
          <div style="font-size: 34px; line-height: 1.5; color: {INK2}"><span dir="ltr">Or Éva</span> תחזור אלייך לתיאום. עד אז: אל תוסיפי שום מוצר חדש.</div>
        </div>
      </div>
    </div>
    {toast('#2AABEE', '✈', 'טלגרם · אל Or Éva', 'ליד חדש: נועה · רגישות ואדמומיות · מאינסטגרם', 1500, 8.95)}
    {toast('#25D366', '✓', 'וואטסאפ · אל נועה', 'היי נועה, כאן Or Éva. קיבלתי. אחזור אלייך עד מחר בבוקר.', 1680, 9.25)}
  </section>'''
css.append(f".type1{{animation-name:type1;animation-timing-function:steps(4,end)}}@keyframes type1{{0%,{p(8.0)}{{clip-path:inset(0 0 0 100%)}}{p(8.35)},100%{{clip-path:inset(0 0 0 0)}}}}")
css.append(f".press{{animation-name:press}}@keyframes press{{0%,{p(8.45)}{{transform:none}}{p(8.55)}{{transform:scale(.93)}}{p(8.7)},100%{{transform:none}}}}")

# B · Or Éva's clock — her hands in the centre, the system turning around them (signature scene)
CX, CY, R = 540, 1010, 370
STOPS = [  # arrive, start of next turn, ring label, word, bg, dark?, bubble head, bubble text, stage
    (9.85, 10.95, '22:14', 'הסוכנת', '#2F2622', True, 'הסוכנת · 22:14', 'CALM נולד בשביל עור שמגיב. אבל קודם מכירים את העור. לקבוע אבחון?', 0),
    (11.4, 12.25, 'יום 1', 'תיאום', '#EAD3C4', False, 'וואטסאפ · יום 1 · 09:05', 'אבחון ביום חמישי ב-10:00, רוטשילד 33. מחכה לך.', 1),
    (12.7, 13.85, 'יום 4', 'אבחון', CREAM, False, None, 'כאן המערכת שותקת.', 2),
    (14.3, 15.0, 'יום 21', 'מה השתנה?', BLUSH, False, 'וואטסאפ · יום 21', 'שלושה שבועות. מה השתנה? שלוש שאלות ואני אדע אם להחליף סרום.', 3),
    (15.45, 16.6, 'יום 28', 'חידוש', '#EFE3D3', False, 'וואטסאפ · יום 28', 'ה-CALM שלך כנראה לקראת הסוף. לשמור לך אחד בטיפול הבא?', 4),
]
n = len(STOPS); A = 360 / n
ring = f'0%,{p(STOPS[0][1])}{{transform:rotate(0deg)}}'
cr = f'0%,{p(STOPS[0][1])}{{transform:rotate(0deg)}}'
for k in range(1, n):
    nxt = p(STOPS[k][1]) if k < n - 1 else '100%'
    ring += f'{p(STOPS[k][0])},{nxt}{{transform:rotate({A * k:.0f}deg)}}'
    cr += f'{p(STOPS[k][0])},{nxt}{{transform:rotate({-A * k:.0f}deg)}}'
css.append(f'.ring{{animation-name:ring}}@keyframes ring{{{ring}}}.cr{{animation-name:cr}}@keyframes cr{{{cr}}}')
# held background + headline colours per stop (recipe 16)
bgk, h1k, h2k = [], [], []
for k, st in enumerate(STOPS):
    a = st[0] if k else 0
    b = STOPS[k + 1][1] if k < n - 1 else 30
    b = st[1]
    bgk.append(f'{p(a)},{p(b)}{{background-color:{st[4]}}}')
    h1k.append(f'{p(a)},{p(b)}{{color:{CREAM if st[5] else INK}}}')
    h2k.append(f'{p(a)},{p(b)}{{color:{LIGHT if st[5] else DEEP}}}')
bgk.append(f'100%{{background-color:{STOPS[-1][4]}}}'); h1k.append(f'100%{{color:{INK}}}'); h2k.append(f'100%{{color:{DEEP}}}')
css.append('.dbg{animation-name:dbg}@keyframes dbg{%s}.dh1{animation-name:dh1}@keyframes dh1{%s}.dh2{animation-name:dh2}@keyframes dh2{%s}' % (''.join(bgk), ''.join(h1k), ''.join(h2k)))
# the silence: ring dims, her hands come forward
css.append(f'.rdim{{animation-name:rdim}}@keyframes rdim{{0%,{p(12.6)}{{opacity:1}}{p(12.9)},{p(13.7)}{{opacity:.28}}{p(14.0)},100%{{opacity:1}}}}')
css.append(f'.hands{{animation-name:hands}}@keyframes hands{{0%,{p(12.6)}{{transform:scale(1)}}{p(13.0)},{p(13.7)}{{transform:scale(1.13)}}{p(14.1)},100%{{transform:scale(1)}}}}')

slots = ''
for k, st in enumerate(STOPS):
    slots += (f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-A * k:.0f}deg) translateY(-{R}px) rotate({A * k:.0f}deg)">'
              f'<div class="cr" style="position: absolute; left: -82px; top: -82px; width: 164px; height: 164px">'
              f'<div style="width: 164px; height: 164px; border-radius: 50%; background: {CREAM2}; border: 2px solid {COPPER}; box-shadow: 0 14px 30px rgba(58,46,41,.25); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px" dir="rtl">'
              f'<span style="font-size: 34px; font-weight: 600; color: {DEEP}">{st[2]}</span><span style="font-size: 23px; color: {INK2}">{st[3]}</span></div></div></div>')
bubbles = ''
for k, st in enumerate(STOPS):
    a = st[0] + .1 if k else 9.7
    b = STOPS[k + 1][1] + .15 if k < n - 1 else 16.8
    if st[6] is None:
        inner = f'<div style="text-align: center; {FR}; font-size: 60px; font-weight: 500; color: {INK}">{st[7]}</div><div style="text-align: center; font-size: 28px; color: {INK2}">ארבעים דקות של ידיים, אור טבעי ושאלות.</div>'
        bubbles += f'<div class="stack" data-show="{a},{b}" data-fade="0.25" style="display: flex; flex-direction: column; justify-content: center; gap: 12px" dir="rtl">{inner}</div>'
    else:
        bubbles += (f'<div class="stack" data-show="{a},{b}" data-fade="0.25" style="display: flex; align-items: center" dir="rtl">'
                    f'<div style="width: 100%; box-sizing: border-box; padding: 24px 30px; background: #FFFFFF; border-radius: 26px 26px 26px 8px; box-shadow: 0 18px 40px -22px rgba(0,0,0,.5); display: flex; flex-direction: column; gap: 6px">'
                    f'<span style="font-size: 23px; color: {COPPER}; font-weight: 500">{st[6]}</span><span style="font-size: 31px; line-height: 1.42; color: {INK}">{st[7].replace("CALM", "<span dir=ltr>CALM</span>")}</span></div></div>')
STAGES = ['חדשה', 'אבחון נקבע', 'עברה אבחון', 'בטיפול', 'בליווי']
def strip(on):
    return ''.join(f'<span style="flex: 1; text-align: center; padding: 12px 0; border-radius: 999px; font-size: 23px; {"background:" + COPPER + "; color:#FFFFFF" if j == on else "background: rgba(255,255,255,.82); color:" + INK2}">{t}</span>' for j, t in enumerate(STAGES))
strips = ''
for k, st in enumerate(STOPS):
    a = st[0] if k else 9.7
    b = STOPS[k + 1][1] + .3 if k < n - 1 else 16.8
    strips += f'<div class="stack" data-show="{a},{b}" data-fade="0.2" style="display: flex; gap: 10px" dir="rtl">{strip(st[8])}</div>'

DIAL = f'''
  <section class="scene" data-show="9.7,16.6">
    <div class="stack dbg"></div>
    {head('היא בחדר הטיפולים.', 'ההודעות יוצאות בקול שלה.', 230, 'dh1', 'dh2')}
    <div style="position: absolute; left: {CX - 250}px; top: {CY - 250}px; width: 500px; height: 500px; border-radius: 50%; overflow: hidden; box-shadow: 0 30px 70px rgba(0,0,0,.3)">
      <div class="stack hands"><img class="cover" src="assets/founder-facial-treatment.webp" alt="" style="object-position: 40% 42%"></div>
    </div>
    <svg class="stack" width="1080" height="1920" viewBox="0 0 1080 1920" aria-hidden="true"><circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{COPPER}" stroke-width="2" stroke-dasharray="4 10" opacity=".7"/></svg>
    <div class="rdim stack"><div style="position: absolute; left: {CX}px; top: {CY}px; width: 0; height: 0"><div class="ring" style="position: absolute; left: 0; top: 0; width: 0; height: 0">{slots}</div></div></div>
    <svg style="position: absolute; left: {CX - 22}px; top: {CY - R - 118}px" width="44" height="30" viewBox="0 0 44 30" aria-hidden="true"><path d="M0 0 H44 L22 30 Z" fill="{COPPER}"/></svg>
    <div style="position: absolute; top: 1520px; left: 80px; right: 80px; height: 200px">{bubbles}</div>
    <div style="position: absolute; top: 1760px; left: 60px; right: 60px; height: 60px">{strips}</div>
  </section>'''

# C · the lead board: Noa moves to "לקוחה קבועה"
def card(name, serum, tone, src, nxt, extra=''):
    return (f'<div style="box-sizing: border-box; width: 100%; padding: 20px 22px; background: #FFFFFF; border: 1.5px solid {STONE}; border-radius: 12px; display: flex; flex-direction: column; gap: 8px; {extra}" dir="rtl">'
            f'<span style="font-size: 31px; font-weight: 500; color: {INK}">{name}</span>'
            f'<span style="align-self: flex-start; padding: 2px 16px; border-radius: 999px; background: {tone}; {CG}; letter-spacing: .18em; font-size: 22px; color: {INK}" dir="ltr">{serum}</span>'
            f'<span style="font-size: 22px; color: #9A8A80">{src}</span><span style="font-size: 23px; color: {DEEP}">{nxt}</span></div>')
COLW, COLX = 300, [715, 395, 75]
def col(x, title, count, cards, final=False):
    return (f'<div style="position: absolute; left: {x}px; top: 560px; width: {COLW}px; height: 930px; box-sizing: border-box; padding: 20px 16px; border-radius: 14px; background: {BLUSH if final else STONE}" dir="rtl">'
            f'<div style="display: flex; justify-content: space-between; font-size: 27px; font-weight: 500; color: {INK}; margin-bottom: 18px"><span>{title}</span><span style="color: #9A8A80">{count}</span></div>'
            f'<div style="display: flex; flex-direction: column; gap: 14px">{cards}</div></div>')
NOA = card('נועה', 'CALM', CALM, 'רגישות ואדמומיות · אינסטגרם', 'טיפול שני · יום 40', f'border-color: {COPPER}; box-shadow: 0 0 0 2px {COPPER}, 0 20px 40px -20px rgba(58,46,41,.5)')
SPACER = '<div style="height: 196px"></div>'
BOARD = f'''
  <section class="scene" data-show="16.3,19.95">
    <div class="stack" style="background: {CREAM2}"></div>
    {head('כל פנייה נכנסת.', 'ליד נסגר כשהלקוחה חוזרת.')}
    {col(COLX[0], 'בטיפול', 1, card('רותם ל.', 'CALM', CALM, 'חברה המליצה', 'ענתה "מגיב" · להתקשר'))}
    {col(COLX[1], 'בליווי', 2, SPACER + card('מיכל ר.', 'DEW', DEW, 'אינסטגרם', 'חידוש DEW · 14.10') + card('קרן ד.', 'GLOW', GLOW, 'הסוכנת באתר', 'טיפול הבא · 29.10'))}
    {col(COLX[2], 'לקוחה קבועה', 3, SPACER + card('דנה כ.', 'GLOW', GLOW, 'חברה המליצה', 'טיפול · 22.10') + card('אורית ג.', 'CALM', CALM, 'חברה המליצה', 'חידוש CALM · 20.10'), True)}
    <div class="noamv" style="position: absolute; left: {COLX[1] + 16}px; top: 641px; width: {COLW - 32}px">{NOA}</div>
    <div style="position: absolute; top: 1560px; left: 80px; right: 80px; text-align: center" data-in="17.7" dir="rtl">
      <div style="display: inline-block; padding: 12px 30px; border-radius: 999px; background: {COPPER}; color: #FFFFFF; font-size: 28px; font-weight: 500">יום 40 · נועה חזרה לטיפול שני</div>
      <div style="margin-top: 22px; {FR}; font-size: 48px; line-height: 1.3; color: {INK}">הפעם השנייה היא מה שעולם מותג בנוי בשבילו.</div>
    </div>
  </section>'''
css.append(f".noamv{{animation-name:noamv}}@keyframes noamv{{0%,{p(16.85)}{{transform:none}}{p(17.45)},100%{{transform:translateX(-{COLX[1] - COLX[2]}px)}}}}")

# D · the dashboard: Or Éva's morning
def appt(t, name, line, on=False):
    bg = f'background: {BLUSH}; margin: 0 -14px; padding-left: 14px; padding-right: 14px; border-radius: 8px;' if on else ''
    return (f'<div style="display: flex; gap: 22px; padding: 18px 0; border-bottom: 1px solid {STONE}; {bg}" dir="rtl">'
            f'<span style="flex: 0 0 96px; font-size: 30px; font-weight: 600; color: {DEEP}; font-variant-numeric: tabular-nums">{t}</span>'
            f'<span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 31px; color: {INK}">{name}</span><span style="font-size: 23px; color: #9A8A80">{line}</span></span></div>')
def task(x, sub, hot=False):
    return (f'<div style="display: flex; gap: 16px; padding: 14px 0; border-bottom: 1px solid {STONE}" dir="rtl"><span style="flex: 0 0 26px; height: 26px; margin-top: 6px; border: 2px solid {COPPER}; border-radius: 6px"></span>'
            f'<span style="display: flex; flex-direction: column; gap: 2px"><span style="font-size: 29px; color: {DEEP if hot else INK}">{x}</span><span style="font-size: 22px; color: #9A8A80">{sub}</span></span></div>')
PCT = [('12%', 20.9, 21.2), ('34%', 21.2, 21.5), ('52%', 21.5, 21.8), ('61%', 21.8, 30)]
pct = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.03">{t}</div>' for t, a, b in PCT)
def kpi(v, l, inner=None):
    return (f'<div style="flex: 1; padding: 18px 20px; background: #FFFFFF; border: 1px solid {STONE}; border-radius: 12px" dir="rtl">'
            f'<div style="position: relative; height: 70px; {CG}; font-size: 66px; line-height: 70px; color: {INK}; font-variant-numeric: tabular-nums">{inner or v}</div>'
            f'<div style="font-size: 22px; color: #9A8A80">{l}</div></div>')
DASH = f'''
  <section class="scene" data-show="19.7,23.25">
    <div class="stack" style="background: {CREAM}"></div>
    {head('הבוקר של <span dir="ltr">Or Éva</span>.', 'הכול במסך אחד.')}
    <div style="position: absolute; top: 540px; left: 70px; right: 70px; height: 970px; box-sizing: border-box; padding: 18px; background: {INK}; border-radius: 34px">
      <div style="width: 100%; height: 100%; box-sizing: border-box; padding: 34px 40px; background: {CREAM}; border-radius: 20px; display: flex; flex-direction: column; gap: 10px" dir="rtl">
        <div style="display: flex; justify-content: space-between; align-items: baseline"><span style="{FR}; font-size: 58px; font-weight: 500; color: {INK}">בוקר טוב, <span dir="ltr">Or</span>.</span><span style="{CG}; letter-spacing: .3em; font-size: 22px; color: {COPPER}" dir="ltr">LE STUDIO</span></div>
        <div style="font-size: 27px; color: {INK2}; margin-bottom: 14px">אבחון אחד, 2 טיפולים ו-3 דברים שמחכים לך.</div>
        <div style="padding: 10px 26px; background: #FFFFFF; border: 1px solid {STONE}; border-radius: 14px" data-in="19.95">
          <div style="font-size: 22px; color: #9A8A80; padding-top: 8px">היומן של היום</div>
          {appt('09:30', 'מיכל ר.', 'טיפול · ממשיכה עם DEW')}
          {appt('10:00', 'נועה', 'אבחון · עור שמגיב לשמש ולחום', True)}
          {appt('11:30', 'שירן א.', 'אבחון · עור עייף, הרבה בשמש')}
        </div>
        <div style="padding: 10px 26px; background: #FFFFFF; border: 1px solid {STONE}; border-radius: 14px; margin-top: 8px" data-in="20.35">
          <div style="font-size: 22px; color: #9A8A80; padding-top: 8px">מה מחכה לך</div>
          {task('להתקשר לרותם ל.', 'ענתה "מגיב" בטופס מה השתנה', True)}
          {task('להציע לנועה GLOW בערב', 'ציון 4 מתוך 5 ביום 25')}
        </div>
      </div>
    </div>
    <div style="position: absolute; top: 1570px; left: 70px; right: 70px; display: flex; gap: 16px" data-in="20.7" dir="rtl">
      {kpi('29', 'לידים החודש')}{kpi('15', 'אבחונים')}{kpi('', 'חזרו לטיפול שני', pct)}
    </div>
  </section>'''

# E · the promise: her hands, then the bloom closes into the bottle (stays inside the outro window)
PROMISE = f'''
  <section class="scene" data-show="23.0,30">
    <div class="stack" data-show="23.0,24.7" data-fade="0.3"><div class="stack push"><img class="cover" src="assets/founder-cream-on-hand.webp" alt="" style="object-position: 30% 50%"></div></div>
    <div class="stack" data-show="24.5,30" data-fade="0.3" style="bottom: auto; height: 1460px; -webkit-mask-image: linear-gradient(to bottom, #000 78%, transparent 100%); mask-image: linear-gradient(to bottom, #000 78%, transparent 100%)"><div class="stack" data-seq="assets/bloom/f%02d.webp" data-from="1" data-to="48" data-by="1" data-start="24.6" data-step="0.055" data-fit="cover" data-pos="63% 50%"></div></div>
    <div class="stack" style="background: linear-gradient(to top, rgba(246,239,231,.97) 0%, rgba(246,239,231,.9) 22%, rgba(246,239,231,0) 42%)"></div>
    <div style="position: absolute; top: 1420px; left: 80px; right: 80px; text-align: center; {FR}; line-height: 1.12" dir="rtl">
      <div style="font-size: 104px; font-weight: 500; color: {INK}" data-in="23.3">קודם הידיים.</div>
      <div style="font-size: 104px; font-weight: 700; color: {DEEP}" data-in="24.9">אחר כך הבקבוק.</div>
    </div>
  </section>'''
css.append(f".push{{animation-name:push;animation-timing-function:linear}}@keyframes push{{0%,{p(23.0)}{{transform:scale(1.1)}}{p(24.8)},100%{{transform:scale(1)}}}}")

# inject scenes
i = s.index('  <!-- A · The Core'); j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + HERO + FORM + DIAL + BOARD + DASH + PROMISE + '\n' + s[j:]
rep('/* ── WORLD scenes: EDIT — add each scene\'s own motion here (percent = s/30*100) ── */',
    '/* ── WORLD scenes ── */\n' + '\n'.join(css))
import re as _re
_left = [l for l in _re.sub(r'<!--.*?-->', '', s.split('<body')[1], flags=_re.S).split('\n') if 'EDIT' in l]
assert not _left, _left[:5]
open(os.path.join(HERE, 'reel.html'), 'w').write(s)
print('wrote reel.html')
