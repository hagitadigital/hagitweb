# VELUNE° · world orbit — ad reels (Instagram / LinkedIn)

- `velune-25-orbit.mp4` / `-4x5.mp4` — 25s: hook "הכל מסתובב סביב דבר אחד." over the red fruit under VELUNE's arch ·
  studio "עולם מותג 25" · four cards orbit the fruit (it walks its story in the centre: fruit → opened → drop → bottle):
  01 האתר (a phone scrolls the site) · 02 הפיד (velune.maison) · 03 המודעה (sponsored: "היא לא מתיזה בושם. היא נכנסת אליו.") ·
  04 האריזה (L'Écrin: the box's two doors open) · outro "עולם מותג אחד. כל נקודות המגע." + אבחון פער המותג.
- `velune-25-orbit-long.mp4` / `-long-4x5.mp4` — 45s: each card opens to a full window and the site itself plays —
  01 the door opens on the scroll and the garden, then the three hours on the sun arc · 02 the feed ·
  03 the fruit film (opens, one drop, the bottle) inside a sponsored post · 04 L'Écrin, the box doors open.

Built on the PARDON ME° orbit engine (`../pardon-me-orbit`), from the 20.10 canvas artboard VE-Orbit.
Rebuild: `cd src && bash build.sh` (25s) or `bash build-long.sh` (long cut); timings and copy in `make.py`.
Site clips in `src/media/clips/`: `node record-site.js ../../../../velune/index.html media/clips` (frame by frame, re-record after the site changes).
