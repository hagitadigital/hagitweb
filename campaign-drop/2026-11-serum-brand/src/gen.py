# Builds the insert pages for the "serum -> brand" talking-head reel (ELVÉA°, World 14).
# Each page is one CSS timeline; render with the reel skill's scripts/render.js (REEL_H=1080 for cards).
HEAD = '''<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Heebo:wght@300;400;500;600&family=Plus+Jakarta+Sans:wght@400;500&display=swap">
<style>
:root{--linen:#F7F3E9;--cream:#F0EADD;--sage:#B9C1A2;--sage-soft:#DFE3CE;--olive:#55613F;--olive-deep:#3E4930;--ink:#2E3526;--nectar:#E9DABC;
--plain:#E6E3DD;--s-bg:#FAF8F3;--s-ink:#6B563F;--s-copper:#C4765A}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:%(H)spx;overflow:hidden;background:var(--plain)}
body{font-family:'Heebo',sans-serif;color:var(--ink);position:relative}
*{animation-duration:%(D)ss;animation-timing-function:linear;animation-fill-mode:both}
.abs{position:absolute}.fill{position:absolute;inset:0}
.chip{position:absolute;padding:10px 26px;border-radius:999px;background:#FFFDF8;color:#3A342C;font-size:34px;font-weight:500;box-shadow:0 6px 18px rgba(60,50,30,.16)}
.pill{position:absolute;top:66px;padding:12px 26px;border-radius:999px;background:rgba(255,253,248,.94);font-size:25px;color:#4A4238;box-shadow:0 4px 14px rgba(60,50,30,.12);white-space:nowrap}
img{display:block}
%(css)s
</style></head><body data-duration="%(D)s">%(body)s
<script>
(function(){const D=+document.body.dataset.duration,css=[];const P=t=>(Math.max(0,Math.min(D,t))/D*100).toFixed(3)+'%%';let n=0;
document.querySelectorAll('[data-show]').forEach(el=>{const [a,b]=el.dataset.show.split(',').map(Number),f=+(el.dataset.fade||.4),k='sh'+(n++);
const s=a<=0?'0%%{opacity:1}':`0%%,${P(a-f)}{opacity:0}${P(a)}{opacity:1}`;const e=b>=D?'100%%{opacity:1}':`${P(b)}{opacity:1}${P(b+f)},100%%{opacity:0}`;
css.push(`@keyframes ${k}{${s}${e}}`);el.style.animationName=k;});
document.querySelectorAll('[data-in]').forEach(el=>{const t=+el.dataset.in,k='in'+(n++),from=el.dataset.from||'translateY(30px)';
css.push(`@keyframes ${k}{0%%,${P(t)}{opacity:0;transform:${from}}${P(t+.7)},100%%{opacity:1;transform:none}}`);el.style.animationName=k;el.style.animationTimingFunction='cubic-bezier(.2,.7,.2,1)';});
document.querySelectorAll('[data-seq]').forEach(el=>{const d=el.dataset,start=+d.start,step=+d.step;let i=0;
for(let f=+d.from;f<=+d.to;f+=+(d.by||1),i++){const im=document.createElement('img'),k='sq'+(n++),t=start+i*step;im.src=d.seq.replace('%%03d',String(f).padStart(3,'0'));
im.style.cssText='position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover';if(i>0){css.push(`@keyframes ${k}{0%%,${P(t-.03)}{opacity:0}${P(t)},100%%{opacity:1}}`);im.style.animationName=k;}el.appendChild(im);}});
const s=document.createElement('style');s.textContent=css.join('\\n');document.head.appendChild(s);})();
</script></body></html>'''
def page(name,H,D,css,body):
    open(name,'w',encoding='utf8').write(HEAD%dict(H=H,D=D,css=css,body=body))
def pc(t,D): return '%.3f%%'%(t/D*100)

FLOOR='<div class="abs" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;border-radius:50%%;background:radial-gradient(closest-side,rgba(70,60,40,.30),rgba(70,60,40,0));%s"></div>'
PLAINBG='<div class="fill" style="background:radial-gradient(120% 90% at 30% 20%,#F1EFEA 0%,#E6E3DD 55%,#D9D5CD 100%)"></div>'

