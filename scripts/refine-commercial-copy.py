#!/usr/bin/env python3
"""Final, context-specific copy refinements; no catalog or tracking changes."""
from pathlib import Path
from html import escape,unescape
import re,json
ROOT=Path(__file__).resolve().parent.parent
Q='Qual é a diferença entre voz humana e voz natural (IA)?'
A='As vozes humanas são gravadas por locutores profissionais, com interpretação, emoção e personalização. As vozes naturais (IA) são geradas por inteligência artificial, com sonoridade realista, agilidade e preços mais acessíveis. Ambas atendem comerciais, anúncios e conteúdos publicitários. A escolha depende do estilo, do orçamento e das necessidades do projeto.'
HUMAN='Nas locuções humanas, o prazo é de 10 a 30 minutos ou de 1 a 2 horas, conforme o status do locutor no catálogo. Confirme a disponibilidade antes do pedido.'
BOTH='A locução com voz natural (IA) tem prazo estimado de até 10 minutos. '+HUMAN+' Para produção completa, considere mais 1 a 2 horas após a conclusão da gravação, para edição e finalização.'
PRODUCED='A produção completa tem prazo estimado de 1 a 2 horas após a conclusão da gravação. A locução com voz natural (IA) leva até 10 minutos. '+HUMAN
OFF='Locução Off é a gravação da voz sem trilha ou efeitos. A produção completa inclui locução, trilha e efeitos sonoros, conforme as características do projeto.'
META={
 'servicos':('Serviços de Locução e Produção de Áudio | A Locução','Locução Off, spots comerciais, URA e narração para vídeos. Ouça as vozes, confira preços e solicite o áudio adequado ao seu projeto.','Locução e produção de áudio para sua comunicação.'),
 'precos':('Preços de Locução Off e Produção Completa | A Locução','Confira preços de locução Off e produção completa por até 40 segundos, com vozes humanas e naturais (IA). Compare os serviços e solicite sua gravação.','Confira os preços de locução e produção de áudio.'),
 'espera-telefonica-ura':('Locução para URA e Espera Telefônica | A Locução','Gravações para URA, PABX e espera telefônica. Ouça as vozes, envie seu roteiro e confirme o formato e o valor para seu sistema.','Locução profissional para URA e espera telefônica.'),
 'locucao-para-video-institucional':('Locução para Vídeos Institucionais e Anúncios | A Locução','Narração profissional para vídeos institucionais, apresentações e anúncios. Escolha a voz e confirme interpretação, formato e prazo da gravação.','A voz certa para seu vídeo institucional.'),
 'spot-para-carro-de-som':('Spot para Carro de Som: Produção Profissional | A Locução','Divulgue suas ofertas com spot para carro de som. Locução, trilha e efeitos para uma mensagem clara. Ouça exemplos e solicite sua produção.','Sua propaganda pronta para o carro de som.'),
 'planos-para-agencias-revenda':('Locução para Agências e Revendedores: Pacotes | A Locução','Locução Off e produção de áudio para agências, produtoras e revendedores. Confira os pacotes de vozes humanas e as opções avulsas com IA.','Locução e produção para agências e revendedores.'),
 'spot-comercial-natal':('Spot de Natal: Locução e Produção Comercial | A Locução','Produza sua campanha de Natal com locução, trilha e efeitos. Ouça os estilos disponíveis, incluindo Papai Noel, e confirme preço e prazo.','Sua campanha de Natal com uma mensagem marcante.'),
 'sobre':('Sobre a A Locução | Produção de Áudio Comercial','Conheça a A Locução: locução profissional e produção de áudio para empresas, agências e produtores, com atendimento online em todo o Brasil.','A voz certa para sua mensagem, do início ao áudio pronto.'),
}
# Each entry updates an existing question; unmatched additions are deliberately limited.
FAQ={
 '':{'Existem opções de gravação rápida?':('Qual é o prazo estimado de entrega?',BOTH)},
 'spot-comercial':{'Qual é o prazo de entrega?':(None,PRODUCED),'Posso escolher a voz?':('Posso ouvir a voz antes de contratar?','Sim. Ouça as demonstrações no catálogo desta página, escolha o estilo e confirme o serviço e o prazo antes de solicitar sua gravação.'),'Qual a diferença entre Locução Off e Spot Comercial?':(None,OFF)},
 'locucao-off':{'Qual é o prazo de entrega?':(None,"Temos locutores que gravam o Off em até 10 minutos, conforme disponibilidade. Outros profissionais possuem prazos diferentes, indicados no catálogo. Confirme a voz e o prazo pelo WhatsApp antes de concluir o pedido. A produção completa tem prazo estimado de 1 a 2 horas após a conclusão da gravação."),'Como o preço é calculado?':(None,"A Locução Off custa R$ 12,00 por crédito de até 40 segundos, independentemente da voz escolhida. Você recebe somente a voz, sem edição, trilha ou efeitos. A produção completa custa R$ 30,00 por crédito. De 41 a 80 segundos, são necessários 2 créditos.")},
 'producao-para-igrejas':{'Qual é o prazo de entrega?':(None,PRODUCED),'O que está incluído nos R$ 29,90?':('O que está incluído na produção completa?','Locução, trilha musical, efeitos, edição e finalização, além da voz Off separada. Por até 40 segundos, a produção custa R$ 29,90 com voz humana ou R$ 19,00 com voz natural (IA).')},
 'producao-para-supermercados':{'Quanto tempo demora para receber minha gravação?':(None,PRODUCED),'Quanto custa uma locução para supermercado?':(None,'Por até 40 segundos, a locução Off custa R$ 11,90 com voz humana ou R$ 8,50 com voz natural (IA). A produção completa custa R$ 29,90 com voz humana ou R$ 19,00 com voz natural (IA).')},
 'off-comercial':{'Qual é o prazo de entrega?':(None,HUMAN)},
 'spot-black-friday':{'Em quanto tempo recebo meu áudio?':(None,HUMAN+' A produção completa tem prazo estimado de 1 a 2 horas após a conclusão da gravação.')},
 'vozes-ia':{'Voz IA substitui a voz humana?':(Q,A),'Quanto tempo demora a gravação?':(None,'A locução com voz natural (IA) tem prazo estimado de até 10 minutos. Para produção completa, a estimativa é de 1 a 2 horas após a gravação. Confirme as condições antes do pedido.'),'Como faço meu pedido pelo WhatsApp?':(None,'Ouça as demonstrações, clique em “Quero esta voz” e envie seu texto pelo WhatsApp. A mensagem identifica a voz escolhida. Nossa equipe confirma o serviço, o valor e o prazo.')},
 'locucao-ia':{'Quanto tempo demora?':(None,'A locução com voz natural (IA) tem prazo estimado de até 10 minutos. A produção completa tem estimativa de 1 a 2 horas após a conclusão da gravação.'),'Como solicitar pelo WhatsApp?':(None,'Ouça as demonstrações, escolha a voz e envie seu texto pelo WhatsApp. Nossa equipe confirma o serviço, o valor e o prazo antes do pedido.')},
 'vozes':{'Como faço meu pedido?':(None,'Escolha a voz no catálogo. Para vozes naturais (IA), o botão abre o WhatsApp com a voz identificada. Para vozes humanas, ele leva à Central de Produção. Confirme o serviço e o prazo antes de concluir.')},
 'locutores':{'Como faço meu pedido?':(None,'Clique em “Quero esta voz” para acessar a Central de Produção e solicitar uma gravação com locutor profissional. Confirme a voz, o serviço e o prazo antes de concluir.')},
}
ADD_DIFFERENCE={'','spot-comercial','locucao-off','producao-para-igrejas','producao-para-supermercados','vozes'}
COPY={
 'Vozes humanas e IA':'Estilos para seu anúncio',
 '✓ Vozes humanas e IA':'✓ Escolha seu estilo de voz',
 'Voz IA':'Voz Natural (IA)',
 'Humanas e IA no mesmo catálogo':'Ouça e escolha sua voz',
 'Vozes humanas e IA no mesmo lugar':'Encontre a voz ideal para seu projeto',
 'Duas opções de voz. Preços claros para escolher.':'Confira os serviços e preços',
 'Vozes humanas e IA para URA':'Uma voz profissional para seu atendimento',
 'Voz Natural ou voz humana?':'Qual modalidade combina com seu projeto?',
}
def plain(v):return unescape(re.sub('<[^>]*>','',v)).strip()
def update(text,route):
 old=text
 text=text.replace('Com Vozes Naturais.', 'Com Vozes Naturais (IA).').replace('Com Vozes Naturais ·', 'Com Vozes Naturais (IA) ·')
 # Label changes only, not educational prose or SEO terms.
 def labels(m):
  body=m[2]
  if plain(body) in COPY:body=COPY[plain(body)]
  body=re.sub(r'\bVozes Naturais\b(?! \(IA\))','Vozes Naturais (IA)',body)
  body=re.sub(r'\bVoz Natural\b(?! \(IA\))','Voz Natural (IA)',body)
  return m[1]+body+m[3]
 text=re.sub(r'(<(?:a|h[1-3]|button|small|span|strong|th|td|em)\b[^>]*>)([^<>]*)(</(?:a|h[1-3]|button|small|span|strong|th|td|em)>)',labels,text)
 # Existing prominent prices stay in their offer blocks; disclosure becomes one clear sentence.
 text=re.sub(r'(<p\b[^>]*data-natural-disclosure[^>]*>).*?</p>',r'\1Vozes Naturais (IA) são geradas por inteligência artificial. Também oferecemos gravações com locutores profissionais.</p>',text,flags=re.S)
 text=text.replace('Vozes humanas e inteligência artificial para mensagens que conectam. Locução off e produção de áudio com atendimento online em todo o Brasil.', 'Locução e produção de áudio para mensagens que conectam. Atendimento online em todo o Brasil.')
 text=text.replace('Valores para vozes IA. Com vozes humanas:', 'Valores com vozes naturais (IA). Com vozes humanas:')
 if route in META:
  title,desc,h1=META[route]
  text=re.sub(r'<title>.*?</title>','<title>'+title+'</title>',text,count=1,flags=re.S)
  text=re.sub(r'<h1\b[^>]*>.*?</h1>','<h1>'+h1+'</h1>',text,count=1,flags=re.S)
  def meta(m):
   tag=m[0];key=re.search(r'(?:name|property)="([^"]+)"',tag)
   if key and key[1] in ['description','og:description','twitter:description','og:title','twitter:title']:
    val=title if key[1].endswith(':title') else desc
    tag=re.sub(r'content="[^"]*"','content="'+escape(val,quote=True)+'"',tag)
   return tag
  text=re.sub(r'<meta\b[^>]*>',meta,text)
 if route=='vozes-ia':text=re.sub(r'<h1\b[^>]*>.*?</h1>','<h1>Vozes Naturais (IA) para Comerciais e Anúncios</h1>',text,count=1,flags=re.S)
 # Existing Q&A only; keep policies, format information and unrelated editorial FAQs intact.
 def faq(m):
  opening,q,rest=m.groups();key=plain(q);value=FAQ.get(route,{}).get(key)
  if not value:return m[0]
  nq,answer=value
  return opening+escape(nq or key)+'</summary><p>'+escape(answer)+'</p></details>'
 text=re.sub(r'(<details\b[^>]*>\s*<summary[^>]*>)(.*?)</summary>(.*?)</details>',faq,text,flags=re.S)
 if route in ADD_DIFFERENCE and Q not in text:
  at=text.rfind('</details>')
  if at>=0:text=text[:at+10]+'<details><summary>'+Q+'</summary><p>'+A+'</p></details>'+text[at+10:]
 # Keep existing FAQ structured data aligned with the visible questions.
 faqs=[(plain(q),plain(a)) for q,a in re.findall(r'<details[^>]*>\s*<summary[^>]*>(.*?)</summary>(.*?)</details>',text,re.S)]
 def schema(m):
  obj=json.loads(m[2]);touched=False
  def visit(v):
   nonlocal touched
   if isinstance(v,dict):
    if v.get('@type')=='FAQPage' and faqs:
     v['mainEntity']=[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs];touched=True
    else:
     for child in v.values():visit(child)
   elif isinstance(v,list):
    for child in v:visit(child)
  visit(obj)
  return m[1]+json.dumps(obj,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+m[3] if touched else m[0]
 if route in FAQ or route in ADD_DIFFERENCE:text=re.sub(r'(<script[^>]*type="application/ld\+json"[^>]*>)(.*?)(</script>)',schema,text,flags=re.S)
 return text
if __name__=='__main__':
 changed=[];reviewed=[]
 for p in ROOT.rglob('*.html'):
  if any(x.startswith('.') for x in p.relative_to(ROOT).parts):continue
  route=p.parent.relative_to(ROOT).as_posix();route='' if route=='.' else route
  text=p.read_text();new=update(text,route);reviewed.append(str(p.relative_to(ROOT)))
  if text!=new:p.write_text(new);changed.append(str(p.relative_to(ROOT)))
 print('Final communication refinements:',len(changed),'of',len(reviewed),'HTML files reviewed')
