#!/usr/bin/env python3
"""Add static, accessible order choices without rewriting existing commercial CTAs."""
from pathlib import Path
from html.parser import HTMLParser
import re
REGISTER='https://vozes.alocucao.com.br/painel/cadastro'
PANEL='https://vozes.alocucao.com.br/painel/'
ONLINE=f'<a class="hybrid-online" href="{REGISTER}" data-cta="online_order">Fazer pedido online</a>'
LOGIN=f'<a href="{PANEL}" data-cta="client_login">Já sou cliente — Acessar painel</a>'
class Nodes(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=False); self.nodes=[];self.stack=[];self.starts=[0]
        for m in re.finditer('\n',text):self.starts.append(m.end())
        self.text=text;self.feed(text)
    def pos(self):
        l,c=self.getpos();return self.starts[l-1]+c
    def handle_starttag(self,t,a):
        n={'tag':t,'attrs':dict(a),'start':self.pos(),'openend':self.pos()+len(self.get_starttag_text()),'end':None,'parent':self.stack[-1] if self.stack else None}
        self.nodes.append(n)
        if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'):self.stack.append(n)
        else:n['end']=n['openend']
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i]['tag']==t:
                self.stack[i]['close']=self.pos();self.stack[i]['end']=self.text.find('>',self.pos())+1;del self.stack[i:];break
    def handle_startendtag(self,t,a):
        self.handle_starttag(t,a)
        if self.stack and self.stack[-1]['tag']==t:self.stack.pop()
def ancestors(n, tag):
    while n:
        if n['tag']==tag:return n
        n=n['parent']
def normalize_hybrid(text):
    if '<body' not in text or re.search(r'http-equiv=["\']refresh',text,re.I):return text
    # Marking also makes historical commerce normalizers leave this strategy intact.
    text=re.sub(r'<body\b(?![^>]*data-order-channels)', '<body data-order-channels="dual"',text,count=1)
    text=text.replace('https://vozes.alocucao.com.br/painel/entrar',PANEL)
    parsed=Nodes(text);edits=[]
    for n in parsed.nodes:
        a=n['attrs'];cl=a.get('class','').split()
        if n['tag']=='div' and 'al-menu' in cl and n.get('close') and 'Área do Cliente' not in text[n['openend']:n['close']]:
            edits.append((n['close'],n['close'],f'<a class="hybrid-client" href="{PANEL}" data-cta="header_client">Área do Cliente</a>'))
        if n['tag']=='header' and 'al-header' not in cl and n.get('close') and 'Área do Cliente' not in text[n['start']:n['end']]:
            # Focused campaign headers retain their current layout.
            containers=[x for x in parsed.nodes if x['parent'] is n and x['tag'] in ('div','nav') and x.get('close')]
            x=containers[0] if containers else n
            edits.append((x['close'],x['close'],f'<a class="hybrid-client" href="{PANEL}" data-cta="header_client">Área do Cliente</a>'))
        if n['tag']=='h2' and n.get('end') and text[n['openend']:n.get('close',0)] in ('Pedidos e atendimento','Pedidos e suporte'):
            parent=n['parent'];content=text[parent['start']:parent['end']]
            if 'data-cta="footer_client"' not in content:edits.append((n['end'],n['end'],f'<a href="{PANEL}" data-cta="footer_client">Área do Cliente — Acessar painel</a>{ONLINE}'))
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    # Add choices only to commercial content; legal, editorial and tutorial pages keep navigation only.
    parsed=Nodes(text)
    canon=re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]+)"',text)
    path=(canon[1].replace('https://alocucao.com.br','') if canon else '')
    informational=path.startswith(('/blog','/tutoriais','/termos','/politica','/sobre','/avaliacoes','/talentos','/indique-e-ganhe','/painel','/cadastro')) or not canon
    if not informational and 'data-cta="online_order"' not in text.split('<main',1)[-1].split('</main>',1)[0] and 'id="panel-link"' not in text:
        # Existing panel CTA on the packages landing is kept, with commercial wording.
        main=next((n for n in parsed.nodes if n['tag']=='main'),None)
        if main:
            panel=next((n for n in parsed.nodes if n['tag']=='a' and n['attrs'].get('href')==REGISTER and ancestors(n,'main')),None)
            if panel and panel.get('close'):
                text=text[:panel['openend']]+'Fazer pedido online'+text[panel['close']:]
            else:
                actions=next((n for n in parsed.nodes if n['tag']=='div' and set(n['attrs'].get('class','').split()) & {'hero-actions','actions','hero-ctas','hero-buttons'} and ancestors(n,'main') and n.get('close')),None)
                if actions:
                    insert=actions['close']
                    # Online option follows the primary WhatsApp CTA.
                    first=next((n for n in parsed.nodes if n['tag']=='a' and n['parent'] is actions and n.get('end')),None)
                    if first:insert=first['end']
                    text=text[:insert]+ONLINE+text[insert:]
                    pos=actions['end']+len(ONLINE)
                    note='<p class="hybrid-login">'+LOGIN+'</p>'
                    if path in ('/spot-black-friday/','/gravacao-off-e-producao/'):
                        note+='<p class="hybrid-channel-note">Para aproveitar a oferta anunciada, confirme as condições pelo WhatsApp. No painel, confira os valores exibidos antes de pagar; o desconto não é aplicado automaticamente.</p>'
                    text=text[:pos]+note+text[pos:]
                else:
                    # Catalog, prices and individual voice profiles: one unobtrusive option near the end.
                    insert=main.get('close')
                    if insert:text=text[:insert]+'<div class="hybrid-catalog-order"><p>Prefere contratar diretamente pela Central A Locução?</p>'+ONLINE+'<p>'+LOGIN+'</p></div>'+text[insert:]
    text=re.sub(r'<p class="login">Já tem conta\?\s*</p>','',text)
    if 'hybrid-commerce.css' not in text:text=text.replace('</head>','<link rel="stylesheet" href="/assets/hybrid-commerce.css?v=20261016">\n</head>')
    text=re.sub(r'/assets/tracking.js(?:\?[^"\s<>]+)?','/assets/tracking.js?v=20261016-hybrid',text)
    text=re.sub(r'/assets/competitor-landing.js(?:\?[^"\s<>]+)?','/assets/competitor-landing.js?v=20261016-hybrid',text)
    return text
if __name__=='__main__':
    root=Path(__file__).resolve().parent.parent;count=0
    for p in root.rglob('*.html'):
        if any(x.startswith('.') or x in ('node_modules','_site') for x in p.relative_to(root).parts) or p.parent.name=='templates':continue
        old=p.read_text();new=normalize_hybrid(old)
        if new!=old:p.write_text(new);count+=1
    print('Hybrid order choices:',count,'pages updated')