# 01 — the serum alone
D=5
page('01-serum-bare.html',1080,D,'''
@keyframes push{0%{transform:scale(1)}100%{transform:scale(1.05)}}
.b{animation-name:push;transform-origin:50% 60%}''',
PLAINBG+'<div class="fill b">'+FLOOR%(250,856,580,64,'')+'<img class="abs" src="assets/bottle-plain.webp" style="height:800px;left:256px;top:150px"></div>')

# 02 — thousands like it
D=6
F=['none','hue-rotate(-16deg) saturate(1.35)','saturate(.15) brightness(1.07)','hue-rotate(28deg) saturate(.85)','sepia(.55) saturate(1.7) brightness(.93)',
   'hue-rotate(160deg) saturate(.45) brightness(1.03)','saturate(.55) brightness(.9)','hue-rotate(-40deg) saturate(.8)','sepia(.3) saturate(.7) brightness(1.05)']
SX=[1,.86,1.05,.9,1,.82,.95,1.08,.88]
rows=''
for r in range(5):
    cells=''
    for c in range(15):
        k=(c*3+r*4)%9; mid=(r==2 and c==7)
        cells+='<div style="flex:0 0 520px;height:800px;position:relative"><img src="assets/bottle-plain.webp" style="position:absolute;height:800px;left:-24px;filter:%s;transform:scaleX(%s) scale(%s);transform-origin:44%% 92%%"></div>'%(
            'none' if mid else F[k], 1 if mid else SX[k], 1 if mid else (.84+.04*((c+r)%5)))
    rows+='<div class="row r%d" style="display:flex;position:absolute;left:%dpx;top:%dpx">%s</div>'%(r%2,540-7.5*520,540-400-90+(r-2)*960,cells)
page('02-thousands.html',1080,D,'''
@keyframes zoom{0%,8%{transform:scale(1.02)}34%{transform:scale(.36)}100%{transform:scale(.30)}}
@keyframes d0{0%,8%{transform:translateX(0)}100%{transform:translateX(-780px)}}
@keyframes d1{0%,8%{transform:translateX(260px)}100%{transform:translateX(1040px)}}
.world{animation-name:zoom;transform-origin:540px 540px;animation-timing-function:cubic-bezier(.3,.1,.2,1)}
.r0{animation-name:d0}.r1{animation-name:d1}''',
PLAINBG+'<div class="fill world">'+rows+'</div>')

# shared "designed product" stage
def stage(D,t_pack,t_name,t_label,chips=True,start_plain=True):
    css='''
@keyframes bgin{0%%,%(a)s{opacity:0}%(b)s,100%%{opacity:1}}
@keyframes arch{0%%,%(a)s{transform:translateY(760px)}%(c)s,100%%{transform:none}}
@keyframes shift{0%%,%(a)s{transform:translateX(125px)}%(c)s,100%%{transform:none}}
@keyframes box{0%%,%(a)s{opacity:0;transform:translateX(230px)}%(a2)s{opacity:1}%(c)s,100%%{opacity:1;transform:none}}
@keyframes lab{0%%,%(l)s{opacity:0}%(l2)s,100%%{opacity:1}}
.bgin{animation-name:bgin}.arch{animation-name:arch;animation-timing-function:cubic-bezier(.2,.7,.2,1)}
.shift{animation-name:shift;animation-timing-function:cubic-bezier(.3,.1,.2,1)}
.box{animation-name:box;animation-timing-function:cubic-bezier(.2,.7,.2,1)}.lab{animation-name:lab}
.wm{font-family:'Cormorant Garamond',serif;font-size:104px;letter-spacing:.2em;color:var(--ink);line-height:1}
.sub{font-family:'Plus Jakarta Sans',sans-serif;font-size:19px;letter-spacing:.44em;color:var(--olive);margin-top:16px}
'''%dict(a=pc(t_pack,D),a2=pc(t_pack+.25,D),b=pc(t_pack+.7,D),c=pc(t_pack+1.0,D),l=pc(t_label,D),l2=pc(t_label+.7,D))
    body=PLAINBG.replace('%','%%')+'''
<div class="fill bgin" style="background:linear-gradient(160deg,#FBF8F0,#F0EADD)"></div>
<div class="fill bgin" style="overflow:hidden"><div class="abs arch" style="left:360px;top:300px;width:900px;height:1100px;border-radius:450px 450px 0 0;background:linear-gradient(180deg,#B9C1A2,#A9B391)"></div></div>
<div class="abs" style="left:0;right:0;top:880px;bottom:0;background:linear-gradient(180deg,rgba(120,110,85,.10),rgba(120,110,85,0) 60%%)"></div>
<div class="fill box">'''+FLOOR%(560,858,470,56,'')+'''<img class="abs" src="assets/box.webp" style="height:690px;left:590px;top:196px"></div>
<div class="fill shift">'''+FLOOR%(190,832,470,56,'')+'''
<img class="abs" src="assets/bottle-plain.webp" style="height:680px;left:160px;top:230px">
<img class="abs bgin" src="assets/bottle-bare.webp" style="height:680px;left:160px;top:230px">
<img class="abs lab" src="assets/bottle-label.webp" style="height:680px;left:160px;top:230px"></div>
<div class="abs" data-in="%(tn)s" dir="ltr" style="left:0;right:0;top:64px;text-align:center"><div class="wm">ELVÉA°</div><div class="sub">BOTANICAL SKIN SCIENCE</div></div>
'''%dict(tn=t_name)
    if chips:
        body+='<div class="chip" data-in="%s" style="right:60px;top:940px">האריזה</div><div class="chip" data-in="%s" style="right:262px;top:940px">השם</div><div class="chip" data-in="%s" style="right:420px;top:940px">התווית</div>'%(t_pack+.8,t_name+.3,t_label+.4)
    return css,body

