#!/usr/bin/env python3
"""Link a finished brand book into the site, in the three places it belongs:

  1. the card in its world      <slug>/index.html   (a.book-link inside the Studio Note)
  2. the card in the studio     studio.html         (a.book-card in Les Livres, before <!-- more books -->)
  3. the sitemap                sitemap.xml         (a <url> before </urlset>)

Name, world number and title come from <slug>/brand-book.json. Each step is skipped
when the link is already there, so running it twice changes nothing.

World:
  python3 link_book.py encore --image /encore/assets/touchpoints/bags-four.webp --image-size 900x1125 \
      --alt "..." --chips "חמישה קודים,ארבע שעות,מבחן הכיסוי,נקודות מגע" \
      --card-text "..." --world-line "..." --accent "#853A26" --dark "#241212" --light "#D9B26A"

Client site (sitemap only):
  python3 link_book.py --root ../client-site --site-url https://client.co.il --book-path brand-book.html --sitemap-only
"""
import argparse
import datetime
import html as H
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[4]
SITE = "https://hagitantebi.co.il"
ALT_LINK = '<link rel="alternate" type="application/json" title="brand-book" href="brand-book.json">'


def esc(s):
    return H.escape(s, quote=True)


def event_name(slug):
    return slug.replace("-", " ").title().replace(" ", "")


def world_card(a, book, indent):
    p = indent
    return (
        f'{p}<a class="book-link" href="brand-book.html" style="display:flex;flex-direction:column;gap:6px;margin:8px 0;'
        f'padding:22px 26px;background:#fff;border:1px solid {a.border};border-inline-start:3px solid {a.accent};'
        f'text-decoration:none;color:{a.ink or a.dark}" '
        f"onclick=\"if(typeof fbq==='function')fbq('trackCustom','{event_name(a.slug)}BookOpen')\">\n"
        f'{p}  <span style="font-size:.8rem;letter-spacing:.16em;opacity:.8">ספר המותג המקוצר</span>\n'
        f"{p}  <span style=\"font-family:'Frank Ruhl Libre',serif;font-size:1.25rem;line-height:1.4\">{esc(a.world_line)}</span>\n"
        f'{p}  <span style="font-size:.9rem;font-weight:500;color:{a.accent}">לפתוח את הספר ←</span>\n'
        f"{p}</a>\n"
    )


def studio_card(a, book):
    b = book["brand"]
    w, h = a.image_size.lower().split("x")
    kicker = "ספר מותג מקוצר" + (f" · עולם מס׳ {b['world_no']}" if b.get("world_no") else "")
    chips = "".join(f"<span>{esc(c.strip())}</span>" for c in a.chips.split(",") if c.strip())
    s = " " * 12
    return (
        f'{s}<a class="book-card" href="/{a.slug}/brand-book.html" style="--bk:{a.dark};--bk-accent:{a.light}">\n'
        f'{s}    <div class="book-card__ph">\n'
        f'{s}        <img src="{esc(a.image)}" width="{w}" height="{h}" loading="lazy" alt="{esc(a.alt)}">\n'
        f"{s}    </div>\n"
        f'{s}    <div class="book-card__body">\n'
        f'{s}        <div class="book-card__kicker">{kicker}</div>\n'
        f'{s}        <div class="book-card__name">{esc(b["name"])}</div>\n'
        f'{s}        <div class="book-card__title">{esc(b["thesis"])}</div>\n'
        f'{s}        <p class="book-card__text">{esc(a.card_text)}</p>\n'
        f'{s}        <div class="book-card__chips">{chips}</div>\n'
        f'{s}        <span class="book-card__go">לפתוח את ספר המותג ←</span>\n'
        f"{s}    </div>\n"
        f"{s}</a>\n"
    )


def sitemap_entry(loc, lastmod):
    return (
        "\n  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{lastmod}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.6</priority>\n"
        "  </url>\n"
    )


