# ORÉVA° Backstage reel — the soundtrack, synthesised here (no licensed audio).
# A quiet pad under the whole reel, a message chime when something comes in, a soft "sent" when it is answered,
# ticks for the clock and the counter. The music drops during "כאן המערכת שותקת".
# Run: python3 sound.py → sound.wav (48 kHz stereo, 30.0 s). Times match gen.py.
import os, wave
import numpy as np

SR, DUR = 48000, 30.0
N = int(SR * DUR)
rng = np.random.default_rng(24)
L = np.zeros(N); R = np.zeros(N)

def at(t): return int(t * SR)
def add(sig, t, gain=1.0, pan=0.0):
    i = at(t); j = min(N, i + len(sig))
    if i >= N: return
    s = sig[:j - i] * gain
    L[i:j] += s * (1 - max(0, pan)); R[i:j] += s * (1 + min(0, pan))
def tt(d): return np.arange(int(d * SR)) / SR
def lowpass(x, cut):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / np.sqrt(1 + (f / cut) ** 4); return np.fft.irfft(X, len(x))

# ── sound effects ────────────────────────────────────────────────────
def bell(freq, d=0.9, decay=5.0):
    t = tt(d); e = np.exp(-decay * t) * np.minimum(1, t / 0.004)
    return e * (np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 2.01 * t) * np.exp(-4 * t) + .12 * np.sin(2 * np.pi * freq * 3.98 * t) * np.exp(-9 * t))
def incoming(t, g=.30):                      # a message arrives: two glassy notes, up a fourth
    add(bell(1318.5, .8, 6), t, g, -.1); add(bell(1760.0, 1.0, 5), t + .085, g * .9, .1)
def sent(t, g=.22):                          # a reply goes out: a soft upward swoop and a light note
    d = .16; x = tt(d); f = 520 + 620 * (x / d) ** 1.6
    sw = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * x / d) ** 2
    add(sw, t, g * .7); add(bell(1567.98, .6, 7), t + .11, g * .8, .05)
def tick(t, g=.10):
    x = tt(.012); add(lowpass(rng.standard_normal(len(x)), 5000) * np.exp(-x * 380), t, g)
def tap(t, g=.18):                           # a soft UI tap
    x = tt(.06); add(np.sin(2 * np.pi * 300 * x) * np.exp(-x * 70) + .3 * lowpass(rng.standard_normal(len(x)), 2500) * np.exp(-x * 200), t, g)
def thud(t, g=.22):                          # "still no answer"
    x = tt(.5); add(np.sin(2 * np.pi * 98 * x) * np.exp(-x * 7) * np.minimum(1, x / .01), t, g)
def whoosh(t, d=.6, g=.10):
    x = tt(d); n = lowpass(rng.standard_normal(len(x)), 1800); env = np.sin(np.pi * x / d) ** 2
    add(n * env, t, g, -.2); add(lowpass(rng.standard_normal(len(x)), 1500) * env, t, g, .2)
def chime(t, g=.16, root=880.0):
    for k, r in enumerate([1, 1.25, 1.5]): add(bell(root * r, 1.6, 2.6), t + k * .07, g, (k - 1) * .25)
def shimmer(t, g=.07):
    for k, fr in enumerate([2093, 2637, 3136, 2349, 2794]): add(bell(fr, 1.2, 3.5), t + k * .09, g, (-1) ** k * .3)

# hook — the lead comes in, nobody answers
incoming(.15, .34)
for t in (.95, 1.45, 1.95): tick(t, .12)
thud(1.0)
# studio window, then full screen
whoosh(2.55, .7, .09); whoosh(5.3, .5, .07)
# the form: chips, typing, the button, the lead arrives and is answered
tap(6.2); tap(7.3)
for t in (8.0, 8.09, 8.18, 8.27): tick(t, .08)
tap(8.5, .22)
incoming(8.95, .26); sent(9.3)
# Or Éva's clock: her question at night is answered; each turn of the ring; the messages that go out
incoming(9.85, .24); sent(10.25)
for t in (10.95, 12.25, 13.85, 15.0): whoosh(t, .45, .06)
sent(11.45); sent(14.35); sent(15.5)
# the board: Noa moves to "לקוחה קבועה"
whoosh(16.85, .6, .07); chime(17.5, .13)
# the dashboard: rows, the counter, 61%
tap(19.95, .12); tap(20.35, .12); tap(20.7, .12)
for t in (20.9, 21.2, 21.5, 21.8): tick(t, .09)
chime(21.85, .08, 1318.5)
# the promise and the outro
shimmer(24.6); whoosh(27.0, .7, .07); chime(28.2, .10, 659.25)

# ── music: a slow, quiet pad, four chords of 4 s, a few soft bell notes on top ──
def hz(m): return 440 * 2 ** ((m - 69) / 12)
CH = [[53, 57, 60, 64], [50, 53, 57, 60, 64], [46, 50, 53, 57], [48, 55, 62, 64]]   # Fmaj7 · Dm9 · Bbmaj7 · Cadd9
pad = np.zeros(N)
seg = 4.0
for c in range(int(DUR / seg) + 1):
    t0 = c * seg - .6; d = seg + 1.8; x = tt(d)
    env = np.minimum(1, x / 1.2) * np.minimum(1, (d - x) / 1.4).clip(0)
    v = np.zeros(len(x))
    for m in CH[c % 4]:
        f = hz(m)
        for det in (-.0015, .0015):
            v += np.sin(2 * np.pi * f * (1 + det) * x + rng.uniform(0, 6)) + .25 * np.sin(2 * np.pi * 2 * f * (1 + det) * x)
    i = max(0, at(t0)); seg_sig = (v * env)[max(0, -at(t0)):]
    j = min(N, i + len(seg_sig)); pad[i:j] += seg_sig[:j - i]
pad = lowpass(pad, 1400)
pad /= np.abs(pad).max()
notes = np.zeros(N)
ARP = [72, 76, 79, 77, 74, 72, 77, 81, 70, 74, 77, 79, 72, 79, 76, 74]
for k in range(int(DUR / 1.0)):
    m = ARP[k % len(ARP)]; b = bell(hz(m), 1.4, 3.2); i = at(k * 1.0 + .5); j = min(N, i + len(b)); notes[i:j] += b[:j - i]
music = pad * .55 + lowpass(notes, 3000) * .18
# level over time: low under the hook, up with the studio window, down for the silence, fade at the end
g = np.interp(np.arange(N) / SR,
              [0, 2.4, 3.2, 12.55, 12.9, 13.7, 14.2, 28.8, 30.0],
              [.35, .35, 1.0, 1.0, .22, .22, 1.0, 1.0, .55])
music *= g * .30
L += music; R += music

# ── master ───────────────────────────────────────────────────────────
mix = np.stack([L, R], 1)
mix /= max(1.0, np.abs(mix).max() / .89)
fade = np.minimum(1, np.arange(N) / (SR * .02)); mix *= fade[:, None]
pcm = (mix * 32767).astype('<i2')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound.wav')
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('wrote', out, 'peak', round(float(np.abs(mix).max()), 3))
