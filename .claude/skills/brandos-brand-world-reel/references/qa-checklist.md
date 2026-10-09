# QA before the full render

Render stills first — they take seconds; a full render takes minutes:
`node scripts/render.js reel.html 30 test/r 45,84,150,240,320,420,500,560,640,720,800,870`
then stack them into one contact sheet with ffmpeg (`hstack=12,scale=2400:-1`) and look at it.

## Every reel
- [ ] There is a signature scene that does not exist on the site, with a visible state change on every step.
- [ ] Hook readable in the first second; the question is the biggest thing on screen; the proof mechanic is visible by 1.2s.
- [ ] Frame 0 already shows the question and the proof (it is the feed thumbnail); nothing builds in from an empty card.
- [ ] Every "ככה משווים" card is a generic no-name product, not the world's product greyed out; no world logo is visible on it.
- [ ] Hook → studio window transition is clean at 2.6–3.0s (no overlap of the hook question with "עולם מותג").
- [ ] "עולם מותג NN" — correct number, Hebrew (not "Monde").
- [ ] Inside the studio window (2.6–5.4s and 27–30s) the world shows something meaningful, not a blank background.
- [ ] HUD tag text matches the scene on screen in every window.
- [ ] No text over a busy area without a gradient behind it; dark text never sits on a dark scene.
- [ ] Subjects centred: check each sequence's last frame and each tile (bottles drift right in 16:9 sources).
- [ ] Per-step colours hold on each stop (no grey in-betweens) and text stays readable on the dark stops (recipe 16).
- [ ] Landed objects touch their surface — no floating jars (recipe 17).
- [ ] Dials turn clockwise; the item under the pointer matches the time label.
- [ ] Labels in cut sequences match their pictures.
- [ ] Every payoff (a card, a name, a reveal) stays fully visible ≈1.5–2s before the next scene starts covering it.
- [ ] Image runs breathe: ≥ ≈1.2s per product/boutique shot with soft crossfades (recipe 12).
- [ ] Any interaction copied from the site matches the site's construction — compare against the site's code or a screen recording (recipe 11).
- [ ] Fonts loaded (render.js prints them) and no BROKEN IMAGES line.
- [ ] The outro answers the hook, then the CTA (studio: אבחון פער המותג · 30 דק׳ · בלי עלות · hagitantebi.co.il).
- [ ] Last frame ≈ first frame of the next loop (cream), so the reel loops softly.

## Delivery
- [ ] 9:16 MP4: 1080×1920, 30fps, H.264, exactly 30.0s (`ffmpeg -i file` shows Duration 00:00:30.00).
- [ ] 4:5 MP4 via `scripts/frame45.sh` (1080×1350) for the LinkedIn / Facebook feed.
- [ ] One short summary to the owner: the hook, the scenes in order with times, what to check, and the 4:5 note
      (9:16 for Reels/Stories, 4:5 for the feed; in Ads Manager both can be attached to one ad per placement).
