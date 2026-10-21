#!/usr/bin/env python3
"""Idempotent commercial copy pass. Preserve SEO, URLs, technical IA identifiers and audio."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
DISCLOSURE='Vozes Naturais são vozes geradas por inteligência artificial, com sonoridade natural. Locução Off por R$ 8,50 e produção completa por R$ 19,00, por até 40 segundos. Locução estimada em até 10 minutos. Pedidos exclusivamente pelo WhatsApp.'
changed=[]
for p in ROOT.rglob('*.html'):
 if any(x.startswith('.') for x in p.relative_to(ROOT).parts): continue
 s=p.read_text(); old=s
 # Only short presentation labels; informative prose and metadata retain technology terms.
 def label(m):
  return m[1]+m[2].replace('Vozes IA Naturais','Vozes Naturais').replace('Vozes IA naturais','Vozes Naturais').replace('Vozes IA','Vozes Naturais').replace('vozes IA','Vozes Naturais').replace('Voz IA','Voz Natural')+m[3]
 s=re.sub(r'(<(?:a|h[1-3]|button|small)\b[^>]*>)([^<>]*)(</(?:a|h[1-3]|button|small)>)',label,s)
 s=s.replace('Com voz IA ·', 'Com Vozes Naturais ·')
 s=s.replace('Com voz IA.', 'Com Vozes Naturais.').replace('Com voz IA. Com voz humana:', 'Com Vozes Naturais. Com voz humana:')
 s=s.replace('Escolha uma voz humana ou sintética conforme seu projeto.', 'Escolha entre Vozes Naturais e locutores profissionais conforme seu projeto.')
 route=p.relative_to(ROOT).as_posix()
 if route=='index.html':
  s=re.sub(r'<h1\b[^>]*>.*?</h1>','<h1>Sua locução pronta com qualidade e agilidade.</h1>',s,count=1,flags=re.S)
  s=s.replace('Fazer pedido online','Pedir voz humana na Central').replace('Já sou cliente — Acessar painel','Já sou cliente — Central de Vozes Humanas')
 if route=='vozes/index.html':
  s=s.replace('Ouça as demonstrações, encontre o estilo que combina com sua campanha e escolha entre locutores humanos e vozes IA naturais. Consulte o prazo e envie seu pedido pelo WhatsApp.', 'Escolha entre Vozes Naturais e Locutores Profissionais. Ouça, compare e siga para o canal de pedido da categoria escolhida.')
  s=re.sub(r'<h1\b[^>]*>.*?</h1>','<h1>Encontre a voz ideal para seu comercial</h1>',s,count=1,flags=re.S)
 if route=='vozes-ia/index.html':
  s=re.sub(r'<h1\b[^>]*>.*?</h1>','<h1>Vozes Naturais para Comerciais e Anúncios</h1>',s,count=1,flags=re.S)
  s=s.replace('Sua próxima locução pode ter a voz perfeita. E custar menos.','Qualidade, naturalidade e agilidade para sua produção.')
  s=s.replace('Por que escolher Voz Natural?', 'Por que escolher Vozes Naturais?')
 # Visible disclosure above category pricing/CTA, outside cards; do not duplicate on reruns.
 if ('data-business-positioning' in s or route=='vozes-ia/index.html') and not route.startswith('perfil-locutor-') and 'data-natural-disclosure' not in s:
  h=re.search(r'</h1>',s)
  if h:s=s[:h.end()]+'<p data-natural-disclosure class="natural-disclosure">'+('Alternativa disponível: ' if route in {'locucao-off/index.html','producao-para-igrejas/index.html','gravacao-off-e-producao/index.html','producao-para-supermercados/index.html'} else '')+DISCLOSURE+'</p>'+s[h.end():]
 if 'data-natural-disclosure' in s and '/assets/natural-positioning.css' not in s:
  s=s.replace('</head>','<link rel="stylesheet" href="/assets/natural-positioning.css">\n</head>',1)
 # Explain the existing operational destination, never imply synthesis inside the panel.
 s=s.replace('>Fazer pedido online<','>Pedir voz humana na Central<')
 if s!=old:p.write_text(s);changed.append(route)
print('Natural positioning updated:',len(changed))
