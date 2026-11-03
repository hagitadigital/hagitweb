# Replace the plinth region (below Y0) of every frame with a static plinth from the
# first/last frame, crossfaded around the clip midpoint, to remove spin flashes.
import subprocess, sys, numpy as np
src, dst = sys.argv[1], sys.argv[2]
W, H, Y0, FEATHER = 1080, 1920, 1335, 24
raw = subprocess.run(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
a = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)
n = len(a); first, last = a[0].copy(), a[-1].copy()
mask = np.zeros((H, 1, 1), np.float32)
mask[Y0:] = 1.0
mask[Y0-FEATHER:Y0, 0, 0] = np.linspace(0, 1, FEATHER)
mid, span = n * 0.45, n * 0.12
out = np.empty_like(a)
for i in range(n):
    t = np.clip((i - (mid - span)) / (2 * span), 0, 1)
    plinth = first * (1 - t) + last * t
    out[i] = a[i] * (1 - mask) + plinth * mask
p = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-',
                      '-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p',dst], stdin=subprocess.PIPE)
p.stdin.write(out.clip(0,255).astype(np.uint8).tobytes()); p.stdin.close(); p.wait()
