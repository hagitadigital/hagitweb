# Serum → brand · inserts for the talking-head reel (ELVÉA°, World 14)

Renders:
- `00-same-serum-twice.mp4` 1080×1080, 4s: plain bottle | branded bottle (frame 0)
- `01-serum-bare.mp4` 1080×1080, 5s: the serum alone, plain cap, no label
- `02-thousands.mp4` 1080×1080, 6s: zoom out to rows of generic bottles
- `03-designed-product.mp4` 1080×1080, 9s: packaging 0.9s · name 3.3s · label 5.4s
- `04-brand-world.mp4` 1080×1920, 10s: story 0.3s · language 2.0s · site 3.7s · boutique 5.4s
- `05-end-card.mp4` 1080×1920, 5s
- `overlay-top-pills.png` 1080×1920, transparent top bar
- `stills/`: end state of each clip, plus transparent PNGs of the bottle and the box

Each clip holds its last state, so it can be trimmed or stretched in the edit.

Rebuild: `cd src && python3 gen.py`, then
`REEL_H=1080 node ../../../.claude/skills/brandos-brand-world-reel/scripts/render.js 03-designed-product.html 9 ../03-designed-product.mp4`
(no `REEL_H` for the two 1080×1920 pages).

The plain bottle is the ELVÉA° hero bottle with the label painted out and the cap recoloured.
