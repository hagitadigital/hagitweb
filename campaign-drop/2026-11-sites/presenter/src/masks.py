import sys
from PIL import Image, ImageDraw
out=sys.argv[1]
for d in (420,300,440):
    k=4; m=Image.new('L',(d*k,d*k),0); ImageDraw.Draw(m).ellipse((0,0,d*k-1,d*k-1),fill=255); m.resize((d,d),Image.LANCZOS).save(f'{out}/mask{d}.png')
    D=d+12; r=Image.new('RGBA',(D*k,D*k),(0,0,0,0)); g=ImageDraw.Draw(r); g.ellipse((0,0,D*k-1,D*k-1),outline=(196,118,90,255),width=5*k); r.resize((D,D),Image.LANCZOS).save(f'{out}/ring{d}.png')
