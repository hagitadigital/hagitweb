// Visual check for a brand book: full-page screenshots at desktop and mobile,
// plus the checks for the problems we already fixed once.
//
//   python3 -m http.server 8765 &                 (from the repo root)
//   node .claude/skills/brand-book/scripts/shoot.mjs encore
//   node .claude/skills/brand-book/scripts/shoot.mjs --url https://client.co.il/brand-book.html --name client
//
// Screenshots go to /tmp/brand-book-shots/. Exit code 1 when a check fails.
import { createRequire } from 'module';
import { execSync } from 'child_process';
import { mkdirSync } from 'fs';
import path from 'path';

async function loadPlaywright() {
  try { return await import('playwright'); } catch {}
  const globalRoot = execSync('npm root -g').toString().trim();
  return createRequire(path.join(globalRoot, 'noop.js'))('playwright');
}

const args = process.argv.slice(2);
const opt = (k) => { const i = args.indexOf(k); return i === -1 ? null : args[i + 1]; };
const base = (opt('--base') || 'http://localhost:8765').replace(/\/$/, '');
const slug = args[0] && !args[0].startsWith('--') ? args[0] : null;
const name = opt('--name') || slug || 'book';
const pages = opt('--url')
  ? [['book', opt('--url')]]
  : [['book', `${base}/${slug}/brand-book.html`], ['world', `${base}/${slug}/`]];
if (!slug && !opt('--url')) { console.error('usage: shoot.mjs <slug> | --url <book url> --name <name>'); process.exit(2); }

const OUT = '/tmp/brand-book-shots';
mkdirSync(OUT, { recursive: true });
const SIZES = [['desktop', 1440, 900], ['mobile', 390, 844]];

// Runs in the page. Returns a list of problems.
function audit(onlyBook) {
  const out = [];
  const say = (kind, el, msg) => {
    const t = (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60);
    out.push(`${kind}: ${msg} — "${t}"`);
  };
  const rgba = (s) => { const m = s.match(/[\d.]+/g); return m ? m.map(Number).concat(m.length === 3 ? [1] : []) : [0, 0, 0, 0]; };
  const lum = ([r, g, b]) => { const f = (c) => { c /= 255; return c <= .03928 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const over = (top, under) => { const a = top[3]; return [0, 1, 2].map((i) => top[i] * a + under[i] * (1 - a)).concat(1); };
  const ownText = (el) => [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
  const visible = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };

  // Effective background: composite ancestors' background colours; give up on images/gradients.
  function background(el) {
    const layers = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage !== 'none') return null;
      const c = rgba(cs.backgroundColor);
      if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let bg = [255, 255, 255, 1];
    for (let i = layers.length - 1; i >= 0; i--) bg = over(layers[i], bg);
    return bg;
  }

  // 1. overflow
  if (document.documentElement.scrollWidth > innerWidth + 1) out.push(`overflow: page is ${document.documentElement.scrollWidth}px wide in a ${innerWidth}px window`);

  // 2. images
  document.querySelectorAll('img[src]').forEach((img) => { if (img.complete && img.naturalWidth === 0) out.push(`image: did not load — ${img.getAttribute('src')}`); });

  const scope = onlyBook ? document.querySelectorAll('body *') : document.querySelectorAll('.book-link, .book-link *');
  const OLDSTYLE = /Cormorant|Garamond|Playfair|Bodoni|Italiana|Baskerville|Didot/i;
  scope.forEach((el) => {
    if (['SCRIPT', 'STYLE', 'svg', 'NOSCRIPT'].includes(el.tagName) || el.closest('svg')) return;
    const text = ownText(el);
    if (!text || !visible(el)) return;
    const cs = getComputedStyle(el);

    // 3. Latin name with ° in RTL flow, not isolated
    if (/[A-Za-zÀ-ÿ]°/.test(text) && cs.direction === 'rtl') say('bidi', el, 'Latin name with ° in RTL text — wrap it in <span class="ltr">');

    // 4. old-style figures in a serif
    if (/\d/.test(text) && OLDSTYLE.test(cs.fontFamily.split(',')[0]) && !/lining-nums/.test(cs.fontVariantNumeric))
      say('numerals', el, `${cs.fontFamily.split(',')[0]} without font-variant-numeric: lining-nums`);

    // 5. contrast
    const bg = background(el);
    if (bg) {
      const fg = over(rgba(cs.color), bg);
      const [l1, l2] = [lum(fg), lum(bg)].sort((a, b) => b - a);
      const ratio = (l1 + .05) / (l2 + .05);
      const size = parseFloat(cs.fontSize), bold = parseInt(cs.fontWeight, 10) >= 700;
      const large = size >= 24 || (size >= 18.66 && bold);
      const need = large ? 3 : 4.5;
      const op = parseFloat(cs.opacity);
      const effective = op < 1 ? 1 + (ratio - 1) * op : ratio; // rough: opacity pulls toward the background
      if (effective < need) say('contrast', el, `${effective.toFixed(2)}:1, needs ${need}:1 (${size}px)`);
    }
  });

  // 6. swallowed space in inline-flex buttons (display:flex links are layouts, not sentences)
  document.querySelectorAll(onlyBook ? 'a, button' : '.book-link').forEach((el) => {
    if (getComputedStyle(el).display !== 'inline-flex') return;
    el.querySelectorAll(':scope > span').forEach((sp) => {
      const prev = sp.previousSibling;
      if (prev && prev.nodeType === 3 && prev.textContent.trim() && !/ $/.test(prev.textContent))
        say('button', el, 'text before the span ends without &nbsp; — the space is swallowed in inline-flex');
      if (/^ /.test(sp.textContent)) say('button', el, '&nbsp; inside the span — put it before the span');
    });
  });
  return out;
}

const { chromium } = await loadPlaywright();
const browser = await chromium.launch(process.env.PLAYWRIGHT_BROWSERS_PATH ? {} : { executablePath: '/opt/pw-browsers/chromium' });
let failed = 0;
for (const [kind, url] of pages) {
  for (const [label, w, h] of SIZES) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const res = await page.goto(url, { waitUntil: 'networkidle' }).catch((e) => ({ status: () => e.message }));
    if (!res || (typeof res.status() === 'number' && res.status() >= 400)) { console.log(`✗ ${url} → ${res && res.status()}`); failed++; await page.close(); continue; }
    // reveal scroll animations and lazy images before measuring
    await page.addStyleTag({ content: '.rv{opacity:1!important;transform:none!important;transition:none!important}' });
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } scrollTo(0, 0); });
    await page.waitForLoadState('networkidle');
    const file = `${OUT}/${name}-${kind}-${label}.png`;
    await page.screenshot({ path: file, fullPage: true });
    const problems = await page.evaluate(audit, kind === 'book');
    console.log(`\n${problems.length ? '✗' : '✓'} ${kind} · ${label} ${w}px → ${file}`);
    problems.forEach((p) => console.log('   ' + p));
    failed += problems.length;
    await page.close();
  }
}
await browser.close();
console.log(failed ? `\n${failed} problem(s). Open the screenshots and fix them.` : '\nNo automatic problems. Now look at every screenshot.');
process.exit(failed ? 1 : 0);