def link_world(a, book, root, changes):
    path = root / a.slug / "index.html"
    src = path.read_text(encoding="utf-8")
    out = src
    if 'class="book-link"' in src and 'href="brand-book.html"' in src:
        print(f"skip  {path.relative_to(root)}: book card already there")
    else:
        marker = "<!-- brand-book-link -->"
        if marker in out:
            i = out.index(marker)
            indent = out[out.rfind("\n", 0, i) + 1 : i]
            out = out.replace(marker, world_card(a, book, indent).lstrip(" ").rstrip("\n"), 1)
        else:
            note = out.find('id="studio-note"')
            end = out.find("Run by AI.</p>", note) if note != -1 else -1
            if end == -1:
                sys.exit(f"{path}: no Studio Note paragraph ending in 'Run by AI.</p>'. "
                         f"Put {marker} where the card should go and run again.")
            line_start = out.rfind("\n", 0, end) + 1
            indent = re.match(r"\s*", out[line_start:]).group(0)
            at = out.index("\n", end) + 1
            out = out[:at] + world_card(a, book, indent) + out[at:]
        print(f"add   {path.relative_to(root)}: book card in the Studio Note")
    if 'href="brand-book.json"' not in out and (root / a.slug / "brand-book.json").exists():
        out = out.replace("</head>", ALT_LINK + "\n</head>", 1)
        print(f"add   {path.relative_to(root)}: <link rel=alternate> to brand-book.json")
    if out != src:
        changes[path] = out


def link_studio(a, book, root, changes):
    path = root / "studio.html"
    src = path.read_text(encoding="utf-8")
    if f'href="/{a.slug}/brand-book.html"' in src:
        print("skip  studio.html: card already in Les Livres")
        return
    marker = "<!-- more books -->"
    if marker not in src:
        sys.exit(f"studio.html: '{marker}' not found in the Les Livres grid")
    i = src.index(marker)
    line_start = src.rfind("\n", 0, i) + 1
    changes[path] = src[:line_start] + studio_card(a, book) + src[line_start:]
    print("add   studio.html: card in Les Livres")


def link_sitemap(loc, root, changes):
    path = root / "sitemap.xml"
    src = changes.get(path) or path.read_text(encoding="utf-8")
    if f"<loc>{loc}</loc>" in src:
        print(f"skip  sitemap.xml: {loc} already listed")
        return
    i = src.rindex("</urlset>")
    changes[path] = src[:i].rstrip("\n") + "\n" + sitemap_entry(loc, datetime.date.today().isoformat()) + src[i:]
    print(f"add   sitemap.xml: {loc}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    ap.add_argument("--site-url", default=SITE)
    ap.add_argument("--book-path", help="path of the book under the site root (default <slug>/brand-book.html)")
    ap.add_argument("--sitemap-only", action="store_true")
    ap.add_argument("--image")
    ap.add_argument("--image-size", help="WxH, e.g. 900x1125")
    ap.add_argument("--alt")
    ap.add_argument("--chips", help="comma separated, e.g. 'חמישה קודים,ארבע שעות,מבחן הכיסוי,נקודות מגע'")
    ap.add_argument("--card-text", help="one line about the world, for the studio card")
    ap.add_argument("--world-line", help="one line for the card in the world")
    ap.add_argument("--accent", help="the world's warm accent: card border and 'open' link")
    ap.add_argument("--dark", help="the world's dark colour (studio card --bk)")
    ap.add_argument("--light", help="the world's light accent (studio card --bk-accent)")
    ap.add_argument("--ink", help="text colour of the world card (default: --dark)")
    ap.add_argument("--border", default="#D9CEC0", help="thin border of the world card")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    root = a.root.resolve()
    changes = {}
    site = a.site_url.rstrip("/")

    if a.sitemap_only:
        if not a.book_path and not a.slug:
            ap.error("--sitemap-only needs --book-path or a slug")
        link_sitemap(f"{site}/{(a.book_path or f'{a.slug}/brand-book.html').lstrip('/')}", root, changes)
    else:
        if not a.slug:
            ap.error("give the world's slug")
        missing = [f for f in ("image", "image_size", "alt", "chips", "card_text", "world_line", "accent", "dark", "light")
                   if not getattr(a, f)]
        if missing:
            ap.error("missing: " + ", ".join("--" + m.replace("_", "-") for m in missing))
        book = json.loads((root / a.slug / "brand-book.json").read_text(encoding="utf-8"))
        link_world(a, book, root, changes)
        link_studio(a, book, root, changes)
        link_sitemap(f"{site}/{(a.book_path or f'{a.slug}/brand-book.html').lstrip('/')}", root, changes)

    if a.dry_run:
        print(f"\n--dry-run: {len(changes)} file(s) would change")
        return
    for path, text in changes.items():
        path.write_text(text, encoding="utf-8")
    print(f"\n{len(changes)} file(s) updated")


if __name__ == "__main__":
    main()
