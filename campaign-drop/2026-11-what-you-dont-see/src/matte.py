"""Cut the figure out of the take frames. Usage: matte.py first last [first last ...]"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter
from rembg import remove, new_session

R = os.path.dirname(os.path.abspath(__file__)) + '/'
os.makedirs(R + 'pm/me', exist_ok=True)
s = new_session('u2net_human_seg')
args = [int(a) for a in sys.argv[1:]]
for a, b in zip(args[::2], args[1::2]):
    for k in range(a, b + 1):
        im = Image.open(R + f'me/{k:04d}.jpg').convert('RGB')
        mask = remove(im, session=s, only_mask=True, post_process_mask=True)
        m = np.asarray(mask).astype(np.float32)
        rgb = np.asarray(im).astype(np.int16)
        # the vase of flowers beside her: pale / pink pixels in that corner are not hair
        reg = np.zeros(m.shape, bool)
        reg[500:720, 0:170] = True
        bright = rgb.sum(axis=2) > 430
        m[reg & bright] = 0
        mk = Image.fromarray(m.astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.6))
        out = im.convert('RGBA')
        out.putalpha(mk)
        out.save(R + f'pm/me/{k:04d}.webp', quality=88, method=2)
print('done')
