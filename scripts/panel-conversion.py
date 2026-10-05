#!/usr/bin/env python3
"""Keep static and generated sales CTAs on the panel; preserve floating support."""
import re
from pathlib import Path

PANEL = 'https://vozlocutor.com.br/painel/alocucao/'
SIGNUP = PANEL + 'cadastro'
AVAILABILITY = 'Nossa plataforma funciona 24h por dia! Locutores de plantão todos os dias, inclusive finais de semana e feriados, até às 22h.'
COPY = {
    'Comece seu pedido pelo WhatsApp e receba orientação da nossa equipe.': 'Faça o pedido online pelo Painel de Gravação. Se precisar de orientação, o suporte humano está disponível pelo WhatsApp.',
    'Comece pelo WhatsApp: envie seu texto e confirme os detalhes com nossa equipe.': 'Faça pedidos pelo Painel de Gravação e acompanhe cada etapa na sua conta.',
    'Fale pelo WhatsApp e conte o que você precisa gravar.': 'Crie sua conta grátis e complete o cadastro.',
    'Receba orientação sobre voz, serviço e compra de créditos via PIX ou cartão no painel.': 'Compre créditos no painel por PIX ou cartão de crédito, com processamento pelo Mercado Pago.',
    'Confirme o serviço, a voz, o valor e o prazo com nossa equipe antes de comprar.': 'Confira no painel o serviço, a quantidade efetiva de créditos, o valor total e o prazo antes de confirmar seu pedido.',
    'Nossa equipe ajuda você a escolher o serviço. Locução Off e Produção são cobradas': 'Escolha o serviço no painel. Locução Off e Produção são cobradas',
    'Orientação pelo WhatsApp antes de comprar.': 'Cadastro grátis e painel disponível 24 horas por dia.',
    'Ouça as demonstrações e confirme a disponibilidade do locutor pelo WhatsApp.': 'Ouça as demonstrações e confira a disponibilidade atual do locutor no Painel de Gravação.',
    'Fale pelo WhatsApp para confirmar a voz disponível e o prazo do seu pedido.': 'Escolha no painel o profissional disponível e confira o prazo antes de enviar.',
    'Confirme a disponibilidade de cada profissional pelo WhatsApp.': 'Consulte a disponibilidade de cada profissional no painel.',
    'Confirme a disponibilidade e o prazo de cada profissional pelo WhatsApp.': 'Consulte a disponibilidade e o prazo de cada profissional no painel.',
    'Fale pelo WhatsApp para começar seu pedido. A gravação depende da disponibilidade e do prazo do locutor escolhido.': 'Faça pedidos a qualquer hora pelo painel. A gravação depende da disponibilidade e do prazo do locutor escolhido.',
    'Nossa equipe orienta a compra de créditos via PIX ou cartão no painel. Confira as condições e o total antes de pagar.': 'Compre créditos via PIX ou cartão pelo Mercado Pago. Confira as condições e o total no painel.',
    'confirme pelo WhatsApp a disponibilidade e o prazo do serviço': 'confira no painel a disponibilidade e o prazo do serviço',
    'e fale pelo WhatsApp para escolher o profissional': 'e escolha o profissional no Painel de Gravação',
    'Fale com nossa equipe pelo WhatsApp. Informe a voz de': 'Cadastre-se grátis ou entre na sua conta. Selecione',
    'e confirme o serviço e o prazo antes de comprar.': 'no painel e confira o serviço e o prazo antes de enviar seu pedido.',
    'Vozes humanas · atendimento pelo WhatsApp': 'Vozes humanas · pedidos pelo painel',
    'Fale com nossa equipe pelo WhatsApp, envie seu texto e receba ajuda para escolher a voz e o serviço ideal. Peça somente a locução ou o spot comercial pronto para divulgar.': 'Escolha sua voz, envie seu texto e acompanhe o pedido no Painel de Gravação. Compre somente a locução ou receba o spot comercial pronto para divulgar.',
    'Converse com nossa equipe antes de comprar. Atendimento pelo WhatsApp de segunda a sexta, das 08h às 18h.': 'Cadastro gratuito. Compra de créditos via PIX ou cartão. Suporte humano quando você precisar.',
    'Comece seu pedido pelo WhatsApp': 'Seu pedido direto no Painel de Gravação',
    'Pedidos e atendimento pelo WhatsApp': 'Pedidos pelo painel online 24h',
    '✓ Atendimento pelo WhatsApp': '✓ Pedidos pelo painel 24h',
    '✓ Atendimento humano pelo WhatsApp': '✓ Painel online com suporte humano',
    'Conheça os serviços e os preços. Pelo WhatsApp, ajudamos você a escolher a voz e confirmamos os detalhes antes de comprar.': 'Conheça o serviço e os preços antes de criar sua conta. Confira as condições do pedido no painel.',
    'Envie seu texto pelo WhatsApp para confirmar o serviço, a duração, o valor e o prazo antes de comprar.': 'Confira o serviço, a duração e o valor no painel antes de enviar o pedido.',
    'Ouça as demonstrações e fale com nossa equipe pelo WhatsApp. Envie o roteiro, a finalidade e a voz desejada para confirmar a disponibilidade e o prazo. Se estiver em dúvida entre vozes, peça uma indicação.': 'Cadastre-se grátis no Painel de Gravação e confira o catálogo disponível para contratação. Escolha o locutor dentro do painel e envie o roteiro, a finalidade e as orientações. As demos e os status são sincronizados com o Painel de Gravação. Se estiver em dúvida entre vozes, peça uma indicação.',
    'Ao encontrar uma voz, fale com nossa equipe pelo WhatsApp. Informe o nome do locutor, envie o roteiro e explique a finalidade do áudio para confirmar os detalhes do pedido.': 'Ao encontrar uma voz, cadastre-se grátis ou entre no Painel de Gravação. Selecione o locutor na sua conta e informe o roteiro, a finalidade do áudio e as orientações antes de enviar o pedido.',
    'Ouça as vozes e consulte os preços sem cadastro. Para começar seu pedido, envie o texto pelo WhatsApp. Nossa equipe ajuda na escolha do serviço e orienta os próximos passos.': 'Ouça as vozes e consulte os preços sem cadastro. Para pedir, crie sua conta grátis, adicione créditos e envie o texto pelo painel. Se precisar de ajuda para escolher o serviço, fale com o suporte.',
    'O cliente começa pelo WhatsApp, recebe orientação e confirma os detalhes do pedido com nossa equipe. O Painel de Gravação continua disponível para comprar créditos, enviar e acompanhar pedidos e baixar arquivos.': 'O cliente pode tirar dúvidas e receber ajuda pelo WhatsApp. Compras, pedidos, acompanhamento e download são realizados pelo painel.',
    'Para começar seu pedido, fale com nossa equipe pelo WhatsApp.': 'Para pedir, cadastre-se grátis no Painel de Gravação.',
    'Fale pelo WhatsApp para escolher o serviço e a voz e confirmar o prazo antes de comprar.': 'Cadastre-se grátis no Painel de Gravação, confira o serviço, a voz e o prazo e acompanhe seu pedido pela sua conta.',
    'Envie seu texto pelo WhatsApp e conte onde o áudio será usado. Nossa equipe ajuda você a escolher a voz, confirma o serviço e o prazo e orienta os próximos passos. O Painel de Gravação continua disponível pelo menu superior.': 'Cadastre-se grátis, adicione créditos, escolha o locutor e envie o roteiro. Acompanhe a produção e baixe o áudio na sua conta.',
    'Prepare a campanha do seu comércio: envie seu texto pelo WhatsApp e receba ajuda para escolher a voz e o serviço ideal.': 'Prepare a campanha do seu comércio: crie sua conta grátis, escolha a voz e faça seu pedido pelo Painel de Gravação. Se precisar de ajuda, nosso suporte está disponível.',
    'Pedidos e atendimento': 'Pedidos e suporte',
    'Fale com nossa equipe para começar seu pedido.': 'A agilidade pelo WhatsApp pode ser menor que pelo painel.',
    'Nossa equipe orienta seu pedido pelo WhatsApp.': 'Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.',
    'Comece seu pedido pelo WhatsApp. Nossa equipe atende de segunda a sexta, das 08h às 18h.': 'Faça seus pedidos diretamente pelo Painel de Gravação. Precisa de ajuda? Nosso suporte pelo WhatsApp atende de segunda a sexta, das 08h às 18h.',
    'Comece seu pedido conversando com nossa equipe.': 'Seus pedidos são feitos pelo painel.',
    'pelo WhatsApp antes de confirmar': 'no painel antes de enviar',
    'pelo WhatsApp antes de fechar': 'no painel antes de fechar',
    'confirme disponibilidade e prazo pelo WhatsApp': 'confirme disponibilidade e prazo no painel',
    'Confirme disponibilidade e prazo pelo WhatsApp': 'Confira disponibilidade e prazo no painel',
    'Confirme a disponibilidade e o prazo pelo WhatsApp': 'Confira a disponibilidade e o prazo no painel',
}

