const { chromium } = require('playwright');
const path = require('path');
const dir = __dirname;
const mode = process.argv[2];
const TEST = [0, 2.5, 5.5, 8.4, 15.2, 17.2, 22.6, 23.2, 27, 29.2, 31.6, 34.6, 36.6, 37.8, 38.5, 40.5];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'reel-chasen.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const el = await p.$('#st');
  if (mode === 'test') {
    for (let i = 0; i < TEST.length; i++) {
      await p.evaluate(t => window.seek(t), TEST[i]);
      await el.screenshot({ path: path.join(dir, 'testc', String(i).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 80 });
    }
  } else {
    const N = Math.round(42.2 * 30);
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => window.seek(t), i / 30);
      await el.screenshot({ path: path.join(dir, 'outc', String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    }
  }
  await b.close();
})();
