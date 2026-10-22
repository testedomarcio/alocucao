#!/usr/bin/env python3
"""Commercial landing offers, external showcase and conversion boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,parse_qs,unquote
import json,re,runpy,unittest
ROOT=Path(__file__).resolve().parent.parent
MODEL=runpy.run_path(str(ROOT/'scripts/standardize-single-offer.py'))
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class Landings(unittest.TestCase):
 def test_routes_and_commercial_boundaries(self):
  for route in MODEL['ROUTES']:
   with self.subTest(route=route):
    text=(ROOT/route/'index.html').read_text();p=Page(text)
    self.assertEqual(len(re.findall('<h1[ >]',text)),1)
    self.assertNotIn('noindex',text)
    self.assertTrue(any(tag=='meta' and a.get('name')=='description' and a.get('content') for tag,a in p.tags))
    ids=[a['id'] for _,a in p.tags if a.get('id')]
    self.assertEqual(len(ids),len(set(ids)))
    frames=[a for tag,a in p.tags if tag=='iframe']
    self.assertEqual(len(frames),1)
    self.assertEqual(frames[0].get('src'),'https://vozes.alocucao.com.br/embed.php')
    self.assertEqual(frames[0].get('id'),'vitrine-vozes')
    self.assertNotIn('uv-catalog',text)
    self.assertNotIn('/assets/unified-voices.js',text)
    self.assertNotIn('al-pricing-dual-grid',text)
    self.assertNotIn('dual-offer:start',text)
    self.assertNotRegex(text,r'R\$\s*(?:11,90|29,90|8,50|19,00|8,90|16,90)')
    self.assertTrue('somente voz sem edição' in text.lower())
    self.assertIn('R$ 12,00',text);self.assertIn('R$ 30,00',text)
    self.assertEqual(len([a for _,a in p.tags if a.get('class')=='sf-floating']),1)
    self.assertEqual(len([a for _,a in p.tags if a.get('class')=='sf-mobile']),1)
    offers=[]
    def visit(obj):
     if isinstance(obj,dict):
      if obj.get('@type')=='Offer':offers.append(obj)
      for v in obj.values():visit(v)
     elif isinstance(obj,list):
      for v in obj:visit(v)
    for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S):visit(json.loads(raw))
    self.assertTrue(offers)
    self.assertEqual({str(o['price']) for o in offers},{'12.00','30.00'})
    for tag,a in p.tags:
     href=a.get('href','');u=urlsplit(href)
     self.assertFalse(any(x in href for x in ['/painel','/cadastro','/central']),href)
     if u.hostname=='wa.me':self.assertEqual(u.path,'/5527996529832');self.assertTrue(parse_qs(u.query).get('text'))
     if href.startswith('#'):self.assertIn(href[1:],ids)
     if tag=='a' and set(a.get('class','').split())&{'btn','sf-button','sf-floating','panel-primary','al-header-cta'} and not href.startswith('#'):self.assertEqual(u.hostname,'wa.me',href)
     for key in ['src','href','data-src']:
      src=a.get(key,'');path=unquote(urlsplit(src).path)
      if path.startswith('/assets/'):self.assertTrue((ROOT/path.lstrip('/')).is_file(),src)
 def test_idempotent_and_home_excluded(self):
  self.assertNotIn('',MODEL['ROUTES']);self.assertNotIn('vozes',MODEL['ROUTES'])
  for route in MODEL['ROUTES']:
   text=(ROOT/route/'index.html').read_text();self.assertEqual(MODEL['update'](text,route),text,route)
  home=(ROOT/'index.html').read_text()
  self.assertNotIn('data-single-offer',home);self.assertNotIn('single-offer-landings',home)
  self.assertIn('data-layout="tabs"',home)
 def test_real_audio_samples_preserved(self):
  self.assertIn('/assets/audio/igreja-evangelica-monte-moria.mp3',(ROOT/'producao-para-igrejas/index.html').read_text())
  self.assertIn('/assets/audio/spot-clinica-ecoar.mp3',(ROOT/'spot-comercial/index.html').read_text())
 def test_external_message_boundary(self):
  script=(ROOT/'assets/single-offer-landings.js').read_text()
  self.assertIn("event.origin !== 'https://vozes.alocucao.com.br'",script)
  self.assertIn('event.source !== frame.contentWindow',script)
  self.assertIn('Number.isFinite(height)',script)
if __name__=='__main__':unittest.main()
