#!/usr/bin/env python3
"""Final commercial policy: retail prices, assisted packages and panel-first CTAs.

Run through integrate-recording-panel.py after the historical generators.
Package markup is removed before retail normalization and rebuilt from integers.
"""
import json
import re
from urllib.parse import quote

REGISTER = 'https://vozes.alocucao.com.br/painel/cadastro'
LOGIN = 'https://vozes.alocucao.com.br/painel/'
WA = 'https://wa.me/5527996529832'
OFF_ROUTES = {'locucao-off', 'off-comercial', 'locucao-ia', 'locucao-para-video-institucional', 'espera-telefonica-ura', 'locucao-voz-infantil', 'locucao-campanha-politica'}
GENERAL = {'', 'precos', 'servicos', 'gravacao-off-e-producao', 'planos-para-agencias-revenda', 'vozes', 'locutores'}
PLANS = [('off', 'Locução Off', 15, [(1, 15), (3, 12), (10, 10), (20, 6)]), ('producao', 'Produção Completa', 30, [(1, 30), (3, 25), (10, 20), (20, 15)])]

def money(n):
    return f'R$ {n},00'

def channels(prefix='commercial'):
    return f'<div class="rp-actions"><a class="rp-button rp-primary" href="{REGISTER}" data-cta="{prefix}_register">Criar conta grátis</a><a class="rp-button rp-secondary" href="{LOGIN}" data-cta="{prefix}_login">Acessar minha conta</a><a class="rp-button rp-secondary" href="{WA}" data-cta="{prefix}_whatsapp">Atendimento pelo WhatsApp</a></div>'

def packages(route):
    selected = PLANS if route in GENERAL or route.startswith('produtora-de-audio-') else [PLANS[0] if route in OFF_ROUTES else PLANS[1]]
    groups = []
    for key, name, retail, plans in selected:
        cards = []
        for qty, unit in plans:
            total = qty * unit
            saving = qty * retail - total
            label = '1 crédito avulso' if qty == 1 else f'{qty} créditos'
            badge = '<span class="cp-badge">Maior economia</span>' if qty == 20 else ''
            note = 'Valor avulso' if not saving else f'Economize {money(saving)} ({round(saving / (qty * retail) * 100)}%) em relação ao avulso.'
            href = REGISTER if qty == 1 else WA + '?text=' + quote(f'Olá! Quero contratar o pacote de {qty} créditos de {name}: {money(unit)} por crédito, total {money(total)}. Origem: /{route}/')
            cta = 'Criar conta grátis' if qty == 1 else 'Consultar contratação'
            cards.append(f'<article class="cp-card{" cp-best" if qty == 20 else ""}" data-package="{key}-{qty}">{badge}<h4>{label}</h4><p class="cp-unit"><strong>{money(unit)}</strong><span>por crédito de até 40 segundos</span></p><p class="cp-total">Total: <strong>{money(total)}</strong></p><p class="cp-saving">{note}</p><a class="rp-button {"rp-primary" if qty == 1 else "rp-secondary"}" href="{href}" data-cta="package_{key}_{qty}">{cta}</a></article>')
        groups.append(f'<div class="cp-group"><h3>{name}</h3><p>{"Somente a voz, sem trilha ou efeitos." if key == "off" else "Locução, trilha sonora, efeitos quando necessários, edição, mixagem e finalização."}</p><div class="cp-grid">'+''.join(cards)+'</div></div>')
    return '<!-- commercial-packages:start --><section class="cp-section" id="pacotes" data-credit-packages><div class="rp-shell"><span class="rp-eyebrow">AVULSOS E PACOTES DE CRÉDITOS</span><h2>Quanto mais você grava, mais economiza!</h2><p>Escolha o avulso ou economize em quantidade. Pacotes para produtores, agências, estúdios e empresas com demanda recorrente.</p>'+''.join(groups)+'<p class="cp-note">Cada crédito corresponde a até 40 segundos de áudio. Os valores reduzidos dependem da contratação do pacote completo. Para contratar pacotes, fale com nossa equipe pelo WhatsApp. Consulte as opções disponíveis no painel para pedidos avulsos.</p></div></section><!-- commercial-packages:end -->'

def retail(text):
    # These are the superseded retail rates in the current generated pages.
    # Never apply this function to the package component.
    text = re.sub(r'R\$\s*(10,00|12,00|11,90|25,00|29,90)(?!\d)', lambda m: 'R$ 15,00' if m[1] in {'10,00','12,00','11,90'} else 'R$ 30,00', text)
    for old, new in [('10','15'),('12','15'),('25','30')]:
        text = text.replace('R%24%20'+old+'%2C00', 'R%24%20'+new+'%2C00')
    text = text.replace('preço único', 'preço avulso').replace('Preço único', 'Preço avulso')
    return re.sub(r"\n(?:[ \t]*\n)+", "\n", text)

