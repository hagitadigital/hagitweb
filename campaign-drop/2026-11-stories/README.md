# Stories — Nov 2026 (6 frames, 1080×1920)

- Root PNGs: clean, ready to upload. Add the Instagram sticker in the empty area of each frame.
- `_guides/`: the same frames with a dashed box showing where the sticker goes and which kind (poll / link / slider / question).
- Source: `src/stories.html`. To render again: open it with Playwright at 1080×1920 and screenshot `#s1`…`#s6` (add `body.hide-guides` for the clean version).
- Top and bottom ~150px are left empty for the Instagram UI.

## questions/ — question & poll series (8 frames)
In the style of the CHASEN / ROSÉE stories. q1 (logo hidden) and q2 (the answer) are posted as a pair.
To render again: `python3 src/build.py`, then screenshot every `section` in `src/questions.html` (body.clean = without the sticker frames).
