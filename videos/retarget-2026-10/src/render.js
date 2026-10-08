// node render.js <track> <hook> <out.mp4>            full 30s MP4, 1080x1350, 30fps
// node render.js <track> <hook> <prefix> 0,90,300    stills
const path = require('path'), fs = require('fs'), { spawn } = require('child_process');
const { chromium } = require(process.env.PW || 'playwright');
const [,, track, hook, out, only] = process.argv;
const FPS = 30, W = 1080, H = 1350;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const tab = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await tab.goto('file://' + path.resolve(__dirname, 'reel.html') + `?track=${track}&hook=${hook}`, { waitUntil: 'load' });
  await tab.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map(i => i.decode().catch(() => {}))); });
  const fonts = await tab.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
  console.error('fonts loaded:', fonts.join(', ') || 'NONE');
  const frames = only ? only.split(',').map(Number) : [...Array(30 * FPS).keys()];
  let ff = null;
  if (!only) ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (const f of frames) {
    await tab.evaluate(t => window.setT(t), f / FPS);
    await tab.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
    const buf = await tab.screenshot({ type: 'jpeg', quality: 92, clip: { x: 0, y: 0, width: W, height: H } });
    if (ff) { if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    else fs.writeFileSync(`${out}-${f}.jpg`, buf);
    if (ff && f % 150 === 0) console.error(track, hook, 'frame', f);
  }
  if (ff) { ff.stdin.end(); await new Promise(r => ff.on('close', r)); }
  await browser.close();
})();
