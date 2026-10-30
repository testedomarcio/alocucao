#!/usr/bin/env python3
"""Build the approved A Locução site from first-party data. No provider synchronization."""
from pathlib import Path
import json,html,re,urllib.parse,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
E=html.escape
BASE='https://alocucao.com.br'
voices=json.loads((ROOT/'data/new-voices.json').read_text())
from manual_reviews import load_reviews,summarize
customer_reviews=load_reviews(ROOT/'data/customer-reviews.json',{v['slug'] for v in voices})
for review in customer_reviews:
 if review.get('image') and not (ROOT/review['image'].lstrip('/')).is_file():raise ValueError('Review image is missing')
latest_works=json.loads((ROOT/'data/latest-works.json').read_text())
top_voices=json.loads((ROOT/'data/top-voices.json').read_text())
top_ranks={entry['voice']:entry['rank'] for entry in top_voices['entries']}
work_voices={project['voice'] for project in latest_works}
from voice_orders import confirmed_counts
delivered_counts=confirmed_counts(json.loads((ROOT/'data/delivered-orders.json').read_text()),{v['slug'] for v in voices})
if delivered_counts:
 import runpy
 top_voices={'basis':'verified_delivered_orders','entries':runpy.run_path(str(ROOT/'scripts/update-top-voices.py'))['rank'](voices,delivered_counts)}
 top_ranks={entry['voice']:entry['rank'] for entry in top_voices['entries']}
HOURS='Segunda a sexta-feira: 08h às 18h. Sábado: 08h às 12h. Horário de Brasília.'
ENTITY='69.502.587 MARCIO PEREIRA DE SOUZA · CNPJ 69.502.587/0001-33'
ADDRESS=''
def wa(message='Olá! Conheci a A Locução e gostaria de solicitar um orçamento.'):
 return 'https://wa.me/5527996529832?text='+urllib.parse.quote(message,safe='')
def cta(label='Solicitar orçamento',message='',css='',voice=''):
 return f'<a class="btn {css}" href="{wa(message) if message else wa()}" data-cta="orcamento" data-voice-name="{E(voice)}">{E(label)} <span aria-hidden="true">↗</span></a>'
header='''<a class="skip" href="#conteudo">Ir para o conteúdo</a><header class="site-head"><div class="wrap head-row"><a class="brand" href="/" aria-label="A Locução — início"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>A LOCUÇÃO<span aria-hidden="true">®</span></a><button class="menu-toggle" aria-expanded="false" aria-controls="menu-principal">Menu</button><nav class="nav" id="menu-principal" aria-label="Navegação principal"><a href="/vozes/">Banco de Vozes</a><a href="/servicos/">Serviços</a><a href="/precos/">Preços</a><a href="/sobre/">Sobre</a>'''+cta('Vamos conversar',css='secondary')+'''</nav></div></header>'''
# Brand registration is not established; use an ordinary wordmark.
header=header.replace('<span aria-hidden="true">®</span>','')
header=header.replace('<a href="/vozes/">Banco de Vozes</a><a href="/servicos/">Serviços</a><a href="/precos/">Preços</a><a href="/sobre/">Sobre</a>', '<a href="/">Início</a><a href="/servicos/">Serviços</a><a href="/vozes/">Banco de Vozes</a><a href="/calculadora/">Calculadora</a><a href="/sobre/">Sobre Nós</a><a href="/contato/">Contato</a>')
footer=f'''<section class="contact-band"><div class="wrap"><h2>Sua mensagem merece<br>uma voz à altura.</h2>{cta('Vamos criar seu próximo áudio')}</div></section><footer class="site-footer"><div class="wrap"><div class="footer-grid"><div><div class="footer-brand">A LOCUÇÃO</div><p>A voz certa para sua mensagem.</p><p>Locução, narração e soluções profissionais em áudio. Atendimento online para empresas, agências, criadores e instituições em todo o Brasil.</p></div><div><h3>Explore</h3><nav class="footer-links" aria-label="Links do rodapé"><a href="/vozes/">Banco de Vozes</a><a href="/servicos/">Serviços</a><a href="/sobre/">Sobre a A Locução</a><a href="/blog/">Conteúdos</a><a href="/contato/">Contato</a></nav></div><div><h3>Atendimento</h3><p>{HOURS}</p><p><a href="{wa()}">WhatsApp: (27) 99652-9832</a><br><a href="mailto:suporte@alocucao.com.br">suporte@alocucao.com.br</a></p><nav class="footer-links" aria-label="Informações legais"><a href="/termos/">Termos de Uso</a><a href="/politica-de-privacidade/">Privacidade</a><a href="/licenciamento-comercial/">Licenciamento Comercial</a></nav></div></div><div class="footer-bottom"><p class="technology-note">As imagens dos perfis são ilustrativas. As vozes deste catálogo são produzidas com tecnologia de inteligência artificial. Saiba mais em nossos <a href="/termos/#tecnologia">Termos de Uso</a>.</p><p>{ENTITY}<br>{ADDRESS}</p><p>© 2026 A Locução. Os horários informados são de atendimento. O prazo de produção é confirmado em cada orçamento.</p></div></div></footer>'''
org={'@type':'Organization','@id':BASE+'/#organization','name':'A Locução','legalName':'69.502.587 MARCIO PEREIRA DE SOUZA','taxID':'69.502.587/0001-33','url':BASE+'/','telephone':'+5527996529832','email':'suporte@alocucao.com.br','address':{'@type':'PostalAddress','streetAddress':'Rua Euzebio Cirilo de Souza, 344, Centro','addressLocality':'Brejetuba','addressRegion':'ES','postalCode':'29630-000','addressCountry':'BR'},'contactPoint':{'@type':'ContactPoint','contactType':'Atendimento','telephone':'+5527996529832','hoursAvailable':[{'@type':'OpeningHoursSpecification','dayOfWeek':['Monday','Tuesday','Wednesday','Thursday','Friday'],'opens':'08:00','closes':'18:00'},{'@type':'OpeningHoursSpecification','dayOfWeek':'Saturday','opens':'08:00','closes':'12:00'}]}}
org.pop('address', None) # Await current company registration before publishing an address.
built=[]
prior_sitemap={}
if (ROOT/'sitemap.xml').exists():
 for node in ET.parse(ROOT/'sitemap.xml').getroot():
  fields={child.tag.rsplit('}',1)[-1]:child.text for child in node}
  prior_sitemap[fields.get('loc')]=fields.get('lastmod')
