"""Generate service pages from one commercial catalog; legal pages stay independent."""
import json, html

def render(g):
    root, write, hero, cta, steps, faq = (g[k] for k in ('ROOT','write','hero','cta','steps','faq'))
    services=json.loads((root/'data/premium-services.json').read_text())
    esc=html.escape
    common='Falhas de execução são corrigidas sem custo, preservados os direitos legais. Uma rodada de interpretação está incluída quando indicada na proposta, dentro do roteiro e estilo aprovados. Mudanças de roteiro, voz ou escopo precisam de novo orçamento, aprovado antes de qualquer cobrança. Prazo e formato são confirmados antes do pagamento.'
    def cards(rows):
        return '<div class="content-grid">'+''.join('<article class="content-card"><span class="eyebrow">'+esc(s['category'])+'</span><h3><a href="/'+s['slug']+'/">'+esc(s['name'])+'</a></h3><p>'+esc(s['description'])+'</p><p class="service-price">'+esc(s['price'])+'</p><p>'+esc(s['unit'])+'</p><a class="mini-link" href="/'+s['slug']+'/">Ver escopo e solicitar orçamento →</a></article>' for s in rows)+'</div>'
    for s in services:
        message='Olá! Gostaria de solicitar um orçamento de '+s['name'].lower()+'.'
        opening=hero(s['category'],esc(s['name']),esc(s['description']),False).replace('</div></section>','<div class="actions">'+cta('Conversar sobre meu projeto',message)+'</div><p class="service-price">'+esc(s['price'])+'</p><p>'+esc(s['unit'])+'</p></div></section>')
        body=opening+'<section class="section service-scope"><div class="wrap content-grid"><article class="content-card"><h2>O que está incluído</h2><p>'+esc(s['included'])+'</p><h3>Limites do serviço</h3><p>'+esc(s['limits'])+'</p></article><article class="content-card"><h2>Onde aplicar</h2><ul>'+''.join('<li>'+esc(a)+'</li>' for a in s['applications'])+'</ul><h3>Para preparar seu orçamento</h3><p>'+esc(s['brief'])+'</p>'+cta('Enviar informações pelo WhatsApp',message)+'</article></div></section>'
        body+='<section class="section dark"><div class="wrap"><span class="eyebrow">Uma contratação bem definida</span><h2>Clareza antes de produzir.</h2><p>'+esc(common)+'</p><p>Vozes sintéticas são identificadas e sua adequação ao projeto é avaliada. A entrega do arquivo não transfere propriedade sobre uma voz nem direitos de terceiros. Mídia, prazo e licença de uso constam do orçamento.</p><a class="btn light" href="/vozes/">Conhecer os timbres do catálogo comercial</a><p class="note">As demonstrações do catálogo são comerciais. Amostras específicas desta modalidade serão apresentadas quando estiverem disponíveis; não representam testes já realizados para seu projeto.</p></div></section>'+steps()+faq(s['faq'])
        related=[x for x in services if x['category']==s['category'] and x['slug']!=s['slug']][:2]
        if not related: related=[x for x in services if x['slug'] in ['narracao-para-videos','producao-de-podcasts'] and x['slug']!=s['slug']]
        body+='<section class="section"><div class="wrap"><h2>Continue seu projeto</h2>'+cards(related)+'</div></section>'
        schema={'@type':'Service','@id':g['BASE']+'/'+s['slug']+'/#service','name':s['name'],'serviceType':s['name'],'description':s['description'],'provider':{'@id':g['BASE']+'/#organization'},'areaServed':{'@type':'Country','name':'Brasil'},'url':g['BASE']+'/'+s['slug']+'/'}
        write(s['slug'],s['name']+' Profissional | A Locução',s['description'],body,extra=[schema])
    commercial='<div class="content-grid"><article class="content-card"><h3><a href="/locucao-off/">Locução Off</a></h3><p>Somente a voz, sem trilha nem efeitos.</p><p class="service-price">R$ 12,00</p><p>Uma peça de até 40 segundos.</p></article><article class="content-card"><h3><a href="/spot-comercial/">Produção Completa</a></h3><p>Locução, edição, trilha licenciada para o uso aprovado e efeitos adequados.</p><p class="service-price">R$ 25,00</p><p>Uma peça de até 40 segundos.</p></article></div>'
    body=hero('Soluções profissionais em áudio','Uma voz. Muitas possibilidades.','Locução, narração e produção para empresas, agências, produtores de conteúdo e instituições. Escolha o serviço e conheça o escopo antes de contratar.')
    body+='<section class="section"><div class="wrap"><nav class="category-nav" aria-label="Categorias de serviços"><a href="#comercial">Comercial</a><a href="#narracao">Narrações</a><a href="#empresarial">Empresarial</a><a href="#especializadas">Especializadas</a></nav><h2 id="comercial">Locução e Produção Comercial</h2>'+commercial+'</div></section>'
    for key,category in [('narracao','Narrações Profissionais'),('empresarial','Comunicação e Soluções Empresariais'),('especializadas','Produções Especializadas')]:
        body+='<section class="section"><div class="wrap"><h2 id="'+key+'">'+esc(category)+'</h2>'+cards([s for s in services if s['category']==category])+'</div></section>'
    body+='<section class="section dark"><div class="wrap"><h2>Seu projeto tem outra necessidade?</h2><p>Envie o objetivo, o material e o prazo desejado. Projetos especiais recebem proposta própria. Pacotes empresariais recorrentes podem ser avaliados conforme a demanda.</p>'+cta('Conversar com a equipe',css='light')+'</div></section>'
    write('servicos','Serviços de Locução, Narração e Áudio | A Locução','Locução, narração para vídeos, URA, tratamento de áudio e produções especiais. Confira preços, escopos e solicite orçamento pelo WhatsApp.',body)
    # Add the catalog to the existing price page without creating another calculator model.
    path=root/'precos/index.html'
    content=path.read_text()
    extra='<section class="section"><div class="wrap"><h2>Outras soluções em áudio</h2>'+cards(services)+'</div></section>'
    path.write_text(content.replace('</main>',extra+'</main>'))
