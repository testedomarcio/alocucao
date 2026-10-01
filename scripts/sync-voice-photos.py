#!/usr/bin/env python3
"""Import public profile photos as small, local WebP thumbnails."""
import concurrent.futures
import io
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit

from bs4 import BeautifulSoup
from PIL import Image, ImageOps

CATALOG = Path('assets/voices-catalog.json')
CACHE = Path('data/voice-photos-cache.json')
DEST = Path('assets/voice-photos')
HEADERS = {'User-Agent':'A-Locucao-Catalog-Sync/1.0 (+https://alocucao.com.br/)'}
PROFILE_HOSTS = {'perfillocutor.com.br','www.perfillocutor.com.br'}
PHOTO_HOSTS = {'locutort.offsbrasil.com.br'}
MAX_IMAGE = 6_000_000
Image.MAX_IMAGE_PIXELS = 20_000_000


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urlsplit(newurl)
        if parsed.scheme != 'https' or parsed.hostname not in PROFILE_HOSTS | PHOTO_HOSTS:
            raise ValueError('Unexpected redirect in public photo source')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def request(url, headers=None):
    return urllib.request.build_opener(SafeRedirect).open(urllib.request.Request(url, headers={**HEADERS, **(headers or {})}), timeout=15)


def process(voice, old, now):
    voice_id = voice['id']
    local = DEST / (voice_id+'.webp')
    if old and now-old.get('checkedAt',0) < 86400 and (not old.get('photo') or local.exists()):
        return voice_id, old, False
    time.sleep(.6)
    try:
        parsed = urlsplit(voice['profile'])
        if parsed.scheme != 'https' or parsed.hostname not in PROFILE_HOSTS:
            raise ValueError('Invalid profile origin')
        with request(voice['profile']) as response:
            html = response.read(1_000_001)
            if len(html)>1_000_000:
                raise ValueError('Profile too large')
        soup = BeautifulSoup(html,'html5lib')
        candidates = [i.get('src','') for i in soup.find_all('img')]
        url = next((u for u in candidates if urlsplit(u).scheme=='https' and urlsplit(u).hostname in PHOTO_HOSTS and '/imgPerfil/' in urlsplit(u).path), None)
        if not url:
            return voice_id, {'checkedAt':now,'photo':None}, False
        # The source adds a date query; the actual image pathname is preserved.
        url = quote(url.split('?',1)[0], safe=':/%')
        conditional = {}
        if old and old.get('source')==url and local.exists():
            if old.get('etag'): conditional['If-None-Match']=old['etag']
            elif old.get('lastModified'): conditional['If-Modified-Since']=old['lastModified']
        try:
            with request(url,conditional) as response:
                raw = response.read(MAX_IMAGE+1)
                if len(raw)>MAX_IMAGE:
                    raise ValueError('Photo too large')
                etag = response.headers.get('ETag');modified = response.headers.get('Last-Modified')
        except urllib.error.HTTPError as error:
            if error.code==304 and old and local.exists():
                return voice_id,{**old,'checkedAt':now},False
            raise
        with Image.open(io.BytesIO(raw)) as original:
            image = ImageOps.exif_transpose(original).convert('RGB')
            image.thumbnail((160,160),Image.Resampling.LANCZOS)
            out=io.BytesIO();image.save(out,format='WEBP',quality=78,method=4)
        data=out.getvalue()
        if not local.exists() or local.read_bytes()!=data:
            temporary=local.with_suffix('.tmp');temporary.write_bytes(data);os.replace(temporary,local)
        return voice_id,{'source':url,'photo':'/'+local.as_posix(),'checkedAt':now,'etag':etag,'lastModified':modified},False
    except Exception as error:
        # No credential fallback, bypass or alternate-source guessing.
        print(f'Photo unavailable for {voice_id}: {type(error).__name__}')
        return voice_id,{**(old or {}),'checkedAt':now},True


def main():
    catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
    cache=json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    DEST.mkdir(parents=True,exist_ok=True);CACHE.parent.mkdir(parents=True,exist_ok=True)
    (DEST/'.gitkeep').touch(exist_ok=True)
    now=int(time.time());failures=0
    # Confirm access on a small group before consulting all profiles.
    pending=[v for v in catalog['voices'] if now-cache.get(v['id'],{}).get('checkedAt',0)>=86400]
    first=pending[:3]
    outcomes=[process(v,cache.get(v['id']),now) for v in first]
    for voice_id,result,failed in outcomes:cache[voice_id]=result;failures+=failed
    if len(first)==3 and failures==3:
        print('Photo source unavailable: retaining initials/previous thumbnails; remaining requests skipped')
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(process,v,cache.get(v['id']),now) for v in pending[3:]]
            for future in concurrent.futures.as_completed(futures):
                voice_id,result,failed=future.result();cache[voice_id]=result;failures+=failed
    for voice in catalog['voices']:
        entry=cache.get(voice['id'],{})
        photo=entry.get('photo')
        if photo and Path(photo.lstrip('/')).exists():voice['photo']=photo
        else:voice.pop('photo',None)
    CACHE.write_text(json.dumps(cache,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    CATALOG.write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(f'Public thumbnails: {sum(bool(v.get("photo")) for v in catalog["voices"])}/{len(catalog["voices"])}; failed profile requests: {failures}')


if __name__=='__main__':main()
