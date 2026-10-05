#!/usr/bin/env python3
"""Preserve the panel purchase journey in generated pages using standard-library HTML edits."""
import re
from pathlib import Path
REGISTER='/cadastro/'
LOGIN='/painel/'
PAYMENT='Compre créditos diretamente no Painel de Gravação, exclusivamente por PIX ou cartão de crédito, com processamento pelo Mercado Pago. A liberação é automática e imediata assim que o pagamento for confirmado. Confira o valor total e eventuais encargos apresentados antes de concluir a compra.'
PRICES='Locução Off avulsa: R$ 11,90 por crédito. Cada crédito vale até 40 segundos de áudio. Produção completa avulsa (spot comercial) + Locução Off: R$ 29,90 por crédito de até 40 segundos. Na produção, você recebe o spot finalizado e a gravação da voz separada, sem trilha e efeitos.'
SUPPORT='Pedidos e atendimento pelo WhatsApp: segunda a sexta, das 08h às 18h. Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.'

from runpy import run_path
PRICE_CARDS = run_path(str(Path(__file__).resolve().parent / 'site-prices.py'))['PRICE_CARDS']
SUPPORT_BUTTON='<a class="panel-whatsapp" data-panel-support data-cta="whatsapp_precos" href="https://wa.me/5527996529832" target="_blank" rel="noopener"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>\n        </svg><span>Prefiro pedir pelo WhatsApp</span></a>'
FLOAT_LINK='<a class="panel-help-link" data-panel-support data-cta="whatsapp_flutuante" href="https://wa.me/5527996529832" target="_blank" rel="noopener" aria-label="Falar com o suporte pelo WhatsApp, segunda a sexta das 08h às 18h"><svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">\n          <path fill-rule="evenodd" clip-rule="evenodd" d="M18.403 5.592A9.002 9.002 0 003.111 16.29L1.87 20.83a.6.6 0 00.732.732l4.54-1.241A9.002 9.002 0 0018.403 5.592zM12.004 2.2a9.792 9.792 0 00-8.48 14.691l-1.3 4.757a1.2 1.2 0 001.465 1.465l4.757-1.3A9.794 9.794 0 1012.004 2.2zm4.846 12.191c-.225-.113-1.328-.655-1.534-.73-.205-.075-.355-.113-.505.113-.15.225-.58.73-.711.88-.131.15-.262.169-.487.056a6.126 6.126 0 01-1.802-1.112 6.757 6.757 0 01-1.248-1.554c-.131-.225-.014-.347.098-.459.1-.1.225-.262.338-.394.113-.131.15-.225.225-.375.075-.15.038-.281-.019-.394-.056-.113-.505-1.218-.692-1.668-.182-.438-.367-.378-.505-.386l-.43-.008a.83.83 0 00-.6.281c-.206.225-.787.769-.787 1.875 0 1.106.806 2.175.918 2.325.113.15 1.587 2.423 3.845 3.398.537.232.956.37 1.283.474.54.172 1.03.148 1.418.09.432-.065 1.328-.543 1.516-1.068.188-.525.188-.975.131-1.068-.056-.094-.206-.15-.431-.263z" fill="currentColor"/>\n        </svg><span>Suporte<small>WhatsApp · seg–sex, 08h–18h</small></span></a>'

