"""Swap the opening shot (frames 0-80) of a SITES reel for a new clip, keeping
the hook card, the zoom-into-the-laptop transition, everything after it, and the music.

usage: python -I swap-opening.py <original.mp4> <new-clip.mp4> <out.mp4> <work-dir> [--start 3.6]
The hook card is lifted from frame 0 of the original, so the text stays pixel-identical.
"""
import subprocess, sys, os, glob
from PIL import Image, ImageFilter, ImageDraw, ImageChops
import numpy as np

orig, clip, out, work = sys.argv[1:5]
start = float(sys.argv[sys.argv.index('--start') + 1]) if '--start' in sys.argv else 3.6
HEAD, XF0, CARD_OUT, ZOOM0 = 81, 73, (62, 68), 64   # frame numbers at 30fps
os.makedirs(work, exist_ok=True)
run = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)

run('-i', orig, '-vf', f'select=eq(n\\,0)+eq(n\\,{HEAD})', '-vsync', '0', f'{work}/o_%d.png')
o0 = Image.open(f'{work}/o_1.png').convert('RGB'); o81 = Image.open(f'{work}/o_2.png').convert('RGB')
W, H = o0.size
# inner picture area: full frame for 9:16, a 9:16 column inside the cream frame for 4:5
iw = round(H * 9 / 32) * 2 if W / H > 0.6 else W
ix = (W - iw) // 2

# --- hook card from frame 0 ---
a = np.asarray(o0).astype(int)
m = (abs(a[:, :, 0] - 246) < 9) & (abs(a[:, :, 1] - 243) < 9) & (abs(a[:, :, 2] - 238) < 11)
m[:, :ix + 8] = False; m[:, ix + iw - 8:] = False
ys = np.where(m[:H // 3].sum(1) > iw * 0.4)[0]; y0, y1 = ys.min(), ys.max() + 1
xs = np.where(m[y0 + 40:y1 - 40].sum(0) > 20)[0]; x0, x1 = xs.min(), xs.max() + 1
r = int(np.where(m[y0 + 1, x0:x0 + 80])[0].min()) + 2          # corner radius
card = o0.crop((x0, y0, x1, y1)).convert('RGBA')
mask = Image.new('L', card.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, card.size[0] - 1, card.size[1] - 1), r, fill=255)
card.putalpha(mask)
pad = 60
sh = Image.new('L', (card.size[0] + 2 * pad, card.size[1] + 2 * pad), 0)
sh.paste(mask.point(lambda v: v * 0.22), (pad, pad + 10))
sh = sh.filter(ImageFilter.GaussianBlur(18))
print('card', (x0, y0, x1, y1), 'radius', r, 'inner', ix, iw)

# --- new clip frames ---
run('-ss', str(start), '-i', clip, '-frames:v', str(HEAD), '-vf',
    f'fps=30,scale={iw}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={iw}:{H},unsharp=5:5:0.5',
    f'{work}/n_%03d.png')

fx, fy = 0.80, 0.84                                           # zoom target: the laptop
for i in range(HEAD):
    f = Image.open(f'{work}/n_{i + 1:03d}.png').convert('RGB')
    if i >= ZOOM0:
        p = ((i - ZOOM0) / (HEAD - 1 - ZOOM0)) ** 2
        s = 1 + 1.6 * p
        cw, ch = iw / s, H / s
        cx = iw / 2 + (fx * iw - iw / 2) * p; cy = H / 2 + (fy * H - H / 2) * p
        l = max(min(cx - cw / 2, iw - cw - 0.01), 0); t = max(min(cy - ch / 2, H - ch - 0.01), 0)
        cw, ch = min(cw, iw - l), min(ch, H - t)
        f = f.resize((iw, H), Image.BILINEAR, box=(l, t, l + cw, t + ch)).filter(ImageFilter.GaussianBlur(16 * p))
    frame = o0.copy(); frame.paste(f, (ix, 0))
    ca = 1 - min(max((i - CARD_OUT[0]) / (CARD_OUT[1] - CARD_OUT[0]), 0), 1)
    if ca > 0:
        frame.paste((40, 25, 15), (x0 - pad, y0 - pad), sh.point(lambda v: v * ca))
        c = card.copy(); c.putalpha(card.getchannel('A').point(lambda v: v * ca))
        frame.paste(c, (x0, y0), c)
    if i >= XF0:
        frame = Image.blend(frame, o81, (i - XF0 + 1) / (HEAD - XF0 + 1))
    frame.save(f'{work}/h_{i:03d}.png')

run('-framerate', '30', '-i', f'{work}/h_%03d.png', '-i', orig, '-filter_complex',
    f'[1:v]trim=start_frame={HEAD},setpts=PTS-STARTPTS[t];[0:v]format=yuv420p[h];[h][t]concat=n=2:v=1[v]',
    '-map', '[v]', '-map', '1:a', '-c:a', 'copy', '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
    '-pix_fmt', 'yuv420p', '-r', '30', '-movflags', '+faststart', out)
for p in glob.glob(f'{work}/*.png'): os.remove(p)
