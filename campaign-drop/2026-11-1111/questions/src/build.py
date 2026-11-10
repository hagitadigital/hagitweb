# Builds questions/src/questions.html — one <section> per story (1080x1920).
import pathlib, html
R = '../../../../'  # repo root from src/
S = [
 dict(id='s2', dark=True, bg='#101A24', img='card-same-product-different-price.jpg', pos='50% 45%', ih=1000, top=700,
      kick='11.11 · Question', pre='11.11. רגע של כנות:', h='כמה <em>הנחה</em><br>נתת השנה?', acc='#D9A57E',
      sub='ומה היה קורה, אם לא היית צריכה לתת?', sticker='סליידר אימוג\'י 💸', sy=1330),
 dict(id='s3', bg='#EAD7CB', img='rosee/assets/touchpoints/box-card-sans.webp', pos='50% 62%', ih=1150, top=640,
      kick='11.11 · Game', pre='משחק קטן ל-11.11:', h='בלי הנחה ובלי לוגו,<br>עדיין <em>יבחרו</em> בך?', acc='#A5555E',
      sub='<bdi>ROSÉE°</bdi> · בלי שם, בלי מבצע. רק טקס של בוקר.', sticker='סקר: כן, בטוח / עוד לא', sy=1330),
 dict(id='s5', dark=True, bg='#0E0B09', img='signe/assets/touchpoints/box-sans.webp', pos='50% 58%', ih=1250, top=600,
      kick='11.11 · Your Turn', pre='השנה, במקום עוד הנחה:', h='בונים <em>עולם</em><br>שבוחרים בו.', acc='#D4B896',
      sub='כתבי לי "עולם", ואחזור אלייך עם הצעד הראשון.', sticker='תיבת שאלה: מה המותג שלך מוכר?', sy=1300, sh=170),
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
