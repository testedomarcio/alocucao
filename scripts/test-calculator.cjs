const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const element=()=>({value:'',events:{},dataset:{},addEventListener(n,f){this.events[n]=f}});
const text=element(),service=element(),result=element(),link=element();
const context={document:{querySelector:s=>({'#calc-text':text,'#calc-service':service,'#calc-result':result,'#calc-whatsapp':link}[s]||null),querySelectorAll:()=>[],addEventListener(){}},navigator:{},window:{addEventListener(){}},encodeURIComponent};
vm.runInNewContext(fs.readFileSync('assets/pricing.js','utf8'),context);
vm.runInNewContext(fs.readFileSync('assets/nova.js','utf8'),context);
assert.match(result.textContent,/Digite um texto/);
const cases=[[40,12,25],[41,20,35],[90,20,35],[91,25,45],[120,25,45],[121,35,60],[180,35,60],[181,50,null],[300,50,null],[301,null,null]];
for(const [seconds,off,production] of cases){
 // Select a word count whose existing 2.5 words/second estimator yields the exact second.
 text.value=Array(Math.floor(seconds*2.5)).fill('palavra').join('\n');
 for(const [value,name,price] of [['off','Locução Off',off],['producao','Produção Completa',production]]){
  service.value=value;service.events.change();
  const expected=price===null?'Orçamento personalizado':`R$ ${price.toFixed(2).replace('.',',')}`;
  assert.ok(result.innerHTML.includes(expected),`${seconds}s ${name}`);
  assert.doesNotMatch(result.innerHTML,/crédit|palavras|caracteres|faixa/i);
  if(price===null)assert.doesNotMatch(result.innerHTML,/R\$/);
  else assert.ok(result.innerHTML.includes(name));
  const msg=new URL(link.href).searchParams.get('text');
  assert.ok(msg.includes(text.value));assert.ok(msg.includes(name));
  assert.ok(msg.includes(price===null?'Sob orçamento':expected));assert.doesNotMatch(msg,/crédit/i);
  assert.equal(link.textContent,price===null?'Solicitar orçamento pelo WhatsApp':'Solicitar pelo WhatsApp');
 }
}
text.value='<script>alert("teste")</script> & orçamento?\nOlá, cliente!';text.events.input();
assert.ok(!result.innerHTML.includes('<script>'));assert.ok(new URL(link.href).searchParams.get('text').includes(text.value));
text.value=' \n\t ';text.events.input();assert.match(result.textContent,/Digite um texto/);assert.ok(!link.dataset.service);assert.equal(link.textContent,'Solicitar pelo WhatsApp');assert.ok(!new URL(link.href).searchParams.get('text').includes('Segue o meu texto'));
const pages=fs.readdirSync('.',{recursive:true}).filter(p=>p.endsWith('.html')&&!p.startsWith('node_modules')&&fs.readFileSync(p,'utf8').includes('id="calc-text"'));
for(const path of pages){
 const html=fs.readFileSync(path,'utf8');
 assert.equal((html.match(/id="calc-text"/g)||[]).length,1,path);
 assert.ok(html.includes('Valor sujeito à confirmação após análise do roteiro.'),path);
 assert.ok(html.includes('/assets/nova.css?v=20261028progressive'),path);
 assert.ok(html.indexOf('/assets/pricing.js?')<html.indexOf('/assets/nova.js?'),path);
 assert.doesNotMatch(html,/em faixas de (?:até )?40 segundos|R\$ 24,00|R\$ 36,00|Créditos necessários/);
}
console.log(`PASS: 20 exact band boundaries, ${pages.length} shared calculators, selected service, full WhatsApp script, custom quote, empty input and script injection.`);
