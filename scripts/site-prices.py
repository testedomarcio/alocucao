#!/usr/bin/env python3
"""Official retail prices and panel-only package lookup, shared by all page generators."""
import re

PANEL = 'https://vozlocutor.com.br/painel/alocucao/'
CREDIT_RULE = 'Cada crédito vale até 40 segundos de áudio.'
PANEL_LOGIN = 'https://vozlocutor.com.br/painel/alocucao/'
PACKAGES = ('<!-- credit-packages:start --><div class="package-callout" id="pacotes"><div><h3>Economize comprando em pacote</h3><p>Preços especiais para compras em quantidade estão disponíveis no Painel de Gravação.</p></div><a class="panel-primary" href="'+PANEL_LOGIN+'" data-cta="pacotes_painel">Ver preços no Painel de Gravação</a></div><!-- credit-packages:end -->')

PRICE_CARDS = ('<div class="panel-grid panel-pricing-grid"><article class="panel-card"><span class="panel-plan-label">Avulso · Somente a voz</span><h3>Locução Off</h3><strong class="panel-value">R$ 11,90</strong><p class="panel-price-unit">por crédito avulso · até 40 segundos</p><p>'+CREDIT_RULE+'</p><ul class="panel-inclusions"><li>Locução com voz humana profissional</li><li>Gravação da voz sem trilha e efeitos</li><li>Escolha do locutor no banco de vozes</li></ul><a class="panel-primary" href="'+PANEL+'cadastro" data-cta="preco_off_painel">Criar Conta Gratuita</a></article>'
 '<article class="panel-card panel-card-featured"><span class="panel-plan-label panel-premium">Avulso · Produção completa</span><h3>Produção completa (Spot) + Locução Off</h3><strong class="panel-value">R$ 29,90</strong><p class="panel-price-unit">por crédito avulso · até 40 segundos</p><p>'+CREDIT_RULE+'</p><ul class="panel-inclusions"><li>Spot comercial com locução profissional</li><li>Trilha, efeitos, edição e finalização</li><li>Locução Off incluída: voz separada, sem trilha e efeitos</li><li>Escolha do locutor no banco de vozes</li></ul><a class="panel-primary" href="'+PANEL+'cadastro" data-cta="preco_spot_painel">Criar Conta Gratuita</a></article>'
 '<p class="panel-pricing-support">Dúvidas antes de começar? use o balão de atendimento no canto da tela. Para comprar em quantidade, consulte as condições no painel abaixo.</p></div>')

def normalize_prices(text):
    # Rewrite complete pricing components so repeated generation never changes
    # the R$ 14,90 Spot package into an Off retail price.
    pattern = r'<div class="panel-grid panel-pricing-grid">.*?<p class="panel-pricing-support">.*?</p></div>'
    text = re.sub(pattern, lambda _: PRICE_CARDS, text, flags=re.S)
    if '<!-- credit-packages:start -->' in text:
        text = re.sub(r'<!-- credit-packages:start -->.*?<!-- credit-packages:end -->', lambda _: PACKAGES, text, flags=re.S)
    elif 'panel-pricing-grid' in text:
        text = re.sub(r'(<p class="panel-pricing-support">.*?</p></div>)', lambda m: m[0]+PACKAGES, text, count=1, flags=re.S)
    text = re.sub(r'(Locução Off:\s*R\$\s*)14,90', r'\g<1>11,90', text)
    text = text.replace('blocks*1490/100', 'blocks*1190/100')
    return text


def normalize_public_prices(text):
    text = normalize_prices_component(text)
    # Whole phrases first: prices in titles, metadata, FAQs and commercial copy.
    for old,new in [('R$ 6,90 cada no pacote de 25 Offs','R$ 11,90 por crédito avulso'),('R$ 10,90 cada no pacote de 30 Spots','R$ 29,90 por crédito avulso')]:
        text = text.replace(old,new)
    text = text.replace('R$ 6,90 cada','R$ 11,90').replace('R$ 10,90 cada','R$ 29,90')
    text = text.replace('R$ 6,90','R$ 11,90').replace('R$ 10,90','R$ 29,90')
    text = re.sub(r'(?:Na compra de 25 Offs · pacote R\$ 172,50\. Avulso: R\$ 11,90\.|Na compra de 30 Spots · pacote R\$ 327,00\. Avulso: R\$ 29,90\.)', 'Valor avulso por crédito de até 40 segundos.', text)
    text = re.sub(r'(?:No pacote de 25 Offs · total R\$ 172,50\. Cada crédito vale até 40 segundos\. Avulso: R\$ 11,90\.|No pacote de 30 Spots · total R\$ 327,00\. Cada crédito vale até 40 segundos\. Avulso: R\$ 29,90\.)', 'Valor avulso por crédito de até 40 segundos.', text)
    text = re.sub(r'no pacote de (?:25 Offs \(R\$ 172,50\)|30 Spots \(R\$ 327,00\))\. Cada crédito vale até 40 segundos de áudio\. Avulso: R\$ (?:11,90|29,90)\.', 'Valor avulso por crédito de até 40 segundos.', text)
    text = text.replace('Pacote completo: R$ 172,50. Cada crédito vale até 40 segundos de áudio. Off avulso: R$ 11,90.', 'Locução Off avulsa por crédito de até 40 segundos de áudio.')
    text = text.replace(' (total R$ 327,00; avulso R$ 29,90 por crédito de até 40 segundos)', ' por crédito de até 40 segundos')
    text = re.sub(r'((?:a partir de|A partir de) )?(R\$ (?:11,90|29,90) por crédito avulso)', r'\2', text)
    return text

# Compatibility for all callers: use the full public policy.
normalize_prices_component = normalize_prices
normalize_prices = normalize_public_prices
