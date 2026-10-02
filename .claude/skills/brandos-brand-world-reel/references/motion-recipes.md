# Motion recipes — proven in the ORÉVA · VELUNE · MIEL · ENCORE · ROSÉE · CREMA · campaign reels

All motion is pure CSS on one 30s timeline. Percent = seconds / 30 × 100. One animated class per element —
when an element needs two motions (move + fade, spin + bob), nest a child and give each level one animation.
Opacity < 1 on an element flattens 3D for its children, so fades go on a wrapper outside the 3D context.

## Contents
1. Frame sequences from the site (the hero of most worlds)
2. Pan to the subject in a 16:9 sequence
3. Dial / clock (ROSÉE, ENCORE) — clockwise
4. 3D carousel around an object (CREMA)
5. Copper ball on a line + circular portal (campaign, her branding)
6. Two lines meeting in a leaf (ELVÉA)
7. Real photo "stirred" by a finger (CREMA cup)
8. Fast cut sequence with synced labels (CREMA cups, MIEL slices)
9. Text reveals
10. Recolouring an inline SVG over time (@property)
11. A signature interaction from the site — rebuild it from the site's own code (ELVÉA's Fil Vert)
12. Pace of image changes

---

## 1. Frame sequences
Most worlds have a scroll-driven image sequence in the repo: `<world>/assets/seq*/f_###.webp`,
`<world>/frames-desktop/`, `oreva/assets/bloom/`, `velune/assets/porte|fruit/`, `miel/assets/a|b/`, `encore/assets/hero/land/`.
Use 40–48 frames (every 2nd of 80) at 0.05–0.06s each → 2–3s of motion, then hold the last frame.
In the template: `<div class="stack" data-seq="seq/f_%03d.webp" data-from="1" data-to="80" data-by="2" data-start="5.4" data-step="0.06">`.
Under the hood each frame is an `img.bf` (visible window ~0.1s) with `animation-delay: start + i*step`; a hold image appears at the end.

## 2. Pan to the subject
Desktop sequences are 16:9; at 1080×1920 "cover" only the middle third shows. Measure where the subject sits
(ELVÉA's bottle ends at ~66% of the width while the flower starts at 50%; ROSÉE's drop is centred).
For a moving subject, make the sequence block wide instead of cover — width = 1920×16/9 ≈ 3413px — and animate
`translateX` from −(centreStart×3413 − 540) to −(centreEnd×3413 − 540) while the sequence plays.
For a still frame in a narrow tile, set `object-position` so the subject is centred (bottle at 66% → ~71% in a 284px tile).

## 3. Dial / clock — clockwise, always
Time must move with the clock. Place items counter-clockwise and rotate the ring clockwise (positive degrees):
```
.ring{animation-name:ring}                 /* positive = clockwise */
@keyframes ring{0%,40%{transform:rotate(0)}43%,52%{transform:rotate(72deg)}55%,100%{transform:rotate(144deg)}}
slot i: transform: rotate(-i*72deg) translateY(-300px) rotate(i*72deg)
.medal (inside slot): counter-rotation keyframes with the negated angles, so photos stay upright
```
Then the item that arrives under the top pointer is i = 1, 2 … in order, matching 05:30 → 06:15 → 07:00.
Pair it with: a centre hero that crossfades to the current item, a time label below, and a "sun" disc behind whose
background-color walks plum → rose → cream-gold with the hours.

## 4. 3D carousel around an object
```
perspective root (0×0 at the centre, perspective:1800px; perspective-origin:0 0)
 └ tilt  transform-style:preserve-3d; rotateX(-24deg)       ← camera above
    ├ ring (translateY(-170px) wrapper) → .ring  rotateY(θ(t))   steps of 360/N with holds
    │   └ slot i  rotateY(i·a) translateZ(R) rotateY(−i·a)
    │       └ .bill  rotateY(−θ(t))   (negated ring keyframes = billboard)
    │           └ rotateX(+24deg)     (undo the tilt so capsules face the camera)
    │               └ capsule (2D)    ← put fades/lifts here, never above
    └ object billboard rotateX(+24deg) at z=0 (machine)
```
R ≈ 380, capsule ≈ 132×172, machine ≈ 360×576. Front item k = −θ/a. Recolour the object and background to the
front item's colour on every step. To "choose" one item: fade the others (scale .55), then translate the chosen one in its
camera-facing frame by (0, R·sin(tilt) − lift, −R·cos(tilt)+40) into the object.

