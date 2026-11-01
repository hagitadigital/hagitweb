"""The three worlds. Copy quotes the sites and brand books; nothing new is promised about a world."""
from gen import CH, kb_img, browser, feed, COPPER, INK_SOFT, DISPLAY, LABEL

SEQ = lambda folder, names: [f'{folder}/{n}' for n in names]


def draw(fm, a, b):
    return fm.kf([(a, 'stroke-dashoffset:1'), (b, 'stroke-dashoffset:0')], 'cubic-bezier(.45,.05,.35,1)')


def pop(fm, t, d=.35):
    return fm.kf([(t, 'opacity:0;transform:scale(.6)'), (t + d, 'opacity:1;transform:scale(1)')])


def fade(fm, t, d=.4):
    return fm.kf([(t, 'opacity:0'), (t + d, 'opacity:1')])


def captions(fm, items, color, t0, dt=.45, font=24):
    spans = ''.join(f'<span style="{fade(fm, t0 + i * dt)}">{s}</span>' for i, s in enumerate(items))
    return (f'<div dir="rtl" style="position:absolute;left:40px;right:40px;bottom:46px;display:flex;justify-content:center;gap:44px;'
            f'font-size:{font}px;letter-spacing:.06em;color:{color}">{spans}</div>')


def chapter(fm, i, inner, bg='transparent'):
    a, b = CH[i]
    return f'<div style="position:absolute;inset:0;background:{bg};{fm.show(a, b)}">{inner}</div>'


