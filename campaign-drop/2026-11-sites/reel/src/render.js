// Captures reel.html frame by frame into PNGs. Usage:
//   node render.js <seq-folder> <out-folder> [fromFrame] [toFrame] [step]
// <seq-folder> holds hf/ oreva/ mirvach/ rue/ as %04d.jpg (see ../RENDER.md).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [seq, out, from = '0', to = '', step = '1'] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'reel.html') + '?seq=' + encodeURIComponent('file://' + path.resolve(seq)));
  await page.evaluate(() => document.fonts.ready);
  const { DUR, FPS } = await page.evaluate(() => window.REEL);
  const last = to === '' ? Math.round(DUR * FPS) - 1 : +to;
  for (let i = +from; i <= last; i += +step) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    await page.screenshot({ path: path.join(out, String(i).padStart(5, '0') + '.png'), clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  }
  await browser.close();
})();
