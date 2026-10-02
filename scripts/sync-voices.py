#!/usr/bin/env python3
"""Sync the public catalog, without browser credentials or protection bypasses."""
import hashlib
import json
import os
import re
import tempfile
import urllib.request
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit


SOURCE = 'https://paineldegravacao.com.br/lista-locutores'
API = 'https://paineldegravacao.com.br/!/t_horarios_locutores/?nIDs='
PROVIDER = 'locucao-brasil'
OUTPUT = Path('assets/voices-catalog.json')
STATES = ['Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Distrito Federal','Espírito Santo','Goiás','Maranhão','Mato Grosso','Mato Grosso do Sul','Minas Gerais','Pará','Paraíba','Paraná','Pernambuco','Piauí','Rio de Janeiro','Rio Grande do Norte','Rio Grande do Sul','Rondônia','Roraima','Santa Catarina','São Paulo','Sergipe','Tocantins']
STYLES = ['Caricata','Padrão','Impacto','Animada','Varejo','Política','VSL']


def safe_url(value, hosts):
    parsed = urlsplit(value or '')
    if parsed.scheme != 'https' or parsed.hostname not in hosts or parsed.username or parsed.password:
        raise ValueError('Unexpected public media/profile URL')
    return value


def plain_html(value):
    import html
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", str(value or "")))).strip()


def normalize_name(value):
    text=unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+',' ',text).strip()


def media_url(filename, folder):
    from urllib.parse import quote
    if not isinstance(filename,str) or not re.fullmatch(r'[A-Za-z0-9_. -]+\.(?:mp3|mpeg|wav|jpg|jpeg|png|webp)',filename,re.I) or '..' in filename:
        raise ValueError('Invalid public media filename')
    return 'https://hd.paineldegravacao.com.br/'+folder+'/'+quote(filename)