# ───────────────────────── ORÉVA° ─────────────────────────
def oreva(A):
    bloom = A.seq(SEQ('oreva/assets/bloom', [f'f{i:02d}.webp' for i in range(1, 49)]), 'bloom')
    cut = {k: A.img(f'oreva/assets/{k}.webp', maxw=700, trim=True) for k in ['p-calm', 'p-dew', 'p-glow', 'p-dew-essence', 'p-eye-veil']}
    im = {k: A.img(f'oreva/assets/{k}.webp') for k in ['packaging-set-ribbon', 'founder-opening-kit-box', 'studio-interior-reception',
                                                      'founder-client-bottle', 'texture-three-swatches', 'skin-face-closeup-drop',
                                                      'hero-glow-serum-splash', 'founder-cream-on-hand']}
    im['journal'] = A.img('oreva/journal-des-mains.webp')
    generic = A.img('images/bw-lp/generic-serum.jpg')
    CU, CU_DEEP = '#B87A57', '#8F5A3C'

    def scenes(fm, A):
        out = []
        # 01 · the symbol: one copper ribbon from the hand to the bottle, a bead at its end
        a, b = CH[0]
        path = 'M70,500 C170,505 165,372 262,352 S420,410 436,300 S372,168 470,118'
        svg = (f'<svg viewBox="0 0 600 600" width="720" height="720" style="position:absolute;top:70px;left:116px" aria-hidden="true">'
               f'<path d="{path}" fill="none" stroke="{CU}" stroke-width="7" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" style="{draw(fm, a + .25, a + 2.0)}"/>'
               f'<path d="{path}" transform="translate(9,-11)" fill="none" stroke="{CU}" stroke-opacity=".45" stroke-width="2.5" stroke-linecap="round" pathLength="1" stroke-dasharray="1 1" style="{draw(fm, a + .45, a + 2.2)}"/>'
               f'<g style="transform-origin:470px 118px;{pop(fm, a + 2.05)}"><circle cx="470" cy="118" r="26" fill="#EFCDBF"/><circle cx="470" cy="118" r="15" fill="{CU}"/></g></svg>')
        out.append(chapter(fm, 0, svg + captions(fm, ['יד · ההתחלה', 'סרט · הקו', 'חרוז · הבקבוק'], '#6E4A35', a + .8, .6), '#FBF7F1'))
        # 02 · the site
        out.append(browser(fm, None, bloom, CH[1][0] + .1, .066, 'hagitantebi.co.il/oreva'))
        # 03 · the products: one copper pump on every bottle, a copper ring walks the line (right to left)
        a, b = CH[2]
        row = [('p-eye-veil', 360, 806), ('p-dew-essence', 560, 640), ('p-glow', 640, 452), ('p-dew', 560, 270), ('p-calm', 560, 96)]
        bottles, xs = '', []
        for k, h, cx in row:
            bottles += f'<img src="{cut[k]}" alt="" style="position:absolute;bottom:170px;left:{cx}px;height:{h}px;transform:translateX(-50%)">'
            xs.append((cx, 830 - h + 46))
        floor = '<div style="position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(180deg,#E9DCCB,#DCC8B2)"></div>'
        steps = []
        for j, (cx, cy) in enumerate(xs):
            t = a + .35 + j * .55
            steps += [(t, f'transform:translate({cx - 70}px,{cy - 70}px)'), (t + .35, f'transform:translate({cx - 70}px,{cy - 70}px)')]
        ring = (f'<div style="position:absolute;top:0;left:0;width:140px;height:140px;{fm.kf(steps)}">'
                f'<div style="position:absolute;inset:0;border-radius:999px;border:4px solid {CU};box-shadow:0 0 0 10px rgba(239,205,191,.35)"></div></div>')
        out.append(chapter(fm, 2, floor + bottles + ring, 'linear-gradient(180deg,#F6EFE7,#EFE2D6)'))
        # 04 · packaging · 05 · the studio
        m = (CH[3][0] + CH[3][1]) / 2
        out.append(kb_img(fm, im['packaging-set-ribbon'], CH[3][0], m + .15, '45% 50%'))
        out.append(kb_img(fm, im['founder-opening-kit-box'], m, CH[3][1], '58% 50%'))
        m = (CH[4][0] + CH[4][1]) / 2
        out.append(kb_img(fm, im['studio-interior-reception'], CH[4][0], m + .15, '62% 50%'))
        out.append(kb_img(fm, im['founder-client-bottle'], m, CH[4][1], '50% 50%'))
        # 06 · the feed
        out.append(feed(fm, None, [im['journal'], im['texture-three-swatches'], im['skin-face-closeup-drop'],
                                   im['hero-glow-serum-splash'], im['founder-cream-on-hand']], CU))
        return out

    return dict(
        name='ORÉVA°', no='No.24', ghost='ORÉVA',
        color=dict(plane=CU_DEEP, text='#FBF7F1', card='#FBF7F1'),
        chapters=['הסמל', 'האתר', 'המוצרים', 'האריזה', 'הסטודיו', 'הפיד'],
        hook=dict(type='price', lines=['ועדיין שואלים אצלך', 'אם יש הנחה?'], hi='הנחה'),
        generic=dict(img=generic, name='סרום · 30 מ״ל', price='₪89', was='₪127'),
        texts=[('קו אחד. מהידיים אל הבקבוק.', 'סרט נחושת אחד, רציף, שמתחיל ביד ונגמר בבקבוק.'),
               ('קודם הידיים. אחר כך הבקבוק.', 'ההבטחה של ORÉVA°&lrm; היא המשפט הראשון באתר.'),
               ('אותה נחושת על כל משאבה.', 'זכוכית בגוון סומק, ראש נחושת. כל הליין נסגר באותה מתכת.'),
               ('הסרט עוטף גם את הקופסה.', 'אותו סרט נחושת, מהקופסה ועד הבקבוק שבתוכה.'),
               ('עולם שלם באותו סרט.', 'מהקבלה בסטודיו ועד הבקבוק שעובר מיד ליד, באותם צבעים.'),
               ('חמישה שקפים. סרט אחד רציף.', 'הקו ממשיך מהאתר אל המודעות.')],
        outro=dict(img=im['hero-glow-serum-splash'], pos='60% 50%', head=['את ORÉVA°&lrm; לא משווים.'], hi='בוחרים.',
                   sub='כשכל מוצר יוצא<br>מאותה החלטה.'),
        scenes=scenes)


# ───────────────────────── ENCORE° ─────────────────────────
NIGHT, DAWN, NOON, DUSK, STONE, GOLD = '#241212', '#6E4E4A', '#34405A', '#853A26', '#EFE8DD', '#D9B26A'
WEDGES = {  # centre 320,320 · r 256 · night always on top, clockwise: 00 · 06 · 12 · 18
    'night': 'M320,320 L139,139 A256,256 0 0 1 501,139 Z', 'dawn': 'M320,320 L501,139 A256,256 0 0 1 501,501 Z',
    'noon': 'M320,320 L501,501 A256,256 0 0 1 139,501 Z', 'dusk': 'M320,320 L139,501 A256,256 0 0 1 139,139 Z'}
WCOL = dict(night=NIGHT, dawn=DAWN, noon=NOON, dusk=DUSK)


