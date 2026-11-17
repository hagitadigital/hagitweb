// Record the PARDON ME site: the window opening on scroll, and the sleeve being torn.
const { chromium } = require('playwright');
const path = require('path');
const out = path.join(__dirname, 'pm');
const pad = n => String(n).padStart(3, '0');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  let p = await ctx.newPage();
  await p.goto('http://localhost:8765/pardon-me/', { waitUntil: 'load' });
  await p.waitForTimeout(2500);
  const r = await p.evaluate(() => { const e = document.getElementById('peek'); return [e.getBoundingClientRect().top + scrollY, e.offsetHeight - innerHeight]; });
  for (let i = 0; i < 80; i++) {
    await p.evaluate(y => scrollTo(0, y), r[0] + r[1] * (i / 79));
    await p.waitForTimeout(120);
    await p.screenshot({ path: path.join(out, 'peek', pad(i) + '.jpg'), type: 'jpeg', quality: 90 });
  }
  await p.close();
  p = await ctx.newPage();
  await p.goto('http://localhost:8765/pardon-me/', { waitUntil: 'load' });
  await p.waitForTimeout(2000);
  await p.evaluate(() => document.getElementById('interrupt').scrollIntoView());
  await p.waitForTimeout(1500);
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('Animation.enable');
  await cdp.send('Animation.setPlaybackRate', { playbackRate: 0.12 });
  for (let i = 0; i < 6; i++) await p.screenshot({ path: path.join(out, 'tear', pad(i) + '.jpg'), type: 'jpeg', quality: 90 });
  await p.evaluate(() => document.getElementById('tear').click());
  for (let i = 6; i < 80; i++) {
    await p.screenshot({ path: path.join(out, 'tear', pad(i) + '.jpg'), type: 'jpeg', quality: 90 });
    await p.waitForTimeout(60);
  }
  await b.close();
})();
