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

## Finished cut (24.11)
`SITES-PRESENTER-v2-9x16.mp4` (42.8s): the avatar take `take/avatar-take-01.mp4` (HeyGen, 720×1280) over the plates.
Built by `cd src && node final.js`: plates render in final mode (`plates.html?final=1`: scene lengths, on-screen notes
and captions follow the pauses in the voice), then the take is laid on top, bottom half in scene 1 and a circle after.
v2 (Hagit's notes on v1): no prices on the end card; the studio's copper thread runs through her circle and the bead
rolls right to left across the whole reel; the five frames run along the bottom; scene 4 plays
`regard-after/landing-desktop.webm` (the frames change in the hero, the chosen one lands on the model) and holds a
3.5s beat with no voice and no circle while it lands.
A new take needs new times: `DUR`, `T` and `CAPSF` at the top of `plates.html`, and `CUT` in `final.js`
(find the pauses with ffmpeg `silencedetect`). The stand-alone plates (`P1`–`P6`, `GUIDE-animatic`) are from before v2.
`SITES-PRESENTER-v1-9x16.mp4` is the first cut, kept for comparison.
