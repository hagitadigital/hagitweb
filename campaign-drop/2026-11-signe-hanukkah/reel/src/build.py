"""SIGNÉ° Les Lumières reel v2: Hagit's v1 (src/reel-v1.html) with three scenes moved onto the Kling clips.

    python -I src/build.py          (run from campaign-drop/2026-11-signe-hanukkah/reel/)

Builds a/ (assets + image sequences cut from ../clips) and reel-v2.html. Then render with the reel skill:
    node src/render.js reel-v2.html 30 out/SIGNE-lumieres-v2.mp4

What changes against v1 (everything else is v1 untouched):
  02 Les Lumières  the four crossfading stills -> drop + three mid-spin swaps; names and candles follow the video
  03 Le Cœur       still -> the filling clip
  04 La Boîte      CSS box + "Signé, ce soir" -> the coffret opening clip (the lid carries the signature)
"""
import os, re, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # .../reel
CAMP = HERE.parent                                    # .../2026-11-signe-hanukkah
REPO = CAMP.parent.parent
A = HERE / 'a'
D = 30.0
def P(t): return f'{max(0, min(D, t)) / D * 100:.3f}%'
SEQ_OUT = ['-f', 'image2', '-c:v', 'libwebp', '-quality', '86']   # one still per frame, not an animated webp
def ff(*args): subprocess.run(['ffmpeg', '-v', 'error', '-y', *map(str, args)], check=True)

# ── timing of 02 Les Lumières (seconds on the reel clock) ─────────────────────────────
SEQ_B = 9.75                  # the clip starts
DROP = (0.6, 2.4)             # source window of drop-noir.mp4, 1x — lands at src 1.9
WHIPS = [('whip-noir-framboise', 1.0, 3.0), ('whip-framboise-pistache', 0.6, 2.6), ('whip-pistache-vanille', 0.9, 2.9)]
WHIP_SPEED = 1.5
WHIP_MID = [1.7, 1.3, 1.55]   # source time where the glaze swaps (middle of the spin)
VAN_HOLD = (2.9, 4.0)         # the settled Vanille after the last spin, 1x

t = SEQ_B
land = SEQ_B + (1.9 - DROP[0]); t += DROP[1] - DROP[0]
swaps = []
for (name, a, b), m in zip(WHIPS, WHIP_MID):
    swaps.append(t + (m - a) / WHIP_SPEED); t += (b - a) / WHIP_SPEED
seq_b_end = t + (VAN_HOLD[1] - VAN_HOLD[0])
FADE = 0.1
labels = [(land, swaps[0] - 0.12), (swaps[0] + 0.12, swaps[1] - 0.12), (swaps[1] + 0.12, swaps[2] - 0.12), (swaps[2] + 0.12, 15.6)]
for (a1, b1), (a2, _) in zip(labels, labels[1:]):
    assert a2 >= b1 + 2 * FADE - 1e-6, 'text would crossfade with text'
CANDLES = [x for (a, _) in labels for x in (a, a + 0.25)]      # two candles light with every edition
CANDLE_X = [850, 758, 666, 574, 482, 390, 298, 206]

