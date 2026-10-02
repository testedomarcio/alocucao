#!/usr/bin/env python3
"""Keep the four selected voice demos and their light catalog in sync."""
import html
import json
import re
from pathlib import Path
from urllib.parse import quote

IDS = ('alvesneto', 'lindy', 'gabrielzamboni', 'elissandra')
START = '<!-- featured-voices:start -->'
END = '<!-- featured-voices:end -->'

def markup(voices):
    cards = []
    for voice in voices:
        name = voice['name'].title()
        esc = lambda value: html.escape(str(value), quote=True)
        photo = f'<img src="{esc(voice["photo"])}" alt="" width="64" height="64" loading="lazy" decoding="async">' if voice.get('photo') else '<span class="featured-initial" aria-hidden="true">' + esc(name[0]) + '</span>'
        message = quote(f'Olá! Ouvi a voz de {name} na A Locução. Quero escolher este locutor para meu projeto. Pode confirmar disponibilidade, valor e prazo?')
        styles = ' · '.join(voice['styles'][:4])
        cards.append(f'''<article class="featured-voice" data-featured-id="{esc(voice['id'])}">
<div class="featured-identity">{photo}<div><h3><a href="{esc(voice['localProfile'])}">{esc(name)}</a></h3><p>Voz {esc(voice['type'].lower())} · {esc(voice['region'])}</p></div></div>
<p class="featured-status" data-featured-status>Disponibilidade sob consulta</p>
<p class="featured-styles">{esc(styles)}</p>
<audio controls preload="none" data-featured-audio data-voice="{esc(voice['name'])}" aria-label="Ouvir demonstração de {esc(name)}" src="{esc(voice['audio'])}"><a href="{esc(voice['audio'])}">Ouvir demonstração</a></audio>
<p class="featured-error" hidden>Não foi possível tocar a demo. <a href="{esc(voice['audio'])}" target="_blank" rel="noopener" data-featured-fallback>Abra o áudio em outra aba</a> ou peça orientação.</p>
<a class="featured-choose" href="https://paineldegravacao.com.br/comerciaistop/cadastro" target="_blank" rel="noopener" data-cta="voz_destaque_{esc(voice['id'])}">Cadastrar e ver vozes ↗</a>
</article>''')
    return START + '''<div class="featured-voices" data-featured-voices>
<p class="featured-label">Entre os mais pedidos</p>
<p class="panel-catalog-note">Demonstrações do catálogo anterior. Confira as vozes, a disponibilidade e o prazo no Painel de Gravação antes de contratar.</p><div class="featured-list">''' + '\n'.join(cards) + '''</div>
<p class="featured-sync" data-featured-sync>Consulte a disponibilidade e o prazo no atendimento.</p>
<a class="featured-all" href="/vozes/#voice-grid" data-cta="vozes_destaque_banco_completo">Ouça todas as vozes <span aria-hidden="true">→</span></a>
<noscript><p>As demonstrações funcionam sem JavaScript. Para confirmar o status atual, fale com o atendimento.</p></noscript>
</div>''' + END

def main():
    data = json.loads(Path('assets/voices-catalog.json').read_text())
    by_id = {voice['id']: voice for voice in data['voices']}
    # Never publish an incomplete selection when the upstream catalog fails.
    voices = [by_id[voice_id] for voice_id in IDS]
    fields = ('id', 'name', 'type', 'region', 'styles', 'status', 'statusLabel', 'audio', 'photo', 'localProfile')
    selected = [{key: voice[key] for key in fields if key in voice} for voice in voices]
    payload = {'schemaVersion': 1, 'count': len(selected), 'fetchedAt': data['fetchedAt'], 'voices': selected}
    Path('assets/featured-voices.json').write_text(json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + '\n')
    block = markup(voices)
    for page in Path('.').rglob('index.html'):
        if any(part.startswith('.') or part in ('node_modules', '_site') for part in page.parts):
            continue
        old = page.read_text()
        if START in old:
            new = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda _: block, old, flags=re.S)
            if new != old:
                page.write_text(new)

if __name__ == '__main__':
    main()
