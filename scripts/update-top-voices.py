#!/usr/bin/env python3
"""Refresh from verified delivered-order aggregates, preserving the historical ranking until available."""
import json,unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from voice_orders import confirmed_counts
ROOT=Path(__file__).resolve().parent.parent

def rank(voices,counts):
 def alphabet(name):return ''.join(c for c in unicodedata.normalize('NFD',name.casefold()) if not unicodedata.combining(c))
 eligible=sorted((v for v in voices if counts.get(v['slug'],0)>0),key=lambda v:(-counts[v['slug']],alphabet(v['name']),v['slug']))
 return [{'rank':i,'voice':v['slug'],'name':v['name'],'order_count':counts[v['slug']]} for i,v in enumerate(eligible[:3],1)]
if __name__=='__main__':
 voices=json.loads((ROOT/'data/new-voices.json').read_text())
 counts=confirmed_counts(json.loads((ROOT/'data/delivered-orders.json').read_text()),{v['slug'] for v in voices})
 if not counts:
  print('No verified order totals. Historical TOP positions preserved; no numbers inferred from published audio.')
 else:
  result={'updated_on':datetime.now(ZoneInfo('America/Sao_Paulo')).date().isoformat(),'basis':'verified_delivered_orders','entries':rank(voices,counts)}
  (ROOT/'data/top-voices.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps(result,ensure_ascii=False))
