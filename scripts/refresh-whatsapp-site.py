#!/usr/bin/env python3
"""Final public-site policy: one price per service, selected demos and WhatsApp orders."""
from pathlib import Path
from html import escape,unescape
from urllib.parse import quote,urlsplit
import json,re,runpy
ROOT=Path(__file__).resolve().parent.parent
HELPERS=runpy.run_path(str(ROOT/'scripts/standardize-single-offer.py'))
rewrite=HELPERS['rewrite'];plain=HELPERS['plain']
VERSION='20261022-selected-voices-v2'
WA='https://wa.me/5527996529832?text='
PRICE='A Locução Off custa R$ 12,00 por crédito de até 40 segundos e inclui somente a voz, sem edição, trilha ou efeitos. A produção completa custa R$ 30,00 por crédito e inclui locução, trilha sonora, efeitos e finalização. O preço é o mesmo para qualquer voz escolhida. De 41 a 80 segundos são necessários 2 créditos.'
META={
 '':('Locução Profissional: Off R$ 12 e Spot R$ 30 | A Locução','Locução profissional para dar voz ao seu anúncio.','Locução profissional para comerciais, vídeos e campanhas. Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos. Ouça as vozes e peça pelo WhatsApp.'),
 'locucao-off':('Locução Off Profissional por R$ 12,00 | A Locução','Locução Off profissional para seu anúncio.','Receba somente a voz, sem edição, trilha ou efeitos, por R$ 12,00 a cada 40 segundos. Ouça as demonstrações e solicite sua gravação pelo WhatsApp.'),
 'spot-comercial':('Spot Comercial Completo por R$ 30,00 | A Locução','Seu spot comercial pronto para divulgar.','Spot comercial com locução, trilha, efeitos e finalização por R$ 30,00 a cada 40 segundos. Ouça exemplos e peça seu anúncio pelo WhatsApp.'),
 'off-comercial':('Off Comercial: Locução Profissional por R$ 12 | A Locução','A voz profissional que seu comercial precisa.','Locução Off para publicidade, rádio e vídeos. Somente a voz por R$ 12,00 a cada 40 segundos. Escolha sua demonstração e peça um orçamento pelo WhatsApp.'),
 'producao-para-igrejas':('Produção de Áudio para Igrejas por R$ 30 | A Locução','Produção de áudio para igrejas e eventos.','Chamadas para cultos, congressos e eventos cristãos com locução, trilha e efeitos. Produção por R$ 30,00 a cada 40 segundos. Peça pelo WhatsApp.'),
 'producao-para-supermercados':('Locução para Supermercados: Off e Spots | A Locução','Locução para supermercado que destaca suas ofertas.','Divulgue ofertas de mercados, hortifrúti e açougue. Off R$ 12,00 ou spot completo R$ 30,00 por até 40 segundos. Solicite pelo WhatsApp.'),
 'gravacao-off-e-producao':('Locução e Produção de Áudio para Campanhas | A Locução','Locução e produção de áudio para suas campanhas.','Grave comerciais, chamadas e anúncios com qualidade profissional. Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos. Atendimento pelo WhatsApp.'),
 'vozes':('Banco de Vozes: Ouça e Peça pelo WhatsApp | A Locução','Ouça, escolha sua voz e peça pelo WhatsApp.','Explore nossa seleção de vozes com fotos, demonstrações e filtros por estilo e gênero. Escolha sua voz e solicite orçamento pelo WhatsApp.'),
 'locutores':('Vozes para Comerciais: Demonstrações e Orçamento | A Locução','Encontre a voz ideal para sua próxima campanha.','Ouça nossa seleção de vozes para publicidade e vídeos. Filtre por nome, gênero e estilo e solicite orçamento pelo WhatsApp, sem cadastro.'),
 'vozes-ia':('Vozes Naturais para Comerciais e Anúncios | A Locução','Vozes naturais para comerciais e anúncios.','Ouça demonstrações de vozes naturais geradas por IA. Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos. Escolha sua voz pelo WhatsApp.'),
 'locucao-ia':('Locução com IA: Demonstrações e Preços | A Locução','Locução com IA para dar voz às suas ideias.','Conheça vozes geradas por IA para anúncios, vídeos e comerciais. Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos. Peça pelo WhatsApp.'),
 'spot-black-friday':('Spot Black Friday: Locução e Produção | A Locução','Spots de Black Friday para destacar suas ofertas.','Prepare suas ofertas de Black Friday com voz, trilha e efeitos. Produção R$ 30,00 ou Off R$ 12,00 por até 40 segundos. Peça pelo WhatsApp.'),
 'spot-comercial-natal':('Spot de Natal: Locução e Produção Comercial | A Locução','Sua campanha de Natal com voz e emoção.','Spots de Natal para lojas, rádio e redes sociais. Produção completa R$ 30,00 ou Off R$ 12,00 por até 40 segundos. Solicite pelo WhatsApp.'),
 'precos':('Preços: Locução Off R$ 12 e Produção R$ 30 | A Locução','Preços claros para sua locução e produção de áudio.','Locução Off R$ 12,00 e produção completa R$ 30,00 por crédito de até 40 segundos, com qualquer voz escolhida. Confira os serviços e peça pelo WhatsApp.'),
 'servicos':('Serviços de Locução e Produção de Áudio | A Locução','Locução e produção de áudio para sua comunicação.','Locução Off, spots, URA, vinhetas e narração para vídeos. Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos. Fale pelo WhatsApp.'),
 'planos-para-agencias-revenda':('Locução para Agências e Revendedores | A Locução','Locução e produção para agências e revendedores.','Produza áudios para as campanhas dos seus clientes. Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos, com atendimento pelo WhatsApp.')}


