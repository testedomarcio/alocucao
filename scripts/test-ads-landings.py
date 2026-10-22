#!/usr/bin/env python3
"""Verify current prices, selected catalog, lazy media and WhatsApp-only order exits."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,parse_qs,unquote
import json,re,runpy,unittest
ROOT=Path(__file__).resolve().parent.parent
MODEL=runpy.run_path(str(ROOT/'scripts/refresh-whatsapp-site.py'))
LANDINGS=runpy.run_path(str(ROOT/'scripts/standardize-single-offer.py'))['ROUTES']
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class Landings(unittest.TestCase):
 def test_sitewide_order_exits_and_prices(self):
  for path in ROOT.rglob('*.html'):
   if any(p.startswith('.') or p in {'node_modules','_site'} for p in path.relative_to(ROOT).parts):continue
   with self.subTest(path=str(path.relative_to(ROOT))):
    text=path.read_text();page=Page(text)
    self.assertFalse(bool(re.search(r'R\$\s*(?:11,90|29,90|8,50|19,00|8,90|16,90)',text)))
    for tag,a in page.tags:
     href=a.get('href','')
     if tag=='a':self.assertFalse(MODEL['is_order_url'](href),href)
     if tag=='a' and set(a.get('class','').split())&{'sv-order','btn','ia-btn','sf-button','sf-floating','panel-primary','al-header-cta'} and href and not href.startswith('#'):
      self.assertEqual(urlsplit(href).hostname,'wa.me',href)
 def test_catalog_complete_and_no_symbol(self):
  voices=MODEL['selected_voices']();self.assertTrue(voices)
  allsource=json.loads((ROOT/'assets/voices-catalog.json').read_text())['voices']
  self.assertEqual({v['id'] for v in voices},{v['id'] for v in allsource if '🧠' in v['name']})
  for route in ['', 'vozes','locutores','calculadora','portfolio']+LANDINGS:
   with self.subTest(route=route):
    text=(ROOT/route/'index.html').read_text();p=Page(text)
    self.assertEqual(text.count('data-selected-voices'),1)
    self.assertEqual(text.count('class="sv-card"'),len(voices))
    self.assertNotIn('vitrine-vozes',text)
    self.assertNotIn('uv-catalog',text)
    bank=re.search(r'<!-- selected-voices:start -->(.*?)<!-- selected-voices:end -->',text,re.S)[1]
    self.assertNotIn('🧠',bank)
    self.assertIn('Conheça mais vozes pelo WhatsApp',bank)
    audio=[a for tag,a in Page(bank).tags if tag=='audio']
    self.assertEqual(len(audio),len(voices));self.assertTrue(all(a.get('preload')=='none' for a in audio))
    self.assertEqual({a['src'] for a in audio},{v['audio'] for v in voices})
    quotes=[a for tag,a in Page(bank).tags if a.get('data-cta')=='selected_voice_quote']
    self.assertEqual(len(quotes),len(voices))
    for a in quotes:
     message=parse_qs(urlsplit(a['href']).query)['text'][0]
     self.assertIn(a['data-voice-name'],message)
 def test_schema_and_page_integrity(self):
  for route in ['', 'vozes','locutores']+LANDINGS:
   with self.subTest(route=route):
    text=(ROOT/route/'index.html').read_text();p=Page(text)
    self.assertEqual(len(re.findall('<h1[ >]',text)),1)
    ids=[a['id'] for _,a in p.tags if a.get('id')];self.assertEqual(len(ids),len(set(ids)))
    for tag,a in p.tags:
     href=a.get('href','')
     if href.startswith('#'):self.assertIn(href[1:],ids,href)
     for key in ['src','href','data-src']:
      src=a.get(key,'');local=unquote(urlsplit(src).path)
      if local.startswith('/assets/'):self.assertTrue((ROOT/local.lstrip('/')).is_file(),src)
    offers=[]
    def visit(o):
     if isinstance(o,dict):
      if o.get('@type')=='Offer':offers.append(o)
      for v in o.values():visit(v)
     elif isinstance(o,list):
      for v in o:visit(v)
    for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S):visit(json.loads(raw))
    for offer in offers:
     self.assertIn(str(offer.get('price')),{'12.00','30.00'})
     if 'Off' in offer.get('name',''):self.assertEqual(str(offer['price']),'12.00')
 def test_final_pass_is_idempotent(self):
  voices=MODEL['selected_voices']()
  for route in ['', 'vozes','locutores']+LANDINGS:
   text=(ROOT/route/'index.html').read_text();self.assertTrue(MODEL['update'](text,route,voices)==text,route)
 def test_real_samples_preserved(self):
  self.assertIn('/assets/audio/igreja-evangelica-monte-moria.mp3',(ROOT/'producao-para-igrejas/index.html').read_text())
  self.assertIn('/assets/audio/spot-clinica-ecoar.mp3',(ROOT/'spot-comercial/index.html').read_text())
if __name__=='__main__':unittest.main()