def encore(A):
    land = A.seq(SEQ('encore/assets/hero/land', [f'l{i:02d}.webp' for i in range(1, 73, 2)]), 'land')
    tp = {k: A.img(f'encore/assets/touchpoints/{k}.webp') for k in ['sign', 'tag-cuff', 'box-open', 'bags-four', 'bag-street']}
    pieces = {k: A.img(f'encore/assets/pieces/{v}.webp', maxw=500, trim=True)
              for k, v in dict(night='earrings-4', dawn='rings-1', noon='pendants-2', dusk='bracelets-1').items()}
    extra = {'premiere': A.img('encore/premiere-heure.webp'), 'landed': A.img('encore/assets/hero/landed.webp'),
             'float': A.img('encore/assets/hero/float-poster.jpg', 'float-poster.webp')}

    def dial(fm, t_ring, t_x, t_fill, size, base_op=0.0, ticks=True, labels=True):
        ring = (f'<circle cx="320" cy="320" r="262" fill="none" stroke="{GOLD}" stroke-width="3.5" pathLength="1" stroke-dasharray="1 1" '
                f'transform="rotate(-90 320 320)" style="{draw(fm, t_ring, t_ring + 1.0)}"/>')
        tk = ''
        if ticks:
            import math
            for i in range(24):
                an = i / 24 * 2 * math.pi
                r0, r1 = (240, 252) if i % 6 else (226, 252)
                tk += f'<line x1="{320 + r0 * math.sin(an):.1f}" y1="{320 - r0 * math.cos(an):.1f}" x2="{320 + r1 * math.sin(an):.1f}" y2="{320 - r1 * math.cos(an):.1f}"/>'
            tk = f'<g stroke="{GOLD}" stroke-width="2" style="{fade(fm, t_ring + .8)}">{tk}</g>'
        wedges = ''.join(f'<path d="{WEDGES[k]}" fill="{WCOL[k]}" style="{fm.kf([(t_fill[j], f"opacity:{base_op}"), (t_fill[j] + .3, "opacity:1")])}"/>'
                         for j, k in enumerate(['night', 'dawn', 'noon', 'dusk']))
        xs = (f'<path d="M139,139 L501,501 M501,139 L139,501" stroke="{GOLD}" stroke-width="3" fill="none" pathLength="1" stroke-dasharray="1 1" '
              f'style="{draw(fm, t_x, t_x + .5)}"/>')
        lab = ''
        if labels:
            for j, (k, x, y, txt) in enumerate([('night', 320, 30, '00:00'), ('dawn', 616, 328, '06:00'), ('noon', 320, 628, '12:00'), ('dusk', 24, 328, '18:00')]):
                lab += f'<text x="{x}" y="{y}" text-anchor="middle" style="{fade(fm, t_fill[j])}">{txt}</text>'
            lab = f'<g font-family="Plus Jakarta Sans" font-size="22" letter-spacing="3" fill="#7A5A2A">{lab}</g>'
        return (f'<svg viewBox="-20 -20 680 680" width="{size}" height="{size}" style="position:absolute;top:50%;left:50%;'
                f'transform:translate(-50%,-50%);overflow:visible" aria-hidden="true">{wedges}{xs}{ring}{tk}{lab}</svg>')

    def scenes(fm, A):
        out = []
        a, b = CH[0]
        sym = dial(fm, a + .2, a + 1.1, [a + 1.5, a + 1.85, a + 2.2, a + 2.55], 720)
        out.append(chapter(fm, 0, f'<div style="position:absolute;inset:0;top:-40px">{sym}</div>'
                           + captions(fm, ['לילה', 'שחר', 'צהריים', 'שקיעה'], '#7A5A2A', a + 1.5, .35), STONE))
        out.append(browser(fm, None, land, CH[1][0] + .1, .088, 'hagitantebi.co.il/encore'))
        # 03 · every piece belongs to an hour: the dial lights one quarter at a time, its piece lands inside
        a, b = CH[2]
        ts = [a + .4, a + 1.05, a + 1.7, a + 2.35]
        big = dial(fm, a - 1, a - 1, ts, 860, base_op=.28, ticks=True, labels=False)
        spots = dict(night=(476, 250, 150), dawn=(690, 500, 180), noon=(476, 720, 300), dusk=(262, 500, 160))
        pcs = ''.join(f'<img src="{pieces[k]}" alt="" style="position:absolute;left:{x}px;top:{y}px;height:{h}px;transform:translate(-50%,-50%);'
                      f'filter:drop-shadow(0 10px 18px rgba(0,0,0,.35));{fm.kf([(ts[j] + .1, "opacity:0;margin-top:-40px"), (ts[j] + .45, "opacity:1;margin-top:0")])}">'
                      for j, (k, (x, y, h)) in enumerate(spots.items()))
        out.append(chapter(fm, 2, big + pcs, STONE))
        m = (CH[3][0] + CH[3][1]) / 2
        out.append(kb_img(fm, tp['box-open'], CH[3][0], m + .15, '50% 40%'))
        out.append(kb_img(fm, tp['tag-cuff'], m, CH[3][1], '50% 50%'))
        m = (CH[4][0] + CH[4][1]) / 2
        out.append(kb_img(fm, tp['sign'], CH[4][0], m + .15, '50% 30%'))
        out.append(kb_img(fm, tp['bags-four'], m, CH[4][1], '50% 50%'))
        out.append(feed(fm, None, [extra['premiere'], extra['landed'], tp['bag-street'], extra['float'], tp['bags-four']], GOLD))
        return out

    return dict(
        name='ENCORE°', no='No.28', ghost='ENCORE',
        color=dict(plane=DAWN, text='#F6EEE4', card=STONE),
        chapters=['הסמל', 'האתר', 'התכשיטים', 'האריזה', 'החנות', 'הפיד'],
        hook=dict(type='logo', lines=['אם נסתיר את הלוגו,', 'עדיין יזהו אותך?'], hi='יזהו אותך'),
        hidden=dict(img=tp['bag-street'], pos='50% 50%', origin='50% 62%', bar='top:1150px;left:470px;width:312px;height:66px'),
        texts=[('יום אחד. ארבע שעות.', 'החוגה מחזיקה את כל המותג. הלילה תמיד למעלה.'),
               ('האתר נפתח בתכשיט שנוחת.', 'תליון אחד יורד אל הצוואר. תכשיט שלא יורד.'),
               ('לכל תכשיט יש שעה.', 'טבעות לשחר, שרשראות לצהריים, צמידים לשקיעה, עגילים ללילה.'),
               ('החוגה נסגרת גם על הקופסה.', 'כל שעה בתא שלה.'),
               ('השלט והשקית. אותה חוגה.', 'ארבעה צבעים של יום אחד, בכל מקום שפוגשים את ENCORE°&lrm;.'),
               ('חמישה שקפים. קו זהב אחד.', 'זהב רק כקו, אף פעם לא כמילוי.')],
        outro=dict(logo=True, head=['יזהו אותך.'], sub='כשהחלטה אחת חוזרת<br>בכל מקום שפוגשים אותך.'),
        scenes=scenes)


