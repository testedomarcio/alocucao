#!/usr/bin/env python3
"""Final, repeatable publishing policy for the assisted and self-service order channels."""
from pathlib import Path
from html import escape,unescape
from urllib.parse import urlsplit,unquote,quote
import re,json,runpy
ROOT=Path(__file__).resolve().parent.parent
H=runpy.run_path(str(ROOT/'scripts/standardize-single-offer.py'))
rewrite=H['rewrite'];plain=H['plain']
POLICY=runpy.run_path(str(ROOT/'scripts/commercial-policy.py'))
Nodes=runpy.run_path(str(ROOT/'scripts/hybrid-commerce.py'))['Nodes']
REGISTER='https://vozes.alocucao.com.br/painel/cadastro'
LOGIN='https://vozes.alocucao.com.br/painel/'
WA='https://wa.me/5527996529832'
VERSION='20261023-ai-disclosure-v2'
COMMERCIAL=(set(H['ROUTES'])-{'vozes-ia'})|{'','vozes','locutores'}
SCHEDULE='segunda a sexta-feira, das 07h às 18h; sábado, das 07h às 14h (horário de Brasília)'
PRODUCTION='Produção todos os dias, inclusive finais de semana e feriados. A estimativa de entrega da produção é de 30 minutos a 4 horas, dependendo da demanda e da complexidade do pedido.'
HOURS='Atendimento e suporte pelo WhatsApp: '+SCHEDULE+'. Pedidos pelo Painel de Gravação: 24 horas por dia, todos os dias. Gravações de Locução Off até as 22h, conforme a disponibilidade de cada locutor. '+PRODUCTION
ATTRIBUTION_VERSION='20261023-audit-v1'
def public_policy(s,route):
 # Update support language without changing the distinction between human and synthetic voices.
 for old,new in [('atendimento humano','atendimento pelo WhatsApp'),('Atendimento humano','Atendimento pelo WhatsApp'),('Suporte humano','Suporte pelo WhatsApp'),('suporte humano','suporte pelo WhatsApp'),('Atendimento exclusivo pelo WhatsApp','Atendimento pelo WhatsApp')]:s=s.replace(old,new)
 s=re.sub(r'(?i)segunda a sexta(?:-feira)?,?\s*(?:das\s*)?0?8h\s*às\s*18h(?:\s*\(Brasília\))?',lambda m:('S' if m[0][0].isupper() else 's')+SCHEDULE[1:],s)
 # Older templates include a second Saturday schedule after the weekday range.
 s=re.sub(re.escape(SCHEDULE)+r';?\s*sábado,?\s*das\s*08h\s*às\s*12h(?:, exceto feriados)?\s*\(Brasília\)',SCHEDULE,s,flags=re.I)
 s=s.replace('Segunda a sexta-feira: das 08h às 18h.','Segunda a sexta-feira: das 07h às 18h.').replace('Sábado: das 08h às 12h.','Sábado: das 07h às 14h.')
 old_delivery=[
  'A produção completa tem prazo estimado de 1 a 2 horas após a conclusão da gravação.',
  'A produção completa tem estimativa de 1 a 2 horas após a conclusão da gravação.',
  'Para produção completa, considere mais 1 a 2 horas após a conclusão da gravação, para edição e finalização.',
  'Para produção completa, a estimativa é de 1 a 2 horas após a gravação.']
 for old in old_delivery:s=s.replace(old,PRODUCTION)
 s=s.replace('Confirme pelo WhatsApp a disponibilidade da voz e o prazo de entrega de até 2 horas antes de finalizar o pedido.','Confirme a disponibilidade da voz antes de finalizar o pedido. '+PRODUCTION)
 s=s.replace('Compras, pedidos, acompanhamento e download são realizados pelo WhatsApp.','Compras, pedidos, acompanhamento e download podem ser realizados pelo Painel de Gravação. Para orientação e pedidos pelo WhatsApp, consulte os horários de atendimento.')
 if route=='termos':
  s=re.sub(r'(Se a entrega ocorrer após o expediente, entre na )<a\b[^>]*>.*?</a>( e consulte seus pedidos\.)',lambda m:m[1]+'<a href="'+LOGIN+'" data-cta="terms_orders_login">Painel de Gravação</a>'+m[2],s,flags=re.S)
  if 'data-production-policy' not in s:
   s=s.replace('<section id="prazos" class="terms-section"><h2>6. Pedidos, disponibilidade e estimativas</h2>','<section id="prazos" class="terms-section"><h2>6. Pedidos, disponibilidade e estimativas</h2><p data-production-policy>'+PRODUCTION+'</p>')
  s=s.replace('<time datetime="2026-10-16">16 de outubro de 2026</time>','<time datetime="2026-10-23">23 de outubro de 2026</time>')
 return s

