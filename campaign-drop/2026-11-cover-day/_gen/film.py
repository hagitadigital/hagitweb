"""Tiny timeline helper: every time is in seconds, turned into @keyframes percentages of the film length.
render.js pauses every CSS animation and steps currentTime, so the page is fully deterministic."""


class Film:
    def __init__(self, dur):
        self.D = dur
        self.css = []
        self.n = 0

    def P(self, t):
        t = max(0.0, min(self.D, t))
        return f"{t / self.D * 100:.3f}%"

    def _name(self, k):
        self.n += 1
        return f"{k}{self.n}"

    def show(self, a, b, f=0.3):
        """visible from a to b (fade f)."""
        k = self._name("s")
        start = "0%{opacity:1}" if a <= 0 else f"0%,{self.P(a - f)}{{opacity:0}}{self.P(a)}{{opacity:1}}"
        end = "100%{opacity:1}" if b >= self.D else f"{self.P(b)}{{opacity:1}}{self.P(b + f)},100%{{opacity:0}}"
        self.css.append(f"@keyframes {k}{{{start}{end}}}")
        return f"animation-name:{k}"

    def kf(self, pts, ease="cubic-bezier(.4,0,.2,1)"):
        """pts: [(t, 'css decls'), ...] in time order; holds the first before and the last after."""
        k = self._name("k")
        body = [f"0%{{{pts[0][1]}}}"]
        body += [f"{self.P(t)}{{{c}}}" for t, c in pts]
        body.append(f"100%{{{pts[-1][1]}}}")
        self.css.append(f"@keyframes {k}{{{''.join(body)}}}")
        return f"animation-name:{k};animation-timing-function:{ease}"

    def rise(self, t, dy=28, d=0.6):
        return self.kf([(t, f"opacity:0;transform:translateY({dy}px)"), (t + d, "opacity:1;transform:none")])

    def window_rise(self, a, b, dy=24, f=0.35):
        """enters at a (rises), leaves at b (fades)."""
        return self.kf([(a - f, f"opacity:0;transform:translateY({dy}px)"), (a, "opacity:1;transform:none"),
                        (b, "opacity:1;transform:none"), (b + f, "opacity:0;transform:none")])

    def seq(self, frames, start, step, fit="cover", pos="50% 50%"):
        """image sequence: frame i visible from start+i*step; the last frame holds."""
        win = step * 1.05
        k = self._name("bf")
        self.css.append(f"@keyframes {k}{{0%{{opacity:0}}0.001%{{opacity:1}}{win / self.D * 100:.3f}%{{opacity:1}}"
                        f"{(win + 0.02) / self.D * 100:.3f}%,100%{{opacity:0}}}}")
        st = f"position:absolute;inset:0;width:100%;height:100%;object-fit:{fit};object-position:{pos};display:block"
        out = [f'<img src="{frames[0]}" alt="" style="{st}">']
        for i, f in enumerate(frames):
            out.append(f'<img src="{f}" alt="" style="{st};animation-name:{k};animation-timing-function:linear;'
                       f'animation-delay:{start + i * step:.3f}s">')
        th = start + len(frames) * step
        out.append(f'<img src="{frames[-1]}" alt="" style="{st};{self.kf([(th - .01, "opacity:0"), (th, "opacity:1")], "linear")}">')
        return "".join(out)

    def style(self):
        return "\n".join(self.css)
