"""Protect the visual pass's commercial and functional boundaries."""
from pathlib import Path
import re,subprocess
from visual_refinement import refine_page
ROOT=Path(__file__).resolve().parent.parent
files=subprocess.check_output(['git','ls-files','*.html'],cwd=ROOT,text=True).splitlines()
count=0
for name in files:
 s=(ROOT/name).read_text()
 old=subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT,text=True)
 # Presentation must not change SEO, scripts, audio sources, or price tables.
 for pattern in [r'<title>.*?</title>',r'<meta [^>]*>',r'<link rel="canonical"[^>]*>',r'<script\b.*?</script>',r'<audio\b[^>]*>',r'<table\b.*?</table>']:
  assert re.findall(pattern,old,re.S)==re.findall(pattern,s,re.S),(name,pattern)
 if name not in ('index.html','vozes/index.html'):
  assert re.findall(r'<a\b[^>]*>',old)==re.findall(r'<a\b[^>]*>',s),name
 assert refine_page(s,dedicated=name=='calculadora/index.html',home=name=='index.html',bank=name=='vozes/index.html')==s,('idempotency',name)
 if 'id="calc-text"' in s:
  count+=1
  for control in ['calc-service','calc-text','calc-result','calc-whatsapp','calc-text-note']:
   assert s.count('id="'+control+'"')==1,(name,control)
  assert 'calc-inputs' in s and 'calc-summary' in s
  assert re.findall(r'<select.*?</select>',old,re.S)==re.findall(r'<select.*?</select>',s,re.S)
for name in ['assets/nova.js','assets/pricing.js']:
 assert (ROOT/name).read_bytes()==subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT),name
home=(ROOT/'index.html').read_text()
assert 'home-sample-conditions' in home and 'class="sample-hero-copy"' in home
assert '<section class="section sample-offer"' not in home
assert 'marca d’água' in home and 'sem obrigação de contratação' in home
bank=(ROOT/'vozes/index.html').read_text()
assert bank.count('class="sample-card-link"')==27
assert 'catalog-sample-conditions' in bank
assert 'calculator-intro' in (ROOT/'calculadora/index.html').read_text()
print(f'PASS: {len(files)} pages, {count} calculators, unchanged SEO/scripts/audio/prices, unique controls, and retained sample conditions.')
