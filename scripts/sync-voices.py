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

from bs4 import BeautifulSoup

SOURCE = 'https://painel.audio.net.br/Vozes/alocucao'
OUTPUT = Path('assets/voices-catalog.json')
STATES = ['Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Distrito Federal','Espírito Santo','Goiás','Maranhão','Mato Grosso','Mato Grosso do Sul','Minas Gerais','Pará','Paraíba','Paraná','Pernambuco','Piauí','Rio de Janeiro','Rio Grande do Norte','Rio Grande do Sul','Rondônia','Roraima','Santa Catarina','São Paulo','Sergipe','Tocantins']
STYLES = ['Caricata','Padrão','Impacto','Animada','Varejo','Política','VSL']


def safe_url(value, hosts):
    parsed = urlsplit(value or '')
    if parsed.scheme != 'https' or parsed.hostname not in hosts or parsed.username or parsed.password:
        raise ValueError('Unexpected public media/profile URL')
    return value


def parse_catalog(html):
    soup = BeautifulSoup(html, 'html5lib')
    table = soup.select_one('table#example')
    if not table:
        raise ValueError('Catalog table missing; preserving last valid catalog')
    voices, seen = [], set()
    from collections import Counter
    print('Source diagnostics:', len(table.select('audio')), 'audio elements;', dict(Counter(len(r.find_all('td', recursive=False)) for r in table.select('tr'))))
    for row in table.select('tr'):
        cells = row.find_all('td', recursive=False)
        if len(cells) != 4:
            continue
        name = ' '.join(str(t).strip() for t in cells[0].find_all(string=True, recursive=False)).strip()
        audio = cells[2].find('audio')
        link = cells[3].find('a', href=True)
        if not name or not audio or not link:
            raise ValueError('Incomplete voice row')
        profile = safe_url(link['href'], {'perfillocutor.com.br','www.perfillocutor.com.br'})
        voice_id = urlsplit(profile).path.strip('/')
        if not re.fullmatch(r'[A-Za-z0-9_-]+', voice_id) or voice_id in seen:
            raise ValueError('Invalid or duplicate voice identifier')
        seen.add(voice_id)
        media = safe_url(audio.get('src'), {'storageoffs.offsbrasil.com.br'})
        # nocache is a transport cache marker, not a version or API key.
        if re.fullmatch(r'nocache=\d+', urlsplit(media).query):
            media = media.split('?', 1)[0]
        media = media.replace(' ', '%20')
        tokens = [s.get_text(strip=True) for s in cells[2].find_all('span')]
        status_cell = BeautifulSoup(str(cells[1]), 'html.parser')
        for span in status_cell.select('span'):
            span.decompose()
        label = status_cell.get_text(' ', strip=True)
        lower = label.lower()
        if 'offline' in lower:
            status = 'offline'
        elif 'indispon' in lower:
            status = 'unavailable'
        elif '10 minutos' in lower:
            status = 'recording_10min'
        elif '30 minutos' in lower:
            status = 'recording_30min'
        elif '5 horas' in lower:
            status = 'recording_1to5h'
        else:
            status = 'unknown'
        styles = [x for x in STYLES if x in tokens]
        if 'vvideo' in tokens:
            styles.append('Vídeo')
        region = next((x for x in STATES if x in tokens), None)
        if 'paulista' in tokens:
            region = 'São Paulo'
        voices.append({'id': voice_id, 'name': name, 'type': 'Feminina' if 'Feminino' in tokens else 'Masculina' if 'Masculino' in tokens else None, 'region': region, 'styles': styles, 'languages': ['Português'] + [x for x in ['Inglês','Espanhol'] if x in tokens], 'status': status, 'statusLabel': label or 'Disponibilidade sob consulta', 'audio': media, 'profile': profile})
    if len(voices) != len(table.select('audio')):
        raise ValueError('Incomplete extraction; preserving previous catalog')
    if len(voices) < 40:
        raise ValueError('Unexpectedly small catalog; manual review required')
    return sorted(voices, key=lambda v: v['id'])



def attach_local_profiles(voices):
    routes_file = Path('data/voice-profile-routes.json')
    existing = json.loads(routes_file.read_text(encoding='utf-8')) if routes_file.exists() else []
    previous = {item['id']:item['path'] for item in existing if isinstance(item,dict) and re.fullmatch(r'/perfil-locutor-[a-z0-9][a-z0-9-]*/',item.get('path','')) and isinstance(item.get('id'),str)}
    groups = {}
    for voice in voices:
        plain = unicodedata.normalize('NFKD',voice['name']).encode('ascii','ignore').decode().lower()
        slug = re.sub(r'[^a-z0-9]+','-',plain).strip('-') or voice['id'].lower()
        groups.setdefault(slug, []).append(voice)
    for slug, members in groups.items():
        for voice in members:
            suffix = '-'+voice['id'].lower() if len(members)>1 else ''
            route = previous.get(voice['id'], '/perfil-locutor-'+slug+suffix+'/')
            voice['localProfile'] = route
            folder = Path(route.strip('/'))
            voice['profilePublished'] = (folder/'index.html').is_file()


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
    request = urllib.request.Request(SOURCE, headers={'User-Agent':'A-Locucao-Catalog-Sync/1.0 (+https://alocucao.com.br/)', 'Accept':'text/html'})
    with urllib.request.urlopen(request, timeout=40) as response:
        if urlsplit(response.url).hostname != 'painel.audio.net.br':
            raise ValueError('Unexpected redirect')
        html = response.read(4_000_001)
        if len(html) > 4_000_000:
            raise ValueError('Catalog response too large')
        voices = parse_catalog(html)
    previous = json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else None
    if previous and len(voices) < len(previous['voices']) * .65:
        raise ValueError('Large catalog shrink; preserving previous catalog')
    attach_local_profiles(voices)
    atomic_write(Path('data/voice-profile-routes.json'),json.dumps([{'id':v['id'],'name':v['name'],'path':v['localProfile'],'url':'https://alocucao.com.br'+v['localProfile'],'published':v['profilePublished']} for v in voices],ensure_ascii=False,indent=2)+'\n')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    content_hash = hashlib.sha256(json.dumps(voices, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    catalog = {'schemaVersion':1, 'source':SOURCE, 'fetchedAt':now, 'contentUpdatedAt':previous['contentUpdatedAt'] if previous and previous.get('contentHash') == content_hash else now, 'contentHash':content_hash, 'count':len(voices), 'voices':voices}
    atomic_write(OUTPUT, json.dumps(catalog, ensure_ascii=False, separators=(',', ':'))+'\n')
    update_schema(voices)
    print(f'Validated {len(voices)} voices; catalog refreshed at {now}')


if __name__ == '__main__':
    main()
