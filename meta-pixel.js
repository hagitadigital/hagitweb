/* ============================================================
   meta-pixel.js — shared Meta Pixel for pages without an inline one
   ------------------------------------------------------------
   Include once in <head>:  <script src="/meta-pixel.js" defer></script>
   - PageView on load (live domain only, same guard as GA4).
   - "Lead" when lead-intake.js confirms a form submission.
   - "Contact" on WhatsApp link clicks.
   Pages that already carry an inline pixel + their own
   lead:intake:success listener (the LPs, index, worlds) must NOT
   include this file, or Lead would fire twice.
   ============================================================ */
(function () {
  "use strict";

  if (!/(^|\.)hagitantebi\.co\.il$/.test(location.hostname) || navigator.webdriver) return;

  !function (f, b, e, v, n, t, s) {
    if (f.fbq) return; n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = "2.0";
    n.queue = [];
  }(window, document);
  fbq("init", "1326960187891724");
  fbq("track", "PageView");

  var t = document.createElement("script");
  t.async = true;
  t.src = "https://connect.facebook.net/en_US/fbevents.js";
  document.head.appendChild(t);

  document.addEventListener("lead:intake:success", function (e) {
    var src = (e && e.detail && e.detail.source) || "form";
    fbq("track", "Lead", { content_name: src });
  });

  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest
      ? e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]')
      : null;
    if (a) fbq("track", "Contact");
  });
})();
