import cv2, numpy as np, os
os.makedirs('base',exist_ok=True)
W,H=1080,1920
def ease(t): t=min(max(t,0),1); return t*t*(3-2*t)
def easeIn(t): t=min(max(t,0),1); return t*t*t
# ---------- S1: over-the-shoulder, push forward into the screen (138 frames)
C=np.float32([[528,974],[1002,1002],[982,1366],[508,1279]])
disp=np.float32([97,82,77])
src=np.float32([[0,0],[1440,0],[1440,900],[0,900]])
Hm=cv2.getPerspectiveTransform(src,C*2)
wm=cv2.resize(cv2.warpPerspective(np.full((900,1440),255,np.uint8),Hm,(W*2,H*2)),(W,H),interpolation=cv2.INTER_AREA).astype(np.float32)/255
cx,cy=C[:,0].mean(),C[:,1].mean()
N1=138
def cam(i):
    t=i/(N1-1)
    z=1+0.10*ease(t/0.45)+1.55*easeIn((t-0.30)/0.70)      # slow drift, then the push
    k=ease((t-0.25)/0.75)
    fx=540+(cx-540)*k; fy=960+(cy-90-960)*k                 # look-at point drifts to the screen
    return z,fx,fy
def s1(i):
    k=min(int(round(i/30*24))+1,121)                        # real clip, 24fps -> 30fps
    ots=cv2.resize(cv2.imread(f'clipB/f{k:04d}.png'),(W,H),interpolation=cv2.INTER_LANCZOS4)
    d=np.linalg.norm(ots.astype(np.float32)-disp,axis=2)
    key=cv2.GaussianBlur(1-np.clip((d-22)/18,0,1),(0,0),1.0)   # hair and notch stay in front
    a=(wm*key)[...,None]
    page=cv2.imread(f'scrB/s{i:04d}.jpg')
    wp=cv2.resize(cv2.warpPerspective(page,Hm,(W*2,H*2),flags=cv2.INTER_AREA),(W,H),interpolation=cv2.INTER_AREA).astype(np.float32)
    f=(wp*0.95+8)*a+ots.astype(np.float32)*(1-a)
    z,fx,fy=cam(i)
    M=np.float32([[z,0,540-z*fx],[0,z,960-z*fy]])
    return cv2.warpAffine(np.clip(f,0,255).astype(np.uint8),M,(W,H),flags=cv2.INTER_LANCZOS4)
# ---------- S2: the page full frame, mobile (180 frames)
def s2(i):
    m=cv2.imread(f'scrM/s{i:04d}.jpg')
    m=m[84:1919,24:1056]                                    # drop the studio top bar
    return cv2.resize(m,(W,H),interpolation=cv2.INTER_LANCZOS4)
# ---------- S3: front shot with the bottle section on the laptop (24fps -> 30fps, 144 frames)
def s3(i):
    k=min(int(round((i/30)*24))+10,144)
    f=cv2.imread(f'outC/o{k:04d}.jpg')
    z=1.0+0.05*(i/143)                                      # slow push
    M=np.float32([[z,0,(1-z)*600],[0,z,(1-z)*1000]])
    return cv2.warpAffine(f,M,(W,H),flags=cv2.INTER_LANCZOS4)
n=0
X=12                                                        # cross-dissolve frames
for i in range(N1):
    f=s1(i)
    if i>=N1-X:
        t=(i-(N1-X)+1)/(X+1); g=s2(0); z=1.25-0.25*t
        M=np.float32([[z,0,540-z*540],[0,z,960-z*960]]); g=cv2.warpAffine(g,M,(W,H))
        f=cv2.addWeighted(f,1-t,g,t,0)
    cv2.imwrite(f'base/b{n:04d}.jpg',f,[cv2.IMWRITE_JPEG_QUALITY,94]); n+=1
for i in range(180):
    f=s2(i)
    if i>=180-8:
        t=(i-172+1)/9; f=cv2.addWeighted(f,1-t,s3(0),t,0)
    cv2.imwrite(f'base/b{n:04d}.jpg',f,[cv2.IMWRITE_JPEG_QUALITY,94]); n+=1
for i in range(144):
    cv2.imwrite(f'base/b{n:04d}.jpg',s3(i),[cv2.IMWRITE_JPEG_QUALITY,94]); n+=1
print(n)
