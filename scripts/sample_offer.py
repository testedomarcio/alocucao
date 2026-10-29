"""Focused sample offer, limited to explicitly eligible first-party voices and pages."""
import html,json,re
from urllib.parse import quote
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
E=html.escape
CONFIG=json.loads((ROOT/'data/sample-availability.json').read_text())
VOICES={v['slug']:v for v in json.loads((ROOT/'data/new-voices.json').read_text())}
assert set(CONFIG['voices']) <= set(VOICES), 'Unknown sample voice'
ELIGIBLE={s:VOICES[s] for s,state in CONFIG['voices'].items() if state.get('exclusive') is True and state.get('accepting_orders') is True}
GENERAL='Olá! Gostaria de solicitar uma amostra gratuita do meu texto com uma das vozes exclusivas da A Locução.'
def button(label='🎧 Solicitar minha amostra grátis',voice=None,service='',css='btn'):
 message=('Olá! Gostaria de solicitar uma amostra personalizada gratuita com a voz '+voice['name']+'.') if voice else ('Olá! Gostaria de solicitar uma amostra gratuita de '+service+' do meu texto com uma das vozes exclusivas da A Locução.') if service else GENERAL
 return '<a class="'+css+'" href="https://wa.me/5527996529832?text='+quote(message,safe='')+'" data-cta="solicitar_amostra" data-voice-name="'+E(voice['name'] if voice else '')+'" data-service="'+E(service)+'">'+E(label)+'</a>'
def status():
 return '<p class="sample-availability"><span aria-hidden="true"></span>Disponível para pedidos</p>'
def conditions(service=''):
 production='<p>O formato da prévia será definido conforme o projeto; trilha sonora, efeitos e produção completa não estão garantidos na amostra.</p>' if service=='Produção Completa / Spot Comercial' else ''
 return '<details class="sample-conditions"><summary>Como funciona a amostra gratuita?</summary><div><p>Exclusiva para as vozes habilitadas da A Locução. Grátis e sem obrigação de contratação. A amostra pode ser parcial conforme a extensão do texto; a preparação de uma demonstração completa fica a critério da equipe.</p>'+production+'<p>A prévia poderá conter marca d’água sonora de proteção. O material demonstrativo não poderá ser utilizado comercialmente sem contratação e autorização.</p><p>As amostras são preparadas mediante solicitação, com formato e prazo combinados pela equipe. Atendimento de segunda a sexta, 08h às 18h, e sábado, 08h às 12h, no horário de Brasília. Você pode enviar seu pedido fora desses horários; o retorno ocorre durante o atendimento, sem promessa de preparação imediata.</p><p>“Disponível para pedidos” indica elegibilidade para novas solicitações; não é um status de pessoa conectada ou de gravação em tempo real.</p></div></details>'
def block(service='',voice=None):
 if voice:
  return '<aside class="sample-profile">'+status()+'<h3>Gostou desta voz? Ouça seu próprio texto!</h3><p>Solicite uma amostra personalizada gratuita, sem compromisso.</p>'+button('🎧 Solicitar amostra com esta voz',voice)+conditions()+'</aside>'
 title='OUÇA SUA LOCUÇÃO ANTES DE CONTRATAR!'
 text='Escolha uma das nossas vozes exclusivas e solicite uma amostra personalizada do seu texto. Você ouve como ficará sua locução antes de decidir. Grátis e sem compromisso!'
 if service=='Locução Off':
  title='Quer saber como seu texto ficará na voz escolhida?'
  text='Solicite uma amostra gratuita de Locução Off com uma das nossas vozes exclusivas. Ouça antes de contratar!'
 elif service:
  title='Ouça uma prévia do seu comercial antes de contratar!'
  text='Escolha uma voz exclusiva e solicite uma amostra personalizada. Descubra como sua mensagem pode ganhar vida com uma produção profissional.'
 return '<section class="section sample-offer" aria-labelledby="sample-heading"><div class="wrap"><div class="sample-panel"><div><span class="eyebrow">Amostra personalizada · Grátis e sem compromisso</span><h2 id="sample-heading">'+title+'</h2><p>'+text+'</p></div><div class="sample-convert">'+button(service=service)+'<p class="note">Preparada pela equipe, mediante solicitação.</p></div>'+conditions(service)+'</div></div></section>'
def enhance(path,body):
 profile=path.split('/',1)[1] if path.startswith('locutores/') else None
 enabled=path in ('','vozes','locucao-off','spot-comercial') or profile in ELIGIBLE
 if not enabled:return body,False
 # Cards retain their audio, hiring button, profile link, ratings, and work controls.
 def card(m):
  markup=m[0];slug=re.search(r'href="/locutores/([^/]+)/"',markup)[1]
  if slug not in ELIGIBLE:return markup
  v=ELIGIBLE[slug]
  markup=re.sub(r'(<p class="voice-style">.*?</p>)',lambda x:x[0]+status(),markup,count=1)
  return markup.replace('<div class="voice-actions">','<div class="sample-card-link">'+button('Solicitar amostra grátis',v,css='mini-link')+'</div><div class="voice-actions">',1)
 body=re.sub(r'<article class="voice-card".*?</article>',card,body,flags=re.S)
 if profile in ELIGIBLE:
  # Place after the demo players, before the existing work link.
  marker=re.search(r'<(?:a|button)[^>]*class="recent-work-link"',body)
  body=body[:marker.start()]+block(voice=ELIGIBLE[profile])+body[marker.start():] if marker else body
 elif path=='':
  body=body.replace('<div class="actions">','<div class="sample-hero-copy"><h2>Sua locução, do jeito que você imaginou.</h2><p>Escolha sua voz, solicite uma amostra gratuita do seu texto e contrate com mais confiança.</p>'+button('Ouvir meu texto grátis',css='btn secondary')+'<p class="note">Com as vozes exclusivas habilitadas. Preparação mediante solicitação.</p></div><div class="actions">',1)
  benefits='<div class="sample-benefits"><article><h3>🎧 Ouça antes de contratar</h3><p>Solicite uma amostra personalizada e conheça a interpretação do seu texto.</p></article><article><h3><span class="sample-dot" aria-hidden="true"></span> Vozes disponíveis para pedidos</h3><p>Encontre vozes exclusivas prontas para receber seu pedido.</p></article><article><h3>✓ Contrate com confiança</h3><p>Avalie a amostra e decida sem compromisso.</p></article></div>'
  offer=block().replace('</div></div></section>',benefits+'</div></div></section>')
  body=body.replace('</section>','</section>'+offer,1)
 else:
  service={'locucao-off':'Locução Off','spot-comercial':'Produção Completa / Spot Comercial'}.get(path,'')
  body=body.replace('</section>','</section>'+block(service),1)
 return body,True
