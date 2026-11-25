#!/usr/bin/env python3
"""Second pass on frames/<clip>/f_*.webp: remove pockets of backdrop that the matte kept between hair, ear and neck.
Only above the collar (y < 1180), only pixels whose colour is the backdrop's.   python3 despill.py [--test file]"""
import sys, glob, pathlib, numpy as np
from PIL import Image, ImageFilter
HERE = pathlib.Path(__file__).resolve().parent
def fix(f, out=None):
    im = Image.open(f).convert('RGBA'); A = np.asarray(im, np.float32)
    rgb, a = A[..., :3], A[..., 3] / 255
    B = rgb[:40, :40].reshape(-1, 3).mean(0)
    d = np.sqrt(((rgb - B) ** 2).sum(-1))
    keep = np.clip((d - 16) / 16, 0, 1)                    # 0 = backdrop colour, 1 = anything else
    y = np.arange(A.shape[0])[:, None]
    zone = np.clip((1180 - y) / 60, 0, 1)                   # fade the effect out at the collar
    k = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    keep = np.asarray(k, np.float32) / 255
    a2 = a * (1 - zone * (1 - keep))
    Image.fromarray(np.dstack([rgb, a2 * 255]).astype(np.uint8), 'RGBA').save(out or f, quality=92, method=2)
if len(sys.argv) > 2 and sys.argv[1] == '--test': fix(sys.argv[2], sys.argv[3])
else:
    for f in sorted(glob.glob(str(HERE / 'frames' / '0*' / 'f_*.webp'))): fix(f)
    print('done')
