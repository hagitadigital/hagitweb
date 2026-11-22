// Renders pendulum.html frame by frame to PNG.
// Usage: node render.cjs <outdir> [frame,frame,...]   (no list = the whole loop at 30fps)
// Then: ffmpeg -framerate 30 -i <outdir>/%04d.png -c:v libx264 -pix_fmt yuv420p -crf 16 out.mp4
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const [, , out, only] = process.argv;
const FPS = 30;

(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto(pathToFileURL(path.join(__dirname, 'pendulum.html')).href);
  await page.evaluate(() => window.ready);
  await page.waitForTimeout(500);
  const dur = await page.evaluate(() => window.DUR);
  const frames = only ? only.split(',').map(Number) : [...Array(Math.round(dur * FPS)).keys()];
  const canvas = page.locator('#c');
  for (const f of frames) {
    await page.evaluate(t => window.show(t), f / FPS);
    await canvas.screenshot({ path: path.join(out, String(f).padStart(4, '0') + '.png') });
  }
  await browser.close();
  console.log('rendered', frames.length, 'frames');
})();
