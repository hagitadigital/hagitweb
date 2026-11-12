# BOL° ad — render notes

Brand-mode ad for the BOL° world (No.09): the brand speaks to its own customers, no studio window.

| File | Format | Use |
|---|---|---|
| `BOL-ad-30s.mp4` | 1080×1920, 30s | Reels / Stories |
| `BOL-ad-30s-4x5.mp4` | 1080×1350, 30s | Feed (cream side panels, nothing cropped) |
| `BOL-ad-15s.mp4` | 1080×1920, 15s | Reels / Stories, short cut |
| `BOL-ad-15s-4x5.mp4` | 1080×1350, 15s | Feed, short cut |

Frame 0 already shows the hook ("מה יש לך בקערה היום?") over a half-full bowl. That frame is the feed thumbnail.

- **30s:** hook 0–2.6 · logo 2.5–4.1 · La Carte 4–9.2 · Le Quart + order card 9.1–16.1 · La Glacerie 16–20.1 · Édition Hanoucca 19.9–24.1 · promise 23.9–27.2 · logo + CTA 27–30
- **15s:** hook 0–2.6 · logo 2.5–3.9 · Le Quart + order card 3.8–10.6 · La Glacerie 10.4–12.7 · logo + CTA 12.5–15

The Hanukkah scene is seasonal. After 12 Dec, remove `hanoucca` from `PLANS[30]` in `src/gen.py`, stretch Le Quart or La Glacerie into its window, and re-render.

Rebuild: `python3 src/gen.py`, then `node .claude/skills/brandos-brand-world-reel/scripts/render.js src/ad-30.html 30 BOL-ad-30s.mp4`, and do the same for the 15s cut.
4:5: `ffmpeg -i in.mp4 -vf "scale=760:1350,pad=1080:1350:160:0:color=0xF7F5F0" …`. The brand version uses plain cream panels instead of the studio frame.
