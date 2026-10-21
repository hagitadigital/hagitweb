# PM-Orbit.dc.html (the Design canvas artboard, 20.10) → orbit.html, a plain page the frame renderer can step through.
# Blob uploads are swapped for PARDON ME's own files (pardon-me/assets) and fresh mobile screenshots of the site.
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, 'PM-Orbit.dc.html')).read()
BLOBS = {
    '05c4298ec96d0e107fc133c0cbbdd12e': 'high-maintenance.webp', '0f1f2d82e47c76d379563060ee6ce499': 'none-of-your-business.webp',
    '45b1fb77266533ab6872be36e3c2fa6d': 'bad-influence.webp', 'c737598e5256c9e60c5a2c2bde6b7774': 'well-hello.webp',
    '6de6b78b41fb2a5ebc709deaade68192': 'print-well-hello.webp', '799228521d8053c4eaf88b6acf91509d': 'print-none-of-your-business.webp',
    'b57dbc7378f17d2306b7c3fa51f686ac': 'print-high-maintenance.webp', 'c603a32080a8e221d426240a846db0b2': 'print-bad-influence.webp',
    '3ad618f462e1ec11e57806eb610e8ee3': 'line.webp', '70c954f7d859a37de7f91988bd168cd0': 'ad-touch-yourself.webp',
    '8da2599babe3ec1b8f61c3d153992c5d': 'ad-i-kept-it.webp', '45c8f3bf75e7c73a323cf665ed187be8': 'ad-bad-decisions.webp',
    'e8dc994f7e5c4dc326cf15a905d1fea6': 'stationery.webp', '66b9d409a74dc718cc0c0504a5a25bf7': 'bag.webp',
    '8d92b6f5b00d8fac0b77858802d3bf2b': 'hero.webp', '3a5fa58dbdaa632668316992286013fa': 'site-phone.jpg',
    '803acb814a447e296d41403c52a83704': 'site-scroll.jpg', 'fee49bf61a63da9cad06c035ea473787': 'reveal.webp',
}
for k, v in BLOBS.items(): s = s.replace('/_blob/' + k, 'media/' + v)
left = re.findall(r'/_blob/[0-9a-f]+', s); assert not left, left
s = s.replace('<script src="./support.js"></script>\n', '')
helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
s = s.replace('<helmet>' + helmet + '</helmet>', '').replace('</head>', helmet + '</head>')
s = s.replace('<x-dc>', '').replace('</x-dc>', '')
s = re.sub(r'<script type="text/x-dc".*?</script>', '', s, flags=re.S)
open(os.path.join(HERE, 'orbit.html'), 'w').write(s)
print('ok')
