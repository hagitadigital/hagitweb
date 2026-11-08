#!/usr/bin/env python3
# EP03 audio + config from separate recordings. Same formulas as the TIMING block in ep03.html.
#   python3 src/mux.py config | audio | mux <silent.mp4> <out.mp4>
import sys, os, subprocess, json
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, '..'); V = os.path.join(root, 'voice')
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout) if os.path.exists(p) else 0.0
f = {k: os.path.join(V, k + '.wav') for k in ['hook', 'studio', 'world', 'biz', 'ask-q']}
HK, SD, WD, BZ, QD = (dur(f[k]) for k in ['hook', 'studio', 'world', 'biz', 'ask-q'])
A = HK + 0.6 if HK else 0.0; B = A + SD + 2.6; W_END = B + WD + 0.2; TO_S6 = W_END + 0.7; BIZ_T = TO_S6 + 0.3
QT = BIZ_T + (BZ + 0.4 if BZ else 0); SIG = QT + QD + 0.35; DUR = SIG + 3.6
ms = lambda x: int(round(x * 1000)); cmd = sys.argv[1]
if cmd == 'config':
    def n(d): p = os.path.join(here, '_build', 'talk-' + d); return len(os.listdir(p)) if os.path.isdir(p) else 0
    open(os.path.join(here, 'config.js'), 'w').write(f"// written by src/mux.py\nwindow.HK = {HK:.3f}; window.SD = {SD:.3f}; window.WD = {WD:.3f}; window.BZ = {BZ:.3f}; window.QD = {QD:.3f}; window.HK_N = {n('hook')}; window.Q_N = {n('ask')};\n")
    print(json.dumps({'DUR': round(DUR, 2), 'A': A, 'B': round(B, 2), 'BIZ_T': round(BIZ_T, 2), 'QT': round(QT, 2)}))
elif cmd == 'audio':   # S6 lip-sync inputs: _hook = hook, _ask = biz + 0.4s + question
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f['biz'], '-i', f['ask-q'], '-filter_complex',
                    '[0:a]aresample=44100,aformat=channel_layouts=mono[b];anullsrc=r=44100:cl=mono,atrim=0:0.4[s];[1:a]aresample=44100,aformat=channel_layouts=mono[q];[b][s][q]concat=n=3:v=0:a=1[o]',
                    '-map', '[o]', '-b:a', '192k', os.path.join(V, '_ask.mp3')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f['hook'], '-b:a', '192k', os.path.join(V, '_hook.mp3')], check=True)
    print('ask', round(dur(os.path.join(V, '_ask.mp3')), 2), 'hook', HK)
elif cmd == 'mux':
    silent, out = sys.argv[2], sys.argv[3]
    parts = [(f['hook'], 0.0), (f['studio'], A), (f['world'], B), (f['biz'], BIZ_T), (f['ask-q'], QT)]
    parts = [(p, t) for p, t in parts if os.path.exists(p)]
    ins = ['-i', silent, '-stream_loop', '-1', '-i', os.path.join(root, '..', 'ep01-elvea', 'voice', 'bed-piano-strings-v1.mp3'), '-f', 'lavfi', '-t', '0.9', '-i', 'anoisesrc=color=pink:amplitude=0.6:r=44100']
    fc = ''; labs = []
    for i, (p, t) in enumerate(parts):
        ins += ['-i', p]; fc += f"[{3 + i}:a]aresample=44100,aformat=channel_layouts=mono,adelay={ms(t)}[v{i}];"; labs.append(f'[v{i}]')
    fc += (f"{''.join(labs)}amix=inputs={len(labs)}:normalize=0,aformat=channel_layouts=stereo[vo];"
           f"[2:a]bandpass=f=1800:w=1600,afade=t=in:d=0.45,afade=t=out:st=0.45:d=0.45,volume=0.22,asplit=2[w1][w2];"
           f"[w1]adelay={ms(A + 11.75)}|{ms(A + 11.75)}[wa];[w2]adelay={ms(W_END - 0.1)}|{ms(W_END - 0.1)}[wb];"
           f"[1:a]atrim=0:{DUR:.2f},afade=t=in:d=1.0,afade=t=out:st={DUR - 2.5:.2f}:d=2.5,volume=0.16[mus];"
           f"[vo]asplit=2[vo1][sc];[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
           f"[vo1][duck][wa][wb]amix=inputs=4:normalize=0,alimiter=limit=0.95[aout]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', f'{DUR:.2f}', '-movflags', '+faststart', out], check=True)
    print('muxed', out, round(DUR, 2))
