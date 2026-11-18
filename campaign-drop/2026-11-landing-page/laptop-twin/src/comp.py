import cv2, numpy as np, sys, os, glob
clipdir, scrdir, outdir = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
frames = sorted(glob.glob(clipdir+'/f*.png')); scr = sorted(glob.glob(scrdir+'/s*.jpg'))
C0 = np.float32([[669,954],[1077,1033],[996,1497],[618,1283]])  # TL TR BR BL display corners, frame 0
f0 = cv2.imread(frames[0]); g0 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY)
H,W = g0.shape
# features on the laptop (lid edges, notch, keyboard), not the person
m = np.zeros_like(g0); cv2.fillPoly(m,[np.int32([[560,900],[1080,980],[1080,1600],[330,1600],[330,1380],[600,1280]])],255)
inner = np.zeros_like(g0); cv2.fillPoly(inner,[np.int32(C0 + np.float32([[25,25],[-25,25],[-25,-25],[25,-25]]))],255)
m[inner>0]=0
p0 = cv2.goodFeaturesToTrack(g0, 400, 0.01, 6, mask=m)
sw, sh = 1440, 900
src = np.float32([[0,0],[sw,0],[sw,sh],[0,sh]])
disp = np.float32([62,53,50])
log=[]
for i,fp in enumerate(frames):
    f = cv2.imread(fp); g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    if i==0: C = C0.copy()
    else:
        p1, st, err = cv2.calcOpticalFlowPyrLK(g0, g, p0, None, winSize=(31,31), maxLevel=4)
        ok = st.ravel()==1
        M, inl = cv2.findHomography(p0[ok], p1[ok], cv2.RANSAC, 2.0)
        C = cv2.perspectiveTransform(C0.reshape(-1,1,2), M).reshape(-1,2)
        log.append((i, int(ok.sum()), int(inl.sum()), np.abs(C-C0).max()))
    page = cv2.imread(scr[min(i,len(scr)-1)])
    # supersampled warp for clean edges
    S = 2
    Hm = cv2.getPerspectiveTransform(src, C*S)
    wp = cv2.warpPerspective(page, Hm, (W*S,H*S), flags=cv2.INTER_AREA)
    wm = cv2.warpPerspective(np.full((sh,sw),255,np.uint8), Hm, (W*S,H*S))
    wp = cv2.resize(wp,(W,H),interpolation=cv2.INTER_AREA); wm = cv2.resize(wm,(W,H),interpolation=cv2.INTER_AREA).astype(np.float32)/255
    # key: keep foreground (hair, notch, anything not display-coloured) on top
    d = np.linalg.norm(f.astype(np.float32)-disp, axis=2)
    key = 1-np.clip((d-28)/22,0,1)                       # 1 = display colour
    key = cv2.GaussianBlur(key,(0,0),1.2)
    a = (wm*key)[...,None]
    # screen look: slightly lifted blacks + soft glare from the original frame
    lit = wp.astype(np.float32)*0.93 + 10
    out = lit*a + f.astype(np.float32)*(1-a)
    cv2.imwrite(f'{outdir}/o{i:04d}.jpg', np.clip(out,0,255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY,95])
for l in log[::24]+log[-1:]: print(l)
