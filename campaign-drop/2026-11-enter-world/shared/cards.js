// World cards around Hagit while she talks to camera (S6). Shared by the episode pages.
// makeCards(stage, base, sets) → draw(t, set, t0, t1, opts)
//   window.CARDS_MODE (set in mode.js): 'orbit' = cards circle slowly around her (depth, tilt, float);
//                                       'seq'   = one card at a time beside her, then it joins a row of thumbnails.
//   opts.still: cards already in place at t0 (frame-0 proof) · opts.beats: [t…] when each card is presented (seq).
(function () {
  const css = `#cards{position:absolute;inset:0;pointer-events:none;z-index:4}
.oc{position:absolute;left:0;top:0;width:240px;height:320px;margin:-160px 0 0 -120px;border-radius:22px;overflow:hidden;background:#fff;
  box-shadow:0 22px 50px rgba(20,25,18,.38),0 0 0 7px #fff;opacity:0;transform-origin:50% 50%}
.oc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}`;
  const c = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), L = (t, a, b) => c((t - a) / (b - a));
  const eo = x => 1 - Math.pow(1 - x, 3), ei = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
  window.makeCards = function (stage, base, sets, pos) {
    const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    const root = document.createElement('div'); root.id = 'cards'; stage.appendChild(root);
    const O = Object.assign({ cx: 540, cy: 700, rx: 420, ry: 480, speed: 0.16, sideY: 760, sideX: [850, 230], rowY: 1190 }, pos || {});
    const C = {};
    for (const [k, list] of Object.entries(sets)) C[k] = list.map(([src, op]) => { const d = document.createElement('div'); d.className = 'oc'; root.appendChild(d);
      const im = document.createElement('img'); im.src = base + src; if (op) im.style.objectPosition = op; d.appendChild(im); return d; });
    const mode = window.CARDS_MODE || 'orbit';
    return function (t, set, t0, t1, opts = {}) {
      const cs = C[set], n = cs.length;
      cs.forEach((el, i) => {
        if (t < t0 - .1 || t > t1 + .7) { el.style.opacity = 0; return; }
        const out = ei(L(t, t1, t1 + .6));
        if (mode === 'orbit') {
          const a = -Math.PI / 2 + i * 2 * Math.PI / n + (t - t0) * O.speed, depth = (Math.sin(a) + 1) / 2;
          let x = O.cx + O.rx * Math.cos(a), y = O.cy + O.ry * Math.sin(a) + 14 * Math.sin(t * 1.3 + i);
          const pop = opts.still ? 1 : eo(L(t, t0 + i * .16, t0 + i * .16 + .45));
          x += (x - O.cx) * .9 * out; y += (y - O.cy) * .9 * out;
          el.style.opacity = pop * (1 - out); el.style.zIndex = Math.round(depth * 10);
          el.style.transform = `translate(${x}px,${y}px) scale(${(.74 + .3 * depth) * (.6 + .4 * pop)}) rotate(${(i % 2 ? 5 : -6) + 3 * Math.sin(t * .9 + i * 1.7)}deg)`;
        } else {
          // presentation: card i comes in beside her at beats[i], holds, then shrinks into its slot in the row
          const beats = opts.beats || cs.map((_, j) => t0 + j * (t1 - t0) / n), b = beats[i], nb = i + 1 < n ? beats[i + 1] : t1;
          const pin = opts.still && i === 0 ? 1 : eo(L(t, b, b + .4)), park = ei(L(t, nb - .05, nb + .4));
          const side = i % 2, sx = O.sideX[side], sy = O.sideY;
          const rx = 540 + (i - (n - 1) / 2) * 150, ry = O.rowY;
          const fromX = side ? -200 : 1280;
          let x = fromX + (sx - fromX) * pin, y = sy + 40 * (1 - pin), s = 1.35, r = (side ? 6 : -6) * (1 - pin) + (side ? -3 : 3);
          x += (rx - x) * park; y += (ry - y) * park; s += (.5 - s) * park; r += (0 - r) * park;
          y += (y - 700) * .5 * out; s *= 1 - .3 * out;
          el.style.opacity = (t >= b - .02 || (opts.still && i === 0) ? 1 : 0) * (1 - out); el.style.zIndex = park < 1 ? 20 + i : i;
          el.style.transform = `translate(${x}px,${y + 6 * Math.sin(t * 1.4 + i)}px) scale(${s}) rotate(${r}deg)`;
        }
      });
    };
  };
})();
