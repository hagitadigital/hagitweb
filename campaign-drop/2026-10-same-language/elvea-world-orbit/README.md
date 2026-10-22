# ELVÉA° · world orbit — ad reels (Instagram / LinkedIn)

- `elvea-14-orbit.mp4` / `-4x5.mp4` — 25s: hook "היא לא בוחרת בין טבע למדע. היא בוחרת עולם." over the bottle with the
  leaf-and-drop symbol · studio "עולם מותג 14" · four cards orbit La Rencontre (the centre walks flower → leaf and drop →
  the drop → the bottle): 01 האתר · 02 הפיד (elvea.skin) · 03 המודעה (Le Fil Vert as a sponsored carousel) ·
  04 האריזה (Le Coffret, the symbol draws itself over the box) · outro "עולם שלם. באותו קו ובאותם צבעים." ·
  "ואצלך, כל נקודת מגע ממשיכה את אותו קו?" + אבחון פער המותג.
- `elvea-14-orbit-long.mp4` / `-long-4x5.mp4` — 47s: each card opens to a full window and the site itself plays —
  01 La Rencontre on the scroll, then the symbol drawing itself · 02 the feed · 03 the real Le Fil Vert carousel swiping
  inside a sponsored post · 04 Le Coffret and the boutique.

Same engine as `../pardon-me-orbit` and `../velune-orbit`. (`../elvea-orbit` is the earlier 20s five-card cut.)
Rebuild: `cd src && bash build.sh` (25s) or `bash build-long.sh` (long cut); timings and copy in `make.py`.
Site clips: `node record-site.js ../../../../elvea/index.html media/clips` — the site's GSAP ScrollTrigger is stepped on
the clip clock; GSAP 3.12.5 is served from `vendor/` when cdnjs is unreachable.
