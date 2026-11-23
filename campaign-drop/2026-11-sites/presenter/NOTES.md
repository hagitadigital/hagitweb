# SITES-PRESENTER · screen plates (23.11.2026)

Plates for a reel Hagit presents herself. 1080×1920, 30fps, no audio, no captions.
Script and ad copy: private repo, `brandos/briefs/campaign-2026-11-sites/PRESENTER-REEL.md`.

| File | Length | Hagit's video goes |
|---|---|---|
| `P1-hook-before.mp4` | 5s | bottom half, from y=1090 down |
| `P2-before-questions.mp4` | 8s | circle, about 380px, bottom right |
| `P3-after-answers.mp4` | 10s | same circle |
| `P4-offer.mp4` | 6s | circle, bottom centre |
| `GUIDE-animatic.mp4` | 29s | preview only: zones and spoken lines marked. Not for publishing |

Each plate holds its last frame, so it can be frozen or trimmed to the voice.
Re-render: `cd src && node render.js clean && node render.js guide` (timings in `plates.html`, `DUR` and the `ramp(t, …)` calls).