def write(path,title,desc,body,index=True,extra=None,canonical=None):
 from sample_offer import enhance
 body,sample_enabled=enhance(path.strip('/'),body)
 path=path.strip('/'); file=ROOT/(path if path.endswith('.html') else path+'/index.html' if path else 'index.html');file.parent.mkdir(parents=True,exist_ok=True)
 url=BASE+('/'+path if path.endswith('.html') else '/'+path+'/' if path else '/')
 canonical=canonical or url
 schemas={'@context':'https://schema.org','@graph':[org,{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'publisher':{'@id':BASE+'/#organization'}}]+(extra or [])}
 service_message={**{s['slug']:'Olá! Gostaria de um orçamento de '+s['name'].lower()+'.' for s in json.loads((ROOT/'data/premium-services.json').read_text())},'locucao-off':'Olá! Gostaria de contratar uma Locução Off.','spot-comercial':'Olá! Quero um orçamento para Produção Completa.'}.get(path)
 if path=='locutores/lucan-rook':service_message=voice_message(next(v for v in voices if v['slug']=='lucan-rook'))
 page_header=header.replace(wa(),wa(service_message)) if service_message else header
 page_footer=footer.replace(wa(),wa(service_message)) if service_message else footer
 nova_version = '20261027services' if 'class="calculator"' in body or 'service-demos' in body or 'calculator-callout' in body else '20261026premium'
 if path=='locutores/lucan-rook':nova_version='20261027lucan'
 if 'class="voice-card"' in body or 'data-review-voice=' in body:nova_version='20261027cards2'
 if 'class="calculator"' in body:nova_version='20261027calculator'
 review_assets = '<meta name="referrer" content="no-referrer"><script data-review-privacy>window.__reviewInvite=new URLSearchParams(location.search).get("convite");if(window.__reviewInvite){const p=new URLSearchParams(location.search);p.delete("convite");history.replaceState(null,"",location.pathname+(p.size?"?"+p:"")+location.hash);}</script><link rel="stylesheet" href="/assets/reviews.css?v=20261027manual1">' if 'data-rating-voice=' in body or 'data-review-admin' in body else ''
 if 'data-work-empty' in body:review_assets+='<script src="/assets/voice-ui.js?v=20261027cards2" defer></script>'
 sample_assets='<link rel="stylesheet" href="/assets/sample-offer.css?v=20261029">' if sample_enabled else ''
 page=f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="{'index,follow' if index else 'noindex,follow'},max-image-preview:large"><link rel="canonical" href="{E(canonical)}"><meta name="theme-color" content="#173b2a"><link rel="icon" href="/favicon.svg"><meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(canonical)}"><meta property="og:image" content="{BASE}/assets/images/estudio-locucao-960.webp"><meta name="twitter:card" content="summary_large_image">{review_assets}{sample_assets}<link rel="stylesheet" href="/assets/nova.css?v={nova_version}"><script src="/assets/privacy.js" defer></script><script src="/assets/tracking.js?v=20261026premium" defer></script><script src="/assets/nova.js?v={nova_version}" defer></script><script type="application/ld+json">{json.dumps(schemas,ensure_ascii=False).replace('<','\\u003c')}</script></head><body data-page="{E(path)}">{page_header}<main id="conteudo">{body}</main>{page_footer}</body></html>'''
 if sample_enabled:page=page.replace('/assets/tracking.js?v=20261026premium','/assets/tracking.js?v=20261029samples')
 if path=='':page=page.replace('</head>','<link rel="stylesheet" href="/assets/home-hero.css?v=20261030"></head>')
 file.write_text(page)
 built.append({'path':str(file.relative_to(ROOT)),'url':url,'index':index,'canonical':canonical})
def hero(kicker,title,desc,buttons=True):
 return f'<section class="hero"><div class="wrap"><span class="eyebrow">{E(kicker)}</span><h1>{title}</h1><p class="lead">{desc}</p>'+(f'<div class="actions">{cta()}<a class="btn secondary" href="/vozes/">Conhecer as vozes</a></div>' if buttons else '')+'</div></section>'
def audio(v,kind,instance=""):
 suffix="-"+instance if instance else ""
 path=v.get(kind)
 if not path:return ''
 label='Locução Off' if kind=='off' else 'Produção Completa'
 temporary=v.get('temporary_demo',{}).get(kind)
 notice='<p class="temporary-demo">Amostra temporária: mesma Locução Off, sem trilha ou produção. Atualização em preparação.</p>' if temporary else ''
 return f'<div class="audio-item"><label class="audio-label" for="audio-{v["slug"]}-{kind}{suffix}">{label}</label><audio id="audio-{v["slug"]}-{kind}{suffix}" controls preload="none" aria-label="{label} de {E(v["name"])}" src="{E(path)}">Seu navegador não suporta reprodução de áudio.</audio>{notice}<p class="audio-error" hidden>Não foi possível carregar este áudio. Solicite a demonstração pelo WhatsApp.</p></div>'
service_demos=json.loads((ROOT/'data/service-demos.json').read_text())
def service_demo(slug):
 demo=service_demos.get(slug)
 if not demo:return '',[]
 players=[];schemas=[]
 for track in demo['tracks']:
  label=('Locução Off' if len(demo['tracks'])>1 else 'Ouvir demonstração — Off') if track['kind']=='off' else 'Versão Produzida'
  player_id='service-demo-'+slug+'-'+track['kind']
  duration=track['duration_seconds']; seconds=round(duration); display=f'{seconds//60}:{seconds%60:02d}'
  accessible=label+' — '+demo['voice']
  players.append(f'<article class="content-card"><h3 id="{player_id}-label">{label}</h3><p>{E(demo["voice"])} · MP3 · {display}</p><div class="audio-item"><audio id="{player_id}" controls preload="none" aria-labelledby="{player_id}-label {player_id}-voice" src="{track["src"]}">Seu navegador não suporta reprodução de áudio.</audio><span id="{player_id}-voice" class="sr-only">Voz: {E(demo["voice"])}</span><p class="audio-error" role="status" hidden>Não foi possível carregar este áudio. Solicite a demonstração pelo WhatsApp.</p></div></article>')
  schemas.append({'@type':'AudioObject','name':slug.replace('-',' ')+' — '+accessible,'contentUrl':BASE+track['src'],'encodingFormat':'audio/mpeg','duration':f'PT{duration}S'})
 note='As amostras ilustram possibilidades de interpretação e acabamento. Trilha e edição da versão produzida dependem do escopo aprovado no orçamento.' if len(demo['tracks'])>1 else 'Amostra de voz sem trilha ou efeitos. As etapas de produção são definidas no orçamento do seu projeto.'
 return '<section class="section service-demos" id="demonstrativos-servico" aria-labelledby="service-demo-heading"><div class="wrap"><span class="eyebrow">Ouça este serviço</span><h2 id="service-demo-heading">Dê o primeiro play.</h2><p>Demonstração com a voz de '+E(demo['voice'])+'.</p><div class="content-grid">'+''.join(players)+'</div><p class="note">'+note+'</p></div></section>',schemas
