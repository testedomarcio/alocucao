"""Presentation-only enhancement, restricted to /vozes/."""
import re

ASSETS = '<link rel="stylesheet" href="/assets/voice-bank-view.css?v=20261030"><script src="/assets/voice-bank-view.js?v=20261030"></script>'

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
        return markup
    body = re.sub(r'<article class="voice-card".*?</article>', card, body, flags=re.S)
    selector = '''<div class="bank-view-switch" role="group" aria-label="Visualização das vozes" hidden>
<button type="button" data-voice-view="list" aria-pressed="false" aria-controls="voice-results"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M8 6h13M8 12h13M8 18h13M3 6h1M3 12h1M3 18h1"/></svg>Lista</button>
<button type="button" data-voice-view="cards" aria-pressed="false" aria-controls="voice-results"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Cartões</button></div>'''
    body = re.sub(r'(<p id="voice-count".*?</p>)', lambda m: '<div class="bank-results-bar">'+m[0]+selector+'</div>', body, count=1)
    return body.replace('<div class="voice-grid">', '<div class="voice-grid" id="voice-results">', 1)