def parse_catalog(payload):
    data=json.loads(payload) if isinstance(payload,(str,bytes)) else payload
    if not isinstance(data,dict) or not isinstance(data.get('data'),list):raise ValueError('Missing public catalog')
    rows=data['data']
    if len(rows)<40 or len(rows)>1500 or int(data.get('recordsTotal',-1))!=len(rows) or int(data.get('recordsFiltered',-1))!=len(rows):
        raise ValueError('Incomplete or unexpectedly sized public catalog')
    voices=[];seen=set()
    for row in rows:
        native_id=row.get('ID');name=plain_html(row.get('nome'))
        if not isinstance(native_id,int) or native_id<=0 or native_id in seen or not name:raise ValueError('Invalid voice identifier')
        seen.add(native_id)
        raw_styles=str(row.get('estilos') or '')
        parts=re.split(r'<br\s*/?>\s*<b>Informações adicionais:</b>',raw_styles,maxsplit=1,flags=re.I)
        style_text=plain_html(parts[0]);styles=[];languages=['Português']
        # Free-text source descriptions are not suitable as hundreds of filter categories.
        patterns=[
            ('Padrão',r'\b(?:padrao|padao)\b'),('Impacto',r'\bimpacto\b'),
            ('Jovem',r'\b(?:jovem|jove)\b'),('Varejo',r'\bvarejo\b'),
            ('Animada',r'\b(?:animad[ao]|alegre|algre|pra cima|up(?: festas?| fest)?|festas?)\b'),
            ('Institucional',r'\b(?:institucional|intitucional|instucional|insitucional|insittucional|insitituciona|instituciona|insititucional)\b'),
            ('Jornalística',r'\b(?:jornalistico|jornalistica|jornalismo|jornalisico|jornalisitico|jornarlistico|josnalistico)\b'),
            ('Caricata',r'\b(?:caricat[ao]s?|personagens?|papai noel|caipira)\b'),
            ('Política',r'\bpolitic[ao]\b'),('VSL',r'\b(?:vsl|vls)\b'),
            ('Vídeo',r'\bvideo\b'),('Narração',r'\b(?:narracao|narrativ[ao]s?|documentarios?)\b'),
            ('Infantil',r'\b(?:infantil|infantiu|infatil|crianca)\b'),
            ('Religiosa',r'\b(?:religioso|igreja)\b'),('Esportiva',r'\b(?:esporte|futebol)\b'),
            ('URA',r'\bura\b'),('Vinhetas',r'\bvinhetas?\b'),
            ('Natural',r'\b(?:natural|coloquial|suave)\b'),('Emotiva',r'\b(?:emotiv[ao]|motivacional)\b'),
            ('Promocional',r'\bpromocional\b'),('Carro de som',r'\bcarro de som\b')
        ]
        normalized=normalize_name(style_text)
        for label,pattern in patterns:
            if re.search(pattern,normalized):styles.append(label)
        if re.search(r'\bingles\b',normalized):languages.append('Inglês')
        if re.search(r'\bespanhol\b',normalized):languages.append('Espanhol')
        details=plain_html(parts[1])[:2500] if len(parts)>1 else ''
        demos=[]
        try:
            groups=json.loads(row.get('demos') or '{}')
            for group in groups.values():
                if not isinstance(group,dict):continue
                for key,demo in group.items():
                    if isinstance(demo,dict) and demo.get('demo'):
                        demos.append({'style':plain_html(demo.get('estilo',key)), 'audio':media_url(demo['demo'],'demos')})
        except (ValueError,TypeError):raise ValueError('Invalid public demo list')
        filename=row.get('demo');audio=media_url(filename,'demos') if filename else next((d['audio'] for d in demos if d['style']=='padrao'),demos[0]['audio'] if demos else None)
        if not audio:raise ValueError('Voice without a playable public demo')
        title=plain_html(row.get('status_titulo'));extra=plain_html(row.get('status_texto'));label=' · '.join(x for x in [title,extra] if x)
        lower=normalize_name(title)
        if lower=='10 min':status='recording_10min'
        elif lower=='30 min':status='recording_30min'
        elif lower=='online':status='recording_online'
        elif lower=='offline':status='offline'
        elif lower.startswith('volto'):status='returning'
        elif lower in ['indisponivel','ferias']:status='unavailable'
        else:status='unknown'
        tokens=str(row.get('filtro','')).lower().split()
        kind='Infantil' if 'infantil' in tokens else 'Feminina' if 'feminina' in tokens else 'Masculina' if 'masculina' in tokens else None
        region=plain_html(row.get('estado')) or None
        voice={'id':'lb-'+str(native_id),'providerId':native_id,'name':name,'type':kind,'region':region,'styles':styles,'languages':languages,'status':status,'statusLabel':label or 'Disponibilidade sob consulta','audio':audio,'audioMime':'audio/wav' if audio.lower().endswith('.wav') else 'audio/mpeg','profile':SOURCE,'recordingInfo':details,'schedule':[]}
        if row.get('imagem'):voice['sourcePhoto']=voice['photo']=media_url(row['imagem'],'perfil')
        voices.append(voice)
    return sorted(voices,key=lambda v:v['providerId'])


def attach_local_profiles(voices):
    routes_file=Path('data/voice-profile-routes.json')
    existing=json.loads(routes_file.read_text()) if routes_file.exists() else []
    valid=[x for x in existing if isinstance(x,dict) and re.fullmatch(r'/perfil-locutor-[a-z0-9][a-z0-9-]*/',x.get('path',''))]
    by_id={x['id']:x['path'] for x in valid};by_name={normalize_name(x.get('name','')):x['path'] for x in valid}
    used=set()
    for voice in voices:
        slug=normalize_name(voice['name']).replace(' ','-') or voice['id']
        route=by_id.get(voice['id']) or by_name.get(normalize_name(voice['name'])) or '/perfil-locutor-'+slug+'/'
        if route in used:route='/perfil-locutor-'+slug+'-'+voice['id']+'/'
        used.add(route);voice['localProfile']=route;voice['profilePublished']=(Path(route.strip('/'))/'index.html').is_file()


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as temp:
        temp.write(text)
        temp_name = temp.name
    os.replace(temp_name, path)


