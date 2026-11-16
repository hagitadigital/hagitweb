# RUE° (World 07) — a reel that opens on the wow: the building lighting up under the hook line.
# Run from a folder that has the world's images in ./a/ (copies of rue/assets/*.webp); writes reel.html next to this file.
import re, math, os
HERE=os.path.dirname(os.path.abspath(__file__))
T=open('/home/user/hagitweb/.claude/skills/brandos-brand-world-reel/assets/reel-template.html',encoding='utf-8').read()
D=30.0
def P(t): return '%.3f%%'%(max(0,min(D,t))/D*100)
css=[]; uid=[0]
def kf(body):
    uid[0]+=1; n='k%d'%uid[0]; css.append('@keyframes %s{%s}'%(n,body)); return n
SERIF="'Frank Ruhl Libre',serif"; NUM="'Bodoni Moda',serif"
NUIT='#14122A'; STONE='#EFE6D8'; PEACH='#F7C9A3'; APR='#F2A977'; INK='#1A1730'

# ---------- the lighting rig (the site's hero, same window map) ----------
COMMON=[[27,80,10,14],[5,90,7,7],[42,91,6,6]]
HOMES=[[16.5,57,5.5,6.5],[28.5,48.5,3.2,5.5],[32.5,39,3.2,5.5],[19.5,44.5,4.2,5],[28.5,62,3.2,5.5],[31.5,26.5,3.2,5],[19,29.5,3.6,4.6],[32.5,51,3.2,5.5],[19.5,15,3.6,5.5],[32.5,64,3.2,5.5],[28.5,36,3.2,5.5],[28,23.5,3.2,5]]
T_LOBBY,T_FIRST,GAP,T_ALL=-1.0,-0.42,0.21,2.95
def lamp(t):
    if t<=0: return kf('0%,100%{opacity:1}')
    return kf('0%%,%s{opacity:0}%s{opacity:.7}%s{opacity:.3}%s,100%%{opacity:1}'%(P(t),P(t+.07),P(t+.13),P(t+.42)))
def rig():
    h='<div style="position:absolute;left:-139px;top:384px;width:2717px;height:1536px">'
    h+='<img src="a/10-hero.webp" alt="" style="position:absolute;inset:0;width:100%;height:100%;filter:brightness(.46) saturate(.42) contrast(1.06) hue-rotate(-8deg)">'
    def glow(g,t):
        m='radial-gradient(ellipse %s%% %s%% at %s%% %s%%,#000 0,#000 52%%,transparent 100%%)'%(g[2],g[3],g[0],g[1])
        return '<div style="position:absolute;inset:0;background:url(a/10-hero.webp) 0 0/100%% 100%%;-webkit-mask-image:%s;mask-image:%s;animation-name:%s;animation-timing-function:linear"></div>'%(m,m,lamp(t))
    for g in COMMON: h+=glow(g,T_LOBBY)
    for i,g in enumerate(HOMES): h+=glow(g,T_FIRST+i*GAP)
    h+='<img src="a/10-hero.webp" alt="" style="position:absolute;inset:0;width:100%%;height:100%%;animation-name:%s">'%kf('0%%,%s{opacity:0}%s,100%%{opacity:1}'%(P(T_ALL),P(T_ALL+1.1)))
    sky=kf('0%%,%s{background-color:#1A202E}%s,100%%{background-color:#36488C}'%(P(T_ALL),P(T_ALL+1.1)))
    m='linear-gradient(to bottom,#000 0,#000 70%,transparent 100%)'
    h+='</div><div style="position:absolute;left:0;right:0;top:0;height:560px;-webkit-mask-image:%s;mask-image:%s;animation-name:%s"></div>'%(m,m,sky)
    return h
def plate(txt,fs,extra='',fill=False):
    st='display:inline-flex;align-items:center;justify-content:center;min-width:1.9em;padding:.16em .36em .08em;border-radius:%dpx;font-family:%s;font-weight:500;font-size:%dpx;line-height:1;direction:ltr;'%(round(fs*.17),SERIF,fs)
    st+=('background:%s;color:%s;'%(STONE,INK)) if fill else ('border:3px solid %s;color:%s;background:rgba(20,18,42,.3);'%(STONE,STONE))
    return '<span style="%s%s">%s</span>'%(st,extra,txt)

