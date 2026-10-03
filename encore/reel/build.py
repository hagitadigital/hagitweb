"""Builds the ENCORE° "מחוץ לטבלה" reel: renders scenes, cuts the clips, adds text, crossfades, adds music.
Run from this folder (needs ffmpeg, node + playwright): python3 build.py [out.mp4]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "build")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(B, "encore-outside-the-table.mp4")
X = 0.4  # crossfade seconds
cfg = json.load(open(os.path.join(HERE, "scenes.json")))
os.makedirs(B, exist_ok=True)


def sh(*a):
    subprocess.run(a, check=True)


env = dict(os.environ, NODE_PATH=subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip())
subprocess.run(["node", os.path.join(HERE, "render.cjs"), os.path.join(HERE, "reel.html"), B], check=True, env=env)

enc = ["-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", "30", "-an"]
segs = []
for i, s in enumerate(cfg["scenes"]):
    seg = os.path.join(B, f"seg_{i:02d}.mp4")
    d = str(s["dur"])
    if s["type"] == "graphic":
        sh("ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", os.path.join(B, s["id"], "%04d.png"), *enc, seg)
    else:
        clip = os.path.join(B, s["id"] + ".mp4")
        if not os.path.exists(clip):
            sh("curl", "-sfL", "-o", clip, s["url"])
        fc = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1[v];"
              "[1:v]format=rgba,fade=in:st=0.25:d=0.45:alpha=1[a];"
              f"[2:v]format=rgba,fade=in:st={s.get('b_at', 1.15)}:d=0.45:alpha=1[b];"
              "[v][a]overlay=0:0[x];[x][b]overlay=0:0,format=yuv420p")
        sh("ffmpeg", "-v", "error", "-y", "-ss", str(s.get("ss", 0)), "-t", d, "-i", clip,
           "-loop", "1", "-t", d, "-i", os.path.join(B, s["id"] + "_a.png"),
           "-loop", "1", "-t", d, "-i", os.path.join(B, s["id"] + "_b.png"),
           "-filter_complex", fc, "-t", d, *enc, seg)
    segs.append((seg, s["dur"]))

# crossfade chain
inputs, fc, total, last = [], [], segs[0][1], "0:v"
for seg, _ in segs:
    inputs += ["-i", seg]
for k in range(1, len(segs)):
    off = total - X
    lab = f"v{k}"
    fc.append(f"[{last}][{k}:v]xfade=transition=fade:duration={X}:offset={off:.3f}[{lab}]")
    total = off + segs[k][1]
    last = lab
silent = os.path.join(B, "silent.mp4")
sh("ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", f"[{last}]", *enc, silent)

music = os.path.join(B, "music.mp3")
if not os.path.exists(music):
    sh("curl", "-sfL", "-o", music, cfg["music"])
ms = cfg.get("music_start", 0)
sh("ffmpeg", "-v", "error", "-y", "-i", silent, "-ss", str(ms), "-i", music,
   "-filter_complex", f"[1:a]atrim=0:{total:.2f},afade=t=in:d=0.4,afade=t=out:st={total-2:.2f}:d=2[a]",
   "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT)
print("done", OUT, f"{total:.2f}s")
