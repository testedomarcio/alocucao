#!/usr/bin/env python3
"""Apply the reviewed landing offer after legacy generators, without touching the home."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape,unescape
from urllib.parse import quote,urlsplit
import re,json
ROOT=Path(__file__).resolve().parent.parent
OFF={'locucao-off','off-comercial','locucao-ia','vozes-ia','locucao-para-video-institucional','espera-telefonica-ura','locucao-voz-infantil','locucao-campanha-politica'}
PRODUCED={'spot-comercial','producao-para-igrejas','producao-para-supermercados','gravacao-off-e-producao','spot-black-friday','spot-comercial-natal','spot-para-carro-de-som','vinhetas-para-podcast-e-radio','servicos','precos','planos-para-agencias-revenda'}
ROUTES=sorted(OFF|PRODUCED|{p.parent.name for p in ROOT.glob('produtora-de-audio-*/index.html')})
PRICE='A Locução Off custa R$ 12,00 por crédito de até 40 segundos, com qualquer locutor escolhido. Você recebe somente a voz, sem edição, trilha ou efeitos. A produção completa custa R$ 30,00 por crédito e inclui voz, trilha sonora, efeitos e finalização. De 41 a 80 segundos são necessários 2 créditos.'
DELIVERY='Temos locutores que gravam o Off em até 10 minutos, conforme disponibilidade. Confira o status no catálogo e confirme o prazo pelo WhatsApp antes de concluir o pedido. A produção completa tem prazo estimado de 1 a 2 horas após a conclusão da gravação.'
DIFFERENCE='A voz humana é gravada por um locutor; a voz natural (IA) é gerada por tecnologia de síntese de voz. Nossa equipe esclarece a modalidade antes da contratação. O preço é o mesmo para qualquer voz escolhida: Off por R$ 12,00 ou produção completa por R$ 30,00, por crédito de até 40 segundos.'
WA='https://wa.me/5527996529832?text='
VERSION='20261022-single-offer'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Spans(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=False);self.s=s;self.lines=[0];self.stack=[];self.items=[]
  self.lines += [m.end() for m in re.finditer('\n',s)];self.feed(s)
 def pos(self):
  line,col=self.getpos();return self.lines[line-1]+col
 def handle_starttag(self,tag,attrs):
  start=self.pos();a=dict(attrs)
  if tag not in VOID:self.stack.append((tag,a,start))
  else:self.items.append((tag,a,start,start+len(self.get_starttag_text())))
 def handle_startendtag(self,tag,attrs):self.items.append((tag,dict(attrs),self.pos(),self.pos()+len(self.get_starttag_text())))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:
    t,a,start=self.stack[i];self.items.append((t,a,start,self.s.find('>',self.pos())+1));del self.stack[i:];break

def rewrite(s,predicate,replacement=''):
 ranges=[]
 for tag,attrs,start,end in sorted(Spans(s).items,key=lambda x:(x[2],-x[3])):
  if predicate(tag,attrs,s[start:end]) and not any(start>=a and end<=b for a,b in ranges):ranges.append((start,end))
 for start,end in reversed(ranges):s=s[:start]+(replacement(s[start:end]) if callable(replacement) else replacement)+s[end:]
 return s

def plain(s):return unescape(re.sub('<[^>]*>',' ',s)).strip()
def offer(route):
 off=route in OFF;name='Locução Off' if off else 'Produção completa';price='12,00' if off else '30,00'
 desc='Somente voz sem edição, sem trilha e sem efeitos.' if off else 'Voz, trilha sonora, efeitos e finalização para divulgar seu anúncio.'
 secondary='Produção completa por R$ 30,00' if off else 'Locução Off por R$ 12,00 — somente voz sem edição'
 return '<section class="sf-offer" id="precos"><div class="sf-shell"><p class="sf-eyebrow">Preço único para qualquer locutor escolhido</p><h2>'+name+' com preço único</h2><div class="sf-price-card"><h3>'+name+'</h3><p>'+desc+'</p><p class="sf-value">R$ '+price+'</p><p>Por crédito de até 40 segundos</p><p class="sf-secondary">'+secondary+' por crédito de até 40 segundos.</p><a class="sf-button" href="'+WA+quote('Olá! Quero solicitar '+name+' por R$ '+price+', de até 40 segundos. Origem: /'+route+'/')+'" data-cta="single_offer_whatsapp" target="_blank" rel="noopener noreferrer">Pedir pelo WhatsApp</a><p class="sf-note">De 41 a 80 segundos são necessários 2 créditos. Confirme a voz, a duração e o prazo com nossa equipe antes do pedido.</p></div></div></section>'

def catalog():
 return '<section class="sf-voices" id="banco-de-vozes"><div class="sf-shell"><h2>Escolha a voz ideal para seu projeto</h2><p>Ouça as demonstrações da nossa vitrine oficial. Informe no WhatsApp o nome da voz escolhida para confirmar o serviço e o prazo.</p><iframe id="vitrine-vozes" src="https://vozes.alocucao.com.br/embed.php" title="Nossas vozes" loading="lazy" style="width:100%;min-height:640px;border:0"></iframe><p><a class="sf-button" href="'+WA+quote('Olá! Quero ajuda para escolher uma voz e fazer meu pedido.')+'" data-cta="voice_bank_whatsapp" target="_blank" rel="noopener noreferrer">Escolher minha voz pelo WhatsApp</a></p></div></section>'

def update(s,route):
 # Preserve real produced-audio samples; remove only the superseded voice catalog sections.
 s=rewrite(s,lambda t,a,b:t=='section' and ('unified-catalog:start' in b or 'vitrine-vozes' in b))
 s=re.sub(r'<!-- unified-catalog:start -->.*?<!-- unified-catalog:end -->','',s,flags=re.S)
 s=rewrite(s,lambda t,a,b:t=='iframe' and a.get('id')=='vitrine-vozes')
 s=rewrite(s,lambda t,a,b:t=='script' and ('vitrineVozes' in b or 'const ended' in b))
 s=re.sub(r'<!-- dual-offer:start -->.*?<!-- dual-offer:end -->','',s,flags=re.S)
 s=rewrite(s,lambda t,a,b:t=='section' and (any(x in a.get('class','').split() for x in ['commercial-pricing','dual-offer','hybrid-central','sf-offer','sf-voices']) or a.get('id') in {'pacotes','ofertas','precos'}))
 s=rewrite(s,lambda t,a,b:t in {'p','div'} and ('commercial-price' in a.get('class','').split() or 'data-natural-disclosure' in a or a.get('id') in {'expired','validity'}))
 # Off/IA hero had technology-specific price cards rather than a single offer.
 s=rewrite(s,lambda t,a,b:t=='div' and 'ai-services-grid' in a.get('class','').split())
 s=rewrite(s,lambda t,a,b:t=='p' and (('Pacote' in plain(b) or 'pacote' in plain(b)) and 'R$' in b or 'condições promocionais' in plain(b).lower()))
 s=rewrite(s,lambda t,a,b:t in {'a','div','p'} and any(x in a.get('class','').split() for x in ['support','mobile-order','mobile-bar','floating-wa','wa-float','whatsapp-float','sticky-wa','sticky-cta','mobile-cta','sf-floating','sf-mobile','hybrid-login','hybrid-online','sticky-mobile','panel-help-link','mobile-conversion-bar','wa-float-widget']))
 s=re.sub(r'<(?:link|script)\b[^>]*(?:href|src)="/assets/(?:unified-voices|hybrid-commerce|catalog-pages|natural-positioning|packages-landing)\.(?:css|js)[^"]*"[^>]*>(?:</script>)?','',s)
 s=s.replace('data-business-positioning="dual"','').replace('data-order-channels="dual"','data-order-channels="whatsapp"')
 s=re.sub(r'\sdata-single-offer="[^"]*"','',s)
 s=s.replace('<body','<body data-single-offer="'+route+'"',1)
 # No technology-dependent prices, discounts or package anchors survive on these landings.
 for old,new in [('11,90','12,00'),('8,50','12,00'),('29,90','30,00'),('19,00','30,00'),('23,80','24,00'),('8,90','12,00'),('16,90','30,00')]:s=s.replace('R$ '+old,'R$ '+new)
 s=re.sub(r'(?i)a partir de (?=R\$)','',s)
 s=s.replace('Com voz humana · até 40 segundos','Mesmo preço para qualquer voz · até 40 segundos').replace('Catálogo Exclusivo IA','Vitrine oficial de vozes').replace('Locução com IA por R$ 12,00','Locução profissional por R$ 12,00')
 s=re.sub(r'(<h1[^>]*>)(.*?)(</h1>)',lambda m:m[1]+(m[2].replace('a partir de','por') if route not in {'locucao-ia','vozes-ia'} else ('Locução com inteligência artificial para anúncios.' if route=='locucao-ia' else 'Encontre a voz para sua próxima gravação.'))+m[3],s,count=1,flags=re.S)
 # A short hero offer is informational; the full price card follows the hero.
 headline=re.search(r'</h1>',s)
 if headline:s=s[:headline.end()]+'<p class="sf-hero-price"><strong>Locução Off R$ 12,00 · Produção completa R$ 30,00</strong><br>Preço por crédito de até 40 segundos, com qualquer locutor escolhido.</p>'+s[headline.end():]
 # Drop any previous hero preview on reruns.
 s=re.sub(r'(<p class="sf-hero-price">.*?</p>)(?:\s*<p class="sf-hero-price">.*?</p>)+',r'\1',s,flags=re.S)
 # Remove stale package Q&A; keep project-specific questions and policies.
 s=rewrite(s,lambda t,a,b:t=='details' and bool(re.search(r'pacot|créditos e o acesso',plain(b),re.I)))
 def faq(m):
  q=plain(m[2]);answer=m[3]
  if re.search('preço|quanto custa|valor|oferta de Black Friday',q,re.I):answer='<p>'+PRICE+'</p>'
  elif re.search('prazo|tempo demora|tempo recebo|Quanto tempo',q,re.I):answer='<p>'+DELIVERY+'</p>'
  elif 'diferença entre voz humana' in q:answer='<p>'+DIFFERENCE+'</p>'
  elif 'diferença' in q and ('Off' in q or 'Produção' in q):answer='<p>'+PRICE+'</p>'
  elif 'incluído na produção' in q:answer='<p>'+PRICE+'</p>'
  return m[1]+m[2]+'</summary>'+answer+'</details>'
 s=re.sub(r'(<details\b[^>]*>\s*<summary[^>]*>)(.*?)</summary>(.*?)</details>',faq,s,flags=re.S)
 # Eliminate lingering cheaper-technology claims in editorial copy.
 s=s.replace('agilidade e preços mais acessíveis','agilidade para diferentes projetos').replace('A escolha depende do estilo, do orçamento e das necessidades do projeto.','A escolha depende do estilo e das necessidades do projeto.').replace('Solicite pelo WhatsApp e aproveite as condições promocionais de locução até 10/11/2026.','Solicite pelo WhatsApp: Off por R$ 12,00 ou produção completa por R$ 30,00, por crédito de até 40 segundos.').replace('Perguntas Frequentes sobre os Pacotes','Perguntas frequentes sobre sua gravação')
 # Preserve specialist political/children's voice suitability; pricing does not promise availability.
 # Conversion buttons and voice/price links stay on this landing or go directly to WhatsApp.
 def link(m):
  pre,href,post,label=m.groups();url=urlsplit(unescape(href));txt=plain(label);attrs=pre+post
  if href.startswith('#'):
   if href=='#pacotes':href='#precos'
   return pre+href+post+label+'</a>'
  if url.hostname=='wa.me':
   return pre+WA+quote('Olá! Quero atendimento sobre '+route.replace('-',' ')+'. Origem: /'+route+'/')+post+label+'</a>'
  if any(x in href for x in ['/vozes/','/locutores/','/vozes-ia/']):return pre+'#banco-de-vozes'+post+'Ouvir vozes disponíveis</a>'
  if '/precos/' in href:return pre+'#precos'+post+'Consultar preços</a>'
  if any(x in href for x in ['/painel','/cadastro','/central']) or re.search(r'class="[^"]*(?:btn|button|primary|hybrid)',attrs):
   return pre+WA+quote('Olá! Quero atendimento sobre '+route.replace('-',' ')+'. Origem: /'+route+'/')+post+('Pedir pelo WhatsApp' if '/painel' in href or '/cadastro' in href else label)+'</a>'
  return m[0]
 s=re.sub(r'(<a\b[^>]*?href=")([^"]*)("[^>]*>)(.*?)</a>',link,s,flags=re.S)
 # Add offer and official showcase immediately after the hero, retaining all niche copy below.
 main=re.search(r'<main\b[^>]*>',s)
 if main:
  sections=[x for x in Spans(s).items if x[0]=='section' and x[2]>=main.end()]
  first=min(sections,key=lambda x:x[2]) if sections else None
  at=first[3] if first else main.end();s=s[:at]+offer(route)+catalog()+s[at:]
 # Every landing has the essential price/turnaround explanation, even if it had no FAQ.
 questions=[plain(q) for q in re.findall(r'<summary[^>]*>(.*?)</summary>',s,re.S)]
 essential=[]
 if not any(re.search('preço|quanto custa|valor|oferta',q,re.I) for q in questions):essential.append(('Como o preço é calculado?',PRICE))
 if not any(re.search('prazo|tempo demora|tempo recebo',q,re.I) for q in questions):essential.append(('Qual é o prazo de entrega?',DELIVERY))
 if essential:s=s.replace('</main>','<section class="sf-faq"><div class="sf-shell"><h2>Preços e prazos para seu pedido</h2>'+''.join('<details><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in essential)+'</div></section></main>')
 # Metadata and structured offers align with visible FAQ and the same per-credit unit.
 title=re.search(r'<title>(.*?)</title>',s,re.S)
 if title:
  clean=plain(title[1]).replace('a partir de R$ 12,00','por R$ 12,00').replace(': Pacotes',': Preço único').replace('Pacotes','Preços')
  s=s.replace(title[0],'<title>'+escape(clean)+'</title>')
 desc=(clean.split('|')[0].strip()+'. Off R$ 12,00 ou produção completa R$ 30,00 por crédito de até 40 segundos. Ouça as vozes e peça pelo WhatsApp.')
 s=re.sub(r'(<meta\b[^>]*(?:name="description"|property="og:description"|name="twitter:description")[^>]*content=")[^"]*(")',lambda m:m[1]+escape(desc,quote=True)+m[2],s)
 if title:
  s=re.sub(r'(<meta\b[^>]*(?:property="og:title"|name="twitter:title")[^>]*content=")[^"]*(")',lambda m:m[1]+escape(clean,quote=True)+m[2],s)
 s=s.replace('Pedidos pelo WhatsApp ou pela Central A Locução.','Pedidos e atendimento pelo WhatsApp.').replace('Preços e Pacotes','Preços e condições')
 faqs=[(plain(q),plain(a)) for q,a in re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>',s,re.S)]
 offers=[{'@type':'Offer','name':name,'price':price,'priceCurrency':'BRL','url':'https://alocucao.com.br/'+route+'/','description':'Preço único por crédito de até 40 segundos, válido para qualquer locutor escolhido.'} for name,price in [('Locução Off — somente voz sem edição','12.00'),('Produção completa — voz, trilha, efeitos e finalização','30.00')]]
 def schema(m):
  try:d=json.loads(m[2])
  except json.JSONDecodeError:return m[0]
  def walk(o):
   if isinstance(o,dict):
    if o.get('@type')=='FAQPage':o['mainEntity']=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]
    if o.get('@type') in {'Service','Product'}:o['offers']=offers;o['description']=desc;o['name']=o.get('name','').replace(' em Pacote','')
    if o.get('@type')=='OfferCatalog':o['itemListElement']=offers
    if o.get('@type')=='Offer':
     name=o.get('name','')+' '+str(o.get('itemOffered',{}));o['price']='30.00' if re.search('produ|spot',name,re.I) else '12.00';o.pop('priceValidUntil',None);o.pop('validThrough',None)
    for v in o.values():walk(v)
   elif isinstance(o,list):
    for v in o:walk(v)
  walk(d);return m[1]+json.dumps(d,ensure_ascii=False,separators=(',',':'))+m[3]
 s=re.sub(r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',schema,s,flags=re.S)
 if 'id="single-offer-schema"' not in s:
  s=s.replace('</head>','<script id="single-offer-schema" type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'OfferCatalog','name':'Locução e produção por crédito de até 40 segundos','itemListElement':offers},ensure_ascii=False,separators=(',',':'))+'</script>\n</head>')
 # Dedicated, scoped assets do not affect the home or the full voice pages.
 if '/assets/single-offer-landings.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/assets/single-offer-landings.css?v='+VERSION+'">\n<script src="/assets/single-offer-landings.js?v='+VERSION+'" defer></script>\n</head>')
 # Clean dangling legacy IDs/links without moving any legal navigation.
 ids=set(re.findall(r'\bid="([^"]+)"',s))
 s=re.sub(r'href="#([^"]+)"',lambda m:m[0] if m[1] in ids else 'href="#banco-de-vozes"',s)
 controls='<a class="sf-floating" href="'+WA+quote('Olá! Quero fazer meu pedido. Origem: /'+route+'/')+'" target="_blank" rel="noopener noreferrer" data-cta="floating_whatsapp" aria-label="Fazer pedido pelo WhatsApp">WhatsApp</a><div class="sf-mobile"><span>Off <strong>R$ 12,00</strong><br>Produção <strong>R$ 30,00</strong></span><a class="sf-button" href="'+WA+quote('Olá! Quero fazer meu pedido. Origem: /'+route+'/')+'" target="_blank" rel="noopener noreferrer" data-cta="commercial_mobile">Pedir pelo WhatsApp</a></div>'
 s=s.replace('</body>',controls+'</body>')
 return re.sub(r'[ \t]+$', '', s, flags=re.M)

def main():
 changed=[]
 for route in ROUTES:
  path=ROOT/route/'index.html'
  if not path.is_file():continue
  old=path.read_text();new=update(old,route)
  if new!=old:path.write_text(new);changed.append(route)
 print('Single-offer landing pages:',len(changed),'updated;',len(ROUTES),'reviewed. Home excluded.')
if __name__=='__main__':main()
