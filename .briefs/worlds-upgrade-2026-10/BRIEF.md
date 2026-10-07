# שדרוג ÉTAGE° · ORBE · ÉCRU — בריף הפקה
2026-10-03 · סטטוס: **טיוטה לאישור**
החלוקה: **את מכינה** תמונות ב-ChatGPT וסרטונים ב-Kling (ב-Higgsfield אין קרדיטים). **אני בונה** כל מה שלא דורש נכסים: מנגנונים, קוד, טקסטים, ספר מותג, הרכבת הסרט.
היעד: שלושת העולמות יעמדו ברף של ENCORE° · ROSÉE° · MIEL°:
- **מנגנון אחד** שהגולשת *עושה*.
- **סרט של 30 שניות** (720×1280, בלי סאונד).
- **נקודות מגע** (אריזה, שלט, כרטיס).
- **ספר מותג מקוצר.**

---

## איך מוסרים נכסים
- **העלאה:** פשוט מעלים כאן בשיחה, עם **שם הקובץ מהטבלה**. אני ממירה ל-webp, חותכת, מכווצת ומכניסה למקום.
- **ChatGPT — תמונה:** לבקש **פורטרט 2:3** (1024×1536), אלא אם כתוב אחרת. לכל פרומפט מצורף **קובץ רפרנס** מהאתר. להעלות אותו יחד עם הפרומפט, זה מה ששומר על אותו עולם.
- **Kling — וידאו:** image-to-video, **5 שניות**, **9:16**, מצב Professional אם יש, בלי סאונד. תמונת הפתיחה היא תמיד תמונה קיימת או תמונה שהכנת ב-ChatGPT (כתוב בכל שורה).
- **כללים לכל התמונות:** בלי טקסט ובלי לוגו בתוך התמונה (אני מוסיפה בקוד). בלי ידיים מעוותות: אם יוצאת יד לא טובה, עדיף לייצר שוב. אור טבעי רך מהצד.
- **סדר עדיפויות בכל עולם:** **א׳** = בלי זה המנגנון לא קיים. **ב׳** = סרט ונקודות מגע. **ג׳** = בונוס.

---

## 1 · ÉTAGE° — מעוגה יפה ל**עוגה של החתונה שלך**

### הבעיה
ÉTAGE° ו-MIEL° הם שני עולמות עוגות, ו-MIEL° החדש כבר עושה "בונה עוגה + חתך". ÉTAGE° צריך להיות **החתונה**, לא העוגה.

### הרעיון
**"העוגה מתלבשת כמו הכלה."** הכלה בוחרת את השמלה שלה ואת מספר האורחים, והעוגה נבנית מהבד של השמלה: טול הופך לסלסולים, סאטן לחלק עם וילון, תחרה לזילוף תחרה, קפלים לקפלים. זה ממשיך את ההבטחה שכבר קיימת בהירו ("The Dress — גללו והיא מתלבשת") ולוקח אותה צעד אחד קדימה: מהעוגה **שלנו** לעוגה **שלך**.

### מה אני בונה בקוד (בלי נכסים)
- **סקשן חדש "La Robe"** במקום האטלייה הנוכחית (ארבע העוגות המוכנות עוברות לקולקציה).
  - 4 כרטיסי בד לבחירה.
  - סליידר אורחים: עד 80 = עוגה אינטימית, 150 ומעלה = עוגה גדולה.
  - העוגה מתחלפת ב-crossfade, ושורת סיכום מתעדכנת: "שמלת סאטן · 140 אורחים · 4 קומות · וילון סוכר".
- **CTA "לקבוע טעימה"** עם הסיכום בתוך הודעת וואטסאפ.
- **מיצוב בטקסטים:** "Couture Wedding Cakes" מול MIEL "Pâtisserie". עדכון כרטיסי השכנים.
- **ספר מותג מקוצר** `etage/brand-book.html`, באותו פורמט כמו ENCORE°.

