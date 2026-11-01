# 2026-11-worlds · Hidden-logo reels, wave 1

Three new worlds in the format of the ELVÉA° hidden-logo reel: a hook, six chapters
(הסמל · האתר · המוצרים · האריזה · החנות · הפיד), and an outro that answers the hook, followed by the CTA
"אבחון פער המותג · 30 דק׳ · בלי עלות". Each world also gets a 3s hook-only clip for retargeting.
Spec and decisions: the "כיווני עולמות — איפיון" Design canvas.

| World | Hook | The line that replaces the logo | Files |
|---|---|---|---|
| ORÉVA° No.24 | ועדיין שואלים אצלך אם יש הנחה? (generic serum, ככה משווים) | the copper ribbon | `oreva/OREVA-*` |
| ENCORE° No.28 | אם נסתיר את הלוגו, עדיין יזהו אותך? (bar over the logo on the bag) | the dial, night on top | `encore/ENCORE-*` |
| MIEL° No.27 | למה תמיד משווים אותך במחיר? (generic cake, ככה משווים) | the slice: layer · heart · layer | `miel/MIEL-*` |

Per world: `*-hidden-logo-4x5.mp4` (feed) and `*-hidden-logo-9x16.mp4` (Reels/Stories), 26.5s;
`*-hook-3s-4x5.mp4` and `*-hook-3s-9x16.mp4`.

Timeline (s): hook 0–2.6 · 01 2.6–5.9 · 02 5.9–9.3 · 03 9.3–12.6 · 04 12.6–16.0 · 05 16.0–19.3 · 06 19.3–22.4 · outro 22.3–26.5.

## Rebuild
From the repo root:

```bash
python3 campaign-drop/2026-11-worlds/_gen/gen.py          # writes <world>/src/{reel,hook}.html + assets
campaign-drop/2026-11-worlds/_gen/render-all.sh [world]   # renders the MP4s (uses the brand-world-reel skill's render.js)
```

Copy and timings live in `_gen/worlds.py`; the shared layout (hook, chapter frame, browser, feed, outro) lives in `_gen/gen.py`.
This is campaign work: it stays on the `claude/*` branch and is never merged into main.
