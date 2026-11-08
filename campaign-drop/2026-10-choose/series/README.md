# Series «ככה בוחרים» — render notes

Six 15s episodes, one layer each. Lineup (it is printed on every end card, so it does not change):

| Ep | Layer | World (gallery No.) | Files |
| --- | --- | --- | --- |
| 01 | הצבע | Pancakerie° (26) | `ep01-pancakerie-9x16.mp4` / `-4x5.mp4` |
| 02 | הבחירה | CHASEN° (22) | `ep02-chasen-…` |
| 03 | מבפנים | MIEL° (27) | `ep03-miel-…` (re-rendered Nov 8: end card now says "בפרק הבא: הסיפור · VELUNE°", was ÉTAGE°) |
| 04 | הסיפור | VELUNE° (25) | `ep04-velune-…` — door opens, garden, fruit → drop → bottle, three hours on the sun arc |
| 05 | האופי | ENCORE° (28) | `ep05-encore-…` — pendant lands ("מכאן, הוא כבר לא יורד."), four hours on the half sun, the box a year later |
| 06 | הידיים | ORÉVA° (24) | `ep06-oreva-…` — "קודם הידיים." → "אחר כך הבקבוק." → 28-day before/after; the end card closes the series |

Every episode: frame 0 = hook question + generic no-name list + the world (feed thumbnail) · generic list with the ball ringing
each price · studio window · the world · end card with the six-bead series line and the diagnosis CTA.

Source: `src/gen.py` builds `src/epNN-*.html` (`python3 src/gen.py`). Render: the brand-world-reel skill's `render.js` (15s),
mux with `audio/epNN-15s.mp3`, then `frame45.sh` for 4:5. Copy for the posts lives in brandos `briefs/campaign-2026-10-choose/SERIES-CAPTIONS.md`.
