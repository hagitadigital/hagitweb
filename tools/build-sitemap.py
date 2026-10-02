#!/usr/bin/env python3
"""Build sitemap.xml from the committed site, with a lastmod that means "the content changed".

Usage:
    python tools/build-sitemap.py            # write sitemap.xml
    python tools/build-sitemap.py --dry-run  # print the diff against the current sitemap only

See tools/README.md for the rules.
"""
import argparse, html, os, re, subprocess, sys
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://hagitantebi.co.il/'
IL = timezone(timedelta(hours=3))
IGNORE_FILE = os.path.join(ROOT, 'tools', 'sitemap-ignore-commits.txt')
# Never sitemap pages: labs, ad renders, recording stages, partials, a separate client site.
EXCLUDE_PREFIXES = ('_', '.', 'node_modules/', 'brandworld_ad/', 'hagit_agent_movie/', 'hila-sharon/',
                    'sonair/src/', 'carousel-skill-html-rendering/')
EXCLUDE_FILES = {'404.html'}
DEFAULT_CHANGEFREQ, DEFAULT_PRIORITY = 'monthly', '0.6'


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True).stdout.decode('utf-8', 'replace')


def url_for(path):
    if path == 'index.html':
        return SITE
    if path.endswith('/index.html'):
        return SITE + path[:-len('index.html')]
    return SITE + path


def fingerprint(src):
    """Title + meta description + visible body copy. Ignores scripts, styles, nav, footer and
    read-more/related blocks, so tracking snippets, footer links and link swaps don't count."""
    if not src:
        return ''
    title = ' '.join(re.findall(r'<title>(.*?)</title>', src, re.S))
    desc = ' '.join(re.findall(r'<meta\s+name=["\x27]description["\x27]\s+content=["\x27]([^"\x27]*)', src, re.I))
    body = re.search(r'<body.*?</body>', src, re.S)
    body = body.group(0) if body else src
    body = re.sub(r'<(script|style|svg|noscript|nav|footer)\b.*?</\1>', ' ', body, flags=re.S | re.I)
    body = re.sub(r'<(section|div)\s+class="(?:read-more|related)[^"]*".*?</\1>', ' ', body, flags=re.S)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    return re.sub(r'\s+', ' ', f'{title} {desc} {text}').strip()


def is_noindex(src):
    return any('robots' in m.lower() and 'noindex' in m.lower() for m in re.findall(r'<meta[^>]*>', src, re.I))


def exclusion_reason(path, src, now):
    if path in EXCLUDE_FILES or path.startswith(EXCLUDE_PREFIXES):
        return 'excluded path'
    if is_noindex(src):
        return 'noindex'
    if re.search(r'<meta[^>]+http-equiv=["\x27]refresh["\x27]', src, re.I):
        return 'redirect stub'
    link = next((t for t in re.findall(r'<link[^>]*>', src, re.I) if re.search(r'rel=["\x27]canonical["\x27]', t, re.I)), None)
    href = re.search(r'href=["\x27]([^"\x27]+)["\x27]', link) if link else None
    if not href:
        return 'no canonical'
    if href.group(1).rstrip('/') != url_for(path).rstrip('/'):
        return 'canonical points elsewhere'
    pub = re.search(r'"datePublished":\s*"([^"]+)"', src)
    if pub:
        try:
            d = datetime.fromisoformat(pub.group(1))
            d = d if d.tzinfo else d.replace(tzinfo=IL)
            if d > now:
                return f'datePublished in the future ({pub.group(1)})'
        except ValueError:
            pass
    return None


def content_lastmod(path, ignored):
    """Date of the newest commit that changed the page's fingerprint."""
    log = [l.split() for l in git('log', '--format=%H %cs', '--', path).splitlines() if l.strip()]
    for sha, day in log:
        if sha in ignored and path not in ignored[sha]:
            continue
        after = fingerprint(git('show', f'{sha}:{path}'))
        before = fingerprint(git('show', f'{sha}^:{path}'))  # '' when the commit created the file
        if after != before:
            return day
    return log[-1][1] if log else None  # every change was ignored: fall back to creation date


def load_ignored():
    """{full sha: {paths the commit still counts for}} from tools/sitemap-ignore-commits.txt.
    Line format: `<sha> [!path ...]  # reason`."""
    out = {}
    if not os.path.exists(IGNORE_FILE):
        return out
    for line in open(IGNORE_FILE, encoding='utf-8'):
        parts = line.split('#')[0].split()
        if parts:
            sha = git('rev-parse', '--verify', '--quiet', parts[0] + '^{commit}').strip()
            if not sha:
                print(f'  ! ignore list: unknown commit {parts[0]} (squash-merged or rebased?)')
                continue
            out[sha] = {p[1:] for p in parts[1:] if p.startswith('!')}
    return out


def old_entries(xml):
    return {m.group(1): (m.group(2), m.group(3)) for m in re.finditer(
        r'<loc>([^<]+)</loc>.*?<changefreq>([^<]+)</changefreq>\s*<priority>([^<]+)</priority>', xml, re.S)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    now = datetime.now(IL)
    ignored = load_ignored()
    sm_path = os.path.join(ROOT, 'sitemap.xml')
    committed_xml = git('show', 'HEAD:sitemap.xml')
    meta = old_entries(committed_xml)

    entries, skipped = [], []
    for path in sorted(git('ls-files', '*.html').splitlines()):  # committed files only
        src = git('show', f'HEAD:{path}')
        why = exclusion_reason(path, src, now)
        if why:
            skipped.append((path, why))
            continue
        url = url_for(path)
        cf, pr = meta.get(url, (DEFAULT_CHANGEFREQ, DEFAULT_PRIORITY))
        entries.append((url, content_lastmod(path, ignored), cf, pr))

    entries.sort(key=lambda e: (-float(e[3]), e[0] != SITE, e[0]))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- Generated by tools/build-sitemap.py — do not edit by hand. -->',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lm, cf, pr in entries:
        xml += ['  <url>', f'    <loc>{url}</loc>', f'    <lastmod>{lm}</lastmod>',
                f'    <changefreq>{cf}</changefreq>', f'    <priority>{pr}</priority>', '  </url>']
    xml.append('</urlset>\n')

    old = set(re.findall(r'<loc>([^<]+)</loc>', committed_xml))
    new = {e[0] for e in entries}
    print(f'{len(entries)} URLs  (was {len(old)})')
    for u in sorted(new - old):
        print('  + ' + u)
    for u in sorted(old - new):
        why = next((w for p, w in skipped if url_for(p) == u), 'file not committed / missing')
        print(f'  - {u}  ({why})')
    if not a.dry_run:
        open(sm_path, 'w', encoding='utf-8', newline='\n').write('\n'.join(xml))
        print('wrote sitemap.xml')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
