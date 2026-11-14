# DESSERT WORLDS MINI v2 (9:16, 1080x1920, 30fps, 16.4s, silent)

Recut of `DESSERT-WORLDS-MINI-9x16.mp4` (the original is not in this folder; it is the first input of the build).

- 0.0-2.6s opening kept; the bowl under the line is `bol/assets/bowl-foret.webp`, turning clockwise
- 2.3-8.0s BOL°: `src/in/kling-bol-berries.mp4` then `src/in/kling-bol-kiwi.mp4` (24fps frames played at 30fps = 1.25x)
- 7.7-10.3s CHASEN°: the walker band of the opening, at 82%, over `src/in/chasen-glasses.webp`
- 10.3s-end SIGNÉ° + end card, original frames

Render:

    node src/labels.js <work>
    python3 src/build.py <orig.mp4> src/in/kling-bol-berries.mp4 src/in/kling-bol-kiwi.mp4 src/in/chasen-glasses.webp <work> <out.mp4>
