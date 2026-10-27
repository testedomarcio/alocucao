"""Validate approved public testimonials and compute ratings without an external service."""
import json
from pathlib import Path
from datetime import date

def load_reviews(path, slugs):
 rows=json.loads(Path(path).read_text())
 if not isinstance(rows,list):raise ValueError('Expected a list of public reviews')
 ids=set()
 for row in rows:
  if not row.get('id') or row['id'] in ids:raise ValueError('Review IDs must be unique')
  ids.add(row['id'])
  if row.get('voice') not in slugs:raise ValueError('Unknown review voice')
  if type(row.get('rating')) is not int or not 1<=row['rating']<=5:raise ValueError('Review rating must be 1–5')
  if not isinstance(row.get('name'),str) or not 2<=len(row['name'])<=120:raise ValueError('Missing public reviewer name')
  if not isinstance(row.get('comment'),str) or not 20<=len(row['comment'])<=3000:raise ValueError('Invalid review comment')
  date.fromisoformat(row['published_on'])
  image=row.get('image')
  if image and (not image.startswith('/assets/reviews/') or '..' in image):raise ValueError('Images must be hosted locally')
 return rows

def summarize(rows,voice):
 selected=[r for r in rows if r['voice']==voice]
 return (sum(r['rating'] for r in selected)/len(selected),len(selected)) if selected else (None,0)