### נכסים — א׳ (המנגנון)
**4 בדי שמלה** — תקריב של בד בלבד, בלי כלה ובלי פנים. ריבוע 1:1.
רפרנס להעלאה: `etage/assets/cake-photo.webp` (בשביל האור והגוון).

| קובץ | הבד |
|---|---|
| `etage-fabric-tulle.png` | טול שכבות (נסיכה) |
| `etage-fabric-satin.png` | סאטן משיי עם וילון (מינימליסטית) |
| `etage-fabric-lace.png` | תחרה צרפתית על טול (בוהו/קלאסית) |
| `etage-fabric-pleat.png` | קרפ עם קפלים אנכיים (מודרנית) |

פרומפט (להחליף את [FABRIC] בכל פעם):
```
Extreme close-up of an ivory bridal gown fabric: [FABRIC]. The fabric fills the whole frame, softly folded, photographed like a couture atelier detail shot. Warm soft window light from the left, gentle shadows, creamy ivory and blush tones matching the reference image. No person, no face, no hands, no text. Square 1:1, high detail, editorial, calm.
```
- tulle: `layers of fine ivory silk tulle gathered in soft ruffles`
- satin: `heavy ivory silk satin with one long fluid drape`
- lace: `delicate ivory Chantilly lace with a scalloped edge over sheer tulle`
- pleat: `structured ivory crepe with crisp vertical knife pleats`

**8 עוגות** — כל בד בשני גדלים. פורטרט 2:3.
רפרנס להעלאה: `etage/assets/coll-rose.webp` (הפדסטל, הקיר והאור חייבים להיות זהים, אחרת זה לא עולם אחד).

| קובץ | בד | גודל |
|---|---|---|
| `etage-cake-tulle-s.png` | טול | 2 קומות |
| `etage-cake-tulle-l.png` | טול | 4 קומות |
| `etage-cake-satin-s.png` | סאטן | 2 קומות |
| `etage-cake-satin-l.png` | סאטן | 4 קומות |
| `etage-cake-lace-s.png` | תחרה | 2 קומות |
| `etage-cake-lace-l.png` | תחרה | 4 קומות |
| `etage-cake-pleat-s.png` | קפלים | 2 קומות |
| `etage-cake-pleat-l.png` | קפלים | 4 קומות |

פרומפט:
```
A [TIERS]-tier ivory wedding cake whose sugar decoration translates a bridal gown fabric: [DECOR]. Same set as the reference image: round cake centered on the same pale travertine pedestal, same warm cream wall, same soft window light from the left with a long gentle shadow, same camera height and distance, cake occupies the middle 60% of the frame with air above and below. Ivory and blush palette only, no flowers unless stated. No text, no people. Portrait 2:3, photorealistic, editorial food photography.
```
- tulle: `soft sugar-paste ruffles layered like tulle on every tier`
- satin: `perfectly smooth satin-finish fondant with one long draped sugar-silk swag falling diagonally across the tiers`
- lace: `fine piped royal-icing lace with scalloped edges over smooth tiers`
- pleat: `crisp vertical sugar pleats on each tier, modern and architectural`
- [TIERS]: `two` / `four`

### נכסים — ב׳ (סרט + נקודות מגע)
**סרט 30 שניות** — 6 קליפים ב-Kling, 5 שניות כל אחד, 9:16. אני חותכת, מרכיבה ומוסיפה כותרות.

