# ROSÉE° · פך אחד. שמונה לילות. (Hanukkah 2026, studio mode)

`out/ROSEE-9x16.mp4` · `out/ROSEE-4x5.mp4` — 30s. Inspired by a "glass letters filled by a pour" reel: here one drop fills a hanukkiah of oil cups.

| Time | Scene |
|---|---|
| 0–2.4 | Hook: "נס פך השמן. כל מותג טיפוח יעלה עליו פוסט. איך יזהו את שלך?" + a generic facial oil (ככה משווים · 30 מ״ל · ₪89) |
| 2.35–5 | Portal from the copper ball into ROSÉE's night: nine empty glass oil cups, Le Réveil's dropper with a drop forming. "ROSÉE° · Née à l'aube · Hanoukka" |
| 5–13 | The Kling clip: the drop falls, the oil leaps from cup to cup, right to left, until all nine are full. "טיפה אחת." → "והיא לא נגמרת." |
| 13.4–20 | The shamash lights, then the 8 floating wicks, right to left ("לילה 1…8"); the night walks toward dawn. "נס פך השמן, בשפה של ROSÉE°" |
| 20.4–24.2 | La Nuit: "ובערב? La Nuit. הטל של מחר נולד הלילה." (site copy) |
| 24.2–27 | "טיפה אחת. שמונה בקרים." |
| 27–30 | Studio outro: "נס פך השמן? אצל ROSÉE° זו טיפה אחת." · "ומה הנס של העסק שלך?" + אבחון פער המותג |

Higgsfield: a/empty.webp (gpt_image_2_6, job 40a72397) and a/full.webp (job fe179ade), Le Réveil as reference;
a/pour.webm = Kling 3.0 pro, 8s, first + last frame (job cc6d3127; variant b118441f not used); a/generic-oil.webp (job 5634a52d).
Credits ≈ 26. Flames: wick tips measured on full.webp (build.py), verified against the clip's last frame.
Rebuild: `cd src && python3 -I build.py`, then `node ../../signe-card/src/render.js reel.html 30 ../out/ROSEE-9x16.mp4`.
