# Hanukkah 2026 · hero film "8 לילות · 8 עולמות" (studio mode)

`out/HANUKKAH-8-worlds-9x16.mp4` (Reels/Stories) · `out/HANUKKAH-8-worlds-4x5.mp4` (feed). 30s, 1080×1920, 30fps.

| Time | Scene |
|---|---|
| 0–2.9 | Hook: "בחנוכה כל העסקים מעלים את אותו פוסט." Proof = the same generic sufganiya in six no-name business posts. The copper ball (a sugar-dusted copper sufganiya) rolls on the copper line under the feed |
| 2.9–6 | The line becomes the hanukkiah's base, the shamash arm draws up from the ball and lights. Window: "8 לילות · 8 עולמות" |
| 5–26.2 | 8 nights × 2.65s: the ball rolls to the next cup → the arm draws → the candle rises and lights → a portal opens from the flame into the world |
| 26.2–30 | All 8 worlds in the window, the hanukkiah fully lit, "ומה העולם שלך מדליק השנה?" + אבחון פער המותג |

Nights (right → left): SIGNÉ° 17 · MIEL° 27 · PARDON ME° 29 · ROSÉE° 15 · ENCORE° 28 · PANCAKERIE° 26 · REGARD° 16 · ORÉVA° 24.

Rebuild: `cd src && python3 -I build.py` (copies and resizes the images into `a/`; `--html` = page only), then
`node ../../../../.claude/skills/brandos-brand-world-reel/scripts/render.js reel.html 30 ../out/HANUKKAH-8-worlds-9x16.mp4`
and `frame45.sh` for 4:5. `a/noir.png` and `a/generic.png` (not committed) come from
`campaign-drop/2026-11-signe-hanukkah/assets/sufg-noir-v1.png` / `generic-sufganiya-v1.png` on branch `claude/kind-cannon-nojzbs`.