def button(href,label,kind='secondary',cta=''):
 return f'<a class="rp-button rp-{kind}" href="{href}" data-cta="{cta}">{label}</a>'
def header():
 return '''<header class="al-header"><nav class="al-shell al-nav" aria-label="Navegação principal"><a class="al-brand" href="/" aria-label="A Locução — início"><img class="al-logo" src="/assets/brand/a-locucao-logo.png" width="1000" height="252" alt="A Locução" decoding="async"></a><button class="al-menu-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="al-main-menu"><span aria-hidden="true">☰</span><span>Menu</span></button><div class="al-menu" id="al-main-menu"><a href="/servicos/">Serviços</a><a href="/vozes/">Banco de Vozes</a><a href="/precos/">Preços</a><a href="/#painel-gravacao">Painel de Gravação</a><a href="'''+LOGIN+'''" data-cta="header_login">Entrar</a><a class="al-header-cta rp-header-register" href="'''+REGISTER+'''" data-cta="header_register">Criar conta grátis</a><a href="'''+WA+'''" data-cta="header_whatsapp">WhatsApp</a></div></nav></header>'''
def catalog():
 return '''<section class="rp-catalog" id="banco-de-vozes" data-recording-catalog><div class="rp-shell"><div class="rp-heading"><span class="rp-eyebrow">OUÇA ANTES DE ESCOLHER</span><h2>Encontre a voz certa para sua mensagem.</h2><p>Ouça as demonstrações, escolha seu locutor e faça seu pedido com praticidade.</p></div><iframe id="vitrine-vozes" data-voice-showcase src="https://vozes.alocucao.com.br/embed.php" title="Nossas vozes — catálogo oficial A Locução" loading="lazy" style="width:100%;min-height:640px;border:0"></iframe><p class="rp-catalog-ai-note" data-ai-voice-legend><strong>🧠</strong> Identificação de vozes IA: As vozes que apresentam o símbolo <strong>🧠</strong> após o nome são geradas por Inteligência Artificial. Ao contratar nossos serviços, você concorda com nossos <a href="https://vozes.alocucao.com.br/termos.php?plataforma=alocucao" target="_blank" rel="noopener">Termos de Uso</a>.</p><p class="rp-catalog-help">Prefere ajuda para escolher? <a href="'''+WA+'''" data-cta="catalog_whatsapp">Fale com nossa equipe pelo WhatsApp.</a></p></div></section>'''
def panel():
 benefits=[('24h','Pedidos a qualquer hora','Envie seu texto e solicite orçamentos, todos os dias.'),('Pix','Créditos com praticidade','Pague por Pix ou cartão. Créditos liberados imediatamente após a confirmação do pagamento.'),('↗','Acompanhe em tempo real','Veja o andamento de cada pedido no painel.'),('↓','Seus áudios organizados','Consulte o histórico e baixe as gravações concluídas.'),('↻','Produção todos os dias',PRODUCTION),('＋','Ofertas exclusivas','Confira as condições especiais disponíveis no painel.')]
 cards=''.join('<li><span class="rp-icon" aria-hidden="true">'+i+'</span><div><h3>'+t+'</h3><p>'+d+'</p></div></li>' for i,t,d in benefits)
 return '''<section class="rp-panel" id="painel-gravacao"><div class="rp-shell"><div class="rp-panel-intro"><div><span class="rp-eyebrow">PAINEL DE GRAVAÇÃO A LOCUÇÃO</span><h2>Seu próximo áudio começa aqui. A qualquer hora.</h2><p>Crie sua conta grátis para pedir locuções, consultar orçamentos e acompanhar suas gravações em um só lugar.</p><p class="rp-availability">Pedidos online 24h. Gravações até as 22h, conforme a disponibilidade de cada locutor.</p></div><figure class="rp-mockup"><div class="rp-laptop-screen"><div class="rp-window-bar" aria-hidden="true"><i></i><i></i><i></i><span>Painel de Gravação · A Locução</span></div><picture><source srcset="/assets/images/painel-real-640.webp 640w, /assets/images/painel-real-1280.webp 1280w" sizes="(max-width:800px) calc(100vw - 64px), 600px" type="image/webp"><img src="/assets/images/painel-real-1280.webp" width="1916" height="904" loading="lazy" decoding="async" alt="Tela real do Painel de Gravação A Locução, com locutores, pedidos e compra de créditos"></picture></div><div class="rp-laptop-base" aria-hidden="true"></div><figcaption>Conheça o ambiente onde você acompanha suas gravações.</figcaption></figure></div><ul class="rp-benefits">'''+cards+'''</ul><div class="rp-panel-bottom"><div class="rp-actions">'''+button(REGISTER,'Criar minha conta grátis','primary','panel_register')+button(LOGIN,'Já tenho conta — Entrar','secondary','panel_login')+'''</div><p>Prefere atendimento personalizado? Recebemos pedidos e oferecemos suporte pelo <a href="'''+WA+'''" data-cta="panel_whatsapp">WhatsApp</a>, de segunda a sexta-feira, das 8h às 18h.</p></div></div></section>'''
