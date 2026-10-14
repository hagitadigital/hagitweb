#!/usr/bin/env python3
"""SONAIR° · World 23 — the world's 30s studio film.

Hook: a spec table of three generic earbuds that read the same ("ככה משווים").
Signature scene: A Finish for Every Story — the five finishes on a clockwise dial; every finish that
reaches the pointer swaps the whole shot (the five stills share one composition), tints the room and
changes the name. Around it, the site's own unbroken film: earbuds float into the case, one lifts and
opens into its parts, the listening ritual, the final frame.

    python3 reels/sonair/build.py            -> reels/sonair/reel.html
    node .claude/skills/brandos-brand-world-reel/scripts/render.js reels/sonair/reel.html 30 reels/sonair/out/SONAIR-23.mp4
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TPL = ROOT / '.claude/skills/brandos-brand-world-reel/assets/reel-template.html'
D = 30.0
IMG = '../../sonair/img/'


def P(t):
    return f'{max(0, min(D, t)) / D * 100:.3f}%'


s = TPL.read_text()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


INK, SOFT, BG, SILVER = '#23262B', '#5C6370', '#F2F2F0', '#8A93A0'
CG = "font-family: 'Cormorant Garamond', serif"
FR = "font-family: 'Frank Ruhl Libre', 'Heebo', serif"
JK = "font-family: 'Plus Jakarta Sans', 'Heebo', sans-serif"
HB = "font-family: 'Heebo', sans-serif"

rep('--w-bg:#F7F0E6;', f'--w-bg:{BG};')
rep('--w-ink:#3B2E33;', f'--w-ink:{INK};')
rep('--w-accent:#C9878E;', f'--w-accent:{SILVER};')
rep('<title>Brand World Reel</title>', '<title>SONAIR° reel</title>')
rep('&amp;family=Plus+Jakarta+Sans:wght@400;500', '&amp;family=Plus+Jakarta+Sans:wght@300;400;500;600&amp;family=Frank+Ruhl+Libre:wght@300;400;500')
rep('color: var(--s-gold)">NN</em>', 'color: var(--s-gold)">23</em>')
rep('EDIT: משפט אחד על העולם, מתוך האתר.', 'אוזניות פרימיום בעולם שמצולם מזווית אחת,<br>כסרט אחד שלא נחתך.')
rep('BRAND° · עולם מותג NN', '<span dir="ltr">SONAIR°</span> · עולם מותג 23')
rep('EDIT: התשובה להוק.<br>שורה שנייה.', 'את <span dir="ltr">SONAIR°</span> לא משווים במפרט.<br><span style="color: var(--s-copper)">מרגישים</span>.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.', 'ואת העסק שלך?<br>מה מרגישים אצלך?')
s = s.replace('Brand Worlds Studio · עולם מותג NN', 'Brand Worlds Studio · עולם מותג 23')

# ── HOOK: three generic earbuds in a spec table, all the same ─────────
BUD = ('<svg viewBox="0 0 120 90" width="150" height="112" fill="none" stroke="#3A3633" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M22 30 a16 16 0 1 1 30 8 l-6 40 a6 6 0 0 1 -12 0 l-2 -34"/><path d="M98 30 a16 16 0 1 0 -30 8 l6 40 a6 6 0 0 0 12 0 l2 -34"/></svg>')
ROWS = [('ANC', ['✓', '✓', '✓']), ('סוללה', ['30 שעות', '28 שעות', '32 שעות']), ('Bluetooth', ['5.3', '5.3', '5.3']), ('מחיר', ['₪399', '₪379', '₪419'])]
cols = ''.join(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px; width: 230px">{BUD}<div style="font-size: 24px; color: #6E6660">דגם {"ABC"[i]}</div></div>' for i in range(3))
rows = ''.join(f'<div style="display: flex; align-items: center; border-top: 1px solid #ECE8E4; height: 74px"><div style="width: 150px; font-size: 24px; color: #8A827B">{k}</div>'
               + ''.join(f'<div style="width: 230px; text-align: center; font-size: 28px; color: #2E2A27; font-weight: {600 if k == "מחיר" else 400}">{v}</div>' for v in vals) + '</div>' for k, vals in ROWS)
HOPS = [(0.0, 0.6, 0), (0.6, 1.1, 2), (1.1, 1.6, 1), (1.6, 2.1, 0), (2.1, 3.2, 2)]
hops = ''.join(f'<div class="stack" data-show="{a},{b}" data-fade="0.08"><div style="position: absolute; left: {150 + (2 - i) * 230 + 10}px; top: -10px; width: 210px; bottom: -10px; '
               f'border: 4px solid var(--s-copper); border-radius: 16px"></div></div>' for a, b, i in HOPS)
HOOK_PROOF = f"""<div style="position: absolute; top: 650px; left: 80px; width: 920px; box-sizing: border-box; padding: 30px 30px 26px; background: #FFFFFF; border-radius: 22px; box-shadow: 0 24px 60px rgba(62,47,37,.14)" dir="rtl">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px"><span style="padding: 8px 20px; border-radius: 999px; background: #2E2A27; color: #F4F2EF; font-size: 24px">ככה משווים</span><span style="font-size: 24px; color: #8A827B">אוזניות אלחוטיות · 3 תוצאות</span></div>
    <div style="position: relative">
      <div style="display: flex; padding-right: 150px">{cols}</div>
      <div style="margin-top: 16px">{rows}</div>
      {hops}
    </div>
  </div>"""
i = s.index('<div class="hq"')
j = s.index('<svg class="stack" width="1080" height="1920"', i)
s = s[:i] + (f'<div style="position: absolute; top: 250px; left: 80px; right: 80px; text-align: right; font-size: 76px; font-weight: 600; '
             f'line-height: 1.18; color: var(--s-dark)" dir="rtl">למה תמיד משווים אותך<br><span style="color: var(--s-copper)">במפרט</span>?</div>\n  '
             + HOOK_PROOF + '\n\n  ') + s[j:]

# ── HUD ───────────────────────────────────────────────────────────────
tags = [('01 · The Core', 'A More Human Sound'), ('02 · A Finish for Every Story', 'גימור לכל סיפור'),
        ('03 · Inside the Extraordinary', 'כל רכיב במקומו'), ('04 · The Listening Ritual', 'ריטואל האזנה אישי'),
        ('05 · The Promise', 'סאונד אנושי יותר')]
old = ['01 · The Core', '02 · The Visual World', '03 · The Narrative', '04 · Live Site', '05 · The Promise']
for (name, line), o in zip(tags, old):
    i = s.index('>' + o + '</span>')
    s = s[:i + 1] + name + s[i + 1 + len(o):]
    k = s.index('EDIT', i)
    e = s.index('</span>', k)
    s = s[:k] + line + s[e:]
for a, b in [('data-show="9.9,14.7"', 'data-show="9.9,15.6"'), ('data-show="14.7,18.7"', 'data-show="15.6,19.5"'),
             ('data-show="18.7,22.7"', 'data-show="19.5,23.1"'), ('data-show="22.7,30"', 'data-show="23.1,30"')]:
    rep(a, b)

css = []


def kf(name, frames, timing=None):
    body = ''.join(f'{P(t)}{{{v}}}' for t, v in frames)
    t_fn = f';animation-timing-function:{timing}' if timing else ''
    css.append(f'.{name}{{animation-name:{name}{t_fn}}}@keyframes {name}{{0%{{{frames[0][1]}}}{body}100%{{{frames[-1][1]}}}}}')


def reveal(name, t, dur=.55):
    css.append(f'.{name}{{animation-name:{name}}}@keyframes {name}{{0%,{P(t)}{{transform:translateY(110%)}}{P(t + dur)},100%{{transform:none}}}}')


def seq(prefix, n, start, step, a, b, fade=.15):
    return (f'<div class="stack" data-show="{a},{b}" data-fade="{fade}"><div class="stack" data-seq="seq/{prefix}_%03d.jpg" data-from="1" data-to="{n}" '
            f'data-start="{start}" data-step="{step}"></div></div>')


GT = '<div style="position: absolute; left: 0; right: 0; top: 0; height: 560px; background: linear-gradient(to bottom, rgba(242,242,240,.94) 40%, rgba(242,242,240,0))"></div>'
GB = '<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 640px; background: linear-gradient(to top, rgba(242,242,240,.96) 46%, rgba(242,242,240,0))"></div>'
WORD = f'<div style="{CG}; font-size: 104px; font-weight: 500; letter-spacing: .26em; color: {INK}; padding-left: .26em" dir="ltr">SONAIR<sup style="font-size: .36em; vertical-align: 1.3em">°</sup></div>'

# ── A · The Core: the earbuds float down into the case ────────────────
reveal('a-l1', 6.1)
reveal('a-l2', 6.6)
A = f"""<section class="scene" data-show="0,10.1">
    {seq('t01', 31, 5.6, .12, 0, 10.2)}
    {GT}{GB}
    <div style="position: absolute; top: 200px; left: 0; right: 0; display: flex; flex-direction: column; align-items: center; gap: 12px">
      {WORD}
      <div style="{JK}; font-size: 21px; font-weight: 500; letter-spacing: .42em; color: {SOFT}" dir="ltr">PREMIUM WIRELESS EARBUDS</div>
    </div>
    <div style="position: absolute; bottom: 230px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center">
      <span class="mask"><span class="a-l1" style="display: block; {CG}; font-size: 104px; font-weight: 400; line-height: 1.05; color: {INK}" dir="ltr">A More Human Sound</span></span>
      <span class="mask"><span class="a-l2" style="display: block; {HB}; font-size: 38px; font-weight: 300; line-height: 1.5; color: {SOFT}; margin-top: 10px" dir="rtl">סאונד מדויק, נקי, ואנושי יותר.</span></span>
    </div>
  </section>"""

# ── B · A Finish for Every Story: a clockwise dial of the five finishes ──
FIN = [('c1-lunar-silver', 'Lunar Silver', 'כסף פנינתי', '#C9CDD3', '#E6E8EB'),
       ('c2-midnight-graphite', 'Midnight Graphite', 'גרפיט כהה', '#3C3F45', '#C9CBCF'),
       ('c3-soft-champagne', 'Soft Champagne', 'שמפניה רכה', '#D9C3A0', '#EFE4D3'),
       ('c4-sage-mist', 'Sage Mist', 'ירוק מרווה מעורפל', '#A9B8A6', '#DDE4DA'),
       ('c5-pearl-ivory', 'Pearl Ivory', 'שנהב פנינתי', '#ECE5D8', '#F3EEE6')]
STEPS = [10.7, 11.7, 12.7, 13.7]
MOVE, CX, CY, LR, RR = .45, 540, 1010, 300, 440


def held(name, prop, first, vals):
    fr = [(9.7, f'{prop}:{first}')]
    for k, t in enumerate(STEPS):
        fr += [(t, f'{prop}:{(first if k == 0 else vals[k - 1])}'), (t + MOVE, f'{prop}:{vals[k]}')]
    kf(name, fr)


held('b-ring', 'transform', 'rotate(0deg)', [f'rotate({72 * (k + 1)}deg)' for k in range(4)])
held('b-cr', 'transform', 'rotate(0deg)', [f'rotate({-72 * (k + 1)}deg)' for k in range(4)])
held('b-bg', 'background-color', FIN[0][4], [f[4] for f in FIN[1:]])
wins = [(9.7, STEPS[0] + .3)] + [(t + .3, (STEPS[k + 1] + .3) if k < 3 else 15.8) for k, t in enumerate(STEPS)]
shots = ''.join(f'<div class="stack" data-show="{a:.2f},{b:.2f}" data-fade="0.3"><img class="cover" src="{IMG}{f[0]}.webp" alt="" style="object-position: 62% 55%; transform: scale(1.25)"></div>'
                for f, (a, b) in zip(FIN, wins))
labels = ''.join(f'<div class="stack" data-show="{a + .1:.2f},{(b - .3) if b < 15 else b:.2f}" data-fade="0.18" style="display: flex; flex-direction: column; align-items: center; gap: 8px">'
                 f'<span style="{CG}; font-size: 72px; line-height: 1; color: {INK}" dir="ltr">{f[1]}</span><span style="{HB}; font-size: 34px; font-weight: 300; color: {SOFT}" dir="rtl">{f[2]}</span></div>'
                 for f, (a, b) in zip(FIN, wins))
sw = ''.join(f'<div style="position: absolute; left: 0; top: 0; transform: rotate({-72 * k}deg) translateY(-{RR}px) rotate({72 * k}deg)"><div class="b-cr" style="position: absolute; left: -46px; top: -46px; width: 92px; height: 92px; '
             f'border-radius: 50%; background: radial-gradient(circle at 35% 30%, #fff 0%, {f[3]} 45%, {f[3]} 70%, rgba(0,0,0,.25) 100%); box-shadow: 0 0 0 3px #fff, 0 12px 24px rgba(35,38,43,.25)"></div></div>'
             for k, f in enumerate(FIN))
reveal('b-l1', 9.9)
B = f"""<section class="scene" data-show="9.7,15.8">
    <div class="stack b-bg" style="background-color: {FIN[0][4]}"></div>
    <div style="position: absolute; left: {CX - RR}px; top: {CY - RR}px; width: {2 * RR}px; height: {2 * RR}px; border-radius: 50%; border: 2px dashed rgba(35,38,43,.25); box-sizing: border-box"></div>
    <div style="position: absolute; left: {CX - LR}px; top: {CY - LR}px; width: {2 * LR}px; height: {2 * LR}px; border-radius: 50%; overflow: hidden; box-shadow: 0 0 0 2px #fff, 0 30px 70px rgba(35,38,43,.25)">{shots}</div>
    <div class="b-ring" style="position: absolute; left: {CX}px; top: {CY}px; width: 0; height: 0">{sw}</div>
    <div style="position: absolute; top: {CY - RR - 92}px; left: {CX - 18}px; width: 0; height: 0; border-left: 18px solid transparent; border-right: 18px solid transparent; border-top: 26px solid {INK}"></div>
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center">
      <span class="mask"><span class="b-l1" style="display: block; {CG}; font-size: 80px; line-height: 1.05; color: {INK}" dir="ltr">A Finish for Every Story</span></span>
      <div data-in="10.2" style="{HB}; font-size: 36px; font-weight: 300; color: {SOFT}; margin-top: 10px" dir="rtl">גימור לכל סיפור. אותה תמונה, גימור אחר.</div>
    </div>
    <div style="position: absolute; top: 1580px; left: 40px; right: 40px; height: 160px">{labels}</div>
  </section>"""

# ── C · Inside the Extraordinary: one earbud lifts, opens into its parts ──
reveal('c-l1', 15.7)
C = f"""<section class="scene" data-show="15.5,19.7">
    {seq('t03', 31, 15.5, .06, 15.5, 17.45)}{seq('t04', 31, 17.4, .06, 17.35, 19.8)}
    {GT}{GB}
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center">
      <span class="mask"><span class="c-l1" style="display: block; {CG}; font-size: 82px; line-height: 1.05; color: {INK}" dir="ltr">Inside the Extraordinary</span></span>
      <div data-in="16.0" style="{HB}; font-size: 36px; font-weight: 300; color: {SOFT}; margin-top: 10px" dir="rtl">אוזנייה אחת נשלפת, ונפתחת לרכיבים.</div>
    </div>
    <div data-in="17.8" style="position: absolute; bottom: 260px; left: 0; right: 0; text-align: center; {JK}; font-size: 26px; letter-spacing: .3em; color: {SOFT}" dir="ltr">DRIVER · ANC CHIP · SILICONE TIP</div>
  </section>"""

# ── D · The Listening Ritual: the presenter, three signatures, a card of her own ──
SIG = [('sig-balanced', 'Balanced'), ('sig-bass', 'Bass'), ('sig-vocal', 'Vocal')]
PICK = 2
sigs = ''
for k, (f, n) in enumerate(SIG):
    on = k == PICK
    sigs += (f'<div data-in="{20.2 + k * .18:.2f}" style="width: 270px; display: flex; flex-direction: column; align-items: center; gap: 12px">'
             f'<div style="width: 270px; height: 360px; border-radius: 18px; overflow: hidden; box-shadow: {"0 0 0 4px " + INK + "," if on else ""} 0 20px 40px rgba(35,38,43,.22)"><img src="{IMG}{f}.webp" alt="" style="width: 100%; height: 100%; object-fit: cover"></div>'
             f'<span style="{CG}; font-size: 40px; color: {INK}" dir="ltr">{n}</span></div>')
kf('d-wave', [(21.4, 'stroke-dashoffset:1'), (22.4, 'stroke-dashoffset:0')], 'linear')
D_ = f"""<section class="scene" data-show="19.5,23.3">
    <div class="stack"><img class="cover" src="{IMG}s4a-presenter.webp" alt="" style="object-position: 72% 40%"></div>
    <div style="position: absolute; left: 0; right: 0; bottom: 0; height: 1180px; background: linear-gradient(to top, rgba(242,242,240,.98) 62%, rgba(242,242,240,0))"></div>
    {GT}
    <div style="position: absolute; top: 210px; left: 60px; right: 60px; text-align: center">
      <div data-in="19.6" style="{CG}; font-size: 80px; line-height: 1.05; color: {INK}" dir="ltr">Build Your Listening Ritual</div>
    </div>
    <div style="position: absolute; top: 1040px; left: 60px; right: 60px; display: flex; justify-content: space-between" dir="ltr">{sigs}</div>
    <div data-in="21.2" style="position: absolute; top: 1560px; left: 140px; right: 140px; display: flex; align-items: center; gap: 26px; padding: 22px 30px; background: #fff; border-radius: 22px; box-shadow: 0 18px 40px rgba(35,38,43,.15)" dir="rtl">
      <div style="display: flex; flex-direction: column; gap: 2px"><span style="{HB}; font-size: 24px; color: {SOFT}">הריטואל שלך</span><span style="{CG}; font-size: 44px; color: {INK}" dir="ltr">Vocal · ANC 70%</span></div>
      <svg width="300" height="60" viewBox="0 0 300 60" aria-hidden="true"><path class="d-wave" pathLength="1" stroke-dasharray="1 1" d="M0 30 C25 5 50 55 75 30 S125 5 150 30 S200 55 225 30 S275 5 300 30" fill="none" stroke="{INK}" stroke-width="3"/></svg>
    </div>
  </section>"""

# ── E · The Promise ────────────────────────────────────────────────────
reveal('e-l1', 23.5)
reveal('e-l2', 23.9)
kf('e-push', [(23.0, 'transform:scale(1.08)'), (30, 'transform:scale(1)')], 'linear')
E = f"""<section class="scene" data-show="23.0,30">
    <div class="stack"><img class="cover e-push" src="{IMG}s8-final.webp" alt="" style="object-position: 60% 50%"></div>
    {GT}{GB}
    <div style="position: absolute; top: 210px; left: 0; right: 0; display: flex; justify-content: center"><div data-in="23.1">{WORD}</div></div>
    <div style="position: absolute; bottom: 250px; left: 60px; right: 60px; display: flex; flex-direction: column; align-items: center; text-align: center">
      <span class="mask"><span class="e-l1" style="display: block; {CG}; font-size: 86px; line-height: 1.05; color: {INK}" dir="ltr">Ready for a Clearer Tomorrow?</span></span>
      <span class="mask"><span class="e-l2" style="display: block; {HB}; font-size: 38px; font-weight: 300; color: {SOFT}; margin-top: 12px" dir="rtl">סאונד שמרגישים, לא רק שומעים.</span></span>
    </div>
  </section>"""

rep("/* ── WORLD scenes: EDIT — add each scene's own motion here (percent = s/30*100) ── */", '/* ── WORLD scenes · SONAIR° ── */\n' + '\n'.join(css))
i = s.index('  <!-- A · The Core')
j = s.index('</div>\n\n<!-- HOOK')
s = s[:i] + '\n  '.join([A, B, C, D_, E]) + '\n' + s[j:]
body = re.sub(r'<!--.*?-->', '', s.split('<body')[1].split('<script>')[0], flags=re.S)
assert 'EDIT' not in body, body[body.find('EDIT') - 80:body.find('EDIT') + 40]
(HERE / 'reel.html').write_text(s)
print('ok', len(s))
