// Records the real SOLUNA shop flow frame by frame on a controlled clock (deterministic), 1080x1920.
// usage: node record-shop.js <site-url> <out-dir>
const { chromium } = require('playwright'); const fs = require('fs');
const [,, URL_, OUT] = process.argv;
const STEP = 40, END = 9800;                                   // site ms per video frame (1.2x), total site ms
const EVENTS = [[600, '.mark[aria-label^="רוגע"]'], [4600, '#lemon'], [6900, '#add'], [7900, '#bagBtn']];
(async () => {
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  await p.clock.install({ time: new Date('2026-11-26T10:30:00') });
  await p.goto(URL_, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  const tick = async ms => {
    await p.clock.runFor(ms);
    await p.evaluate(ms => { const S = window.__an || (window.__an = new Map());
      for (const a of document.getAnimations()) { if (!S.has(a)) { a.pause(); S.set(a, 0); }
        const t = S.get(a) + ms; S.set(a, t);
        const end = a.effect.getComputedTiming().endTime;
        if (t >= end && isFinite(end)) { try { a.finish(); } catch (e) {} } else a.currentTime = t; } }, ms);
  };
  for (let i = 0; i < 40; i++) await tick(50);
  await p.click('#enter'); for (let i = 0; i < 60; i++) await tick(50);
  const log = []; let ei = 0, n = 0;
  for (let t = 0; t <= END; t += STEP) {
    if (ei < EVENTS.length && t >= EVENTS[ei][0]) {
      const l = p.locator(EVENTS[ei][1]).first(); const bb = await l.boundingBox();
      log.push({ frame: n, sel: EVENTS[ei][1], x: (bb.x + bb.width / 2) * 3, y: (bb.y + bb.height / 2) * 3 });
      await l.click({ force: true }); ei++;
    }
    await tick(STEP);
    fs.writeFileSync(`${OUT}/s_${String(n++).padStart(3, '0')}.jpg`, await p.screenshot({ type: 'jpeg', quality: 90 }));
  }
  fs.writeFileSync(`${OUT}/events.json`, JSON.stringify(log)); console.log(n, JSON.stringify(log));
  await b.close();
})();
