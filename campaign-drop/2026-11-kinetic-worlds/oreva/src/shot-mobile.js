// First screen of oreva/index.html on a phone (390×844 @3x) + where its headline, reason and buttons sit.
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true });
  await p.goto('file://' + path.resolve(__dirname, '../../../../oreva/index.html'), { waitUntil: 'load' }); await p.waitForTimeout(3000);
  await p.screenshot({ path: path.join(__dirname, 'oreva-mobile.jpg'), type: 'jpeg', quality: 90 });
  const r = await p.evaluate(() => { const q = s => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; };
    const h = document.querySelector('#hero'); const ps = [...h.querySelectorAll('p')].map(e => [e.className, e.innerText.slice(0, 50), Math.round(e.getBoundingClientRect().top), Math.round(e.getBoundingClientRect().height)]);
    const as = [...h.querySelectorAll('a,button')].map(e => { const r = e.getBoundingClientRect(); return [e.innerText.trim(), Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)]; });
    return { h1: q('#hero h1'), ps, as, img: [...h.querySelectorAll('img')].map(i => i.getAttribute('src')) }; });
  console.log(JSON.stringify(r)); await b.close(); })();
