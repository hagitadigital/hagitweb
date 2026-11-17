"""Soft ambient bed: warm pad chords + sparse bell notes. Usage: music.py out.wav seconds"""
import sys
import numpy as np
import soundfile as sf

out, dur = sys.argv[1], float(sys.argv[2])
sr = 44100
n = int(sr * dur)
t = np.arange(n) / sr
L = np.zeros(n)
R = np.zeros(n)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


# Fmaj7 - Am7 - Dm9 - Cmaj7 (midi notes), 6 s per chord
chords = [
    [41, 53, 57, 60, 64],
    [45, 52, 57, 60, 67],
    [38, 50, 57, 60, 64],
    [36, 52, 55, 59, 64],
]
bar = 6.0
rng = np.random.default_rng(7)

for i in range(int(dur / bar) + 2):
    ch = chords[i % 4]
    t0 = i * bar - 1.0
    seg = (t >= t0) & (t < t0 + bar + 2.5)
    x = t[seg] - t0
    env = np.clip(x / 2.2, 0, 1) * np.clip((bar + 2.5 - x) / 2.5, 0, 1)
    env = env ** 1.5
    for j, m in enumerate(ch):
        f = hz(m)
        amp = 0.16 if j == 0 else 0.09
        det = 1.0 + 0.0025 * (j - 2)
        trem = 1 + 0.08 * np.sin(2 * np.pi * (0.11 + 0.03 * j) * x + j)
        w = np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * f * 2 * x * det) + 0.12 * np.sin(2 * np.pi * f * 3 * x)
        w2 = np.sin(2 * np.pi * f * det * x + 0.7)
        pan = 0.5 + 0.3 * np.sin(j * 1.7)
        L[seg] += amp * env * trem * (w * (1 - pan) + 0.4 * w2)
        R[seg] += amp * env * trem * (w * pan + 0.4 * w2)
    # sparse bell notes from the chord, an octave up
    for k in range(3):
        m = ch[1 + (k * 2 + i) % 4] + 12
        st = i * bar + 0.8 + k * 1.9 + rng.uniform(-0.1, 0.1)
        s0 = int(st * sr)
        if s0 < 0 or s0 >= n:
            continue
        ln = min(n - s0, int(sr * 3.5))
        x = np.arange(ln) / sr
        f = hz(m)
        e = np.exp(-x * 1.6) * np.clip(x / 0.012, 0, 1)
        w = np.sin(2 * np.pi * f * x) + 0.3 * np.sin(2 * np.pi * f * 2.01 * x) * np.exp(-x * 3)
        pan = 0.3 + 0.4 * ((k + i) % 2)
        L[s0:s0 + ln] += 0.11 * e * w * (1 - pan)
        R[s0:s0 + ln] += 0.11 * e * w * pan

st = np.stack([L, R], axis=1)
# simple echo for space
d = int(sr * 0.37)
st[d:] += 0.28 * st[:-d]
d2 = int(sr * 0.61)
st[d2:] += 0.16 * st[:-d2][:, ::-1]
st /= np.max(np.abs(st)) * 1.15
fade = np.clip(t / 1.2, 0, 1) * np.clip((dur - t) / 2.0, 0, 1)
st *= fade[:, None]
sf.write(out, st, sr)
