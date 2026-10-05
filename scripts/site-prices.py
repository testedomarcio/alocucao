#!/usr/bin/env python3
"""Keep current retail prices and secondary credit packages in generated pages."""
import re
PACKAGES = '<!-- credit-packages:start --><details class="credit-packages" id="pacotes"><summary>Pacotes para pedidos recorrentes</summary><div class="credit-packages-grid"><div><h3>Locução Off</h3><table><thead><tr><th>Pacote</th><th>Por crédito</th><th>Total</th></tr></thead><tbody><tr><td>5 Offs</td><td>R$ 10,00</td><td>R$ 50,00</td></tr><tr><td>25 Offs</td><td>R$ 6,00</td><td>R$ 150,00</td></tr></tbody></table></div><div><h3>Produção completa (Spot)</h3><table><thead><tr><th>Pacote</th><th>Por crédito</th><th>Total</th></tr></thead><tbody><tr><td>15 Spots</td><td>R$ 15,00</td><td>R$ 225,00</td></tr><tr><td>30 Spots</td><td>R$ 10,00</td><td>R$ 300,00</td></tr></tbody></table></div></div><p>O valor por crédito depende da compra do pacote completo. Confira o consumo de créditos e as condições do pedido antes de comprar. <a href="https://wa.me/5527996529832?text=Ol%C3%A1%21%20Quero%20informa%C3%A7%C3%B5es%20sobre%20os%20pacotes%20de%20cr%C3%A9ditos.">Consultar pacotes pelo WhatsApp</a></p></details><!-- credit-packages:end -->'

def normalize_prices(text):
    text = text.replace('11,90','14,90').replace('24,90','29,90').replace('11.90','14.90').replace('24.90','29.90')
    text = text.replace('blocks*1190/100','blocks*1490/100').replace('blocks*2490/100','blocks*2990/100')
    if 'panel-pricing-grid' in text and '<!-- credit-packages:start -->' not in text:
        text = re.sub(r'(<p class="panel-pricing-support">.*?</p></div>)', lambda m:m[0]+PACKAGES, text, count=1, flags=re.S)
    return text
