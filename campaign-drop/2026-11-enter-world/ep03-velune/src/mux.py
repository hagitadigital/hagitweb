#!/usr/bin/env python3
# EP03 audio + config. Same timeline formulas as the TIMING block in ep03.html — keep them in step.
#   python3 src/mux.py config            → measures voice/hook.wav and voice/biz.wav (if present), writes src/config.js
#   python3 src/mux.py audio             → writes voice/_ask.wav (biz + pause + question) for the S6 lip-sync clip, and voice/_hook.wav
#   python3 src/mux.py mux <silent.mp4> <out.mp4>
import sys, os, subprocess, json
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.join(here, '..'); V = os.path.join(root, 'voice')
def dur(p): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)
vo = os.path.join(V, 'ep03-vo-cartesia.wav'); hook = os.path.join(V, 'hook.wav'); biz = os.path.join(V, 'biz.wav')
HK = dur(hook) if os.path.exists(hook) else 0.0; BZ = dur(biz) if os.path.exists(biz) else 0.0
A = HK + 0.6 if HK else 0.0; B = A + 2.2; W_END = B + 35.6; TO_S6 = W_END + 0.7; BIZ_T = TO_S6 + 0.3
Q = BIZ_T + (BZ + 0.4 if BZ else 0) - 35.75; SIG = Q + 43.44 + 0.3; DUR = SIG + 3.6
cmd = sys.argv[1]
if cmd == 'config':
    def n(d): p = os.path.join(here, '_build', 'talk-' + d); return len(os.listdir(p)) if os.path.isdir(p) else 0
    open(os.path.join(here, 'config.js'), 'w').write(f"// written by src/mux.py — recording lengths (s) and talking-clip frame counts\nwindow.HK = {HK:.3f}; window.BZ = {BZ:.3f}; window.HK_N = {n('hook')}; window.Q_N = {n('ask')};\n")
    print(json.dumps({'HK': HK, 'BZ': BZ, 'DUR': round(DUR, 2), 'BIZ_T': round(BIZ_T, 2)}))
elif cmd == 'audio':
    parts = []
    if BZ: parts += ['-i', biz]
    fc = (f"[0:a]anull[b];anullsrc=r=44100:cl=mono,atrim=0:0.4[s];" if BZ else "") + f"[{1 if BZ else 0}:a]atrim=35.75,asetpts=PTS-STARTPTS[q];"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *parts, '-i', vo, '-filter_complex', fc + (f"[b][s][q]concat=n=3:v=0:a=1[o]" if BZ else "[q]anull[o]"), '-map', '[o]', '-ar', '44100', '-ac', '1', os.path.join(V, '_ask.wav')], check=True)
    print('ask', round(dur(os.path.join(V, '_ask.wav')), 2))
elif cmd == 'mux':
    silent, out = sys.argv[2], sys.argv[3]; ms = lambda x: int(round(x * 1000))
    ins = ['-i', silent, '-i', vo, '-stream_loop', '-1', '-i', os.path.join(root, '..', 'ep01-elvea', 'voice', 'bed-piano-strings-v1.mp3'), '-f', 'lavfi', '-t', '0.9', '-i', 'anoisesrc=color=pink:amplitude=0.6:r=44100']
    fc = (f"[1:a]asplit=3[a][b][c];[a]atrim=0:12.2,asetpts=PTS-STARTPTS,adelay={ms(A)}|{ms(A)}[v1];"
          f"[b]atrim=12.2:35.75,asetpts=PTS-STARTPTS,adelay={ms(B + 12.2)}|{ms(B + 12.2)}[v2];[c]atrim=35.75,asetpts=PTS-STARTPTS,adelay={ms(Q + 35.75)}|{ms(Q + 35.75)}[v3];")
    vos = ['[v1]', '[v2]', '[v3]']; k = 4
    if HK: ins += ['-i', hook]; fc += f"[{k}:a]anull[vh];"; vos.append('[vh]'); k += 1
    if BZ: ins += ['-i', biz]; fc += f"[{k}:a]adelay={ms(BIZ_T)}|{ms(BIZ_T)}[vb];"; vos.append('[vb]'); k += 1
    fc += (f"{''.join(vos)}amix=inputs={len(vos)}:normalize=0,aformat=channel_layouts=stereo[vo];"
           f"[3:a]bandpass=f=1800:w=1600,afade=t=in:d=0.45,afade=t=out:st=0.45:d=0.45,volume=0.22,asplit=2[w1][w2];"
           f"[w1]adelay={ms(A + 12.0)}|{ms(A + 12.0)}[wa];[w2]adelay={ms(W_END - 0.1)}|{ms(W_END - 0.1)}[wb];"
           f"[2:a]atrim=0:{DUR:.2f},afade=t=in:d=1.0,afade=t=out:st={DUR - 2.5:.2f}:d=2.5,volume=0.16[mus];"
           f"[vo]asplit=2[vo1][sc];[mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
           f"[vo1][duck][wa][wb]amix=inputs=4:normalize=0,alimiter=limit=0.95[aout]")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *ins, '-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-t', f'{DUR:.2f}', '-movflags', '+faststart', out], check=True)
    print('muxed', out, round(DUR, 2))
