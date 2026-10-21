#!/usr/bin/env python3
"""Commercial boundaries must survive the complete build and scheduled catalog sync."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,parse_qs,unquote
import json,re,runpy,unittest
ROOT=Path(__file__).resolve().parent.parent
HUMAN=['off-comercial','locucao-off','producao-para-igrejas','gravacao-off-e-producao','producao-para-supermercados','spot-black-friday']
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class Landings(unittest.TestCase):
 def test_routes_and_commercial_boundaries(self):
  for route in HUMAN+['locucao-ia']:
   with self.subTest(route=route):
    text=(ROOT/route/'index.html').read_text();p=Page(text)
    self.assertEqual(len(re.findall('<h1[ >]',text)),1)
    self.assertIn('https://alocucao.com.br/'+route+'/',text)
    self.assertNotIn('noindex',text);self.assertNotIn('http-equiv="refresh"',text)
    self.assertTrue(any(tag=='meta' and attrs.get('name')=='description' and attrs.get('content') for tag,attrs in p.tags))
    panels=[a.get('data-kind') for tag,a in p.tags if a.get('class')=='uv-panel']
    self.assertEqual(panels,['ia' if route=='locucao-ia' else 'human'])
    if route in HUMAN:
     plain=re.sub(r'<script\b.*?</script>','',text,flags=re.S)
     self.assertNotRegex(plain,r'(?i)vozes? IA|inteligência artificial|R\$ 8,50|R\$ 19,00|/vozes-ia/')
     self.assertEqual(len(re.findall('class="uv-row"',text)),10)
    else:self.assertNotRegex(text,r'R\$ 11,90|R\$ 29,90|data-kind="human"')
    for tag,attrs in p.tags:
     href=attrs.get('href','');u=urlsplit(href)
     if route!='gravacao-off-e-producao':self.assertFalse(any(x in href for x in ['/painel','/cadastro','/central']))
     if u.hostname=='wa.me':
      self.assertEqual(u.path,'/5527996529832');self.assertTrue(parse_qs(u.query).get('text'))
     if href.startswith('#'):self.assertTrue(any(a.get('id')==href[1:] for _,a in p.tags),href)
     for key in ['src','data-src']:
      src=attrs.get(key,'');path=unquote(urlsplit(src).path)
      if path.startswith('/assets/'):self.assertTrue((ROOT/path.lstrip('/')).is_file(),src)
    if route=='gravacao-off-e-producao':self.assertIn('https://vozes.alocucao.com.br/painel/cadastro',text)
    for content in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S):json.loads(content)
 def test_build_preserves_target_pages(self):
  normalize=runpy.run_path(str(ROOT/'scripts/standardize-layout.py'))['standardize_page']
  update=runpy.run_path(str(ROOT/'scripts/review-dual-positioning.py'))['update']
  for route in HUMAN+['locucao-ia']:
   path=ROOT/route/'index.html';text=path.read_text();self.assertEqual(normalize(text),text);self.assertEqual(update(text,path),text)
 def test_portfolio_and_distinct_off(self):
  self.assertIn('/assets/audio/igreja-evangelica-monte-moria.mp3',(ROOT/'producao-para-igrejas/index.html').read_text())
  self.assertIn('Off Comercial para quem produz publicidade',(ROOT/'off-comercial/index.html').read_text())
 def test_avatar_fallback(self):
  for route in HUMAN:
   t=(ROOT/route/'index.html').read_text()
   for avatar in re.findall(r'<div class="uv-avatar">(.*?)</div>',t,re.S):self.assertNotIn('<span>',avatar) if '<img ' in avatar else self.assertIn('<span>',avatar)
if __name__=='__main__':unittest.main()