# ── assets ────────────────────────────────────────────────────────────────────────────
def build_assets():
    if A.exists(): shutil.rmtree(A)
    (A / 'pour').mkdir(parents=True)
    for f in sorted((REPO / 'signe/assets/pour').glob('f*.webp')): shutil.copy(f, A / 'pour' / f.name)
    shutil.copy(REPO / 'signe/assets/piping-signature.webp', A / 'piping-signature.webp')
    ff('-i', CAMP / 'assets/generic-sufganiya-v1.png', '-vf', 'scale=1200:-1', '-quality', '86', A / 'generic-sufganiya.webp')
    for e in ['noir', 'framboise', 'pistache', 'vanille']:   # v1 still references them (unused classes stay harmless)
        ff('-i', CAMP / f'assets/sufg-{e}-v1.png', '-vf', 'scale=900:-1', '-quality', '86', A / f'sufg-{e}.webp')
    C = CAMP / 'clips'
    # 02: one continuous 30fps segment, cropped to the masked window (620×827 at 230,470 on screen)
    parts, chain = [], []
    ins = [C / 'drop-noir.mp4'] + [C / f'{n}.mp4' for n, _, _ in WHIPS] + [C / 'whip-pistache-vanille.mp4']
    chain.append(f'[0:v]trim={DROP[0]}:{DROP[1]},setpts=PTS-STARTPTS[s0]')
    for i, (_, a, b) in enumerate(WHIPS, 1):
        chain.append(f'[{i}:v]trim={a}:{b},setpts=(PTS-STARTPTS)/{WHIP_SPEED}[s{i}]')
    chain.append(f'[4:v]trim={VAN_HOLD[0]}:{VAN_HOLD[1]},setpts=PTS-STARTPTS[s4]')
    chain.append('[s0][s1][s2][s3][s4]concat=n=5:v=1:a=0,fps=30,crop=620:827:230:640[v]')
    (A / 'lum').mkdir()
    args = []
    for f in ins: args += ['-i', f]
    ff(*args, '-filter_complex', ';'.join(chain), '-map', '[v]', *SEQ_OUT, A / 'lum/f%03d.webp')
    # 03 and 04: full frame, 24fps (native)
    # (as VP9 <video>: Playwright's Chromium has no H.264; render.js seeks them frame by frame)
    vp9 = ['-an', '-c:v', 'libvpx-vp9', '-crf', '18', '-b:v', '0', '-g', '12', '-row-mt', '1', '-deadline', 'good', '-cpu-used', '2']
    ff('-i', C / 'filling.mp4', '-t', '3.7', *vp9, A / 'coeur.webm')
    ff('-ss', '1.2', '-i', C / 'coffret-open.mp4', '-t', '3.8', *vp9, A / 'boite.webm')
    return {'lum': len(list((A / 'lum').glob('*.webp')))}