def update(text, route, commercial):
    if '<main' not in text or 'http-equiv="refresh"' in text:
        return re.sub(r"\n(?:[ \t]*\n)+", "\n", text)
    text = retail(text)
    # Keep schema price types scoped; the free calculator is not a paid service.
    def schema(match):
        obj = json.loads(match[2])
        def walk(o):
            if isinstance(o, dict):
                if o.get('@type') == 'WebApplication' and route == 'calculadora':
                    o['offers'] = {'@type':'Offer', 'price':'0', 'priceCurrency':'BRL'}
                elif o.get('@type') == 'Offer':
                    val = str(o.get('price',''))
                    if val in {'10','10.00','12','12.00','11.90'}: o['price'] = '15.00'
                    elif val in {'25','25.00','29.90'}: o['price'] = '30.00'
                for v in o.values(): walk(v)
            elif isinstance(o,list):
                for v in o: walk(v)
        walk(obj)
        return match[1]+json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+match[3]
    text = re.sub(r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',schema,text,flags=re.S)
    if route not in commercial:
        return re.sub(r"\n(?:[ \t]*\n)+", "\n", text)
    if '/assets/credit-packages.css' not in text:
        text = text.replace('</head>','<link rel="stylesheet" href="/assets/credit-packages.css?v=20261025">\n</head>',1)
    text = re.sub(r'<div class="rp-actions rp-hero-actions">.*?</div>', lambda _: '<div class="rp-actions rp-hero-actions">'+channels('hero').removeprefix('<div class="rp-actions">').removesuffix('</div>')+'</div>',text,flags=re.S)
    # Conversion controls go to registration; assistance controls retain WhatsApp.
    def action(m):
        tag, label = m[1], m[2]
        if 'wa.me/' not in tag:
            return m[0]
        if any(x in tag for x in ['single_offer_whatsapp','commercial_mobile','al-cta-primary','btn primary','button primary']):
            tag = re.sub(r'href="[^"]*"',f'href="{REGISTER}"',tag)
            tag = re.sub(r'data-cta="[^"]*"','data-cta="order_register"',tag)
            return tag+'Criar conta grátis</a>'
        if 'floating' in tag:
            tag = re.sub(r'aria-label="[^"]*"','aria-label="Atendimento pelo WhatsApp"',tag)
            return tag+'Atendimento</a>'
        return m[0]
    text = re.sub(r'(<a\b[^>]*>)(.*?)</a>',action,text,flags=re.S)
    text = text.replace('Ouça as demonstrações e peça pelo WhatsApp. Nossa equipe ajuda você a escolher a voz e o formato ideal.', 'Ouça as demonstrações e faça seu pedido pelo Painel de Gravação. Conte com nossa equipe pelo WhatsApp para dúvidas e orientação.')
    text = text.replace('Ouça sem cadastro. Peça uma proposta pelo WhatsApp.', 'Ouça sem cadastro. Crie sua conta grátis para fazer seu pedido.')
    text = text.replace('Escolha sua voz e confirme a disponibilidade para gravação rápida pelo WhatsApp.', 'Escolha sua voz, crie sua conta grátis e confira as opções disponíveis no Painel de Gravação.')
    text = text.replace('Solicite seu orçamento pelo WhatsApp, sem cadastro.', 'Cadastre-se gratuitamente para fazer seu pedido no painel. Para dúvidas e pacotes, fale pelo WhatsApp.')
    text = text.replace('Envie seu texto pelo WhatsApp e informe se precisa somente da voz ou do áudio completo. Assim conseguimos orientar o pedido corretamente.', 'Crie sua conta grátis e escolha entre receber somente a voz ou a produção completa. Para orientação e pedidos especiais, fale com nossa equipe pelo WhatsApp.')
    # Preços page did not originally have hero actions.
    if 'data-cta="hero_register"' not in text:
        text = re.sub(r'(<p class="sf-hero-price">.*?</p>)',lambda m:m[0]+channels('hero'),text,count=1,flags=re.S)
    if 'data-cta="hero_register"' not in text:
        text = re.sub(r'(<h1\b[^>]*>.*?</h1>)',lambda m:m[0]+channels('hero'),text,count=1,flags=re.S)
    # A final clear panel CTA supplements any existing specialist content.
    text = re.sub(r'<section class="cp-final".*?</section>','',text,flags=re.S)
    final = '<section class="cp-final"><div class="rp-shell"><h2>Sua próxima gravação começa aqui.</h2><p>Crie sua conta grátis para solicitar seu áudio. Para pacotes, dúvidas e pedidos especiais, conte com o atendimento pelo WhatsApp.</p>'+channels('final')+'</div></section>'
    text = text.replace('</main>',final+'</main>',1)
    section = packages(route)
    if '<section class="rp-panel"' in text:
        text = text.replace('<section class="rp-panel"',section+'\n<section class="rp-panel"',1)
    else:
        text = text.replace('</main>',section+'</main>',1)
    return re.sub(r"\n(?:[ \t]*\n)+", "\n", text)
