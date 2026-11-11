# SIGNÉ° · כרטיס החתימה (Hanukkah 2026, studio mode) — direction B, approved 11.11, no price on SIGNÉ's card

`out/SIGNE-carte-9x16.mp4` · `out/SIGNE-carte-4x5.mp4` — 30s.

| Time | Scene |
|---|---|
| 0–2.45 | Hook on a white catalogue: "בחנוכה כולם מוכרים סופגנייה. מה כתוב על הכרטיס שלך?" Generic sufganiya + grey card (ככה משווים · 90 גר׳ · ₪12). The copper ball is the card's pin |
| 1.55–3.3 | The ball rolls down the card's line onto the sufganiya; a portal opens from it into SIGNÉ's dark set |
| 3.75–16.6 | Le Noir lands; the glass card: edition, what is inside, "חתום ביד" + the signature where the price was. Three mid-spin swaps (7.35 · 9.95 · 13.1), the card follows, the ball hops |
| 16.7–20.5 | The filling: "החתימה שרואים — בחוץ. ההבטחה — בפנים." |
| 20.3–24.7 | Coffret des Lumières opening |
| 24.6–30 | Both cards side by side, the ball rolls from the grey one to SIGNÉ's: "אותה סופגנייה? לא אותו כרטיס. כי זה לא אותו עולם." + CTA |

Rebuild: `cd src && CLIPS=<folder> python3 -I build.py` (clips: `campaign-drop/2026-11-signe-hanukkah/clips/` on branch
`claude/kind-cannon-nojzbs`), then `node render.js reel.html 30 ../out/SIGNE-carte-9x16.mp4` (render.js seeks the `<video>`s)
and the reel skill's `frame45.sh` for 4:5.
