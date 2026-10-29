"""Apply only the approved commercial pricing components, including after rebuilds."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent.parent
POLICY=json.loads((ROOT/'assets/pricing.js').read_text().split('window.ALocucaoPricing = ',1)[1].rstrip(';\n'))
VERSION='20261028progressive'
def money(n):return f'R$ {n:.2f}'.replace('.',',')
def duration(n):
 if n<60:return f'{n} segundos'
 m,s=divmod(n,60)
 return f'{m}min'+(f'{s:02d}s' if s else '')
def table(key):
 spec=POLICY[key];rows=[];low=0
 for high,value in spec['bands']:
  label='Até '+duration(high) if low==0 else duration(low+1)+' a '+duration(high)
  rows.append(f'<tr><th scope="row">{label}</th><td>{money(value)}</td></tr>');low=high
 rows.append(f'<tr><th scope="row">Acima de {duration(low)}</th><td>Sob orçamento</td></tr>')
 return f'<article class="price-card progressive-card"><h3>{spec["name"]}</h3><p class="price-sub">A partir de</p><div class="price">{money(spec["bands"][0][1])}</div><table class="duration-prices"><caption class="sr-only">Tabela de preços de {spec["name"]}</caption><thead><tr><th scope="col">Duração</th><th scope="col">Valor total</th></tr></thead><tbody>'+''.join(rows)+f'</tbody></table><a class="btn light" href="https://wa.me/5527996529832?text=Ol%C3%A1%21%20Gostaria%20de%20contratar%20'+('Locu%C3%A7%C3%A3o%20Off' if key=='off' else 'Produ%C3%A7%C3%A3o%20Completa')+'." data-cta="orcamento">Solicitar pelo WhatsApp ↗</a></article>'
def prices(keys=('off','producao'),compact=False):
 head='<section class="section dark progressive-pricing" id="precos"><div class="wrap"><div class="section-head"><div><span class="eyebrow">Mais tempo de gravação, mais economia para você.</span><h2>Seu texto ficou maior?<br>O preço não precisa dobrar!</h2></div><p>Seu texto não precisa caber em apenas 40 segundos. Nossa tabela progressiva oferece preços mais vantajosos para gravações maiores, com qualidade profissional e contratação simplificada.</p></div>'
 if compact:return head+'<p class="progressive-start">Locução Off a partir de <strong>R$ 12,00</strong> · Produção Completa a partir de <strong>R$ 25,00</strong></p><a class="btn light" href="/calculadora/#precos">Ver tabela e calcular meu roteiro ↗</a></div></section>'
 return head+'<div class="price-grid'+(' single-price' if len(keys)==1 else '')+'">'+''.join(table(k) for k in keys)+'</div><p class="note">Valores totais por faixa de duração estimada. Projetos de complexidade excepcional: sob orçamento. Valor, prazo e condições de uso confirmados antes do pagamento.</p></div></section>'
def update(root=ROOT):
 changed=[]
 for p in root.rglob('*.html'):
  if any(x in p.parts for x in ['.git','node_modules','templates','reports']):continue
  s=p.read_text();original=s
  if 'id="calc-text"' in s:
   name=re.search(r'<body data-page="([^"]*)',s)[1]
   keys=('off',) if name=='locucao-off' else ('producao',) if name=='spot-comercial' else ('off','producao')
   s=re.sub(r'<section class="section dark(?: progressive-pricing)?" id="precos">.*?</section>',lambda _:prices(keys,compact=name==''),s,flags=re.S)
   if name=='precos':s=re.sub(r'<section class="section"><div class="wrap editorial"><h2>Quando o texto passa de 40 segundos.*?</section>','',s,flags=re.S)
   if name=='calculadora' and 'id="precos"' not in s:s=s.replace('</main>',prices()+'</main>')
   s=re.sub(r'/assets/nova\.(css|js)\?v=[^"\s]+',lambda m:f'/assets/nova.{m[1]}?v={VERSION}',s)
   if '/assets/pricing.js' not in s:s=s.replace('<script src="/assets/nova.js',f'<script src="/assets/pricing.js?v={VERSION}" defer></script><script src="/assets/nova.js')
   # Preserve the estimator, with an honest short explanation on its dedicated page.
   if name=='calculadora':
    s=s.replace('Seu texto cabe no tempo do anúncio?','Quanto custa gravar seu texto?')
    s=s.replace('A duração real depende da interpretação, do ritmo e das pausas.','Estime o valor pela duração do roteiro. Pausas, velocidade, interpretação e leitura de números podem alterar o tempo real.')
   s=s.replace('Consulte valores de locução por até 40 segundos e condições para trabalhos especiais.','Consulte a tabela progressiva por duração e as condições para trabalhos especiais.')
   s=s.replace('Estime duração e preço da sua peça comercial: Off R$ 12 e Produção Completa R$ 25 por até 40 segundos.','Estime duração e preço pela tabela progressiva: Off a partir de R$ 12 e Produção Completa a partir de R$ 25.')
  if p.relative_to(root).as_posix() in ['termos/index.html','termos-de-uso/index.html']:
   legal=json.loads((root/'data/legal-pages.json').read_text())['termos']['body']
   s=re.sub(r'<article class="wrap editorial">.*?</article>',lambda _: '<article class="wrap editorial">'+legal+'</article>',s,flags=re.S)
   s=s.replace('Atualização: 26 de outubro de 2026.','Atualização: 28 de outubro de 2026.')
  if s!=original:p.write_text(s);changed.append(str(p.relative_to(root)))
 return changed
if __name__=='__main__':print('\n'.join(update()))
