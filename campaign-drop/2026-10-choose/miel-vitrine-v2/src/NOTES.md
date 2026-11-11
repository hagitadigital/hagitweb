# MIEL° vitrine ad v2: render notes

18.5s recut of `MIEL-vitrine-ad-v1-9x16.mp4` (32s). The v1 file is not in the repo; pass it to the build.

    bash src/build.sh <path/to/MIEL-vitrine-ad-v1-9x16.mp4> .

| Time | Scene | Source |
|---|---|---|
| 0.0–3.0 | Hook: «נכנסות לאתר שלך, ולא קונות?», generic grid («ככה משווים», ₪290) over the MIEL vitrine («ככה בוחרים», ₪290). Frame 0 already shows both | `scenes.html#hook` |
| 3.0–5.5 | Drag a slice in the vitrine | v1 5.0–7.5 |
| 5.5–8.5 | Bags fill under the laptop | v1 12.0–15.0 |
| 8.5–11.5 | «חמש עוגות. חמש שקיות.» | v1 16.0–19.0 |
| 11.5–14.0 | «אותו מחיר. ₪290.» / «אבל עכשיו יש סיבה לקנות דווקא אצלך.» | `scenes.html#bridge` |
| 14.0–18.5 | «MIEL° לא קיימת. החנות שלך כן.» + CTA, holds to the last frame | `#end-b` or `#end-long` |

Two end cards, one per landing page:
- `-lpB`: «שלחי לי קישור לחנות שלך… 3 מקומות שבהם משווים אותך» → `brand-world-start-b.html`
- `-lpLong`: «אבחון פער המותג · 30 דק׳» → `brand-world.html`

v1 footage comes from the 9:16 master; the 4:5 files are built from the 9:16 with the skill's frame45.sh.
The end-card button copies the v1 CTA (`#6A553E`, radius 10px, 452×136).
No audio (v1 has none). `assets/` are stills cropped from v1.