def update_schema(voices):
    page = Path('vozes/index.html')
    html = page.read_text(encoding='utf-8')
    schema = {'@context':'https://schema.org', '@type':'ItemList', 'name':'Banco de vozes da A Locução', 'numberOfItems':len(voices), 'itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'Person','name':v['name'],'url':'https://alocucao.com.br'+v['localProfile'] if v.get('profilePublished') else v['profile'],'jobTitle':'Profissional de locução'}} for i,v in enumerate(voices)]}
    data = json.dumps(schema, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    html = re.sub(r'(<script id="voices-schema" type="application/ld\+json">).*?(</script>)', lambda m: m[1]+data+m[2], html, flags=re.S)
    import html as escaping
    fallback = '<ul class="fallback-list">' + ''.join('<li>'+('<a href="'+escaping.escape(v['localProfile'],quote=True)+'">'+escaping.escape(v['name'])+'</a>' if v.get('profilePublished') else escaping.escape(v['name']))+' — '+escaping.escape(v['type'] or 'Voz humana')+'</li>' for v in voices) + '</ul>'
    html = re.sub(r'<!-- voices-fallback:start -->.*?<!-- voices-fallback:end -->', lambda _: '<!-- voices-fallback:start -->'+fallback+'<!-- voices-fallback:end -->', html, flags=re.S)
    directory = '<!-- voices-directory:start --><details class="profile-directory"><summary>Ver todos os perfis de locutores</summary>' + fallback + '</details><!-- voices-directory:end -->'
    if '<!-- voices-directory:start -->' in html:
        html = re.sub(r'<!-- voices-directory:start -->.*?<!-- voices-directory:end -->', lambda _: directory, html, flags=re.S)
    else:
        html = html.replace('</noscript>', '</noscript>\n' + directory, 1)
    if '/assets/contextual-cta.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/contextual-cta.css">\n</head>', 1)
    if html != page.read_text(encoding='utf-8'):
        atomic_write(page, html)


def main():
    request = urllib.request.Request(API, headers={'User-Agent':'A-Locucao-Catalog-Sync/1.0 (+https://alocucao.com.br/)', 'Accept':'application/json'})
    with urllib.request.urlopen(request, timeout=40) as response:
        if urlsplit(response.url).hostname != 'paineldegravacao.com.br':
            raise ValueError('Unexpected redirect')
        html = response.read(4_000_001)
        if len(html) > 4_000_000:
            raise ValueError('Catalog response too large')
        voices = parse_catalog(html)
    previous = json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else None
    if previous and previous.get('provider')==PROVIDER and len(voices) < len(previous['voices']) * .65:
        raise ValueError('Large catalog shrink; preserving previous catalog')
    attach_local_profiles(voices)
    atomic_write(Path('data/voice-profile-routes.json'),json.dumps([{'id':v['id'],'name':v['name'],'path':v['localProfile'],'url':'https://alocucao.com.br'+v['localProfile'],'published':v['profilePublished']} for v in voices],ensure_ascii=False,indent=2)+'\n')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    content_hash = hashlib.sha256(json.dumps(voices, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    catalog = {'schemaVersion':1, 'provider':PROVIDER, 'source':SOURCE, 'fetchedAt':now, 'contentUpdatedAt':previous['contentUpdatedAt'] if previous and previous.get('contentHash') == content_hash else now, 'contentHash':content_hash, 'count':len(voices), 'idAliases':json.loads(Path('data/provider-voice-aliases.json').read_text()) if Path('data/provider-voice-aliases.json').exists() else {}, 'voices':voices}
    atomic_write(OUTPUT, json.dumps(catalog, ensure_ascii=False, separators=(',', ':'))+'\n')
    update_schema(voices)
    print(f'Validated {len(voices)} voices; catalog refreshed at {now}')


if __name__ == '__main__':
    main()
