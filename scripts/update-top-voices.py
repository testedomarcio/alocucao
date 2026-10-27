#!/usr/bin/env python3
"""Refresh the fortnightly ranking. Each published project counts once; alternate takes do not add orders."""
import json, unicodedata
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def rank(voices, works):
    counts = Counter(p['voice'] for p in works)
    def alphabet(name):
        return ''.join(c for c in unicodedata.normalize('NFD', name.casefold()) if not unicodedata.combining(c))
    eligible = sorted((v for v in voices if counts[v['slug']]), key=lambda v: (-counts[v['slug']], alphabet(v['name']), v['slug']))
    return [{'rank': i, 'voice': v['slug'], 'name': v['name'], 'work_count': counts[v['slug']]} for i, v in enumerate(eligible[:3], 1)]

if __name__ == '__main__':
    voices = json.loads((ROOT/'data/new-voices.json').read_text())
    works = json.loads((ROOT/'data/latest-works.json').read_text())
    result = {'updated_on': datetime.now(ZoneInfo('America/Sao_Paulo')).date().isoformat(), 'basis': 'published_projects', 'entries': rank(voices, works)}
    (ROOT/'data/top-voices.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))
