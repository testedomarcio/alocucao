#!/usr/bin/env python3
"""Audit canonical sitemap pages; --fix applies only reviewed consistency repairs."""
import argparse
from collections import defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = 'https://alocucao.com.br'
ADDRESS = 'Rua Euzebio Cirilo de Souza, 344, Centro'

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals, self.descriptions, self.robots, self.images = [], [], [], []
        self.scripts, self.script = [], None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in attrs.get('rel', '').split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta':
            name = attrs.get('name', '').lower()
            if name == 'description': self.descriptions.append(attrs.get('content', ''))
            if name == 'robots': self.robots.append(attrs.get('content', ''))
        if tag == 'img' and 'alt' not in attrs: self.images.append(attrs.get('src', ''))
        if tag == 'script' and attrs.get('type') == 'application/ld+json': self.script = ''
    def handle_data(self, data):
        if self.script is not None: self.script += data
    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.scripts.append(self.script)
            self.script = None

def repair(text):
    text = text.replace('Av. Firmino Teixeira Griffo, 344, Centro', ADDRESS)
    text = text.replace('Rua Ademar da Mota Couto, C/N - Centro - Brejetuba - Espírito Santo - Cep 29630-000', ADDRESS + ' - Brejetuba - ES - 29630-000')
    # Normalize link targets, never visible legal text or redirect destinations outside this origin.
    text = re.sub(r'((?:href|content)=["\'])(?:https://alocucao\.com\.br)?/termos-de-uso/?(?=["\'#?])', lambda m: m.group(1) + '/termos/', text)
    text = re.sub(r'((?:href|content)=["\'])(https://alocucao\.com\.br)?/termos(?=["\'#?])', lambda m: m.group(1) + (m.group(2) or '') + '/termos/', text)
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix', action='store_true')
    args = parser.parse_args()
    tree = ET.parse(ROOT / 'sitemap.xml')
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = [e.text.strip() for e in tree.findall('s:url/s:loc', ns)]
    errors, changed, titles, headings = [], [], defaultdict(list), defaultdict(list)
    if len(urls) != len(set(urls)): errors.append('Duplicate URLs in sitemap')
    for url in urls:
        parts = urlsplit(url)
        if parts.scheme != 'https' or parts.netloc != 'alocucao.com.br' or parts.query or parts.fragment:
            errors.append('Invalid sitemap URL: ' + url); continue
        local = ROOT / unquote(parts.path).lstrip('/')
        if local.is_dir(): local = local / 'index.html'
        if not local.resolve().is_relative_to(ROOT) or not local.is_file():
            errors.append('Missing sitemap page: ' + url); continue
        text = local.read_text(encoding='utf-8')
        if args.fix:
            updated = repair(text)
            if updated != text:
                local.write_text(updated, encoding='utf-8')
                changed.append(str(local.relative_to(ROOT)))
                text = updated
        meta = Metadata(); meta.feed(text)
        if meta.canonicals != [url]: errors.append('Canonical mismatch: ' + url + ' ' + repr(meta.canonicals))
        if len(meta.descriptions) != 1 or not meta.descriptions[0].strip(): errors.append('Missing or duplicate description: ' + url)
        if any('noindex' in r.lower() for r in meta.robots): errors.append('Sitemap page is noindex: ' + url)
        title = re.findall(r'<title\b[^>]*>(.*?)</title>', text, re.S | re.I)
        h1 = re.findall(r'<h1\b[^>]*>(.*?)</h1>', text, re.S | re.I)
        for label, values, inventory in [('title', title, titles), ('H1', h1, headings)]:
            if len(values) != 1: errors.append('Expected one ' + label + ': ' + url)
            else:
                value = re.sub(r'<[^>]+>', '', values[0]).strip()
                if not value: errors.append('Empty ' + label + ': ' + url)
                inventory[value].append(url)
        if meta.images: errors.append('Image without alt: ' + url)
        for raw in meta.scripts:
            try: json.loads(raw)
            except json.JSONDecodeError as exc: errors.append('Invalid JSON-LD: ' + url + ' ' + str(exc))
    for label, inventory in [('title', titles), ('H1', headings)]:
        for value, locations in inventory.items():
            if len(locations) > 1: errors.append('Duplicate ' + label + ': ' + repr(locations))
    print(json.dumps({'sitemap_pages': len(urls), 'changed_files': changed, 'errors': errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))

if __name__ == '__main__': main()
  