# ── html ──────────────────────────────────────────────────────────────────────────────
def build_html(n):
    h = (HERE / 'src/reel-v1.html').read_text(encoding='utf-8')
    def sub(old, new, count=1):
        nonlocal h
        assert h.count(old) == count, (old[:70], h.count(old))
        h = h.replace(old, new)
    def resub(pat, new):
        nonlocal h
        h, k = re.subn(pat, lambda m: new, h, flags=re.S); assert k == 1, pat

    # 02 · the stills window -> the clip, same window and the same soft oval mask
    resub(r'<div style="position: absolute; left: 230px; top: 470px;[^\n]*\n',
          '<div style="position: absolute; left: 230px; top: 470px; width: 620px; height: 827px; '
          '-webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 58%, transparent 100%); '
          'mask-image: radial-gradient(ellipse 50% 50% at 50% 50%, #000 58%, transparent 100%)">'
          f'<div class="stack" data-seq="a/lum/f%03d.webp" data-from="1" data-to="{n["lum"]}" data-start="{SEQ_B}" '
          'data-step="0.0333"></div></div>\n')
    for old, (a, b) in zip(['10.95,11.77', '12.12,12.94', '13.29,14.11', '14.46,15.30'], labels):
        sub(f'data-show="{old}" data-fade="0.15"', f'data-show="{a:.2f},{b:.2f}" data-fade="{FADE}"')
    # the closing line comes in after the last name has gone
    sub('@keyframes bpay{0%,52.167%{opacity:0;transform:translateY(40px)}53.833%,56.667%{opacity:1;transform:none}',
        f'@keyframes bpay{{0%,{P(15.75)}{{opacity:0;transform:translateY(40px)}}{P(16.3)},56.667%{{opacity:1;transform:none}}')
    # candles: two per edition, at the moment its name appears; the ball reaches each candle as it lights
    fl = ''.join(f'.fl{k}{{animation-name:fl{k}}}@keyframes fl{k}{{0%,{P(T - .17)}{{opacity:0;transform:scale(0)}}'
                 f'{P(T)}{{opacity:1;transform:scale(1.3)}}{P(T + .2)},100%{{opacity:1;transform:scale(1)}}}}'
                 for k, T in enumerate(CANDLES))
    resub(r'\.fl0\{animation-name:fl0\}.*?\n', fl + '\n')
    off = [(960 - x) / 754 * 100 for x in CANDLE_X]
    ball = f'0%,{P(10.2)}{{offset-distance:0%;opacity:1}}' + ''.join(
        f'{P(T - .05)}{{offset-distance:{o:.1f}%;opacity:1}}' for T, o in zip(CANDLES, off)) + \
        f'{P(CANDLES[-1] + .4)},100%{{offset-distance:100%;opacity:0}}'
    resub(r'@keyframes bball\{[^\n]*\n', f'@keyframes bball{{{ball}}}\n')
    roll = f'0%,{P(10.2)}{{transform:rotate(0)}}' + ''.join(
        f'{P(T - .05)}{{transform:rotate({-7.2 * o:.0f}deg)}}' for T, o in zip(CANDLES, off)) + '100%{transform:rotate(-720deg)}'
    resub(r'@keyframes broll\{[^\n]*?deg\)\}\}', f'@keyframes broll{{{roll}}}')
    glow = f'0%,{P(CANDLES[0])}{{opacity:0}}' + ''.join(
        f'{P(T + .3)}{{opacity:{(k + 1) * .1125:.3f}}}' for k, T in enumerate(CANDLES)) + '100%{opacity:.9}'
    resub(r'@keyframes bglow\{[^\n]*?\}\}', f'@keyframes bglow{{{glow}}}')

    # 03 · the filling, moving
    sub('<img class="cover c-push" src="a/sufg-filling.webp" alt="Vanilla cream piped straight into a sufganiya" style="object-position: 44% 50%">',
        '<video class="cover c-push" src="a/coeur.webm" data-vstart="16.8" muted playsinline preload="auto"></video>')

    # 04 · the real coffret opening; the lid already carries the signature
    grad = ('<div style="position: absolute; left: 0; right: 0; top: 0; height: 520px; background: linear-gradient(to bottom, rgba(18,14,8,.9) 45%, rgba(18,14,8,0))"></div>'
            '<div style="position: absolute; left: 0; right: 0; bottom: 0; height: 300px; background: linear-gradient(to top, rgba(18,14,8,.95) 40%, rgba(18,14,8,0))"></div>')
    sub('<div class="stack" style="background: radial-gradient(ellipse 80% 50% at 50% 55%, #2A2016, #120E08 75%)"></div>',
        '<div class="stack" style="background: #120E08"></div>'
        '<video class="cover" src="a/boite.webm" data-vstart="20.0" muted playsinline preload="auto"></video>' + grad)
    resub(r'\n    <div style="position: absolute; left: 160px; top: 560px;.*?Signé, ce soir</div>\n    </div>', '')
    sub('data-in="22.6" style="position: absolute; top: 1600px;', 'data-in="22.6" style="position: absolute; top: 1770px;')
    sub('<title>SIGNÉ Les Lumières reel</title>', '<title>SIGNÉ Les Lumières reel v2</title>')
    (HERE / 'reel-v2.html').write_text(h, encoding='utf-8')

if __name__ == '__main__':
    n = build_assets(); build_html(n)
    print('frames', n, '| land', round(land, 2), '| swaps', [round(s, 2) for s in swaps], '| seq ends', round(seq_b_end, 2))
    print('labels', [(round(a, 2), round(b, 2)) for a, b in labels]); print('candles', [round(c, 2) for c in CANDLES])