def recent_works(v):
 projects=sorted([p for p in latest_works if p['voice']==v['slug']],key=lambda p:(p['date'],p['id']),reverse=True)
 if not projects:return '',[]
 cards=[];schemas=[]
 for project in projects:
  date=project['date'];display_date='/'.join(reversed(date.split('-')));players=[]
  for i,track in enumerate(project['tracks'],1):
   player_id='work-'+project['id']+'-'+str(i)
   label=track['title']+' — '+project['title']+' — '+v['name']
   players.append(f'<div class="audio-item"><label class="audio-label" for="{E(player_id)}">{E(track["title"])}</label><audio id="{E(player_id)}" controls preload="none" aria-label="{E(label)}" src="{E(track["src"])}">Seu navegador não suporta reprodução de áudio.</audio><p class="audio-error" hidden>Não foi possível carregar este áudio. Fale com nossa equipe pelo WhatsApp.</p></div>')
   schemas.append({'@type':'AudioObject','name':label,'contentUrl':BASE+track['src'],'encodingFormat':'audio/mpeg'})
  cards.append(f'<article class="content-card"><span class="eyebrow">{E(project["format"])}</span><h3>{E(project["title"])}</h3><p><time datetime="{E(date)}">{E(display_date)}</time></p>'+''.join(players)+'</article>')
 return '<section class="section" id="ultimos-trabalhos" aria-labelledby="recent-work-heading"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Na prática</span><h2 id="recent-work-heading">Últimos trabalhos</h2></div><p>Ouça trabalhos recentes com a voz '+E(v['name'])+'.</p></div><div class="content-grid">'+''.join(cards)+'</div></div></section>',schemas
def portrait(v):
 if v.get('image'):return f'<img src="{v["image"]}" width="480" height="480" loading="lazy" decoding="async" alt="Retrato ilustrativo da voz {E(v["name"])}">'
 return f'<div class="portrait-placeholder" aria-label="Perfil de voz {E(v["name"])}">{E(v["name"][0])}</div>'
def display_name(v):
 return E(v['name'])+(' <span class="exclusive-badge" aria-label="Voz exclusiva A Locução">💎</span>' if v.get('exclusive') is True else '')
def language_badge(v):
 if not v.get('language_code'):return ''
 return '<p class="voice-language"><span aria-hidden="true">'+E(v['language_flag'])+'</span> '+E(v['language_label'])+' <span lang="en">· English (US)</span></p>'
def voice_message(v):
 if v.get('language_code')=='en-US':return 'Olá! Tenho interesse na voz do locutor '+v['name']+', em inglês americano. Gostaria de mais informações.'
 return f'Olá! Conheci a voz {v["name"]} no site da A Locução e gostaria de solicitar um orçamento.'
def voice_search(v):
 text=v['name']+' '+v['style']+' '+ ' '.join(v['applications'])
 if v.get('language_label'):text+=' '+v['language_label']+' English US'
 return text
def rating(slug,linked=True):
 average,count=summarize(customer_reviews,slug)
 label=(f"{average:.1f}".replace(".",",")+"/5 · "+str(count)+(" avaliação" if count==1 else " avaliações")) if count else "0 avaliações"
 fill=f"{average*20:.4f}".rstrip("0").rstrip(".") if count else "0"
 star_svg='<svg viewBox="0 0 120 24" width="120" height="24" focusable="false">'+''.join('<path transform="translate('+str(i*24)+' 0)" d="m12 2 3.1 6.3 7 .9-5.1 5 1.2 7-6.2-3.3L5.8 21l1.2-6.8-5.1-5 7-.9Z"/>' for i in range(5))+'</svg>'
 markup = '<div class="review-rating" data-rating-voice="'+E(slug)+'" aria-label="'+E(label if count else 'Ainda sem avaliações')+'"><span class="review-stars" aria-hidden="true"><span>'+star_svg+'</span><span class="review-stars-fill" style="width:'+fill+'%">'+star_svg+'</span></span><span class="review-count">'+E(label)+'</span></div>'
 return '<a class="review-rating-link" href="/locutores/'+E(slug)+'/#avaliacoes-clientes" aria-label="Ver avaliações deste locutor">'+markup+'</a>' if linked else markup
def icon(kind):
 paths={'headphones':'<path d="M4 14v-3a8 8 0 0 1 16 0v3M4 13h3v8H4a2 2 0 0 1-2-2v-4a2 2 0 0 1 2-2Zm16 0h-3v8h3a2 2 0 0 0 2-2v-4a2 2 0 0 0-2-2Z"/>','trophy':'<path d="M8 3h8v7a4 4 0 0 1-8 0V3Zm0 2H4v3a4 4 0 0 0 4 4m8-7h4v3a4 4 0 0 1-4 4m-4 2v5m-4 2h8"/>','medal':'<path d="m7 2 5 7 5-7M5 2h4m6 0h4"/><circle cx="12" cy="15" r="7"/><path d="m12 11 1.2 2.4 2.7.4-2 1.9.5 2.7-2.4-1.3-2.4 1.3.5-2.7-2-1.9 2.7-.4Z"/>','check':'<path d="m8 12 3 3 5-6"/><circle cx="12" cy="12" r="9"/>'}
 return '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+paths[kind]+'</svg>'
def top_badge(v):
 rank=top_ranks.get(v['slug'])
 if not rank:return ''
 label='TOP 1 · Mais pedido' if rank==1 else 'TOP '+str(rank)+' · Entre os mais pedidos'
 basis='Classificação atual pelos trabalhos publicados; não representa um total de pedidos entregues.' if top_voices.get('basis')=='published_projects' else 'Classificação por pedidos entregues confirmados.'
 return '<span class="top-voice-badge top-rank-'+str(rank)+'" title="'+basis+'">'+icon('trophy' if rank==1 else 'medal')+'<span>'+label+'</span></span>'
def delivered_indicator(v):
 count=delivered_counts.get(v['slug'])
 if not count:return ''
 return '<p class="delivered-orders">'+icon('check')+'<span>'+str(count)+' '+('pedido entregue' if count==1 else 'pedidos entregues')+'</span></p>'
def works_link(v):
 inner=icon('headphones')+'<span><strong>Ver últimos trabalhos</strong><small>Conheça produções realizadas</small></span><span class="work-arrow" aria-hidden="true">↗</span>'
 if v['slug'] in work_voices:return '<a class="recent-work-link" href="/locutores/'+v['slug']+'/#ultimos-trabalhos">'+inner+'</a>'
 return '<button type="button" class="recent-work-link" data-work-empty="'+v['slug']+'" data-voice-label="'+E(v['name'])+'" aria-haspopup="dialog">'+inner+'</button>'
