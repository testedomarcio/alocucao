#!/usr/bin/env python3
"""Keep WhatsApp as the sales entry point, including regenerated content."""
import re
from pathlib import Path

WHATSAPP = 'https://wa.me/5527996529832?text=Ol%C3%A1%21%20Vim%20pelo%20site%20A%20Locu%C3%A7%C3%A3o%20e%20quero%20fazer%20um%20pedido.'

COPY = {
 'Faça o pedido online pelo Painel de Gravação. Se precisar de orientação, o suporte humano está disponível pelo WhatsApp.': 'Comece seu pedido pelo WhatsApp e receba orientação da nossa equipe.',
 'Faça pedidos pelo Painel de Gravação e acompanhe cada etapa na sua conta.': 'Comece pelo WhatsApp: envie seu texto e confirme os detalhes com nossa equipe.',
 'Como funciona pelo Painel de Gravação': 'Como fazer seu pedido',
 'Crie sua conta grátis e complete o cadastro.': 'Fale pelo WhatsApp e conte o que você precisa gravar.',
 'Compre créditos no painel por PIX ou cartão de crédito, com processamento pelo Mercado Pago.': 'Receba orientação sobre voz, serviço e compra de créditos via PIX ou cartão no painel.',
 'Confira no painel o serviço, a quantidade efetiva de créditos, o valor total e o prazo antes de confirmar seu pedido.': 'Confirme o serviço, a voz, o valor e o prazo com nossa equipe antes de comprar.',
 'Escolha o serviço no painel. Locução Off e Produção são cobradas': 'Nossa equipe ajuda você a escolher o serviço. Locução Off e Produção são cobradas',
 'Cadastro grátis e painel disponível 24 horas por dia.': 'Orientação pelo WhatsApp antes de comprar.',
 'Ouça as demonstrações e confira a disponibilidade atual do locutor no Painel de Gravação.': 'Ouça as demonstrações e confirme a disponibilidade do locutor pelo WhatsApp.',
 'Escolha no painel o profissional disponível e confira o prazo antes de enviar.': 'Fale pelo WhatsApp para confirmar a voz disponível e o prazo do seu pedido.',
 'Consulte a disponibilidade de cada profissional no painel.': 'Confirme a disponibilidade de cada profissional pelo WhatsApp.',
 'Consulte a disponibilidade e o prazo de cada profissional no painel.': 'Confirme a disponibilidade e o prazo de cada profissional pelo WhatsApp.',
 'Faça pedidos a qualquer hora pelo painel. A gravação depende da disponibilidade e do prazo do locutor escolhido.': 'Fale pelo WhatsApp para começar seu pedido. A gravação depende da disponibilidade e do prazo do locutor escolhido.',
 'Compre créditos via PIX ou cartão pelo Mercado Pago. Confira as condições e o total no painel.': 'Nossa equipe orienta a compra de créditos via PIX ou cartão no painel. Confira as condições e o total antes de pagar.',
 'confira no painel a disponibilidade e o prazo do serviço': 'confirme pelo WhatsApp a disponibilidade e o prazo do serviço',
 'e escolha o profissional no Painel de Gravação': 'e fale pelo WhatsApp para escolher o profissional',
 'Cadastre-se grátis ou entre na sua conta. Selecione': 'Fale com nossa equipe pelo WhatsApp. Informe a voz de',
 'no painel e confira o serviço e o prazo antes de enviar seu pedido.': 'e confirme o serviço e o prazo antes de comprar.',
 'Vozes humanas · pedidos pelo painel': 'Vozes humanas · atendimento pelo WhatsApp',
 'Escolha sua voz, envie seu texto e acompanhe o pedido no Painel de Gravação. Compre somente a locução ou receba o spot comercial pronto para divulgar.': 'Fale com nossa equipe pelo WhatsApp, envie seu texto e receba ajuda para escolher a voz e o serviço ideal. Peça somente a locução ou o spot comercial pronto para divulgar.',
 'Cadastro gratuito. Compra de créditos via PIX ou cartão. Suporte humano quando você precisar.': 'Converse com nossa equipe antes de comprar. Atendimento pelo WhatsApp de segunda a sexta, das 08h às 18h.',
 'Seu pedido direto no Painel de Gravação': 'Comece seu pedido pelo WhatsApp',
 'Pedido direto no painel': 'Atendimento pelo WhatsApp',
 'Pedidos pelo painel online 24h': 'Pedidos e atendimento pelo WhatsApp',
 '✓ Pedido direto no painel': '✓ Atendimento pelo WhatsApp',
 '✓ Pedidos pelo painel 24h': '✓ Atendimento pelo WhatsApp',
 '✓ Painel online com suporte humano': '✓ Atendimento humano pelo WhatsApp',
 'Conheça o serviço e os preços antes de criar sua conta. Confira as condições do pedido no painel.': 'Conheça os serviços e os preços. Pelo WhatsApp, ajudamos você a escolher a voz e confirmamos os detalhes antes de comprar.',
 'Confira o serviço, a duração e o valor no painel antes de enviar o pedido.': 'Envie seu texto pelo WhatsApp para confirmar o serviço, a duração, o valor e o prazo antes de comprar.',
 'Cadastre-se grátis no Painel de Gravação e confira o catálogo disponível para contratação. Escolha o locutor dentro do painel e envie o roteiro, a finalidade e as orientações. As demos e os status são sincronizados com o Painel de Gravação. Se estiver em dúvida entre vozes, peça uma indicação.': 'Ouça as demonstrações e fale com nossa equipe pelo WhatsApp. Envie o roteiro, a finalidade e a voz desejada para confirmar a disponibilidade e o prazo. Se estiver em dúvida entre vozes, peça uma indicação.',
 'Ao encontrar uma voz, cadastre-se grátis ou entre no Painel de Gravação. Selecione o locutor na sua conta e informe o roteiro, a finalidade do áudio e as orientações antes de enviar o pedido.': 'Ao encontrar uma voz, fale com nossa equipe pelo WhatsApp. Informe o nome do locutor, envie o roteiro e explique a finalidade do áudio para confirmar os detalhes do pedido.',
 'Ouça as vozes e consulte os preços sem cadastro. Para pedir, crie sua conta grátis, adicione créditos e envie o texto pelo painel. Se precisar de ajuda para escolher o serviço, fale com o suporte.': 'Ouça as vozes e consulte os preços sem cadastro. Para começar seu pedido, envie o texto pelo WhatsApp. Nossa equipe ajuda na escolha do serviço e orienta os próximos passos.',
 'O cliente pode tirar dúvidas e receber ajuda pelo WhatsApp. Compras, pedidos, acompanhamento e download são realizados pelo painel.': 'O cliente começa pelo WhatsApp, recebe orientação e confirma os detalhes do pedido com nossa equipe. O Painel de Gravação continua disponível para comprar créditos, enviar e acompanhar pedidos e baixar arquivos.',
 'Para pedir, cadastre-se grátis no Painel de Gravação.': 'Para começar seu pedido, fale com nossa equipe pelo WhatsApp.',
 'Cadastre-se grátis no Painel de Gravação, confira o serviço, a voz e o prazo e acompanhe seu pedido pela sua conta.': 'Fale pelo WhatsApp para escolher o serviço e a voz e confirmar o prazo antes de comprar.',
 'Cadastre-se grátis, adicione créditos, escolha o locutor e envie o roteiro. Acompanhe a produção e baixe o áudio na sua conta.': 'Envie seu texto pelo WhatsApp e conte onde o áudio será usado. Nossa equipe ajuda você a escolher a voz, confirma o serviço e o prazo e orienta os próximos passos. O Painel de Gravação continua disponível pelo menu superior.',
 'Prepare a campanha do seu comércio: crie sua conta grátis, escolha a voz e faça seu pedido pelo Painel de Gravação. Se precisar de ajuda, nosso suporte está disponível.': 'Prepare a campanha do seu comércio: envie seu texto pelo WhatsApp e receba ajuda para escolher a voz e o serviço ideal.',
 'Falar com o suporte': 'Falar pelo WhatsApp',
 'Fale com o suporte': 'Fale pelo WhatsApp',
 'Suporte humano pelo WhatsApp': 'Atendimento humano pelo WhatsApp',
 'Suporte WhatsApp:': 'WhatsApp:',
 'Pedidos e suporte': 'Pedidos e atendimento',
 'Pedidos pelo painel; WhatsApp para suporte e dúvidas.': 'Fale com nossa equipe para começar seu pedido.',
 'A agilidade pelo WhatsApp pode ser menor que pelo painel.': 'Fale com nossa equipe para começar seu pedido.',
 'Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.': 'Nossa equipe orienta seu pedido pelo WhatsApp.',
 'Faça seus pedidos diretamente pelo Painel de Gravação. Precisa de ajuda? Nosso suporte pelo WhatsApp atende de segunda a sexta, das 08h às 18h.': 'Comece seu pedido pelo WhatsApp. Nossa equipe atende de segunda a sexta, das 08h às 18h.',
 'Seus pedidos são feitos pelo painel.': 'Comece seu pedido conversando com nossa equipe.',
 'no painel antes de enviar': 'pelo WhatsApp antes de confirmar',
 'no painel antes de fechar': 'pelo WhatsApp antes de fechar',
 'confirme disponibilidade e prazo no painel': 'confirme disponibilidade e prazo pelo WhatsApp',
 'Confirme disponibilidade e prazo no painel': 'Confirme disponibilidade e prazo pelo WhatsApp',
 'Confira a disponibilidade e o prazo no painel': 'Confirme a disponibilidade e o prazo pelo WhatsApp',
 'Confira disponibilidade e prazo no painel': 'Confirme disponibilidade e prazo pelo WhatsApp',
 'Suporte<small>WhatsApp': 'Faça seu pedido<small>WhatsApp',
 'Falar com o suporte pelo WhatsApp': 'Fazer pedido pelo WhatsApp',
}