# 03 — packaging, name, label
css,body=stage(9,0.9,3.3,5.4)
page('03-designed-product.html',1080,9,css,body)

# 00 — cover: the same serum twice (frame 0)
D=4
page('00-same-serum-twice.html',1080,D,"""
@keyframes push{0%{transform:scale(1)}100%{transform:scale(1.04)}}
.b{animation-name:push;transform-origin:50% 70%}""",
'<div class="abs" style="right:0;top:0;bottom:0;width:540px;overflow:hidden">'+PLAINBG+'<div class="fill b">'+FLOOR%(60,826,420,52,'')+'<img class="abs" src="assets/bottle-plain.webp" style="height:640px;left:44px;top:260px"></div></div>'
+'<div class="abs" style="left:0;top:0;bottom:0;width:540px;overflow:hidden"><div class="fill" style="background:linear-gradient(160deg,#FBF8F0,#F0EADD)"></div>'
+'<div class="abs" style="left:70px;top:330px;width:400px;height:900px;border-radius:200px 200px 0 0;background:linear-gradient(180deg,#B9C1A2,#A9B391)"></div>'
+'<div class="fill b">'+FLOOR%(60,826,420,52,'')+'<img class="abs" src="assets/bottle-label.webp" style="height:640px;left:44px;top:260px"></div>'
+'<div class="abs" dir="ltr" style="left:0;right:0;top:92px;text-align:center"><div style="font-family:\'Cormorant Garamond\',serif;font-size:62px;letter-spacing:.2em;color:#2E3526;line-height:1">ELVÉA°</div><div style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:13px;letter-spacing:.44em;color:#55613F;margin-top:12px">BOTANICAL SKIN SCIENCE</div></div></div>'
+'<div class="abs" style="left:539px;top:0;bottom:0;width:2px;background:rgba(255,255,255,.8)"></div>')

# 04 — the brand world (full screen)
D=10
PILLS='<div class="pill" style="right:44px">חגית אנטבי · <span dir="ltr" style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:23px">Brand Worlds Studio</span></div><div class="pill" style="left:44px"><span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#55613F;margin-left:10px;vertical-align:middle"></span>עולם מותג 14 · <span dir="ltr" style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:23px">ELVÉA°</span></div>'
def card(x,y,t,label,inner,bg='#EDE7DA'):
    return '<div class="abs" data-in="%s" style="left:%dpx;top:%dpx;width:500px;height:620px;border-radius:26px;overflow:hidden;background:%s;box-shadow:0 14px 34px rgba(70,60,40,.16)">%s<div class="chip" style="right:22px;bottom:22px">%s</div></div>'%(t,x,y,bg,inner,label)
