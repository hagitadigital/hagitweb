---
name: brandos-brand-world-reel
description: >
  יוצר ריל מושן-גרפיקה מדויק לעולם מותג של Brand Worlds Studio (חגית אנטבי) — תמיד עם הוק בשניות הראשונות —
  מתוך האתר של העולם עצמו (רצפי פריימים, מוצרים, טקסטים), ומרנדר MP4 9:16 + גרסת 4:5 לפיד.
  שני מצבים: מצב סטודיו (ההוק מדבר אל הכאב של הלקוחה: "למה תמיד משווים אותך במחיר?", "אם נסתיר את הלוגו, עדיין יזהו אותך?",
  והסטודיו מציג את העולם כתשובה) ומצב מותג ל-BrandOS (הוק בקול של המותג עצמו מתוך ה-Brand DNA, בלי מסגרת סטודיו).
  השתמש בסקיל הזה בכל פעם שמבקשים ריל / סרטון / reel / מושן / וידאו לעולם מותג או לאחד העולמות
  (ORÉVA, VELUNE, MIEL, ENCORE, ROSÉE, ELVÉA, CREMA, AURELLE וכל עולם חדש), "עוד עולם באותו קו", הוק לריל,
  סרטון קמפיין שמשלב עולמות, או ריל למותג של לקוח BrandOS — גם אם לא נאמר במפורש "הוק" או "סקיל".
  לתכנון הפקת וידאו AI בכלים חיצוניים (Kling, Seedance, Suno) — brandos-video-production-planner.
---

# Brand World Reel

A 30-second vertical motion reel built from a brand world's own website: its frame sequences, product photos,
signature element and copy. Every reel opens with a hook and is built around one signature scene that goes beyond the site. The motion is pure CSS on one timeline, rendered frame by
frame in a headless browser, so the result is exact and repeatable.

Why it works this way: the worlds already exist as sites with AI-generated sequences and a single promise. Reusing
those exact assets (not regenerating them) keeps the reel identical to the world, and a deterministic CSS timeline lets
every frame be checked before the MP4 is made.

## The heart of every reel: a signature scene
What makes these reels worth watching is at least one scene that goes beyond the site: the world's idea rebuilt as a new
mechanism. ENCORE's sundial turned into a dial with the jewellery of each hour inside it; ROSÉE's products on a clockwise dial
while the sky walks from night to day; the Pancakerie swap; CREMA's capsules orbiting the machine in 3D. Replaying the site's
assets is the frame around that moment, not the reel itself. Read `references/signature-scenes.md` before writing the spec.

## Pick the mode first

| | Studio mode (default) | Brand mode (BrandOS) |
|---|---|---|
| Who publishes | Brand Worlds Studio, to business owners | The brand, to its own customers |
| Hook speaks to | the client's pain — price comparison, not recognised without the logo, "too expensive"… | the brand's customer moment, from Brand DNA |
| Wrapper | hook → studio window "עולם מותג NN" with crop marks → world full screen with HUD layer tags → back to the window | hook → logo reveal → world → logo + brand CTA |
| Outro | answers the hook, then "אבחון פער המותג · 30 דק׳ · בלי עלות" | brand promise + shop/book CTA |

If the request does not say, it is studio mode. Read `references/hooks.md` before writing any hook.

## Workflow

### 1. Read the world
- Find the world in the repo (`<world>/index.html` or `<world>.html`) and its assets: frame sequences (`seq/`, `frames-desktop/`,
  `bloom/`, `porte/`, `land/` …), product and boutique images, and the world number (in `<title>`, e.g. "World N°14", "No.26").
- Pull the copy: the promise, the section headlines, the signature element (a dial, a drop, a leaf line, a sundial, a slice…).
  Quote the site; don't invent new slogans.
- Look at the sequence's first, middle and last frames (contact sheet) to see where the subject sits.
- If the site has a signature interaction (a carousel, a dial, a line through slides), read how the site builds it in its
  HTML/CSS/JS and plan to rebuild it the same way (recipe 11). If the owner sends a screen recording, treat it as the reference.

### 2. Spec first — always, before building
Send a short spec and wait for approval. The owner works "קודם איפיון, אחר כך יצירה". The spec has:
1. **Three hook options**: the line, the visual proof, the outro that answers it. Recommend one, in one line.
2. **Two signature-scene concepts**: idea → mechanism → what changes on every step. Recommend one. It takes the centre of the reel.
3. **A scene table** on the fixed timeline (time · scene · what is on screen · text), using the world's own moments.
4. At most 2–3 open questions, each with a recommended default.

Fixed studio timeline (30s):