def normalize_whatsapp(text):
    if re.search(r'http-equiv=["\']refresh', text, re.I): return text
    header = re.search(r'<!-- site-header:start -->.*?<!-- site-header:end -->', text, re.S)
    saved = header[0] if header else None
    if saved: text = text.replace(saved, '__SALES_HEADER__', 1)
    def anchor(match):
        tag = match[0]
        href = re.search(r'href=(["\'])(.*?)\1', tag)
        if not href: return tag
        url = href[2]
        if not (re.match(r'/(?:painel|cadastro)/?(?:[?#].*)?$', url) or re.match(r'https://(?:paineldegravacao\.com\.br/comerciaistop|painel\.audio\.net\.br)', url)): return tag
        tag = tag[:href.start(2)] + WHATSAPP + tag[href.end(2):]
        tag = re.sub(r'(<a\b[^>]*>).*?(</a>)', r'\1Fazer pedido pelo WhatsApp\2', tag, flags=re.S)
        tag = re.sub(r'data-cta="([^"]+)"', lambda m: 'data-cta="'+m[1].replace('cadastro','whatsapp').replace('login','whatsapp')+'"', tag)
        return tag
    text = re.sub(r'<a\b[^>]*>.*?</a>', anchor, text, flags=re.S)
    # Tutorial and legal text retain accurate panel instructions. Sales language changes elsewhere.
    tutorial = 'class="tutorial-' in text or 'class="tutorials-' in text
    legal = '<h2>1. Identificação e serviços</h2>' in text or 'Esta política explica' in text
    if not tutorial and not legal and 'data-panel-page' not in text:
        for old, new in COPY.items(): text = text.replace(old, new)
        text = re.sub(r'(?i)(envie(?: seu| o| as)?[^<>.!?]*?)pelo Painel de Gravação', r'\1pelo WhatsApp', text)
        text = text.replace('envia o roteiro pelo Painel de Gravação', 'envia o roteiro pelo WhatsApp')
        text = text.replace('cadastre-se grátis e envie seu texto no painel', 'fale com nossa equipe e envie seu texto pelo WhatsApp')
        text = text.replace('Indique a voz desejada em nosso painel', 'Indique a voz desejada pelo WhatsApp')
        text = text.replace('Precisa de mais opções? Acesse nosso painel de clientes e escolha a voz perfeita.', 'Precisa de mais opções? Fale pelo WhatsApp e peça uma indicação de voz para seu projeto.')
        text = text.replace('Selecione a locutora ou locutor ideal em nosso painel de vozes.', 'Ouça as vozes e peça ajuda pelo WhatsApp para escolher seu locutor.')
        text = text.replace('Copie seu roteiro para enviá-lo na sua conta; ele não é transferido automaticamente.', 'Copie seu roteiro para enviá-lo pelo WhatsApp; ele não é transferido automaticamente.')
        text = re.sub(r'Cadastre-se grátis no painel e selecione ([^<>]+?) ao enviar seu pedido\. Se já tem conta, use Entrar no menu\.', r'Fale pelo WhatsApp e informe que deseja uma gravação com \1. Nossa equipe confirma a disponibilidade e orienta seu pedido.', text)
        if 'data-voice-id=' in text:
            text = text.replace('no painel', 'pelo WhatsApp').replace('alinhados no painel', 'alinhados pelo WhatsApp')
        text = re.sub(r'<section\b[^>]*id="painel-de-gravacao"[^>]*>.*?</section>', '<section class="panel-section" id="painel-de-gravacao"><div class="panel-shell"><h2>Vamos preparar seu áudio?</h2><p class="panel-intro">Envie seu texto pelo WhatsApp, informe onde o áudio será usado e o prazo desejado. Nossa equipe ajuda na escolha da voz e do serviço e orienta a compra.</p><p class="panel-note">O Painel de Gravação continua disponível no menu superior para clientes que desejam comprar créditos, enviar e acompanhar pedidos e baixar as gravações.</p><div class="panel-actions"><a class="panel-primary" href="'+WHATSAPP+'" data-cta="pedido_whatsapp">Fazer pedido pelo WhatsApp</a></div><p class="panel-note">Atendimento pelo WhatsApp de segunda a sexta, das 08h às 18h. O prazo de entrega depende do roteiro, do serviço e da disponibilidade do locutor.</p></div></section>', text, flags=re.S)
        text = re.sub(r'<section\b[^>]*id="como-funciona"[^>]*>.*?</section>', '<section class="panel-section focus-process" id="como-funciona"><div class="panel-shell"><h2>Seu áudio começa com uma conversa</h2><p>Conte o que você precisa e receba orientação para fazer seu pedido.</p><ol class="focus-steps"><li><strong>Fale pelo WhatsApp</strong><span>Envie seu roteiro e informe onde o áudio será usado e quando precisa receber.</span></li><li><strong>Escolha a voz e o serviço</strong><span>Nossa equipe ajuda a escolher entre Locução Off e Spot Comercial e confirma disponibilidade, valor e prazo.</span></li><li><strong>Receba orientação para comprar</strong><span>Orientamos a compra de créditos e o envio do pedido no Painel de Gravação.</span></li><li><strong>Receba sua gravação</strong><span>Acompanhe o pedido e baixe o áudio pelo painel. Se precisar de ajuda, fale com nossa equipe.</span></li></ol><div class="panel-actions"><a class="panel-primary" href="'+WHATSAPP+'" data-cta="como_funciona_whatsapp">Começar pelo WhatsApp</a></div><p class="panel-note">Já usa o painel? O acesso continua no menu superior. Os tutoriais seguem disponíveis para consultar as etapas.</p></div></section>', text, flags=re.S)
        # A second hero action should help evaluation instead of repeating the same contact.
        text = re.sub(r'<a class="btn btn-light"[^>]*data-cta="home_acessar_painel"[^>]*>.*?</a>', '<a class="btn btn-light" href="/vozes/">Ouvir vozes</a>', text, flags=re.S)
        # Preserve voice context in static and regenerated profile/featured links.
        if 'data-cta="perfil_escolher"' in text:
            name = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
            if name:
                from urllib.parse import quote
                from html import unescape
                voice = unescape(re.sub(r'<[^>]+>', '', re.sub(r'<(?:span|em)\b[^>]*>.*?</(?:span|em)>', '', name[1], flags=re.S))).strip()
                url = 'https://wa.me/5527996529832?text='+quote('Olá! Vi o perfil de '+voice+' no site A Locução. Quero confirmar a disponibilidade e fazer um pedido.')
                text = re.sub(r'<a\b[^>]*data-cta="perfil_escolher"[^>]*>.*?</a>', '<a class="btn-wa" href="'+url+'" data-cta="perfil_escolher">Pedir esta voz pelo WhatsApp</a>', text, flags=re.S)
    # Contact and footer wording must match the main conversion on every page.
    text = text.replace('Falar com o suporte pelo WhatsApp', 'Fazer pedido pelo WhatsApp').replace('Suporte<small>WhatsApp', 'Faça seu pedido<small>WhatsApp')
    text = re.sub(r'src="(/assets/(?:site|voice-bank|voice-profile|featured-voices)\.js)(?:\?[^"]*)?"', r'src="\1?v=20261005-voice-choice"', text)
    # Keep the floating sales button concise, without attendance hours.
    text = re.sub(r'(<a\b[^>]*class="panel-help-link"[^>]*>).*?(</a>)', lambda m: re.sub(r'<span>.*?</span>', '<span>Faça seu pedido pelo WhatsApp</span>', re.sub(r'aria-label="[^"]*"', 'aria-label="Faça seu pedido pelo WhatsApp"', m[0]), flags=re.S), text, flags=re.S)
    if saved:
        saved = re.sub(r'<a class="al-login"[^>]*>.*?</a>', '<a class="al-login" href="/painel/" data-cta="cabecalho_painel">Painel de Gravação</a>', saved, flags=re.S)
        saved = re.sub(r'<a class="al-header-cta[^"\n]*"[^>]*>.*?</a>', '<a class="al-header-cta" href="'+WHATSAPP+'" data-cta="cabecalho_whatsapp">Falar pelo WhatsApp</a>', saved, flags=re.S)
        text = text.replace('__SALES_HEADER__', saved)
    return text

if __name__ == '__main__':
    root = Path(__file__).resolve().parent.parent
    count = 0
    for path in root.rglob('*.html'):
        if any(part.startswith('.') or part in ('node_modules','_site') for part in path.relative_to(root).parts): continue
        old = path.read_text(); new = normalize_whatsapp(old)
        if new != old: path.write_text(new); count += 1
    print('WhatsApp sales paths updated:', count)
