#!/usr/bin/env python3
"""Reviewed commercial changes; human profiles and completed work keep their labels."""
from pathlib import Path
import re, runpy, json, html
ROOT=Path(__file__).resolve().parent.parent
SHARED=runpy.run_path(str(ROOT/'scripts/unified-catalog.py'))
OFFER=runpy.run_path(str(ROOT/'scripts/dual-offer.py'))['render_offer']()
META={
 '':('Locução Profissional com Vozes Humanas e IA | A Locução','Produzimos locuções comerciais, spots e vinhetas com vozes humanas e inteligência artificial. Off humano R$ 11,90 ou IA R$ 8,50 por até 40 segundos.','A voz ideal para seu comercial: humana ou inteligência artificial.'),
 'locucao-off':('Locução Off com Vozes Humanas e IA | A Locução','Receba somente a voz para seus anúncios e vídeos. Off humano R$ 11,90 ou IA R$ 8,50 por até 40 segundos. Ouça e peça pelo WhatsApp.','Locução Off com vozes humanas e IA para seu projeto.'),
 'spot-comercial':('Spot Comercial com Produção Completa | A Locução','Produzimos spots comerciais com locução, trilha, efeitos e finalização profissional em até 2 horas. A partir de R$ 30,00.','Sua propaganda com a voz certa para vender mais.'),
 'producao-para-supermercados':('Locução para Supermercado com Vozes Humanas e IA | A Locução','Divulgue ofertas do supermercado com vozes humanas ou IA. Off IA R$ 8,50; Off humano R$ 11,90 por até 40 segundos. Conheça também a produção completa.','Locução para supermercado com vozes humanas e IA.'),
 'producao-para-igrejas':('Locução para Igrejas, Eventos e Congressos | A Locução','Produza convites para cultos, congressos e eventos com vozes humanas ou IA. Produção IA R$ 19,00 ou humana R$ 29,90 por até 40 segundos.','Locução para igrejas, eventos e congressos.'),
 'gravacao-off-e-producao':('Locução Humana e IA: Off, Produção e Pacotes Humanos | A Locução','Compare locutores humanos e vozes IA para seus anúncios. Off IA R$ 8,50 ou humano R$ 11,90 por até 40 segundos; consulte os pacotes humanos.','Já compra locução? Compare vozes humanas e IA na A Locução.'),
 'spot-black-friday':('Locução Black Friday com Vozes Humanas e IA | A Locução','Prepare sua Black Friday com locução humana ou IA. Ouça as vozes, compare os preços avulsos e confira as condições promocionais indicadas na página.','Anúncios de Black Friday com vozes humanas e IA.'),
 'servicos':('Serviços de Locução com Vozes Humanas e IA | A Locução','Locução Off, spots, vinhetas, URA e vídeos com vozes humanas ou IA. Compare as modalidades e confirme formato, preço e prazo pelo WhatsApp.','Serviços de locução e produção com vozes humanas e IA.'),
 'precos':('Preços de Locução Humana e IA: Off e Produzida | A Locução','Até 40 segundos: Off humano R$ 11,90 e IA R$ 8,50; Produzida humana R$ 29,90 e IA R$ 19,00. Consulte também os pacotes humanos.','Preços de locução: vozes humanas e inteligência artificial.'),
 'sobre':('Sobre a A Locução | Vozes Humanas e IA','Conheça a A Locução: locutores humanos e vozes IA, produção comercial e orientação para escolher o áudio do seu projeto, com atendimento online no Brasil.','A voz certa para seu projeto, humana ou IA.'),
 'espera-telefonica-ura':('Locução para URA e Espera Telefônica: Humana ou IA | A Locução','Escolha vozes humanas ou IA para saudações, menus e espera telefônica. Compare as demonstrações e confirme o formato e o orçamento da sua URA.','Locução para URA e espera telefônica com vozes humanas ou IA.'),
 'locucao-para-video-institucional':('Locução para Vídeo com Vozes Humanas e IA | A Locução','Narração para vídeos institucionais, tutoriais e anúncios com vozes humanas ou IA. Ouça as opções e confirme interpretação, sincronização e prazo.','Locução para vídeos com vozes humanas e IA.'),
 'vinhetas-para-podcast-e-radio':('Vinhetas para Rádio e Podcast: Voz Humana ou IA | A Locução','Conheça vozes humanas e IA para vinhetas de rádio, podcast e marcas. Escolha o perfil e confirme o formato da gravação e da produção com a equipe.','Vinhetas para rádio e podcast com a voz do seu projeto.'),
 'spot-para-carro-de-som':('Spot para Carro de Som com Voz Humana ou IA | A Locução','Anúncio para carro de som com voz, trilha e finalização. Até 40 segundos: Produzida IA R$ 19,00 ou humana R$ 29,90. Compare as vozes e peça.','Spot para carro de som com voz humana ou IA.'),
 'planos-para-agencias-revenda':('Locução para Agências: Vozes Humanas, IA e Pacotes | A Locução','Compare locuções humanas e IA para agências e revendedores. Pacotes humanos preservados; IA avulsa com Off de R$ 8,50 por até 40 segundos.','Vozes humanas e IA para agências e revendedores.'),
 'spot-comercial-natal':('Spot de Natal com Vozes Humanas e IA | A Locução','Campanhas de Natal com locutores humanos ou vozes IA, incluindo perfil temático de Papai Noel. Ouça demonstrações e confirme o formato e o prazo.','Sua campanha de Natal com voz humana ou IA.'),
 'locucao-urgente-entrega-rapida':('Locução Ágil com Voz Humana ou IA | A Locução','Escolha voz humana ou IA e consulte o prazo para seu áudio. A entrega depende do texto, da disponibilidade e da produção; confirme antes de pedir.','Precisa de locução com agilidade? Escolha sua voz e confirme o prazo.'),
}
COMMERCIAL=set(META)-{'sobre'}
FOOTER_OLD='Vozes humanas para mensagens que conectam. Locução off e produção de áudio com atendimento online em todo o Brasil.'
FOOTER_NEW='Vozes humanas e inteligência artificial para mensagens que conectam. Locução off e produção de áudio com atendimento online em todo o Brasil.'
def metadata(text,title,description,h1=None):
    text=re.sub(r'<title>.*?</title>',lambda _: '<title>'+html.escape(title)+'</title>',text,count=1,flags=re.S)
    text=re.sub(r'(<meta\b[^>]*(?:name="description"|property="og:description"|name="twitter:description")[^>]*content=")[^"]*(")',lambda m:m[1]+html.escape(description,quote=True)+m[2],text)
    text=re.sub(r'(<meta\b[^>]*(?:property="og:title"|name="twitter:title")[^>]*content=")[^"]*(")',lambda m:m[1]+html.escape(title,quote=True)+m[2],text)
    if h1:text=re.sub(r'<h1\b[^>]*>.*?</h1>',lambda _:'<h1>'+html.escape(h1)+'</h1>',text,count=1,flags=re.S)
    def schema(m):
        try:data=json.loads(m[1])
        except json.JSONDecodeError:return m[0]
        def visit(o):
            if isinstance(o,dict):
                if o.get('@type') in ('WebPage','CollectionPage','Service','Article','BlogPosting'):
                    if o.get('description'):o['description']=description
                    if o.get('@type') in ('WebPage','CollectionPage'):o['name']=title
                for v in o.values():visit(v)
            elif isinstance(o,list):
                for v in o:visit(v)
        visit(data)
        return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,text,flags=re.S)
