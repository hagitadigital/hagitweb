"""Find the laptop's white screen in a frame of the take: four corners (tl,tr,br,bl; may lie outside the frame) and a matte of its visible part."""
import cv2, numpy as np
ASPECT = 1.78   # measured on the frames where the whole screen is in view
def screen(img):
    H, W = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 178) & (hsv[..., 1] < 34)).astype(np.uint8) * 255
    m[:int(H * .60)] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2: return None, None
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    if st[k, cv2.CC_STAT_AREA] < 9000: return None, None
    comp = (lab == k).astype(np.uint8) * 255
    comp = cv2.morphologyEx(comp, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cnt = max(cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea)
    hull = cv2.convexHull(cnt)
    ap = cv2.approxPolyDP(hull, .012 * cv2.arcLength(hull, True), True).reshape(-1, 2).astype(np.float64)
    edges = []
    for i in range(len(ap)):
        a, b = ap[i], ap[(i + 1) % len(ap)]
        border = (min(a[0], b[0]) > W - 4) or (min(a[1], b[1]) > H - 4) or (max(a[0], b[0]) < 3)
        if not border and np.linalg.norm(b - a) > 25: edges.append((np.linalg.norm(b - a), a, b))
    hor = sorted([e for e in edges if abs(e[2][0] - e[1][0]) > abs(e[2][1] - e[1][1])], key=lambda e: -e[0])
    ver = sorted([e for e in edges if abs(e[2][0] - e[1][0]) <= abs(e[2][1] - e[1][1])], key=lambda e: -e[0])
    mid = lambda e, ax: (e[1][ax] + e[2][ax]) / 2
    def two(es, ax):
        out = es[:1]
        for e in es[1:]:
            if abs(mid(e, ax) - mid(out[0], ax)) > 60: out.append(e); break
        return out
    hs, vs = two(hor, 1), two(ver, 0)
    if len(hs) < 1 or len(vs) < 1: return None, comp
    def X(e, f):
        (x1, y1), (x2, y2) = e[1], e[2]; (x3, y3), (x4, y4) = f[1], f[2]
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        return np.array([((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d, ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d])
    unit = lambda e: (e[2] - e[1]) / np.linalg.norm(e[2] - e[1])
    top = min(hs, key=lambda e: mid(e, 1)); left = min(vs, key=lambda e: mid(e, 0))
    tl = X(top, left)
    dt = unit(top); dt = dt if dt[0] > 0 else -dt
    dl = unit(left); dl = dl if dl[1] > 0 else -dl
    if len(vs) == 2:
        right = max(vs, key=lambda e: mid(e, 0)); tr = X(top, right)
    else: right = None
    if len(hs) == 2:
        bot = max(hs, key=lambda e: mid(e, 1)); bl = X(bot, left)
    else: bot = None
    if bot is None and right is None: return None, comp
    if bot is None:  bl = tl + dl * np.linalg.norm(tr - tl) / ASPECT
    if right is None: tr = tl + dt * np.linalg.norm(bl - tl) * ASPECT
    if bot is not None and right is not None: br = X(bot, right)
    elif bot is not None:
        db = unit(bot); db = db if db[0] > 0 else -db; br = bl + db * np.linalg.norm(tr - tl)
    else:
        dr = unit(right); dr = dr if dr[1] > 0 else -dr; br = tr + dr * np.linalg.norm(bl - tl)
    return np.array([tl, tr, br, bl], np.float32), comp
