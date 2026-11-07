// Deterministic reel render: pause every CSS animation, step currentTime frame by frame, screenshot, pipe to ffmpeg.
// Usage:
//   node render.js <page.html> <seconds> <out.mp4>              full MP4 (1080×1920, 30fps, H.264)
//   node render.js <page.html> <seconds> <prefix> 0,90,300      test stills: <prefix>-0.jpg, <prefix>-90.jpg …
// Pages load from file://, so keep assets as relative paths next to the page.
const path = require('path'), fs = require('fs'), { spawn, execSync } = require('child_process');
function load(name) {
  for (const p of [name, '/opt/node22/lib/node_modules/' + name, '/usr/lib/node_modules/' + name, '/usr/local/lib/node_modules/' + name]) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright not found — npm i -g playwright (browsers are usually preinstalled)');
}
function ffmpeg() {
  if (process.env.FFMPEG) return process.env.FFMPEG;
  try { return execSync('command -v ffmpeg').toString().trim(); } catch (e) {}
  return execSync('python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"').toString().trim();
}
const { chromium } = load('playwright');
const [,, page, durS, out, only] = process.argv;
if (!page || !durS || !out) { console.error('usage: node render.js <page.html> <seconds> <out.mp4|prefix> [frames]'); process.exit(1); }
const FPS = 30, W = 1080, H = +(process.env.REEL_H || 1920);
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const tab = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await tab.goto('file://' + path.resolve(page), { waitUntil: 'load' });
  await tab.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
    document.getAnimations().forEach(a => a.pause());
  });
  const broken = await tab.evaluate(() => [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src')));
  if (broken.length) console.error('BROKEN IMAGES', [...new Set(broken)].slice(0, 8));
  const fonts = await tab.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
  console.error('fonts loaded:', fonts.join(', ') || 'NONE (check network/proxy)');
  const frames = only ? only.split(',').map(Number) : [...Array(Math.round(+durS * FPS)).keys()];
  let ff = null;
  if (!only) ff = spawn(ffmpeg(), ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (const f of frames) {
    await tab.evaluate(t => document.getAnimations().forEach(a => { a.currentTime = t; }), f * 1000 / FPS);
    await tab.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    const buf = await tab.screenshot({ type: 'jpeg', quality: 92 });
    if (ff) { if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    else fs.writeFileSync(`${out}-${f}.jpg`, buf);
    if (ff && f % 150 === 0) console.error('frame', f, '/', frames.length);
  }
  if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await browser.close();
})();
