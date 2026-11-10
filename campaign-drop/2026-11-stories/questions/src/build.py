# Builds questions/src/questions.html — one <section> per story (1080x1920).
import pathlib, html
R = '../../../../'  # repo root from src/
S = [
 dict(id='q1', bg='#EFE6DA', img='encore/assets/touchpoints/bags-four-sans.webp', pos='50% 60%', ih=1180, top=710,
      kick='Question 01', pre='משחק קטן:', h='אם נסתיר את הלוגו,<br>עדיין <em>יזהו</em> אותך?', acc='#9A5B3C',
      sub='ארבע שקיות. בלי שם, בלי לוגו.', sticker='סקר: כן, מיד / עוד לא', sy=1300),
 dict(id='q2', bg='#EFE6DA', img='encore/assets/touchpoints/bags-four.webp', pos='50% 60%', ih=1180, top=710,
      kick='The Answer', pre='זיהית?', h='הצבעים <em>אמרו</em><br>את השם קודם.', acc='#9A5B3C',
      sub='<bdi>ENCORE°</bdi> · ארבע שעות ביום, ארבעה צבעים. הלוגו הוא רק חתימה.', sticker='קישור: לעולם ENCORE°', sy=1300),
 dict(id='q3', kind='ab', bg='#E4E9F0', a='velune/assets/10-bottle-aube-day-m.webp', b='velune/assets/09-bottle-blush-garden-m.webp',
      la='AUBE', lb='BLUSH', kick='This or That', pre='אותו בקבוק. שני בקרים.', h='איזה מהם<br><em>שלך</em>?', acc='#8E2E4E',
      sub='<bdi>VELUNE° Maison de Parfum</bdi>', sticker='סקר: Aube / Blush', sy=1380, sh=120),
 dict(id='q4', bg='#F3E6D4', img='chasen/img/glass_fraise.webp', pos='50% 30%', ih=1400, top=670, narrow=True,
      kick='CHASEN° 01', pre='לפני הכוס, היה משפט:', h='מאצ\'ה לא מזמינים.<br><em>מרכיבים.</em>', acc='#4F7A34',
      sub='מאצ\'ה עם תות. כן או ממש לא?', sticker='סליידר אימוג\'י 🍓', sy=1330),
 dict(id='q5', bg='#E3DCCB', img='elvea/assets/img/collection-lineup.webp', pos='50% 50%', ih=1100, top=790, wide=True,
      kick='Question 02', pre='כנות, רגע:', h='מה גורם לך<br><em>לקנות</em>?', acc='#4E6A3A',
      sub='כשיש שני מוצרים טובים באותו מחיר.', sticker='סקר: המחיר / הסיפור', sy=1320),
 dict(id='q6', dark=True, bg='#0E0B09', img='signe/assets/touchpoints/box-sans.webp', pos='50% 55%', ih=1300, top=710,
      kick='Question 03', pre='בלי לחשוב יותר מדי:', h='קונים את הקופסה,<br>או את <em>מה שבפנים</em>?', acc='#D4B896',
      sub='<bdi>SIGNÉ°</bdi> · קופסה שחורה, וחוט זהב אחד.', sticker='סקר: את הקופסה / את מה שבפנים', sy=1330),
 dict(id='q7', bg='#E6DBCC', img='pardon-me/assets/hero.webp', pos='52% 50%', ih=1150, top=810, wide=True,
      kick='Your Turn', pre='לפני הקופסה, היה משפט:', h='מה המשפט<br>של <em>המותג שלך</em>?', acc='#8C2340',
      sub='<bdi>PARDON ME°</bdi> · "מנומס מבחוץ. לא מתנצל מבפנים."', sticker='תיבת שאלה: כתבי לי את המשפט', sy=1270, sh=230),
 dict(id='q8', bg='#EBD3CA', img='miel/assets/41-slice-vanille-framboise-m.webp', pos='50% 60%', ih=1250, top=750, wide=True,
      kick='MIEL° 27', pre='רואים מה שבפנים:', h='כמה בא לך<br><em>עכשיו</em>?', acc='#B0475E',
      sub='וניל ופטל. חתך אחד, ארבע שכבות.', sticker='סליידר אימוג\'י 🍰', sy=1330),
]
css = open(pathlib.Path(__file__).with_name('style.css')).read()
out = ['<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">',
 '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Heebo:wght@300;400;500;700;800&display=swap" rel="stylesheet">',
 f'<style>{css}</style></head><body>']
for s in S:
    dark = ' dark' if s.get('dark') else ''
    o = [f'<section class="s{dark}" id="{s["id"]}" style="--bg:{s["bg"]};--acc:{s["acc"]}">']
    if s.get('kind') == 'ab':
        o.append(f'<div class="ab"><figure><div class="ph" style="background-image:url({R}{s["a"]})"></div><figcaption>A · {s["la"]}</figcaption></figure>'
                 f'<figure><div class="ph" style="background-image:url({R}{s["b"]})"></div><figcaption>B · {s["lb"]}</figcaption></figure></div>')
    else:
        o.append(f'<div class="img" style="top:{s["top"]}px;height:{s["ih"]}px;background-image:url({R}{s["img"]});background-position:{s["pos"]}"></div>')
    o.append('<header><div class="brand"><b>Brand Worlds Studio</b><span>חגית אנטבי</span></div>'
             f'<div class="kick">{s["kick"]}</div></header>')
    o.append(f'<div class="head"><p class="pre">{s["pre"]}</p><h1>{s["h"]}</h1><p class="sub">{s["sub"]}</p></div>')
    o.append(f'<div class="sticker" style="top:{s["sy"]}px;height:{s.get("sh",150)}px">{html.escape(s["sticker"])}</div>')
    o.append('<footer><span class="site">hagitantebi.co.il</span><span class="cta"><i></i>ענו לי ←</span></footer></section>')
    out.append(''.join(o))
out.append('</body></html>')
pathlib.Path(__file__).with_name('questions.html').write_text('\n'.join(out), encoding='utf-8')
print([s['id'] for s in S])
