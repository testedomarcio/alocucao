#!/usr/bin/env python3
"""Preserve the panel purchase journey in generated pages using standard-library HTML edits."""
import re
from pathlib import Path
REGISTER='https://paineldegravacao.com.br/comerciaistop/cadastro'
LOGIN='https://paineldegravacao.com.br/comerciaistop'
PAYMENT='Pagamento via PIX ou cartão de crédito pelo Mercado Pago. Crédito liberado imediatamente após a aprovação do pagamento. O Mercado Pago cobra uma pequena taxa por pagamento; confira o valor total antes de confirmar.'
PRICES='Locução Off: R$ 11,90 por fração de 40 segundos. Produção: R$ 24,40 por fração de 40 segundos. Quatro vinhetas off de até 10 segundos cada, com o mesmo locutor: R$ 11,90. Quatro vinhetas produzidas nas mesmas condições: R$ 24,90.'
SUPPORT='Pedidos e atendimento pelo WhatsApp: segunda a sexta, das 08h às 18h. Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.'

def normalize_page(text):
    if re.search(r'http-equiv=["\']refresh',text,re.I):return text
    text=re.sub(r'https://painel\.audio\.net\.br/[^"\s<>]+',LOGIN,text)
    text=re.sub(r'R\$\s*12(?:,00)?(?![\d,])','R$ 11,90',text)
    text=re.sub(r'R\$\s*25(?:,00)?(?![\d,])','R$ 24,40',text)
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
    text=re.sub(r'src=(["\'])/assets/site\.js(?:\?[^"\']*)?\1', lambda m: 'src='+m.group(1)+'/assets/site.js?v=20261002-painel-2'+m.group(1),text)
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