def process():
 return '''<section class="rp-process" id="como-funciona"><div class="rp-shell"><div class="rp-heading"><span class="rp-eyebrow">COMO FUNCIONA</span><h2>Você escolhe como prefere pedir.</h2><p>Conte com nossa equipe ou faça tudo online pelo Painel de Gravação.</p></div><div class="rp-paths"><article><h3>Pelo Painel de Gravação</h3><p class="rp-channel-hours">Pedidos 24 horas por dia</p><ol><li>Crie sua conta grátis.</li><li>Escolha a voz, envie seu texto e as orientações.</li><li>Confira o valor e adquira os créditos necessários.</li><li>Confirme o pedido e acompanhe o andamento.</li><li>Baixe seu áudio quando estiver pronto.</li></ol>'''+button(REGISTER,'Criar conta grátis','primary','process_register')+'''</article><article><h3>Pelo WhatsApp</h3><p class="rp-channel-hours">Segunda a sexta, das 8h às 18h</p><ol><li>Entre em contato com nossa equipe.</li><li>Envie o texto e as orientações.</li><li>Escolha a voz e confirme o orçamento.</li><li>Receba seu áudio conforme o prazo informado.</li></ol>'''+button(WA,'Pedir pelo WhatsApp','whatsapp','process_whatsapp')+'''</article></div></div></section>'''
FAQ=[('Preciso criar uma conta para pedir uma locução?','Não necessariamente. Você pode pedir pelo WhatsApp durante o horário comercial ou criar uma conta gratuita para fazer pedidos pelo Painel de Gravação.'),('O cadastro no Painel de Gravação é gratuito?','Sim. Criar a conta é gratuito. Você paga pelos serviços e créditos que contratar.'),('Posso fazer pedidos de madrugada?','Sim. O painel aceita pedidos 24 horas por dia. As gravações seguem o horário e a disponibilidade de cada locutor, com profissionais disponíveis até as 22h.'),('Como posso pagar pelo painel?','Você pode comprar créditos por Pix ou cartão de crédito, com liberação imediata após a confirmação do pagamento.'),('Posso acompanhar meus pedidos?','Sim. No painel você acompanha o andamento dos pedidos, consulta o histórico e baixa as gravações concluídas.'),('Ainda posso ser atendido pelo WhatsApp?','Sim. Nossa equipe orienta e recebe pedidos de segunda a sexta-feira, das 8h às 18h.')]
def faqs(route):
 selected=FAQ if route in {'','precos','vozes'} else [FAQ[0],FAQ[2],FAQ[5]]
 return '<section class="rp-faq" id="duvidas-painel"><div class="rp-shell"><div class="rp-heading"><h2>Dúvidas sobre pedidos e atendimento</h2></div>'+''.join('<details><summary>'+q+'</summary><p>'+a+'</p></details>' for q,a in selected)+'</div></section>'
def prices(s):
 for old,new in [('12','10'),('30','25')]:
  s=re.sub(r'R\$\s*'+old+r'(?:,00)?(?![\d,])','R$ '+new+',00',s)
  s=s.replace('R%24%20'+old+'%2C00','R%24%20'+new+'%2C00')
 return s

