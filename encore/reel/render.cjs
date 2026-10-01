// Renders the graphic scenes (frame by frame) and the text overlays (transparent PNGs) of the reel.
// Usage: node render.cjs <reel.html> <outdir>
// CommonJS so NODE_PATH (global playwright) resolves.
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const [, , html, out] = process.argv;
const FPS = 30;
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'scenes.json')));

(async () => {
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(pathToFileURL(path.resolve(html)).href);
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);

for (const s of cfg.scenes) {
  if (s.type === 'graphic') {
    const dir = path.join(out, s.id);
    fs.mkdirSync(dir, { recursive: true });
    const n = Math.round(s.dur * FPS);
    for (let f = 0; f < n; f++) {
      await page.evaluate(([id, t]) => window.show(id, t), [s.id, f / FPS]);
      await page.screenshot({ path: path.join(dir, String(f).padStart(4, '0') + '.png') });
    }
  } else {
    for (const part of ['a', 'b']) {
      await page.evaluate(([o]) => window.show('ov', 0, o), [{ ...s.text, part }]);
      await page.screenshot({ path: path.join(out, `${s.id}_${part}.png`), omitBackground: true });
    }
  }
  console.log('rendered', s.id);
}
await browser.close();
})();
