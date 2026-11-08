# Series «נכנסים לעולם מותג» · studio stills

Hagit's fixed studio stills for every episode (look א׳, black blazer). Brief and episode scripts: `brandos/briefs/series-enter-world-2026-11/`.

| File | Shot |
|---|---|
| `series-P0-studio.webp` | empty studio, board |
| `series-S1-open.webp` | opening, "come in" gesture |
| `series-S2-top.webp` | points at the top panel (colours) |
| `series-S3-bottom.webp` | points at the bottom panel (product) |
| `series-S4-middle.webp` | points at the middle panel (code), entry shot |
| `series-S5-draw.webp` | draws a line at the worktable |
| `series-S6-ask.webp` | the question to the viewer, board soft behind |


`test-board-elvea-S4.jpg` — board test: ELVÉA° colours / code / product warped onto S4, hand kept on top.
`src/panels.html` renders the three panel faces (720×700), `src/warp.py <still> <out.jpg>` warps them onto the board
(corner quads are per still, in the `quads` dict, 941×1672 px) and keeps the hand via a colour-deviation mask.
