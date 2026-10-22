// Records PARDON ME's own site interactions as 9:16 clips (1080×1920, 30fps) for the long cut:
//   peek     — the first scroll grows the oval window over the print
//   tear     — "Pardon the interruption": Tear here, the sleeve rips, the ad bursts through
//   ads      — the campaign: the oval lens follows the pointer over a polite ad, a tap strips it bare
//   colls    — the collections: a tap on the oval takes the sleeve off and shows the product
// Recorded frame by frame: each frame sets the scroll and the pointer for its time, then pauses every CSS animation and
// transition and seeks it to that time, so the clips play at the site's real speed with no dropped or doubled frames.
// Usage: node record-site.js <repo>/pardon-me/index.html <outdir>   → <outdir>/<clip>.mp4
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
    for (let k = 1; k < 2000; k++) clearInterval(k);           // the peek's print cycle is driven from the clip clock instead
  });
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

  // peek: hold on the small window, then scroll the whole pinned section; the print behind the window changes twice
  const peekRun = await page.evaluate(() => { const p = document.getElementById('peek'); return p.offsetHeight - innerHeight });
  const prints = ['var(--p-hello)', 'var(--p-nyb)', 'var(--p-hm)', 'var(--p-bi)'];
  const setPrint = i => page.evaluate(([i, pr]) => {
    const prs = document.querySelectorAll('#peek .inside .pr');
    prs.forEach((p, k) => p.classList.toggle('on', k === i));
    document.querySelectorAll('.s-top .wm .o').forEach(o => o.style.backgroundImage = pr);
  }, [i, prints[i]]);
  await clip('peek', 6, async () => { await scrollTo(0); await setPrint(2); }, async (ct, once) => {
    if (ct > 1.1 && once('p1')) await setPrint(3);
    if (ct > 3.0 && once('p2')) await setPrint(0);
    await scrollTo(peekRun * .98 * ease((ct - .9) / 4.2));
  });

  // tear: the half-sheets sit still, the button nudges, then it rips
  const tearY = await top('#interrupt');
  await clip('tear', 3.6, async () => { await page.evaluate(() => document.getElementById('interrupt').classList.remove('torn')); await scrollTo(tearY); },
    async (ct, once) => { if (ct > 1.0 && once('rip')) await page.click('#tear'); });

  // ads: the first ad, centred; the lens follows the pointer around it, then a tap strips the polite layer
  const adBox = async () => page.evaluate(() => { const r = document.querySelector('.cc--ad .ad').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height } });
  await clip('ads', 4.2, async () => {
    await page.evaluate(() => document.querySelectorAll('.ad').forEach(a => a.classList.remove('bare')));
    const y = await top('.cc--ad .ad'); const h = (await adBox()).h; await scrollTo(y - (H - h) / 2);
  }, async (ct, once) => {
    const r = await adBox();
    if (ct > .3 && ct < 2.7) {
      const a = (ct - .3) / 2.4 * Math.PI * 2;
      await page.mouse.move(r.x + r.w * (.5 + .22 * Math.sin(a)), r.y + r.h * (.55 - .2 * Math.sin(a) * Math.cos(a) * 1.6));
    }
    if (ct > 2.9 && once('tap')) await page.mouse.click(r.x + r.w * .5, r.y + r.h * .55);
  });

  // collections: tap the first box's oval, glide to the second, tap it
  const boxes = await page.evaluate(() => [...document.querySelectorAll('.coll .box')].map(b => b.getBoundingClientRect().top + scrollY));
  const boxH = await page.evaluate(() => document.querySelector('.coll .box').getBoundingClientRect().height);
  const at = i => boxes[i] - (H - boxH) / 2 + 40;
  await clip('colls', 6.4, async () => {
    await page.evaluate(() => document.querySelectorAll('.box').forEach(b => b.setAttribute('aria-pressed', 'false')));
    await scrollTo(at(1));
  }, async (ct, once) => {
    await scrollTo(at(1) + (at(2) - at(1)) * ease((ct - 2.6) / 1.0));
    const tap = async i => { const r = await page.evaluate(i => { const e = document.querySelectorAll('.coll .box')[i].getBoundingClientRect(); return { x: e.left + e.width / 2, y: e.top + e.height * .57 } }, i); await page.mouse.click(r.x, r.y); await page.mouse.move(2, 2); };
    if (ct > .9 && once('t1')) await tap(1);
    if (ct > 4.0 && once('t2')) await tap(2);
  });
  await b.close();
})();
