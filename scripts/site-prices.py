#!/usr/bin/env python3
"""Current prices and explicit package conditions, shared by all page generators."""
import re

WHATSAPP = 'https://wa.me/5527996529832?text=Ol%C3%A1%21%20Quero%20informa%C3%A7%C3%B5es%20sobre%20os%20pacotes%20de%20cr%C3%A9ditos.'
CREDIT_RULE = 'Cada crédito vale até 40 segundos de áudio.'
PACKAGES = ('<!-- credit-packages:start --><details class="credit-packages" id="pacotes" open><summary>Preços avulsos e pacotes</summary><div class="credit-packages-grid">'
 '<div><h3>Locução Off</h3><table><thead><tr><th>Opção</th><th>Por crédito</th><th>Total</th></tr></thead><tbody>'
 '<tr><td>Avulso · 1 Off</td><td>R$ 11,90</td><td>R$ 11,90</td></tr><tr><td>5 Offs</td><td>R$ 9,90</td><td>R$ 49,50</td></tr><tr><td>25 Offs</td><td>R$ 6,90</td><td>R$ 172,50</td></tr></tbody></table></div>'
 '<div><h3>Produção completa (Spot)</h3><table><thead><tr><th>Opção</th><th>Por crédito</th><th>Total</th></tr></thead><tbody>'
 '<tr><td>Avulso · 1 Spot</td><td>R$ 29,90</td><td>R$ 29,90</td></tr><tr><td>15 Spots</td><td>R$ 14,90</td><td>R$ 223,50</td></tr><tr><td>30 Spots</td><td>R$ 10,90</td><td>R$ 327,00</td></tr></tbody></table></div></div>'
 '<p><strong>'+CREDIT_RULE+'</strong> Os valores de pacote por crédito dependem da compra do pacote completo. Textos maiores consomem mais créditos. Confira o total final e as condições antes de pagar. <a href="'+WHATSAPP+'">Consultar pacotes pelo WhatsApp</a></p></details><!-- credit-packages:end -->')

PRICE_CARDS = ('<div class="panel-grid panel-pricing-grid"><article class="panel-card"><span class="panel-plan-label">Pacote de 25 créditos · Somente a voz</span><h3>Locução Off</h3><strong class="panel-value">R$ 6,90</strong><p class="panel-price-unit">cada, na compra do pacote de 25 Offs</p><p><strong>Pacote completo: R$ 172,50.</strong> '+CREDIT_RULE+' Avulso: R$ 11,90 por crédito.</p><ul class="panel-inclusions"><li>Locução com voz humana profissional</li><li>Gravação da voz sem trilha e efeitos</li><li>Escolha do locutor no banco de vozes</li></ul><a class="panel-primary" href="'+WHATSAPP+'" data-cta="preco_off_whatsapp">Fazer pedido pelo WhatsApp</a></article>'
 '<article class="panel-card panel-card-featured"><span class="panel-plan-label panel-premium">Pacote de 30 créditos · Produção completa</span><h3>Produção completa (Spot) + Locução Off</h3><strong class="panel-value">R$ 10,90</strong><p class="panel-price-unit">cada, na compra do pacote de 30 Spots</p><p><strong>Pacote completo: R$ 327,00.</strong> '+CREDIT_RULE+' Avulso: R$ 29,90 por crédito.</p><ul class="panel-inclusions"><li>Spot comercial com locução profissional</li><li>Trilha, efeitos, edição e finalização</li><li>Locução Off incluída: voz separada, sem trilha e efeitos</li><li>Escolha do locutor no banco de vozes</li></ul><a class="panel-primary" href="'+WHATSAPP+'" data-cta="preco_spot_whatsapp">Fazer pedido pelo WhatsApp</a></article>'
 '<p class="panel-pricing-support">Dúvidas antes de começar? <a data-panel-support href="https://wa.me/5527996529832" target="_blank" rel="noopener">Fale pelo WhatsApp</a>. Confira todas as opções avulsas e de pacote abaixo.</p></div>')

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
