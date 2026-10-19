// Screenshots every concept frame in mock.html → ../frames/<name>.jpg
// The ad frames come from the two hidden-logo ads (ELVÉA° ritual, the dessert worlds), cut with:
//   ffmpeg -ss <t> -i <ad.mp4> -frames:v 1 -q:v 3 src/_build/ad/<elvea|desserts>-<t>.jpg
const path = require('path'), fs = require('fs');
function load(name) {
  for (const p of [name, '/opt/node22/lib/node_modules/' + name, '/usr/lib/node_modules/' + name, '/usr/local/lib/node_modules/' + name]) {
    try { return require(p); } catch (e) {}
  }
  throw new Error('playwright not found');
}
const { chromium } = load('playwright');
(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const tab = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await tab.goto('file://' + path.join(__dirname, 'mock.html'), { waitUntil: 'load' });
  await tab.evaluate(() => window.ready);
  const out = path.join(__dirname, '..', 'frames');
  fs.mkdirSync(out, { recursive: true });
  for (const n of await tab.evaluate(() => window.NAMES)) {
    await tab.evaluate(n => window.show(n), n);
    fs.writeFileSync(path.join(out, n + '.jpg'), await tab.screenshot({ type: 'jpeg', quality: 86 }));
  }
  await browser.close();
})();
