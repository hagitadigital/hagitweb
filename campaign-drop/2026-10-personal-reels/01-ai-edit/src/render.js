// Lays overlay.html over a talking-head take, frame by frame.
// Usage:
//   node render.js <take.mp4> <out.mp4>                 full reel: 1080×1920, 30fps, H.264, the take's own audio
//   node render.js <take.mp4> <prefix> 0,75,270         QA stills over the placeholder still: <prefix>-75.jpg …
// The overlay is screenshotted with a transparent background and piped to ffmpeg as PNG, on top of the take
// (scaled to cover 9:16). Length = the overlay's DUR, cut short if the take is shorter.
const path = require('path'), fs = require('fs'), { spawn } = require('child_process');
function load(name) {
  for (const p of [name, '/opt/node22/lib/node_modules/' + name, '/usr/lib/node_modules/' + name, '/usr/local/lib/node_modules/' + name]) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright not found — npm i -g playwright (browsers are usually preinstalled)');
}
const { chromium } = load('playwright');
const [,, take, out, only] = process.argv;
if (!take || !out) { console.error('usage: node render.js <take.mp4> <out.mp4|prefix> [frames]'); process.exit(1); }
const FPS = 30, W = 1080, H = 1920, PAGE = path.join(__dirname, 'overlay.html');
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const tab = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await tab.goto('file://' + PAGE, { waitUntil: 'load' });
  await tab.evaluate(() => window.ready);
  const fonts = await tab.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
  console.error('fonts loaded:', fonts.join(', ') || 'NONE (check network/proxy)');
  const dur = await tab.evaluate(() => window.DUR);
  const draw = async f => {
    await tab.evaluate(t => window.seek(t), f / FPS);
    await tab.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  };
  if (only) {
    await tab.evaluate(() => document.getElementById('stage').classList.add('preview'));
    for (const f of only.split(',').map(Number)) {
      await draw(f);
      fs.writeFileSync(`${out}-${f}.jpg`, await tab.screenshot({ type: 'jpeg', quality: 88 }));
    }
    return browser.close();
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', take,
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-filter_complex', `[0:v]scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=${FPS},setsar=1[b];[b][1:v]overlay=0:0:shortest=1,format=yuv420p[v]`,
    '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k',
    '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(dur * FPS);
  for (let f = 0; f < total; f++) {
    await draw(f);
    const buf = await tab.screenshot({ type: 'png', omitBackground: true });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.error('frame', f, '/', total);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
})();
