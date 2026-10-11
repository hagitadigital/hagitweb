// Deterministic render for wall.html: step window.setT(t), seek every visible video to its time, screenshot, pipe to ffmpeg.
//   node render.js wall.html 20 ../wall-9x16.mp4            full MP4 (1080×1920, 30fps, H.264)
//   node render.js wall.html 20 test/w 0,60,120             stills: test/w-0.jpg …
const path = require('path'), fs = require('fs'), { spawn } = require('child_process');
let pw; for (const n of ['playwright', '/opt/node22/lib/node_modules/playwright', '/usr/lib/node_modules/playwright']) { try { pw = require(n); break; } catch (e) {} }
const [,, page, durS, out, only] = process.argv;
const FPS = 30;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await pw.chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors', '--autoplay-policy=no-user-gesture-required'] });
  const tab = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await tab.goto('file://' + path.resolve(page), { waitUntil: 'load' });
  await tab.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
    await Promise.all([...document.querySelectorAll('video')].map(v => v.readyState >= 2 ? 0 : new Promise(r => { v.onloadeddata = r; v.onerror = r; v.load(); })));
  });
  const bad = await tab.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src).concat(
    [...document.querySelectorAll('video')].filter(v => !v.videoWidth).map(v => v.src)));
  if (bad.length) console.error('BROKEN MEDIA', bad.slice(0, 8));
  console.error('fonts loaded:', (await tab.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))])).join(', '));
  const frames = only ? only.split(',').map(Number) : [...Array(Math.round(+durS * FPS)).keys()];
  let ff = null;
  if (!only) ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (const f of frames) {
    await tab.evaluate(async t => {
      window.setT(t);
      const vids = [...document.querySelectorAll('video')];
      await Promise.all(window.videoTimes(t).map(([i, vt]) => new Promise(r => {
        const v = vids[i]; if (Math.abs(v.currentTime - vt) < 1e-3) return r();
        v.addEventListener('seeked', r, { once: true }); v.currentTime = vt;
      })));
      await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    }, f / FPS);
    const buf = await tab.screenshot({ type: 'jpeg', quality: 92 });
    if (ff) { if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    else fs.writeFileSync(`${out}-${f}.jpg`, buf);
    if (ff && f % 60 === 0) console.error('frame', f, '/', frames.length);
  }
  if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await browser.close();
})();
