# Hanukkah 2026 · SIGNÉ° + MIEL° + ROSÉE° in one film (studio mode, campaign cut)

`out/HANUKKAH-trio-9x16.mp4` · `out/HANUKKAH-trio-4x5.mp4` — 30s, faster than the single films.

| Time | Scene |
|---|---|
| 0–2.45 | Hook: "בחנוכה כל העסקים מעלים את אותו פוסט." — the generic feed (six businesses, the same sufganiya). "ועכשיו — שלושה עסקים, כל אחד בעולם שלו." The copper ball rolls |
| 2.45–10 | Portal → 01 SIGNÉ° (signe-card 3.3–16.6 at 1.85×): Le Noir lands, the glass card, three edition swaps |
| 9.75–17.3 | Ball + portal → 02 MIEL° (miel-table 2.5–24.1 at 3×): the bubbles fly onto the table, the candles light |
| 17.05–24.6 | Ball + portal → 03 ROSÉE° (rosee 4.6–20.2 at 2.15×): the drop, the pour, the wicks |
| 24.6–30 | Outro: "אותו חג. שלושה עולמות." + the three end frames + "ואף אחד מהם לא נראה כמו הפוסט בפיד." · "ומה העולם שלך מדליק השנה?" + אבחון פער המותג |

Segments are cut from the three films' renders (`src/a/*.webm`, rebuilt with ffmpeg setpts — see the commit). `src/reel.html` is the wrapper.
Render: `cd src && node ../../signe-card/src/render.js reel.html 30 ../out/HANUKKAH-trio-9x16.mp4`.