def reviews_section(v):
 rows=sorted([r for r in customer_reviews if r['voice']==v['slug']],key=lambda r:(r['published_on'],r['id']),reverse=True)
 cards=[]
 for row in rows:
  picture=('<img src="'+E(row['image'])+'" width="72" height="72" loading="lazy" decoding="async" alt="'+E(row.get('company') or row['name'])+'">') if row.get('image') else ''
  company='<p class="review-company">'+E(row['company'])+'</p>' if row.get('company') else ''
  links=('<ul class="review-links">'+''.join('<li><a href="'+E(link['url'])+'" target="_blank" rel="noopener noreferrer">'+E(link['label'])+'</a></li>' for link in row.get('links',[]))+'</ul>') if row.get('links') else ''
  cards.append('<article class="review-card" data-review-id="'+E(row['id'])+'"><header class="review-client">'+picture+'<div><h3>'+E(row['name'])+'</h3>'+company+'<p class="review-score">'+str(row['rating'])+'/5</p></div></header><blockquote>'+E(row['comment'])+'</blockquote>'+links+'<p class="review-date">Publicado em <time datetime="'+row['published_on']+'">'+'/'.join(reversed(row['published_on'].split('-')))+'</time></p></article>')
 content=''.join(cards[:10])+('<details class="review-more"><summary>Ver mais avaliações</summary>'+''.join(cards[10:])+'</details>' if len(cards)>10 else '') if rows else '<p>Ainda não há avaliações publicadas para este locutor.</p>'
 return '<section class="section reviews-section" id="avaliacoes-clientes"><span id="avalie" aria-hidden="true"></span><div class="wrap"><span class="eyebrow">Experiências com esta voz</span><h2>Avaliações de clientes</h2>'+rating(v['slug'],False)+content+'</div></section>'
def voicecard(v,primary="off",context="",heading=3,filter_language=False):
 secondary="off" if primary=="producao" else "producao"
 language_attr=(' data-language="'+E(v.get("language_code","pt-BR"))+'"') if filter_language else ""
 flag=('<span class="portrait-language" aria-label="Idioma: '+E(v["language_label"])+'">'+E(v["language_flag"])+'</span>') if filter_language and v.get("language_flag") else ""
 work_link=works_link(v)
 badge=top_badge(v)
 message=voice_message(v)
 if context: message=f'Olá! Conheci a voz {v["name"]} no site da A Locução e gostaria de um orçamento de {context}.'
 return f'''<article class="voice-card" data-search="{E(voice_search(v))}" data-gender="{E(v['gender'])}"{language_attr} data-tags="{E('|'.join(v['tags']))}"><a class="portrait" style="display:block" href="/locutores/{v['slug']}/" aria-label="Ver perfil de {E(v['name'])}">{portrait(v)}{flag}</a><div class="voice-body"><h{heading}><a href="/locutores/{v['slug']}/">{display_name(v)}</a></h{heading}>{badge}<p class="voice-style">{E(v['style'])}</p>{rating(v["slug"])}{delivered_indicator(v)}{language_badge(v)}{('<p class="voice-summary">'+E(v['short_description'])+'</p>') if v.get('short_description') else ''}<div class="voice-tags">{''.join('<span class="tag">'+E(t)+'</span>' for t in v['tags'])}</div>{audio(v,primary)}{audio(v,secondary)}{work_link}<div class="voice-actions">{cta('Contratar esta voz',message,voice=v['name'])}<a class="profile-link" href="/locutores/{v['slug']}/">Ver perfil completo</a></div></div></article>'''
CATALOG_INIT = """<script>(()=>{const grid=document.currentScript.previousElementSibling;const cards=Array.from(grid.children);for(let i=cards.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[cards[i],cards[j]]=[cards[j],cards[i]];}cards.forEach(card=>grid.appendChild(card));const filters=grid.parentElement.querySelector('.filters');if(filters)filters.hidden=false;})();</script>"""
def catalog(subset=None,filters=False,primary="off",context=""):
 selected=subset or voices
 f=''
 if filters:
  opts=sorted({t for v in voices for t in v['tags']})
  available={v.get('language_code','pt-BR') for v in selected}
  languages=[('pt-BR','Português brasileiro'),('en-US','🇺🇸 Inglês americano'),('es-419','Espanhol latino-americano'),('fr-FR','Francês'),('it-IT','Italiano'),('de-DE','Alemão')]
  language_options='<option value="">Todos os idiomas</option>'+''.join('<option value="'+code+'"'+(' disabled' if code not in available else '')+'>'+E(label+(' (em breve)' if code not in available else ''))+'</option>' for code,label in languages)
  f='<form class="filters" hidden aria-label="Filtrar vozes"><label>Buscar por nome ou aplicação<input type="search" placeholder="Qual voz você procura?" autocomplete="off"></label><label>Perfil<select id="gender"><option value="">Todos os perfis</option><option>Masculina</option><option>Feminina</option><option>Personagem</option></select></label><label>Estilo<select id="style"><option value="">Todos os estilos</option>'+''.join('<option>'+E(t)+'</option>' for t in opts)+'</select></label><label class="language-filter">Idioma<select id="language">'+language_options+'</select></label><button type="button">Limpar filtros</button></form><p id="voice-count" class="status" role="status" aria-live="polite">'+str(len(voices))+' vozes no catálogo</p>'
 return f+f'<div class="voice-grid">{"".join(voicecard(v,primary,context,2 if filters else 3,filters) for v in selected)}</div>{CATALOG_INIT}<p id="empty-voices" hidden>Nenhuma voz encontrada. Tente outro nome ou limpe os filtros.</p>'
def acquisition_hero(slug):
 production=slug=='spot-comercial'
 label='Produção Completa' if production else 'Locução Off'
 value='25,00' if production else '12,00'
 title='Spot comercial.<br>Sua mensagem pronta.' if production else 'Locução Off.<br>A voz para sua edição.'
 desc='Locução, trilha licenciada para a mídia aprovada, edição, mixagem e finalização. Seu anúncio com o cuidado de uma produtora de áudio.' if production else 'A voz escolhida para o seu roteiro, sem trilha ou efeitos. Para agências, produtoras e empresas que precisam seguir com a edição.'
 v=next(v for v in voices if v['slug']==('will' if production else 'audrey'))
 primary='producao' if production else 'off';secondary='off' if production else 'producao'
 message='Olá! Quero um orçamento para Produção Completa.' if production else 'Olá! Gostaria de contratar uma Locução Off.'
 return f'''<section class="acquisition-hero"><div class="wrap acquisition-grid"><div><span class="eyebrow">{label} · A Locução</span><h1>{title}</h1><p class="lead">{desc}</p><p class="hero-price"><strong>R$ {value}</strong><span>por peça comercial de até 40 segundos</span></p><div class="actions">{cta('Pedir '+label+' pelo WhatsApp',message)}<a class="mini-link" href="#demonstracoes">Ouvir mais exemplos ↓</a></div><p class="hero-assurance">Atendimento direto com a equipe · Orçamento aprovado antes de produzir</p><p class="note">Projetos especiais e narrativos: sob orçamento.</p></div><aside class="hero-demo" aria-label="Demonstrações de {v['name']}"><span class="eyebrow">Ouça o resultado</span><div class="demo-identity"><img src="{v['image']}" width="72" height="72" alt="Retrato ilustrativo da voz {E(v['name'])}"><div><h2>{v['name']}</h2><p>{E(v['style'])}</p></div></div>{audio(v,primary,'hero')}{audio(v,secondary,'hero')}<a class="mini-link" href="/locutores/{v['slug']}/">Conhecer esta voz →</a><p class="note">Compare os formatos e escolha a interpretação para seu projeto.</p></aside></div></section>'''
