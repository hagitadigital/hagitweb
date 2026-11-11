# SIGNÉ° · רואים מה בפנים — transparent sufganiyot (Hanukkah 2026, studio mode)

`out/SIGNE-verre-9x16.mp4` · `out/SIGNE-verre-4x5.mp4` — 30s.

| Time | Scene |
|---|---|
| 0–2.4 | Hook: "בחנוכה כולם מוכרים סופגנייה. אף אחד לא מראה מה בפנים." + generic sufganiya card (ככה משווים · ₪12 · "מה בפנים? לא כתוב.") |
| 2.35–3.6 | Portal from the copper ball onto SIGNÉ's set: a hollow glass sufganiya, the piping nozzle in it. "אצל SIGNÉ° — רואים." |
| 3.6–24.8 | 4 editions × 5.3s: "מה בפנים?" → the filling pours and rises in the glass (Kling) → the glass "sets" into the real Les Lumières sufganiya (crossfade + light sweep) → "ועכשיו — חתום." · Le Noir, La Framboise, La Pistache, La Vanille |
| 24.8–27.3 | Coffret des Lumières: "החתימה שרואים — בחוץ. ההבטחה — בפנים." (site copy) |
| 27.3–30 | Studio outro: "כולם מוכרים סופגנייה. SIGNÉ° מראה מה בפנים." + the four + "ומה יש בפנים אצלך?" + אבחון פער המותג |

Higgsfield: empty glass gpt_image_2_6 job 1fb35bee (from the Noir still); full glasses noir cdc87ca6 · framboise cb089005 ·
pistache ccdd8fc5 · vanille 1a28733b; pours Kling 3.0 pro 5s first+last frame: 995a2267 · c3324f31 · ac501c97 · 9c55ab77
(sped to 3.9s in a/pour-*.webm). Credits ≈ 45. a/real-*.webp + a/coffret.webp = the Les Lumières stills (branch claude/kind-cannon-nojzbs).
Rebuild: `cd src && python3 -I build.py`, then `node render.js reel.html 30 ../out/SIGNE-verre-9x16.mp4`.
