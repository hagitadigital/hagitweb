"""Sound bed for the build-a-world reel: a soft snap every time an element drops into place,
a low bell when the page turns into the world. Synthesised. Usage: python sound.py out.wav"""
import sys, wave
import numpy as np

SR, DUR = 48000, 12.0
n = int(SR * DUR)
out = np.zeros(n)

def add(sig, t):
    i = int(round(t * SR)); m = min(len(sig), n - i)
    if i >= 0 and m > 0: out[i:i + m] += sig[:m]

def snap(f):
    t = np.arange(int(0.12 * SR)) / SR
    click = np.random.default_rng(3).standard_normal(len(t)) * np.exp(-t * 700) * 0.3
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 55) + click) * 0.26

def bell(f, amp, decay):
    t = np.arange(int(2.6 * SR)) / SR
    s = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * decay * d)
            for r, a, d in ((1, 1, 1), (2.76, .4, 1.6), (5.4, .16, 2.4)))
    return s * amp * np.minimum(1, t / 0.004)

DROPS = [0.32, 1.65, 2.2, 2.7, 3.2, 5.25, 6.15, 7.1, 7.9, 8.65]       # element start + 0.7s
PITCH = [520, 620, 700, 780, 880, 660, 440, 520, 620, 700]
for t, f in zip(DROPS, PITCH): add(snap(f), t)
add(bell(1318.5, 0.10, 3.0), 4.45)                                    # the signature is finished
for f, a in ((220.0, 0.22), (329.6, 0.16), (659.3, 0.10)): add(bell(f, a, 1.6), 9.2)   # the world

out = np.tanh(out * 1.1) * 0.8
pcm = (np.stack([out, out], 1) * 32767).astype('<i2')
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