def prices():
 return f'''<section class="section dark" id="precos"><div class="wrap"><div class="section-head"><div><span class="eyebrow">O formato certo para seu projeto</span><h2>Da voz à produção.<br>Você escolhe.</h2></div><p>Valores para peças comerciais de até 40 segundos. Sem contratação mínima de várias peças.</p></div><div class="price-grid"><article class="price-card"><h3>Locução Off</h3><div class="price"><small>R$</small> 12<span aria-hidden="true">,00</span></div><p class="price-sub">por peça de até 40 segundos</p><p>A voz para entrar na sua edição.</p><ul><li>Gravação da voz escolhida</li><li>Sem trilha musical ou efeitos</li><li>Orientações de interpretação no briefing</li></ul>{cta('Quero uma Locução Off','Olá! Gostaria de contratar uma Locução Off.',css='light')}</article><article class="price-card"><h3>Produção Completa</h3><div class="price"><small>R$</small> 25<span aria-hidden="true">,00</span></div><p class="price-sub">por peça de até 40 segundos</p><p>Seu anúncio com acabamento para divulgação.</p><ul><li>Locução, edição, mixagem e finalização</li><li>Trilha licenciada para o uso aprovado</li><li>Efeitos quando adequados ao roteiro</li></ul>{cta('Quero Produção Completa','Olá! Quero um orçamento para Produção Completa.',css='light')}</article></div><p class="note">Projetos narrativos, trabalhos longos e produções especiais: sob orçamento. Mídia, prazo, direitos de uso e condições finais são confirmados antes do pagamento.</p></div></section>'''
def steps():
 return '<section class="section"><div class="wrap"><span class="eyebrow">Uma boa produção começa com uma boa conversa</span><h2>Do seu roteiro<br>ao áudio final.</h2><div class="steps">'+''.join(f'<article><span class="step-num">0{i+1}</span><h3>{t}</h3><p>{d}</p></article>' for i,(t,d) in enumerate([('Escolha a voz','Ouça as demonstrações e encontre o timbre e o estilo que combinam com sua mensagem.'),('Conte sua ideia','Envie o texto e as orientações pelo WhatsApp. Confirme o formato, o valor, o uso e o prazo.'),('Receba sua produção','Após a aprovação e o pagamento combinado, produzimos seu áudio conforme o briefing.')] ))+'</div></div></section>'
def faq(items=None):
 items=items or [('Qual é a diferença entre Off e Produção Completa?','Na Locução Off, você recebe a gravação da voz, sem trilha e efeitos. A Produção Completa inclui locução, trilha licenciada para o uso aprovado, efeitos quando adequados, edição, mixagem e finalização.'),('Qual é o prazo de entrega?','Confirmamos o prazo no orçamento, conforme o texto, a voz, a disponibilidade e a complexidade. Não há promessa de entrega instantânea.'),('Como contratar?','Escolha a voz e fale pelo WhatsApp. Envie o texto, o tipo de projeto, a duração aproximada e onde pretende utilizar o áudio. A equipe confirma o orçamento antes do pagamento.'),('É possível pedir correções?','Falhas de execução são corrigidas gratuitamente. Há uma rodada de interpretação de cortesia dentro do estilo contratado nos serviços elegíveis, informados no orçamento. Alterações de roteiro ou de escopo passam por avaliação. Consulte os Termos de Uso.'),('Quais são os horários de atendimento?',HOURS+' Os horários de produção e o prazo de entrega são combinados por pedido.')]
 return '<section class="section"><div class="wrap"><span class="eyebrow">Antes de dar o play</span><h2>Perguntas frequentes.</h2><div class="faq">'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in items)+'</div></div></section>'
services=[('Locução e Produção Comercial','Voz, trilha e acabamento para anúncios e campanhas. Off R$ 12 e Produção Completa R$ 25 por até 40 segundos.','/servicos/#comercial'),('Narrações Profissionais','Vídeos a partir de R$ 25 por até 1 minuto. Narração longa a partir de R$ 75 por até 5 minutos.','/servicos/#narracao'),('Soluções Empresariais','URA: R$ 20 por mensagem de até 30 segundos ou 5 por R$ 75. Tratamento de áudio a partir de R$ 25 por arquivo de até 5 minutos.','/servicos/#empresarial'),('Produções Especializadas','Audiobooks, podcasts e avaliação de dublagem para conteúdos autorizados. Escopo e licença conferidos por projeto.','/servicos/#especializadas')]
def calculator(selected="off"):
 component = '<section class="section" id="calculadora"><div class="wrap"><span class="eyebrow">Planeje sua peça comercial</span><h2>Uma estimativa para começar.</h2><div class="calculator"><label for="calc-service">Qual serviço você precisa?</label><select id="calc-service"><option value="off">Locução Off</option><option value="producao">Produção Completa</option></select><label for="calc-text">Digite ou cole o roteiro</label><textarea id="calc-text" placeholder="Seu texto fica no navegador durante a estimativa."></textarea><div id="calc-result" class="calc-result" role="status" aria-live="polite">Digite um texto para estimar duração e valor.</div><a class="btn" id="calc-whatsapp" href="'+wa('Olá! Preciso de ajuda para orçar uma peça comercial.')+'" data-cta="calculadora_orcamento">Solicitar pelo WhatsApp</a><p class="note calc-disclaimer">Valor sujeito à confirmação após análise do roteiro.</p></div></div></section>'
 return component.replace('value="'+selected+'"', 'value="'+selected+'" selected', 1)

def service_list():
 return '<div class="service-list">'+''.join(f'<article class="service-row"><span class="number">0{i+1}</span><h3>{t}</h3><p>{d}</p><a href="{url}" aria-label="Conhecer {t}">↗</a></article>' for i,(t,d,url) in enumerate(services))+'</div>'
# Retained editorial pages are normalized in one audited migration, then remain source data.
for p in json.loads((ROOT/'data/site-pages.json').read_text()):
 write(p['path'],p['title'],p['description'],p['body'],p.get('index',True),canonical=p.get('canonical'))
