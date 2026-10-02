const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const code = fs.readFileSync(require('node:path').join(__dirname,'../assets/tracking.js'),'utf8');
function setup({saved, memory, blocked=false, path='/perfil-locutor-alan/'}={}) {
  const events={}, clicks={}, tags=[], storage=new Map();
  class Element { constructor(href='https://wa.me/5527996529832'){this.href=href;this.dataset={cta:'teste'};this.textContent='Escolher este locutor';} closest(){return this;} getAttribute(){return null;} }
  const window={location:{pathname:path,search:'',href:'https://alocucao.com.br'+path}, alocucaoConsent:memory,addEventListener:(n,f)=>events[n]=f};
  const document={title:'Teste',referrer:'',head:{appendChild:s=>tags.push(s)},createElement:()=>({}),addEventListener:(n,f)=>clicks[n]=f};
  const context={window,document,Element,URL,URLSearchParams,Date,localStorage:{getItem:()=>{if(blocked)throw Error('blocked');return saved;}},sessionStorage:{getItem:k=>storage.get(k),setItem:(k,v)=>storage.set(k,v)}};
  vm.runInNewContext(code,context);
  const calls=()=>window.dataLayer.map(x=>Array.from(x));
  return {window,tags,calls,storage,consent:v=>events['alocucao:consent']({detail:{value:v}}),click:href=>clicks.click({target:new Element(href)})};
}
const t=setup();t.click();assert.equal(t.tags.length,0);assert.equal(t.storage.size,0);assert.equal(t.calls().filter(x=>x[0]==='event').length,0);
t.consent('accepted');assert.equal(t.tags.length,1);assert.match(t.tags[0].src,/G-TBHF64CH1R/);
const granted=t.calls().findIndex(x=>x[0]==='consent'&&x[1]==='update'&&x[2].analytics_storage==='granted');const config=t.calls().findIndex(x=>x[0]==='config');assert(granted<config);
t.consent('accepted');assert.equal(t.tags.length,1);t.click();let measured=t.calls().filter(x=>x[0]==='event');assert.equal(measured.length,1);assert.equal(measured[0][1],'whatsapp_click');assert.equal(measured[0][2].send_to,'G-TBHF64CH1R');assert.equal(measured[0][2].service_name,'perfil_locutor');
t.click('https://wa.me.evil.example/');assert.equal(t.calls().filter(x=>x[0]==='event').length,1);
t.consent('rejected');t.click();assert.equal(t.calls().filter(x=>x[0]==='event').length,1);assert.equal(t.calls().filter(x=>x[0]==='consent').at(-1)[2].analytics_storage,'denied');
assert.equal(setup({saved:'accepted'}).tags.length,1);assert.equal(setup({memory:'accepted',blocked:true}).tags.length,1);assert.equal(setup({saved:'rejected'}).tags.length,0);
for(const [path,service] of [['/produtora-de-audio-sao-paulo/','servico_regional'],['/spot-black-friday/','spot_black_friday'],['/espera-telefonica-ura/','ura_telefonica'],['/locucao-off/','locucao_off']]){const x=setup({saved:'accepted',path});x.click();assert.equal(x.calls().find(c=>c[0]==='event')[2].service_name,service);}
console.log('PASS: consent denied/granted/revoked, saved consent, blocked storage, single loader, single WhatsApp event, hostname allowlist and service classification.');
