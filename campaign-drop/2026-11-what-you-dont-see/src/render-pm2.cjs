const { chromium } = require('playwright');
const path = require('path');
const dir = __dirname;
const mode = process.argv[2];
const TEST = [0, 2.5, 4.4, 5.3, 6.5, 7.3, 7.7, 8.2, 8.5, 9.2, 10.6, 11.5, 13, 13.8, 14.8, 17.5];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'pm2.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const el = await p.$('#st');
  if (mode === 'test') {
    for (let i = 0; i < TEST.length; i++) {
      await p.evaluate(t => window.seek(t), TEST[i]);
      await el.screenshot({ path: path.join(dir, 'testpm2', String(i).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 80 });
    }
  } else {
    const N = Math.round(18.2 * 30);
    for (let i = 0; i < N; i++) {
      await p.evaluate(t => window.seek(t), i / 30);
      await el.screenshot({ path: path.join(dir, 'outpm2', String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 92 });
    }
  }
  await b.close();
})();
