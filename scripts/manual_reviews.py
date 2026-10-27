"""Validate approved public testimonials and compute ratings without an external service."""
import json
from pathlib import Path
from datetime import date
from urllib.parse import urlsplit

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
  links=row.get('links',[])
  if not isinstance(links,list) or len(links)>5:raise ValueError('Invalid review links')
  for link in links:
   if not isinstance(link,dict) or not isinstance(link.get('label'),str) or not 2<=len(link['label'])<=120:raise ValueError('Invalid link label')
   url=link.get('url')
   if not isinstance(url,str) or any(c.isspace() or ord(c)<32 for c in url):raise ValueError('Invalid link URL')
   parsed=urlsplit(url)
   if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password:raise ValueError('Review links must use HTTPS without credentials')
 return rows

def summarize(rows,voice):
 selected=[r for r in rows if r['voice']==voice]
 return (sum(r['rating'] for r in selected)/len(selected),len(selected)) if selected else (None,0)
