const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('assets/nova.js','utf8');
const text={value:'',events:{},addEventListener(n,f){this.events[n]=f}},service={value:'off',events:{},addEventListener(n,f){this.events[n]=f}},result={},link={};
vm.runInNewContext(source,{document:{querySelector:s=>({'#calc-text':text,'#calc-service':service,'#calc-result':result,'#calc-whatsapp':link}[s]||null),querySelectorAll:()=>[],addEventListener(){}},navigator:{},window:{addEventListener(){}},encodeURIComponent});
for(const [words,seconds,blocks] of [[1,1,1],[100,40,1],[101,41,2],[200,80,2],[201,81,3],[300,120,3],[301,121,4]]){
 text.value=('palavra\n').repeat(words);text.events.input();
 assert.ok(result.textContent.includes(`${words} palavras · aproximadamente ${seconds} segundos · ${blocks} faixa`));
 const msg=new URL(link.href).searchParams.get('text');assert.ok(msg.includes(`R$ ${(blocks*12).toFixed(2).replace('.',',')}`));assert.ok(!msg.includes('palavra\npalavra'));
 service.value='producao';service.events.change();assert.ok(new URL(link.href).searchParams.get('text').includes(`R$ ${(blocks*25).toFixed(2).replace('.',',')}`));
 service.value='off';
}
text.value=' \n\t ';text.events.input();assert.ok(!result.textContent.includes('R$ 0'));assert.ok(!link.href.includes('R%24'));
const manifest=JSON.parse(fs.readFileSync('reports/reformulacao-2026-10-26/manifesto.json'));
const services=JSON.parse(fs.readFileSync('data/premium-services.json'));
for(const s of services){
 const p=fs.readFileSync(`${s.slug}/index.html`,'utf8');assert.ok(p.includes(s.price));assert.ok(p.includes(s.limits));assert.ok(p.includes('"@type": "Service"'));
 assert.equal((p.match(/<h1[ >]/g)||[]).length,1);assert.ok(manifest.find(x=>x.path===`${s.slug}/index.html`&&x.index));
}
assert.equal(new Set(manifest.map(x=>x.path)).size,manifest.length);
console.log('PASS: calculator boundaries, selected-service WhatsApp estimate, empty input, no script leakage, seven scoped pages and unique manifest.');
// Service samples must remain distinct from profile samples and specialized pricing.
const demos=JSON.parse(fs.readFileSync('data/service-demos.json'));
const samplePaths=[];
for(const [slug,demo] of Object.entries(demos)){
 const page=fs.readFileSync(`${slug}/index.html`,'utf8');
 assert.ok(page.includes('id="demonstrativos-servico"'));
 assert.ok(!page.includes('id="calc-text"'));
 const players=[...page.matchAll(/<audio\b[^>]*>/g)].map(x=>x[0]);
 assert.equal(players.length,demo.tracks.length);
 for(const track of demo.tracks){
  assert.ok(fs.statSync('.'+track.src).size>0);samplePaths.push(track.src);
  assert.equal(players.filter(p=>p.includes(`src="${track.src}"`)&&p.includes('preload="none"')&&!p.includes('autoplay')).length,1);
  assert.ok(track.duration_seconds>0);
 }
 assert.ok(page.includes(demo.tracks.length===1?'Ouvir demonstração — Off':'Versão Produzida'));
}
assert.equal(samplePaths.length,8);assert.equal(new Set(samplePaths).size,8);
for(const [slug,selected] of [['','off'],['locucao-off','off'],['locucao_off','off'],['spot-comercial','producao'],['spot_comercial','producao'],['precos','off']]){
 const page=fs.readFileSync(slug?`${slug}/index.html`:'index.html','utf8');
 assert.equal((page.match(/id="calc-text"/g)||[]).length,1);
 assert.ok(page.includes(`value="${selected}" selected`));
 assert.ok(page.indexOf('id="precos"')<page.indexOf('id="calculadora"'));
}
for(const slug of ['espera-telefonica-ura','locucao-para-video-institucional']){
 const page=fs.readFileSync(`${slug}/index.html`,'utf8');assert.ok(page.includes('id="demonstrativos-servico"'));assert.ok(!page.includes('id="calc-text"'));assert.ok(!page.includes('id="precos"'));
}
assert.ok(fs.readFileSync('servicos/index.html','utf8').includes('Calcular minha peça comercial'));
console.log('PASS: eight real service files, correct player counts, no specialized commercial calculator, canonical/compatibility defaults and homepage price-to-calculator order.');
