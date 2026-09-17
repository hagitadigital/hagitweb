# La Vitrine — `/vitrine/` (built 17.9.2026, awaiting approval)

**What:** a scroll page of five hero objects from the brand worlds, in real 3D (drag to turn, click the name to enter the world). Replaces the Atelier prototype as the site's single 3D destination.

**Objects (Higgsfield 3D Jutsu → GLB → Draco):**
| Station | Model | Higgsfield project | Notes |
|---|---|---|---|
| MELTÉ° No.05 | `models/melte.glb` (374 KB) | bdd43c9b… | built-in turntable anim |
| VELUNE° No.22 | `models/velune.glb` (90 KB) | 2c88896a… | two hinge anims merged into "Doors"; sway ±26° instead of full turn |
| Pétale° No.01 | `models/petale.glb` (204 KB) | 3dee23e3… | lid opens on click to 22% of the clip (full open leaves the frame) |
| MIEL° No.24 | `models/miel.glb` (864 KB) | ed93235c… | cake only; box+ribbon detached (`_lab/3d-rail/strip-nodes.js "^(BOX_|RIBBON_)"`); full scene kept in `_lab/3d-rail/models/_miel-full-scene.glb` |
| ORÉVA° No.21 | `models/oreva.glb` (102 KB) | 027ecacd… rev 8 | bubbles (DROP_*) detached — export as opaque white |

**Pipeline:** pull GLB via MCP `scene_builder_3d_get_glb` → `_lab/3d-rail/strip-nodes.js` if needed → `npx @gltf-transform/cli@4 draco in out` → posters via `crema-rec/_vitrine_posters.js` (toDataURL from the live page, stage scrolled into view first) → QA `crema-rec/_vitrine_qa.js`.

**Learned:**
- model-viewer ships `height:150px` by default; set `display:block;height:auto` or `aspect-ratio` is ignored.
- `field-of-view` does not tighten framing (clamped); zoom via `camera-orbit` radius % + `min-camera-orbit`.
- Cards wrapped in `<a>`: `draggable=false` + `dragstart` preventDefault or link-drag swallows the spin.
- Only the on-screen object turns (IntersectionObserver toggles `auto-rotate` / pause).
- Draco decoder is fetched by model-viewer from gstatic at runtime.

**Open before publish:** Hagit's approval of copy + headline; real-phone check; then commit + IndexNow. Teaser link on brand-world.html (worlds-more) + homepage teaser card under the worlds strip (`#vitrine-teaser`, ORÉVA poster → model-viewer imported only when scrolled into view; click on the object = go to /vitrine/). Sitemap entry added. OG: `/vitrine-og.jpg`.

**Next uses:** each GLB = turntable reel asset; a prospect's real product built the same way = outreach piece ("בניתי את המוצר שלך. סובבי אותו.").
