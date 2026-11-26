#!/usr/bin/env python3
"""NADLAN reel prep.
1) frames/her/b_###.jpg + f_###.webp — Hagit's opening (from her laptop take, frames in ../../2026-11-hagit-worlds/src/frames/take),
   with the RUE° site on the laptop screen, and her cut out for the number behind her.
2) frames/bld/{old,site,new}.webp — the three same-camera states of number 14 with the sky removed, so the number can sit behind the building."""
import pathlib, subprocess, numpy as np, cv2
from rembg import remove, new_session
from PIL import Image
from screen import screen
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TAKE = HERE.parents[1] / '2026-11-hagit-worlds/src/frames/take'
(HERE / 'frames/her').mkdir(parents=True, exist_ok=True); (HERE / 'frames/bld').mkdir(parents=True, exist_ok=True); (HERE / 'frames/rue').mkdir(parents=True, exist_ok=True)
if not (HERE / 'frames/rue/001.jpg').exists():
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(ROOT / 'sites/a/rue.mp4'), '-q:v', '2', str(HERE / 'frames/rue/%03d.jpg')], check=True)
# ── the three states of the building: flood the sky from the top edge, keep everything else
for name, src in [('old', 'rue/assets/01-old.webp'), ('site', 'sites/nadlan/fence.webp'), ('new', 'rue/assets/03-new.webp')]:
    img = cv2.cvtColor(np.asarray(Image.open(ROOT / src).convert('RGB')), cv2.COLOR_RGB2BGR)
    h, w = img.shape[:2]; blur = cv2.GaussianBlur(img, (0, 0), 1.2); sky = np.zeros((h + 2, w + 2), np.uint8)
    for x in range(4, w, 12):
        if sky[1, x + 1] == 0: cv2.floodFill(blur, sky, (x, 0), 0, (3, 3, 3), (3, 3, 3), 4 | (255 << 8) | cv2.FLOODFILL_MASK_ONLY)
    sky = sky[1:-1, 1:-1]; sky[int(h * .62):] = 0
    a = 255 - cv2.GaussianBlur(cv2.dilate(sky, np.ones((3, 3), np.uint8)), (0, 0), 1.0)
    Image.fromarray(np.dstack([cv2.cvtColor(img, cv2.COLOR_BGR2RGB), a]), 'RGBA').save(HERE / f'frames/bld/{name}.webp', quality=92, method=4)
    print(name, 'sky share', round(float((sky > 0).mean()), 3), flush=True)
# ── her opening: 2 seconds = 60 output frames
F0, SP, N = 300, .7, 60
take = lambda f: cv2.imread(str(TAKE / f'b_{f + 1:03d}.jpg'))
lo, hi = F0 - 8, F0 + int(N * SP) + 8
Q = {f: q for f in range(lo, hi + 1) for q in [screen(take(f))[0]] if q is not None}
ks = sorted(Q); arr = np.array([Q[k] for k in ks]).reshape(len(ks), 8)
full = np.array([[np.interp(f, ks, arr[:, j]) for j in range(8)] for f in range(lo, hi + 1)])
med = np.array([np.median(full[max(0, i - 6):i + 7], axis=0) for i in range(len(full))]); bad = np.abs(full - med).max(1) > 16; full[bad] = med[bad]
ker = np.array([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], float); ker /= ker.sum()
sm = np.array([np.convolve(np.pad(full[:, j], 5, mode='edge'), ker, 'valid') for j in range(8)]).T
sess = new_session('isnet-general-use'); alpha = {}
for n in range(N):
    f = F0 + round(n * SP); img = take(f); q = sm[f - lo].reshape(4, 2).astype(np.float32)
    src = cv2.imread(str(HERE / f'frames/rue/{12 + n:03d}.jpg')); h, w = src.shape[:2]
    warp = cv2.warpPerspective(src, cv2.getPerspectiveTransform(np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32), q), (720, 1280), flags=cv2.INTER_AREA)
    poly = np.zeros((1280, 720), np.uint8); cv2.fillConvexPoly(poly, q.astype(np.int32), 255)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    scr = cv2.morphologyEx(cv2.bitwise_and(((hsv[..., 1] < 52) & (hsv[..., 2] > 105)).astype(np.uint8) * 255, poly), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    a = cv2.GaussianBlur(scr, (0, 0), 1.1).astype(np.float32)[..., None] / 255
    shade = np.clip(hsv[..., 2:3].astype(np.float32) / 235, .55, 1.0) ** .6
    comp = (img * (1 - a) + warp * shade * a).astype(np.uint8)
    if f not in alpha: alpha[f] = np.asarray(remove(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), session=sess, only_mask=True))
    cv2.imwrite(str(HERE / f'frames/her/b_{n:03d}.jpg'), comp, [cv2.IMWRITE_JPEG_QUALITY, 93])
    Image.fromarray(np.dstack([cv2.cvtColor(comp, cv2.COLOR_BGR2RGB), alpha[f]]), 'RGBA').save(HERE / f'frames/her/f_{n:03d}.webp', quality=90, method=2)
print('done', flush=True)
