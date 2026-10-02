#!/usr/bin/env python3
"""Shared static navigation: usable and crawlable without JavaScript."""
from pathlib import Path
import re
from runpy import run_path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / 'templates/site-header.html').read_text().strip()
FOOTER = (ROOT / 'templates/site-footer.html').read_text().strip()
CSS = '<link rel="stylesheet" href="/assets/site-layout.css?v=20261002">'
JS = '<script src="/assets/site-layout.js?v=20261002" defer></script>'

def standardize_page(text):
    if re.search(r'http-equiv=["\']refresh', text, re.I) or '<body' not in text:
        return text
    if '<!-- site-header:start -->' in text:
        text = re.sub(r'<!-- site-header:start -->.*?<!-- site-header:end -->', lambda _: HEADER, text, flags=re.S)
    else:
        text = re.sub(r'<header\b[^>]*>.*?</header>', lambda _: HEADER, text, count=1, flags=re.S)
    if '<!-- site-footer:start -->' in text:
        text = re.sub(r'<!-- site-footer:start -->.*?<!-- site-footer:end -->', lambda _: FOOTER, text, flags=re.S)
    else:
        text = re.sub(r'<footer\b[^>]*>.*?</footer>', lambda _: FOOTER, text, count=1, flags=re.S)
    if '<!-- site-header:start -->' not in text or '<!-- site-footer:start -->' not in text:
        raise ValueError('Content page lacks header/footer')
    # Keep the shared rules last so legacy per-page CSS cannot change navigation.
    text = re.sub(r'<link\b[^>]*href=["\']/assets/site-layout\.css[^"\']*["\'][^>]*>\s*', '', text)
    text = text.replace('</head>', CSS + '\n</head>')
    text = re.sub(r'<script\b[^>]*src=["\']/assets/site-layout\.js[^"\']*["\'][^>]*>\s*</script>\s*', '', text)
    text = text.replace('</body>', JS + '\n</body>')
    text = run_path(str(ROOT / "scripts/panel-commerce.py"))["normalize_page"](text)
    text = re.sub(r'<link\b[^>]*href=["\']/assets/panel-commerce\.css[^"\']*["\'][^>]*>\s*', '', text)
    text = text.replace("</head>", '<link rel="stylesheet" href="/assets/panel-commerce.css?v=20261002-1">\n</head>')
    text = re.sub(r'/assets/voice-bank.js(?:\?[^"\s<>]+)?', '/assets/voice-bank.js?v=20261002-lb-2', text)
    text = re.sub(r'/assets/featured-voices.js(?:\?[^"\s<>]+)?', '/assets/featured-voices.js?v=20261002-lb', text)
    text = re.sub(r'/assets/voice-profile.js(?:\?[^"\s<>]+)?', '/assets/voice-profile.js?v=20261002-lb', text)
    return text

def main():
    changed = 0
    for page in sorted(ROOT.rglob('*.html')):
        if any(part.startswith('.') or part in ('node_modules', '_site') for part in page.relative_to(ROOT).parts):
            continue
        if page.name in ('site-header.html', 'site-footer.html'):
            continue
        old = page.read_text()
        new = standardize_page(old)
        if new != old:
            page.write_text(new); changed += 1
    print(f'Standardized layout: {changed} files changed')

if __name__ == '__main__':
    main()
