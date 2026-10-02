#!/usr/bin/env python3
"""Preserve the panel purchase journey in generated pages using standard-library HTML edits."""
import re
from pathlib import Path
REGISTER='https://paineldegravacao.com.br/comerciaistop/cadastro'
LOGIN='https://paineldegravacao.com.br/comerciaistop'
PAYMENT='Pagamento via PIX ou cartão de crédito pelo Mercado Pago. Crédito liberado imediatamente após a aprovação do pagamento. O Mercado Pago cobra uma pequena taxa por pagamento; confira o valor total antes de confirmar.'
PRICES='Locução Off: R$ 11,90 por fração de 40 segundos. Produção (spot comercial) + Locução Off: R$ 24,90 por fração de 40 segundos. Na produção, você recebe o spot finalizado e a gravação da voz separada, sem trilha e efeitos.'
SUPPORT='Pedidos e atendimento pelo WhatsApp: segunda a sexta, das 08h às 18h. Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.'

PRICE_CARDS='<div class="panel-grid panel-pricing-grid"><article class="panel-card"><span class="panel-plan-label">Somente a voz</span><h3>Locução Off</h3><strong class="panel-value">R$ 11,90</strong><p class="panel-price-unit">por fração de 40 segundos</p><p>Para quem já tem editor e precisa da voz profissional para seu projeto.</p><ul class="panel-inclusions"><li>Locução com voz humana profissional</li><li>Gravação da voz sem trilha e efeitos</li><li>Escolha do locutor no banco de vozes</li></ul><a class="panel-primary" href="https://paineldegravacao.com.br/comerciaistop/cadastro" target="_blank" rel="noopener" data-cta="preco_off_cadastro">Cadastrar grátis e pedir Off</a><a class="panel-whatsapp" data-panel-support data-cta="whatsapp_precos" href="https://wa.me/5527996529832" target="_blank" rel="noopener"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>\n        </svg><span>Prefiro pedir pelo WhatsApp</span></a></article><article class="panel-card panel-card-featured"><span class="panel-plan-label panel-premium">Produção completa</span><h3>Produção (spot comercial) + Locução Off</h3><strong class="panel-value">R$ 24,90</strong><p class="panel-price-unit">por fração de 40 segundos</p><p>Receba o anúncio pronto para divulgar e a gravação da voz separada.</p><ul class="panel-inclusions"><li>Spot comercial com locução profissional</li><li>Trilha, efeitos, edição e finalização</li><li>Locução Off incluída: voz separada, sem trilha e efeitos</li><li>Escolha do locutor no banco de vozes</li></ul><a class="panel-primary" href="https://paineldegravacao.com.br/comerciaistop/cadastro" target="_blank" rel="noopener" data-cta="preco_spot_cadastro">Cadastrar grátis e pedir produção</a><a class="panel-whatsapp" data-panel-support data-cta="whatsapp_precos" href="https://wa.me/5527996529832" target="_blank" rel="noopener"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>\n        </svg><span>Prefiro pedir pelo WhatsApp</span></a></article></div>'
SUPPORT_BUTTON='<a class="panel-whatsapp" data-panel-support data-cta="whatsapp_precos" href="https://wa.me/5527996529832" target="_blank" rel="noopener"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>\n        </svg><span>Prefiro pedir pelo WhatsApp</span></a>'
FLOAT_LINK='<a class="panel-help-link" data-panel-support data-cta="whatsapp_flutuante" href="https://wa.me/5527996529832" target="_blank" rel="noopener" aria-label="Pedir ou falar pelo WhatsApp, segunda a sexta das 08h às 18h"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>\n        </svg><span>Fale pelo WhatsApp<small>Seg–sex · 08h às 18h</small></span></a>'

