"""Refine shared presentation without changing prices, scripts, metadata or routes.

Runs after the existing page and progressive-pricing generators. Safe to repeat.
"""
from pathlib import Path
import re
REVISION='20261030premium'

def refine_calculator(match, dedicated=False):
 section=match[0]
 if 'calc-inputs' in section:return section
 controls=re.search(r'(<label for="calc-service">.*?</textarea>)',section,re.S)[1]
 controls=controls.replace('id="calc-text"','id="calc-text" aria-describedby="calc-text-note"')
 result=re.search(r'<div id="calc-result".*?</div>',section,re.S)[0]
 link=re.search(r'<a [^>]*id="calc-whatsapp".*?</a>',section,re.S)[0]
 disclaimer=re.search(r'<p class="note calc-disclaimer">.*?</p>',section,re.S)[0]
 heading='' if dedicated else '<div class="calculator-heading"><span class="eyebrow">Planeje sua peça comercial</span><h2>Calcule sua locução.</h2></div>'
 return ('<section class="section calculator-section" id="calculadora"><div class="wrap">'+heading+
  '<div class="calculator"><div class="calc-inputs">'+controls+
  '<p class="note" id="calc-text-note">A duração real varia conforme o ritmo, as pausas e a interpretação.</p></div>'+
  '<div class="calc-summary"><h3>Estimativa do seu projeto</h3>'+result+link+disclaimer+'</div></div></div></section>')

def refine_page(s, dedicated=False, home=False, bank=False):
 s=re.sub(r'(/assets/nova\.css\?v=[^"&]+)(?:&amp;refine=[^"&]+)?"',r'\1&amp;refine='+REVISION+'"',s)
 s=re.sub(r'<section class="section" id="calculadora">.*?</section>',lambda m:refine_calculator(m,dedicated),s,flags=re.S)
 if dedicated:
  s=s.replace('<section class="hero">','<section class="hero calculator-intro">',1)
  s=s.replace('Estime o valor pela duração do roteiro. Pausas, velocidade, interpretação e leitura de números podem alterar o tempo real.', 'Cole seu roteiro e estime a duração e o valor da gravação.')
 if home or bank:
  def conditions_only(m):
   conditions=re.search(r'<details class="sample-conditions">.*?</details>',m[0],re.S)[0]
   return '<section class="'+('home-sample-conditions' if home else 'catalog-sample-conditions')+'" aria-label="Condições da amostra gratuita"><div class="wrap">'+conditions+'</div></section>'
  s=re.sub(r'<section class="section sample-offer" aria-labelledby="sample-heading">.*?</section>',conditions_only,s,flags=re.S)
 return s

def update(root):
 for p in root.rglob('*.html'):
  if any(x.startswith('.') or x=='node_modules' for x in p.relative_to(root).parts):continue
  s=p.read_text()
  if '/assets/nova.css?' not in s:continue
  route=p.relative_to(root).as_posix()
  new=refine_page(s,dedicated=route=='calculadora/index.html',home=route=='index.html',bank=route=='vozes/index.html')
  if new!=s:p.write_text(new)

if __name__=='__main__':update(Path(__file__).resolve().parent.parent)
