# Lays the recorded site clips (and their chapter chips) over the silent long-cut render, adds the music, writes 9:16 + 4:5.
# Usage: python3 compose-long.py f/silent-long.mp4 ../pardon-me-29-orbit-long
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
silent, out = sys.argv[1], sys.argv[2]
sched = json.load(open(os.path.join(HERE, 'long-overlays.json')))
D = sched['duration']
args, chains, last = ['-i', silent], [], '0:v'
ninp = lambda: args.count('-i')   # index of the next input
for n, o in enumerate(sched['overlays']):
    # optional: 'crop' [w, h, x, y] of the clip and 'at' [x, y] in the frame (a clip inside a post); 'chip' None = the label is in the render
    vi, a, b = ninp(), o['start'], o['start'] + o['dur']
    args += ['-i', os.path.join(HERE, 'media', 'clips', o['clip'] + '.mp4')]
    crop = 'crop=%d:%d:%d:%d,' % tuple(o['crop']) if o.get('crop') else ''
    x, y = o.get('at', [0, 0])
    chain = f"[{vi}:v]{crop}setpts=PTS-STARTPTS+{a}/TB[c{n}];[{last}][c{n}]overlay={x}:{y}:eof_action=pass:enable='between(t,{a},{b - .001})'[v{n}]"
    if o['chip'] is not None:
        ci = ninp()
        args += ['-loop', '1', '-i', os.path.join(HERE, 'f', 'chip-%d.png' % o['chip'])]
        chain = chain[:-len(f'[v{n}]')] + f"[v{n}a];[v{n}a][{ci}:v]overlay=0:0:enable='between(t,{a},{b - .001})'[v{n}]"
    chains.append(chain)
    last = f'v{n}'
music = os.path.join(HERE, 'media', 'arrete-chic-30.m4a')
m = ninp()
args += ['-i', music, '-i', music]
# the 30s track runs into a second pass from 0:06, crossfaded, trimmed to the cut
chains.append(f"[{m + 1}:a]atrim=start=6,asetpts=PTS-STARTPTS[b];[{m}:a][b]acrossfade=d=2.5[x];[x]atrim=0:{D},afade=t=in:d=0.3,afade=t=out:st={D - 1.8}:d=1.8[a]")
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', *args, '-filter_complex', ';'.join(chains), '-map', f'[{last}]', '-map', '[a]',
                '-t', str(D), '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k',
                '-movflags', '+faststart', out + '.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out + '.mp4', '-i', os.path.join(HERE, 'f', 'frame-4x5.png'), '-filter_complex',
                "color=c=0xFAF8F3:s=1080x1350:r=30[bg];[0:v]scale=760:1350:flags=lanczos[v];[bg][v]overlay=160:0:shortest=1[a];[a][1:v]overlay=0:0,format=yuv420p[o]",
                '-map', '[o]', '-map', '0:a', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'copy', '-movflags', '+faststart', out + '-4x5.mp4'], check=True)
print('wrote', out + '.mp4', out + '-4x5.mp4')