# ---------- HOOK: opens on the wow ----------
count=''.join('<span class="stack" data-show="%.2f,%.2f" data-fade="0.02" style="display:flex;align-items:center;justify-content:center">%d</span>'%(0 if i==2 else T_FIRST+i*GAP+.06,(T_FIRST+(i+1)*GAP+.06) if i<11 else 30,i+1) for i in range(2,12))
hook=f'''<div class="hook stack" style="background:#1A202E">
  {rig()}
  <div style="position:absolute;top:84px;right:80px;display:flex;flex-direction:column;align-items:flex-end;gap:4px">
    <div style="font-family:'Cormorant Garamond',serif;font-style:italic;font-size:36px;color:{STONE}" dir="ltr">Brand Worlds Studio</div>
    <div style="font-size:17px;letter-spacing:.3em;color:rgba(239,230,216,.7)">חגית אנטבי</div>
  </div>
  <div style="position:absolute;top:214px;left:70px;right:70px;text-align:right;font-family:{SERIF};font-size:84px;font-weight:500;line-height:1.14;color:{STONE}" dir="rtl">כל יזם מראה הדמיה.<br><span style="color:{PEACH}">מי זוכר של מי הבניין?</span></div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(to top,rgba(20,18,42,.95),rgba(20,18,42,0))"></div>
  <div style="position:absolute;left:70px;top:1470px;display:flex;align-items:center;gap:26px;direction:ltr">
    <span style="position:relative;width:230px;height:170px;border:3px solid {STONE};border-radius:26px;background:rgba(20,18,42,.4);font-family:{SERIF};font-weight:500;font-size:120px;line-height:1;color:{STONE}">{count}</span>
    <span style="font-size:34px;line-height:1.3;color:{STONE};direction:rtl;text-align:right">משפחות<br>חזרו הביתה</span>
  </div>
'''
a,b=T.index('<div class="hook stack"'),T.index('  <svg class="stack" width="1080"')
T=T[:a]+hook+T[b:]

# ---------- scenes ----------
head=lambda top,l1,l2,size=96: f'<div style="position:absolute;top:{top}px;left:70px;right:70px;text-align:right;font-family:{SERIF};font-weight:400;font-size:{size}px;line-height:1.1;color:{STONE}" dir="rtl">{l1}<br><span style="color:{PEACH}">{l2}</span></div>'
# A · core
sA=f'''<section class="scene" data-show="0,10"><div class="stack" style="background:#1F1C4E"></div>{rig()}
  <div data-show="5.7,10" style="position:absolute;inset:0">{head(210,'אותה כתובת.','סטנדרט אחר.',112)}</div>
  <div style="position:absolute;left:0;right:0;bottom:0;height:560px;background:linear-gradient(to top,rgba(20,18,42,.96),rgba(20,18,42,0))"></div>
  <div data-in="6.3" style="position:absolute;left:70px;top:1500px;display:flex;align-items:center;gap:26px;direction:ltr">{plate('14',120)}<span style="direction:rtl;text-align:right;color:{STONE}"><b style="display:block;font-family:{SERIF};font-weight:400;font-size:52px;line-height:1.15">הדקל 14, רמת גן</b><span style="font-size:30px;color:rgba(239,230,216,.75)">12 משפחות חזרו לאותו מספר</span></span></div>
</section>'''
# B · signature: the plate stays, everything else changes
steps=[('01-old.webp','1964','השיכון','50% 50%'),('17-model.webp','2025','היתר','50% 50%'),('18-boxes.webp','2026','דיור חלופי','50% 50%'),('19-site.webp','2027','בנייה','40% 50%'),('16-flagship.webp','2029','חוזרים הביתה','50% 60%')]
B0,BS=9.9,1.12
imgs=''; labs=''
for i,(src,yr,nm,pos) in enumerate(steps):
    t=B0+i*BS
    an='' if i==0 else 'animation-name:%s;'%kf('0%%,%s{clip-path:inset(100%% 0 0 0)}%s,100%%{clip-path:inset(0 0 0 0)}'%(P(t-.45),P(t)))
    dim='' if i==4 else 'filter:brightness(.8) saturate(.75);'
    imgs+=f'<div class="stack" style="{an}"><img class="cover" src="a/{src}" alt="" style="object-position:{pos};{dim}"></div>'
    e=30 if i==4 else t+BS-.12
    labs+=f'<div class="stack" data-show="{t:.2f},{e:.2f}" data-fade="0.12" style="display:flex;align-items:baseline;justify-content:center;gap:22px;direction:rtl"><span style="font-family:{NUM};font-size:92px;color:{PEACH};direction:ltr">{yr}</span><span style="font-size:42px;color:{STONE}">{nm}</span></div>'