EXTRA_REPLACEMENTS={'Mande o roteiro completo pelo WhatsApp.': 'Crie sua conta grátis e envie o roteiro pelo Painel de Gravação.', 'Mande as mensagens do seu menu (ex: "Tecle 1 para comercial...") pelo WhatsApp.': 'Envie as mensagens do seu menu (ex.: "Tecle 1 para comercial...") pelo Painel de Gravação.', 'Você não precisa criar conta para começar.': 'O cadastro é grátis. Você pode ouvir as demos e ver os preços antes de criar sua conta.', 'O processo pode começar sem cadastro: escolha uma voz ou peça uma indicação, envie o texto pelo Painel de Gravação e diga se precisa somente da voz ou do áudio completo. Com essas informações, conseguimos orientar o pedido e confirmar o formato adequado.': 'Ouça as vozes e consulte os preços sem cadastro. Para pedir, crie sua conta grátis, adicione créditos e envie o texto pelo painel. Se precisar de ajuda para escolher o serviço, fale com o suporte.', 'Informações importantes ficam visíveis no site e são confirmadas no atendimento.': 'Conheça o serviço e os preços antes de criar sua conta. Confira as condições do pedido no painel.', 'no atendimento antes do pagamento': 'no painel antes de enviar o pedido', 'confirmados no atendimento': 'informados no painel', 'confirmada no atendimento': 'informada no painel', 'confirme a disponibilidade no atendimento': 'confira a disponibilidade no painel', 'para receber a confirmação no atendimento': 'e confira o prazo informado no painel', 'explique o formato necessário no atendimento': 'informe o formato necessário no painel', 'explique no atendimento como a gravação será utilizada': 'informe no painel como a gravação será utilizada', 'Definimos valor, prazo e orientações.': 'Confira o serviço, o valor e o prazo no painel antes de enviar o pedido.', 'Valem os preços informados no site ou confirmados no atendimento no momento da contratação.': 'Valem os preços informados no site e as condições apresentadas no painel no momento da contratação.'}
EDITORIAL_REPLACEMENTS={'Pedidos e atendimento pelo WhatsApp: segunda a sexta, das 08h às 18h. Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.': 'Faça seus pedidos diretamente pelo Painel de Gravação. Precisa de ajuda? Nosso suporte pelo WhatsApp atende de segunda a sexta, das 08h às 18h.', 'Pedir ou tirar dúvidas pelo WhatsApp': 'Falar com o suporte', 'O pedido pode ser orientado online pelo WhatsApp da A Locução.': 'Faça o pedido online pelo Painel de Gravação. Se precisar de orientação, o suporte humano está disponível pelo WhatsApp.', 'envie seu roteiro pelo WhatsApp para orçamento.': 'envie seu roteiro pelo Painel de Gravação. Suporte humano disponível para dúvidas.', 'Você escolhe a voz, envia o roteiro pelo WhatsApp e recebe o arquivo digital. Confirme orçamento, disponibilidade e prazo no atendimento.': 'Você escolhe a voz, envia o roteiro pelo Painel de Gravação e recebe o arquivo digital na sua conta. Confira o valor e o prazo no painel antes de enviar.', 'peça seu orçamento pelo WhatsApp.': 'confira os serviços e faça seu pedido no Painel de Gravação.', 'Envie seu roteiro pelo WhatsApp para receber um orçamento exato de imediato.': 'Confira o serviço, a duração e o valor no painel antes de enviar seu roteiro. Se precisar de orientação, fale com o suporte.', 'Envie pelo WhatsApp e informe onde a propaganda será usada.': 'Envie pelo Painel de Gravação e informe onde a propaganda será usada.', 'Explique seu projeto no WhatsApp e receba orientação sobre voz e formato.': 'Escolha a voz e o formato no painel. Se precisar de orientação, fale com o suporte.', 'Fale conosco pelo WhatsApp, escolha a locução e receba sua vinheta exclusiva.': 'Escolha a locução no Painel de Gravação, envie seu pedido e receba sua vinheta na sua conta.', 'O fim de ano já começou no comércio! Clique no botão abaixo, fale com a nossa equipe no WhatsApp e receba um orçamento sob medida para o seu negócio.': 'Prepare a campanha do seu comércio: crie sua conta grátis, escolha a voz e faça seu pedido pelo Painel de Gravação. Se precisar de ajuda, nosso suporte está disponível.', 'ou nos enviar o texto no WhatsApp para uma cotação rápida.': 'e conferir o serviço e o valor no Painel de Gravação antes de enviar seu roteiro.', 'Pedidos pelo WhatsApp ou sistema 24h': 'Pedidos pelo painel online 24h', 'use o WhatsApp para atendimento humano ou a Área de Pedidos 24h para fazer tudo pelo sistema.': 'faça seu pedido pelo Painel de Gravação. Se precisar de ajuda, fale com nosso suporte pelo WhatsApp.', '✓ Atendimento direto no WhatsApp': '✓ Painel online com suporte humano', '✓ Atendimento via WhatsApp': '✓ Painel online com suporte humano', 'Atendimento humano pelo WhatsApp': 'Suporte humano pelo WhatsApp', 'conforme as condições confirmadas no atendimento.': 'conforme as condições exibidas no painel antes da confirmação.', 'Confirme orçamento, disponibilidade e prazo no atendimento.': 'Confira valor, disponibilidade e prazo no painel.', 'Consulte a disponibilidade e o prazo no atendimento.': 'Confira a disponibilidade e o prazo no painel.', 'Confirmamos disponibilidade e prazo no atendimento.': 'Confira disponibilidade e prazo no painel antes de enviar.', 'A agilidade pelo WhatsApp pode ser menor que pelo painel.': 'Pedidos pelo painel; WhatsApp para suporte e dúvidas.', 'Pagamento via PIX ou cartão pelo Mercado Pago, conforme as condições confirmadas no pedido.': 'Compre créditos via PIX ou cartão pelo Mercado Pago. Confira as condições e o total no painel.', 'Analisamos o texto e confirmamos serviço, duração e valor antes da produção.': 'Confira o serviço, a duração e o valor no painel antes de enviar o pedido.', 'Prazo e disponibilidade são confirmados no atendimento.': 'Prazo e disponibilidade são informados no painel.', 'Suporte pelo WhatsApp: segunda a sexta, das 08h às 18h.': 'Suporte pelo WhatsApp: segunda a sexta, das 08h às 18h.', 'Pedidos e atendimento': 'Pedidos e suporte', 'Cadastrar grátis e fazer pedido ↗': 'Criar conta grátis', 'Cadastrar grátis e pedir ↗': 'Criar conta grátis e pedir', 'Cadastro grátis no painel ↗': 'Criar conta grátis', 'Cadastrar grátis ↗': 'Criar conta grátis', 'Já sou cliente: entrar no painel ↗': 'Já tenho conta: acessar painel', 'Entrar e fazer pedidos ↗': 'Acessar Painel de Gravação'}

