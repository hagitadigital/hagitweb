"""Sound bed for the intro reel: a soft thump on every word, a snap on every card,
a low bell when everything gathers into the ring. Synthesised. Usage: python sound.py out.wav"""
import sys, wave
import numpy as np

SR, DUR = 48000, 15.4
n = int(SR * DUR)
out = np.zeros(n)

def add(sig, t):
    i = int(round(t * SR)); m = min(len(sig), n - i)
    if i >= 0 and m > 0: out[i:i + m] += sig[:m]

def thump(f=95):
    t = np.arange(int(0.22 * SR)) / SR
    return np.sin(2 * np.pi * (f + 90 * np.exp(-t * 40)) * t) * np.exp(-t * 22) * 0.5

def snap(f):
    t = np.arange(int(0.12 * SR)) / SR
    click = np.random.default_rng(3).standard_normal(len(t)) * np.exp(-t * 700) * 0.3
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 55) + click) * 0.26

def bell(f, amp, decay):
    t = np.arange(int(2.8 * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * decay * d)
            for r, a, d in ((1, 1, 1), (2.76, .4, 1.6), (5.4, .16, 2.4)))
    return s * amp * np.minimum(1, t / 0.004)

for t in (0.02, 1.0, 1.22, 2.1, 2.5, 2.9, 3.6, 3.9): add(thump(), t)          # words
for k in range(7): add(snap(520 + 50 * k), 5.0 + k * 1.0 + 0.38)                # cards
add(bell(1318.5, 0.09, 3.0), 4.4)                                              # the signature under the logo
for f, a in ((220.0, 0.22), (329.6, 0.16), (659.3, 0.10)): add(bell(f, a, 1.5), 12.8)   # the whole world

out = np.tanh(out * 1.1) * 0.8
pcm = (np.stack([out, out], 1) * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
