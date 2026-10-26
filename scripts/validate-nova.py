#!/usr/bin/env python3
"""Check all generated pages, canonical URLs, local links and first-party demo mapping."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.links=[];self.assets=[];self.h1=0;self.canon=[];self.robot='';self.scripts=[];self.schema=[];self.text=[];self.skip=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  d=dict(attrs)
  if d.get('id'):self.ids.add(d['id'])
  if tag=='a':self.links.append(d.get('href',''))
  if tag=='h1':self.h1+=1
  if tag in ['audio','img','script'] and d.get('src'):self.assets.append(d['src'])
  if tag=='script' and d.get('src'):self.scripts.append(d['src'])
  if tag=='link' and d.get('rel')=='canonical':self.canon.append(d.get('href'))
  if tag=='link' and d.get('rel')=='stylesheet':self.assets.append(d['href'])
  if tag=='meta' and d.get('name')=='robots':self.robot=d.get('content','')
  if tag in ['script','style']:self.skip+=1
 def handle_endtag(self,tag):
  if tag in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip:self.text.append(data)
manifest=json.loads((ROOT/'reports/reformulacao-2026-10-26/manifesto.json').read_text())
pages={row['path']:Page((ROOT/row['path']).read_text()) for row in manifest}
errors=[]
for path,p in pages.items():
 if p.h1!=1:errors.append(f'{path}: {p.h1} H1 headings')
 if len(p.canon)!=1:errors.append(f'{path}: canonical count {len(p.canon)}')
 if len(p.scripts)!=len(set(p.scripts)):errors.append(f'{path}: duplicate scripts')
 visible=' '.join(p.text)
 if re.search(r'painel de gravação|central de gravação|créditos?|cadastre|criar conta|🧠|multilíng|idiomas|07h|22h',visible,re.I):errors.append(f'{path}: obsolete copy')
 if any('drive.google' in s or 'vozes.alocucao.com.br' in s for s in p.links+p.assets):errors.append(f'{path}: external legacy dependency')
 for src in p.assets:
  u=urlsplit(src)
  if u.scheme or u.netloc:continue
  target=ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else (ROOT/path).parent/unquote(u.path)
  if not target.is_file():errors.append(f'{path}: missing asset {src}')
 for href in p.links:
  u=urlsplit(href)
  if u.hostname in ['wa.me','api.whatsapp.com'] and (u.hostname!='wa.me' or u.path!='/5527996529832'):errors.append(f'{path}: wrong WhatsApp')
  if u.scheme or u.netloc:continue
  target=(ROOT/unquote(u.path).lstrip('/') if u.path.startswith('/') else (ROOT/path).parent/unquote(u.path)) if u.path else ROOT/path
  if target.is_dir():target=target/'index.html'
  if not target.is_file():errors.append(f'{path}: missing link {href}');continue
  key=str(target.relative_to(ROOT))
  if u.fragment and key in pages and unquote(u.fragment) not in pages[key].ids:errors.append(f'{path}: broken anchor {href}')
voices=json.loads((ROOT/'data/new-voices.json').read_text());seen=set()
for v in voices:
 if v['slug'] in seen:errors.append('duplicate voice slug')
 seen.add(v['slug'])
 expected=re.sub('[^a-z0-9]','',__import__('unicodedata').normalize('NFKD',v['name']).encode('ascii','ignore').decode().lower())+'@alocucao.com.br'
 if v['email']!=expected:errors.append('wrong email: '+v['name'])
 for kind in ['off','producao']:
  if v[kind] and not v[kind].endswith('-'+v.get('temporary_demo',{}).get(kind,kind)+'.mp3'):errors.append('wrong demo label: '+v['name'])
  if v[kind] and not(ROOT/v[kind].lstrip('/')).is_file():errors.append('missing demo: '+v['name'])
works=json.loads((ROOT/'data/latest-works.json').read_text());work_ids=set();source_ids=set()
for work in works:
 if work['voice'] not in seen:errors.append('unknown work voice: '+work['voice']);continue
 if work['id'] in work_ids:errors.append('duplicate work id: '+work['id'])
 work_ids.add(work['id'])
 profile=(ROOT/'locutores'/work['voice']/'index.html').read_text()
 if 'id="ultimos-trabalhos"' not in profile:errors.append('missing latest works section: '+work['voice'])
 for track in work['tracks']:
  if track['source_file_id'] in source_ids:errors.append('duplicate work source')
  source_ids.add(track['source_file_id'])
  if not track['src'].startswith('/assets/trabalhos/'+work['voice']+'-') or not(ROOT/track['src'].lstrip('/')).is_file():errors.append('wrong work asset: '+track['src'])
  if profile.count('src="'+track['src']+'"')!=1:errors.append('wrong work mapping: '+track['src'])
  if track['duration_seconds']<=0:errors.append('invalid work duration: '+track['src'])
  for other in seen-{work['voice']}:
   if 'src="'+track['src']+'"' in (ROOT/'locutores'/other/'index.html').read_text():errors.append('work assigned to another voice: '+track['src'])
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)]
expected={r['url'] for r in manifest if r['index'] and r['url']==r['canonical']}
if set(urls)!=expected or len(urls)!=len(set(urls)):errors.append('sitemap mismatch or duplicates')
summary={'pages':len(pages),'voices':len(voices),'demos':sum(bool(v[k]) for v in voices for k in ['off','producao']),'sitemap_urls':len(urls),'errors':errors}
(ROOT/'reports/reformulacao-2026-10-26/validacao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
print(json.dumps(summary,ensure_ascii=False,indent=2));sys.exit(bool(errors))
