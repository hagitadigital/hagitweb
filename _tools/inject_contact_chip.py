# -*- coding: utf-8 -*-
"""
Injects the Brand Worlds Studio contact chip (direct WhatsApp → אבחון פער המותג)
into every brand-world page. Idempotent: re-running replaces the existing block.

    python _tools/inject_contact_chip.py          # inject/refresh
    python _tools/inject_contact_chip.py --remove # strip the block

The chip:
- fixed pill, bottom-left, cream/navy/copper studio palette, no dependency on the world's CSS
- appears after ~60% of a viewport of scroll, or after 7s, whichever first
- never shows under navigator.webdriver (reel recordings / QA bots) unless ?chip=1
- one action: wa.me/972528351676 with a prefilled message naming the world
- the existing ga4-wa-tracking click listener already logs it as whatsapp_click
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# path (relative to site root) -> world display name used in the WhatsApp message
WORLDS = {
    "arco/index.html": "ARCO°",
    "aurelle/index.html": "AURELLE",
    "basalt/index.html": "BASALT",
    "chasen/index.html": "CHASEN°",
    "elvea/index.html": "ELVÉA°",
    "etage/index.html": "ÉTAGE°",
    "lumera/index.html": "LUMÉRA",
    "maison/index.html": "Maison de l'Heure",
    "orbe/index.html": "ORBE",
    "orea/index.html": "ORÉA",
    "oreva/index.html": "ORÉVA°",
    "miel/index.html": "MIEL°",
    "encore/index.html": "ENCORE°",
    "pancakerie/index.html": "PANCAKERIE°",
    "regard/index.html": "REGARD°",
    "rosee/index.html": "ROSÉE°",
    "signe/index.html": "SIGNÉ°",
    "solara-wild/index.html": "SOLARA WILD",
    "sonair/index.html": "SONAIR°",
    "trame/index.html": "TRAME°",
    "vela-motion/index.html": "VELA MOTION",
    "velune/index.html": "VELUNE°",
    "aerea.html": "AERÉA",
    "crema.html": "Crema°",
    "ecru.html": "ÉCRU",
    "lusha.html": "LUSHA",
    "melte.html": "MELTÉ°",
    "petale.html": "Pétale°",
    "poppi.html": "POPPI",
    "soluna.html": "SOLUNA",
    "souffle.html": "SOUFFLÉ°",
}

START = "<!-- studio-contact-chip -->"
END = "<!-- /studio-contact-chip -->"

SNIPPET = START + r"""
<style>
#studioChip{position:fixed;left:max(18px,env(safe-area-inset-left));bottom:max(18px,env(safe-area-inset-bottom));z-index:2147483000;direction:rtl;
  display:inline-flex;align-items:center;gap:.55rem;padding:.62rem 1.05rem .62rem .9rem;border-radius:999px;
  background:#F2EBDC;color:#15202E;border:1px solid rgba(21,32,46,.14);box-shadow:0 10px 30px rgba(21,32,46,.18),0 1px 0 rgba(255,255,255,.6) inset;
  font:600 .86rem/1 'Heebo','Assistant',system-ui,-apple-system,'Segoe UI',Arial,sans-serif;letter-spacing:.01em;text-decoration:none;white-space:nowrap;
  opacity:0;transform:translateY(14px);pointer-events:none;transition:opacity .5s ease,transform .5s cubic-bezier(.2,.7,.2,1),border-color .25s,box-shadow .25s}