| קובץ | תמונת פתיחה | פרומפט Kling |
|---|---|---|
| `etage-k1-dress.mp4` | `etage/assets/cake-photo.webp` | `Slow push-in on the wedding cake. A silk ribbon gently wraps around the bottom tier by itself, soft light shifts warmly. Calm, elegant, no people.` |
| `etage-k2-fabric.mp4` | `etage-fabric-satin.png` | `Ivory satin fabric slowly ripples and flows as if in a light breeze, macro, soft window light, dreamy and slow.` |
| `etage-k3-turn.mp4` | `etage-cake-lace-l.png` | `The cake slowly rotates on its pedestal, 90 degrees, camera static, soft shadows move naturally.` |
| `etage-k4-cut.mp4` | `etage/assets/inside-cut.webp` | `A silver cake server slowly lifts the slice away from the plate, revealing the layers, shallow depth of field, slow motion.` |
| `etage-k5-table.mp4` | `etage/assets/finale.webp` | `Candle flames flicker, fairy lights twinkle softly in the background, very slow dolly-in toward the cake. Evening wedding atmosphere.` |
| `etage-k6-hands.mp4` | `etage/assets/finale.webp` | `Two hands, a bride and a groom, meet on the cake knife together and begin to cut. Slow, romantic, warm candlelight.` |

הערה: `finale.webp` רחבה (16:9). ב-Kling לבחור 9:16 ולתת לו לחתוך את המרכז, או להכין קודם ב-ChatGPT גרסה אנכית (פרומפט: `Recompose this exact scene as a vertical 9:16 frame, cake centered` + העלאת התמונה).

**4 נקודות מגע** — פורטרט 4:5 (כמו ENCORE°). רפרנס: `etage/assets/coll-rose.webp`.

| קובץ | מה רואים |
|---|---|
| `etage-tp-tasting-box.png` | קופסת טעימות פתוחה: 6 קוביות עוגה בתאים, כרטיס שמנת קטן |
| `etage-tp-box.png` | קופסת עוגה גבוהה בשנהב עם סרט משי בורדו, על שיש |
| `etage-tp-card.png` | כרטיס הזמנה/סקיצה בעבודת יד עם דוגמת בד מוצמדת וסיכה |
| `etage-tp-studio.png` | שולחן האטלייה: סקיצות עוגה, דוגמאות בד, כלי זילוף |

פרומפט בסיס:
```
Luxury wedding-cake atelier brand still life: [SCENE]. Palette ivory, blush, warm travertine, one deep bordeaux accent (#6B2E3A) and soft copper (#B57A5E). Soft window light from the left, editorial, calm, high detail. Leave the label area plain — no text, no logo. Portrait 4:5.
```

---

## 2 · ORBE — מטיפה יפה ל**טיפה שלך**

### הבעיה
ה-WOW קיים, אבל הבושם נשאר מופשט עד הסוף. אין רגע שבו הגולשת בוחרת משהו, ואין מגע אמיתי: עור, כלי זכוכית, טקס.

### הרעיון
**"שלוש מילים. טיפה אחת."** אחרי שלוש השכבות (אור · לב · עומק) הגולשת בוחרת 3 מילים מתוך 9, למשל שקט · משי · מלח · לילה · עור · גן · עשן · אור · פרי. הכדור מתערבב לצבעים של ההרכב שלה, היחס בין השכבות משתנה, ויוצא כרטיס "ORBE Nº 1 — הטיפה של ___" לשיתוף.

### מה אני בונה בקוד (בלי נכסים)
- **מנגנון 3 המילים:** צביעה מחדש של החלקיקים, היחסים בין השכבות, כרטיס תוצאה שנשמר כתמונה ומתאים לשיתוף בסטורי.
- **בידול מ-AERÉA בטקסטים:** ORBE = "התמצית, הריכוז", AERÉA = "האוויר".
- **שדרוג אזור הרכישה:** במקום תיבה בודדת יש כלי זכוכית, טקס ומחיר.
- **ספר מותג מקוצר** `orbe/brand-book.html`.

### נכסים — א׳
אין. המנגנון כולו קוד. אפשר להתחיל מיד.

### נכסים — ב׳ (טקס + סרט + נקודות מגע)
**4 תמונות** — פורטרט 4:5. רפרנס: `orbe/orbe-og.jpg` (הפלקון, הצבעים, החושך).

