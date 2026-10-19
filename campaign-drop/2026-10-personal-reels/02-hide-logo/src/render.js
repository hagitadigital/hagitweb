// Renders reel.html with Hagit's take INSIDE the page, frame by frame (so the grade recolours her).
// Usage:
//   node render.js <take.mp4> <out.mp4>              full reel: 1080×1920, 30fps, H.264, the take's own audio
//   node render.js <take.mp4> <prefix> 0,75,270      QA stills: <prefix>-75.jpg …
// The take is cut to 9:16 frames in src/_build/take/ first (reused while the take file is unchanged).
const path = require('path'), fs = require('fs'), { spawn, execFileSync } = require('child_process');
function load(name) {
  for (const p of [name, '/opt/node22/lib/node_modules/' + name, '/usr/lib/node_modules/' + name, '/usr/local/lib/node_modules/' + name]) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright not found — npm i -g playwright (browsers are usually preinstalled)');
}
const { chromium } = load('playwright');
const [,, take, out, only] = process.argv;
if (!take || !out) { console.error('usage: node render.js <take.mp4> <out.mp4|prefix> [frames]'); process.exit(1); }
const FPS = 30, W = 1080, H = 1920, PAGE = path.join(__dirname, 'reel.html');
const FR = path.join(__dirname, '_build/take'), STAMP = path.join(FR, '.source');
const sig = path.resolve(take) + ':' + fs.statSync(take).mtimeMs;
if (!fs.existsSync(STAMP) || fs.readFileSync(STAMP, 'utf8') !== sig) {
  fs.rmSync(FR, { recursive: true, force: true }); fs.mkdirSync(FR, { recursive: true });
  console.error('cutting the take into frames…');
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', take, '-vf',
    `scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},fps=${FPS},setsar=1`, '-q:v', '3', path.join(FR, '%05d.jpg')]);
  fs.writeFileSync(STAMP, sig);
}
const nTake = fs.readdirSync(FR).filter(f => f.endsWith('.jpg')).length;
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const tab = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  await tab.goto('file://' + PAGE, { waitUntil: 'load' });
  await tab.evaluate(() => window.ready);
  const fonts = await tab.evaluate(() => [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family))]);
  console.error('fonts loaded:', fonts.join(', ') || 'NONE (check network/proxy)');
  const dur = await tab.evaluate(() => window.DUR);
  const total = Math.min(Math.round(dur * FPS), nTake);
  const draw = async f => {
    const src = 'file://' + path.join(FR, String(Math.min(f, nTake - 1) + 1).padStart(5, '0') + '.jpg');
    await tab.evaluate(([s, t]) => window.setBg(s).then(() => window.seek(t)), [src, f / FPS]);
    await tab.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));
  };
  if (only) {
    for (const f of only.split(',').map(Number)) {
      await draw(f);
      fs.writeFileSync(`${out}-${f}.jpg`, await tab.screenshot({ type: 'jpeg', quality: 88 }));
    }
    return browser.close();
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', take, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
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
