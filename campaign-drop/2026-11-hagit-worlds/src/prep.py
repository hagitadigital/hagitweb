#!/usr/bin/env python3
"""Builds frames/out/b_###.jpg + f_###.webp for every output frame of Hagit's shots, from schedule.json:
the laptop's white screen is replaced by the scheduled site recording, and she (with the laptop) is cut out for the words behind her.
Also frames/site/<site>_###.jpg for the full-screen cards.   Needs ffmpeg, rembg, onnxruntime, opencv-python-headless."""
import json, pathlib, subprocess, numpy as np, cv2
from rembg import remove, new_session
from PIL import Image
from screen import screen
HERE = pathlib.Path(__file__).resolve().parent
SITES = HERE.parents[2] / 'sites/a'
S = json.loads((HERE / 'schedule.json').read_text())
(HERE / 'frames/out').mkdir(parents=True, exist_ok=True); (HERE / 'frames/site').mkdir(parents=True, exist_ok=True)
for site in ('oreva', 'mirvach', 'rue'):
    if not (HERE / f'frames/site/{site}_001.jpg').exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(SITES / f'{site}.mp4'), '-q:v', '2', str(HERE / f'frames/site/{site}_%03d.jpg')], check=True)
take = lambda f: cv2.imread(str(HERE / f'frames/take/b_{f + 1:03d}.jpg'))
# 1) track the screen on every take frame that shows it, fill gaps, smooth
need = sorted({e['take'] for e in S['her'] if e['screen']})
lo, hi = need[0], need[-1]
Q = {}
for f in range(lo, hi + 1):
    q, _ = screen(take(f))
    if q is not None:
        W = 720
        if q[1][0] < W - 6 and q[2][0] > W - 6 or (q[1][0] > W - 30): pass
        Q[f] = q
ks = sorted(Q); arr = np.array([Q[k] for k in ks]).reshape(len(ks), 8)
full = np.array([[np.interp(f, ks, arr[:, j]) for j in range(8)] for f in range(lo, hi + 1)])
# reject jumps (a mis-detected edge), then smooth
med = np.array([np.median(full[max(0, i - 4):i + 5], axis=0) for i in range(len(full))])
bad = np.abs(full - med).max(1) > 28; full[bad] = med[bad]
ker = np.array([1, 2, 3, 2, 1], float); ker /= ker.sum()
sm = np.array([np.convolve(np.pad(full[:, j], 2, mode='edge'), ker, 'valid') for j in range(8)]).T
quad = {f: sm[f - lo].reshape(4, 2).astype(np.float32) for f in range(lo, hi + 1)}
print('tracked', len(ks), 'of', hi - lo + 1, 'rejected', int(bad.sum()), flush=True)
# 2) composite + cut out, one pair per output frame
sess = new_session('isnet-general-use'); alpha = {}
for e in S['her']:
    f = e['take']; img = take(f); comp = img
    if e['screen']:
        site, sf = e['screen']; src = cv2.imread(str(HERE / f'frames/site/{site}_{sf:03d}.jpg')); q = quad[f]
        h, w = src.shape[:2]
        M = cv2.getPerspectiveTransform(np.array([[0, 0], [w, 0], [w, h], [0, h]], np.float32), q)
        warp = cv2.warpPerspective(src, M, (720, 1280), flags=cv2.INTER_AREA)
        poly = np.zeros((1280, 720), np.uint8); cv2.fillConvexPoly(poly, q.astype(np.int32), 255)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        scr = ((hsv[..., 1] < 52) & (hsv[..., 2] > 105)).astype(np.uint8) * 255      # white screen; fingers and bezel fall out
        scr = cv2.morphologyEx(cv2.bitwise_and(scr, poly), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        a = cv2.GaussianBlur(scr, (0, 0), 1.1).astype(np.float32)[..., None] / 255
        shade = np.clip(hsv[..., 2:3].astype(np.float32) / 235, .55, 1.0) ** .6          # keep the screen's own light falloff
        comp = (img * (1 - a) + warp * shade * a).astype(np.uint8)
    if f not in alpha:
        alpha[f] = np.asarray(remove(Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), session=sess, only_mask=True))
    n = e['out']
    cv2.imwrite(str(HERE / f'frames/out/b_{n:03d}.jpg'), comp, [cv2.IMWRITE_JPEG_QUALITY, 93])
    rgba = np.dstack([cv2.cvtColor(comp, cv2.COLOR_BGR2RGB), alpha[f]])
    Image.fromarray(rgba, 'RGBA').save(HERE / f'frames/out/f_{n:03d}.webp', quality=90, method=2)
    if n % 60 == 0: print('frame', n, flush=True)
print('done', flush=True)
