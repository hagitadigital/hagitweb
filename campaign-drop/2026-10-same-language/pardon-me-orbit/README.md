# PARDON ME° · world orbit — 25s ad reel (Instagram / LinkedIn)

- `pardon-me-29-orbit.mp4` — 9:16 (Reels / Stories), with Arrête Chic soundtrack
- `pardon-me-29-orbit-4x5.mp4` — 4:5 (feed, LinkedIn)
- `pardon-me-29-orbit-long.mp4` / `-long-4x5.mp4` — the long cut (43.9s): at each stop the front card opens to a full
  window and the site itself plays — 01 the peek scroll (the window grows into NOT SORRY) · 02 the feed (pardonme.studio) ·
  03 Pardon the interruption (Tear here) and the campaign lens · 04 the collections (a tap on the oval takes the sleeve off)

Rebuilt from the 20.10 Design-canvas artboard (`src/PM-Orbit.dc.html`; `src/port.py` renders the original as is).
0–2.6 hook "היא לא קונה מוצר טיפוח. היא בוחרת עולם." over the sleeve with its oval window · 2.6–4.3 studio "עולם מותג 29",
the copper line opens the centre · 4.3–21 four cards orbit the oval window, each plays its mechanic at the front:
01 האתר (the phone scrolls the real site) · 02 הפיד (grid pops) · 03 המודעות (the lens opens on the truth) ·
04 האריזה (Take it off: the sleeve slides up); the print in the centre window changes with each stop and the berry
line closes a quarter per stop · 22–25 outro: "עולם שבוחרים בו. בכל נקודת מגע." + אבחון פער המותג.

Rebuild: `cd src && bash build.sh` (25s) or `bash build-long.sh` (long cut); timings and copy in `make.py` (`REEL=long` for the long cut).
The site clips in `src/media/clips/` come from `node record-site.js ../../../../pardon-me/index.html media/clips` (re-record after the site changes).
