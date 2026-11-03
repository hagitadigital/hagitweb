# ENCORE° · world orbit — ad reels (Instagram / LinkedIn)

- `encore-28-orbit.mp4` / `-4x5.mp4` — 25s: hook "היא לא קונה תכשיט. היא קונה זמן." over the sundial with the dawn ring ·
  studio "עולם מותג 28" · the four cards are the four hours: at each stop the world takes the hour's colour and the dial
  turns to its piece — 06:00 האתר · 12:00 הפיד · 18:00 התווית והשקית · 00:00 הקופסה (the dial lid lifts) ·
  the sun's arc closes on a full day · outro "תכשיט אחד. שנים עלייך." · "ואצלך, מוכרים קישוט או זמן?" + אבחון פער המותג.
- `encore-28-orbit-long.mp4` / `-long-4x5.mp4` — 50s: each card opens to a full window and the site itself plays —
  01 the sundial turning on the scroll · 02 the feed · 03 out of the box: the box, the tag, the bag, the four bags, the sign ·
  04 "הסט שלך" (a piece for each hour flies into the clock face) and the 3D box closing on them.

Same engine as the PARDON ME° / VELUNE° / ELVÉA° orbits.
Rebuild: `cd src && bash build.sh` (25s) or `bash build-long.sh` (long cut); timings and copy in `make.py`.
Site clips: `node record-site.js ../../../../encore/index.html media/clips` — three.js 0.170.0 is served from `vendor/three`
when jsdelivr is unreachable; the 3D box renders in software, so that clip takes ~10 minutes.
