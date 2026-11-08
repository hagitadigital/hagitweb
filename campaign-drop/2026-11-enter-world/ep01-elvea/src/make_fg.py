# Cuts the hand/arm that overlaps the board panels out of each pointing still, so it can sit on top of the board content.
# Output: studio/fg/<S>.png (941x1672 RGBA, opaque only where something covers a panel).
import json, numpy as np, os
from PIL import Image, ImageDraw, ImageFilter
here = os.path.dirname(os.path.abspath(__file__)); studio = os.path.join(here, '..', '..', 'studio')
Q = json.load(open(os.path.join(studio, 'quads.json')))
names = {'S1': 'series-S1-open', 'S2': 'series-S2-top', 'S3': 'series-S3-bottom', 'S4': 'series-S4-middle'}
os.makedirs(os.path.join(studio, 'fg'), exist_ok=True)
for k, n in names.items():
    im = Image.open(os.path.join(studio, n + '.webp')).convert('RGB'); a = np.asarray(im).astype(int)
    alpha = np.zeros(a.shape[:2], np.uint8)
    for q in Q[k]:
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).polygon([tuple(p) for p in q], fill=255)
        inside = np.asarray(m) > 0
        # chroma (colour normalised by brightness) so the panel's own shading doesn't count; dark sleeve counts
        lum = a.sum(-1, keepdims=True) + 1
        ch = a / lum; med = np.median(ch[inside], axis=0)
        dev = ((np.abs(ch - med).sum(-1) > 0.045) | (a.max(-1) < 110)) & inside
        alpha |= (dev * 255).astype(np.uint8)
    am = Image.fromarray(alpha).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert('RGBA'); out.putalpha(am); out.save(os.path.join(studio, 'fg', k + '.png'))
    print(k, int((np.asarray(am) > 128).sum()), 'px')
