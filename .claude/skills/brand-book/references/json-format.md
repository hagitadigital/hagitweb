# brand-book.json

הגרסה של הספר שמכונה קוראת. BrandOS טוען אותה ישירות כשמכניסים לינק לאתר, ומכניס אותה לכל פרומפט כקונטקסט קבוע. המפתחות תואמים לאפיון ב-`hagitadigital/brandos` (`docs/brand-book-spec.md`): `decision`, `codes`, `palette`, `type`, `voice` ו-`rules` באותם שמות. כל השאר נוסף עליהם.

## איפה הוא יושב

| אתר | כתובת |
| --- | --- |
| עולם של הסטודיו | `https://hagitantebi.co.il/<slug>/brand-book.json`, ליד `brand-book.html` |
| אתר של לקוחה | `https://<domain>/brand-book.json`, בשורש |

בשני המקרים, ה-`<head>` של הספר ושל עמוד הבית מכיל:

```html
<link rel="alternate" type="application/json" title="brand-book" href="brand-book.json">
```

ככה BrandOS מוצא את הספר: קודם מחפש את התגית בעמוד שהודבק, אחר כך `/<path>/brand-book.json`, ואחר כך `/brand-book.json` בשורש.

## השדות

```jsonc
{
  "version": 1,                         // מבנה הקובץ. עולה רק כשמבנה השדות משתנה
  "updated": "2026-10-02",              // תאריך העדכון האחרון של הספר

  "brand": {
    "name": "ENCORE°",                  // בדיוק כמו בעמוד, כולל °
    "slug": "encore",
    "category": "תכשיטים",
    "url": "https://hagitantebi.co.il/encore/",
    "book_url": "https://hagitantebi.co.il/encore/brand-book.html",
    "world_no": 28,                     // רק בעולמות של הסטודיו. אחרת null. המספר הנוכחי בגלריה /brand-worlds/ (העולמות מוספרו מחדש ב-3.10)
    "fictional": true,                  // עולם קונספט = true, לקוחה אמיתית = false
    "thesis": "השעה היא הלוגו.",        // ה-h1 של הספר
    "language": "he"
  },

  "decision": {
    "problem": "…",                     // איך נראית הקטגוריה כשכולם נראים אותו דבר
    "promise": "…",                     // 01 · ההבטחה
    "element": "…",                     // 02 · האלמנט
    "result": "…",                      // 03 · התוצאה
    "why_not_compared": "…"             // משפט אחד: למה אי אפשר להשוות
  },

  "codes": [                            // 3 עד 5
    {
      "id": "dial",                     // אנגלית, לשימוש פנימי
      "name": "החוגה",                  // כמו בעמוד
      "rule": "…",                      // הכלל, בשורה אחת
      "where": ["שלט", "מכסה הקופסה"],  // איפה הוא מופיע
      "min_per_asset": false            // true = חייב להופיע על כל פריט תוכן
    }
  ],
  "min_codes_per_asset": 3,             // כמה קודים לפחות בכל נקודת מגע

  "palette": [
    {
      "hex": "#853A26",                 // שש ספרות, אותיות גדולות
      "name": "שקיעה",
      "role": "primary",                // primary | secondary | base | text | line
      "meaning": "18:00",               // מה הצבע מייצג בעולם
      "use": "צמידים, שקית של צמיד"     // איפה משתמשים בו
    }
  ],

  "type": {
    "display": "Frank Ruhl Libre",      // כותרות בעברית
    "body": "Heebo",                    // גוף
    "accent": "Cormorant Garamond",     // שמות, מספרים, סימן. null אם אין
    "wordmark": {"tracking": "+220", "notes": "…"},
    "languages": ["…", "…", "…"],       // "שלוש שפות שלא מתערבבות"
    "numerals": "lining"                // תמיד lining
  },

  "voice": {
    "tone": "…",
    "say": ["…"],                       // מילים שלנו
    "never": ["…"],                     // מילים שלא
    "examples": ["…", "…", "…"]         // בדיוק שלושה, מהעולם עצמו
  },

  "cover_test": [                       // בדיוק ארבעה
    {"detail": "פינת שקית", "codes": ["צבע השעה", "חותמת השעה"]}
  ],

  "touchpoints": [
    {"name": "השלט", "codes": ["החוגה", "קו הזהב"], "image": "/encore/assets/touchpoints/sign.webp"}
  ],

  "rules": {
    "never_changes": "…",
    "first_question": "…",              // השאלה ששואלים לפני כל תוכן. null אם אין
    "may_change": "…",
    "breaking_mistake": "…",
    "dos": [{"yes": "…", "no": "…"}]    // ארבעה זוגות, כמו ברשת כן/לא
  },

  "source": {
    "studio": "Brand Worlds Studio",
    "author": "Hagit Antebi"
  }
}
```

