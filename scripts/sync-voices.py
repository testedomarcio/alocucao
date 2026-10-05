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


SOURCE = 'https://vozlocutor.com.br/'
API = SOURCE
PROVIDER = 'vozlocutor'
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


def parse_catalog(payload):
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    soup = BeautifulSoup(payload, 'html.parser')
    rows = soup.select('tbody tr')
    if not 40 <= len(rows) <= 1500:
        raise ValueError('Incomplete or unexpectedly sized public catalog')
    voices = []; seen = set()
    abbreviations = dict(zip(['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'], STATES))
    for row in rows:
        cell = row.select_one('[data-locutor-id]')
        name = row.select_one('.locutor-name')
        audio = row.select_one('audio[src]')
        metadata = row.select_one('td[data-label="Locutor"] > span')
        if not cell or not name or not audio or not metadata:
            raise ValueError('Incomplete public voice row')
        native_id = cell.get('data-locutor-id', '')
        if not native_id.isdigit() or native_id in seen:
            raise ValueError('Invalid or duplicate voice identifier')
        seen.add(native_id)
        label = cell.get_text(' ', strip=True)
        normalized = normalize_name(label)
        if re.search(r'\d.*(?:min|hora)', normalized) and not normalized.startswith('locutor'):
            status = 'recording_online'
        elif normalized == 'offline': status = 'offline'
        elif 'volta' in normalized: status = 'returning'
        elif normalized in ['indisponivel','ferias']: status = 'unavailable'
        else: status = 'unknown'
        parts = [x.strip() for x in metadata.get_text(' ',strip=True).split(',')]
        if len(parts) != 5: raise ValueError('Unexpected public metadata')
        gender, _, style_text, details, region = parts
        kind = 'Feminina' if normalize_name(gender) in ['feminino','f'] else 'Masculina' if normalize_name(gender) in ['masculino','m'] else None
        styles = [style for style in STYLES if normalize_name(style) in normalize_name(style_text)]
        region = abbreviations.get(region.upper(), next((state for state in STATES if normalize_name(state)==normalize_name(region)),region))
        media = safe_url(urljoin(SOURCE,audio['src']), {'vozlocutor.com.br'})
        if urlsplit(media).path != '/download-audio.php': raise ValueError('Unexpected demo endpoint')
        voice = {'id':'vl-'+native_id,'providerId':int(native_id),'name':name.get_text(' ',strip=True),'type':kind,'region':region or None,'styles':styles,'languages':['Português'],'status':status,'statusLabel':label or 'Disponibilidade sob consulta','audio':media,'audioMime':'audio/mpeg','recordingInfo':details,'schedule':[]}
        photo = row.select_one('img.avatar-img[src]')
        if photo:
            value = safe_url(urljoin(SOURCE,photo['src']), {'vozlocutor.com.br'})
            if urlsplit(value).path not in ['/perfil-img.php','/img/avatar-masculino.png','/img/avatar-feminino.png']:
                # Skip placeholder images; do not invent photos.
                if urlsplit(value).path != '/perfil-img.php': value = None
            if value: voice['photo'] = value
        voices.append(voice)
    if len(soup.select('tbody audio[src]')) != len(voices): raise ValueError('Incomplete demos')
    return sorted(voices,key=lambda v:v['providerId'])


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as temp:
        temp.write(text)
        temp_name = temp.name
    os.replace(temp_name, path)


def update_schema(voices):
    page = Path('vozes/index.html')
    html = page.read_text(encoding='utf-8')
    schema = {'@context':'https://schema.org', '@type':'ItemList', 'name':'Banco de vozes da A Locução', 'numberOfItems':len(voices), 'itemListElement':[{'@type':'ListItem','position':i+1,'item':{'@type':'Person','name':v['name'],'jobTitle':'Profissional de locução'}} for i,v in enumerate(voices)]}
    data = json.dumps(schema, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    html = re.sub(r'(<script id="voices-schema" type="application/ld\+json">).*?(</script>)', lambda m: m[1]+data+m[2], html, flags=re.S)
    import html as escaping
    fallback = '<ul class="fallback-list">' + ''.join('<li>'+escaping.escape(v['name'])+' — '+escaping.escape(v['type'] or 'Voz humana')+'</li>' for v in voices) + '</ul>'
    html = re.sub(r'<!-- voices-fallback:start -->.*?<!-- voices-fallback:end -->', lambda _: '<!-- voices-fallback:start -->'+fallback+'<!-- voices-fallback:end -->', html, flags=re.S)
    html = re.sub(r'<!-- voices-directory:start -->.*?<!-- voices-directory:end -->', '', html, flags=re.S)
    if '/assets/contextual-cta.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="/assets/contextual-cta.css">\n</head>', 1)
    if html != page.read_text(encoding='utf-8'):
        atomic_write(page, html)


def main():
    request = urllib.request.Request(API, headers={'User-Agent':'A-Locucao-Catalog-Sync/1.0 (+https://alocucao.com.br/)', 'Accept':'text/html'})
    with urllib.request.urlopen(request, timeout=40) as response:
        if urlsplit(response.url).hostname != 'vozlocutor.com.br':
            raise ValueError('Unexpected redirect')
        html = response.read(4_000_001)
        if len(html) > 4_000_000:
            raise ValueError('Catalog response too large')
        voices = parse_catalog(html)
    previous = json.loads(OUTPUT.read_text(encoding='utf-8')) if OUTPUT.exists() else None
    if previous and previous.get('provider')==PROVIDER and len(voices) < len(previous['voices']) * .65:
        raise ValueError('Large catalog shrink; preserving previous catalog')
    now = datetime.now(timezone.utc).isoformat(timespec='seconds')
    content_hash = hashlib.sha256(json.dumps(voices, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    catalog = {'schemaVersion':1, 'provider':PROVIDER, 'source':SOURCE, 'fetchedAt':now, 'contentUpdatedAt':previous['contentUpdatedAt'] if previous and previous.get('contentHash') == content_hash else now, 'contentHash':content_hash, 'count':len(voices), 'idAliases':json.loads(Path('data/provider-voice-aliases.json').read_text()) if Path('data/provider-voice-aliases.json').exists() else {}, 'voices':voices}
    atomic_write(OUTPUT, json.dumps(catalog, ensure_ascii=False, separators=(',', ':'))+'\n')
    update_schema(voices)
    print(f'Validated {len(voices)} voices; catalog refreshed at {now}')


if __name__ == '__main__':
    main()
