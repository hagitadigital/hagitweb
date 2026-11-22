"""Sound bed for the pendulum loop: a soft tick on every pass through the centre, a small bell on
every swap, a lower bell when the hour changes. Synthesised, loops seamlessly. Usage: python sound.py out.wav"""
import sys, wave
import numpy as np

SR, DUR, HALF, T0 = 48000, 10.0, 1.25, 0.3
n = int(SR * DUR)
out = np.zeros(n)

def add(sig, t):
    i = int(round(t * SR)) % n
    idx = (i + np.arange(len(sig))) % n      # tails wrap around, so the loop has no seam
    np.add.at(out, idx, sig)

def tick(f):
    t = np.arange(int(0.09 * SR)) / SR
    body = np.sin(2 * np.pi * f * t) * np.exp(-t * 70)
    click = np.random.default_rng(7).standard_normal(len(t)) * np.exp(-t * 900) * 0.35
    return (body + click) * 0.30

def bell(f, amp, decay):
    t = np.arange(int(2.2 * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * decay * d)
            for r, a, d in ((1, 1, 1), (2.76, .45, 1.6), (5.4, .2, 2.4), (8.9, .08, 3.2)))
    return s * amp * np.minimum(1, t / 0.004)

NOTES = [1318.5, 1568.0, 1318.5, 1760.0, 1318.5, 1568.0, 1318.5, 1975.5]   # E6 G6 E6 A6 E6 G6 E6 B6
for k in range(8):
    add(tick(820 if k % 2 == 0 else 640), (k + 0.5) * HALF - T0)            # centre of each pass
    apex = k * HALF - T0                                                     # piece k arrives
    add(bell(NOTES[k], 0.16, 4.5), apex)
    if k % 2 == 0:                                                           # the hour changes
        add(bell(329.6, 0.20, 2.2), apex)

out = np.tanh(out * 1.1) * 0.8
pcm = (np.stack([out, out], 1) * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
