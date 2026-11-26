#!/usr/bin/env python3
"""Cuts Hagit out of her own takes (shots/*.mp4, kept out of the repo) for every shot in schedule.json.
Writes frames/<shot>/f_###.webp (RGBA, 1080x1920, as shot) and stats.json (head top / head centre per shot, used by gen.py to place her).
    python3 gen.py && python3 prep.py && python3 gen.py        Needs ffmpeg, rembg, onnxruntime, opencv-python-headless."""
import json, pathlib, subprocess, sys, numpy as np, cv2
from rembg import remove, new_session
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
S = json.loads((HERE / 'schedule.json').read_text())
only = sys.argv[1:]
sess = new_session('isnet-general-use')
stats = json.loads((HERE / 'stats.json').read_text()) if (HERE / 'stats.json').exists() else {}
for sh in S['shots']:
    if only and sh['id'] not in only: continue
    d = HERE / 'frames' / sh['id']; d.mkdir(parents=True, exist_ok=True)
    for p in d.glob('*'): p.unlink()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{sh['f0'] / 30:.4f}", '-i', str(HERE / 'shots' / f"{sh['clip']}.mp4"),
                    '-frames:v', str(sh['n']), '-q:v', '2', str(d / 'b_%03d.jpg')], check=True)
    tops, cxs, hand = [], [], []
    for i in range(1, sh['n'] + 1):
        img = cv2.imread(str(d / f'b_{i:03d}.jpg'))
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        a = np.asarray(remove(Image.fromarray(rgb), session=sess, only_mask=True)).copy()
        a = np.clip((a.astype(np.float32) - 20) * (255 / 215), 0, 255).astype(np.uint8)      # drop the faint wall haze
        # keep the largest blob only (the light switch on the wall sometimes survives)
        n, lab, st, _ = cv2.connectedComponentsWithStats((a > 40).astype(np.uint8))
        if n > 2:
            keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); a[(lab != keep) & (lab != 0)] = 0
        ys = np.where((a > 128).sum(1) > 30)[0]
        if len(ys):
            top = int(ys[0]); band = a[top:top + 330] > 128; xs = np.where(band.sum(0) > 0)[0]
            tops.append(top); cxs.append(float((xs[0] + xs[-1]) / 2))
        if sh.get('track'):                                   # the offered palm: largest skin blob below the face
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); ycc = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            skin = ((ycc[..., 1] > 138) & (ycc[..., 2] < 128) & (hsv[..., 2] > 120) & (a > 128)).astype(np.uint8)
            skin[:int(tops[-1]) + 560] = 0
            skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
            m, lab2, st2, cen = cv2.connectedComponentsWithStats(skin)
            if m > 1:
                j = 1 + int(np.argmax(st2[1:, cv2.CC_STAT_AREA])); hand.append([float(cen[j][0]), float(st2[j, cv2.CC_STAT_TOP]), float(cen[j][1]), float(st2[j, cv2.CC_STAT_WIDTH])])
            else: hand.append(hand[-1] if hand else [540, 1200, 1300, 200])
        Image.fromarray(np.dstack([rgb, a]), 'RGBA').save(d / f'f_{i:03d}.webp', quality=90, method=2)
        (d / f'b_{i:03d}.jpg').unlink()
    stats[sh['id']] = dict(top=float(np.median(tops)), cx=float(np.median(cxs)))
    if hand:
        h = np.array(hand); ker = np.ones(7) / 7
        h = np.array([np.convolve(np.pad(h[:, j], 3, mode='edge'), ker, 'valid') for j in range(4)]).T
        stats[sh['id']]['hand'] = [[round(v, 1) for v in r] for r in h.tolist()]
    (HERE / 'stats.json').write_text(json.dumps(stats, indent=1))
    print(sh['id'], stats[sh['id']], flush=True)
print('done', flush=True)
