const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const tracking=fs.readFileSync('assets/tracking.js','utf8');
function setup(saved,path='/locutores/amanda-kelly/'){
 const events={},clicks={},tags=[],storage=new Map();
 class Element{constructor(href='https://wa.me/5527996529832'){this.href=href;this.dataset={cta:'voice',voiceName:'Amanda Kelly'};this.textContent='Contratar esta voz';}closest(){return this}getAttribute(){return null}}
 const window={location:{pathname:path,search:'?utm_source=bing&utm_campaign=teste',href:'https://alocucao.com.br'+path},addEventListener:(n,f)=>events[n]=f};
 const document={title:'Perfil Amanda',referrer:'',head:{appendChild:s=>tags.push(s)},createElement:()=>({}),addEventListener:(n,f)=>clicks[n]=f};
 vm.runInNewContext(tracking,{window,document,Element,URL,URLSearchParams,Date,localStorage:{getItem:()=>saved},sessionStorage:{getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)}});
 return {window,tags,storage,consent:v=>events['alocucao:consent']({detail:{value:v}}),click:href=>clicks.click({target:new Element(href)}),events:()=>window.dataLayer.map(c=>Array.from(c)).filter(c=>c[0]==='event' && c[1]==='whatsapp_click')};
}
let t=setup();t.click();assert.equal(t.tags.length,0);assert.equal(t.events().length,0);assert.equal(t.storage.size,0);
t.consent('accepted');t.consent('accepted');assert.equal(t.tags.length,2);t.click();assert.equal(t.events().length,1);
const lead=t.events()[0][2];assert.equal(lead.service_name,'perfil_locutor');assert.equal(lead.voice_name,'Amanda Kelly');assert.equal(lead.voice_kind,'synthetic');assert.equal(lead.traffic_source,'bing');assert.equal(lead.campaign_name,'teste');
t.click('https://wa.me.evil.example/');assert.equal(t.events().length,1);t.consent('rejected');t.click();assert.equal(t.events().length,1);
assert.equal(setup('rejected').tags.length,0);assert.equal(setup('accepted').tags.length,2);
for(const [path,service] of [['/','pagina_inicial'],['/vozes/','banco_de_vozes'],['/locucao-off/','locucao_off'],['/spot-black-friday/','spot_black_friday'],['/gravacao-off-e-producao/','off_producao']]){const x=setup('accepted',path);x.click();assert.equal(x.events()[0][2].service_name,service)}
console.log('PASS: consent, revocation, one WhatsApp event, attribution, voice and page classification.');
// Exercise real filter handlers with accented names, combined filters, empty results and reset.
function node(value=''){return {value,hidden:false,events:{},addEventListener(n,f){this.events[n]=f},focus(){this.focused=true}}}
const search=node(),gender=node(),style=node(),reset=node();
const cards=[{dataset:{search:'Mário Comercial',gender:'Masculina',tags:'Comercial|Energética'},hidden:false},{dataset:{search:'Amanda Kelly Suave',gender:'Feminina',tags:'Comercial|Suave'},hidden:false}];
const count=node(),empty=node();const form={hidden:true,events:{},querySelector:s=>({'input':search,'#gender':gender,'#style':style,'button':reset}[s]),addEventListener(n,f){this.events[n]=f},reset(){search.value='';gender.value='';style.value=''}};
const doc={querySelector:s=>s==='.filters'?form:s==='#voice-count'?count:s==='#empty-voices'?empty:null,querySelectorAll:s=>s==='.voice-card'?cards:[],addEventListener(){}};
vm.runInNewContext(fs.readFileSync('assets/nova.js','utf8'),{document:doc,navigator:{},window:{addEventListener(){}}});
search.value='mario';form.events.input();assert.deepEqual(cards.map(c=>c.hidden),[false,true]);
search.value='';gender.value='Feminina';style.value='Suave';form.events.change();assert.deepEqual(cards.map(c=>c.hidden),[true,false]);
search.value='none';form.events.input();assert.equal(empty.hidden,false);reset.events.click();assert.deepEqual(cards.map(c=>c.hidden),[false,false]);assert.equal(search.focused,true);assert.equal(form.hidden,false);
console.log('PASS: accented search, gender/style combination, empty state and reset.');
let playHandler;const audios=[{tagName:'AUDIO',addEventListener(){},pause(){this.paused=true}},{tagName:'AUDIO',addEventListener(){},pause(){this.paused=true}}];
vm.runInNewContext(fs.readFileSync('assets/nova.js','utf8'),{document:{querySelector:()=>null,querySelectorAll:s=>s==='audio'?audios:[],addEventListener:(name,handler)=>{if(name==='play')playHandler=handler}},navigator:{},window:{addEventListener(){}}});
playHandler({target:audios[0]});assert.equal(audios[1].paused,true);assert.equal(audios[0].paused,undefined);
console.log('PASS: starting one demo pauses other players.');
// A known random sequence changes order without adding or losing voices; restored pages reshuffle.
const grid={children:[{name:'A'},{name:'B'},{name:'C'}],appendChild(card){this.children=this.children.filter(x=>x!==card);this.children.push(card)}};
let restored;
vm.runInNewContext(fs.readFileSync('assets/nova.js','utf8'),{document:{querySelector:()=>null,querySelectorAll:s=>s==='.voice-grid'?[grid]:[],addEventListener(){}},navigator:{},window:{addEventListener:(n,f)=>{if(n==='pageshow')restored=f}},Math:{random:()=>0,floor:Math.floor}});
assert.deepEqual(grid.children.map(c=>c.name),['A','B','C']);
const catalogHtml=fs.readFileSync('vozes/index.html','utf8');
const inline=catalogHtml.split('<script>')[1].split('</script>')[0];
grid.parentElement={querySelector:()=>null};
vm.runInNewContext(inline,{document:{currentScript:{previousElementSibling:grid}},Math:{random:()=>0,floor:Math.floor}});
assert.deepEqual(grid.children.map(c=>c.name),['B','C','A']);
restored({persisted:true});assert.deepEqual(grid.children.map(c=>c.name),['C','A','B']);assert.equal(new Set(grid.children).size,3);
console.log('PASS: initial random order and back/forward restore preserve every voice exactly once.');
// Language filtering combines with existing filters and resets to the whole catalog.
{
 const search=node(),gender=node(),style=node(),language=node(),reset=node(),count=node(),empty=node();
 const cards=[{dataset:{search:'Voz Brasileira',gender:'Masculina',tags:'Comercial',language:'pt-BR'}},{dataset:{search:'Lucan Rook English US Inglês Americano',gender:'Masculina',tags:'Comercial|Energética',language:'en-US'}}];
 const form={hidden:true,events:{},querySelector:s=>({'input':search,'#gender':gender,'#style':style,'#language':language,'button':reset}[s]),addEventListener(n,f){this.events[n]=f},reset(){search.value='';gender.value='';style.value='';language.value=''}};
 const document={querySelector:s=>s==='.filters'?form:s==='#voice-count'?count:s==='#empty-voices'?empty:null,querySelectorAll:s=>s==='.voice-card'?cards:[],addEventListener(){}};
 vm.runInNewContext(fs.readFileSync('assets/nova.js','utf8'),{document,navigator:{},window:{addEventListener(){}}});
 language.value='en-US';form.events.change();assert.deepEqual(cards.map(c=>c.hidden),[true,false]);assert.equal(count.textContent,'1 voz encontrada');
 gender.value='Feminina';form.events.change();assert.equal(empty.hidden,false);
 reset.events.click();assert.deepEqual(cards.map(c=>c.hidden),[false,false]);assert.equal(language.value,'');
 language.value='pt-BR';form.events.change();assert.deepEqual(cards.map(c=>c.hidden),[false,true]);
 const html=fs.readFileSync('vozes/index.html','utf8');
 for(const [code,label] of [['es-419','Espanhol latino-americano'],['fr-FR','Francês'],['it-IT','Italiano'],['de-DE','Alemão']])assert.ok(html.includes(`<option value="${code}" disabled>${label} (em breve)</option>`));
 assert.equal((html.match(/class="portrait-language"/g)||[]).length,1);
 console.log('PASS: Portuguese/English language filtering, combined filters, empty state, reset, disabled upcoming languages and one visible country flag.');
}
