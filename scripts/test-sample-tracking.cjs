const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function setup(consent){
 const handlers={};class Element{constructor(href,cta,label){this.href=href;this.dataset={cta,voiceName:'Christine'};this.textContent=label;}closest(){return this;}getAttribute(){return null;}}
 const window={location:{href:'https://alocucao.com.br/locutores/christine/',origin:'https://alocucao.com.br',pathname:'/locutores/christine/',search:''},addEventListener:(n,f)=>handlers[n]=f};
 const document={title:'Christine',referrer:'',head:{appendChild(){}},createElement:()=>({}),addEventListener:(n,f)=>handlers[n]=f};
 vm.runInNewContext(fs.readFileSync('assets/tracking.js','utf8'),{window,document,Element,URL,URLSearchParams,Date,localStorage:{getItem:()=>consent},sessionStorage:{getItem(){},setItem(){}}});
 return {click:(href,cta,label)=>handlers.click({target:new Element(href,cta,label)}),events:()=>Array.from(window.dataLayer,c=>Array.from(c)).filter(c=>c[0]==='event'),revoke:()=>handlers['alocucao:consent']({detail:{value:'rejected'}})};
}
let t=setup('accepted');t.click('https://wa.me/5527996529832?text=teste','solicitar_amostra','Amostra grátis');
assert.deepEqual(t.events().map(e=>e[1]),['solicitar_amostra_click','whatsapp_click']);
assert.equal(t.events()[1][2].cta_intent,'solicitar_amostra');assert.equal(t.events()[0][2].voice_name,'Christine');
t=setup('accepted');t.click('https://wa.me/5527996529832','orcamento','Contratar esta voz');assert.deepEqual(t.events().map(e=>e[1]),['contratar_locucao_click','whatsapp_click']);
t=setup('accepted');t.click('https://alocucao.com.br/locutores/christine/','','Ver perfil completo');assert.deepEqual(t.events().map(e=>e[1]),['escolher_voz_click']);
t=setup('rejected');t.click('https://wa.me/5527996529832','solicitar_amostra','Amostra');assert.equal(t.events().length,0);
t=setup('accepted');t.revoke();t.click('https://wa.me/5527996529832','solicitar_amostra','Amostra');assert.equal(t.events().length,0);
console.log('PASS: distinct sample/hire/voice interactions, exactly one WhatsApp event per contact, correct voice and no tracking after refusal/revocation.');