def _normalize_panel_rules(text):
    if re.search(r'http-equiv=["\']refresh',text,re.I):return text
    text=re.sub(r'https://painel\.audio\.net\.br/[^"\s<>]+',LOGIN,text)
    text=re.sub(r'R\$\s*12(?:,00)?(?!\d|,\d)','R$ 11,90',text)
    text=re.sub(r'R\$\s*25(?:,00)?(?!\d|,\d)','R$ 29,90',text)
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
    text=re.sub(r'src=(["\'])/assets/site\.js(?:\?[^"\']*)?\1', lambda m: 'src='+m.group(1)+'/assets/site.js?v=20261003-panel-pages'+m.group(1),text)

    # Keep prices, delivery details and support choices consistent in regenerated pages.
    text=text.replace('24,40','29,90').replace('"price":"24.40"','"price":"29.90"').replace('"price": "24.40"','"price": "29.90"')
    text=re.sub(r'Quatro vinhetas off de até 10 segundos cada, com o mesmo locutor: R\$ 11,90\. Quatro vinhetas produzidas nas mesmas condições: R\$ 29,90\.', '',text)
    text=text.replace('Voz, trilha, efeitos e finalização. Valor por fração de 40 segundos.','Spot finalizado com voz, trilha, efeitos e finalização + Locução Off separada. Valor por fração de 40 segundos.')
    text=text.replace('Produção: R$ 29,90 por fração de 40 segundos.','Produção completa avulsa (spot comercial) + Locução Off: R$ 29,90 por crédito de até 40 segundos. Você recebe o spot finalizado e a voz separada, sem trilha e efeitos.')
    text=re.sub(r'<div class="panel-grid(?: panel-pricing-grid)?">.*?</div>',lambda m:PRICE_CARDS if 'panel-card' in m[0] else m[0],text,flags=re.S)
    text=re.sub(r'<tr><td>4 vinhetas (?:off|produzidas)</td>.*?</tr>','',text,flags=re.S)
    text=text.replace('<td>Produção</td>','<td>Produção (spot comercial) + Locução Off</td>')
    text=text.replace('Preços de locução, produção e vinhetas','Preços de Locução Off e Produção').replace('preços de locução off, produção e vinhetas','preços de locução off e produção').replace('Valores de locução off, produção de spot comercial e vinhetas.','Valores de Locução Off e Produção (spot comercial) com Locução Off incluída.')
    text=text.replace('Preços por serviço, sem pacotes','Escolha o áudio que você precisa')
    text=text.replace('blocks*2440/100','blocks*2990/100')
    text=text.replace('A Produção Completa reúne locução, trilha, efeitos e finalização para que você receba o material pronto para divulgação.','A Produção Completa inclui o spot com locução, trilha, efeitos e finalização, além da Locução Off separada, sem trilha e efeitos.')
    text=text.replace('A produção completa reúne locução, trilha, efeitos e finalização.','A produção completa inclui o spot finalizado com voz, trilha e efeitos, além da Locução Off separada, sem trilha e efeitos.')
    # Vinheta services remain listed without an advertised price.
    text=re.sub(r'<article class="card">.*?</article>',lambda m:re.sub(r'<span class="price">.*?</span>','',m[0],flags=re.S) if re.search(r'<h3>Vinheta',m[0]) else m[0],text,flags=re.S)
    # The panel owns purchase actions; WhatsApp offers human support.
    text=re.sub(r'<a class="panel-whatsapp"[^>]*>.*?</a>','',text,flags=re.S)
    text=re.sub(r'<a class="panel-help-link"[^>]*>.*?</a>',FLOAT_LINK,text,flags=re.S)
    if '<body' in text and 'class="panel-help-link"' not in text:
        text=text.replace('</body>',FLOAT_LINK+'\n</body>')

    text=text.replace('Suporte Suporte WhatsApp:', 'Suporte WhatsApp:')
    text=re.sub(r'(?<!Suporte )WhatsApp: \(27\) 99652-9832','Suporte WhatsApp: (27) 99652-9832',text)
    for old,new in EXTRA_REPLACEMENTS.items():text=text.replace(old,new)
    for old,new in EDITORIAL_REPLACEMENTS.items():text=text.replace(old,new)
    text=re.sub(r"(?:Suporte )+WhatsApp:", "Suporte WhatsApp:", text)
    # Preserve approved payment, plantão and per-order rules in regenerated pages.
    text=text.replace('Pagamento via PIX ou cartão de crédito pelo Mercado Pago. Crédito liberado imediatamente após a aprovação do pagamento. O Mercado Pago cobra uma pequena taxa por pagamento; confira o valor total antes de confirmar.','Compre créditos diretamente no Painel de Gravação, exclusivamente por PIX ou cartão de crédito, com processamento pelo Mercado Pago. A liberação é automática e imediata assim que o pagamento for confirmado. Confira o valor total e eventuais encargos apresentados antes de concluir a compra.')
    text=text.replace('Alguns profissionais também possuem disponibilidade em finais de semana e feriados.','Temos locutores de plantão todos os dias, inclusive finais de semana e feriados. Consulte a disponibilidade e o prazo de cada profissional no painel.')
    text=text.replace('Temos locutores com diferentes janelas de disponibilidade, inclusive opções de gravação rápida e atendimento em horários ampliados.','Temos locutores de plantão todos os dias, inclusive finais de semana e feriados. Escolha no painel o profissional disponível e confira o prazo antes de enviar.')
    text=text.replace('Locutores com disponibilidade todos os dias, inclusive finais de semana e feriados, conforme a agenda de cada profissional.','Locutores de plantão todos os dias, inclusive finais de semana e feriados. Consulte a disponibilidade de cada profissional no painel.')
    text=text.replace('Créditos via PIX ou cartão pelo Mercado Pago, liberados após aprovação.','Créditos comprados no painel via PIX ou cartão de crédito pelo Mercado Pago, com liberação automática e imediata após a confirmação do pagamento.')
    text=text.replace('Liberação imediata de crédito após aprovação do pagamento via PIX ou cartão de crédito pelo Mercado Pago.','Liberação automática e imediata dos créditos após a confirmação do pagamento pelo Mercado Pago, via PIX ou cartão de crédito no painel.')
    text=text.replace('As demonstrações funcionam sem JavaScript. Para confirmar o status atual, fale com o atendimento.','Ouça as demonstrações e confira a disponibilidade atual do locutor no Painel de Gravação.')
    text=text.replace('Não atendo mais que 16 vinhetas no pacote somente avulso.','Para este profissional, pedidos com mais de 16 vinhetas exigem contratação individual. Confira as condições no painel.')
    text=text.replace('um tema por pacote.','um tema por pedido.')
    text=text.replace('Não gravo vinhetas e chamadas artistico / promocionais para emissoras de Rádio no pacote.','Vinhetas e chamadas artísticas ou promocionais para emissoras de rádio exigem contratação específica com este profissional.')
    text=text.replace('href="#pacote"','href="#pedidos-recorrentes"')
    text=text.replace('id="pacote"','id="pedidos-recorrentes"')
    return text

def normalize_page(text):
    from runpy import run_path
    normalize_whatsapp = run_path(str(Path(__file__).resolve().parent / 'whatsapp-commerce.py'))['normalize_whatsapp']
    return normalize_whatsapp(text)

def main():
    root=Path(__file__).resolve().parent.parent
    changed=0
    for p in root.rglob('*.html'):
        if any(x.startswith('.') for x in p.relative_to(root).parts):continue
        old=p.read_text();new=normalize_page(old)
        if new!=old:p.write_text(new);changed+=1
    print('Panel purchase paths updated:',changed)
if __name__=='__main__':main()