ring=kf('0%%,%s{box-shadow:0 0 0 0 rgba(242,169,119,0),0 30px 80px rgba(20,18,42,.6)}%s,100%%{box-shadow:0 0 0 14px rgba(242,169,119,.95),0 0 120px 30px rgba(242,169,119,.55)}'%(P(B0+4*BS),P(B0+4*BS+.6)))
sB=f'''<section class="scene" data-show="9.7,15.6"><div class="stack" style="background:{NUIT}"></div>{imgs}
  <div class="stack" style="background:linear-gradient(to bottom,rgba(20,18,42,.9) 0,rgba(20,18,42,.35) 30%,rgba(20,18,42,.1) 52%,rgba(20,18,42,.88) 82%)"></div>
  <div style="position:absolute;top:230px;left:70px;right:70px;text-align:right;font-family:{SERIF};font-size:104px;line-height:1.1;color:{STONE}" dir="rtl"><div data-in="10.0">הבניין מתחלף.</div><div data-in="13.5" style="color:{PEACH}">המספר נשאר.</div></div>
  <div style="position:absolute;left:0;right:0;top:830px;display:flex;justify-content:center"><span style="display:inline-flex;border-radius:44px;animation-name:{ring}">{plate('14',250,fill=True)}</span></div>
  <div style="position:absolute;left:0;right:0;top:1500px;height:120px">{labs}</div>
  <div style="position:absolute;left:230px;right:230px;top:1660px;height:4px;background:rgba(239,230,216,.25);direction:ltr"><div style="height:4px;background:{APR};transform-origin:left;animation-name:{kf('0%%,%s{transform:scaleX(.2)}%s,100%%{transform:scaleX(1)}'%(P(B0),P(B0+4*BS)))};animation-timing-function:linear"></div></div>
</section>'''
# C · the element: the plate is the pin
routes=['M330,310 H400','M330,310 H220 V268','M330,310 H400 V190','M330,310 H560 V364','M330,310 H220 V430 H124','M330,310 H560 V190']
spots=[(400,310,2),(220,268,3),(400,190,4),(560,364,6),(124,430,7),(560,190,8)]
C0=15.7
rs=''.join('<path pathLength="1" d="%s" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" style="animation-name:%s"/>'%(d,APR,kf('0%%,%s{stroke-dashoffset:1}%s,100%%{stroke-dashoffset:0}'%(P(C0+i*.2),P(C0+i*.2+.8)))) for i,d in enumerate(routes))
ss=''.join('<g style="animation-name:%s"><circle cx="%d" cy="%d" r="19" fill="#15122D" stroke="%s" stroke-width="3"/><text x="%d" y="%d" text-anchor="middle" font-family="Bodoni Moda" font-size="20" fill="%s">%d</text></g>'%(kf('0%%,%s{opacity:0}%s,100%%{opacity:1}'%(P(C0+i*.2+.6),P(C0+i*.2+.9))),x,y,APR,x,y+7,STONE,n) for i,(x,y,n) in enumerate(spots))
row=''.join('<span data-in="%.2f" style="display:flex;flex-direction:column;align-items:center;gap:10px">%s<span style="font-size:22px;color:rgba(239,230,216,.75)">%s</span></span>'%(16.5+i*.16,plate(n,64),c) for i,(n,c) in enumerate([('14','רמת גן'),('3','בת ים'),('7','רחובות'),('22','כפר סבא'),('9','תל אביב')]))
sC=f'''<section class="scene" data-show="15.3,19"><div class="stack" style="background:linear-gradient(to bottom,#1D1942,#221C4A)"></div>
  {head(220,'אצלנו לפרויקט אין שם.','יש לו כתובת.',84)}
  <svg viewBox="0 0 800 620" style="position:absolute;left:40px;top:560px;width:1000px;height:775px;border-radius:18px;background:#15122D">
    <rect x="98" y="204" width="106" height="92" rx="10" fill="rgba(90,68,128,.4)"/>
    <g fill="none" stroke="rgba(239,230,216,.08)" stroke-width="8" stroke-linecap="round"><path d="M0,92 C200,40 500,112 800,62"/><path d="M0,550 H800"/><path d="M80,0 V620"/><path d="M720,0 V620"/><path d="M540,620 L800,392"/></g>
    <g fill="none" stroke="rgba(239,230,216,.12)" stroke-width="16" stroke-linecap="round"><path d="M0,190 H800"/><path d="M0,430 H800"/><path d="M220,0 V620"/><path d="M400,0 V620"/><path d="M560,0 V620"/><path d="M0,310 H800" stroke="rgba(239,230,216,.2)"/></g>
    <circle cx="330" cy="310" r="150" fill="none" stroke="rgba(247,201,163,.3)" stroke-dasharray="3 8"/><circle cx="330" cy="310" r="292" fill="none" stroke="rgba(247,201,163,.3)" stroke-dasharray="3 8"/>
    {rs}{ss}
    <g transform="translate(330 310)"><path d="M0,0 L-11,-20 H11 Z" fill="{STONE}"/><rect x="-46" y="-80" width="92" height="62" rx="12" fill="{STONE}"/><text x="0" y="-35" text-anchor="middle" font-family="Frank Ruhl Libre" font-weight="500" font-size="40" fill="{INK}">14</text></g>
  </svg>
  <div style="position:absolute;left:50px;right:50px;top:1420px;display:flex;justify-content:space-between;direction:rtl">{row}</div>
</section>'''
# D · live site: the fan of rooms + what improves
CX,CY,R,R0=540,1080,500,112
rooms=['16-flagship.webp','22-lobby.webp','20-kitchen.webp','23-living.webp','21-balcony.webp']
W=36.0; D0=19.0
pt=lambda r,a:(R+r*math.cos(math.radians(a)), R-r*math.sin(math.radians(a)))
sector='polygon(50% 50%,'+','.join('%.2f%% %.2f%%'%(pt(R,.7+k*(W-1.4)/12)[0]/10,pt(R,.7+k*(W-1.4)/12)[1]/10) for k in range(13))+')'
fan=''
for i,src in enumerate(rooms):
    a=W*i
    pts=[pt(R0,a),pt(R,a),pt(R,a+W),pt(R0,a+W)]+[pt(R,q) for q in (90,) if a<q<a+W]
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    x,y,w,h=min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)
    ko=kf('0%%,%s{transform:rotate(0deg)}%s,100%%{transform:rotate(-%.1fdeg)}'%(P(D0),P(D0+1.3),a))
    ki=kf('0%%,%s{transform:rotate(0deg)}%s,100%%{transform:rotate(%.1fdeg)}'%(P(D0),P(D0+1.3),a))
    fan+=f'<div style="position:absolute;inset:0;clip-path:{sector};animation-name:{ko}"><div style="position:absolute;inset:0;animation-name:{ki}"><img src="a/{src}" alt="" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;height:{h:.0f}px;object-fit:cover"></div></div>'
