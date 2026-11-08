import sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
def coeffs(dst, src):
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A+= [[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; B+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
base=Image.open(sys.argv[1]).convert('RGB'); W,H=base.size
arr=np.asarray(base).astype(int)
out=base.copy()
quads={'top':[(50,348),(400,357),(410,693),(52,697)],'mid':[(56,712),(413,708),(428,1056),(68,1070)],'bot':[(70,1090),(430,1076),(447,1468),(88,1505)]}
for k,q in quads.items():
    pan=Image.open(f'panel-{k}.png').convert('RGB'); w,h=pan.size
    # dst corners in order TL TR BR BL ; PIL maps output->input
    warped=pan.transform((W,H),Image.PERSPECTIVE,coeffs(q,[(0,0),(w,0),(w,h),(0,h)]),Image.BICUBIC)
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(q,fill=255)
    # light: modulate by board luminance so room light stays
    lum=np.asarray(base.convert('L').filter(ImageFilter.GaussianBlur(25))).astype(float)
    ref=np.median(lum[np.asarray(m)>0]); shade=np.clip(lum/ref,0.85,1.12)[...,None]
    wa=np.clip(np.asarray(warped).astype(float)*shade,0,255).astype('uint8')
    # hand mask: deviation from panel cream
    med=np.median(arr[np.asarray(m)>0],axis=0)
    dev=np.abs(arr-med).sum(-1)>70
    hand=Image.fromarray((dev*255).astype('uint8')).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.5))
    mm=np.asarray(m.filter(ImageFilter.GaussianBlur(0.8))).astype(float)/255*(1-np.asarray(hand).astype(float)/255)
    o=np.asarray(out).astype(float); o=o*(1-mm[...,None])+wa*mm[...,None]; out=Image.fromarray(o.astype('uint8'))
out.resize((1080,1920),Image.LANCZOS).save(sys.argv[2],quality=90)
