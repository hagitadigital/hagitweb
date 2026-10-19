# ריל אישי 01 · "את כל העריכה פה עשה AI"

`01-ai-edit-placeholder.mp4` is the template over a placeholder (the portrait). When Hagit's take arrives, render the same overlay on it.

## הטקסט לצילום (22 שניות, טייק אחד)

| זמן | מה אומרים | מה קורה על המסך |
|---|---|---|
| 0–2.3 | "את כל העריכה פה עשה AI." | הכותרת כבר על המסך בפריים 0, ולוח "IN THIS VIDEO". המילים נופלות למטה |
| 2.4–4.4 | "לא פתחתי שום תוכנת עריכה." | אייקון של תוכנת עריכה, ועליו קו אדום |
| 4.4–5.9 | "פשוט כתבתי לו מה אני רוצה:" | שורת פרומפט יורדת מלמעלה |
| 5.9–8.4 | (שקט, מבט למעלה אל השורה) | מוקלד: "תוסיפי כתוביות ענקיות", ואז שליחה |
| 8.6–10.3 | "כתוביות ענקיות." | הכתובית מתפוצצת לגודל ענק |
| 10.3–12.7 | "וככה אני בונה עולמות מותג." | חמשת סרטוני העולמות מרחפים סביב הראש |
| 12.7–15.3 | "אבל הסוד הוא לא הכלי." | הכרטיסים עפים החוצה |
| 15.3–18.8 | "הכלי לא משנה. השפה שאת נותנת לו משנה." | מחברת עם המשפט, מרקר צהוב על "השפה" |
| 18.7–22 | "כתבי 'עולם' בתגובות, ואשלח לך איך." | תגובה ממותגת, ועוד שתי תגובות "עולם" נופלות |

## איך לצלם
- טלפון אנכי, 1080p או 4K, 30fps, בגובה העיניים, מיקרופון דש.
- הראש בשליש העליון, עם אוויר מעל ובצדדים. הלוח וכרטיסי הסרטונים נכנסים שם.
- חצי שנייה שקט בין משפט למשפט. ב-5.9–8.4 להסתכל למעלה, אל שורת הפרומפט.
- לא חייבים לעמוד בזמנים בדיוק. התזמון מסתדר אחר כך לפי הצילום.

## Render (Claude)
```
bash src/prep.sh                                  # placeholder take + world-film frames → src/_build/
node src/render.js <take.mp4> out.mp4             # overlay on the take, keeps its audio
node src/render.js <take.mp4> src/_build/qa/s 0,90,300   # QA stills
```
Retime to the real take: edit only the `BEATS`, `CAPS`, `PROMPT_TYPE` and `DROPS` block at the top of the script in `src/overlay.html`. Captions must match what she actually says.
Browser preview: open `src/overlay.html?play` (after `prep.sh`).
