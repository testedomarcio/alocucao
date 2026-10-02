#!/usr/bin/env python3
"""Maintain crawlable contextual links without duplicating existing WhatsApp CTAs.

Run from the repository root: python3 scripts/optimize-conversion-paths.py
Optional arguments restrict processing to the supplied HTML paths.
"""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = {
    'locucao-off': 'Locução Off', 'spot-comercial': 'Spot Comercial',
    'spot-black-friday': 'Spot Black Friday', 'spot-comercial-natal': 'Spot de Natal',
    'spot-para-carro-de-som': 'Spot para carro de som',
    'locucao-campanha-politica': 'Locução para campanha política',
    'locucao-para-video-institucional': 'Locução para vídeo institucional',
    'locucao-voz-infantil': 'Locução com voz infantil',
    'espera-telefonica-ura': 'Espera telefônica e URA',
    'vinhetas-para-podcast-e-radio': 'Vinhetas para podcast e rádio',
    'planos-para-agencias-revenda': 'Planos para agências e revenda',
}
MATRIX = {
    'locucao-off-o-que-e': ('locucao-off', 'Entender preços e formatos de locução off'),
    'agencia-de-vozes-locucao-comercial': ('vozes', 'Comparar vozes para sua campanha'),
    'locucao-profissional-como-contratar-locutor': ('vozes', 'Ouvir locutores antes de contratar'),
    'locucao-comercial-publicitaria': ('vozes', 'Escolher uma voz para seu anúncio'),
    'voz-ia-ou-locucao-humana': ('vozes', 'Comparar demonstrações de vozes humanas'),
    'audio-para-campanha-eleitoral': ('locucao-campanha-politica', 'Ver formatos para campanha política'),
    'como-fazer-roteiro-para-carro-de-som': ('spot-para-carro-de-som', 'Conhecer a produção para carro de som'),
    'locucao-para-supermercado': ('spot-comercial', 'Ver a produção de spot comercial'),
    'propaganda-dia-das-criancas': ('spot-comercial', 'Transformar o roteiro em spot comercial'),
    'quanto-custa-um-spot-comercial': ('precos', 'Consultar preços de locução e spot'),
    'roteiro-spot-black-friday': ('spot-black-friday', 'Produzir seu spot de Black Friday'),
    'spot-black-friday': ('spot-black-friday', 'Conhecer o serviço de spot Black Friday'),
}

class Nodes(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.offsets = [0]
        for line in source.splitlines(keepends=True): self.offsets.append(self.offsets[-1] + len(line))
        self.stack, self.nodes = [], []
        self.feed(source)
    def pos(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col
    def handle_starttag(self, tag, attrs):
        if tag in {'div', 'section', 'article', 'main'}:
            self.stack.append({'tag': tag, 'attrs': dict(attrs), 'start': self.pos()})
    def handle_endtag(self, tag):
        if tag not in {'div', 'section', 'article', 'main'}: return
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i]['tag'] == tag:
                node = self.stack.pop(i)
                node['end'] = self.pos() + len(tag) + 3
                self.nodes.append(node)
                break

def marked(kind, content):
    return '\n<!-- contextual-' + kind + ':start -->' + content + '<!-- contextual-' + kind + ':end -->\n'

def links(primary, label, kind):
    route = '/' + primary + '/'
    key = kind.replace('-', '_')
    extra = '<a href="/vozes/" data-cta="'+key+'_vozes">Ouvir e escolher uma voz</a>' if primary != 'vozes' else '<a href="/precos/" data-cta="'+key+'_precos">Consultar preços</a>'
    return '<nav class="contextual-links" aria-label="Próximos passos"><a href="'+route+'" data-cta="'+key+'_principal">'+html.escape(label)+'</a>'+extra+'</nav>'

def optimize(path):
    before = path.read_text(encoding='utf-8')
    source = re.sub(r'\n?<!-- contextual-(?:answer|final):start -->.*?<!-- contextual-(?:answer|final):end -->\n?', '', before, flags=re.S)
    if 'http-equiv="refresh"' in source or '<h1' not in source: return False
    relative = path.relative_to(ROOT)
    if len(relative.parts) < 2: return False
    blog = relative.parts[0] == 'blog' and len(relative.parts) == 3
    slug = relative.parts[-2]
    if blog:
        if slug not in MATRIX: return False
        primary, label = MATRIX[slug]
        nodes = Nodes(source).nodes
        answer = next((n for n in nodes if 'answer-box' in n['attrs'].get('class','').split()), None)
        if not answer: raise ValueError(f'No answer box: {relative}')
        final_boxes = [n for n in nodes if 'conversion-box' in n['attrs'].get('class','').split()]
        # Add the contextual internal link to the existing final CTA; retain its copy and WhatsApp URL.
        if final_boxes:
            last = max(final_boxes, key=lambda n:n['start'])
            source = source[:last['end']-6] + marked('final', links(primary,label,'artigo_final')) + source[last['end']-6:]
        else:
            article = next(n for n in nodes if 'article' in n['attrs'].get('class','').split())
            source = source[:article['end']-10] + marked('final',links(primary,label,'artigo_final')) + source[article['end']-10:]
        source = source[:answer['end']] + marked('answer', links(primary,label,'artigo_resposta')) + source[answer['end']:]
    elif slug in SERVICES or slug.startswith('produtora-de-audio-'):
        nodes = Nodes(source).nodes
        hero = next((n for n in nodes if n['tag']=='section' and 'hero' in n['attrs'].get('class','').split()),None)
        if not hero: raise ValueError(f'No hero: {relative}')
        main = next(n for n in nodes if n['tag']=='main')
        # Preserve existing WhatsApp buttons; reinforce internal exploration at the end.
        source = source[:main['end']-7] + marked('final',links('vozes','Ouvir os locutores disponíveis','servico_final')) + source[main['end']-7:]
        source = source[:hero['end']] + marked('answer',links('vozes','Escolher uma voz para este serviço','servico_resposta')) + source[hero['end']:]
    else: return False
    if '/assets/contextual-cta.css' not in source:
        source = source.replace('</head>', '<link rel="stylesheet" href="/assets/contextual-cta.css">\n</head>', 1)
    # Add the missing breadcrumb to the political service; do not add Service schema to redirect aliases.
    if slug == 'locucao-campanha-politica' and 'BreadcrumbList' not in source:
        schema = {'@context':'https://schema.org','@type':'BreadcrumbList','@id':'https://alocucao.com.br/'+slug+'/#breadcrumb', 'itemListElement':[
            {'@type':'ListItem','position':1,'name':'A Locução','item':'https://alocucao.com.br/'},
            {'@type':'ListItem','position':2,'name':SERVICES[slug],'item':'https://alocucao.com.br/'+slug+'/'}]}
        source = source.replace('</head>', '<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>\n</head>',1)
    if source != before:
        path.write_text(source,encoding='utf-8')
        return True
    return False

if __name__ == '__main__':
    paths = [ROOT / p for p in sys.argv[1:]] if len(sys.argv)>1 else sorted(ROOT.rglob('index.html'))
    changed = [str(p.relative_to(ROOT)) for p in paths if optimize(p)]
    print(json.dumps({'updated':len(changed),'paths':changed},ensure_ascii=False))