site=''.join('<img src="assets/site-%02d.jpg" style="width:100%%">'%i for i in (0,4,5,10))
body='<div class="fill" style="background:linear-gradient(180deg,#F7F3E9,#EFE8DA)"></div>'+PILLS+'''
<div class="abs" dir="ltr" style="left:0;right:0;top:182px;text-align:center;font-family:'Cormorant Garamond',serif;font-size:36px;letter-spacing:.42em;color:#7A6F5C">ELVÉA° · ONE WORLD</div>'''
body+=card(550,270,0.3,'הסיפור','<div class="fill" data-seq="assets/seq/f_%03d.jpg" data-from="1" data-to="79" data-by="2" data-start="0.9" data-step="0.11"></div>')
body+=card(30,270,2.0,'השפה','<img class="kb" src="assets/fil-02.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 50%">')
body+=card(550,910,3.7,'האתר','<div class="abs" style="left:70px;top:36px;width:360px;height:640px;border-radius:34px 34px 0 0;overflow:hidden;border:8px solid #2E3526;border-bottom:0;background:#F0EADD"><div class="scr">'+site+'</div></div>','#DFE3CE')
body+=card(30,910,5.4,'החנות','<img class="kb" src="assets/boutique.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 50%">')
page('04-brand-world.html',1920,D,'''
@keyframes kb{0%{transform:scale(1.02)}100%{transform:scale(1.14)}}
@keyframes scr{0%,44%{transform:translateY(0)}54%,62%{transform:translateY(-25%)}72%,80%{transform:translateY(-50%)}90%,100%{transform:translateY(-75%)}}
.kb{animation-name:kb}.scr{animation-name:scr;animation-timing-function:ease-in-out}''',body)

# 05 — end card
D=5
page('05-end-card.html',1920,D,'''
@keyframes line{0%,24%{transform:scaleX(0)}60%,100%{transform:scaleX(1)}}
@keyframes ball{0%,24%{transform:translateX(760px)}60%,100%{transform:none}}''',
'''<div class="fill" style="background:var(--s-bg)"></div>
<div class="abs" dir="ltr" style="left:0;right:0;top:96px;text-align:center;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:50px;color:#3A342C">Brand Worlds Studio</div>
<div class="abs" style="left:320px;top:190px;width:440px;height:530px;border-radius:220px 220px 26px 26px;overflow:hidden;box-shadow:0 18px 40px rgba(70,60,40,.18)"><img src="assets/hagit.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%"></div>
<div class="abs" style="left:0;right:0;top:748px;text-align:center;font-size:27px;letter-spacing:.12em;color:#8B7B6E">חגית אנטבי · בונה עולמות מותג</div>
<div class="abs" data-in="0.3" style="left:60px;right:60px;top:836px;text-align:center;font-size:82px;font-weight:600;line-height:1.18;color:var(--s-ink)">ההבדל בין לעצב מוצר<br>לבין <span style="color:var(--s-copper)">לבנות מותג.</span></div>
<div class="abs" style="left:150px;width:780px;top:1099px;height:3px;background:var(--s-copper);transform-origin:100% 50%;animation-name:line"></div>
<div class="abs" style="left:108px;top:1058px;width:84px;height:84px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#E9B08F,#C4765A 55%,#8E4E36);box-shadow:0 0 0 8px rgba(255,255,255,.75),0 10px 24px rgba(120,70,40,.35);animation-name:ball"><div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:'Cormorant Garamond',serif;font-size:24px;color:#F5DEC4" dir="ltr">BW</div></div>
<div class="abs" data-in="1.6" style="left:0;right:0;top:1186px;text-align:center;font-size:42px;line-height:1.4;color:var(--s-copper)">המוצר שלך כבר שם.<br>רוצה לדעת מה חסר סביבו?</div>
<div class="abs" data-in="2.2" style="left:240px;width:600px;top:1372px;padding:26px 0;border-radius:12px;background:var(--s-ink);color:var(--s-bg);text-align:center"><div style="font-size:44px;font-weight:600">אבחון פער המותג</div><div style="font-size:27px;opacity:.85;margin-top:4px">30 דק׳ · בלי עלות</div></div>
<div class="abs" dir="ltr" style="left:0;right:0;top:1566px;text-align:center;font-family:'Plus Jakarta Sans',sans-serif;font-size:25px;letter-spacing:.3em;color:#8B7355">HAGITANTEBI.CO.IL</div>''')

# overlay — top pills on transparent background (PNG)
page('overlay-top-pills.html',1920,1,'html,body{background:transparent!important}',PILLS)
print('ok')
