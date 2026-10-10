# Campaign & ad work (paid ads, retargeting reels, ad recuts)

Applies to every session, local or cloud (claude.ai/code).

- **Cloud session:** put everything you make for a campaign under `campaign-drop/<YYYY-MM-campaign>/`
  (e.g. `campaign-drop/2026-10-choose/retarget/…`): renders (.mp4) plus their source (html/js) in `src/`.
  Commit and push to your `claude/*` branch. **Never merge campaign work into main** — main is the public
  GitHub Pages site. Hagit's machine pulls the branch into `brandworld_ad/` with
  `brandworld_ad/_tools/sync-branches.py`.
- **Local session:** campaign files live in `brandworld_ad/<YYYY-MM-campaign>/` (local only, gitignored).
  Before any campaign/ad work, run `python -I brandworld_ad/_tools/sync-branches.py` and pull what's new,
  then read `brandworld_ad/INDEX.md`. Add a row to INDEX.md for every creative you make.
- Meta setup docs stay in `.briefs/campaign-sep2026/` (or the current campaign's `.briefs/` folder).
- Creative rules: frame 0 already shows the hook question and its proof (it is the feed thumbnail);
  a "ככה משווים" card is a generic no-name product, never the world's product greyed out.

# New brand world — where it must appear

Every new world (`<slug>/index.html`, next number in the gallery) is added in the same change to all four places:
- `brand-worlds/index.html` — a `world-card` at the top of the grid with the next `No.`, plus the 30s film button when a reel exists
  (`images/home-worlds/live/films/<slug>.mp4` + `.jpg`).
- `links.html` — the "Now" rail: new card first with `World No.NN · New`, remove "New" from the previous one, drop the fifth card.
- `index.html` — the worlds train (`#worldsTrain`): new `motion-card` first.
- `sitemap.xml` — rebuild with `python tools/build-sitemap.py` after the commit.
Card image: `images/home-worlds/<slug>.webp` (1200×630).