home='''<section class="home-hero"><div class="wrap"><div class="hero-top"><div><span class="eyebrow">Produtora de locução e áudio</span><h1>Uma boa mensagem<br>começa com a<br><em>voz certa.</em></h1><p class="lead">Locução, narração e soluções em áudio para empresas, agências, produtores de conteúdo e instituições.</p><div class="actions"><a class="btn" href="/vozes/">Encontre sua voz ↗</a>'''+cta('Falar com a equipe',css='secondary')+'''</div></div><div class="side"></div></div><div class="hero-image"><img src="/assets/images/estudio-locucao-960.webp" srcset="/assets/images/estudio-locucao-480.webp 480w,/assets/images/estudio-locucao-960.webp 960w" sizes="(max-width:760px) 100vw,1280px" width="960" height="540" fetchpriority="high" alt="Microfone e equipamentos em estúdio de áudio"><span class="image-caption">A LOCUÇÃO · A voz certa para sua mensagem.</span></div><div class="strip"><span>PUBLICIDADE & CAMPANHAS</span><span>CONTEÚDO & NARRATIVAS</span><span>COMUNICAÇÃO & MARCAS</span></div></div></section><section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Mais intenção em cada palavra</span><h2>Áudio que faz parte<br>da sua comunicação.</h2></div><p>Para agências, produtoras e empresas que precisam transformar um roteiro em uma mensagem com identidade.</p></div>'''+service_list()+'''</div></section><section class="section" id="vozes"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Ouça. Compare. Encontre.</span><h2>Personalidades diferentes.<br>A sua próxima voz.</h2></div><a class="mini-link" href="/vozes/">Explorar o Banco de Vozes ↗</a></div>'''+catalog([next(v for v in voices if v['slug']==s) for s in ['amanda-kelly','will','david']])+'''</div></section>'''+prices()+calculator()+steps()+faq()
write('','Locução, Narração e Soluções em Áudio | A Locução','Locução, narração, URA e produção de áudio para empresas e criadores. Conheça as vozes, confira escopos e fale com a equipe pelo WhatsApp.',home)
write('vozes','Banco de Vozes: ouça e escolha sua voz | A Locução','Explore perfis vocais, ouça demonstrações Off e de Produção Completa e contrate pelo WhatsApp da A Locução.',hero('Banco de Vozes','Uma voz para cada <br>intenção.','Timbres, ritmos e estilos para a sua mensagem. Compare as demonstrações disponíveis e conheça cada perfil.',False)+'<section class="section" style="padding-top:0"><div class="wrap">'+catalog(filters=True)+'</div></section>')
write('locutores','Perfis de Vozes da A Locução','Conheça os perfis individuais de voz, suas características, aplicações e contatos profissionais na A Locução.',hero('Perfis de voz','Conheça cada<br>identidade vocal.','Uma escolha cuidadosa considera timbre, interpretação e aplicação. Explore os perfis para conhecer características e ouvir as demonstrações disponíveis.',False)+'<section class="section"><div class="wrap"><p>Os perfis do catálogo atual são identidades vocais sintéticas, com retratos ilustrativos. A contratação é feita diretamente com a equipe da A Locução pelo WhatsApp.</p><div class="link-grid">'+''.join('<a href="/locutores/'+v['slug']+'/">'+E(v['name'])+'<br><small>'+E(v['style'])+'</small> ↗</a>' for v in voices)+'</div><div class="actions"><a class="btn" href="/vozes/">Comparar vozes no catálogo</a></div></div></section>')
for v in voices:
 works_body,works_schema=recent_works(v)
 demos=audio(v,'off')+audio(v,'producao')
 if not demos:demos='<p class="note">Solicite uma demonstração desta voz pelo WhatsApp.</p>'
 body=f'''<section class="hero"><div class="wrap"><nav class="breadcrumb" aria-label="Caminho"><a href="/">Início</a> / <a href="/vozes/">Banco de Vozes</a> / {E(v['name'])}</nav><div class="profile-hero"><div class="portrait">{portrait(v)}</div><div class="profile-copy"><span class="eyebrow">Identidade vocal · {E(v['gender'])}</span><h1>{display_name(v)}</h1>{top_badge(v)}{rating(v["slug"])}{delivered_indicator(v)}<p class="style">{E(v['style'])}</p>{language_badge(v)}<p>{E(v['about'])}</p><h2>Minha voz e meu estilo</h2><p>{E(v['description'])}</p><h2 id="demonstracoes">Ouça as demonstrações</h2>{demos}{works_link(v)}<p class="note">Voz sintética, produzida com tecnologia de inteligência artificial. O retrato é ilustrativo. <a href="/termos/#tecnologia">Entenda o serviço</a>.</p><div class="actions">{cta('Contratar esta voz',voice_message(v),voice=v['name'])}</div><p class="mini-link">Contato secundário: <a href="mailto:{v['email']}">{v['email']}</a></p><h2>Aplicações recomendadas</h2><ul class="application-list">{''.join('<li>'+E(a)+'</li>' for a in v['applications'])}</ul><p class="note">Sugestões baseadas no perfil vocal. A adequação da interpretação ao roteiro é avaliada com a equipe.</p><a class="mini-link" href="/vozes/">Conhecer outras vozes →</a></div></div></div></section>'''+works_body+reviews_section(v)+faq(v['faq'])
 desc=v['meta_description']
 if not(v['off'] and v['producao']): desc=f'Conheça a voz {v["name"]}: {v["style"].lower()}. Veja o perfil e consulte as demonstrações e as condições pelo WhatsApp da A Locução.'
 audio_schema=[{'@type':'AudioObject','name':v['name']+' — '+('Locução Off' if k=='off' else 'Produção Completa — amostra temporária de Locução Off' if v.get('temporary_demo',{}).get(k) else 'Produção Completa'),'contentUrl':BASE+v[k],'encodingFormat':'audio/mpeg',**({'inLanguage':v['language_code']} if v.get('language_code') else {})} for k in ['off','producao'] if v[k]]
 write('locutores/'+v['slug'],v['seo_title'],desc,body,extra=audio_schema+works_schema)