| קובץ | מה רואים |
|---|---|
| `orbe-tp-wrist.png` | טיפה זהובה אחת על מפרק כף יד, מאקרו, רקע כהה |
| `orbe-tp-flacon-hand.png` | הפלקון הכדורי מונח בכף יד פתוחה |
| `orbe-tp-box.png` | קופסה כחול-לילה פתוחה, הפלקון בתוך שקע קטיפה, קו זהב |
| `orbe-tp-ritual.png` | הפלקון על משטח אבן כהה, פקק פתוח, טיפה תלויה על המוליך |

פרומפט בסיס:
```
Haute parfumerie brand still life for ORBE, a perfume concentrate sold as a single drop: [SCENE]. Same spherical glass flacon as the reference image (clear sphere filled with amber-gold liquid, dark stopper with gold collar). Palette: deep night navy (#0B1018), amber gold (#E0B26C), copper (#C28A5A). Low-key lighting, one warm rim light, floating gold dust bokeh. No text, no logo. Portrait 4:5, photorealistic, macro detail.
```

**סרט 30 שניות** — 5 קליפים ב-Kling, 9:16:

| קובץ | תמונת פתיחה | פרומפט Kling |
|---|---|---|
| `orbe-k1-drop.mp4` | `orbe-tp-ritual.png` | `A single golden drop slowly forms and falls from the glass applicator, extreme macro, slow motion, gold dust floats in the dark.` |
| `orbe-k2-skin.mp4` | `orbe-tp-wrist.png` | `The golden drop gently spreads on the skin and glows softly, macro, slow, warm rim light.` |
| `orbe-k3-flacon.mp4` | `orbe/orbe-og.jpg` | `Slow orbit around the glass sphere flacon, the amber liquid catches the light, particles drift.` |
| `orbe-k4-hand.mp4` | `orbe-tp-flacon-hand.png` | `The hand slowly closes around the flacon, then opens again, intimate, dark background, gold glints.` |
| `orbe-k5-box.mp4` | `orbe-tp-box.png` | `Very slow push-in on the open box, gold edge glints, dust floats in the light beam.` |

---

## 3 · ÉCRU — ממוזה אחת ל**מוזה בכל מקום**

### הבעיה
ההבטחה היא "אינסוף לוקים, אפס הפקה", אבל כל התמונות באותו סטודיו ועל אותו רקע, אז זה לא *נראה* אינסופי. בנוסף, הבוטיק נראה כמו תבנית כללית.

### הרעיון
**"הלבישי את המוזה — ואז תזיזי אותה בעולם."** בוחרים לוק (3) ובוחרים מקום (3): סטודיו · רחוב בפריז · ערב. אותה דמות, אותו בגד, עולם אחר. 9 תמונות שנראות כמו 3 ימי צילום, והן אפס ימי צילום. זה בדיוק מה שמוכרים ללקוחת אופנה.

### מה אני בונה בקוד (בלי נכסים)
- **מטריצת "לוק × מקום"** (3×3) בתוך הסקשן "מהמדף אל המוזה" שכבר קיים. הסליידר נשאר, ומתחתיו נוספת שורת מקומות.
- **הבוטיק מקבל זהות:** גריד מוצרים שבו כל כרטיס מתחלף בריחוף בין המקומות, וכרטיס "Shop the look".
- **ספר מותג מקוצר** `ecru/brand-book.html`.

### נכסים — א׳ (המטריצה)
**6 תמונות** — 3 לוקים × 2 מקומות חדשים (הסטודיו כבר קיים). פורטרט 3:4 (ב-ChatGPT 2:3 זה בסדר, אני אחתוך).
**חובה להעלות את תמונת הלוק כרפרנס.** זה מה ששומר על אותה דמות ואותו בגד.

