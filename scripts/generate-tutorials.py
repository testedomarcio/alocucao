#!/usr/bin/env python3
"""Generate crawlable tutorials from reviewed panel instructions and real screenshots."""
import html
import json
import re
import struct
from pathlib import Path
from runpy import run_path

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://alocucao.com.br'
DATE = '2026-10-03'
GUIDES = json.loads((ROOT / 'data/tutorials.json').read_text())
BY_SLUG = {g['slug']: g for g in GUIDES}
HEADER = (ROOT / 'templates/site-header.html').read_text().strip()
FOOTER = (ROOT / 'templates/site-footer.html').read_text().strip()
e = html.escape

def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value))

def url(g):
    return '/tutoriais/' + g['slug'] + '/'

def image(name, caption):
    path = ROOT / 'assets/tutorials' / name
    data = path.read_bytes()
    if data.startswith(b'\x89PNG'):
        width, height = struct.unpack('>II', data[16:24])
    else:
        # Read the JPEG frame dimensions without an imaging dependency.
        offset = 2
        while offset < len(data):
            if data[offset] != 0xff:
                raise ValueError(f'Invalid JPEG header: {path}')
            marker = data[offset+1]
            length = struct.unpack('>H', data[offset+2:offset+4])[0]
            if marker in (0xc0, 0xc1, 0xc2):
                height, width = struct.unpack('>HH', data[offset+5:offset+9])
                break
            offset += 2 + length
        else:
            raise ValueError(f'No dimensions in {path}')
    src = '/assets/tutorials/' + name
    return f'<figure class="t-figure"><a href="{src}" target="_blank" rel="noopener" aria-label="Ampliar captura do painel"><img src="{src}" width="{width}" height="{height}" loading="lazy" decoding="async" alt="{e(caption)}"></a><figcaption>{e(caption)}</figcaption></figure>'

def breadcrumbs(title=None, path=None):
    result = '<nav class="t-shell t-breadcrumb" aria-label="Caminho da página"><a href="/">Início</a><span aria-hidden="true">/</span>'
    result += '<a href="/tutoriais/">Tutoriais</a>' if title else '<span aria-current="page">Tutoriais</span>'
    if title:
        result += f'<span aria-hidden="true">/</span><span aria-current="page">{e(title)}</span>'
    return result + '</nav>'

def breadcrumb_schema(title=None, path=None):
    entries = [('Início', '/'), ('Tutoriais', '/tutoriais/')]
    if title:
        entries.append((title, path))
    return {'@type': 'BreadcrumbList', 'itemListElement': [dict({'@type': 'ListItem'}, position=i, name=name, item=BASE+p) for i, (name, p) in enumerate(entries, 1)]}

def document(title, description, path, body, schema, article=False):
    output = f'''<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | A Locução</title><meta name="description" content="{e(description)}">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{BASE+path}">
<meta name="theme-color" content="#0d1b2a"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:locale" content="pt_BR"><meta property="og:site_name" content="A Locução"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE+path}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}">
<link rel="stylesheet" href="/assets/tutorials.css?v=20261003"><link rel="stylesheet" href="/assets/site-layout.css?v=20261002">
<script src="/assets/privacy.js" defer></script><script src="/assets/tracking.js?v=20261003-panel-pages" defer></script>
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':schema},ensure_ascii=False,separators=(',',':'))}</script>
</head><body>{HEADER}<main id="conteudo">{body}</main>{FOOTER}<script src="/assets/site-layout.js?v=20261002" defer></script></body></html>'''

    return run_path(str(ROOT / "scripts/standardize-layout.py"))["standardize_page"](output)

def render_guide(g):
    title, path = g['title'], url(g)
    toc = ''.join(f'<li><a href="#passo-{i}">{e(s["title"])}</a></li>' for i, s in enumerate(g['steps'],1))
    steps = ''.join(f'<section class="t-step" id="passo-{i}"><span class="t-step-number">PASSO {i:02d}</span><h3>{e(s["title"])}</h3><p>{s["text"]}</p>{image(s["image"],s["caption"]) if s["image"] else ""}</section>' for i,s in enumerate(g['steps'],1))
    faqs = ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in g['faqs'])
    related = ''.join(f'<a href="{url(BY_SLUG[s])}">{e(BY_SLUG[s]["title"])}</a>' for s in g['related'])
    body = f'''{breadcrumbs(title,path)}<section class="t-hero"><div class="t-shell"><span class="t-label">Guia do Painel de Gravação</span><h1>{e(title)}</h1><p class="t-lead">{e(g['intro'])}</p><p class="t-meta">Atualizado em 03 de outubro de 2026 · Equipe A Locução</p></div></section>
<div class="t-shell t-layout"><article class="t-article"><div class="t-callout"><strong>Antes de começar</strong><p>{g['prereq']}</p></div><h2>Passo a passo</h2>{steps}{g['extra']}<section class="t-faq"><h2>Perguntas frequentes</h2>{faqs}</section><div class="t-next"><h2>Continue com estes tutoriais</h2>{related}<p><a href="/tutoriais/">Ver todos os tutoriais</a></p></div><p class="t-meta">Guia elaborado a partir das telas e dos termos do painel consultados em 03/10/2026. Os nomes e as condições podem mudar. Consulte Informações → Termos de Uso na área do cliente antes de confirmar pedidos ou pagamentos.</p></article>
<aside class="t-aside" aria-label="Navegação do tutorial"><div class="t-aside-box"><h2>Neste passo a passo</h2><ol>{toc}</ol></div><div class="t-aside-box"><h2>Pronto para começar?</h2><a class="t-button" href="/painel/">Entrar no painel</a><p><a href="/cadastro/">Criar conta grátis</a></p><p><a data-panel-support href="https://wa.me/5527996529832" target="_blank" rel="noopener">Suporte WhatsApp</a></p></div></aside></div>'''
    article = {'@type':'Article','headline':title,'description':g['description'],'datePublished':DATE,'dateModified':DATE,'inLanguage':'pt-BR','author':{'@type':'Organization','name':'A Locução','url':BASE+'/'},'publisher':{'@type':'Organization','name':'A Locução','url':BASE+'/'},'mainEntityOfPage':BASE+path}
    howto = {'@type':'HowTo','name':title,'description':g['description'],'inLanguage':'pt-BR','step':[{'@type':'HowToStep','position':i,'name':s['title'],'text':plain(s['text']),'url':BASE+path+f'#passo-{i}',**({'image':BASE+'/assets/tutorials/'+s['image']} if s['image'] else {})} for i,s in enumerate(g['steps'],1)]}
    faq = {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in g['faqs']]}
    folder = ROOT / path.strip('/')
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'index.html').write_text(document(title,g['description'],path,body,[breadcrumb_schema(title,path),article,howto,faq],True))

