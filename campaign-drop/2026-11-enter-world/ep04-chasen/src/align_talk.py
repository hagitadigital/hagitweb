# Finds the similarity transform (scale + shift) that maps a lip-sync clip's frames onto the original still,
# using ORB features on the static background (left of the person). Prints JSON {s, tx, ty} in 1080x1920 px:
# still_xy = s * clip_xy + (tx, ty).   usage: python3 align_talk.py <still.webp> <frame.jpg>
import sys, json, os, glob, cv2, numpy as np
def fit(ga, gb, orb, ka, da):
    kb, db = orb.detectAndCompute(gb, None)
    m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(db, da), key=lambda x: x.distance)[:800]
    src = np.float32([kb[x.queryIdx].pt for x in m]); dst = np.float32([ka[x.trainIdx].pt for x in m])
    return cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.0)
if len(sys.argv) > 3 and sys.argv[2] == '--dir':
    a = cv2.resize(cv2.imread(sys.argv[1]), (1080, 1920)); ga = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(ga); mask[:, :470] = 255; mask[:330, :] = 255          # static background only
    orb = cv2.ORB_create(6000); ka, da = orb.detectAndCompute(ga, mask)
    fs = sorted(glob.glob(os.path.join(sys.argv[3], 'f_*.jpg'))); Ms = []
    for f in fs:
        gb = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY); M, _ = fit(ga, gb, orb, ka, da); Ms.append(M)
    Ms = np.array(Ms); k = 7; P = np.pad(Ms, ((k, k), (0, 0), (0, 0)), mode='edge')
    Sm = np.array([P[i:i + 2 * k + 1].mean(0) for i in range(len(Ms))])           # smooth jitter
    for f, M in zip(fs, Sm):
        b = cv2.imread(f); w = cv2.warpAffine(b, M, (1080, 1920), borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
        cov = cv2.warpAffine(np.full((1920, 1080), 255, np.uint8), M, (1080, 1920)); cov = cv2.erode(cov, np.ones((9, 9), np.uint8))
        w[cov == 0] = a[cov == 0]; cv2.imwrite(f, w, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(json.dumps({'frames': len(fs), 's_first': round(float(np.hypot(*Sm[0][:, 0])), 4), 's_last': round(float(np.hypot(*Sm[-1][:, 0])), 4),
                      'tx': [round(float(Sm[0][0, 2]), 1), round(float(Sm[-1][0, 2]), 1)], 'ty': [round(float(Sm[0][1, 2]), 1), round(float(Sm[-1][1, 2]), 1)]}))
    sys.exit()
a = cv2.resize(cv2.imread(sys.argv[1]), (1080, 1920)); b = cv2.imread(sys.argv[2])
ga, gb = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(b, cv2.COLOR_BGR2GRAY)
orb = cv2.ORB_create(6000)
ka, da = orb.detectAndCompute(ga, None); kb, db = orb.detectAndCompute(gb, None)
m = sorted(cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(db, da), key=lambda x: x.distance)[:800]
src = np.float32([kb[x.queryIdx].pt for x in m]); dst = np.float32([ka[x.trainIdx].pt for x in m])
M, inl = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=2.0)
s = float(np.hypot(M[0, 0], M[1, 0]))
w = cv2.warpAffine(b, M, (1080, 1920))
err = float(np.abs(w[:, :480].astype(int) - a[:, :480].astype(int)).mean())
print(json.dumps({'s': round(s, 5), 'rot': round(float(np.degrees(np.arctan2(M[1, 0], M[0, 0]))), 3), 'tx': round(float(M[0, 2]), 2), 'ty': round(float(M[1, 2]), 2), 'inliers': int(inl.sum()), 'board_err': round(err, 1)}))

# usage 2: python3 align_talk.py <still.webp> --dir <frames_dir>
#   warps every frame onto the still (per-frame transform, smoothed), fills the uncovered border from the still, overwrites in place.
