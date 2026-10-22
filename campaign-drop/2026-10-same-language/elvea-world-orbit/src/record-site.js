// Records ELVÉA's own site interactions as 9:16 clips (1080×1920, 30fps) for the long cut:
//   rencontre — La Rencontre: the scroll plays the flower, the leaf and the drop meeting, the pour, the bottle
//   symbole   — the symbol draws itself: the leaf line, the drop line, the meeting point
//   fil       — Le Fil Vert: the launch carousel swiped sideways, five slides on one green line
//   coffret   — Le Coffret, then the boutique: "עולם שלם, באותו קו ובאותם צבעים"
// The site animates with GSAP ScrollTrigger (scrubbed): its ticker is put to sleep and stepped on the clip clock,
// so the scrub's easing plays out exactly as in a browser, one frame at a time.
// Recorded frame by frame: each frame sets the scroll and the pointer for its time, then pauses every CSS animation and
// transition and seeks it to that time, so the clips play at the site's real speed with no dropped or doubled frames.
// Usage: node record-site.js <repo>/elvea/index.html <outdir>   → <outdir>/<clip>.mp4
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
let pw; for (const n of ['playwright', '/opt/node22/lib/node_modules/playwright']) { try { pw = require(n); break } catch (e) {} }
const [, , SITE, OUT, ONLY] = process.argv;   // ONLY: a comma list of clips to re-record
const FPS = 30, W = 432, H = 768, DPR = 2.5;
const ease = u => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u) };

(async () => {
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const b = await pw.chromium.launch({ proxy, args: ['--allow-file-access-from-files', '--ignore-certificate-errors'] });
  const page = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: DPR });
  // the site loads GSAP 3.12.5 from cdnjs; the same files from npm (vendor/) are served in their place when cdnjs is unreachable
  await page.route(/cdnjs\.cloudflare\.com\/ajax\/libs\/gsap\/3\.12\.5\/(gsap|ScrollTrigger)\.min\.js/, (route, req) =>
    route.fulfill({ contentType: 'text/javascript', body: fs.readFileSync(path.join(__dirname, 'vendor', req.url().split('/').pop())) }));
  await page.goto('file://' + path.resolve(SITE), { waitUntil: 'load' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    document.querySelectorAll('img[loading="lazy"]').forEach(i => i.loading = 'eager');
    await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
  });
  await page.waitForTimeout(8000);   // the hero's canvas sequence loads its frames in two passes
  await page.evaluate(() => { gsap.ticker.lagSmoothing(0); gsap.ticker.sleep(); });   // GSAP runs on the clip clock from here
  const top = sel => page.evaluate(s => { const e = document.querySelector(s); return e.getBoundingClientRect().top + scrollY }, sel);
  // scroll, then make sure the site's own scroll handler has drawn this position before the frame is taken
  const scrollTo = async y => { await page.evaluate(v => { window.scrollTo(0, v); dispatchEvent(new Event('scroll')) }, y); await raf(); };
  const raf = () => page.evaluate(() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r))));

  async function clip(name, dur, setup, step) {
    if (ONLY && !ONLY.split(',').includes(name)) return;
    await page.mouse.move(2, 2);
    await setup(); await page.waitForTimeout(1200); await raf();
    await page.evaluate(() => {   // let the scrub settle on the new position before frame 0 (4s of GSAP time)
      window.__st = new Map();
      for (let i = 0; i < 40; i++) { ScrollTrigger.update(); window.__gt = (window.__gt || gsap.ticker.time) + .1; gsap.updateRoot(window.__gt); }
      window.__g0 = window.__gt;
    });
    const dir = path.join(OUT, 'tmp-' + name); fs.mkdirSync(dir, { recursive: true });
    const fired = new Set(), n = Math.round(dur * FPS);
    for (let f = 0; f < n; f++) {                      // frame by frame on the clip's own clock
      const ct = f / FPS;
      await step(ct, k => { if (fired.has(k)) return false; fired.add(k); return true });
      await page.evaluate(ct => { ScrollTrigger.update(); gsap.updateRoot(window.__g0 + ct); }, ct);
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
    await page.evaluate(d => { window.__gt = window.__g0 + d }, dur);
    execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(dir, 'f_%04d.jpg'),
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', path.join(OUT, name + '.mp4')]);
    fs.rmSync(dir, { recursive: true });
    console.error(name, n, 'frames');
  }

  const vh = H;
  // La Rencontre: the hero is pinned for 620% of the viewport; scroll it all, then let the scrub settle
  const heroLen = await page.evaluate(() => innerHeight * 6.2);
  await clip('rencontre', 7.2, async () => { await scrollTo(0); }, async ct => { await scrollTo(heroLen * ease((ct - .4) / 5.8)); });

  // the symbol: from the moment it enters to where its drawing ends (start 'top 62%', end 'bottom 78%')
  const sym = await page.evaluate(() => { const r = document.getElementById('symbole').getBoundingClientRect(); return [r.top + scrollY, r.height] });
  const s0 = sym[0] - vh * .42, s1 = sym[0] + sym[1] - vh * .78;   // start once the previous section has left the screen
  await clip('symbole', 4.0, async () => { await scrollTo(s0 - 200); await scrollTo(s0); }, async ct => { await scrollTo(s0 + (s1 - s0) * ease((ct - .2) / 2.8)); });

  // Le Fil Vert: the stage centred, then swiped from the first slide to the last
  const st = await page.evaluate(() => { const s = document.getElementById('filStage'), r = s.getBoundingClientRect(); return [r.top + scrollY, r.height] });
  let left0 = 0, span = 0;
  await clip('fil', 6.4, async () => {
    await scrollTo(st[0] - (vh - st[1]) / 2);
    [left0, span] = await page.evaluate(() => { const s = document.getElementById('filStage'), f = s.querySelector('.fil-panel'), sr = s.getBoundingClientRect(), fr = f.getBoundingClientRect();
      s.scrollLeft += (fr.left + fr.width / 2) - (sr.left + sr.width / 2); return [s.scrollLeft, s.scrollWidth - s.clientWidth] });
  }, async ct => {
    await page.evaluate(([l, d]) => { document.getElementById('filStage').scrollLeft = l - d; }, [left0, span * ease((ct - .5) / 5.4)]);
  });

  // Le Coffret, then the boutique
  const cof = await page.evaluate(() => { const r = document.querySelectorAll('#cards .card')[2].getBoundingClientRect(); return [r.top + scrollY, r.height] });
  const bq = await page.evaluate(() => { const r = document.querySelector('#boutique .wide').getBoundingClientRect(); return [r.top + scrollY, r.height] });
  const c0 = cof[0] - (vh - cof[1]) / 2, c1 = bq[0] - (vh - bq[1]) / 2;
  await clip('coffret', 6.0, async () => { await scrollTo(c0 - 300); await scrollTo(c0); }, async ct => { await scrollTo(c0 + (c1 - c0) * ease((ct - 1.6) / 3.2)); });
  await b.close();
})();
