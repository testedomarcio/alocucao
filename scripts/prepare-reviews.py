#!/usr/bin/env python3
"""Update the backend's allowed voice IDs from the canonical catalog."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parent.parent
voices=json.loads((root/'data/new-voices.json').read_text())
assert all(re.fullmatch('[a-z0-9-]+',v['slug']) for v in voices)
(root/'supabase/seed-review-voices.sql').write_text('-- Regenerate after adding voices: python3 scripts/prepare-reviews.py\ninsert into public.review_voices(slug) values\n'+',\n'.join("('"+v['slug']+"')" for v in voices)+'\non conflict do nothing;\n')
