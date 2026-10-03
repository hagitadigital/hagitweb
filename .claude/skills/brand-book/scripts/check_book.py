#!/usr/bin/env python3
"""Check a brand book: brand-book.json is complete and matches brand-book.html,
and the HTML is free of the problems we already fixed once.

  python3 check_book.py <slug>                      # a world: <root>/<slug>/brand-book.*
  python3 check_book.py --dir <path-to-folder>      # a client site: <folder>/brand-book.*

Exit code 1 when something must be fixed.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # repo root: .claude/skills/brand-book/scripts/..
HEX = re.compile(r"^#[0-9A-F]{6}$")
LATIN_NAME = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’.\- ]*°")
LTR_CLASSES = {"ltr", "wm", "stamp", "hex", "fr", "hr"}
SKIP_TAGS = {"script", "style", "title", "svg", "noscript"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class TextScan(HTMLParser):
    """Collect text nodes that sit in RTL context and hold a Latin name with °."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []  # (tag, is_ltr, is_skip)
        self.hits = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        parent_ltr = self.stack[-1][1] if self.stack else False
        parent_skip = self.stack[-1][2] if self.stack else False
        is_ltr = parent_ltr or a.get("dir") == "ltr" or bool(classes & LTR_CLASSES)
        if a.get("dir") == "rtl":
            is_ltr = False
        self.stack.append((tag, is_ltr, parent_skip or tag in SKIP_TAGS))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if not self.stack or self.stack[-1][1] or self.stack[-1][2]:
            return
        for m in LATIN_NAME.finditer(data):
            self.hits.append((self.getpos()[0], m.group(0).strip(), data.strip()[:70]))


def check_json(book, html, errors, warnings):
    def need(cond, msg):
        if not cond:
            errors.append(msg)

    for key in ("brand", "decision", "codes", "palette", "type", "voice", "cover_test", "touchpoints", "rules"):
        need(key in book, f"json: missing '{key}'")
    if errors:
        return

    b = book["brand"]
    for k in ("name", "slug", "book_url", "fictional", "thesis"):
        need(b.get(k) not in (None, ""), f"json: brand.{k} is empty")
    if b.get("name"):
        need(b["name"] in html, f"json: brand.name '{b['name']}' does not appear in the page")

    d = book["decision"]
    for k in ("promise", "element", "result", "why_not_compared"):
        need(bool(d.get(k)), f"json: decision.{k} is empty")
    for k in ("promise", "element"):
        if d.get(k) and d[k].rstrip(".") not in html:
            warnings.append(f"json: decision.{k} '{d[k]}' is not written as-is in the page")

    codes = book["codes"]
    need(3 <= len(codes) <= 5, f"json: {len(codes)} codes — a book has 3 to 5")
    for c in codes:
        need(bool(c.get("name")) and bool(c.get("rule")), f"json: code without name or rule: {c}")
        if c.get("name") and c["name"] not in html:
            errors.append(f"json: code '{c['name']}' does not appear in the page")

    for p in book["palette"]:
        hx = p.get("hex", "")
        need(bool(HEX.match(hx)), f"json: palette hex '{hx}' must be #RRGGBB in capitals")
        if hx and hx.lower() not in html.lower():
            errors.append(f"json: palette {hx} ({p.get('name')}) does not appear in the page")

    v = book["voice"]
    need(bool(v.get("tone")), "json: voice.tone is empty")
    need(len(v.get("examples", [])) == 3, "json: voice.examples needs exactly three lines")
    need(bool(v.get("never")), "json: voice.never is empty")

    need(len(book["cover_test"]) == 4, f"json: cover_test has {len(book['cover_test'])} details — it needs four")

    known = {c.get("name") for c in codes} | {p.get("name") for p in book["palette"]}
    for group in ("cover_test", "touchpoints"):
        for item in book[group]:
            for name in item.get("codes", []):
                if name not in known:
                    warnings.append(f"json: {group} names '{name}', which is neither a code nor a palette colour")
            img = item.get("image")
            if img and not (ROOT / img.lstrip("/")).exists():
                warnings.append(f"json: {group} image {img} not found in the repo")

    r = book["rules"]
    for k in ("never_changes", "may_change", "breaking_mistake"):
        need(bool(r.get(k)), f"json: rules.{k} is empty")

    if book["type"].get("numerals") not in (None, "lining"):
        errors.append("json: type.numerals must be 'lining'")


def check_html(html, errors, warnings):
    if 'href="brand-book.json"' not in html:
        errors.append('html: <link rel="alternate" type="application/json" title="brand-book" href="brand-book.json"> missing from <head>')

    scan = TextScan()
    scan.feed(html)
    # A Latin name with ° flips even when it is alone in its element (<b>ORÉVA°</b>
    # inside a Hebrew paragraph), so every unwrapped one counts.
    for line, name, ctx in scan.hits:
        errors.append(f"html:{line}: '{name}' sits in RTL text without <span class=\"ltr\"> — it can flip ({ctx!r})")

    for m in re.finditer(r'<a class="btn[^"]*"[^>]*>([^<]*)<span class="ltr">(&nbsp;)?', html):
        line = html.count("\n", 0, m.start()) + 1
        before, inner = m.group(1), m.group(2)
        if inner:
            errors.append(f"html:{line}: &nbsp; inside the .ltr span of a button — put it before the span")
        elif before and not before.endswith("&nbsp;") and not before.endswith(" "):
            errors.append(f"html:{line}: button text before <span class=\"ltr\"> needs &nbsp; — a plain space is swallowed in inline-flex")

    if "Cormorant" in html and "lining-nums" not in html:
        errors.append("html: Cormorant Garamond is loaded but nothing sets font-variant-numeric: lining-nums — hours will use old-style figures")

    if "bws-legal" not in html:
        warnings.append("html: the legal line (privacy · terms · accessibility) is missing")
    if "/studio.html#books" not in html:
        warnings.append("html: footer does not link to /studio.html#books")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--dir", help="folder holding brand-book.html and brand-book.json (client sites)")
    args = ap.parse_args()
    if not args.slug and not args.dir:
        ap.error("give a slug or --dir")
    folder = Path(args.dir) if args.dir else ROOT / args.slug

    errors, warnings = [], []
    html_path, json_path = folder / "brand-book.html", folder / "brand-book.json"
    html = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    if not html:
        errors.append(f"{html_path} not found")
    if not json_path.exists():
        errors.append(f"{json_path} not found")
    else:
        try:
            book = json.loads(json_path.read_text(encoding="utf-8"))
            check_json(book, html, errors, warnings)
        except json.JSONDecodeError as e:
            errors.append(f"json: not valid JSON — {e}")
    if html:
        check_html(html, errors, warnings)

    for w in warnings:
        print("warn  ", w)
    for e in errors:
        print("ERROR ", e)
    print(f"\n{folder.name}: {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