def normalize_page(text):
    if re.search(r'http-equiv=["\']refresh',text,re.I):return text
    text=re.sub(r'https://painel\.audio\.net\.br/[^"\s<>]+',LOGIN,text)
    text=re.sub(r'R\$\s*12(?:,00)?(?![\d,])','R$ 11,90',text)
    text=re.sub(r'R\$\s*25(?:,00)?(?![\d,])','R$ 24,90',text)
    text=text.replace('Preços e pacotes','Preços').replace('preços e pacotes','preços').replace('preço por pacote','preço por serviço')
    # Convert purchase CTAs; contact links in the footer stay available as support.
    def anchor(m):
        tag=m.group(0)
        if not re.search(r'href=["\']https://(?:wa\.me|api\.whatsapp\.com)',tag):return tag
        if 'rodape_whatsapp' in tag or 'data-panel-support' in tag or 'avaliac' in tag.lower():return tag
        label='Cadastrar grátis e fazer pedido ↗'
        tag=re.sub(r'href=(["\']).*?\1',lambda n:'href='+n.group(1)+REGISTER+n.group(1),tag,count=1)
        tag=re.sub(r'(?<=\>).*?(?=</a>)',label,tag,flags=re.S)
        return tag
    text=re.sub(r'<a\b[^>]*>.*?</a>',anchor,text,flags=re.S)
    text=text.replace('por 1 produção completa','por fração de 40 segundos').replace('por 1 locução off de até 40 segundos','por fração de 40 segundos')
    text=text.replace('Gravações até 22h','Pedidos online 24h').replace('Alguns locutores trabalham em horário ampliado. A disponibilidade é confirmada antes do pedido.','Faça pedidos a qualquer hora pelo painel. A gravação depende da disponibilidade e do prazo do locutor escolhido.')
    text=text.replace('peça pelo WhatsApp','faça seu pedido no Painel de Gravação').replace('Peça pelo WhatsApp','Faça seu pedido no Painel de Gravação').replace('envie seu texto pelo WhatsApp','cadastre-se grátis e envie seu texto no painel').replace('Enviar roteiro pelo WhatsApp','Enviar roteiro no painel').replace('contratação pelo WhatsApp','contratação pelo Painel de Gravação')
    text=re.sub(r'src=(["\'])/assets/site\.js(?:\?[^"\']*)?\1', lambda m: 'src='+m.group(1)+'/assets/site.js?v=20261002-compras-3'+m.group(1),text)

    # Keep prices, delivery details and support choices consistent in regenerated pages.
    text=text.replace('24,40','24,90').replace('"price":"24.40"','"price":"24.90"').replace('"price": "24.40"','"price": "24.90"')
    text=re.sub(r'Quatro vinhetas off de até 10 segundos cada, com o mesmo locutor: R\$ 11,90\. Quatro vinhetas produzidas nas mesmas condições: R\$ 24,90\.', '',text)
    text=text.replace('Voz, trilha, efeitos e finalização. Valor por fração de 40 segundos.','Spot finalizado com voz, trilha, efeitos e finalização + Locução Off separada. Valor por fração de 40 segundos.')
    text=text.replace('Produção: R$ 24,90 por fração de 40 segundos.','Produção (spot comercial) + Locução Off: R$ 24,90 por fração de 40 segundos. Você recebe o spot finalizado e a voz separada, sem trilha e efeitos.')
    text=re.sub(r'<div class="panel-grid(?: panel-pricing-grid)?">.*?</div>',lambda m:PRICE_CARDS if 'panel-card' in m[0] else m[0],text,flags=re.S)
    text=re.sub(r'<tr><td>4 vinhetas (?:off|produzidas)</td>.*?</tr>','',text,flags=re.S)
    text=text.replace('<td>Produção</td>','<td>Produção (spot comercial) + Locução Off</td>')
    text=text.replace('Preços de locução, produção e vinhetas','Preços de Locução Off e Produção').replace('preços de locução off, produção e vinhetas','preços de locução off e produção').replace('Valores de locução off, produção de spot comercial e vinhetas.','Valores de Locução Off e Produção (spot comercial) com Locução Off incluída.')
    text=text.replace('Preços por serviço, sem pacotes','Escolha o áudio que você precisa')
    text=text.replace('blocks*2440/100','blocks*2490/100')
    text=text.replace('A Produção Completa reúne locução, trilha, efeitos e finalização para que você receba o material pronto para divulgação.','A Produção Completa inclui o spot com locução, trilha, efeitos e finalização, além da Locução Off separada, sem trilha e efeitos.')
    text=text.replace('A produção completa reúne locução, trilha, efeitos e finalização.','A produção completa inclui o spot finalizado com voz, trilha e efeitos, além da Locução Off separada, sem trilha e efeitos.')
    # Vinheta services remain listed without an advertised price.
    text=re.sub(r'<article class="card">.*?</article>',lambda m:re.sub(r'<span class="price">.*?</span>','',m[0],flags=re.S) if re.search(r'<h3>Vinheta',m[0]) else m[0],text,flags=re.S)
    # Add an alternative beside the panel's main actions, without requiring an account.
    def support_action(m):
        block=m[0]
        if 'panel-whatsapp' not in block:block=block.replace('</div>',SUPPORT_BUTTON+'</div>')
        return block
    text=re.sub(r'<div class="(?:panel-actions|hero-actions)">.*?</div>',support_action,text,flags=re.S)
    text=text.replace('Preciso de ajuda pelo WhatsApp','Pedir ou tirar dúvidas pelo WhatsApp')
    text=re.sub(r'<a class="panel-help-link"[^>]*>.*?</a>',FLOAT_LINK,text,flags=re.S)
    if '<body' in text and 'class="panel-help-link"' not in text:
        text=text.replace('</body>',FLOAT_LINK+'\n</body>')
    return text

def main():
    root=Path(__file__).resolve().parent.parent
    changed=0
    for p in root.rglob('*.html'):
        if any(x.startswith('.') for x in p.relative_to(root).parts):continue
        old=p.read_text();new=normalize_page(old)
        if new!=old:p.write_text(new);changed+=1
    print('Panel purchase paths updated:',changed)
if __name__=='__main__':main()
