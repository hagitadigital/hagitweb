# Stories — Nov 2026 (6 frames, 1080×1920)

- Root PNGs: clean, ready to upload. Add the Instagram sticker in the empty area of each frame.
- `_guides/`: the same frames with a dashed box showing where the sticker goes and which kind (poll / link / slider / question).
- Source: `src/stories.html`. To render again: open it with Playwright at 1080×1920 and screenshot `#s1`…`#s6` (add `body.hide-guides` for the clean version).
- Instagram safe zone: nothing important in the top 250px or the bottom 340px (the reply bar and the action buttons cover them).

## questions/ — question & poll series (8 frames)
In the style of the CHASEN / ROSÉE stories. q1 (logo hidden) and q2 (the answer) are posted as a pair.
To render again: `python3 src/build.py`, then screenshot every `section` in `src/questions.html` (body.clean = without the sticker frames).

## copper/ — animated series with the copper ball and line (4 × MP4, 9:16)
The ball rolls along the copper line through the story; frame 0 already shows the question.
PNG = the final frame (for a still story). `_guides/` = where the sticker goes.
To render again: `node copper/src/render.js copper <a|b|c|d> 30`, then ffmpeg from `_frames/<s>/%04d.jpg`.
