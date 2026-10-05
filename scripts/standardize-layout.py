#!/usr/bin/env python3
"""Shared static navigation: usable and crawlable without JavaScript."""
from pathlib import Path
import re
from runpy import run_path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / 'templates/site-header.html').read_text().strip()
FOOTER = (ROOT / 'templates/site-footer.html').read_text().strip()
CSS = '<link rel="stylesheet" href="/assets/site-layout.css?v=20261005-brand">'
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
    text = text.replace("</head>", '<link rel="stylesheet" href="/assets/panel-commerce.css?v=20261005-prices">\n</head>')
    text = re.sub(r'/assets/voice-profile.js(?:\?[^"\s<>]+)?', '/assets/voice-profile.js?v=20261005-whatsapp', text)
    if 'data-panel-page' in text:
        text = re.sub(r'<a class="al-header-cta"[^>]*>.*?</a>', '<a class="al-header-cta al-support-cta" href="https://wa.me/5527996529832" target="_blank" rel="noopener" data-panel-support data-cta="cabecalho_whatsapp">Suporte WhatsApp</a>', text, count=1)
    text = run_path(str(ROOT / 'scripts/whatsapp-commerce.py'))['normalize_whatsapp'](text)
    text = run_path(str(ROOT / 'scripts/site-prices.py'))['normalize_prices'](text)
    text = re.sub(r'/assets/voice-bank.js(?:\?[^"\s<>]+)?', '/assets/voice-bank.js?v=20261005-vl', text)
    text = re.sub(r'/assets/featured-voices.js(?:\?[^"\s<>]+)?', '/assets/featured-voices.js?v=20261005-vl', text)
    # Apply the official brand to every generated page as well as existing pages.
    text = re.sub(r'<link\b[^>]*rel=["\'](?:icon|shortcut icon|apple-touch-icon)["\'][^>]*>\s*', '', text, flags=re.I)
    icons = '<link rel="icon" href="/assets/brand/favicon-64.png?v=20261005" type="image/png" sizes="64x64">\n<link rel="icon" href="/favicon.ico?v=20261005" sizes="any">\n<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">'
    text = text.replace('</head>', icons + '\n</head>')
    text = re.sub(r'("logo"\s*:\s*")https://alocucao.com.br/favicon.svg(")', r'\1https://alocucao.com.br/assets/brand/a-locucao-logo.png\2', text)
    text = text.replace('https://alocucao.com.br/favicon.svg', 'https://alocucao.com.br/assets/brand/icon-192.png')
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
