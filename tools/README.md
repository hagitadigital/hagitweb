# tools/

## build-sitemap.py — sitemap עם lastmod אמיתי

```bash
python tools/build-sitemap.py --dry-run   # רק מראה מה נוסף/הוסר מול ה-sitemap שב-HEAD
python tools/build-sitemap.py             # כותב sitemap.xml
```

**להריץ אחרי commit**, לא לפני — הסקריפט קורא את המצב המחויב (`HEAD`), לא את תיקיית העבודה.
זמן ריצה: כ-2 דקות (הוא עובר על היסטוריית git של כל דף).

### אילו דפים נכנסים

כל קובץ `.html` שעשה commit, **חוץ מ**:

| מוחרג | למה |
|---|---|
| קבצים שלא עשו commit | GitHub Pages לא מגיש אותם |
| `noindex` | |
| stub הפניה (`meta refresh`) | דפים שאוחדו |
| בלי canonical, או canonical שמצביע לכתובת אחרת | |
| `datePublished` עתידי | מאמר מתוזמן נכנס רק מהיום שהוא עולה |
| נתיבים ב-`EXCLUDE_PREFIXES` | `_lab`, `brandworld_ad/`, `hagit_agent_movie/`, `hila-sharon/`, partials של `sonair/src/` |

`changefreq` ו-`priority` נשמרים מה-sitemap הקודם (דף חדש מקבל `monthly` / `0.6`).

### איך נקבע lastmod

תאריך ה-commit האחרון ש**שינה את התוכן** של הדף — לא סתם נגע בקובץ.

לכל commit שנגע בדף, הסקריפט משווה "טביעת תוכן" לפני ואחרי: `<title>`, `meta description`
והטקסט הגלוי של ה-body — **בלי** `script`, `style`, `svg`, `nav`, `footer` ובלוקי
`read-more` / `related`. לכן commit שהוסיף תגית GA4, החליף `href`, או שינה קישורים בפוטר
לא מזיז את ה-lastmod — בלי שצריך לרשום אותו בשום מקום.

### commits גורפים — `sitemap-ignore-commits.txt`

כשסוויפ גורף כן שינה טקסט גלוי (למשל ה-commit של 5.9 שיישר את צורת השם ב-70 דפים),
הטביעה לא יודעת שזה "לא באמת עדכון". לזה יש רשימה ידנית:

```
<sha> [!path ...]  # סיבה
```

- הסקריפט מדלג על ה-commit הזה בכל הדפים.
- `!path` = חוץ מהדף הזה — שם ה-commit כן עשה שינוי אמיתי (למשל `0c95db6 !links.html`).
- **להוסיף לרשימה** כל commit של קישורים פנימיים / תיקוני ניסוח רוחביים, באותו PR שבו הוא נוצר.
- הרשימה עובדת לפי SHA: ב-merge רגיל הוא נשמר. ב-squash/rebase ה-SHA משתנה — הסקריפט
  מדפיס אזהרה על SHA לא מוכר, וצריך לעדכן אותו לשורה החדשה.

### בדיקה לפני commit

- הפלט של `--dry-run` מפרט כל URL שנוסף (`+`) או הוסר (`-`) עם הסיבה.
- אף `lastmod` לא אמור להיות אחרי היום.
