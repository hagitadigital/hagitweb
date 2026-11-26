import sys
from PIL import Image
fs=sys.argv[2].split(','); n=len(fs); cols=min(n,7); rows=(n+cols-1)//cols
sh=Image.new('RGB',(270*cols,480*rows))
for i,f in enumerate(fs): sh.paste(Image.open('test/r-%s.jpg'%f).resize((270,480)),((i%cols)*270,(i//cols)*480))
sh.save(sys.argv[1],quality=85)