def update(s,route):
 s=re.sub(r'<link[^>]*href="/assets/credit-packages\.css[^"]*"[^>]*>','',s)
 s=re.sub(r'<section class="cp-final".*?</section>','',s,flags=re.S)
 s=re.sub(r'<!-- commercial-packages:start -->.*?<!-- commercial-packages:end -->','',s,flags=re.S)
 s=public_policy(prices(s),route)
 s=re.sub(r'<(?:script|link)\b[^>]*(?:src|href)=[\"\']/assets/selected-voices\.(?:js|css)[^\"\']*[\"\'][^>]*>(?:</script>)?','',s)
 if re.search(r'http-equiv=["\']refresh',s,re.I):
  if route in {'cadastro','painel'}:
   dest=REGISTER if route=='cadastro' else LOGIN
   s=re.sub(r'(<meta[^>]*http-equiv=["\']refresh["\'][^>]*content=)["\'][^"\']*["\']',lambda m:m[1]+'"0;url='+dest+'"',s,flags=re.I)
   s=re.sub(r'href=["\']https://wa.me/[^"\']*["\']','href="'+dest+'"',s)
   s=s.replace('Fazer pedido pelo WhatsApp','Continuar para o Painel de Gravação').replace('Solicitar orçamento pelo WhatsApp','Continuar para o Painel de Gravação')
  return s
 if '<main' not in s or '<body' not in s:return s
 # Discard superseded widgets and their global link rewriter before restoring panel exits.
 s=re.sub(r'<!-- selected-voices:start -->.*?<!-- selected-voices:end -->',catalog(),s,flags=re.S)
 s=re.sub(r'<!-- unified-catalog:start -->.*?<!-- unified-catalog:end -->',catalog(),s,flags=re.S)
 s=rewrite(s,lambda t,a,b:t=='script' and 'vitrineVozes' in b)
 s=re.sub(r'<(?:script|link)\b[^>]*(?:src|href)=["\']/assets/(?:selected-voices|unified-voices|voice-bank|landing-voices|home-voices|featured-voices)\.(?:js|css)[^"\']*["\'][^>]*>(?:</script>)?','',s)
 # Duplicate historical help blocks obscure the two channels.
 s=rewrite(s,lambda t,a,b:(t=='div' and 'hybrid-catalog-order' in a.get('class','').split()) or (t=='section' and a.get('id')=='painel-de-gravacao'))
 s=re.sub(r'<body\b[^>]*>',lambda m:re.sub(r'\sdata-order-channels=["\'][^"\']*["\']','',m[0])[:-1]+' data-order-channels="dual">',s,count=1)
 s=rewrite(s,lambda t,a,b:t=='header',header())
 # A consistent menu has a single accessible mobile toggle on every layout.
 for asset,kind in [('site-layout.css','link'),('site-layout.js','script'),('recording-panel.css','link'),('recording-panel.js','script')]:
  s=re.sub(r'<(?:link|script)\b[^>]*(?:href|src)=["\']/assets/'+re.escape(asset)+r'[^"\']*["\'][^>]*>(?:</script>)?','',s)
  tag='<link rel="stylesheet" href="/assets/'+asset+'?v='+VERSION+'">' if kind=='link' else '<script src="/assets/'+asset+'?v='+VERSION+'" defer></script>'
  s=s.replace('</head>',tag+'\n</head>',1)
 # Replace contradictory hours, including historical Saturday support.
 s=rewrite(s,lambda t,a,b:t=='p' and bool(re.search(r'(?:Atendimento pelo WhatsApp:|Atendimento humano de segunda|Atendimento e pedidos pelo WhatsApp:)',plain(b),re.I)), '<p>'+HOURS+'</p>')
 s=s.replace('Pedidos e atendimento pelo WhatsApp.','Pedidos pelo painel ou pelo WhatsApp.').replace('Faça pedidos e acompanhe cada etapa pelo WhatsApp.','Faça pedidos e acompanhe cada etapa pelo Painel de Gravação, ou conte com nossa equipe pelo WhatsApp.')
 s=s.replace('A seleção desta página identifica a modalidade das demonstrações.','Consulte as características e a disponibilidade da voz antes de confirmar seu pedido.')
 s=s.replace('Envie seu texto pelo WhatsApp. Nossa equipe confirma a voz, o serviço, o valor e o prazo e acompanha seu pedido até a entrega.','Faça pedidos 24h pelo painel e acompanhe cada etapa online. Para orientação, fale pelo WhatsApp de segunda a sexta, das 8h às 18h.')
 # Footer access is available on editorial pages, too.
 def footer(m):
  f=m[0]
  f=re.sub(r'(<h2>Pedidos e (?:atendimento|suporte)</h2>)(?:<a[^>]*data-cta="footer_(?:register|login)"[^>]*>.*?</a>)*',lambda x:x[1]+f'<a href="{REGISTER}" data-cta="footer_register">Criar conta grátis</a><a href="{LOGIN}" data-cta="footer_login">Acessar minha conta</a>',f,flags=re.S)
  if 'data-cta="footer_register"' not in f:
   f=f.replace('</footer>','<div class="rp-footer-access">'+button(REGISTER,'Criar conta grátis','secondary','footer_register')+button(LOGIN,'Acessar minha conta','secondary','footer_login')+'<p>'+HOURS+'</p></div></footer>')
  return f
 s=re.sub(r'<footer\b.*?</footer>',footer,s,flags=re.S)
 if route in COMMERCIAL:
  # Remove prior integration sections before inserting the canonical versions.
  s=rewrite(s,lambda t,a,b:t=='section' and bool(set(a.get('class','').split()) & {'rp-panel','rp-process','rp-faq'}))
  s=rewrite(s,lambda t,a,b:t=='section' and (a.get('id')=='como-funciona' or ('rp-process' not in a.get('class','').split() and '<audio' not in b and '<details' not in b and bool(re.search(r'<h2[^>]*>\s*(?:Como fazer seu pedido|Seu áudio começa com uma conversa|Como funciona)\s*</h2>',b,re.I)))))
  # A single voice showcase; real produced-work audio remains outside it.
  sections=[n for n in Nodes(s).nodes if n['tag']=='section' and n['attrs'].get('id')=='banco-de-vozes']
  edits=[]
  for i,n in enumerate(sections):edits.append((n['start'],n['end'],catalog() if i==0 else ''))
  for a,b,c in reversed(edits):s=s[:a]+c+s[b:]
  if not sections:s=s.replace('</main>',catalog()+'</main>',1)
  # Hero actions always distinguish the direct conversation from account creation.
  def actions(m):
   original=m[0]
   href=re.search(r'href=["\'](https://wa.me/[^"\']*)',original)
   wa=href[1] if href else WA
   return '<div class="rp-actions rp-hero-actions">'+button(wa,'Pedir pelo WhatsApp','whatsapp','hero_whatsapp')+button(REGISTER,'Criar conta grátis','secondary','hero_register')+'</div>'
  s=re.sub(r'<div\b[^>]*class=["\'][^"\']*(?:commercial-actions|hero-actions|hero-ctas|hero-buttons)[^"\']*["\'][^>]*>.*?</div>',actions,s,count=1,flags=re.S)
  # The integration's own hero actions need the same treatment on repeated builds.
  s=re.sub(r'<div class="rp-actions rp-hero-actions">.*?</div>',actions,s,count=1,flags=re.S)
  # Remove repeated historical pricing summaries; one full section is sufficient.
  summaries=[n for n in Nodes(s).nodes if n['tag']=='section' and 'sv-price-summary' in n['attrs'].get('class','').split()]
  for n in reversed(summaries[1:]):s=s[:n['start']]+s[n['end']:]
  # Order only top-level commercial sections; preserve all other content and sample files.
  nodes=Nodes(s).nodes;main=next(n for n in nodes if n['tag']=='main')
  top=[n for n in nodes if n['parent'] is main and n['tag']=='section' and n.get('end')]
  bank=next((n for n in top if n['attrs'].get('id')=='banco-de-vozes'),None)
  price=next((n for n in top if n['attrs'].get('id')=='precos' or set(n['attrs'].get('class','').split()) & {'sf-offer','sv-price-summary'}),None)
  samples=[n for n in top if '<audio' in s[n['start']:n['end']] and 'banco-de-vozes'!=n['attrs'].get('id')]
  if bank:
   fragments=[]
   # Curated real-work samples precede the full catalog and prices.
   fragments.extend(s[n['start']:n['end']] for n in samples)
   fragments.append(s[bank['start']:bank['end']])
   if price:fragments.append(s[price['start']:price['end']])
   fragments.extend([panel(),process()])
   moved=[bank]+samples+([price] if price else [])
   edits=[(n['start'],n['end'],'') for n in moved]
   # Insert at the original showcase position, after the service presentation.
   edits=[(a,b,'\n'.join(fragments) if a==bank['start'] else c) for a,b,c in edits]
   for a,b,c in sorted(edits,reverse=True):s=s[:a]+c+s[b:]
  s=s.replace('</main>',faqs(route)+'</main>',1)
  # Repair obsolete catalog-only metadata with current, verifiable capabilities.
  if route in {'vozes','locutores'}:
   title='Banco de Vozes: Ouça e Escolha seu Locutor | A Locução' if route=='vozes' else 'Locutores para Comerciais e Vídeos | A Locução'
   desc='Ouça demonstrações na vitrine oficial, consulte a disponibilidade dos locutores e peça pelo painel ou WhatsApp. Cadastro gratuito no Painel de Gravação.'
   s=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',s,count=1,flags=re.S)
   s=re.sub(r'(<meta[^>]*(?:name|property)="(?:description|og:description|twitter:description)"[^>]*content=")[^"]*',lambda m:m[1]+desc,s)
   s=re.sub(r'(<meta[^>]*(?:name|property)="(?:og:title|twitter:title)"[^>]*content=")[^"]*',lambda m:m[1]+title,s)
   if route=='vozes':s=re.sub(r'<h1[^>]*>.*?</h1>','<h1>Ouça, escolha sua voz e faça seu pedido.</h1>',s,count=1,flags=re.S)
  # Every anchor stays meaningful after removal of superseded widgets.
  ids=set(re.findall(r'\bid="([^"]+)"',s))
  s=re.sub(r'href="#([^"]+)"',lambda m:m[0] if m[1] in ids else 'href="#banco-de-vozes"',s)
 # Existing order/payment FAQs must describe the same two channels.
 def faq_answer(m):
  question=plain(m[2]);answer=m[3]
  if re.search(r'(?:pedido|pedir).*(?:qualquer hora|24h)|(?:qualquer hora|24h).*(?:pedido|pedir)',question,re.I):answer='<p>'+FAQ[2][1]+' Pelo WhatsApp, recebemos pedidos de segunda a sexta, das 8h às 18h.</p>'
  elif re.search(r'(?:pagar|pagamento|cartão)',question,re.I):answer='<p>'+FAQ[3][1]+' Para pedidos pelo WhatsApp, nossa equipe orienta o pagamento antes da confirmação.</p>'
  return m[1]+m[2]+'</summary>'+answer+'</details>'
 s=re.sub(r'(<details\b[^>]*>\s*<summary[^>]*>)(.*?)</summary>(.*?)</details>',faq_answer,s,flags=re.S)
 # Apply current operational policy to generated sections before synchronizing schemas.
 s=public_policy(s,route)
 # Attribution must cover editorial navigation and every ad landing, not only older layouts.
 s=re.sub(r'<script\b[^>]*src=[\"\']/assets/commercial-refresh\.js[^\"\']*[\"\'][^>]*></script>','',s)
 s=s.replace('</head>','<script src="/assets/commercial-refresh.js?v='+ATTRIBUTION_VERSION+'" defer></script>\n</head>',1)
 # Sync structured prices and FAQ answers to the published copy; no stale manual voice list.
 faqlist=[(plain(q),plain(a)) for q,a in re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>',s,re.S)]
 def schema(m):
  try:d=json.loads(m[2])
  except json.JSONDecodeError:return m[0]
  def walk(o):
   if isinstance(o,dict):
    if o.get('@type')=='FAQPage' and faqlist:o['mainEntity']=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqlist]
    if o.get('@type') in {'ItemList'} and re.search(r'vozes|locutores',o.get('name',''),re.I):
     o.pop('numberOfItems',None);o.pop('itemListElement',None)
    for k,v in list(o.items()):
     if k in {'price','lowPrice','highPrice'} and str(v) in {'12','12.00','30','30.00'}:o[k]='10.00' if str(v).startswith('12') else '25.00'
     elif isinstance(v,str):o[k]=prices(v)
     else:walk(v)
   elif isinstance(o,list):
    for v in o:walk(v)
  walk(d)
  return m[1]+json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+m[3]
 s=re.sub(r'(<script[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',schema,s,flags=re.S)
 s=re.sub(r"</section>\s*<section", "</section>\n<section", s)
 return POLICY['update'](re.sub(r"\n(?:[ \t]*\n)+", "\n", s),route,COMMERCIAL)

def main():
 changed=[]
 for p in sorted(ROOT.rglob('*.html')):
  if any(x.startswith('.') or x in {'node_modules','_site'} for x in p.relative_to(ROOT).parts):continue
  route=p.parent.relative_to(ROOT).as_posix();route='' if route=='.' else route
  if p.name!='index.html':route='file:'+p.relative_to(ROOT).as_posix()
  old=p.read_text();new=update(old,route)
  if old!=new:p.write_text(new);changed.append(str(p.relative_to(ROOT)))
 print('Recording panel integration:',len(changed),'pages updated')
if __name__=='__main__':main()
