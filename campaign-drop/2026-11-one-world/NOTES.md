# 2026-11 · One World — render notes

| File | Length | What |
|---|---|---|
| `one-world-A-cta.mp4` (+`-4x5`) | 20s | Direction 1, short CTA |
| `one-world-A-gap.mp4` (+`-4x5`) | 20s | Direction 1, CTA with the line "גלי מה מונע…" |
| `one-world-B.mp4` (+`-4x5`) | 15s | Direction 2 · differentiation and value |

Direction 1: 0–4 generic serum "יש עסקים שנראים טוב." · 4–9 hard cuts VELUNE° ↔ Crema° (0.8s each) ·
9–15 ROSÉE° box → clip-path into a phone with the live site (hero, "נולד עם שחר", the dial) · 15–20 studio window + CTA.
Direction 2: 0–2.3 two generic cards "ככה משווים" · copper portal · 2.3–11.6 montage product/packaging/digital/atmosphere
(VELUNE, ROSÉE, ROSÉE site, ENCORE, VELUNE, Crema) · 11.4–15 "תהיי המותג שבוחרים." + CTA.

Rebuild: `cd src && python3 gen.py && node render.js reel-a-cta.html 20 ../one-world-A-cta.mp4`
(reel-b: 15s). 4:5: `.claude/skills/brandos-brand-world-reel/scripts/frame45.sh in.mp4 out-4x5.mp4`.
Site screens in `src/a/rosee-site-*.jpg` are captures of `rosee/index.html` at 390×844 @2x.
