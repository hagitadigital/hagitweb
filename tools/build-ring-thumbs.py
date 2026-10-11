"""Square thumbnails for the archive ring on brand-worlds/index.html.

Reads every world card in the gallery grid and writes brand-worlds/ring/<No>.webp
(360x360) for any number that doesn't have one yet. Pass --all to rebuild every thumbnail.
The ring falls back to the card image when a thumbnail is missing, so this is an optimisation.
"""
import os, re, sys, urllib.parse
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'brand-worlds', 'index.html')
OUT = os.path.join(ROOT, 'brand-worlds', 'ring')

html = open(PAGE, encoding='utf-8').read()
start = html.find('class="worlds-grid')
grid = html[start:html.find('</section>', start)]
os.makedirs(OUT, exist_ok=True)
for m in re.finditer(r'class="world-card[^"]*".*?world-card__nº">No\. (\d+)<.*?<img[^>]*src="([^"]+)"', grid, re.S):
    no, src = m.group(1), urllib.parse.unquote(m.group(2))
    out = os.path.join(OUT, f'{no}.webp')
    if os.path.exists(out) and '--all' not in sys.argv:
        continue
    im = Image.open(os.path.normpath(os.path.join(ROOT, 'brand-worlds', src))).convert('RGB')
    w, h = im.size
    side = min(w, h)
    left, top = (w - side) // 2, max(0, int((h - side) * 0.35))
    im.crop((left, top, left + side, top + side)).resize((360, 360), Image.LANCZOS).save(out, 'WEBP', quality=78)
    print('wrote', os.path.relpath(out, ROOT))
