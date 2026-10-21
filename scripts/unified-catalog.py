#!/usr/bin/env python3
"""Shared, crawlable voice lists; human data is refreshed by the scheduled sync."""
from pathlib import Path
import html, json, re
from urllib.parse import quote
ROOT = Path(__file__).resolve().parent.parent
VERSION = '20261021-landings'
HUMAN_LANDINGS = {'/off-comercial/','/locucao-off/','/producao-para-igrejas/','/gravacao-off-e-producao/','/producao-para-supermercados/','/spot-black-friday/'}
TABBED_LANDINGS = {'/spot-comercial/','/locucao-off/','/producao-para-igrejas/','/gravacao-off-e-producao/','/producao-para-supermercados/'}
def select_humans(voices, origin):
    if origin not in HUMAN_LANDINGS and origin not in TABBED_LANDINGS: return voices
    preferred = {'Varejo','Impacto','Animada'} if origin in {'/producao-para-supermercados/','/spot-black-friday/','/off-comercial/','/spot-comercial/'} else {'Padrão'}
    voices = [v for v in voices if v.get('audio') and v.get('photo') and v.get('name','').strip().lower() != 'teste']
    return sorted(voices, key=lambda v: -len(preferred.intersection(v.get('styles',[]))))[:10]
def esc(value): return html.escape(str(value), quote=True)
def rows(kind):
    if kind == 'human':
        return json.loads((ROOT/'assets/voices-catalog.json').read_text())['voices']
    return [dict(v, type=v['gender'], styles=v['tags'], photo='/assets/vozes-ia/images/'+v['id']+'.webp', audio='/assets/vozes-ia/audio/'+v['audio'] if v.get('audio') else '') for v in json.loads((ROOT/'data/vozes-ia.json').read_text())]
def row(v, kind, origin):
    name=v['name'];type_label='IA' if kind=='ia' else 'humana'
    message=f'Olá! Gostei da voz {type_label} {name} no site A Locução e gostaria de solicitar uma gravação. Origem: https://alocucao.com.br{origin}. Podem me orientar?'
    photo=f'<img src="{esc(v["photo"])}" alt="{esc("Retrato ilustrativo da voz IA " if kind=="ia" else "Perfil do locutor ")}{esc(name)}" width="56" height="56" loading="lazy" decoding="async">' if v.get('photo') else f'<span>{esc(name[:1])}</span>'
    styles=v.get('styles',[]);description=v.get('description') or ('Interpretações disponíveis: '+', '.join(styles)+'.' if styles else 'Ouça a demonstração para conhecer o estilo desta voz.')
    media=(f'<button class="uv-play" type="button" aria-label="Ouvir {esc(name)}">▶ Ouvir</button><audio class="uv-audio" hidden controls preload="none" data-src="{esc(v["audio"])}" data-voice="{esc(name)}" aria-label="Demonstração de {esc(name)}"></audio>' if v.get('audio') else '<span class="uv-pending">Demonstração em breve</span>')
    if v.get('audio') and v.get('additional_demos'):
        options='<option value="'+esc(v['audio'])+'">Demonstração original</option>'
        for demo in v['additional_demos']:
            options+='<option value="/assets/vozes-ia/audio/'+esc(demo['audio'])+'">'+esc(demo['label'])+'</option>'
        media='<label class="uv-demo-label">Demonstração<select class="uv-demo-select">'+options+'</select></label>'+media
    status='● Online' if kind=='ia' else 'Disponibilidade sob consulta'
    return f'''<article class="uv-row" data-id="{esc(v['id'])}" data-name="{esc(name)}" data-gender="{esc(v.get('type',''))}" data-styles="{esc('|'.join(styles))}"><div class="uv-avatar">{photo}</div><div class="uv-identity"><h3>{esc(name)}{' <small>Voz IA</small>' if kind=='ia' else ''}</h3><p class="uv-meta">{esc(v.get('type',''))} · {esc(v.get('style') or ' · '.join(styles))}</p><p class="uv-description">{esc(description)}</p><span class="uv-status{' uv-online' if kind=='ia' else ''}">{status}</span></div><div class="uv-controls">{media}<a class="uv-choose" href="https://wa.me/5527996529832?text={quote(message)}" target="_blank" rel="noopener noreferrer" data-cta="unified_{kind}_{esc(v['id'])}" data-voice-name="{esc(name)}" data-voice-kind="{kind}">Escolher esta voz</a></div><p class="uv-error" hidden role="status">Não foi possível carregar a demonstração. Solicite o áudio pelo WhatsApp.</p></article>'''
