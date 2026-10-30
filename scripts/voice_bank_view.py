"""Presentation-only enhancement, restricted to /vozes/."""
import re

ASSETS = '<link rel="stylesheet" href="/assets/voice-bank-view.css?v=20261030compact2"><script src="/assets/voice-bank-view.js?v=20261030compact2"></script>'

def enhance(body):
    def card(match):
        markup = match.group(0)
        markup = markup.replace('<div class="voice-body">', '<div class="voice-body"><div class="bank-identity">', 1)
        markup = markup.replace('<div class="audio-item">', '</div><div class="audio-item">', 1)
        # Conversion markup is added by sample_offer before this enhancement.
        marker = re.search(r'<(?:a|button)[^>]*class="recent-work-link"', markup)
        if marker:
            markup = markup[:marker.start()] + '<div class="bank-conversion">' + markup[marker.start():]
            markup = markup.replace('</article>', '</div></article>')
        # Native players are reused; these lightweight controls exist only in list view.
        name = re.search(r'<h2><a[^>]*>(.*?)</a></h2>', markup).group(1)
        buttons = []
        def panel(audio_match):
            item = audio_match.group(0)
            audio_id = re.search(r'<audio id="([^"]+)"', item).group(1)
            label = re.search(r'aria-label="([^"]+)"', item).group(1)
            produced = audio_id.endswith('-producao')
            title = 'Produção Completa' if produced else 'Locução Off — voz sem trilha'
            buttons.append(f'<button type="button" data-bank-demo="{audio_id}" aria-controls="panel-{audio_id}" aria-expanded="false" aria-label="Ouvir {label}" title="{title}"><span aria-hidden="true">▷</span>{"Produzido" if produced else "Off"}</button>')
            item = item.replace('<div class="audio-item">', f'<div class="audio-item" id="panel-{audio_id}">', 1)
            return item[:-6] + f'<button type="button" class="bank-demo-close" aria-label="Fechar {label}" title="Fechar demonstração">×</button></div>'
        markup = re.sub(r'<div class="audio-item">.*?</div>', panel, markup, flags=re.S)
        controls = '<div class="bank-demo-controls" role="group" aria-label="Demonstrações de '+name+'">'+''.join(buttons)+'</div>'
        markup = markup.replace('</div><div class="audio-item"', '</div>'+controls+'<div class="audio-item"', 1)
        markup = re.sub(r'<a class="profile-link" href="([^"]+)">Ver perfil completo</a>', lambda m: '<a class="profile-link" href="'+m[1]+'" aria-label="Ver perfil completo de '+name+'"><span class="bank-profile-full">Ver perfil completo</span><span class="bank-profile-short" aria-hidden="true">Perfil ↗</span></a>', markup)
        if 'aria-label="Ainda sem avaliações"' not in markup:
            markup = markup.replace('class="voice-card"', 'class="voice-card" data-bank-reviewed', 1)
        return markup
    body = re.sub(r'<article class="voice-card".*?</article>', card, body, flags=re.S)
    selector = '''<div class="bank-view-switch" role="group" aria-label="Visualização das vozes" hidden>
<button type="button" data-voice-view="list" aria-pressed="false" aria-controls="voice-results"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M8 6h13M8 12h13M8 18h13M3 6h1M3 12h1M3 18h1"/></svg>Lista</button>
<button type="button" data-voice-view="cards" aria-pressed="false" aria-controls="voice-results"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Cartões</button></div>'''
    body = re.sub(r'(<p id="voice-count".*?</p>)', lambda m: '<div class="bank-results-bar">'+m[0]+selector+'</div>', body, count=1)
    return body.replace('<div class="voice-grid">', '<div class="voice-grid" id="voice-results">', 1)