def update(text,path):
    route=path.parent.relative_to(ROOT).as_posix();route='' if route=='.' else route
    if 'data-commercial-refresh=' in text: return text
    if route in {'off-comercial','locucao-off','producao-para-igrejas','gravacao-off-e-producao','producao-para-supermercados','spot-black-friday','locucao-ia','spot-comercial'}:
        return text
    text=text.replace('<a href="/vozes/#banco-de-vozes">Ouvir vozes humanas e IA</a>', '<a href="/vozes/#banco-de-vozes">Ouvir vozes humanas</a> · <a href="/vozes-ia/#banco-de-vozes">Ouvir vozes IA</a>')
    # Shared identity is updated on all pages, including human-only profiles.
    text=text.replace(FOOTER_OLD,FOOTER_NEW)
    text=text.replace('Produção de anúncios em áudio com vozes humanas, trilha, efeitos e finalização para empresas em todo o Brasil.','Produção de anúncios em áudio com vozes humanas ou IA, trilha, efeitos e finalização para empresas em todo o Brasil.')
    if '<footer' in text and 'data-ia-disclosure' not in text:
        text=text.replace('</footer>','<p data-ia-disclosure style="font-size:12px;line-height:1.7;max-width:1180px;margin:20px auto;padding:0 24px">Os retratos de vozes IA são ilustrativos e representam perfis sintéticos. Os áudios IA utilizam tecnologia de síntese de voz.</p></footer>')
    text=text.replace('<a href="/vozes/">Banco de Vozes</a><a href="/portfolio/">','<a href="/vozes/">Banco de Vozes</a><a href="/locutores/">Locutores humanos</a><a href="/vozes-ia/">Vozes IA</a><a href="/portfolio/">')
    def footer_links(m):
        footer=m[0]
        if 'href="/locutores/"' not in footer:
            footer=footer.replace('<a href="/vozes/">Banco de Vozes</a>','<a href="/vozes/">Banco de Vozes</a><a href="/locutores/">Locutores humanos</a>')
        if 'href="/vozes-ia/"' not in footer:
            footer=footer.replace('<a href="/vozes/">Banco de Vozes</a>','<a href="/vozes/">Banco de Vozes</a><a href="/vozes-ia/">Vozes IA</a>')
        return footer
    text=re.sub(r'<footer\b.*?</footer>',footer_links,text,flags=re.S)
    if route in META:
        title,desc,h1=META[route];text=metadata(text,title,desc,h1)
        for before,after in {
          'Vozes humanas · escolha como pedir':'Vozes humanas e IA · escolha como pedir',
          'As duas soluções usam vozes humanas profissionais. A diferença está no que você recebe ao final do pedido.':'Nas duas soluções, escolha entre locutores humanos e vozes IA. Compare a modalidade e o formato de áudio que você recebe ao final do pedido.',
          '✓ Mais de 100 vozes humanas':'✓ Vozes humanas e IA',
          'Mais de 100 vozes':'Vozes humanas e IA',
          '✓ Vozes humanas profissionais':'✓ Vozes humanas e IA',
          '✓ Vozes humanas e conversacionais':'✓ Vozes humanas e IA para diferentes estilos',
          '✓ Voz humana profissional':'✓ Voz humana ou IA',
          'Locução humana profissional para vídeos, anúncios e apresentações. Receba somente a voz, sem trilha, efeitos ou edição final do projeto.':'Locução com voz humana ou IA para vídeos, anúncios e apresentações. No Off, você recebe somente a voz, sem trilha, efeitos ou edição final do projeto.',
          'Vozes Humanas para URA':'Vozes humanas e IA para URA',
          'Voz humana e tom alinhado à empresa':'Voz humana ou IA e tom alinhado à empresa',
          'A Locução conecta empresas, agências, rádios, produtores e criadores a vozes humanas profissionais e cuida do projeto desde a escolha da voz até a conferência do arquivo final.':'A Locução oferece locutores humanos profissionais e vozes geradas por inteligência artificial para empresas, agências, rádios, produtores e criadores. Nossa equipe orienta a escolha da modalidade e acompanha a preparação do áudio.',
          'Sim. Temos mais de 100 vozes humanas no catálogo. Ouça as demonstrações, selecione o locutor e confirme disponibilidade e prazo com nossa equipe.':'Sim. Compare as vozes humanas e IA do catálogo. Ouça as demonstrações e confirme a modalidade, a disponibilidade e o prazo com nossa equipe.',
        }.items():text=text.replace(before,after)
        # Existing package and human-price components retain their amounts and labels.
        text=text.replace('<h2>Escolha o áudio que você precisa</h2>','<h2>Preços e condições de locução humana</h2>')
        text=text.replace('Locução Off avulsa</h3>','Locução Off humana avulsa</h3>').replace('Produção Completa avulsa</h3>','Produção Completa humana avulsa</h3>')
        if route in ('locucao-off','spot-comercial','producao-para-igrejas','producao-para-supermercados'):
            text=text.replace('<div class="price">','<div class="price"><span class="human-offer-label">Condição para voz humana</span>',1) if 'human-offer-label' not in text else text
            if route in ('producao-para-igrejas','producao-para-supermercados'):
                text=text.replace('<div class="prices">','<div class="prices"><p>Valores de referência com voz humana; veja as opções IA abaixo.</p>',1)
    if route.startswith('produtora-de-audio-'):
        text=text.replace('Ouça vozes humanas e envie','Ouça vozes humanas e IA e envie')
        text=re.sub(r'banco de vozes humanas(?: e IA)*', 'banco de vozes humanas e IA', text)
    if route.startswith('blog/') and route!='blog/voz-ia-ou-locucao-humana':
        text=text.replace('✓ Vozes humanas profissionais','✓ Vozes humanas e IA').replace('✓ Mais de 100 vozes humanas','✓ Vozes humanas e IA').replace('✓ Vozes humanas','✓ Vozes humanas e IA')
        text=text.replace('✓ Vozes humanas e IA e IA','✓ Vozes humanas e IA')
        text=text.replace('A Locução trabalha com mais de 150 opções de vozes humanas e pode orientar a seleção.','A Locução oferece vozes humanas e IA e pode orientar a seleção conforme o seu projeto.')
        text=text.replace('a contratar vozes humanas e produção de áudio com mais clareza','a contratar vozes humanas ou IA e produção de áudio com mais clareza')
        text=text.replace('Compare interpretação, atendimento e preços. Ouça vozes humanas e conheça opções por R$ 11,90 por crédito avulso.','Compare interpretação, atendimento e preços de vozes humanas e IA. Off humano R$ 11,90 ou IA R$ 8,50 por até 40 segundos.')
    if route in COMMERCIAL or route.startswith('produtora-de-audio-'):
        if '<!-- dual-offer:start -->' not in text:
            # Before the first service section after the hero; never replace portfolios.
            m=re.search(r'</section>',text[text.find('<main'):])
            if m:
                at=text.find('<main')+m.end();text=text[:at]+OFFER+text[at:]
        if '/assets/catalog-pages.css' not in text:text=text.replace('</head>','<link rel="stylesheet" href="/assets/catalog-pages.css">\n</head>')
        if 'id="dual-prices-schema"' not in text:
            origin='https://alocucao.com.br/'+route+('/' if route else '')
            schema={'@context':'https://schema.org','@type':'OfferCatalog','name':'Locuções avulsas de até 40 segundos','url':origin,'itemListElement':[{'@type':'Offer','price':price,'priceCurrency':'BRL','itemOffered':{'@type':'Service','name':name}} for name,price in [('Off com voz humana — até 40 segundos','11.90'),('Off com voz IA — até 40 segundos','8.50'),('Produzida com voz humana — até 40 segundos','29.90'),('Produzida com voz IA — até 40 segundos','19.00')]]}
            text=text.replace('</head>','<script id="dual-prices-schema" type="application/ld+json">'+json.dumps(schema,ensure_ascii=False,separators=(',',':'))+'</script>\n</head>')
    if route in META or route.startswith('produtora-de-audio-') or '<!-- unified-catalog:start -->' in text:
        text=re.sub(r'<body\b(?![^>]*data-business-positioning)', '<body data-business-positioning="dual"',text,count=1)
    return text
def main():
    changed=[]
    for path in ROOT.rglob('*.html'):
        if any(p.startswith('.') for p in path.relative_to(ROOT).parts):continue
        text=path.read_text();new=update(text,path)
        if text!=new:
            new=re.sub(r'[ \t]+$', '', new, flags=re.M).rstrip()+'\n'
            path.write_text(new);changed.append(str(path.relative_to(ROOT)))
    print(f'Dual positioning updated: {len(changed)} pages/templates')
if __name__=='__main__':main()