def selected_voices():
 data=json.loads((ROOT/'assets/voices-catalog.json').read_text());rows=[]
 for v in data['voices']:
  if '🧠' not in v.get('name',''):continue
  for field in ['audio','photo']:
   u=urlsplit(v.get(field,''))
   if u.scheme!='https' or u.hostname!='vozes.alocucao.com.br':raise ValueError('Missing or invalid public media for '+v['name'])
  rows.append({'id':v['id'],'name':re.sub(r'\s+',' ',v['name'].replace('🧠','')).strip(),'gender':v.get('type',''),'styles':v.get('styles',[]),'audio':v['audio'],'photo':v['photo'],'kind':'ia'})
 if not rows:raise ValueError('No 🧠 voices found; refusing to erase the selection')
 return sorted(rows,key=lambda v:v['name'].casefold())

def render_catalog(voices,route):
 e=lambda s:escape(str(s),quote=True)
 styles=sorted({style for v in voices for style in v['styles']})
 cards=[]
 for v in voices:
  msg='Olá! Gostei da voz '+v['name']+' e gostaria de solicitar um orçamento. Origem: https://alocucao.com.br/'+route+('/' if route else '')
  cards.append('<article class="sv-card" data-sv-name="'+e(v['name'])+'" data-sv-gender="'+e(v['gender'])+'" data-sv-styles="'+e('|'.join(v['styles']))+'"><div class="sv-card-head"><img src="'+e(v['photo'])+'" alt="Perfil ilustrativo da voz '+e(v['name'])+'" width="80" height="80" loading="lazy" decoding="async"><div><h3>'+e(v['name'])+'</h3><p>'+e(v['gender'])+'</p></div></div><div class="sv-tags">'+''.join('<span>'+e(x)+'</span>' for x in v['styles'])+'</div><audio controls preload="none" src="'+e(v['audio'])+'" aria-label="Ouvir demonstração de '+e(v['name'])+'" data-voice="'+e(v['name'])+'">Seu navegador não suporta áudio.</audio><p class="sv-audio-error" hidden>Não foi possível carregar o áudio. Solicite a demonstração pelo WhatsApp.</p><a class="sv-order" href="'+WA+quote(msg)+'" target="_blank" rel="noopener noreferrer" data-cta="selected_voice_quote" data-voice-kind="ia" data-voice-name="'+e(v['name'])+'">Quero essa voz</a></article>')
 more=WA+quote('Olá! Quero conhecer mais opções de vozes para meu projeto. Origem: https://alocucao.com.br/'+route+('/' if route else ''))
 return '<!-- selected-voices:start --><section class="sv-section" id="banco-de-vozes" data-selected-voices><div class="sv-shell"><div class="sv-heading"><span>OUÇA ANTES DE ESCOLHER</span><h2>Encontre a voz do seu próximo anúncio</h2><p>Ouça as demonstrações, encontre seu estilo e peça um orçamento direto pelo WhatsApp.</p></div><div class="sv-filters"><label>Buscar voz<input type="search" class="sv-search" placeholder="Nome da voz" autocomplete="off"></label><label>Gênero<select class="sv-gender"><option value="">Todos</option><option>Masculina</option><option>Feminina</option></select></label><label>Estilo<select class="sv-style"><option value="">Todos os estilos</option>'+''.join('<option>'+e(x)+'</option>' for x in styles)+'</select></label><button type="button" class="sv-clear">Limpar filtros</button></div><p class="sv-count" role="status" aria-live="polite">'+str(len(voices))+' vozes na seleção</p><div class="sv-grid">'+''.join(cards)+'</div><p class="sv-empty" hidden>Nenhuma voz encontrada. Tente outro nome ou limpe os filtros.</p><button class="sv-more" type="button" hidden>Mostrar mais vozes</button><div class="sv-footer"><p>Quer explorar outros estilos e locutores? Nossa equipe ajuda você a escolher.</p><a class="sv-order sv-more-whatsapp" href="'+more+'" target="_blank" rel="noopener noreferrer" data-cta="more_voices_whatsapp">Conheça mais vozes pelo WhatsApp</a><p class="sv-disclosure">Esta seleção reúne vozes geradas por inteligência artificial. As fotos representam perfis ilustrativos. Confirme o formato, a disponibilidade e o prazo antes do pedido.</p></div></div></section><!-- selected-voices:end -->'


