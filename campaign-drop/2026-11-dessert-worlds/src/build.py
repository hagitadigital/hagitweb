"""DESSERT WORLDS MINI v2 — 9:16, 1080x1920, 30fps, silent.
Recut of DESSERT-WORLDS-MINI-9x16.mp4:
  A  opening (walker on the line) kept; the bowl under the line is now the BOL° site bowl, turning
  B  BOL°: two Kling clips (she turns the bowl) replace the "sitting in the bowl" shot
  C  CHASEN°: she walks the line under the five matcha glasses (replaces MIEL°)
  D  SIGNÉ° + end card, untouched
Run: node labels.js <work> ; python3 build.py <orig.mp4> <kling_berries.mp4> <kling_kiwi.mp4> <matcha.webp> <work> <out.mp4>
"""
import sys, os, subprocess, glob
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
ORIG, K1, K2, MATCHA, WORK, OUT = sys.argv[1:7]
HERE = os.path.dirname(os.path.abspath(__file__))
BOWL = os.path.join(HERE, '..', '..', '..', 'bol', 'assets', 'bowl-foret.webp')
W, H, FPS = 1080, 1920, 30
BG = np.array([241, 234, 218], np.float32)          # opening cream
ease = lambda x: x * x * (3 - 2 * x)
clamp = lambda x: max(0.0, min(1.0, x))

def frames(src, name, vf=None):
    d = os.path.join(WORK, name)
    if not glob.glob(d + '/*.png'):
        os.makedirs(d, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src] + (['-vf', vf] if vf else []) + [d + '/%04d.png'], check=True)
    return sorted(glob.glob(d + '/*.png'))
load = lambda p: np.asarray(Image.open(p).convert('RGB'), np.float32)

of = frames(ORIG, 'of')
KV = 'scale=1084:1922:flags=lanczos,crop=1080:1920,unsharp=5:5:0.5'
k1 = frames(K1, 'k1', KV); k2 = frames(K2, 'k2', KV)      # 24fps frames played at 30fps (1.25x)

def over(base, rgba, x=0, y=0, a=1.0):
    """alpha-composite a float RGBA array onto base at (x, y)"""
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    src = rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    al = src[..., 3:4] / 255 * a
    base[y0:y1, x0:x1] = base[y0:y1, x0:x1] * (1 - al) + src[..., :3] * al

# ── labels (pill + name, then the tagline) ──
def label(name):
    im = np.asarray(Image.open(os.path.join(WORK, f'label-{name}.png')).convert('RGBA'), np.float32)
    return im[:352], im[352:]
def put_label(fr, lab, t, t_out=None):
    top, tag = lab
    fo = 1 - clamp((t - t_out) / .25) if t_out is not None else 1
    a = ease(clamp((t - .15) / .35)); over(fr, top, 0, int(round(14 * (1 - a))), a * fo)
    a = ease(clamp((t - .55) / .35)); over(fr, tag, 0, 352 + int(round(14 * (1 - a))), a * fo)
L_BOL, L_CHA = label('bol'), label('chasen')