## 5. Copper ball on a line + portal (her branding — use in hooks and transitions)
The line: `<path class="line" pathLength="1">` with `stroke-dasharray:1 1` and stroke-dashoffset 1 → 0 (linear).
The ball: `.ball` with `offset-path: path(same d)`, offset-distance 0 → 100% on the same timing, the inner `.rl` spins −400°.
Shape the line after the world (ORÉVA petal loop, ROSÉE drop, VELUNE arch, MIEL steps, ENCORE sun arc, ELVÉA leaf).
Portal into the world at the end point (830,1200): the world layer gets `clip-path: circle(0 → 2300px at 830px 1200px)`
over 0.9s, a copper SVG ring grows with it (r 44 → 2000, then fades), the ball scales 1.5 and fades.

## 6. Two lines meeting in a leaf (ELVÉA)
Both paths start off-screen bottom-right, share a short stem, split and meet at the tip:
`M1140 1690 L1010 1560 C1066 1382 1006 1262 830 1200` and `M1140 1690 L1010 1560 C834 1498 774 1378 830 1200`.
The ball rides one, a small copper drop (34px radial gradient) rides the other, a soft flash at the tip, then the portal.

## 7. Real photo stirred by a finger
Two copies of the top-down cup photo: the base, and an overlay clipped to the liquid
(`clip-path: circle(18.9% at 49.5% 47.07%)`) rotating around the liquid centre (0 → 78° → −12° → 0).
A translucent finger dot (86px, white 42%, white border) travels an arc with `offset-path` synced to the rotation.

## 8. Fast cut sequence with synced labels
One keyframe `ce` with a visible window of exactly one step (e.g. 0.38s = 1.267%); images and their labels share
the same class and the same `animation-delay`, so the label always matches the picture. Put the "before" image under
the run and an "after" image that appears when the run ends.

## 9. Text reveals
- Mask reveal: `<span class="mask"><span class="l1">…</span></span>` with translateY(110%) → 0, the second line 0.3–0.5s later.
- Headline swap in the same spot: old line goes to translateY(−110%) as the new one comes from 110%.
- Over photos, add a top gradient (300px) and a bottom gradient (700–820px, 45% opaque at the text) in the world's light colour.
- RTL blocks: `dir="rtl"` with `align-items:flex-start` (flex-end pushes text to the left). Centre with `left:0; right:0; margin:0 auto`,
  not translateX(−50%) (an animated transform overrides it).

## 10. Recolouring an inline SVG
```
@property --mc{syntax:"<color>";inherits:true;initial-value:#D2382B}
.mc{animation-name:mc} @keyframes mc{…{--mc:#4F9D58}…}
<svg> … style="fill:var(--mc)" …
```
SVGs copied from the site's own code (e.g. CREMA's capsuleSVG/machineSVG) keep the reel identical to the site; give every
copy unique gradient ids.

## 11. A signature interaction from the site — rebuild it from the site's own code
When the world's site has a built interaction (a carousel, a dial, a line that runs through slides), open the site's HTML/CSS/JS
and copy its construction — proportions, gaps, path data, end marks — instead of approximating it. The owner knows her sites;
an approximation reads as wrong at once.

ELVÉA's Le Fil Vert, as built on the site (`elvea/index.html`, section `.fil`):
- A `direction: rtl` flex track: slide 1 on the right. Slides keep their own ratios (768×1200, 960×1200, 960×1200, 720×1200, 728×1200)
  at one height, rounded 22px, soft shadow, the site's figcaption under each (`01 · La Main` + the Hebrew line).
- Between slides a `.fil-link` gap (≈130px at a 1000px slide height) holding
  `<svg viewBox="0 0 100 100" preserveAspectRatio="none">` with one path from the exit height on the right slide's edge to the entry
  height on the next slide's edge (y in % of the slide height). The site's four paths:
  `M100,50.3 C58,50.3 42,52 0,52` · `M100,52.1 C58,52.1 42,61.7 0,61.7` · `M100,61.7 C58,61.7 42,65.2 0,65.2` · `M100,71.5 C58,71.5 42,52.2 0,52.2`
  (`pathLength="100"`, `vector-effect="non-scaling-stroke"`, olive #55613F).
- After slide 5: a tail at 59.2% and the mark `··· O ···`.
- In the reel: step the track slide by slide (hold ≈0.35s, move ≈0.65s, translateX positive because the track is RTL) and draw each
  link (dashoffset 100 → 0) during the move that brings the next slide in. Give the scene ≈6s.

## 12. Pace of image changes
Product, boutique and lifestyle shots need time to be read: at least ≈1.2s per image, with 0.4–0.45s crossfades and one slow push
(scale 1.08 → 1) across the run. Hard cuts under a second felt rushed. Keep fast hard cuts only for runs of near-identical
frames where the change itself is the point (the rim colour across CREMA's cups).
