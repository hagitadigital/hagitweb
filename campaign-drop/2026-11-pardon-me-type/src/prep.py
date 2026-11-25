#!/usr/bin/env python3
"""Cut the presenter out of every frame of clips/*.mp4 (shot on a plain cream backdrop).
    python3 prep.py [clip-name ...]  ->  frames/<clip>/f_###.webp (figure with alpha, backdrop colour removed from the edges)
Needs: ffmpeg, pip install rembg onnxruntime. frames/ is generated, not committed."""
import pathlib, subprocess, sys, glob, os
import numpy as np
from rembg import remove, new_session
from PIL import Image, ImageFilter

HERE = pathlib.Path(__file__).resolve().parent
names = sys.argv[1:] or sorted(p.stem for p in (HERE / 'clips').glob('*.mp4'))
sess = new_session('isnet-general-use')
for c in names:
    d = HERE / 'frames' / c
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(HERE / 'clips' / f'{c}.mp4'), str(d / 'b_%03d.png')], check=True)
    for f in sorted(glob.glob(str(d / 'b_*.png'))):
        im = Image.open(f).convert('RGB')
        m = remove(im, session=sess, only_mask=True).filter(ImageFilter.MinFilter(3))
        I = np.asarray(im, np.float32); a = np.asarray(m, np.float32)[..., None] / 255
        B = I[:40, :40].reshape(-1, 3).mean(0)                       # the backdrop colour, from the top corner
        F = np.clip((I - (1 - a) * B) / np.maximum(a, .08), 0, 255)  # take the backdrop out of half-transparent edge pixels
        out = np.dstack([np.where(a > .02, F, I), a * 255]).astype(np.uint8)
        Image.fromarray(out, 'RGBA').save(f.replace('b_', 'f_').replace('.png', '.webp'), quality=92, method=2)
        os.remove(f)
    print(c, 'done', flush=True)
