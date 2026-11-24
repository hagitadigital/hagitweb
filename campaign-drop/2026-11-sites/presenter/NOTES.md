# SITES-PRESENTER · screen plates (24.11.2026)

Plates for a reel Hagit presents herself: the REGARD° hero, before and after. 1080×1920, 30fps, no audio, no captions.
Script and ad copy: private repo, `brandos/briefs/campaign-2026-11-sites/PRESENTER-REEL.md`.

| File | Length | Hagit's video goes |
|---|---|---|
| `P1-hook-before.mp4` | 5s | bottom half, from y=1090 down |
| `P2-before.mp4` | 6s | circle, about 420px, centre, below the screen |
| `P3-after.mp4` | 8s | same circle |
| `P4-sections.mp4` | 7s | same circle |
| `P5-mobile.mp4` | 4s | small circle, bottom centre |
| `P6-offer.mp4` | 6s | circle, bottom centre |
| `GUIDE-animatic.mp4` | 35s | preview only: zones and spoken lines marked. Not for publishing |

`P4` plays `regard-after/scroll-desktop.webm`: a scroll recording of the live page from the hero down to the shop
(the frame flies to the face, the five portraits, the collection), sped up 1.78×.

`regard-before/` and `regard-after/`: stills and screen recordings of the hero (desktop 1920×1080, mobile 390×844),
taken before and after commit `3d536f3` on main. The plates read their stills from these folders.

Each plate holds its last frame, so it can be frozen or trimmed to the voice.
Re-render: `cd src && node render.js clean && node render.js guide` (timings in `plates.html`, `DUR` and the `ramp(t, …)` calls).
