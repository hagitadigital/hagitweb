// Records ENCORE's own site interactions as 9:16 clips (1080×1920, 30fps) for the long cut:
//   dial     — the sundial turns on the scroll: dawn, noon, sunset, night, a piece for each hour
//   hors     — out of the box: the box, the tag with no price, the bag in the colour of the hour, the four bags, the sign
//   set      — "הסט שלך": a piece for each hour flies into the clock face, then into the box
//   boite    — the 3D box: the sundial closes, the lid lifts, the engraving inside
// Recorded frame by frame: each frame sets the scroll and the pointer for its time, then pauses every CSS / Web animation and
// seeks it to that time (finishing it when it is past its end, so its onfinish runs), so the clips play at the site's real speed.
// three.js 0.170.0 is loaded by the site from jsdelivr; the same files from npm (vendor/three) are served in their place.
// Usage: node record-site.js <repo>/encore/index.html <outdir> [clip,clip]
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
let pw; for (const n of ['playwright', '/opt/node22/lib/node_modules/playwright']) { try { pw = require(n); break } catch (e) {} }
const [, , SITE, OUT, ONLY] = process.argv;   // ONLY: a comma list of clips to re-record
const FPS = 30, W = 432, H = 768, DPR = 2.5;
const ease = u => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u) };

(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await pw.chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const page = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  await page.route(/cdn\.jsdelivr\.net\/npm\/three@0\.170\.0\/(.*)$/, (route, req) =>
    route.fulfill({ contentType: 'text/javascript', body: fs.readFileSync(path.join(__dirname, 'vendor', 'three', req.url().split('three@0.170.0/')[1])) }));
  await page.goto('file://' + path.resolve(SITE), { waitUntil: 'load' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  });
  await page.waitForTimeout(6000);   // the hero's landing frames and the box's textures load
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
          const t = Math.max(0, (ct - __st.get(a)) * 1000), end = a.effect ? a.effect.getComputedTiming().endTime : Infinity;
          if (t >= end) a.finish(); else a.currentTime = t;   // finish() runs the animation's onfinish (the set's flying pieces land)
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

  const run = id => page.evaluate(id => { const e = document.getElementById(id); return [e.getBoundingClientRect().top + scrollY, e.offsetHeight - innerHeight] }, id);
  async function scroller(name, id, dur, a, b, from = 0, to = .995) {
    const [y0, len] = await run(id);
    await clip(name, dur, async () => { await scrollTo(y0 - 1); await scrollTo(y0 + len * from); }, async ct => { await scrollTo(y0 + len * (from + (to - from) * ease((ct - a) / (b - a)))); });
  }
  await scroller('dial', 'dial', 7.4, .4, 6.6);
  await scroller('hors', 'hors', 6.4, .3, 5.9);

  // the set: four taps, one piece for each hour, each flies into the clock face; then into the box
  const setTop = await page.evaluate(() => { const r = document.getElementById('clockface').getBoundingClientRect(); return r.top + scrollY });
  await clip('set', 6.6, async () => { await scrollTo(setTop - 60); }, async (ct, once) => {
    for (const [k, t] of [[0, .6], [1, 1.7], [2, 2.8], [3, 3.9]]) {
      if (ct > t && once('o' + k)) {
        await page.evaluate(k => { const tab = document.querySelector('.tab[data-i="' + k + '"]'); tab.click(); }, k);
        const r = await page.evaluate(() => { const o = document.querySelectorAll('#opts .opt')[1].getBoundingClientRect(); return { x: o.left + o.width / 2, y: o.top + o.height / 2 } });
        await page.mouse.click(r.x, r.y); await page.mouse.move(2, 2);
      }
    }
    if (ct > 5.4 && once('cta')) await page.evaluate(() => document.getElementById('cta').click());
  });
  await scroller('boite', 'boite', 6.0, .3, 5.4);
  await b.close();
})();
