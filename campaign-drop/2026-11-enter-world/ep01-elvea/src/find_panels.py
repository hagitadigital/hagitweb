# Finds the three cream panels of the board in each studio still (941x1672) -> quads TL,TR,BR,BL.
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage
res={}
for n in sys.argv[1:]:
    im=np.asarray(Image.open(n).convert('RGB')).astype(int); H,W,_=im.shape
    mx=im.max(-1); mn=im.min(-1)
    m=(mx>195)&((mx-mn)<40); m[:, int(W*0.6):]=False
    m=ndimage.binary_opening(m,iterations=3)
    lab,k=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,k+1))
    big=sorted([(s,i+1) for i,s in enumerate(sizes) if s>25000],reverse=True)[:3]
    out=[]
    for s,i in big:
        reg=ndimage.binary_fill_holes(lab==i)
        ys,xs=np.nonzero(reg)
        q=[(int(xs[j]),int(ys[j])) for j in (np.argmin(xs+ys),np.argmax(xs-ys),np.argmax(xs+ys),np.argmin(xs-ys))]
        out.append((ys.mean(),q,int(s)))
    out.sort(); res[n.split('/')[-1].split('.')[0]]=[o[1] for o in out]
    print(n.split('/')[-1], [ (o[1],o[2]) for o in out])
json.dump(res,open('/tmp/claude-0/-home-user/6b09a262-53cb-5f9d-b72a-2c8359943c4e/scratchpad/series/quads.json','w'))
