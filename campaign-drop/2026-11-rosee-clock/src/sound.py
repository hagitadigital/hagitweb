"""Sound bed for the dawn-clock loop: a soft tick when the hand lands on a product, a glassy drop
and a small bell when the dew wakes it. Synthesised, loops seamlessly. Usage: python sound.py out.wav"""
import sys, wave
import numpy as np

SR, STEP, T0, N = 48000, 2.0, 0.55, 5
n = int(SR * STEP * N)
out = np.zeros(n)

def add(sig, t):
    i = int(round(t * SR)) % n
    np.add.at(out, (i + np.arange(len(sig))) % n, sig)      # tails wrap, so the loop has no seam

def tick(f):
    t = np.arange(int(0.09 * SR)) / SR
    click = np.random.default_rng(7).standard_normal(len(t)) * np.exp(-t * 900) * 0.35
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 70) + click) * 0.28

def drop():
    t = np.arange(int(0.22 * SR)) / SR
    f = 900 + 1500 * np.exp(-t * 30)                          # quick downward chirp, like a water drop
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 26) * 0.22

def bell(f, amp, decay):
    t = np.arange(int(2.4 * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * decay * d)
            for r, a, d in ((1, 1, 1), (2.76, .4, 1.6), (5.4, .16, 2.4)))
    return s * amp * np.minimum(1, t / 0.004)

NOTES = [1046.5, 1174.7, 1318.5, 1568.0, 880.0]              # C6 D6 E6 G6, then A5 for the night
for k in range(N):
    arrive = k * STEP - T0
    add(tick(760), arrive)
    add(drop(), arrive + 0.06)
    add(bell(NOTES[k], 0.17, 3.6), arrive + 0.24)

out = np.tanh(out * 1.1) * 0.8
pcm = (np.stack([out, out], 1) * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
