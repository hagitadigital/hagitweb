# 2026-11-cover-day · «מכסים את השם», wave 2 (series A)

Three 19s reels, ENCORE°, ROSÉE° and CHASEN°, built from the approved storyboard
(Design canvas "מכסים את השם · סטוריבורד"). Each world's touchpoints come in two pixel-identical versions,
with the name and without it, so the name comes off inside the frame: no bar, no cut. The world's own codes light up one by
one and the counter climbs 3 → 6 → 9 → 12 → 15.

| World | The name comes off | Between touchpoints |
|---|---|---|
| ENCORE° | the gold veil of the site's cover test | the gold hand sweeps the touchpoint into the dial; the dial takes the colour of the next hour (06 → 12 → 18 → 00, then all four) |
| ROSÉE° | the dew drop from the site's opening; a rose ripple | the morning dial turns to the next hour (05:30 → 06:15 → 07:00 → 07:45 → 22:00) with that hour's product inside |
| CHASEN° | the whisk zigzags across the name, the foam settles | the same atelier cup swaps flavour, pixel-aligned (Classique → Fraise → Hōjicha → Yuzu → Bleu) |

ROSÉE° and CHASEN° use a 2:3 window (780×1170) so their 2:3 photos show whole; ENCORE° keeps the 4:5 window (920×1150).

Timeline (s): hook 0–1.8 · window rises 1.8–2.2 · touchpoints 1.9 / 5.0 / 7.5 / 10.0 / 12.5 (transitions centred on 5.0, 7.5, 10.0, 12.5) ·
outro 15.0–19.0 («השם ירד. עדיין ___. ואצלך?», the five touchpoints without the name, CTA «אבחון פער המותג · 30 דק׳ · בלי עלות»).
The 3s hook clip is the first 3 seconds of the same page; the counter reaches 3 at 2.8s.

Per world: `<WORLD>-cover-9x16.mp4` (Reels/Stories), `<WORLD>-cover-4x5.mp4` (feed), `<WORLD>-cover-hook-3s-{9x16,4x5}.mp4` (retargeting).
No soundtrack yet. Landing page: `brand-world-logo.html` with `utm_campaign=cover-v2`.

## Rebuild
From the repo root:

```bash
python3 campaign-drop/2026-11-cover-day/_gen/gen.py          # writes <world>/src/reel.html + assets
campaign-drop/2026-11-cover-day/_gen/render-all.sh [world]   # renders the MP4s (uses the brand-world-reel skill's render.js)
```

Copy, codes, positions and timings live in `_gen/gen.py`; `_gen/film.py` and `_gen/frame-4x5.html` come from wave 1 (`2026-11-worlds`).
This is campaign work: it stays on the `claude/*` branch and is never merged into main.
