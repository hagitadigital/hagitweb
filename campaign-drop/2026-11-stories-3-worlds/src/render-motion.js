// Renders story 06 (motion) frame by frame, then encodes ../story-06.mp4 (10s loop, 30fps).
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path'), fs = require('fs');
const FPS = 30, DUR = 10, out = path.join(__dirname, '_frames');
(async () => {
  fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(out);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'stories.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const el = p.locator('#s6');
  for (let i = 0; i < FPS * DUR; i++) {
    await p.evaluate(t => setT(t), i / FPS);
    await el.screenshot({ path: path.join(out, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 96 });
  }
  await b.close();
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${out}/f%04d.jpg -c:v libx264 -pix_fmt yuv420p -crf 16 -preset slow -movflags +faststart ${path.join(__dirname, '..', 'story-06.mp4')}`);
  fs.rmSync(out, { recursive: true, force: true });
})();
