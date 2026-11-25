"""Find the laptop's white screen in a frame of the take: returns its four corners (tl,tr,br,bl; may lie outside the frame) and a matte."""
import cv2, numpy as np
def screen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    m = ((hsv[..., 2] > 200) & (hsv[..., 1] < 40)).astype(np.uint8) * 255
    m[:int(img.shape[0] * .55)] = 0                                   # the screen is always in the lower part of the frame
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2: return None, None
    k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
    if st[k, cv2.CC_STAT_AREA] < 4000: return None, None
    comp = (lab == k).astype(np.uint8) * 255
    hull = cv2.convexHull(max(cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0], key=cv2.contourArea))
    ap = cv2.approxPolyDP(hull, .006 * cv2.arcLength(hull, True), True).reshape(-1, 2).astype(np.float64)
    H, W = img.shape[:2]
    edges = []
    for i in range(len(ap)):
        a, b = ap[i], ap[(i + 1) % len(ap)]
        on_border = (a[0] > W - 3 and b[0] > W - 3) or (a[1] > H - 3 and b[1] > H - 3) or (a[0] < 2 and b[0] < 2)
        if not on_border: edges.append((np.linalg.norm(b - a), a, b))
    # merge collinear neighbours, then keep the four longest directions (two near-horizontal, two near-vertical)
    hor = sorted([e for e in edges if abs(e[2][0] - e[1][0]) > abs(e[2][1] - e[1][1])], key=lambda e: -e[0])
    ver = sorted([e for e in edges if abs(e[2][0] - e[1][0]) <= abs(e[2][1] - e[1][1])], key=lambda e: -e[0])
    def pick(es, axis):
        out = [es[0]]
        for e in es[1:]:
            if abs((e[1][axis] + e[2][axis]) / 2 - (out[0][1][axis] + out[0][2][axis]) / 2) > 40: out.append(e); break
        return out
    if not hor or not ver: return None, comp
    hs, vs = pick(hor, 1), pick(ver, 0)
    if len(hs) < 2 or len(vs) < 2: return None, comp
    top, bot = sorted(hs, key=lambda e: e[1][1] + e[2][1]); left, right = sorted(vs, key=lambda e: e[1][0] + e[2][0])
    def X(e, f):
        (x1, y1), (x2, y2) = e[1], e[2]; (x3, y3), (x4, y4) = f[1], f[2]
        d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        return [((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d, ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d]
    return np.array([X(top, left), X(top, right), X(bot, right), X(bot, left)], np.float32), comp
