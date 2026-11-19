// Renders carousel.html: for each slide a still (../carousel/slide-0N.png) and a looping mp4 (../carousel/slide-0N.mp4, 30fps).
// Usage: node render-carousel.js [stills]   — "stills" skips the videos.
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path'), fs = require('fs');
const FPS = 30, here = __dirname, outDir = path.join(here, '..', 'carousel'), tmp = path.join(here, '_frames'), mains = path.join(here, '_mains');
(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  // CHASEN whisking clip -> frame sequence (temporary, removed at the end)
  fs.rmSync(mains, { recursive: true, force: true }); fs.mkdirSync(mains);
  execSync(`ffmpeg -y -loglevel error -i ${path.join(here, '../../../chasen/assets/lecon/mains.mp4')} -q:v 2 ${mains}/m%03d.jpg`);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(here, 'carousel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForLoadState('networkidle');
  await p.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  const slides = await p.$$eval('.slide', s => s.map(e => ({ id: e.id, T: +e.dataset.t, still: +e.dataset.still })));
  for (const [n, s] of slides.entries()) {
    const el = p.locator('#' + s.id), name = `slide-0${n + 1}`;
    await p.evaluate(([id, t]) => setT(id, t), [s.id, s.still]);
    await el.screenshot({ path: path.join(outDir, name + '.png') });
    if (process.argv[2] === 'stills') continue;
    fs.rmSync(tmp, { recursive: true, force: true }); fs.mkdirSync(tmp);
    for (let i = 0; i < FPS * s.T; i++) {
      await p.evaluate(([id, t]) => setT(id, t), [s.id, i / FPS]);
      await el.screenshot({ path: path.join(tmp, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 96 });
    }
    execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${tmp}/f%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 17 -preset slow -movflags +faststart ${path.join(outDir, name + '.mp4')}`);
  }
  await b.close();
  fs.rmSync(tmp, { recursive: true, force: true }); fs.rmSync(mains, { recursive: true, force: true });
})();