# ───────────────────────── MIEL° ─────────────────────────
def miel(A):
    coupe = A.video_seq('miel/assets/coupe.mp4', 'coupe', 8)
    im = {k: A.img(f'miel/assets/{k}.webp') for k in ['02-maison-giftbox', '04-maison-cake-in-box', '03-maison-storefront', '01-maison-counter',
                                                     '08-still-slice-pink-topper', '15-still-macarons', '16-still-cupcakes', 'sig-rose',
                                                     '41-slice-vanille-framboise']}
    cut = {k: A.img(f'miel/assets/{k}.webp', maxw=800, trim=True) for k in ['22-base-vanille', '25-fill-framboise', '27-shell-rose', '32-top-mix']}
    generic = A.img('images/bw-lp/generic-cake.jpg')
    ROSE, CACAO, OR = '#C98989', '#4A2C24', '#B8956A'

    def scenes(fm, A):
        out = []
        # 01 · the symbol: the slice. layer · heart · layer · heart · layer
        a, b = CH[0]
        L = lambda d, t0, t1, w=4: (f'<path d="{d}" fill="none" stroke="{ROSE}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round" '
                                    f'pathLength="1" stroke-dasharray="1 1" style="{draw(fm, t0, t1)}"/>')
        band = lambda y, t: f'<rect x="112" y="{y}" width="376" height="44" fill="{ROSE}" style="{fm.kf([(t, "opacity:0"), (t + .35, "opacity:.42")])}"/>'
        heart = (f'<path d="M300,357 c-14,-16 -36,-6 -30,10 c4,10 18,18 30,26 c12,-8 26,-16 30,-26 c6,-16 -16,-26 -30,-10z" fill="{ROSE}" '
                 f'style="transform-origin:300px 372px;{pop(fm, a + 2.25)}"/>')
        svg = (f'<svg viewBox="0 0 600 600" width="720" height="720" style="position:absolute;top:60px;left:116px" aria-hidden="true">'
               f'{band(258, a + 1.5)}{band(350, a + 1.8)}'
               + L('M110,210 L462,112 L490,210 M462,112 L462,350 L490,446', a + .2, a + .9)
               + L('M110,210 L110,446 L490,446 L490,210 Z', a + .5, a + 1.4)
               + L('M110,258 H490 M110,302 H490 M110,350 H490 M110,394 H490', a + 1.0, a + 1.6, 3)
               + heart + '</svg>')
        out.append(chapter(fm, 0, svg + captions(fm, ['שכבה', 'לב', 'שכבה', 'לב', 'שכבה'], '#8A4E4E', a + .9, .3), '#F6EADF'))
        out.append(browser(fm, None, coupe, CH[1][0] + .1, .08, 'hagitantebi.co.il/miel', '40% 50%'))
        # 03 · the cake builds from the inside out
        a, b = CH[2]
        lay = [('22-base-vanille', 600, 600, a + .2), ('25-fill-framboise', 590, 545, a + .65), ('22-base-vanille', 600, 490, a + 1.1)]
        stack = ''
        for k, wdt, top, t in lay:
            stack += (f'<img src="{cut[k]}" alt="" style="position:absolute;left:50%;top:{top}px;width:{wdt}px;margin-left:-{wdt // 2}px;'
                      f'{fm.kf([(t, "opacity:0;transform:translateY(-160px)"), (t + .4, "opacity:1;transform:none")], "cubic-bezier(.3,.7,.4,1)")}">')
        shell = (f'<img src="{cut["27-shell-rose"]}" alt="" style="position:absolute;left:50%;top:330px;width:640px;margin-left:-320px;'
                 f'{fm.kf([(a + 1.6, "opacity:0;transform:translateY(-120px)"), (a + 2.0, "opacity:1;transform:none")], "cubic-bezier(.3,.7,.4,1)")}">')
        top = (f'<img src="{cut["32-top-mix"]}" alt="" style="position:absolute;left:50%;top:150px;width:560px;margin-left:-280px;'
               f'{fm.kf([(a + 2.2, "opacity:0;transform:translateY(-120px)"), (a + 2.6, "opacity:1;transform:none")], "cubic-bezier(.3,.7,.4,1)")}">')
        stand = f'<div style="position:absolute;left:50%;top:930px;width:700px;height:26px;margin-left:-350px;border-radius:999px;background:rgba(74,44,36,.12)"></div>'
        out.append(chapter(fm, 2, stand + stack + shell + top, 'linear-gradient(180deg,#F6EADF,#F3E4DF)'))
        m = (CH[3][0] + CH[3][1]) / 2
        out.append(kb_img(fm, im['02-maison-giftbox'], CH[3][0], m + .15, '50% 50%'))
        out.append(kb_img(fm, im['04-maison-cake-in-box'], m, CH[3][1], '40% 50%'))
        m = (CH[4][0] + CH[4][1]) / 2
        out.append(kb_img(fm, im['03-maison-storefront'], CH[4][0], m + .15, '50% 50%'))
        out.append(kb_img(fm, im['01-maison-counter'], m, CH[4][1], '40% 50%'))
        out.append(feed(fm, None, [im['08-still-slice-pink-topper'], im['15-still-macarons'], im['16-still-cupcakes'],
                                   im['sig-rose'], im['41-slice-vanille-framboise']], ROSE))
        return out

    return dict(
        name='MIEL°', no='No.27', ghost='MIEL',
        color=dict(plane=CACAO, text='#F6EADF', card='#F6EADF'),
        chapters=['הסמל', 'האתר', 'העוגות', 'האריזה', 'הבוטיק', 'הפיד'],
        hook=dict(type='price', lines=['למה תמיד משווים', 'אותך במחיר?'], hi='במחיר'),
        generic=dict(img=generic, name='עוגה · 8 מנות', price='₪189', was='₪270'),
        texts=[('שכבה. לב. שכבה.', 'הסמל של MIEL°&lrm; הוא מה שיש בפנים: הפרוסה.'),
               ('האתר נפתח בחיתוך.', 'רומנטיקה מתחילה מבפנים. הסכין חותכת, והשכבות נגלות.'),
               ('העוגה נבנית מבפנים החוצה.', 'בסיס, מילוי, ציפוי וכתר. אף שכבה לא מתחבאת.'),
               ('העוגה יוצאת בקופסה. עם סרט.', 'קופסה לבנה, סרט ורוד, והשם שלה על הכרטיס.'),
               ('מקום שמריח כמו יום הולדת.', 'החלון, הוויטרינה והדלפק. אותו ורוד ואותו זהב.'),
               ('חמש פרוסות. רומנטיקה אחת.', 'כל שקף נפתח מבפנים, כמו העוגה.')],
        outro=dict(img=im['sig-rose'], pos='50% 70%', head=['את MIEL°&lrm; לא משווים.'], hi='בוחרים.',
                   sub='כשהעולם מתחיל<br>מבפנים.'),
        scenes=scenes)


WORLDS = dict(oreva=oreva, encore=encore, miel=miel)