def is_order_url(href):
 u=urlsplit(unescape(href));h=u.hostname or '';p=u.path.lower()
 return (any(x in p for x in ['/painel','/cadastro','/central-de-gravacao','/central-de-producao']) or h in {'vozlocutor.com.br','www.vozlocutor.com.br','paineldegravacao.com.br','www.paineldegravacao.com.br','hd.paineldegravacao.com.br'} and not p.endswith(('.mp3','.jpg','.png','.webp','.wav')))

def normalize_prices(s):
 # Public legacy prices converge on a service price; never change the 40-second unit.
 for old,new in [('11,90','12,00'),('8,50','12,00'),('29,90','30,00'),('19,00','30,00'),('8,90','12,00'),('16,90','30,00'),('23,80','24,00')]:s=re.sub(r'R\$\s*'+re.escape(old), 'R$ '+new,s)
 s=re.sub(r'(?i)a partir de\s*(?=R\$\s*(?:12,00|30,00))','',s)
 return s

def update(s,route,voices,template=False):
 s=normalize_prices(s)
 # Remove customer endorsements sitewide, including legacy templates and generated sections.
 s=rewrite(s,lambda t,a,b:t=='section' and (bool(re.search(r'testimonial|depoimento|reviews-public',a.get('class','')+' '+a.get('id',''),re.I)) or 'testimonial-card' in b or 'spot-testimonial' in b))
 s=rewrite(s,lambda t,a,b:t=='a' and (urlsplit(unescape(a.get('href',''))).path.rstrip('/')=='/avaliacoes' or bool(re.search(r'depoimento',a.get('href',''),re.I))))
 s=re.sub(r'<link\b[^>]*href=["\'][^"\']*/assets/testimonials\.css[^"\']*["\'][^>]*>','',s)
 s=s.replace('Avalie sua experiência com a A Locução e leia depoimentos autorizados de clientes de locução e produção de áudio.','Envie sua avaliação sobre o atendimento e os serviços de locução e produção de áudio da A Locução.')
 # Isolate all old voice widgets, preserving separate real-work/portfolio audio.
 s=re.sub(r'<!-- selected-voices:start -->.*?<!-- selected-voices:end -->','<!-- selected-voices:slot -->',s,flags=re.S)
 s=rewrite(s,lambda t,a,b:t=='section' and ('unified-catalog:start' in b or 'vitrine-vozes' in b), '<!-- selected-voices:slot -->')
 s=re.sub(r'<!-- unified-catalog:start -->.*?<!-- unified-catalog:end -->','<!-- selected-voices:slot -->',s,flags=re.S)
 s=rewrite(s,lambda t,a,b:t=='iframe' and a.get('id')=='vitrine-vozes','<!-- selected-voices:slot -->')
 s=rewrite(s,lambda t,a,b:t=='script' and 'vitrineVozes' in b)
 if '<!-- selected-voices:slot -->' in s:
  s=s.replace('<!-- selected-voices:slot -->',render_catalog(voices,route),1).replace('<!-- selected-voices:slot -->','')
 elif route in set(META)|set(HELPERS['ROUTES']) and not template and not re.search(r'http-equiv=["\']refresh',s,re.I):
  if '</main>' in s:s=s.replace('</main>',render_catalog(voices,route)+'</main>',1)
 # Old dual prices and package tables are replaced by a compact service explanation.
 summary='<section class="sv-price-summary"><div><h2>Locução Off R$ 12,00 · Produção completa R$ 30,00</h2><p>'+PRICE+'</p><a class="sv-order" href="'+WA+quote('Olá! Quero um orçamento para meu áudio.')+'" data-cta="prices_whatsapp">Pedir orçamento pelo WhatsApp</a></div></section>'
 s=re.sub(r'<!-- dual-offer:start -->.*?<!-- dual-offer:end -->',summary,s,flags=re.S)
 s=rewrite(s,lambda t,a,b:t in {'table','section'} and ('al-pricing-dual-grid' in b or t=='table' and bool(re.search(r'R\$|Pacote',b,re.I))),summary)
 # Remove legacy technology-price statements; keep the factual FAQ disclosure.
 s=rewrite(s,lambda t,a,b:t in {'p','small'} and bool(re.search(r'Com Vozes Naturais.*Com voz humana|Com voz humana:|Valores com vozes naturais.*Com vozes humanas|Economia aproximada com IA|pacotes existentes são',plain(b),re.I)), '<p>Mesmo preço para qualquer voz escolhida, por crédito de até 40 segundos.</p>')
 s=s.replace('agilidade e preços mais acessíveis','agilidade para diferentes projetos').replace('IA oferece economia e consistência.','IA oferece consistência e diferentes estilos de interpretação.')
 s=s.replace('A escolha depende do estilo, do orçamento e das necessidades do projeto.','A escolha depende do estilo e das necessidades do projeto.')
 s=s.replace('Pedidos pelo WhatsApp ou pela Central A Locução.','Pedidos e atendimento pelo WhatsApp.')
 s=rewrite(s,lambda t,a,b:t=='section' and 'hybrid-central' in a.get('class','').split())
 s=rewrite(s,lambda t,a,b:t in {'p','li'} and bool(re.search(r'(?:Central A Locução|Central de Produção|pelo painel|no painel|se cadastra|contratar online pela Central)',plain(b),re.I)), '<p>Envie seu texto pelo WhatsApp. Nossa equipe confirma a voz, o serviço, o valor e o prazo e acompanha seu pedido até a entrega.</p>')
 s=rewrite(s,lambda t,a,b:t=='a' and a.get('data-cta') in {'header_client','footer_client','client_login','online_order'})
 # Convert registration and panel exits, including old relative aliases and redirect pages.
 def anchor(m):
  pre,href,post,label=m.groups()
  if is_order_url(href) or (re.search(r'class=[\"\'][^\"\']*(?:btn|button|panel-primary|panel-secondary|al-header-cta)',pre+post) and not href.startswith('#') and urlsplit(unescape(href)).hostname!='wa.me' and not re.search(r'\.(?:mp3|wav|pdf)(?:[?#]|$)',href,re.I)):
   name=plain(label)
   label='Solicitar orçamento pelo WhatsApp' if '<img' not in label else label
   return pre+WA+quote('Olá! Quero solicitar um orçamento. Origem: https://alocucao.com.br/'+route+('/' if route else ''))+post+label+'</a>'
  return m[0]
 s=re.sub(r'(<a\b[^>]*?href=["\'])([^"\']*)(["\'][^>]*>)(.*?)</a>',anchor,s,flags=re.S)
 # Avoid stale panel actions hidden in data attributes or inline click handlers.
 s=re.sub(r'((?:action|data-href|data-url)=["\'])([^"\']+)(["\'])',lambda m:m[1]+WA+quote('Olá! Quero atendimento sobre uma gravação.')+m[3] if is_order_url(m[2]) else m[0],s)
 s=re.sub(r'(http-equiv=["\']refresh["\'][^>]*content=["\'][^"\']*url=)([^"\']+)',lambda m:m[1]+WA+quote('Olá! Quero fazer meu pedido pelo WhatsApp.') if is_order_url(m[2]) else m[0],s,flags=re.I)
 # Every changed commercial title keeps the page-specific topic instead of duplicating headings.
 if route in META and not template and '<main' in s:
  title,h1,description=META[route]
  s=re.sub(r'<title>.*?</title>','<title>'+escape(title)+'</title>',s,count=1,flags=re.S)
  s=re.sub(r'<h1\b[^>]*>.*?</h1>','<h1>'+escape(h1)+'</h1>',s,count=1,flags=re.S)
  def meta(m):
   tag=m[0];key=re.search(r'(?:name|property)=["\']([^"\']+)["\']',tag)
   if key and key[1] in ['description','og:description','twitter:description','og:title','twitter:title']:
    value=title if key[1].endswith(':title') else description
    tag=re.sub(r'content=["\'][^"\']*["\']','content="'+escape(value,quote=True)+'"',tag)
   return tag
  s=re.sub(r'<meta\b[^>]*>',meta,s)
 # FAQ explains one price per service; existing rights/correction/project questions remain.
 def faq(m):
  q=plain(m[2]);answer=m[3]
  if re.search(r'quanto custa|preço|valor|oferta|pacote|créditos e o acesso',q,re.I):
   if re.search('pacote|créditos e o acesso',q,re.I):q='Como funciona a contratação pelo WhatsApp?'
   answer='<p>'+PRICE+' Solicite seu orçamento pelo WhatsApp, sem cadastro.</p>'
  if 'diferença entre voz humana' in q:answer='<p>A voz humana é gravada por um locutor. A voz natural (IA) é gerada por síntese de voz. A seleção desta página identifica a modalidade das demonstrações. O valor é o mesmo para qualquer voz escolhida: Off R$ 12,00 e produção completa R$ 30,00 por até 40 segundos.</p>'
  return m[1]+escape(q)+'</summary>'+answer+'</details>'
 s=re.sub(r'(<details\b[^>]*>\s*<summary[^>]*>)(.*?)</summary>(.*?)</details>',faq,s,flags=re.S)
 # Keep structured service offers and FAQ text equal to public copy.
 faqs=[(plain(q),plain(a)) for q,a in re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>',s,re.S)]
 def schema(m):
  try:d=json.loads(m[2])
  except json.JSONDecodeError:return m[0]
  def walk(o,context=''):
   if isinstance(o,dict):
    kind=o.get('@type');name=str(o.get('name',''))
    for key in ['review','reviews','aggregateRating']:o.pop(key,None)
    if kind=='FAQPage' and faqs:o['mainEntity']=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]
    if kind in {'Service','Product'} and ('offers' in o or 'hasOfferCatalog' in o):
     o.pop('hasOfferCatalog',None);o['offers']=[{'@type':'Offer','name':name,'price':price,'priceCurrency':'BRL','description':'Preço por crédito de até 40 segundos, com qualquer voz escolhida.','url':'https://alocucao.com.br/'+route+('/' if route else '')} for name,price in [('Locução Off — somente voz','12.00'),('Produção completa','30.00')]]
    if kind=='Offer':
     item=(name+' '+str(o.get('itemOffered',''))).strip() or context
     o['price']='30.00' if re.search('produ|spot',item,re.I) else '12.00';o['priceCurrency']='BRL'
     for k in ['priceValidUntil','validThrough','lowPrice','highPrice']:o.pop(k,None)
    if kind=='ItemList' and re.search(r'vozes|locutores',name,re.I):o['numberOfItems']=len(voices);o['itemListElement']=[{'@type':'ListItem','position':i+1,'name':v['name']} for i,v in enumerate(voices)]
    if kind=='AggregateOffer':o.update({'lowPrice':'12.00','highPrice':'30.00','priceCurrency':'BRL'})
    if kind in {'WebPage','CollectionPage'} and route in META:o['name']=META[route][0]
    for v in list(o.values()):walk(v,name or context)
   elif isinstance(o,list):
    for v in o:walk(v,context)
  walk(d)
  return m[1]+json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+m[3]
 s=re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',schema,s,flags=re.S)
 # Only one catalog's assets are shipped; shared commerce handles future injected links too.
 s=re.sub(r'<(?:link|script)\b[^>]*(?:href|src)="/assets/(?:unified-voices|single-offer-landings|featured-voices|voice-bank)\.(?:css|js)[^"]*"[^>]*>(?:</script>)?',lambda m:'' if 'single-offer-landings.css' not in m[0] else m[0],s)
 s=re.sub(r'<script\b[^>]*src="/assets/selected-voices\.js[^\"]*"[^>]*></script>\s*','',s)
 s=re.sub(r'<link\b[^>]*href="/assets/selected-voices\.css[^\"]*"[^>]*>\s*','',s)
 if not template and '</head>' in s:
  s=s.replace('</head>','<link rel="stylesheet" href="/assets/selected-voices.css?v='+VERSION+'">\n<script src="/assets/selected-voices.js?v='+VERSION+'" defer></script>\n</head>')
 if 'id="precos"' not in s and 'class="sv-price-summary"' in s:s=s.replace('class="sv-price-summary"','class="sv-price-summary" id="precos"',1)
 ids=set(re.findall(r'\bid="([^"]+)"',s))
 if 'banco-de-vozes' in ids:
  s=re.sub(r'href="#([^"]+)"',lambda m:m[0] if m[1] in ids else 'href="#banco-de-vozes"',s)
 # Avoid duplicate adjacent menu exits after panel actions become the same WhatsApp action.
 s=re.sub(r'(<a\b[^>]*>Ouvir vozes disponíveis</a>)(?:\s*<a\b[^>]*>Ouvir vozes disponíveis</a>)+',r'\1',s)
 # Stale panel-first positioning should not remain visible on PWA/help pages.
 for old,new in [('Pedir voz humana na Central','Pedir pelo WhatsApp'),('Já sou cliente — Acessar painel','Falar pelo WhatsApp'),('Área do Cliente — Acessar painel','Atendimento pelo WhatsApp'),('Faça seu pedido pela Central A Locução','Faça seu pedido pelo WhatsApp'),('Prefere contratar diretamente pela Central A Locução?','Precisa de ajuda para contratar? Fale pelo WhatsApp.'),('Faça pedidos pelo WhatsApp e acompanhe cada etapa na sua conta.','Faça pedidos e acompanhe cada etapa pelo WhatsApp.')]:s=s.replace(old,new)
 return re.sub(r'[ \t]+$','',s,flags=re.M)


def main():
 voices=selected_voices()
 selected={'source':'https://vozes.alocucao.com.br/#locutores','selection':'🧠','count':len(voices),'voices':voices}
 (ROOT/'assets/selected-voices.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
 changed=[]
 for path in sorted(ROOT.rglob('*.html')):
  if any(p.startswith('.') or p in {'node_modules','_site'} for p in path.relative_to(ROOT).parts):continue
  route=path.parent.relative_to(ROOT).as_posix();route='' if route=='.' else route
  old=path.read_text();new=update(old,route,voices,route.startswith('templates'))
  if new!=old:path.write_text(new);changed.append(str(path.relative_to(ROOT)))
 print('WhatsApp-only pages:',len(changed),'updated; selected voices:',len(voices))
if __name__=='__main__':main()