| Time | Layer |
|---|---|
| 0.0–2.8 | HOOK: question + proof mechanic, copper ball rolling on its line |
| 2.6–5.4 | Studio window: "Brand Worlds Studio · עולם מותג NN", the world inside the window with crop marks, opens to full screen |
| 5.4–10 | 01 The Core — the hero sequence and the promise |
| 9.7–14.8 | 02 The Visual World — the signature scene (invented, beyond the site; may run longer and push the others) |
| 14.5–18.8 | 03 The Narrative / The Element |
| 18.5–22.8 | 04 Live Site / Touchpoints — boutique, cart, packaging, real product |
| 22.5–30 | 05 The Promise — calm, centred; it stays inside the window in the outro |
| 27–30 | Outro in the studio window: the answer to the hook + CTA |

A campaign film that combines several worlds uses the campaign structure instead (hook question → one before/after pair
per world with her copper ball and a world-shaped line opening a circular portal → pride line → close). See recipe 5 in
`references/motion-recipes.md`.

### 3. Build
- Copy `assets/reel-template.html` next to a local copy of the assets it uses (relative paths; the page loads from file://).
  The easiest path is a small Python generator that fills the template (see `examples/chasen-gen.py`): it keeps every timing
  in one place and makes re-renders after feedback quick.
- Fill the EDIT blocks: palette, world number, concept line, hook (keep one proof mechanic), HUD names, outro, the five scenes.
- Time things with the template's `data-show="a,b"`, `data-in="t"` and `data-seq=…` attributes (seconds). Write custom
  `@keyframes` only for real motion (dials, carousels, pans), with percentages = seconds / 30 × 100.
- Use the recipes in `references/motion-recipes.md` instead of inventing new mechanics; they already solve the traps
  (two animations on one element, 3D flattening, RTL alignment, clockwise dials, subjects drifting off-centre).
- Keep her brand elements: the copper ball and copper line (Brand Worlds Studio's signature), cream `#FAF8F3`, ink `#6B563F`,
  copper `#C4765A`, Cormorant Garamond for Latin display, Heebo for Hebrew.

### 4. Check stills, then render
- Stills: `node scripts/render.js reel.html 30 test/r 45,84,150,240,320,420,500,560,640,720,800,870`, stack them into one
  contact sheet and go through `references/qa-checklist.md`. Fix, re-shoot only the frames that changed.
- Full render (a few minutes, run it in the background): `node scripts/render.js reel.html 30 out/<WORLD>-<NN>.mp4`.
- 4:5 feed version: `scripts/frame45.sh out/<WORLD>-<NN>.mp4 out/<WORLD>-<NN>-4x5.mp4`.

### 5. Deliver
Send both MP4s with a short Hebrew summary: the hook, the scenes in order with times, and anything the owner should look at.
If the work lives on a Design canvas, add a board and a note there too. Mention once: 9:16 for Reels/Stories, 4:5 for the feed.

## Brand mode notes (BrandOS)
Inputs come from the client's Brand DNA: audience pain/moment, promise, signature element, palette, fonts, CTA, and the
assets (sequence, product shots). Replace the studio intro/outro/HUD with the brand's own: a 1.5s logo reveal after the hook,
chapter labels in the brand's typography (or none), and the brand CTA at the end. Timeline: hook 0–2.5 · world 2.5–27 ·
logo + CTA 27–30. Everything else — recipes, QA, render — is the same.

## Files
- `assets/reel-template.html` — studio-mode skeleton with the fixed wrapper, hook, HUD, outro and the timing helper.
- `assets/frame-4x5.html` — side panels for the 4:5 version (rendered once to PNG by frame45.sh).
- `scripts/render.js` — deterministic renderer (Playwright + ffmpeg). Prints loaded fonts and broken images.
- `scripts/frame45.sh` — 9:16 → 4:5 with the studio side panels; the reel is never cropped.
- `scripts/video2seq.sh` — a site film (mp4) → an image sequence for `data-seq`.
- `examples/chasen-gen.py` — a complete worked build (CHASEN°, World 19): fills the template from Python, flavour dial,
  pours, toppings, menu, promise. Start new worlds by copying its structure.
- `references/signature-scenes.md` — how to invent the scene beyond the site, mechanisms per idea, ready concepts.
- `references/hooks.md` — hook bank for both modes, writing rules, how to pick.
- `references/motion-recipes.md` — sequences, pans, clockwise dials, 3D carousel, ball + portal, leaf lines, stirred cup, cut runs, text.
- `references/qa-checklist.md` — what to check on the contact sheet and before delivery.
