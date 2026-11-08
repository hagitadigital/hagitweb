# Align sentences of the script to the pauses of a recording (no ASR): speech chunks between pauses,
# DP chooses sentence boundaries at pauses so each sentence's length best matches its syllable count.
import sys, subprocess, re, json, numpy as np
wav = sys.argv[1]
S = [l.split('|') for l in open(sys.argv[2]).read().strip().split('\n')]   # "syllables|caption text"
out = subprocess.run(['ffmpeg','-hide_banner','-i',wav,'-af','silencedetect=noise=-32dB:d=0.07','-f','null','-'],capture_output=True,text=True).stderr
st = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]; en = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',wav],capture_output=True,text=True).stdout)
gaps = [(s, e) for s, e in zip(st, en) if s > 0.05 and e < dur - 0.02]
start = en[0] if st and st[0] < 0.05 else 0.0
# candidate boundaries = pauses; weight = pause length
B = [(s, e, e - s) for s, e in gaps]
syl = np.array([float(x[0]) for x in S]); n = len(S); m = len(B)
total_speech = (B[-1][0] if False else dur) - start
rate = syl.sum() / (dur - start - sum(b[2] for b in B) * 0.6)
INF = 1e9
# dp[i][j]: first i sentences end at boundary j (j = -1 means start)
dp = np.full((n + 1, m + 1), INF); arg = np.zeros((n + 1, m + 1), int); dp[0][0] = 0
pos = [start] + [b[1] for b in B]          # sentence start positions (after pause j-1)
endp = [b[0] for b in B] + [dur]           # sentence end positions (at pause j)
for i in range(1, n + 1):
    for j in range(1, m + 2):
        if j > m and i < n: continue
        e = endp[j - 1]
        for k in range(0, j):
            if dp[i - 1][k] >= INF: continue
            s0 = pos[k]; d = e - s0; exp = syl[i - 1] / rate
            pen = (d - exp) ** 2 / max(exp, .5) - 0.6 * (B[j - 1][2] if j <= m else .3)
            jj = min(j, m)
            if dp[i - 1][k] + pen < dp[i][jj]: dp[i][jj] = dp[i - 1][k] + pen; arg[i][jj] = k
j = m; seg = []
for i in range(n, 0, -1):
    k = arg[i][j]; seg.append((pos[k], endp[j - 1] if j <= m else dur)); j = k
seg = seg[::-1]
for (a, b), (sy, txt) in zip(seg, S): print(f'{a:6.2f} {b:6.2f}  {sy:>3}  {txt}')
json.dump([[round(a, 2), round(b, 2), t] for (a, b), (_, t) in zip(seg, S)], open(sys.argv[3], 'w'), ensure_ascii=False)
