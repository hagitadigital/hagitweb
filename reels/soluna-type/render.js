// Renders reel.html frame by frame (the page steps its own fluid: window.__frame(n)).
//   node render.js reel.html out/SOLUNA-type.mp4        full MP4, 1080×1920, 30fps
//   node render.js reel.html test/r 0,60,150            stills: test/r-0.jpg …
const path = require('path'), fs = require('fs'), { spawn } = require('child_process');
let pw; for (const n of ['playwright', '/opt/node22/lib/node_modules/playwright', '/usr/lib/node_modules/playwright']) { try { pw = require(n); break; } catch (e) {} }
const [,, page, out, only] = process.argv;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await pw.chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const tab = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  tab.on('pageerror', e => console.error('PAGE ERROR', e.message)); tab.on('console', m => m.type() === 'error' && console.error('console:', m.text().slice(0, 200)));
  await tab.goto('file://' + path.resolve(page), { waitUntil: 'load' });
  await tab.waitForFunction('window.__ready', null, { timeout: 60000 });
  console.error('fonts:', (await tab.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))])).join(', '));
  const broken = await tab.evaluate(() => [...document.images].filter(i => i.getAttribute('src') && !i.naturalWidth).map(i => i.getAttribute('src')));
  if (broken.length) console.error('BROKEN IMAGES', broken);
  const total = Math.round((await tab.evaluate('window.__dur')) * 30);
  const frames = only ? only.split(',').map(Number) : [...Array(total).keys()];
  let ff = null;
  if (!only) ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', '30', '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (const f of frames) {
    await tab.evaluate(f => window.__frame(f), f);
    await tab.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    const buf = await tab.screenshot({ type: 'jpeg', quality: 93 });
    if (ff) { if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); } else fs.writeFileSync(`${out}-${f}.jpg`, buf);
    if (f % 60 === 0) console.error('frame', f, '/', total);
  }
  if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await b.close();
})();