write('servicos','Serviços de Locução e Produção de Áudio | A Locução','Locução comercial, produção de spots, narração institucional e URA. Escolha o serviço e peça orçamento pelo WhatsApp.',hero('Soluções em áudio','Sua ideia.<br>Nossa produção.','Locução comercial é o nosso ponto de partida. Voz e produção também dão vida a vídeos, conteúdos e comunicação institucional.')+'<section class="section"><div class="wrap">'+service_list()+'<div class="link-grid"><a href="/producao-para-igrejas/">Produção para igrejas ↗</a><a href="/producao-para-supermercados/">Supermercados e varejo ↗</a><a href="/spot-black-friday/">Black Friday ↗</a><a href="/vinhetas-para-podcast-e-radio/">Vinhetas e chamadas ↗</a><a href="/spot-para-carro-de-som/">Carro de som ↗</a><a href="/locucao-ia/">Tecnologia de voz ↗</a></div></div></section>'+steps())
landings={
'locucao-off':('Locução Off','A voz certa.<br>Pronta para sua edição.','Gravação de voz sem trilha ou efeitos para agências, produtoras e empresas que já têm uma equipe de edição.','Seu roteiro ganha intenção','Envie o texto, indique pronúncias, referências e o estilo desejado. A gravação é preparada conforme as orientações aprovadas.','Para diferentes formatos','Comerciais, vídeos, apresentações e conteúdos que precisam da voz separada para a montagem. Narrativas longas e projetos especiais têm orçamento próprio.'),
'off-comercial':('Off Comercial','Sua campanha<br>começa pela voz.','Interpretação para comunicar a oferta, apresentar uma marca e dar ritmo ao seu anúncio, sem trilha musical.','Direção no briefing','Informe o público, o ritmo, a duração e a intenção do anúncio. Escolha a voz ouvindo as demonstrações.','Pronto para sua produtora','O Off entrega somente a voz para a edição do seu comercial. Para receber uma peça finalizada, escolha Produção Completa.'),
'spot-comercial':('Spot Comercial','Sua mensagem.<br>Uma produção completa.','Locução, trilha licenciada para a mídia aprovada, efeitos quando adequados, edição, mixagem e finalização.','Um anúncio com identidade','A produção organiza voz, música, ritmo e pausas para comunicar com clareza. Envie a proposta da campanha e suas referências.','Conte onde vai divulgar','Rádio, vídeo, redes sociais e outras mídias têm condições de uso específicas. Confirmamos as licenças necessárias antes de produzir.'),
'gravacao-off-e-producao':('Gravação e produção de áudio','Da interpretação<br>ao último detalhe.','Contrate somente a voz ou a produção comercial completa. Receba orientação da equipe pelo WhatsApp.','Off ou produção?','Se você vai editar, escolha Off. Se precisa do anúncio finalizado com voz, música e acabamento, escolha Produção Completa.','Briefing bem resolvido','Confirme roteiro, duração, mídia, pronúncias e referências antes da gravação. Isso ajuda a chegar ao resultado esperado.'),
'producao-para-igrejas':('Comunicação para igrejas','Uma voz para<br>aproximar pessoas.','Locução e produção de áudio para convites, encontros, celebrações e comunicação da sua comunidade.','Convites com propósito','Informe data, horário, local, tema e forma de participação. A mensagem deve orientar com clareza e preservar o tom da sua comunidade.','Cuidado com a trilha','O uso de uma música em culto ou evento não significa que ela esteja autorizada para um anúncio. A produção utiliza material compatível com a finalidade aprovada.'),
'producao-para-supermercados':('Supermercados e varejo','Sua oferta merece<br>ser bem ouvida.','Spots promocionais para comunicar produtos, preços e condições com energia e clareza.','Oferta sem informação faltando','Envie produtos, unidades, preços, validade e condições da promoção. A duração do anúncio precisa acomodar a informação com boa compreensão.','A voz no ritmo da sua marca','Compare estilos de varejo, vozes energéticas e interpretações mais próximas. Ajustamos a proposta de produção ao briefing.'),
'spot-black-friday':('Campanhas de Black Friday','Impacto para anunciar.<br>Clareza para vender.','Produção de spots para divulgar ofertas de Black Friday com voz, trilha e acabamento.','Prepare a campanha','Envie a oferta real, validade, restrições e chamada para ação. Informações objetivas ajudam a aproveitar os segundos do anúncio.','Energia com equilíbrio','Interpretação e produção valorizam a campanha sem prejudicar a leitura das condições da oferta. O prazo é confirmado conforme a demanda.'),
'locucao-ia':('Tecnologia aplicada à voz','Mais possibilidades<br>para a sua mensagem.','Perfis vocais sintéticos para locução e produção de áudio, com escolha de timbre e orientação da A Locução.','Escolha pela demonstração','Cada perfil tem uma identidade sonora. Ouça o timbre e o ritmo e converse com a equipe sobre a adequação ao seu roteiro.','Tecnologia com transparência','Estas vozes são geradas por inteligência artificial. Não representam uma pessoa gravando ao vivo. Os retratos dos perfis são ilustrativos.'),
'locucao-para-video-institucional':('Vídeos institucionais','A voz que apresenta<br>a sua marca.','Narração para vídeos corporativos, apresentações, treinamentos e conteúdos institucionais.','Uma narrativa coerente','Compartilhe o roteiro, a duração do vídeo e referências de tom. A voz pode orientar, acolher ou dar presença à história da empresa.','Roteiro e duração','A sincronização com imagens e as necessidades de edição fazem parte da avaliação. Projetos longos e direção especial são orçados individualmente.'),
'espera-telefonica-ura':('URA e telefonia','A primeira impressão<br>também tem voz.','Locução para saudações, menus de atendimento e mensagens telefônicas da sua empresa.','Informação fácil de seguir','Organize os setores, opções e instruções na ordem em que o usuário precisa ouvir. Envie também a pronúncia de nomes e siglas.','Entrega para seu sistema','Informe os requisitos de arquivo da central telefônica para confirmar a compatibilidade. Frases, versões e projetos de vários ramais são avaliados no orçamento.')}
for slug,(name,title,desc,t1,p1,t2,p2) in landings.items():
 primary='producao' if slug in ['spot-comercial','producao-para-supermercados','producao-para-igrejas','spot-black-friday'] else 'off'
 special={'espera-telefonica-ura':'gravacao-de-ura','locucao-para-video-institucional':'narracao-para-videos'}.get(slug)
 opening=acquisition_hero(slug) if slug in ['spot-comercial','locucao-off'] else hero(name,title,desc,not special)
 demo_markup,demo_schemas=service_demo(special)
 opening+=demo_markup
 body=opening+'<section class="section"><div class="wrap content-grid">'+f'<article class="content-card"><h2>{t1}</h2><p>{p1}</p></article><article class="content-card"><h2>{t2}</h2><p>{p2}</p></article></div></section>'
 if special:
  spec=next(row for row in json.loads((ROOT/'data/premium-services.json').read_text()) if row['slug']==special)
  body+='<section class="section"><div class="wrap"><h2>Um orçamento para o seu projeto.</h2><p class="service-price">'+E(spec['price'])+'</p><p>'+E(spec['unit'])+'</p><p>'+E(spec['limits'])+'</p><p><a href="/'+special+'/">Confira o escopo e as condições deste serviço →</a></p>'+cta('Solicitar orçamento personalizado','Olá! Gostaria de um orçamento de '+spec['name'].lower()+'.')+'</div></section>'+steps()+faq(spec['faq'])
 else:
  body+='<section class="section" id="demonstracoes"><div class="wrap"><span class="eyebrow">Conheça os estilos</span><h2>Ouça antes de escolher.</h2>'+catalog([next(v for v in voices if v['slug']==s) for s in (['noel-natal','paulo-becker','mario'] if slug=='producao-para-igrejas' else ['will','audrey','amanda-kelly'])],primary=primary,context='Produção Completa' if primary=='producao' else 'Locução Off')+'</div></section>'+prices()+calculator(primary)+steps()+faq()
 write(slug,name+' Profissional | A Locução',re.sub('<[^>]+>','',desc),body,extra=demo_schemas)
