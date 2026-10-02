#!/usr/bin/env python3
"""Sync public provider metadata; use its photos without mixing previous suppliers."""
import concurrent.futures
import json
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from runpy import run_path

CATALOG=Path('assets/voices-catalog.json')
CACHE=Path('data/voice-photos-cache.json')
ENDPOINT='https://paineldegravacao.com.br/!/disponibilidade'
HEADERS={'User-Agent':'A-Locucao-Catalog-Sync/1.0 (+https://alocucao.com.br/)'}
VERSION=4

def parse_schedule(markup):
    plain=run_path('scripts/sync-voices.py')['plain_html'](re.sub(r'<!--.*?-->','',markup,flags=re.S))
    days={'segunda-feira':'Segunda-feira','terça-feira':'Terça-feira','quarta-feira':'Quarta-feira','quinta-feira':'Quinta-feira','sexta-feira':'Sexta-feira','sábado':'Sábado','domingo':'Domingo'}
    pattern='('+'|'.join(re.escape(x) for x in days)+')'
    parts=re.split(pattern,plain,flags=re.I);result=[]
    for i in range(1,len(parts),2):
        key=parts[i].lower();body=parts[i+1];intervals=[]
        for start,end in re.findall(r'((?:[01]\d|2[0-3]):[0-5]\d)\s*(?:às|até|a|-)\s*((?:[01]\d|2[0-3]):[0-5]\d)',body,re.I):
            pair={'start':start,'end':end}
            if pair not in intervals:intervals.append(pair)
        if intervals:result.append({'day':days[key],'intervals':intervals[:8]})
    return result[:7]

def process(voice,old,now):
    request=urllib.request.Request(ENDPOINT,data=urlencode({'acao':'consultar-horarios','locutor':voice['providerId']}).encode(),headers=HEADERS)
    try:
        with urllib.request.urlopen(request,timeout=20) as r:
            if urlsplit(r.url).hostname!='paineldegravacao.com.br':raise ValueError('Unexpected schedule host')
            raw=r.read(1_000_001)
        if len(raw)>1_000_000:raise ValueError('Schedule too large')
        schedule=parse_schedule(raw.decode('utf-8'))
        return voice['id'],{'provider':'locucao-brasil','sourceVersion':VERSION,'checkedAt':now,'schedule':schedule,'scheduleCheckedAt':now},False
    except Exception:
        # Never carry metadata over from a different provider.
        previous=old if old and old.get('provider')=='locucao-brasil' else {}
        return voice['id'],{**previous,'provider':'locucao-brasil','sourceVersion':VERSION,'checkedAt':now,'schedule':previous.get('schedule',[])},True

def main():
    catalog=json.loads(CATALOG.read_text());old=json.loads(CACHE.read_text()) if CACHE.exists() else {};now=int(time.time())
    cache={v['id']:old[v['id']] for v in catalog['voices'] if v['id'] in old and old[v['id']].get('provider')=='locucao-brasil'}
    pending=[v for v in catalog['voices'] if now-cache.get(v['id'],{}).get('checkedAt',0)>=86400]
    done=0;failures=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures=[pool.submit(process,v,cache.get(v['id']),now) for v in pending]
        for f in concurrent.futures.as_completed(futures):
            identifier,entry,failed=f.result();cache[identifier]=entry;done+=1;failures+=failed
            if done%25==0:print(f'Public schedules: {done}/{len(pending)} checked',flush=True)
    for v in catalog['voices']:
        photo=v.get('sourcePhoto')
        if photo and urlsplit(photo).hostname=='hd.paineldegravacao.com.br':v['photo']=photo
        else:v.pop('photo',None)
        entry=cache.get(v['id'],{});v['schedule']=entry.get('schedule',[])
        if entry.get('scheduleCheckedAt'):v['scheduleCheckedAt']=entry['scheduleCheckedAt']
    CACHE.write_text(json.dumps(cache,ensure_ascii=False,separators=(',',':'))+'\n')
    CATALOG.write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n')
    print(f'New-provider schedules: {sum(bool(v["schedule"]) for v in catalog["voices"])}; temporarily unavailable: {failures}')
if __name__=='__main__':main()
