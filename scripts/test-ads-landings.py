#!/usr/bin/env python3
"""Check the public dual-channel journey, current prices, embeds, schema and sample preservation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,runpy,unittest
ROOT=Path(__file__).resolve().parent.parent
MODEL=runpy.run_path(str(ROOT/'scripts/integrate-recording-panel.py'))
class Page(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
class Landings(unittest.TestCase):
 def test_prices_and_no_legacy_catalog(self):
  for path in ROOT.rglob('*.html'):
   if any(p.startswith('.') or p in {'node_modules','_site'} for p in path.relative_to(ROOT).parts):continue
   with self.subTest(path=str(path.relative_to(ROOT))):
    text=path.read_text()
    retail=re.sub(r'<!-- commercial-packages:start -->.*?<!-- commercial-packages:end -->','',text,flags=re.S)
    self.assertFalse(bool(re.search(r'R\$\s*(?:10,00|25,00|12,00|11,90|29,90|8,50|19,00|8,90|16,90)',retail)))
    self.assertNotIn('data-selected-voices',text)
    self.assertNotIn('/assets/selected-voices.js',text)
 def test_commercial_journey(self):
  for route in MODEL['COMMERCIAL']:
   with self.subTest(route=route):
    text=(ROOT/route/'index.html').read_text();tags=Page(text).tags
    self.assertEqual(text.count('data-recording-catalog'),1)
    frames=[a for t,a in tags if t=='iframe' and 'data-voice-showcase' in a]
    self.assertEqual(len(frames),1);self.assertEqual(frames[0]['src'],'https://vozes.alocucao.com.br/embed.php')
    self.assertEqual(frames[0]['loading'],'lazy');self.assertTrue(frames[0].get('title'))
    self.assertEqual(text.count('class="rp-panel"'),1)
    self.assertEqual(text.count('class="rp-process"'),1)
    self.assertIn(MODEL['REGISTER'],text);self.assertIn(MODEL['LOGIN'],text)
    for cta,host in [('hero_register','vozes.alocucao.com.br'),('hero_whatsapp','wa.me')]:
     action=[a for t,a in tags if a.get('data-cta')==cta]
     if 'commercial-hero' in text or route=='':self.assertEqual(len(action),1);self.assertEqual(urlsplit(action[0]['href']).hostname,host)
    self.assertNotIn('sábado, das 08h às 12h',text)
    self.assertLess(text.index('id="banco-de-vozes"'),text.index('id="painel-gravacao"'))
    if 'id="precos"' in text:self.assertLess(text.index('id="banco-de-vozes"'),text.index('id="precos"'))
 def test_integrity_and_schema(self):
  for route in MODEL['COMMERCIAL']:
   with self.subTest(route=route):
    text=(ROOT/route/'index.html').read_text();page=Page(text)
    self.assertEqual(len(re.findall('<h1[ >]',text)),1)
    ids=[a['id'] for _,a in page.tags if a.get('id')];self.assertEqual(len(ids),len(set(ids)))
    for tag,a in page.tags:
     href=a.get('href','')
     if href.startswith('#'):self.assertIn(href[1:],ids)
     for key in ['src','href','data-src']:
      src=a.get(key,'');local=unquote(urlsplit(src).path)
      if local.startswith('/assets/'):self.assertTrue((ROOT/local.lstrip('/')).is_file(),src)
    def visit(o):
     if isinstance(o,dict):
      if o.get('@type')=='Offer':self.assertIn(str(o.get('price')),{'15.00','30.00'})
      for v in o.values():visit(v)
     elif isinstance(o,list):
      for v in o:visit(v)
    for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S):visit(json.loads(raw))
 def test_packages_and_primary_channel(self):
  policy=runpy.run_path(str(ROOT/'scripts/commercial-policy.py'))
  for route in MODEL['COMMERCIAL']:
   text=(ROOT/route/'index.html').read_text();tags=Page(text).tags
   self.assertEqual(text.count('data-credit-packages'),1,route)
   chosen=policy['PLANS'] if route in policy['GENERAL'] or route.startswith('produtora-de-audio-') else [policy['PLANS'][0] if route in policy['OFF_ROUTES'] else policy['PLANS'][1]]
   cards=re.findall(r'<article class="cp-card.*?</article>',text,re.S)
   self.assertEqual(len(cards),len(chosen)*4,route)
   for key,name,retail,plans in chosen:
    for qty,unit in plans:
     card=next(c for c in cards if f'data-package="{key}-{qty}"' in c)
     self.assertIn(f'R$ {unit},00',card);self.assertIn(f'Total: <strong>R$ {qty*unit},00</strong>',card)
     href=next(a['href'] for t,a in Page(card).tags if t=='a')
     self.assertEqual(urlsplit(href).hostname,'vozes.alocucao.com.br' if qty==1 else 'wa.me')
   hero=[a for t,a in tags if a.get('data-cta')=='hero_register']
   self.assertEqual(len(hero),1,route);self.assertIn('rp-primary',hero[0]['class'])
 def test_repeatable_and_samples_preserved(self):
  for route in MODEL['COMMERCIAL']:
   text=(ROOT/route/'index.html').read_text();self.assertEqual(text,MODEL['update'](text,route),route)
  self.assertIn('/assets/audio/igreja-evangelica-monte-moria.mp3',(ROOT/'producao-para-igrejas/index.html').read_text())
  self.assertIn('/assets/audio/spot-clinica-ecoar.mp3',(ROOT/'spot-comercial/index.html').read_text())
if __name__=='__main__':unittest.main()
