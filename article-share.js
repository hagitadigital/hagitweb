/*
 * article-share.js — Brand Worlds Studio
 * Self-contained share bar for article pages. No backend, no tracking.
 * Usage: add  <script src="/article-share.js" defer></script>  before </body>.
 * It auto-inserts a share bar before the .read-more section (or before the footer),
 * reading the page's own title + canonical URL. Native share on mobile, explicit
 * buttons + copy-link everywhere.
 */
(function () {
  'use strict';

  function init() {
    // Avoid double-insert
    if (document.querySelector('.bws-share')) return;

    var url =
      (document.querySelector('link[rel="canonical"]') || {}).href ||
      (document.querySelector('meta[property="og:url"]') || {}).content ||
      window.location.href;

    var title =
      (document.querySelector('meta[property="og:title"]') || {}).content ||
      document.title ||
      'מאמר';

    var encUrl = encodeURIComponent(url);
    var encTitle = encodeURIComponent(title);
    var encShare = encodeURIComponent(title + ' — ' + url);

    // ---- styles (injected once) ----
    var css = '\
.bws-share{max-width:760px;margin:0 auto;padding:36px clamp(24px,5vw,48px);\
  border-top:1px solid rgba(139,115,85,0.15);text-align:center}\
.bws-share__label{font-family:"Plus Jakarta Sans",sans-serif;font-size:0.65rem;\
  font-weight:600;letter-spacing:0.3em;text-transform:uppercase;color:#C4765A;\
  margin-bottom:18px}\
.bws-share__row{display:flex;justify-content:center;align-items:center;\
  gap:12px;flex-wrap:wrap}\
.bws-share__btn{width:44px;height:44px;border-radius:50%;display:inline-flex;\
  align-items:center;justify-content:center;background:#F5F1E8;color:#8B7355;\
  border:1px solid rgba(139,115,85,0.12);cursor:pointer;text-decoration:none;\
  transition:background .25s cubic-bezier(.4,0,.2,1),color .25s,transform .25s;\
  padding:0}\
.bws-share__btn:hover{background:#C4765A;color:#FAF8F3;transform:translateY(-2px);\
  border-color:#C4765A}\
.bws-share__btn svg{width:19px;height:19px;display:block}\
.bws-share__toast{font-family:"Heebo",sans-serif;font-size:0.8rem;color:#C4765A;\
  margin-top:14px;min-height:18px;opacity:0;transition:opacity .3s}\
.bws-share__toast.is-on{opacity:1}';
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    // ---- icons ----
    var ic = {
      native: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.6" y1="13.5" x2="15.4" y2="17.5"/><line x1="15.4" y1="6.5" x2="8.6" y2="10.5"/></svg>',
      whatsapp: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.5 14.4c-.3-.15-1.7-.84-1.96-.94-.26-.1-.45-.15-.64.15-.19.28-.74.94-.9 1.13-.17.19-.33.21-.61.07-.3-.15-1.24-.46-2.36-1.46-.87-.78-1.46-1.73-1.63-2.02-.17-.29-.02-.45.13-.6.13-.13.29-.34.44-.51.15-.17.19-.29.29-.48.1-.19.05-.36-.02-.51-.08-.15-.64-1.55-.88-2.12-.23-.55-.47-.48-.64-.49-.17-.01-.36-.01-.55-.01-.19 0-.5.07-.76.36-.26.29-1 .98-1 2.38s1.02 2.76 1.17 2.95c.15.19 2.02 3.08 4.9 4.32.69.3 1.22.47 1.64.6.69.22 1.32.19 1.81.12.55-.08 1.7-.69 1.94-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.19-.55-.34z"/><path d="M12.04 2.01c-5.52 0-10 4.48-10 10 0 1.76.46 3.48 1.34 5L2 22.01l5.13-1.35a9.96 9.96 0 0 0 4.9 1.25c5.52 0 10-4.48 10-10s-4.48-9.9-10-9.9zm0 18.18c-1.5 0-2.97-.4-4.25-1.16l-.3-.18-3.04.8.81-2.97-.2-.31a8.27 8.27 0 0 1-1.27-4.41c0-4.58 3.73-8.31 8.32-8.31 2.22 0 4.31.87 5.88 2.44a8.25 8.25 0 0 1 2.43 5.88c0 4.58-3.73 8.31-8.31 8.31z"/></svg>',
      linkedin: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5A2.5 2.5 0 1 0 5 8.5a2.5 2.5 0 0 0-.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-.95 1.83-1.95 3.77-1.95 4.03 0 4.78 2.5 4.78 5.75V21h-4v-5.3c0-1.26-.02-2.9-1.77-2.9-1.77 0-2.04 1.38-2.04 2.8V21H9z"/></svg>',
      facebook: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.78-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.44 2.89h-2.34v6.99A10 10 0 0 0 22 12z"/></svg>',
      copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'
    };

    function btn(href, label, svg, extra) {
      var a = document.createElement(href ? 'a' : 'button');
      a.className = 'bws-share__btn';
      a.setAttribute('aria-label', label);
      a.setAttribute('title', label);
      a.innerHTML = svg;
      if (href) {
        a.href = href;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
      } else {
        a.type = 'button';
      }
      if (extra) extra(a);
      return a;
    }

    // ---- build ----
    var wrap = document.createElement('section');
    wrap.className = 'bws-share';
    var label = document.createElement('div');
    label.className = 'bws-share__label';
    label.textContent = 'שיתוף המאמר';
    var row = document.createElement('div');
    row.className = 'bws-share__row';
    var toast = document.createElement('div');
    toast.className = 'bws-share__toast';
    toast.setAttribute('aria-live', 'polite');

    // Native share (mobile) — first, when supported
    if (navigator.share) {
      row.appendChild(btn(null, 'שיתוף', ic.native, function (el) {
        el.addEventListener('click', function () {
          navigator.share({ title: title, url: url }).catch(function () {});
        });
      }));
    }

    row.appendChild(btn('https://api.whatsapp.com/send?text=' + encShare, 'שיתוף בוואטסאפ', ic.whatsapp));
    row.appendChild(btn('https://www.linkedin.com/sharing/share-offsite/?url=' + encUrl, 'שיתוף בלינקדאין', ic.linkedin));
    row.appendChild(btn('https://www.facebook.com/sharer/sharer.php?u=' + encUrl, 'שיתוף בפייסבוק', ic.facebook));

    // Copy link
    row.appendChild(btn(null, 'העתקת קישור', ic.copy, function (el) {
      el.addEventListener('click', function () {
        var done = function () {
          toast.textContent = 'הקישור הועתק ✦';
          toast.classList.add('is-on');
          setTimeout(function () { toast.classList.remove('is-on'); }, 2200);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(done, function () { fallbackCopy(url, done); });
        } else {
          fallbackCopy(url, done);
        }
      });
    }));

    wrap.appendChild(label);
    wrap.appendChild(row);
    wrap.appendChild(toast);

    // ---- insert: before .read-more, else before footer, else end of body ----
    var anchor = document.querySelector('.read-more') || document.querySelector('.footer');
    if (anchor && anchor.parentNode) {
      anchor.parentNode.insertBefore(wrap, anchor);
    } else {
      document.body.appendChild(wrap);
    }
  }

  function fallbackCopy(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
