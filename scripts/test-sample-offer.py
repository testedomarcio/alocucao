"""Check eligibility boundaries, correct voice/service links and retained content."""
import json,re,sys,subprocess
from pathlib import Path
from urllib.parse import urlparse,parse_qs
sys.path.insert(0,str(Path(__file__).parent))
import sample_offer as offer
root=Path(__file__).resolve().parent.parent
for slug,v in offer.ELIGIBLE.items():
 text=(root/'locutores'/slug/'index.html').read_text()
 links=re.findall(r'<a[^>]*href="([^"]+)"[^>]*data-cta="solicitar_amostra"',text)
 assert len(links)==1,slug
 assert v['name'] in parse_qs(urlparse(links[0]).query)['text'][0]
 assert 'Disponível para pedidos' in text and 'marca d’água' in text
for slug,service in [('locucao_off','Locução Off'),('spot_comercial','Produção Completa / Spot Comercial')]:
 text=(root/slug/'index.html').read_text()
 href=re.search(r'<a[^>]*href="([^"]+)"[^>]*data-cta="solicitar_amostra"',text)[1]
 assert service in parse_qs(urlparse(href).query)['text'][0]
# Disabling one voice removes its status and offer without affecting other cards.
voice=offer.ELIGIBLE.pop('christine')
try:
 markup='<section><article class="voice-card"><a href="/locutores/christine/">Christine</a><p class="voice-style">Estilo</p><div class="voice-actions">Contratar</div></article></section>'
 assert offer.enhance('vozes',markup)[0].count('class="sample-availability"')==0
 assert offer.enhance('locutores/christine',markup)==(markup,False)
 assert offer.enhance('servico-de-terceiro',markup)==(markup,False)
finally:offer.ELIGIBLE['christine']=voice
# Assert invariant parts against the preceding published revision.
files=subprocess.check_output(['git','ls-files','*.html'],cwd=root,text=True).splitlines()
for name in files:
 old=subprocess.check_output(['git','show','HEAD:'+name],cwd=root,text=True);new=(root/name).read_text()
 for pattern in [r'<title>.*?</title>',r'<meta name="description"[^>]*>',r'<link rel="canonical"[^>]*>',r'<audio[^>]*>',r'<section class="section dark progressive-pricing".*?</section>',r'<div class="calculator">.*?</div></div></section>']:
  assert re.findall(pattern,old)==re.findall(pattern,new),(name,pattern)
 for review in re.findall(r'<article class="review-card".*?</article>',old):assert review in new,name
print('PASS: eligibility suspension, third-party boundary, voice/service messages and preservation of SEO, audio, prices, calculators and reviews.')
