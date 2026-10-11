// Records the four live sections as image sequences, on a controlled clock (15 fps, every frame exact).
// usage: node capture.js <outdir>   (needs the site served at http://localhost:8765)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const OUT = process.argv[2], STEP = 1000 / 15;
const fs = require('fs'); fs.mkdirSync(OUT, { recursive: true });
async function shoot(p, name, i, clip) {
  await p.screenshot({ path: `${OUT}/${name}_${String(i + 1).padStart(3, '0')}.jpg`, type: 'jpeg', quality: 84, clip });
}
(async () => {
  const b = await chromium.launch();
  const page = async (url, vp) => { const p = await b.newPage({ viewport: vp }); await p.clock.install(); await p.goto(url, { waitUntil: 'networkidle' }); await p.clock.runFor(1500); return p; };
  const rect = (p, sel, pad = 0) => p.evaluate(([s, d]) => { const r = document.querySelector(s).getBoundingClientRect(); return { x: Math.max(0, r.left - d), y: Math.max(0, r.top - d), width: Math.min(innerWidth, r.width + 2 * d), height: r.height + 2 * d }; }, [sel, pad]);

  // 1 · PARDON ME° cascade: still, a fast scroll (plates slip), back, settle.
  //     A very tall window keeps the whole cascade in view while the page runs ~30px per frame.
  { const p = await page('http://localhost:8765/pardon-me/', { width: 1440, height: 2500 });
    await p.addStyleTag({ content: '.topbar,#studioChip{visibility:hidden!important}' });
    await p.evaluate(() => { document.querySelectorAll('.ad').forEach(a => a.classList.add('bare'));   // the ads' real copy, not the polite cover
      const a = document.getElementById('ads'); scrollTo({ top: a.getBoundingClientRect().top + scrollY - 1560, behavior: 'instant' }); });
    await p.clock.runFor(1200);
    const N = 54;
    for (let i = 0; i < N; i++) {
      const v = i < 8 ? 0 : i < 20 ? 30 : i < 32 ? -30 : 0;            // px per animation frame
      for (let k = 0; k < 4; k++) { if (v) await p.evaluate(d => scrollBy({ top: d, behavior: 'instant' }), v); await p.clock.runFor(STEP / 4); }
      await shoot(p, 'pm', i, await rect(p, '#ads', 10));
    }
    await p.close(); }

  if (process.argv[3] === "pm") { await b.close(); return; }
  // 2 · SONAIR° signatures: hover Balanced → Deep Bass → Vocal Clarity, the pointer drifting down each card
  { const p = await page('http://localhost:8765/sonair/', { width: 1440, height: 1300 });
    await p.evaluate(() => document.querySelector('.sig-row').scrollIntoView({ block: 'center', behavior: 'instant' }));
    await p.clock.runFor(800);
    const cards = await p.$$('.sig .frame'); const order = [2, 1, 0];   // RTL: Balanced is the right-most
    const boxes = []; for (const c of cards) boxes.push(await c.boundingBox());
    const clip = await rect(p, '.sig-row', 14); clip.height = Math.round((boxes[0].y + boxes[0].height + 90) - clip.y);
    const N = 60;
    for (let i = 0; i < N; i++) {
      const k = Math.min(2, Math.floor(i / 20)), bx = boxes[order[k]], f = (i % 20) / 20;
      await p.mouse.move(bx.x + bx.width * .5, bx.y + bx.height * (.25 + .5 * f));
      await p.clock.runFor(STEP);
      await shoot(p, 'so', i, clip);
    }
    await p.close(); }

  // 3 · Les Livres spiral: ENCORE° turning, then the PARDON ME° tab
  { const p = await page('http://localhost:8765/studio.html', { width: 1440, height: 1300 });
    await p.evaluate(() => { const s = document.getElementById('spiral'); scrollTo({ top: s.getBoundingClientRect().top + scrollY - 140, behavior: 'instant' }); });
    await p.clock.runFor(800);
    const clip = await rect(p, '#spiral', 6), N = 60;
    for (let i = 0; i < N; i++) {
      if (i === 30) await p.evaluate(() => document.querySelector('#spiralTabs button:nth-child(5)').click());
      await p.clock.runFor(STEP);
      await shoot(p, 'sp', i, clip);
    }
    await p.close(); }

  // 4 · the gallery ring: scrolling turns it, the front world grows and names itself
  { const p = await page('http://localhost:8765/brand-worlds/', { width: 1440, height: 1100 });
    await p.evaluate(() => scrollTo({ top: document.getElementById('ring').offsetTop, behavior: 'instant' }));
    await p.clock.runFor(800);
    const N = 60;
    for (let i = 0; i < N; i++) {
      await p.evaluate(() => scrollBy({ top: 9, behavior: 'instant' }));
      await p.clock.runFor(STEP);
      await shoot(p, 'rg', i, { x: 200, y: 60, width: 1040, height: 1000 });
    }
    await p.close(); }
  await b.close();
})();