| קובץ | רפרנס להעלאה | מקום |
|---|---|---|
| `ecru-shirt-paris.png` | `ecru-media/look-shirt.jpg` | רחוב בפריז |
| `ecru-shirt-evening.png` | `ecru-media/look-shirt.jpg` | ערב |
| `ecru-vest-paris.png` | `ecru-media/look-vest.jpg` | רחוב בפריז |
| `ecru-vest-evening.png` | `ecru-media/look-vest.jpg` | ערב |
| `ecru-blazer-paris.png` | `ecru-media/look-blazer.jpg` | רחוב בפריז |
| `ecru-blazer-evening.png` | `ecru-media/look-blazer.jpg` | ערב |

פרומפט:
```
Use the reference photo. Keep EXACTLY the same woman (same face, hair, body) and EXACTLY the same outfit, every garment unchanged. Change only the location and light: [PLACE]. Full-body, standing, relaxed natural pose similar to the reference, camera at waist height, she occupies the center of the frame. Warm, soft, editorial fashion photography, muted ecru and caramel palette. No text, no logo. Portrait 3:4.
```
- paris: `a quiet Paris street in the morning, cream limestone Haussmann facade, soft overcast light, a café chair blurred in the background`
- evening: `a warmly lit hotel lobby at dusk, travertine and brass, golden lamp light, soft bokeh`

**בדיקה לפני שליחה:** הפנים זהות? כפתורי הוסט, צבע הג'ינס ואורך הבלייזר זהים? אם משהו זז, לייצר שוב. זאת כל ההבטחה.

### נכסים — ב׳ (תנועה + סרט)
**3 קליפים** — התנועה למטריצה ולסרט. Kling, 5 שניות, 9:16:

| קובץ | תמונת פתיחה | פרומפט Kling |
|---|---|---|
| `ecru-k-shirt-paris.mp4` | `ecru-shirt-paris.png` | `She takes two slow steps toward the camera and glances sideways, hair moves slightly, the street stays still. Natural, editorial.` |
| `ecru-k-vest-evening.mp4` | `ecru-vest-evening.png` | `She turns slowly from three-quarter to facing the camera, lamp light glows warmly, subtle and elegant.` |
| `ecru-k-blazer-paris.mp4` | `ecru-blazer-paris.png` | `She adjusts the blazer lapel with one hand and looks into the camera, a slight breeze, calm confidence.` |

את הסרט של 30 השניות אני מרכיבה מהקליפים האלה, מ-3 הקליפים שכבר יש (`motion-*.mp4`), ומחיתוכי סליידר "מהמדף אל המוזה".

### נכסים — ג׳ (בונוס)
`ecru-tp-bag.png` · `ecru-tp-tag.png` — שקית קרפט בגוון אקרו עם ידית חבל, ותווית בד תפורה. פורטרט 4:5.
```
Minimal fashion boutique brand still life: [an ecru kraft shopping bag with a cotton rope handle, standing on travertine | a woven ecru fabric clothing label stitched inside a white shirt collar, macro]. Palette ecru, caramel, ink navy (#15202E). Soft window light. Label area left plain — no text, no logo. Portrait 4:5.
```

---

## סיכום — כמה זה
| עולם | א׳ (מנגנון) | ב׳ (סרט + מגע) | אני בלי נכסים |
|---|---|---|---|
| ÉTAGE° | 4 בדים + 8 עוגות (ChatGPT) | 6 קליפים Kling + 4 סטילס | La Robe, CTA, מיצוב, ספר מותג |
| ORBE | — | 4 סטילס + 5 קליפים Kling | 3 מילים, בידול, רכישה, ספר מותג |
| ÉCRU | 6 תמונות (ChatGPT) | 3 קליפים Kling | מטריצה, בוטיק, ספר מותג |

**ההמלצה לסדר:**
1. **ORBE:** המנגנון שלו בלי נכסים, אז אני מתחילה מיד.
2. **ÉCRU:** בינתיים את מכינה את 6 התמונות. זה הכי קרוב ללקוחות.
3. **ÉTAGE°:** הכי הרבה נכסים, ולכן בסוף.
