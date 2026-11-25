#!/usr/bin/env python3
"""Cut the figure out of every frame of REGARD's five portrait clips.
    python3 prep.py   ->  frames/<n>/b_###.jpg (full frame) + f_###.webp (figure with alpha)
Needs: ffmpeg, pip install rembg onnxruntime. frames/ is generated, not committed."""
import pathlib, subprocess, glob
from rembg import remove, new_session
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
PORT = HERE.parents[2] / 'regard/assets/portraits'
CLIPS = ['01-la-muse', '02-licone', '03-la-poete', '04-la-directrice', '05-letoile']
sess = new_session('isnet-general-use')
for i, c in enumerate(CLIPS, 1):
    d = HERE / 'frames' / str(i)
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(PORT / f'{c}.mp4'), '-q:v', '2', str(d / 'b_%03d.jpg')], check=True)
    for f in sorted(glob.glob(str(d / 'b_*.jpg'))):
        im = Image.open(f).convert('RGB')
        m = remove(im, session=sess, only_mask=True)
        im.putalpha(m)
        im.save(f.replace('b_', 'f_').replace('.jpg', '.webp'), quality=90, method=2)
    print(c, 'done', flush=True)
