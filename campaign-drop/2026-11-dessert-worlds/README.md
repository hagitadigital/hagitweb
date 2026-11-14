# DESSERT WORLDS MINI v3 (30fps, 15.7s, silent)

- `DESSERT-WORLDS-MINI-v3-9x16.mp4` 1080x1920
- `DESSERT-WORLDS-MINI-v3-4x5.mp4` 1080x1350

Recut of `DESSERT-WORLDS-MINI-9x16.mp4` (the original is not in this folder; it is the first argument of the build).

- 0.0-2.6s opening kept; the bowl under the line is `bol/assets/bowl-foret.webp`, turning clockwise
- 2.3-8.0s BOL°: `src/in/kling-bol-berries.mp4` then `src/in/kling-bol-kiwi.mp4` (24fps frames played at 30fps = 1.25x)
- 7.7-10.3s CHASEN°: the walker band of the opening, scaled down, over `src/in/chasen-glasses.webp`
- 10.3-13.2s SIGNÉ°: `src/in/kling-signe-chou.mp4` (Kling 4.0 image-to-video of `src/in/signe-still-clean.png`, the original frame with its label removed); the label is lifted from the original frames
- 12.9s-end end card, original frames

4x5 uses the same timeline; each scene is laid out for its own 1350px window (see `Y_A..Y_E` in `build.py`).

Render:

    node src/labels.js <work>
    python3 src/build.py <orig.mp4> <work> <out.mp4> 9x16
    python3 src/build.py <orig.mp4> <work> <out.mp4> 4x5
