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


SOURCE = 'https://vozes.alocucao.com.br/'
API = SOURCE
PROVIDER = 'alocucao-official'
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
    from urllib.parse import urljoin
    match = re.search(r'const locutoresData = (\[.*?\]);', payload.decode('utf-8') if isinstance(payload, bytes) else payload, re.S)
    if not match:
        raise ValueError('Official catalog missing; preserving published catalog')
    rows = json.loads(match.group(1))
    if not 40 <= len(rows) <= 1500:
        raise ValueError('Incomplete official catalog')
    voices = []; seen = set()
    for row in rows:
        native_id = str(row.get('id', ''))
        if not native_id.isdigit() or native_id in seen or not row.get('nome'):
            raise ValueError('Invalid or duplicate official voice')
        seen.add(native_id)
        gender = normalize_name(row.get('sexo'))
        label = plain_html(row.get('display') or row.get('status') or 'Sob consulta')
        status = 'recording_online' if re.search(r'\d.*(?:minuto|hora)', normalize_name(label)) and not 'offline' in normalize_name(label) else 'unavailable'
        media = safe_url(urljoin(SOURCE, row.get('demo_principal_url') or row.get('demo_url') or ''), {'vozes.alocucao.com.br'})
        if urlsplit(media).path not in ['/midia.php', '/download-audio.php']:
            raise ValueError('Unexpected official demo endpoint')
        voice = {'id': 'vl-'+native_id, 'providerId': int(native_id), 'name': plain_html(row['nome']), 'type': 'Feminina' if gender in ['feminino', 'f'] else 'Masculina' if gender in ['masculino', 'm'] else '', 'region': plain_html(row.get('estado')), 'styles': [plain_html(x) for x in row.get('estilos', '').split(' - ') if x.strip()], 'languages': ['Português'], 'status': status, 'statusLabel': label, 'audio': media, 'audioMime': 'audio/mpeg'}
        if row.get('avatar_url'):
            voice['photo'] = safe_url(urljoin(SOURCE, row['avatar_url']), {'vozes.alocucao.com.br'})
            if urlsplit(voice['photo']).path != '/midia.php':
                raise ValueError('Unexpected official photo endpoint')
        voices.append(voice)
    return sorted(voices, key=lambda v: v['providerId'])


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
        if urlsplit(response.url).hostname != 'vozes.alocucao.com.br':
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