## `continues` — העולם ממשיך (מומלץ)

הפרק "העולם ממשיך" בספר מראה שהעולם לא נגמר באתר: אותה החלטה כותבת מאמרים, קמפיין, מודעות וריל. זה בדיוק מה ש-BrandOS צריך להפיק, ולכן הפרק נכנס גם ל-JSON, כדוגמה שהמערכת יכולה ללמוד ממנה ולהמשיך. דוגמאות מלאות: `rosee/brand-book.json` (עם ריל), `encore/brand-book.json`, `oreva/brand-book.json` (עולם בלי שעות).

```jsonc
"continues": {
  "intro": "…",                          // משפט הפתיחה של הפרק
  "articles": [                          // 3–4 כיווני מאמרים
    {"hour": "05:30", "product": "La Brume", "title": "…", "search": ["חיפוש אמיתי"], "angle": "…", "opening": "המשפט הראשון, בקול של המותג"}
    // עולם בלי שעות: "opener" במקום hour/product (ORÉVA°: "Le soin · 01"). כותרת בשתי שורות נכתבת עם " / " ביניהן
  ],
  "campaign": {
    "name": "שבעה בקרים", "name_fr": "Sept Matins",
    "line": "…", "idea": "…", "rule": "…",   // rule = הכלל שהקמפיין שומר (למשל: כל פיסה לפני 08:00)
    "open_facts": ["…"],                 // אופציונלי: עובדות שחסרות מהלקוחה לפני שהקמפיין עולה (לא ממציאים מספרים)
    "phases": [{"hour": "…", "format": "ריל 9:16", "line": "…", "detail": "…", "codes": ["…"]}]
  },
  "ads": [{"format": "פיד 4:5", "line": "…", "codes": ["…"], "without_name": "מה נשאר כשמכסים את השם"}],
  "reel": {                              // null כשעוד אין ריל לקמפיין
    "video": "/<slug>/<file>.mp4", "poster": "…", "seconds": 30,
    "hook": "…", "close": "…", "signature_scene": "…",
    "scenes": [{"from": 0, "to": 2.5, "name": "הוק", "what": "…"}]
  },
  "same_brief": {"brief": "פוסט לסוף השנה", "generic": "…", "ours": "…", "why": "…"}
}
```

- `codes` בתוך הפרק משתמשים באותם שמות של `codes[].name` או של צבעי הפלטה.
- `same_brief.generic` הוא תמיד מוצר גנרי בלי שם, לא המוצר של העולם באפור.
- כמו בכל הקובץ: כל ערך כתוב גם בעמוד.

## כללים

- **כל ערך מגיע מהעמוד.** לא כותבים ב-JSON משהו שלא כתוב בספר. ההפך מותר: בעמוד יש יותר הסבר.
- **שמות קודים זהים.** `codes[].name` הם בדיוק השמות ב-`h3` של כרטיסי הקודים, וב-`cover_test[].codes` וב-`touchpoints[].codes` משתמשים באותם שמות או בשמות של צבעי הפלטה.
- **HEX זהה.** כל `palette[].hex` מופיע בעמוד (במשתני `:root` או בטקסט).
- **בלי HTML ובלי markdown** בתוך ערכים. טקסט נקי, עם ° ו-· כמו בעמוד.
- **UTF-8, הזחה של 2 רווחים**, ובלי הערות (ההערות למעלה הן רק להסבר).

`scripts/check_book.py` בודק את כל אלה.
