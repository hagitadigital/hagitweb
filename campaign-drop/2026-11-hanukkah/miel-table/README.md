# MIEL° · השולחן מתמלא (Hanukkah 2026, brand mode) — direction A, approved 11.11

`out/MIEL-table-9x16.mp4` · `out/MIEL-table-4x5.mp4` (4:5 with plain poudre side panels, no studio frame — brand mode). 30s.

A profile screen in MIEL's own design (not Instagram's): avatar M°, "רומנטיקה מתחילה מבפנים.", highlight bubbles = the 8 nights.

| Time | Scene |
|---|---|
| 0–4 | Hook over the empty table: "שמונה נרות. שמונה פרוסות. / כל לילה — לב אחר." (site copy). Shamash lights at 2.0 |
| 2.7–23.9 | 8 nights × 2.65s: the gold ball rolls along the line under the bubbles → the bubble is tapped → flies into the post → lands on the table as that night's slice (ripple on the marble) → that night's candle lights. Caption chip: "Nuit N · ביסקוויט X · לב Y" |
| 23.9–30 | Full table, all candles lit; the header becomes the close: "מדליקים נר. חותכים פרוסה. ומגלים מה בפנים." + "להזמנת שמונה הפרוסות לחנוכה" |

Images (`src/a/`): six slices are MIEL's own (`miel/assets/35–41`); pistachio + ריבת חלב generated from slice 35
(Higgsfield gpt_image_2_6, jobs 12c54f5c / 91ca1fe2); all eight cut out with Higgsfield's background remover; the table is
gpt_image_2_6 (job 0ba413f6), wick positions measured on it (see build.py). Credits used: ≈ 2.

Rebuild: `cd src && python3 -I build.py`, then `node ../../signe-card/src/render.js reel.html 30 ../out/MIEL-table-9x16.mp4`.