gain=''.join(f'<div data-in="{20.5+i*.45:.2f}" style="display:grid;grid-template-columns:1fr 110px 50px 250px;align-items:baseline;gap:14px;padding:20px 0;border-bottom:1.5px solid rgba(239,230,216,.2);direction:rtl;font-size:38px;color:{STONE}"><span>{l}</span><span style="font-family:{NUM};font-size:42px;color:rgba(239,230,216,.5);direction:ltr;text-align:right">{o}</span><span style="color:{APR}">←</span><span style="display:flex;align-items:baseline;gap:12px;font-size:26px;color:rgba(239,230,216,.75)"><b style="font-family:{SERIF};font-weight:500;font-size:84px;line-height:1;color:{PEACH}">{n}</b>{u}</span></div>' for i,(l,o,n,u) in enumerate([('שטח הדירה',68,93,'מ״ר'),('שעות אור בסלון',3,9,'ביום'),('עצים ברחוב',9,31,'עצים')]))
sD=f'''<section class="scene" data-show="18.7,22.9"><div class="stack" style="background:linear-gradient(to bottom,#2F2659,#493873)"></div>
  {head(215,'סטנדרט אחר','מתחיל בפנים.',100)}
  <div style="position:absolute;left:{CX-R}px;top:{CY-R}px;width:{2*R}px;height:{R}px;overflow:hidden"><div style="position:absolute;left:0;top:0;width:{2*R}px;height:{2*R}px">{fan}
    <div style="position:absolute;left:{R-R0}px;top:{R-R0}px;width:{2*R0}px;height:{2*R0}px;border-radius:50%;background:#3A2E69"></div>
    <div style="position:absolute;left:{R-R0+22}px;top:{R-R0+22}px;width:{2*R0-44}px;height:{2*R0-44}px;border-radius:50%;background:radial-gradient(circle,#F7C9A3 0,#F2A977 70%,#A8718F 100%)"></div></div></div>
  <div style="position:absolute;left:80px;right:80px;top:1150px">{gain}</div>
</section>'''
# E · the promise
sE=f'''<section class="scene" data-show="22.6,30"><img class="cover" src="a/16-flagship.webp" alt="" style="object-position:50% 60%">
  <div class="stack" style="background:linear-gradient(to bottom,rgba(20,18,42,.82) 0,rgba(20,18,42,.2) 30%,rgba(20,18,42,.15) 50%,rgba(20,18,42,.92) 78%)"></div>
  <div style="position:absolute;left:0;right:0;top:440px;display:flex;justify-content:center"><span data-in="23.0" style="font-family:{NUM};font-weight:500;font-size:96px;letter-spacing:.12em;border:3px solid {STONE};border-radius:26px;padding:.3em .5em .22em .6em;color:{STONE};background:rgba(20,18,42,.35)" dir="ltr">RUE<span style="color:{APR}">°</span></span></div>
  <div data-in="23.5" style="position:absolute;left:0;right:0;top:1010px;text-align:center;font-family:{SERIF};font-size:104px;line-height:1.1;color:{STONE}" dir="rtl">אותה כתובת.<br><span style="color:{PEACH}">סטנדרט אחר.</span></div>
  <div data-in="24.2" style="position:absolute;left:0;right:0;top:1270px;text-align:center;font-family:{NUM};font-style:italic;font-size:42px;color:{STONE}" dir="ltr">Same address. Another standard.</div>
</section>'''
secs=[sA,sB,sC,sD,sE]; it=iter(secs)
T,n=re.subn(r'<section class="scene" data-show="[^"]*">.*?</section>',lambda m:next(it),T,flags=re.S); assert n==5
T=re.sub(r'\n\s*<!-- frame sequence example:.*?-->','',T,flags=re.S)