#studioChip.is-on{opacity:1;transform:none;pointer-events:auto}
#studioChip:hover,#studioChip:focus-visible{border-color:#C28A5A;box-shadow:0 14px 34px rgba(21,32,46,.22);transform:translateY(-2px);outline:none}
#studioChip .sc-dot{width:8px;height:8px;border-radius:50%;background:#C28A5A;box-shadow:0 0 0 0 rgba(194,138,90,.45);animation:scPulse 2.6s ease-out infinite}
#studioChip .sc-wa{width:17px;height:17px;flex:none;fill:#15202E}
#studioChip .sc-sub{font-weight:400;opacity:.72;margin-inline-start:.15rem}
@keyframes scPulse{0%{box-shadow:0 0 0 0 rgba(194,138,90,.45)}70%{box-shadow:0 0 0 9px rgba(194,138,90,0)}100%{box-shadow:0 0 0 0 rgba(194,138,90,0)}}
@media (max-width:560px){#studioChip{font-size:.8rem;padding:.58rem .95rem .58rem .8rem}#studioChip .sc-sub{display:none}}
@media (prefers-reduced-motion:reduce){#studioChip{transition:opacity .3s}#studioChip .sc-dot{animation:none}}
</style>
<a id="studioChip" data-world="__WORLD__" href="https://wa.me/972528351676" target="_blank" rel="noopener" aria-label="וואטסאפ ישיר לחגית, לאבחון פער המותג">
  <span class="sc-dot" aria-hidden="true"></span>
  <span>לאבחון פער המותג</span><span class="sc-sub">· חגית</span>
  <svg class="sc-wa" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 12 12 0 0 0 4.6 4c1.7.7 2.3.6 2.7.5a2.3 2.3 0 0 0 1.5-1.1 1.9 1.9 0 0 0 .1-1.1c0-.1-.2-.2-.4-.3z"/></svg>
</a>
<script>
(function(){
  var a=document.getElementById('studioChip');if(!a)return;
  var q=location.search;
  if(/[?&]chip=0/.test(q))return;
  if(navigator.webdriver&&!/[?&]chip=1/.test(q))return; /* recordings + QA bots never see it */
  var w=a.getAttribute('data-world')||'העולם';
  a.href='https://wa.me/972528351676?text='+encodeURIComponent('היי חגית, ראיתי את '+w+' ואשמח לאבחון פער המותג');
  var on=false;function show(){if(on)return;on=true;a.classList.add('is-on');window.removeEventListener('scroll',chk)}
  function chk(){if((window.scrollY||document.documentElement.scrollTop||0)>window.innerHeight*0.6)show()}
  window.addEventListener('scroll',chk,{passive:true});
  /* some worlds scroll inside a container, not the window */
  document.addEventListener('scroll',function(e){if(e.target&&e.target!==document&&e.target.scrollTop>window.innerHeight*0.6)show()},true);
  setTimeout(show,7000);
  if(/[?&]chip=1/.test(q))show();
})();
</script>
""" + END + "\n"

GA4_BLOCK = r"""<!-- GA4 + WhatsApp click tracking (ga4-wa-tracking) -->
  <script>
  (function(){
    if (!/(^|\.)hagitantebi\.co\.il$/.test(location.hostname) || navigator.webdriver) return; /* ga4-live-guard */
    if (typeof window.gtag !== 'function') {
      var s=document.createElement('script');s.async=true;
      s.src='https://www.googletagmanager.com/gtag/js?id=G-30WB1J2R2T';
      document.head.appendChild(s);
      window.dataLayer=window.dataLayer||[];
      window.gtag=function(){dataLayer.push(arguments);};
      gtag('js',new Date());
      gtag('config','G-30WB1J2R2T');
    }
    document.addEventListener('click',function(e){
      var t=e.target instanceof Element?e.target:null;
      var a=t&&t.closest?t.closest('a[href*="wa.me"],a[href*="api.whatsapp.com"]'):null;
      if(a)gtag('event','whatsapp_click',{link_url:a.href,page_path:location.pathname});
    },true);
  })();
  </script>
"""

BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"\n?", re.S)


def process(rel, world, remove=False):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return "MISSING"
    with io.open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html
    html = BLOCK_RE.sub("", html)
    note = ""
    if not remove:
        if "ga4-wa-tracking" not in html:
            html = html.replace("</body>", GA4_BLOCK + "</body>", 1)
            note = " +ga4"
        block = SNIPPET.replace("__WORLD__", world)
        if "</body>" not in html:
            return "NO </body>"
        html = html.replace("</body>", block + "</body>", 1)
    if html != orig:
        with io.open(path, "w", encoding="utf-8", newline="") as f:
            f.write(html)
        return ("removed" if remove else "injected") + note
    return "unchanged"


if __name__ == "__main__":
    remove = "--remove" in sys.argv
    for rel, world in WORLDS.items():
        print("%-24s %s" % (rel, process(rel, world, remove)))
