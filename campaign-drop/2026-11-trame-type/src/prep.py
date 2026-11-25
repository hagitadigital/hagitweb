#!/usr/bin/env python3
"""TRAME° runway clips -> frames/<look>/b_###.jpg (820x1080 crop around the model) + f_###.webp (the model, cut out).
Also frames/maison/b_###.jpg from the atelier film.   python3 prep.py
Needs ffmpeg, pip install rembg onnxruntime. frames/ is generated, not committed."""
import pathlib, subprocess, glob
from rembg import remove, new_session
from PIL import Image
HERE = pathlib.Path(__file__).resolve().parent
A = HERE.parents[2] / 'trame/assets'
CLIPS = {'emotion': (1030, 0, 241), 'form': (968, 40, 120), 'movement': (974, 40, 120), 'future': (978, 40, 120)}  # crop x, first frame, count
d = HERE / 'frames/maison'; d.mkdir(parents=True, exist_ok=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(A / 'maison-film.mp4'), '-q:v', '3', str(d / 'b_%03d.jpg')], check=True)
sess = new_session('isnet-general-use')
for c, (x0, f0, n) in CLIPS.items():
    d = HERE / 'frames' / c; d.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(A / f'hero-{c}.mp4'), '-vf', f"select='gte(n,{f0})*lt(n,{f0+n})',crop=820:1080:{x0}:0",
                    '-vsync', '0', '-q:v', '2', str(d / 'b_%03d.jpg')], check=True)
    for f in sorted(glob.glob(str(d / 'b_*.jpg'))):
        im = Image.open(f).convert('RGB'); im.putalpha(remove(im, session=sess, only_mask=True))
        im.save(f.replace('b_', 'f_').replace('.jpg', '.webp'), quality=90, method=2)
    print(c, 'done', flush=True)