# ── A: opening, bowl replaced by the turning site bowl ──
NA = 78
D = 1400; CX, CY = 935, 1985
bowl = Image.open(BOWL).convert('RGBA').resize((D, D), Image.LANCZOS)
sh = Image.new('RGBA', (D + 240, D + 240), (0, 0, 0, 0))
ImageDraw.Draw(sh).ellipse((120 + 14, 120 + 14, 120 + D - 14, 120 + D - 14), fill=(70, 50, 30, 80))
sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(40)), np.float32)
ramp = np.clip((np.arange(H, dtype=np.float32) - 1204) / 24, 0, 1)[:, None, None]
def scene_a(i):
    fr = load(of[min(i, NA - 1)])
    fr = fr * (1 - ramp) + BG * ramp                       # clear everything under the line
    over(fr, sh, CX - D // 2 - 120 + 10, CY - D // 2 - 120 + 34)
    ang = 20 - 62 * (i / NA)                               # clockwise, steady
    b = np.asarray(bowl.rotate(ang, Image.BICUBIC), np.float32)
    over(fr, b, CX - D // 2, CY - D // 2)
    return fr

# ── B: BOL°, the two Kling clips ──
XF = 10; N1 = len(k1); N2 = 88
def scene_b(i):
    t = i / FPS
    if i < N1 - XF: fr = load(k1[i])
    elif i < N1:
        a = ease((i - (N1 - XF) + 1) / (XF + 1)); fr = load(k1[i]) * (1 - a) + load(k2[i - (N1 - XF)]) * a
    else: fr = load(k2[i - (N1 - XF)])
    put_label(fr, L_BOL, t)
    return fr
NB = N1 - XF + N2

# ── C: CHASEN°, the walker on the line under the matcha glasses ──
S = 0.82; LY = 1570                                        # walker scale, line y
m = Image.open(MATCHA).convert('RGB'); mw = W; mh = round(m.height * W / m.width)
m = m.resize((mw, mh), Image.LANCZOS); OY = -70
cv = Image.new('RGB', (W, H)); cv.paste(m, (0, OY))
edge = np.asarray(m, np.float32)[-30:].mean(0)             # extend the backdrop below the photo
edge = np.asarray(Image.fromarray(edge[None].astype(np.uint8)).resize((6, 1), Image.BOX).resize((W, 1), Image.BICUBIC), np.float32)
cvn = np.asarray(cv, np.float32); by = OY + mh
cvn[by:] = edge
f = np.clip((np.arange(H, dtype=np.float32) - (by - 90)) / 90, 0, 1)[:, None, None]
cvn = cvn * (1 - f) + edge * f
Y0, Y1 = 540, 1200; ORIG_LY = 1159                         # walker band in the opening
def to_c(band_rgb):
    """band from the opening → same band scaled, with its cream background divided out"""
    r = np.clip(band_rgb / BG, 0, 1.25)
    im = Image.fromarray(np.clip(r * 200, 0, 255).astype(np.uint8)).resize((round(W * S), round((Y1 - Y0) * S)), Image.LANCZOS)
    return np.asarray(im, np.float32) / 200
BX = round((W - W * S) / 2); BY = LY - round((ORIG_LY - Y0) * S)
f0 = load(of[0])
line_rgb = f0[1158, 60]; lh = 3
base_c = cvn.copy()
base_c[LY - lh // 2 - 1:LY + lh // 2 + 1] = line_rgb / BG * base_c[LY - lh // 2 - 1:LY + lh // 2 + 1]
bw, bh = round(W * S), round((Y1 - Y0) * S)
xs = np.arange(bw, dtype=np.float32)
def paste_cols(fr, ratio, x0, x1, feather=26):
    a = np.clip(np.minimum(xs - (x0 - feather), (x1 + feather) - xs) / feather, 0, 1)[None, :, None]
    reg = fr[BY:BY + bh, BX:BX + bw]
    fr[BY:BY + bh, BX:BX + bw] = reg * (1 - a) + np.clip(cvn[BY:BY + bh, BX:BX + bw] * ratio, 0, 255) * a
NC = NA
def scene_c(i):
    fr = base_c.copy()
    band = load(of[i])[Y0:Y1]
    cols = np.where((np.abs(band[:ORIG_LY - Y0 - 8] - BG).max(2) > 28).sum(0) > 6)[0]   # walker + the dot that leads her
    if len(cols): paste_cols(fr, to_c(band), cols.min() * S, cols.max() * S)
    put_label(fr, L_CHA, i / FPS)
    return fr

# ── D: SIGNÉ° + end card from the original ──
D0 = 286; ND = len(of) - D0
scene_d = lambda i: load(of[D0 + i])

# ── timeline ──
XAB, XBC, FCD = 10, 9, 6
tl = []
for i in range(NA - XAB): tl.append(('a', i))
for j in range(XAB): tl.append(('ab', NA - XAB + j, j))
for i in range(XAB, NB - XBC): tl.append(('b', i))
for j in range(XBC): tl.append(('bc', NB - XBC + j, j))
for i in range(XBC, NC): tl.append(('c', i))
for i in range(ND): tl.append(('d', i))
print(len(tl), 'frames', len(tl) / FPS, 's')
only = [int(x) for x in sys.argv[7].split(',')] if len(sys.argv) > 7 else None
ff = None if only else subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for n, e in enumerate(tl):
    if only and n not in only: continue
    k = e[0]
    if k == 'a': fr = scene_a(e[1])
    elif k == 'ab':
        a = ease((e[2] + 1) / (XAB + 1)); fr = scene_a(e[1]) * (1 - a) + scene_b(e[2]) * a
    elif k == 'b': fr = scene_b(e[1])
    elif k == 'bc':
        a = ease((e[2] + 1) / (XBC + 1)); fr = scene_b(e[1]) * (1 - a) + scene_c(e[2]) * a
    elif k == 'c':
        fr = scene_c(e[1]); left = NC - 1 - e[1]
        if left < FCD: fr = fr * ((left + 1) / (FCD + 1))            # dip to black, as the original does before SIGNÉ°
    else: fr = scene_d(e[1])
    out = np.clip(fr + .5, 0, 255).astype(np.uint8)
    if only: Image.fromarray(out).save(os.path.join(WORK, f'chk-{n:04d}.png'))
    else: ff.stdin.write(out.tobytes())
if ff: ff.stdin.close(); ff.wait()
