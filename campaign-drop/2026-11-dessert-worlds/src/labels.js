// Renders the world labels (BOL°, CHASEN°) as transparent PNGs: node labels.js <outdir>
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const out = process.argv[2] || '.';
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1100 } });
  await p.goto('file://' + path.join(__dirname, 'labels.html')); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  for (const id of ['bol', 'chasen']) await p.locator('#' + id).screenshot({ path: path.join(out, `label-${id}.png`), omitBackground: true });
  await b.close();
})();
