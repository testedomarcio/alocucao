#!/usr/bin/env python3
"""Preserve the panel registration journey and existing WhatsApp voice controls."""
import re
from pathlib import Path
REGISTER='https://vozes.alocucao.com.br/painel/cadastro'
PANEL='https://vozes.alocucao.com.br/painel/entrar'
HOURS='Gravações de Locução Off todos os dias, até as 22h, inclusive finais de semana e feriados.'
COPY={"Comece seu pedido pelo WhatsApp e receba orientação da nossa equipe.": "Faça o pedido online pelo Painel de Gravação. Se precisar de orientação, o suporte humano está disponível pelo WhatsApp.", "Comece pelo WhatsApp: envie seu texto e confirme os detalhes com nossa equipe.": "Faça pedidos pelo Painel de Gravação e acompanhe cada etapa na sua conta.", "Fale pelo WhatsApp e conte o que você precisa gravar.": "Crie sua conta grátis e complete o cadastro.", "Receba orientação sobre voz, serviço e compra de créditos via PIX ou cartão no painel.": "Compre créditos no painel por PIX ou cartão de crédito, com processamento pelo Mercado Pago.", "Confirme o serviço, a voz, o valor e o prazo com nossa equipe antes de comprar.": "Confira no painel o serviço, a quantidade efetiva de créditos, o valor total e o prazo antes de confirmar seu pedido.", "Nossa equipe ajuda você a escolher o serviço. Locução Off e Produção são cobradas": "Escolha o serviço no painel. Locução Off e Produção são cobradas", "Ouça as demonstrações e confirme a disponibilidade do locutor pelo WhatsApp.": "Ouça as demonstrações e confira a disponibilidade atual do locutor no Painel de Gravação.", "Fale pelo WhatsApp para confirmar a voz disponível e o prazo do seu pedido.": "Escolha no painel o profissional disponível e confira o prazo antes de enviar.", "Confirme a disponibilidade de cada profissional pelo WhatsApp.": "Consulte a disponibilidade de cada profissional no painel.", "Confirme a disponibilidade e o prazo de cada profissional pelo WhatsApp.": "Consulte a disponibilidade e o prazo de cada profissional no painel.", "Fale pelo WhatsApp para começar seu pedido. A gravação depende da disponibilidade e do prazo do locutor escolhido.": "Faça pedidos a qualquer hora pelo painel. A gravação depende da disponibilidade e do prazo do locutor escolhido.", "Nossa equipe orienta a compra de créditos via PIX ou cartão no painel. Confira as condições e o total antes de pagar.": "Compre créditos via PIX ou cartão pelo Mercado Pago. Confira as condições e o total no painel.", "confirme pelo WhatsApp a disponibilidade e o prazo do serviço": "confira no painel a disponibilidade e o prazo do serviço", "e fale pelo WhatsApp para escolher o profissional": "e escolha o profissional no Painel de Gravação", "Fale com nossa equipe pelo WhatsApp. Informe a voz de": "Cadastre-se grátis ou entre na sua conta. Selecione", "e confirme o serviço e o prazo antes de comprar.": "no painel e confira o serviço e o prazo antes de enviar seu pedido.", "Fale com nossa equipe pelo WhatsApp, envie seu texto e receba ajuda para escolher a voz e o serviço ideal. Peça somente a locução ou o spot comercial pronto para divulgar.": "Escolha sua voz, envie seu texto e acompanhe o pedido no Painel de Gravação. Compre somente a locução ou receba o spot comercial pronto para divulgar.", "Converse com nossa equipe antes de comprar. Atendimento pelo WhatsApp de segunda a sexta, das 08h às 18h.": "Cadastro gratuito. Compra de créditos via PIX ou cartão. Suporte humano quando você precisar.", "Conheça os serviços e os preços. Pelo WhatsApp, ajudamos você a escolher a voz e confirmamos os detalhes antes de comprar.": "Conheça o serviço e os preços antes de criar sua conta. Confira as condições do pedido no painel.", "Envie seu texto pelo WhatsApp para confirmar o serviço, a duração, o valor e o prazo antes de comprar.": "Confira o serviço, a duração e o valor no painel antes de enviar o pedido.", "Ouça as demonstrações e fale com nossa equipe pelo WhatsApp. Envie o roteiro, a finalidade e a voz desejada para confirmar a disponibilidade e o prazo. Se estiver em dúvida entre vozes, peça uma indicação.": "Cadastre-se grátis no Painel de Gravação e confira o catálogo disponível para contratação. Escolha o locutor dentro do painel e envie o roteiro, a finalidade e as orientações. As demos e os status são sincronizados com o Painel de Gravação. Se estiver em dúvida entre vozes, peça uma indicação.", "Ao encontrar uma voz, fale com nossa equipe pelo WhatsApp. Informe o nome do locutor, envie o roteiro e explique a finalidade do áudio para confirmar os detalhes do pedido.": "Ao encontrar uma voz, cadastre-se grátis ou entre no Painel de Gravação. Selecione o locutor na sua conta e informe o roteiro, a finalidade do áudio e as orientações antes de enviar o pedido.", "Ouça as vozes e consulte os preços sem cadastro. Para começar seu pedido, envie o texto pelo WhatsApp. Nossa equipe ajuda na escolha do serviço e orienta os próximos passos.": "Ouça as vozes e consulte os preços sem cadastro. Para pedir, crie sua conta grátis, adicione créditos e envie o texto pelo painel. Se precisar de ajuda para escolher o serviço, fale com o suporte.", "O cliente começa pelo WhatsApp, recebe orientação e confirma os detalhes do pedido com nossa equipe. O Painel de Gravação continua disponível para comprar créditos, enviar e acompanhar pedidos e baixar arquivos.": "O cliente pode tirar dúvidas e receber ajuda pelo WhatsApp. Compras, pedidos, acompanhamento e download são realizados pelo painel.", "Para começar seu pedido, fale com nossa equipe pelo WhatsApp.": "Para pedir, cadastre-se grátis no Painel de Gravação.", "Fale pelo WhatsApp para escolher o serviço e a voz e confirmar o prazo antes de comprar.": "Cadastre-se grátis no Painel de Gravação, confira o serviço, a voz e o prazo e acompanhe seu pedido pela sua conta.", "Envie seu texto pelo WhatsApp e conte onde o áudio será usado. Nossa equipe ajuda você a escolher a voz, confirma o serviço e o prazo e orienta os próximos passos. O Painel de Gravação continua disponível pelo menu superior.": "Cadastre-se grátis, adicione créditos, escolha o locutor e envie o roteiro. Acompanhe a produção e baixe o áudio na sua conta.", "Prepare a campanha do seu comércio: envie seu texto pelo WhatsApp e receba ajuda para escolher a voz e o serviço ideal.": "Prepare a campanha do seu comércio: crie sua conta grátis, escolha a voz e faça seu pedido pelo Painel de Gravação. Se precisar de ajuda, nosso suporte está disponível.", "Fale com nossa equipe para começar seu pedido.": "A agilidade pelo WhatsApp pode ser menor que pelo painel.", "Nossa equipe orienta seu pedido pelo WhatsApp.": "Pelo WhatsApp não garantimos a mesma agilidade do Painel de Gravação.", "Comece seu pedido pelo WhatsApp. Nossa equipe atende de segunda a sexta, das 08h às 18h.": "Faça seus pedidos diretamente pelo Painel de Gravação. Precisa de ajuda? Nosso suporte pelo WhatsApp atende de segunda a sexta, das 08h às 18h.", "Comece seu pedido conversando com nossa equipe.": "Seus pedidos são feitos pelo painel.", "confirme disponibilidade e prazo pelo WhatsApp": "confirme disponibilidade e prazo no painel", "Confirme disponibilidade e prazo pelo WhatsApp": "Confira disponibilidade e prazo no painel", "Confirme a disponibilidade e o prazo pelo WhatsApp": "Confira a disponibilidade e o prazo no painel"}
def normalize_whatsapp(text):
    # Compatibility entry point used by the existing generators.
    if re.search(r'http-equiv=["\']refresh',text,re.I):return text
    saved=[]
    def protect(m):
        saved.append(m[0]);return '__PRESERVED_CONTROL_%d__'%(len(saved)-1)
    if 'data-voice-id=' in text or 'id="voice-grid"' in text:
        text=re.sub(r'<main\b[^>]*>.*?</main>',protect,text,flags=re.S)
    text=re.sub(r'<!-- featured-voices:start -->.*?<!-- featured-voices:end -->',protect,text,flags=re.S)
    text=re.sub(r'<a\b[^>]*class=["\'][^"\']*(?:panel-help-link|whatsapp-float|wa-float-button)[^"\']*["\'][^>]*>.*?</a>',protect,text,flags=re.S)
    # The mobile bar belongs to the currently installed floating widget.
    text=re.sub(r'<div\b[^>]*class="(?:mobile-conversion-bar|mobile-bar|sticky-mobile|mobile)"[^>]*>.*?</div>',protect,text,flags=re.S)
    text=re.sub(r'<section\b[^>]*id="identificacao"[^>]*>.*?</section>',protect,text,flags=re.S)
    text=re.sub(r'<section\b[^>]*class="testimonials"[^>]*>.*?</section>',protect,text,flags=re.S)
    def anchor(m):
        tag=m[0]
        if "data-legal-contact" in tag:return tag
        href=re.search(r'href=(["\'])(.*?)\1',tag)
        if not href:return tag
        if re.match(r'https?://(?:wa\.me|(?:api|web)\.whatsapp\.com)(?:/|$)',href[2]):
            if re.search(r'(?:perfil_escolher|voz_destaque_|featured-choose|class="choose")',tag):return tag
            tag=tag[:href.start(2)]+REGISTER+tag[href.end(2):]
            tag=re.sub(r'(<a\b[^>]*>).*?(</a>)',r'\1Criar conta grátis\2',tag,flags=re.S)
            tag=re.sub(r'(?:aria-label|title)="[^"]*"',lambda m:m[0].split('=')[0]+'="Criar conta grátis"',tag)
            tag=re.sub(r'data-cta="([^"]+)"',lambda m:'data-cta="'+m[1].replace('whatsapp','cadastro')+'"',tag)
            tag=tag.replace(' data-panel-support','')
        if 'class="al-login"' in tag:tag=re.sub(r'href=(["\']).*?\1','href="'+PANEL+'"',tag)
        return tag
    text=re.sub(r'<a\b[^>]*>.*?</a>',anchor,text,flags=re.S)
    for old,new in sorted(COPY.items(),key=lambda x:len(x[0]),reverse=True):text=text.replace(old,new)
    replacements={
      'Vozes humanas · atendimento pelo WhatsApp':'Vozes humanas · pedidos pelo Painel de Gravação',
      'Seu áudio começa com uma conversa':'Peça seu áudio pelo painel: simples e fácil',
      'Conte o que você precisa e receba orientação para fazer seu pedido.':'Crie sua conta grátis e faça seu pedido em poucos passos, direto pelo Painel de Gravação.',
      'Envie o texto pelo WhatsApp.':'Crie sua conta grátis e envie o texto pelo painel.',
      'Envie seu texto pelo WhatsApp':'Envie seu texto pelo Painel de Gravação',
      'Envie o roteiro pelo WhatsApp':'Envie o roteiro pelo Painel de Gravação',
      'Envie o texto e receba orientação.':'Crie sua conta grátis, escolha a voz e envie seu texto pelo painel.',
      'Já usa o painel? O acesso continua no menu superior. Os tutoriais seguem disponíveis para consultar as etapas.':'Já tem uma conta? Acesse o painel. Se precisar de ajuda, consulte nossos tutoriais.',
      'Dúvidas antes de começar?':'Comece pelo painel:',
      'O Painel de Gravação continua disponível no menu superior para clientes que desejam comprar créditos, enviar e acompanhar pedidos e baixar as gravações.':'No Painel de Gravação você compra créditos, envia e acompanha pedidos e baixa suas gravações.',
      'Temos locutores de plantão todos os dias, inclusive finais de semana e feriados.':HOURS,
      'Atendimento humano pelo WhatsApp':'Pedidos pelo Painel de Gravação',
      'Atendimento pelo WhatsApp':'Pedidos pelo Painel de Gravação',
    }
    for old,new in replacements.items():text=text.replace(old,new)
    text=re.sub(r'(?:fale com nossa equipe e ){2,}','',text,flags=re.I)
    text=re.sub(r'(<div><h2>Pedidos e atendimento</h2>.*?<p>).*?(</p></div>)',lambda m:m[1]+'Pedidos pelo painel 24h. '+HOURS+' Suporte humano de segunda a sexta, das 08h às 18h.'+m[2],text,flags=re.S)
    text=re.sub(r'<a class="panel-secondary" href="'+re.escape(REGISTER)+r'"[^>]*>Criar conta grátis</a>','<a class="panel-secondary" href="'+PANEL+'" data-cta="painel_acessar">Já tenho conta</a>',text)
    steps='<ol class="focus-steps"><li><strong>1. Crie sua conta grátis</strong><span>Cadastre-se no Painel de Gravação e complete seus dados. É simples e gratuito.</span></li><li><strong>2. Compre seus créditos</strong><span>Escolha Locução Off ou Produção e pague por PIX ou cartão. Os créditos são liberados automaticamente após a confirmação do pagamento.</span></li><li><strong>3. Escolha a voz e envie o texto</strong><span>Selecione o locutor, informe seu roteiro e as orientações. Confira o serviço, os créditos necessários e o prazo antes de confirmar.</span></li><li><strong>4. Acompanhe e baixe seu áudio</strong><span>Acompanhe o andamento pelo painel e baixe a gravação quando estiver pronta. Se necessário, solicite a correção pela sua conta.</span></li></ol>'
    text=re.sub(r'<ol class="focus-steps">.*?</ol>',lambda _:steps,text,flags=re.S)
    text=text.replace('Cadastro gratuito. Compra de créditos via PIX ou cartão. Suporte humano quando você precisar.','Cadastro grátis. Pedidos pelo painel 24h. '+HOURS)
    text=text.replace('Envie seu texto e receba sugestões de vozes para seu projeto. Confira disponibilidade e prazo pelo WhatsApp antes de confirmar.','Crie sua conta grátis, escolha a voz e envie seu texto pelo painel. Confira a disponibilidade e o prazo antes de confirmar.')
    text=text.replace('Pedidos pelo Painel de Gravação de segunda a sexta, das 08h às 18h. O prazo de entrega depende do roteiro, do serviço e da disponibilidade do locutor.','Pedidos pelo painel 24h. '+HOURS+' Confira a disponibilidade da voz e o prazo no painel.')
    text=text.replace('Envie seu texto pelo Painel de Gravação, informe onde o áudio será usado e o prazo desejado. Nossa equipe ajuda na escolha da voz e do serviço e orienta a compra.','Crie sua conta grátis, compre créditos, escolha a voz e envie seu texto e as orientações. Acompanhe seu pedido e baixe o áudio pelo painel.')
    text=re.sub(r'([Ee]nvie (?:seu|o) (?:texto|roteiro)) pelo WhatsApp',r'\1 pelo Painel de Gravação',text)
    text=text.replace('<strong>Atendimento humano</strong><span>direto no WhatsApp</span>','<strong>Pedido online</strong><span>direto pelo painel</span>')
    for i,value in enumerate(saved):text=text.replace('__PRESERVED_CONTROL_%d__'%i,value)
    return text
if __name__=='__main__':
    root=Path(__file__).resolve().parent.parent
    count=0
    for p in root.rglob('*.html'):
        if any(x.startswith('.') or x in ('node_modules','_site') for x in p.relative_to(root).parts):continue
        old=p.read_text();new=normalize_whatsapp(old)
        if old!=new:p.write_text(new);count+=1
    print('Registration paths updated:',count)
