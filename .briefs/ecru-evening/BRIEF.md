# ÉCRU · The Evening Edit — בריף הפקה
2026-10-07 · סטטוס: **לאישור**

## הבעיה
הבאנר "The Evening Edit" מראה חולצה לבנה וג׳ינס, לוק של יום. הקישור "בגדי ערב" בתפריט לא מוביל לשום מקום, ואין אף פריט ערב בבוטיק. ההבטחה של ÉCRU ("אותה מוזה, אינסוף לוקים") נעצרת בשש בערב.

## הרעיון
**"הקפסולה יוצאת בערב."** הערב לא בא במקום הקפסולה, הוא ממשיך אותה: כל פריט ערב מגיע עם פריט אחד מארבעת פריטי הקפסולה (חולצה לבנה · וסט · ג׳ינס · בלייזר שחור). אותה מוזה, אותו ארון, שעה אחרת.
זה גם המסר ללקוחת אופנה: עולם מותג שמחזיק גם קולקציה שנייה בלי צילום נוסף.

## מה אני בונה בקוד (אחרי שהתמונות מגיעות)
- **הבאנר** מקבל תמונת ערב אמיתית.
- **סקשן חדש `#evening`** אחרי הבאנר: 4 כרטיסי ערב. בריחוף הכרטיס מתחלף מהפריט על המדף למוזה שלובשת אותו (אותו מנגנון "מהמדף אל המוזה").
- בכל כרטיס שורת **"עם מהקפסולה:"**, שמציגה איזה פריט קפסולה משלים אותו.
- הקישור "בגדי ערב" בתפריט וכפתור "לקולקציית הערב" מובילים ל-`#evening`.

## נכסים — א׳ (9 תמונות, ChatGPT)
**רפרנס חובה לכל תמונה של המוזה:** `ecru-media/look-shirt.jpg`, בשביל הפנים, השיער והגוף.
**בדיקה לפני שליחה:** אותן פנים? אותו שיער? אם לא, לייצר שוב. זאת כל ההבטחה.

### 1 · באנר — 3:2 לרוחב (1536×1024)
`ecru-eve-banner.png`
```
Use the reference photo. Keep EXACTLY the same woman (same face, hair, body). She wears a bias-cut ecru silk slip dress, midi length, with a black tailored blazer draped over her shoulders. She stands in a warmly lit hotel lobby at dusk, travertine walls and brushed brass, golden lamp light, soft bokeh. She is on the LEFT third of the frame, three-quarter body, calm gaze off-camera; the right half is quiet travertine wall with soft light (space for text). Editorial fashion photography, muted ecru, caramel and ink-navy palette, film grain. No text, no logo. Landscape 3:2.
```

### 2 · ארבעה לוקים של ערב על המוזה — פורטרט 2:3
אותו סטודיו כמו `look-*.jpg`, כדי שהגריד ייראה כמו קולקציה אחת.

| קובץ | הלוק | עם מהקפסולה |
|---|---|---|
| `ecru-eve-slip.png` | שמלת סלִיפ משי אקרו + הבלייזר השחור על הכתפיים | הבלייזר |
| `ecru-eve-satin.png` | מכנסי סאטן רחבים בכחול-דיו + החולצה הלבנה, פתוחה בצוואר, מקופלת בשרוולים | החולצה |
| `ecru-eve-column.png` | שמלת סריג קרמל ארוכה ומחמיאה, צווארון גבוה | — (פריט עצמאי) |
| `ecru-eve-vest.png` | הווסט הבז׳ כטופ לבד (בלי חולצה) + חצאית מידי סאטן אקרו | הווסט |

פרומפט (להחליף את [LOOK]):
```
Use the reference photo. Keep EXACTLY the same woman (same face, hair, body), same studio, same warm beige backdrop and soft window light as the reference. Change only the outfit to an evening look: [LOOK]. Full-body, standing, relaxed natural pose similar to the reference, camera at waist height, centered. Simple evening touches: hair loosely tucked behind one ear, small gold earrings, minimal strappy sandals. Editorial fashion photography, muted ecru, caramel and ink-navy palette. No text, no logo. Portrait 2:3.
```
- slip: `a bias-cut ecru silk slip dress, midi length, with a black tailored blazer draped over her shoulders`
- satin: `wide-leg ink-navy satin trousers with a crisp white oversized shirt, collar open, sleeves rolled`
- column: `a long caramel fine-knit column dress with a soft high neck`
- vest: `a beige tailored waistcoat worn alone as a top, buttoned, with an ecru satin midi skirt`

### 3 · ארבעה לוקים על המדף (flat-lay) — פורטרט 2:3
בשביל ההחלפה בריחוף (מדף → מוזה). אותו סגנון כמו `flat-*.jpg`: כל הלוק מונח שטוח על רקע שמנת, פריט ליד פריט, מצולם מלמעלה.

| קובץ | מה מונח |
|---|---|
| `ecru-eve-slip-flat.png` | שמלת הסליפ + הבלייזר השחור |
| `ecru-eve-satin-flat.png` | מכנסי הסאטן + החולצה הלבנה מקופלת |
| `ecru-eve-column-flat.png` | שמלת הסריג לבד |
| `ecru-eve-vest-flat.png` | הווסט + חצאית הסאטן |

רפרנס להעלאה: `ecru-media/flat-blazer.jpg` (הרקע, האור, המרווחים).
```
Use the reference photo as the style: same plain cream background, same soft even light, same top-down flat-lay framing and generous spacing. Replace the garments with [ITEMS], each laid flat and neatly, no person, no hanger. Editorial product photography, muted ecru, caramel and ink-navy palette. No text, no logo. Portrait 2:3.
```
- slip: `an ecru bias-cut silk slip dress, midi length, beside a black tailored blazer`
- satin: `wide-leg ink-navy satin trousers below a neatly folded crisp white shirt`
- column: `a long caramel fine-knit column dress with a high neck, laid alone`
- vest: `a beige tailored waistcoat above an ecru satin midi skirt`

## נכסים — ב׳ (בונוס)
`ecru-k-eve-slip.mp4`: Kling, 5 שניות, 9:16, תמונת פתיחה `ecru-eve-slip.png`.
`She turns slowly toward the camera, the silk dress catches the light and moves softly, the blazer stays on her shoulders. Calm, elegant, editorial.`

## סדר
1. הבאנר + 4 הלוקים: בלעדיהם אין קולקציה.
2. 4 הפריטים על המדף: בלעדיהם הכרטיסים פשוט לא מתחלפים בריחוף.
3. הקליפ.