def render_hub():
    groups = []
    for group in ['Comece por aqui','Faça seu pedido','Depois do pedido']:
        cards = ''.join(f'<article class="t-card"><span class="t-label">{i:02d} · {e(group)}</span><h3><a href="{url(g)}">{e(g["title"])}</a></h3><p>{e(g["description"])}</p><a href="{url(g)}">Ver passo a passo →</a></article>' for i,g in enumerate(GUIDES,1) if g['group']==group)
        groups.append(f'<section><h2>{e(group)}</h2><div class="t-cards">{cards}</div></section>')
    title = 'Tutoriais do Painel de Gravação'
    description = 'Aprenda a se cadastrar, completar seus dados, comprar créditos, pedir Off ou Spot, solicitar correção e baixar áudios no Painel de Gravação.'
    body = f'''{breadcrumbs()}<section class="t-hero"><div class="t-shell"><span class="t-label">Central de ajuda · A Locução</span><h1>Aprenda a usar o Painel de Gravação</h1><p class="t-lead">Do primeiro cadastro ao download do áudio: encontre o passo a passo que você precisa para fazer seus pedidos de Locução Off e Spot Comercial.</p><a class="t-button" href="/painel/">Entrar no painel</a><a class="t-button t-button-alt" href="/cadastro/">Criar conta grátis</a></div></section><div class="t-shell t-hub"><div class="t-callout"><strong>Vai comprar créditos pela primeira vez?</strong><p><a href="/tutoriais/como-completar-cadastro/">Complete o cadastro em Minha conta</a> antes de iniciar. Essa etapa é necessária para adquirir créditos de forma automática.</p></div>{''.join(groups)}<section><h2>O caminho do seu primeiro pedido</h2><ol class="t-checklist"><li>Crie o acesso e complete os dados cadastrais.</li><li>Compre créditos de Off ou Produção no painel por PIX ou cartão de crédito, com processamento pelo Mercado Pago.</li><li>Após a confirmação do pagamento, receba os créditos automaticamente e de imediato.</li><li>Ouça as vozes, revise o roteiro e confirme o pedido.</li><li>Acompanhe em Meus Pedidos e baixe os arquivos entregues.</li></ol></section><section class="t-rules"><h2>Confira as condições do painel</h2><p>Antes de enviar, leia Informações → Termos de Uso na área do cliente. Revise o texto e o estilo escolhido; mudanças depois da entrega podem ser um novo pedido cobrado. Para erros de execução, os termos consultados preveem solicitação de correção em até três dias após a entrega, enquanto a função estiver disponível. Esse prazo operacional não limita os direitos legais; se a função estiver indisponível, procure o suporte. Baixe e guarde os arquivos: a disponibilidade mínima prevista é de 30 dias.</p></section><p>Precisa de ajuda com uma mensagem do painel? <a data-panel-support href="https://wa.me/5527996529832" target="_blank" rel="noopener">Fale com o suporte pelo WhatsApp</a>. Atendimento de segunda a sexta, das 08h às 18h.</p><p class="t-meta">Tutoriais e capturas baseados no painel consultado em 03/10/2026. Valores e condições devem ser conferidos na tela antes de confirmar.</p></div>'''
    schema = {'@type':'CollectionPage','name':title,'description':description,'url':BASE+'/tutoriais/','inLanguage':'pt-BR','mainEntity':{'@type':'ItemList','itemListElement':[{'@type':'ListItem','position':i,'name':g['title'],'url':BASE+url(g)} for i,g in enumerate(GUIDES,1)]}}
    folder = ROOT/'tutoriais'
    folder.mkdir(exist_ok=True)
    (folder/'index.html').write_text(document(title,description,'/tutoriais/',body,[breadcrumb_schema(),schema]))

if __name__ == '__main__':
    for guide in GUIDES:
        render_guide(guide)
    render_hub()
    print(f'Generated tutorial hub and {len(GUIDES)} guides')