def render_catalog(mode='both', origin='/vozes/'):
    # The Banco de Vozes route is exclusively human, including future rebuilds.
    if origin in TABBED_LANDINGS: mode = 'both'
    elif origin == '/vozes/' or origin in HUMAN_LANDINGS: mode = 'human'
    if origin == '/locucao-ia/': mode = 'ia'
    kinds=['human','ia'] if mode=='both' else [mode]
    prefix='uv-'+re.sub('[^a-z0-9]+','-',origin.lower()).strip('-')
    tabs=f'<div class="uv-tabs" role="tablist" aria-label="Tipo de voz">'+''.join(f'<button type="button" role="tab" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" aria-controls="{prefix}-{k}" data-tab="{k}">{"Vozes Humanas" if k=="human" else "Vozes IA"}</button>' for i,k in enumerate(kinds))+'</div>' if mode=='both' else ''
    panels=[]
    for kind in kinds:
        voices=select_humans(rows(kind),origin) if kind=='human' else rows(kind);styles=sorted(set(s for v in voices for s in v.get('styles',[])))
        labels=['Masculina','Feminina','Personagem'];labels=[x for x in labels if any(v.get('type')==x for v in voices)]
        title='Locutores humanos' if kind=='human' else 'Vozes IA'
        prices='Off R$ 11,90 · Produzida R$ 29,90' if kind=='human' else 'Off R$ 8,50 · Produzida R$ 19,00'
        note='Catálogo atualizado automaticamente pela fonte oficial. Confirme a disponibilidade e o prazo ao pedir.' if kind=='human' else 'Imagens ilustrativas utilizadas para representar os perfis das vozes IA. Online significa disponível para solicitação.'
        panels.append(f'''<section class="uv-panel" id="{prefix}-{kind}" data-kind="{kind}" aria-label="{title}"><div class="uv-panel-head"><span class="uv-category">{'Profissionais de locução' if kind=='human' else 'Inteligência artificial'}</span><h2>{title}</h2><p class="uv-prices">{prices}<small> por locução de até 40 segundos</small></p></div><div class="uv-filters" hidden><label>Buscar voz<input class="uv-search" type="search" placeholder="Nome, estilo ou característica…" autocomplete="off"></label><div><label>Gênero<select class="uv-gender"><option value="">Todos</option>{''.join('<option>'+esc(x)+'</option>' for x in labels)}</select></label><label>Estilo<select class="uv-style"><option value="">Todos os estilos</option>{''.join('<option>'+esc(s)+'</option>' for s in styles)}</select></label><button type="button" class="uv-clear">Limpar</button></div></div><p class="uv-count" role="status" aria-live="polite">{len(voices)} vozes no catálogo</p><p class="uv-sync">{note}</p><div class="uv-list">{''.join(row(v,kind,origin) for v in voices)}</div><p class="uv-empty" hidden>Nenhuma voz encontrada. Tente outro termo ou limpe os filtros.</p><button class="uv-more" type="button" hidden>Mostrar mais vozes</button><a class="uv-full" href="{'/locutores/' if kind=='human' else '/vozes-ia/'}">{'Conhecer os locutores humanos' if kind=='human' else 'Conhecer as vozes IA'} →</a></section>''')
    footnote = 'Escolha um locutor humano e confirme o serviço, a disponibilidade e o prazo com a equipe antes de pedir.' if mode == 'human' else 'Escolha uma voz IA e confirme o serviço e o prazo com a equipe. Os retratos são ilustrativos.' if mode == 'ia' else 'Escolha uma voz humana ou sintética conforme seu projeto. Confira o serviço e o prazo com a equipe antes de confirmar. Os retratos de IA são ilustrativos e representam perfis sintéticos.'
    result = '<!-- unified-catalog:start --><div class="uv-catalog" data-mode="'+mode+'" data-active="'+kinds[0]+'" data-origin="'+esc(origin)+'">'+tabs+'<div class="uv-panels">'+''.join(panels)+'</div><p class="uv-footnote">'+footnote+'</p></div><!-- unified-catalog:end -->'
    if origin in TABBED_LANDINGS:
        result = result.replace('class="uv-catalog"', 'class="uv-catalog" data-layout="tabs"').replace('>Vozes IA</button>', '>Vozes IA Naturais</button>').replace('<h2>Locutores humanos</h2>', '<h2>Locutores humanos profissionais</h2>').replace('<h2>Vozes IA</h2>', '<h2>Vozes IA naturais</h2>')
    return result
def install_assets(text):
    version = VERSION + '-commercial' if 'data-commercial-refresh=' in text else VERSION
    for filename,tag in [('unified-voices.css',f'<link rel="stylesheet" href="/assets/unified-voices.css?v={version}">'),('unified-voices.js',f'<script src="/assets/unified-voices.js?v={version}" defer></script>')]:
        text=re.sub(r'(/assets/'+re.escape(filename)+r')(?:\?[^"\s<>]*)?',lambda m:m[1]+'?v='+version,text)
        if '/assets/'+filename not in text:text=text.replace('</head>',tag+'\n</head>',1)
    return text
def refresh():
    count=0
    for p in ROOT.rglob('*.html'):
        if any(x.startswith('.') for x in p.relative_to(ROOT).parts):continue
        text=p.read_text()
        if '<!-- unified-catalog:start -->' not in text:continue
        mode=re.search(r'class="uv-catalog"[^>]*data-mode="(both|human|ia)"',text)[1]
        origin=re.search(r'class="uv-catalog"[^>]*data-origin="([^"]+)"',text)[1]
        new=re.sub(r'<!-- unified-catalog:start -->.*?<!-- unified-catalog:end -->',lambda _:render_catalog(mode,html.unescape(origin)),text,flags=re.S)
        new=install_assets(new)
        if text!=new:p.write_text(new);count+=1
    print(f'Unified catalogs refreshed: {count}')
if __name__=='__main__':refresh()
