// Records VELUNE's own site interactions as 9:16 clips (1080×1920, 30fps) for the long cut:
//   seuil    — the first scroll opens the arched door and walks into the garden
//   heures   — one bottle, three hours: the scroll turns the sun along its arc and the bottle changes colour
//   fruit    — the fruit opens, one drop falls, the drop becomes the bottle
//   ecrin    — the door returns as a box: its two leaves open on the scroll
//   cart     — the boutique: "הוספה לסל" and the cart slides in
// Recorded frame by frame: each frame sets the scroll and the pointer for its time, then pauses every CSS animation and
// transition and seeks it to that time, so the clips play at the site's real speed with no dropped or doubled frames.
// Usage: node record-site.js <repo>/velune/index.html <outdir>   → <outdir>/<clip>.mp4
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
let pw; for (const n of ['playwright', '/opt/node22/lib/node_modules/playwright']) { try { pw = require(n); break } catch (e) {} }
const [, , SITE, OUT, ONLY] = process.argv;   // ONLY: a comma list of clips to re-record
const FPS = 30, W = 432, H = 768, DPR = 2.5;
const ease = u => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u) };

(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await pw.chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const page = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  await page.goto('file://' + path.resolve(SITE), { waitUntil: 'load' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
    try { localStorage.removeItem('velune-cart') } catch (e) {}
  });
  await page.waitForTimeout(9000);   // the canvas sequences (door, fruit) load their frames one by one
  const top = sel => page.evaluate(s => { const e = document.querySelector(s); return e.getBoundingClientRect().top + scrollY }, sel);
  // scroll, then make sure the site's own scroll handler has drawn this position before the frame is taken
  const scrollTo = async y => { await page.evaluate(v => { window.scrollTo(0, v); dispatchEvent(new Event('scroll')) }, y); await raf(); };
  const raf = () => page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));

  async function clip(name, dur, setup, step) {
    if (ONLY && !ONLY.split(',').includes(name)) return;
    await page.mouse.move(2, 2);
    await setup(); await page.waitForTimeout(1200); await raf();
    await page.evaluate(() => { window.__st = new Map() });
    const dir = path.join(OUT, 'tmp-' + name); fs.mkdirSync(dir, { recursive: true });
    const fired = new Set(), n = Math.round(dur * FPS);
    for (let f = 0; f < n; f++) {                      // frame by frame on the clip's own clock
      const ct = f / FPS;
      await step(ct, k => { if (fired.has(k)) return false; fired.add(k); return true });
      await raf();
      // every CSS animation and transition is paused and seeked to the clip clock (counted from when it first appears)
      await page.evaluate(ct => {
        for (const a of document.getAnimations()) {
          if (!__st.has(a)) { __st.set(a, ct - (a.currentTime || 0) / 1000); a.pause(); }
          a.currentTime = Math.max(0, (ct - __st.get(a)) * 1000);
        }
      }, ct);
      await raf();
      fs.writeFileSync(path.join(dir, `f_${String(f + 1).padStart(4, '0')}.jpg`), await page.screenshot({ type: 'jpeg', quality: 92 }));
    }
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f_%04d.jpg'),
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', path.join(OUT, name + '.mp4')]);
    fs.rmSync(dir, { recursive: true });
    console.error(name, n, 'frames');
  }

  // a pinned scroller: hold, scroll its whole run, hold
  const run = id => page.evaluate(id => { const e = document.getElementById(id); return [e.getBoundingClientRect().top + scrollY, e.offsetHeight - innerHeight] }, id);
  async function scroller(name, id, dur, a, b) {
    const [y0, len] = await run(id);
    await clip(name, dur, async () => { await scrollTo(y0 - 1); await scrollTo(y0); }, async ct => { await scrollTo(y0 + len * .995 * ease((ct - a) / (b - a))); });
  }
  await scroller('seuil', 'seuil', 6.0, .6, 5.4);
  await scroller('heures', 'heures', 4.6, .3, 4.2);
  await scroller('fruit', 'fruit', 6.2, .3, 5.8);
  await scroller('ecrin', 'ecrin', 4.6, .4, 3.9);

  // the boutique: the first bottle card, centred; a tap on "הוספה לסל" and the cart slides in
  const card = await page.evaluate(() => { const r = document.querySelector('.p-card').getBoundingClientRect(); return [r.top + scrollY, r.height] });
  await clip('cart', 3.6, async () => { await scrollTo(card[0] - (H - card[1]) / 2); }, async (ct, once) => {
    if (ct > .9 && once('add')) {
      const r = await page.evaluate(() => { const e = document.querySelector('.p-card .add').getBoundingClientRect(); return { x: e.left + e.width / 2, y: e.top + e.height / 2 } });
      await page.mouse.click(r.x, r.y); await page.mouse.move(2, 2);
    }
  });
  await b.close();
})();