def normalize_panel(text):
    if re.search(r'http-equiv=["\']refresh', text, re.I):
        return text
    floating = []
    def protect(match):
        floating.append(match[0])
        return f'__PRESERVED_FLOAT_{len(floating)-1}__'
    text = re.sub(r'<a\b[^>]*(?:panel-help-link|whatsapp-float|wa-float-button)[^>]*>.*?</a>', protect, text, flags=re.S)
    def anchor(match):
        tag = match[0]
        href = re.search(r'href=(["\'])(.*?)\1', tag)
        if not href:
            return tag
        url = href[2]
        whatsapp = re.match(r'https://(?:wa\.me|(?:api|web)\.whatsapp\.com)', url)
        legacy = re.match(r'/(?:painel|cadastro)/?(?:[?#].*)?$', url)
        placeholder = url in ('{{whatsappUrl}}', '{{panelUrl}}')
        current_panel = url.startswith(PANEL)
        if not (whatsapp or legacy or placeholder or current_panel):
            return tag
        secondary = any(marker in tag for marker in ('al-login', 'panel-secondary', 'pacotes_painel')) or bool(re.search(r'>\s*(?:Entrar|Acessar|Já tenho|Já sou|Ver preços)', tag))
        signup = not secondary
        if whatsapp and ('data-panel-support' in tag or any(label in tag for label in ('Consultar meu benefício', 'Falar sobre a campanha'))):
            return 'balão de atendimento no canto da tela'
        target = SIGNUP if signup else PANEL
        tag = tag[:href.start(2)] + target + tag[href.end(2):]
        tag = re.sub(r'(<a\b[^>]*>).*?(</a>)', lambda m: m[1]+('Criar Conta Gratuita' if signup else 'Acessar Painel')+m[2], tag, flags=re.S)
        tag = re.sub(r'\saria-label=(["\']).*?\1', '', tag)
        tag = re.sub(r'data-cta="([^"]+)"', lambda m: 'data-cta="'+m[1].replace('cabecalho_whatsapp', 'cabecalho_cadastro').replace('whatsapp', 'painel')+'"', tag)
        return tag
    text = re.sub(r'<a\b[^>]*>.*?</a>', anchor, text, flags=re.S)
    for old, new in sorted(COPY.items(), key=lambda pair: len(pair[0]), reverse=True):
        text = text.replace(old, new)
    text = re.sub(r'(?:fale com nossa equipe e ){2,}', '', text)
    replacements = {
        'Pedido direto no painel de segunda a sexta, das 08h às 18h. Envie seu texto e receba orientação para começar.': 'Suporte humano: segunda a sexta, das 08h às 18h.',
        'Pedido direto no painel de segunda a sexta, das 08h às 18h. O prazo de entrega depende do roteiro, do serviço e da disponibilidade do locutor.': 'Faça pedidos pelo painel a qualquer hora. O prazo de entrega depende do roteiro, do serviço e da disponibilidade do locutor.',
        'Seu áudio começa com uma conversa': 'Seu áudio começa no Painel de Gravação',
        'Conte o que você precisa e receba orientação para fazer seu pedido.': 'Crie sua conta grátis, escolha a voz e envie seu roteiro pelo painel.',
        '<strong>Fale pelo WhatsApp</strong>': '<strong>Crie sua conta gratuita</strong>',
        'Envie seu roteiro e informe onde o áudio será usado e quando precisa receber.': 'Complete seu cadastro para comprar créditos e enviar seu roteiro.',
        'Nossa equipe ajuda a escolher entre Locução Off e Spot Comercial e confirma disponibilidade, valor e prazo.': 'Escolha Locução Off ou Produção completa e confira a voz, o valor e o prazo no painel.',
        'Receba orientação para comprar': 'Compre créditos e envie o pedido',
        'Orientamos a compra de créditos e o envio do pedido no Painel de Gravação.': 'Compre créditos por PIX ou cartão e envie seu roteiro com as orientações da gravação.',
        'Já usa o painel? O acesso continua no menu superior. Os tutoriais seguem disponíveis para consultar as etapas.': 'Já tem conta? Acesse o painel. Consulte nossos tutoriais para acompanhar cada etapa.',
        'O Painel de Gravação continua disponível no menu superior para clientes que desejam comprar créditos, enviar e acompanhar pedidos e baixar as gravações.': 'No Painel de Gravação você compra créditos, envia e acompanha pedidos e baixa suas gravações.',
        'Atendimento pelo WhatsApp de segunda a sexta, das 08h às 18h. Envie seu texto e receba orientação para começar.': AVAILABILITY,
        'Envie o roteiro pelo WhatsApp': 'Envie o roteiro pelo Painel de Gravação',
        'Envie o texto pelo WhatsApp': 'Envie o texto pelo Painel de Gravação',
        'Envie seu texto pelo WhatsApp': 'Envie seu texto pelo Painel de Gravação',
        'envia o roteiro pelo WhatsApp': 'envia o roteiro pelo Painel de Gravação',
        'pelo WhatsApp antes de confirmar': 'no painel antes de confirmar',
        'pelo WhatsApp antes de fechar': 'no painel antes de fechar',
        'direto no WhatsApp': 'direto no Painel de Gravação',
        'Confirme a disponibilidade e o prazo pelo WhatsApp.': 'Confira a disponibilidade e o prazo no painel.',
        'Confirme disponibilidade e prazo pelo WhatsApp': 'Confira disponibilidade e prazo no painel',
        'Copie seu roteiro para enviá-lo pelo WhatsApp': 'Copie seu roteiro para enviá-lo na sua conta do painel',
        'Envie pelo WhatsApp e informe': 'Envie pelo Painel de Gravação e informe',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.replace('pelo número balão de atendimento no canto da tela', 'pelo balão de atendimento no canto da tela')
    text = text.replace('Dúvidas antes de começar? balão de atendimento no canto da tela.', 'Dúvidas? Use o balão de atendimento no canto da tela.')
    text = text.replace('Precisa de ajuda com uma mensagem do painel? balão de atendimento no canto da tela.', 'Precisa de ajuda com uma mensagem do painel? Use o balão de atendimento no canto da tela.')
    text = text.replace('envie seu texto pelo WhatsApp', 'crie sua conta gratuita e envie seu texto pelo Painel de Gravação')
    text = re.sub(r'<div class="ref-actions">\s*balão de atendimento no canto da tela\s*</div>', '<p>Para consultar benefícios, use o balão de atendimento no canto da tela.</p>', text)
    # Every shared footer carries the availability statement, including generated pages.
    if '<!-- site-footer:start -->' in text:
        text = re.sub(r'(<div><h2>Pedidos e (?:atendimento|suporte)</h2>)(.*?)(</div>)',
            lambda m: m[0] if AVAILABILITY in m[0] else m[1]+m[2]+'<p>'+AVAILABILITY+'</p>'+m[3], text, flags=re.S)
    text = text.replace('data-cta="cabecalho_painel">Criar Conta Gratuita', 'data-cta="cabecalho_cadastro">Criar Conta Gratuita')
    text = re.sub(r'src="(/assets/(?:site|voice-bank|voice-profile|featured-voices|tracking)\.js)(?:\?[^"]*)?"', r'src="\1?v=20261005-panel-conversion"', text)
    for i, original in enumerate(floating):
        text = text.replace(f'__PRESERVED_FLOAT_{i}__', original)
    return text

if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    changed = 0
    for page in root.rglob('*.html'):
        if any(part.startswith('.') or part in ('node_modules', '_site') for part in page.relative_to(root).parts):
            continue
        old = page.read_text(); new = normalize_panel(old)
        if old != new:
            page.write_text(new); changed += 1
    print('Panel conversion pages updated:', changed)
