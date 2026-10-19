# ריל אישי 02 · "אם אסתיר את הלוגו, עדיין יזהו אותך?"

`02-hide-logo-placeholder.mp4` is the template over a placeholder (the portrait). When Hagit's take arrives, render the same page on it.

## הטקסט לצילום (22 שניות, טייק אחד)

| זמן | מה אומרים | מה קורה על המסך |
|---|---|---|
| 0–2.6 | "אם אסתיר לך את הלוגו, עדיין יזהו אותך?" | השאלה למעלה, ומתחת שלושה מוצרים גנריים עם פס שחור על הלוגו. כבר בפריים 0 |
| 2.7–5.0 | "שלושה מוצרים. בלי לוגו." | |
| 5.0–6.8 | "מי זה מי?" | המוצרים רועדים, וסימני שאלה קופצים |
| 6.8–9.2 | "אין דרך לדעת. אז משווים במחיר." | תגיות מחיר נופלות, ותווית "ככה משווים" |
| 9.4–11.6 | "עכשיו תסתכלי על זה." | הסרטון של ROSÉE° עולה, והשם שלו מכוסה |
| 11.6–14.3 | "צבע. מרקם. תחושה." | טפטפת דוגמת את הוורוד, והצבע מתפשט על כל הפריים, כולל עלייך |
| 14.4–16.6 | "ידעת מי זה עוד לפני השם." | הפס זז ו-ROSÉE° מתגלה |
| 16.8–22 | "אם צריך לוגו כדי לזהות אותך, את עוד לא מותג." | משפט ענק, ואחריו "כתבי 'זיהוי' ואבדוק את המותג שלך" |

ההצעה בסוף ("אבדוק את המותג שלך") היא הצעה לבדיקה. אם לא מתאים לך להבטיח את זה, נחליף.

## איך לצלם
- טלפון אנכי, 30fps, בגובה העיניים, מיקרופון דש.
- הראש באמצע הפריים: הכתוביות יושבות מעליו (280–480), והמוצרים והכרטיס מתחתיו (1000–1540).
- ב-11.6–14 אפשר להסתכל אל הכרטיס, למטה מימין.

## Render (Claude)
```
bash src/prep.sh                                       # placeholder take + ROSÉE° film frames → src/_build/
node src/render.js <take.mp4> out.mp4                  # the take is cut into frames and drawn inside the page; keeps its audio
node src/render.js <take.mp4> src/_build/qa/s 0,300    # QA stills
```
Retime to the real take: edit only the `EFFECTS`, `BEATS`, `CAPS` and `PICK` block at the top of the script in `src/reel.html`.
Browser preview: open `src/reel.html?play` (after `prep.sh`).
