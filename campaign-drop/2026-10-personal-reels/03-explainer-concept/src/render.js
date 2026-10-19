// Renders an explainer page (no take: stills + ad frames live in the page) frame by frame.
// Usage:
//   node render.js <page.html> <out.mp4>                 1080×1920, 30fps, H.264, silent (music goes on in the app)
//   node render.js <page.html> <prefix> 0,120,300        QA stills: <prefix>-120.jpg …
// Ad frames in src/_build/ad/ are cut from the ad with: ffmpeg -ss <t> -i <ad.mp4> -frames:v 1 -q:v 3 _build/ad/elvea-<t>.jpg
const path = require('path'), fs = require('fs'), { spawn } = require('child_process');
function load(name) {
  for (const p of [name, '/opt/node22/lib/node_modules/' + name, '/usr/lib/node_modules/' + name, '/usr/local/lib/node_modules/' + name]) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright not found');
}
const { chromium } = load('playwright');
const [,, page, out, only] = process.argv;
if (!page || !out) { console.error('usage: node render.js <page.html> <out.mp4|prefix> [frames]'); process.exit(1); }
const FPS = 30;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const tab = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await tab.goto('file://' + path.resolve(page), { waitUntil: 'load' });
  await tab.evaluate(() => window.ready);
  const broken = await tab.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')));
  if (broken.length) console.error('BROKEN IMAGES', broken);
  const dur = await tab.evaluate(() => window.DUR);
  const draw = async f => {
    await tab.evaluate(t => window.seek(t), f / FPS);
    await tab.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  };
  if (only) {
    for (const f of only.split(',').map(Number)) { await draw(f); fs.writeFileSync(`${out}-${f}.jpg`, await tab.screenshot({ type: 'jpeg', quality: 86 })); }
    return browser.close();
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(dur * FPS);
  for (let f = 0; f < total; f++) {
    await draw(f);
    const buf = await tab.screenshot({ type: 'jpeg', quality: 94 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.error('frame', f, '/', total);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