# ---------- studio texts ----------
def rep(a,b,c=1):
    global T
    assert T.count(a)==c,(a,T.count(a)); T=T.replace(a,b)
rep('BRAND° · עולם מותג NN','RUE° · עולם מותג 07')
T=T.replace('NN','07')
rep('EDIT: משפט אחד על העולם, מתוך האתר.','חברת יזמות שהמותג שלה הוא הכתובת.')
rep('EDIT: התשובה להוק.<br>שורה שנייה.','את <span dir="ltr">RUE°</span> זוכרים<br>לפי הכתובת.')
rep('EDIT: שאלה חוזרת ללקוחה<br>על העסק שלה.','ואת החברה שלך,<br>לפי מה זוכרים?')
names=[('The Core','אותה כתובת. סטנדרט אחר.'),('The Visual World','השלט נשאר. הכול מתחלף.'),('The Element','שלט מספר הבית'),('Live Site','המניפה, והמספרים של המחר'),('The Promise','אותה כתובת. סטנדרט אחר.')]
nt=iter(names)
def hud(m):
    e,h=next(nt); return 'dir="ltr">0%s · %s</span><span style="font-size: 22px; color: var(--s-ink)">%s</span>'%(m.group(1),e,h)
T,n=re.subn(r'dir="ltr">0(\d) · [^<]*</span><span style="font-size: 22px; color: var\(--s-ink\)">[^<]*</span>',hud,T); assert n==5,n
rep('data-show="9.9,14.7"','data-show="9.9,15.4"'); rep('data-show="14.7,18.7"','data-show="15.4,18.8"'); rep('data-show="18.7,22.7"','data-show="18.8,22.7"')
rep("--w-bg:#F7F0E6;","--w-bg:#14122A;"); rep("--w-ink:#3B2E33;","--w-ink:#EFE6D8;"); rep("--w-accent:#C9878E;","--w-accent:#F2A977;")
rep('</style>\n</head>','\n'.join(css)+'\n</style>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&amp;family=Frank+Ruhl+Libre:wght@300..700&amp;display=swap">\n</head>')
assert 'EDIT' not in re.sub(r'<!--.*?-->|/\*.*?\*/','',T,flags=re.S), re.findall(r'.{30}EDIT.{30}',re.sub(r'<!--.*?-->|/\*.*?\*/','',T,flags=re.S))[:3]
open(os.path.join(HERE,'reel.html'),'w',encoding='utf-8').write(T); print('ok',len(T))
