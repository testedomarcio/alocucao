const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const element=()=>({value:'',events:{},dataset:{},addEventListener(n,f){this.events[n]=f}});
const text=element(),service=element(),result=element(),link=element();
vm.runInNewContext(fs.readFileSync('assets/nova.js','utf8'),{document:{querySelector:s=>({'#calc-text':text,'#calc-service':service,'#calc-result':result,'#calc-whatsapp':link}[s]||null),querySelectorAll:()=>[],addEventListener(){}},navigator:{},window:{addEventListener(){}},encodeURIComponent});
assert.match(result.textContent,/Digite um texto/);
for(const [words,seconds,credits] of [[1,1,1],[39,16,1],[100,40,1],[101,41,2],[200,80,2],[201,81,3],[301,121,4]]){
 text.value=Array(words).fill('palavra').join('\n');text.events.input();
 for(const [value,name,price] of [['off','Locução Off',12],['producao','Produção Completa',25]]){
  service.value=value;service.events.change();
  assert.ok(result.innerHTML.includes(`${credits} ${credits===1?'crédito':'créditos'}`));
  assert.ok(result.innerHTML.includes(`R$ ${(credits*price).toFixed(2).replace('.',',')}`));
  assert.ok(result.innerHTML.includes(name));assert.doesNotMatch(result.innerHTML,/palavras|caracteres|faixa/);
  const msg=new URL(link.href).searchParams.get('text');
  assert.ok(msg.includes(`Roteiro:\n${text.value}\n\n`));assert.ok(msg.includes(name));
  assert.ok(msg.includes(`Créditos necessários: ${credits} crédito`));
  if(seconds<60)assert.ok(msg.includes(`${seconds} segundo`));
 }
}
text.value='<script>alert("teste")</script> & orçamento?\nOlá, cliente!';text.events.input();
assert.ok(!result.innerHTML.includes('<script>'));assert.ok(new URL(link.href).searchParams.get('text').includes(text.value));
text.value=' \n\t ';text.events.input();assert.match(result.textContent,/Digite um texto/);assert.ok(!link.dataset.service);assert.ok(!new URL(link.href).searchParams.get('text').includes('Roteiro:'));
const pages=fs.readdirSync('.',{recursive:true}).filter(p=>p.endsWith('.html')&&!p.startsWith('node_modules')&&fs.readFileSync(p,'utf8').includes('id="calc-text"'));
for(const path of pages){
 const html=fs.readFileSync(path,'utf8');
 assert.equal((html.match(/id="calc-text"/g)||[]).length,1,path);
 assert.ok(html.includes('Solicitar pelo WhatsApp'),path);
 assert.ok(html.includes('Valor sujeito à confirmação após análise do roteiro.'),path);
 assert.doesNotMatch(html,/Referência: 150 palavras|O botão leva apenas serviço/);
 assert.ok(html.includes('/assets/nova.css?v=20261027calculator'),path);
 assert.ok(html.includes('/assets/nova.js?v=20261027calculator'),path);
}
console.log(`PASS: ${pages.length} shared calculators, live events, rounding boundaries, selected prices, empty input and full WhatsApp script.`);
