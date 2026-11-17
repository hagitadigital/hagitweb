const { chromium } = require('playwright');
const path = require('path');
const dir = __dirname;
const mode = process.argv[2];
const TEST = [0, 2.5, 3.95, 4.1, 5.5, 6.8, 7.8, 8.3, 9.6, 10.8, 12, 13, 13.9, 14.6, 15.3, 17.5];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'pm.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const el = await p.$('#st');
  if (mode === 'test') {
    for (let i = 0; i < TEST.length; i++) {
      await p.evaluate(t => window.seek(t), TEST[i]);
      await el.screenshot({ path: path.join(dir, 'testpm', String(i).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 80 });
    }
  } else {
    const N = Math.round(18.2 * 30);
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => window.seek(t), i / 30);
      await el.screenshot({ path: path.join(dir, 'outpm', String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    }
  }
  await b.close();
})();