write('precos','Preços: Off R$ 12 e Produção Completa R$ 25 | A Locução','Consulte valores de locução por até 40 segundos e condições para trabalhos especiais. Orçamento e contratação pelo WhatsApp.',hero('Valores claros','O investimento<br>na sua mensagem.','Escolha entre Locução Off e Produção Completa. A equipe confirma o total, as condições de uso e o prazo antes de produzir.',False)+prices()+'<section class="section"><div class="wrap editorial"><h2>Quando o texto passa de 40 segundos</h2><p>Para peças comerciais padronizadas, o valor é calculado em faixas de até 40 segundos.</p><table><caption>Referência para peças comerciais</caption><thead><tr><th>Duração</th><th>Locução Off</th><th>Produção Completa</th></tr></thead><tbody><tr><td>Até 40 segundos</td><td>R$ 12,00</td><td>R$ 25,00</td></tr><tr><td>Até 80 segundos</td><td>R$ 24,00</td><td>R$ 50,00</td></tr><tr><td>Até 120 segundos</td><td>R$ 36,00</td><td>R$ 75,00</td></tr></tbody></table><p>Narrativas, projetos longos e produções complexas têm orçamento específico. O tempo depende da interpretação e das pausas, não apenas da quantidade de palavras.</p><a href="/calculadora/">Estimar a duração do roteiro →</a></div></section>'+calculator()+faq())
write('contato','Contato e Atendimento | A Locução','Fale com a A Locução pelo WhatsApp (27) 99652-9832. Atendimento de segunda a sexta, 08h–18h, e sábado, 08h–12h, horário de Brasília.',hero('Vamos conversar','Conte sua ideia.<br>Vamos dar voz a ela.','Envie seu roteiro, a duração aproximada, o estilo desejado e a mídia de divulgação. Nossa equipe orienta a escolha da voz e confirma o orçamento.')+f'<section class="section"><div class="wrap content-grid"><article class="content-card"><h2>Atendimento</h2><p>{HOURS}</p><p>Os horários de atendimento não determinam o horário de produção. O prazo de cada trabalho é combinado no orçamento.</p><p>E-mail: <a href="mailto:suporte@alocucao.com.br">suporte@alocucao.com.br</a></p></article><article class="content-card"><h2>A Locução</h2><p>{ENTITY}</p><p>{ADDRESS}</p></article></div></section>')
write('sobre','Sobre a A Locução | Produtora de Locução e Áudio','Conheça a A Locução: produção de locução e áudio profissional para publicidade, conteúdo e comunicação.',hero('A Locução','A voz certa<br>para sua mensagem.','Somos uma produtora de locução e áudio para publicidade, conteúdo e comunicação. Atendemos agências, produtoras, empresas e anunciantes de forma online.')+'<section class="section"><div class="wrap content-grid"><article class="content-card"><h2>Da intenção ao áudio</h2><p>Um roteiro comunica melhor quando timbre, interpretação e produção trabalham juntos. Nossa proposta é ajudar você a escolher a voz e preparar o áudio conforme o objetivo do projeto.</p></article><article class="content-card"><h2>Clareza em cada etapa</h2><p>O orçamento, o prazo, as condições de uso e as orientações de interpretação são combinados pelo WhatsApp. Usamos tecnologias de produção de áudio que podem incluir inteligência artificial, com informações acessíveis sobre a natureza dos serviços.</p></article></div></section>'+steps())
write('calculadora','Calculadora de Locução Off e Produção Completa | A Locução','Estime duração e preço da sua peça comercial: Off R$ 12 e Produção Completa R$ 25 por até 40 segundos. Confirme o orçamento pelo WhatsApp.',hero('Planeje seu roteiro','Seu texto cabe no tempo do anúncio?','A duração real depende da interpretação, do ritmo e das pausas.',False)+calculator())
from premium_pages import render
render(globals())
write('administracao/avaliacoes','Gestão de avaliações | A Locução','Informações sobre avaliações de clientes.',hero('Avaliações de clientes','Publicação manual','As avaliações são recebidas pelo atendimento e publicadas pela equipe, com autorização do cliente.',False),index=False)
# Legal copy is plain-language draft; never present it as professional legal certification.
legal=json.loads((ROOT/'data/legal-pages.json').read_text())
for slug,p in legal.items(): write(slug,p['title']+' | A Locução',p['description'],hero('Informações e condições',p['title'],'Atualização: 26 de outubro de 2026.',False)+'<article class="wrap editorial">'+p['body']+'</article>')
# Same-document compatibility routes retain query strings and self-contained content; no false HTTP 301 claims.
aliases={'termos-de-uso':'termos','vozes-ia':'vozes','talentos':'vozes','locucao_off':'locucao-off','locucaooff':'locucao-off','spot_comercial':'spot-comercial','spotcomercial':'spot-comercial','spot_supermercado':'producao-para-supermercados','locucao_off.html':'locucao-off','spot_comercial.html':'spot-comercial'}
for alias,target in aliases.items():
 source=(ROOT/target/'index.html').read_text();url=BASE+'/'+target+'/'
 file=ROOT/(alias if alias.endswith('.html') else alias+'/index.html');file.parent.mkdir(parents=True,exist_ok=True)
 source=re.sub(r'(<meta name="robots" content=")[^"]+',r'\1noindex,follow',source)
 file.write_text(source)
 built.append({'path':str(file.relative_to(ROOT)),'url':BASE+'/'+alias+('' if alias.endswith('.html') else '/'),'index':False,'canonical':url})
# Keep shared templates coherent; do not include old injectors.
(ROOT/'templates/site-header.html').write_text(header)
(ROOT/'templates/site-footer.html').write_text(footer)
(ROOT/'sw.js').write_text("self.addEventListener('install',()=>self.skipWaiting());self.addEventListener('activate',event=>event.waitUntil(caches.keys().then(keys=>Promise.all(keys.map(key=>caches.delete(key)))).then(()=>self.registration.unregister()).then(()=>self.clients.claim())));\n")
built=list({row['path']:row for row in built}.values())
ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns);tree=ET.Element('{'+ns+'}urlset')
for row in sorted(built,key=lambda p:p['url']):
 if row['index'] and row['url']==row['canonical']:
  node=ET.SubElement(tree,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=row['url'];ET.SubElement(node,'{'+ns+'}lastmod').text=prior_sitemap.get(row['url']) or ('2026-10-27' if row['url'] in {BASE+'/vozes/',BASE+'/locutores/lucan-rook/'}|{BASE+'/locutores/'+r['voice']+'/' for r in customer_reviews} else '2026-10-26')
ET.ElementTree(tree).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(ROOT/'reports/reformulacao-2026-10-26/manifesto.json').write_text(json.dumps(built,ensure_ascii=False,indent=2))
print(f'Built {len(built)} page entries and {len(voices)} individual voice profiles.')

# Retain the approved pricing policy after any subsequent build.
from progressive_pricing import update as update_progressive_pricing
update_progressive_pricing(ROOT)

# Apply the hybrid view only to the canonical bank, preserving compatibility pages.
from voice_bank_view import enhance as enhance_bank, ASSETS as bank_assets
bank_file=ROOT/"vozes/index.html"
bank_file.write_text(enhance_bank(bank_file.read_text()).replace("</head>",bank_assets+"</head>"))
