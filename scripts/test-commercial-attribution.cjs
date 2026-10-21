const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const code = fs.readFileSync(require('node:path').join(__dirname, '../assets/commercial-refresh.js'), 'utf8');
class Element {
 constructor(href, kind) { this.href=href;this.dataset=kind?{voiceKind:kind}:{}; }
 closest(){return this;}
}
const links=[new Element('https://wa.me/5527996529832?text=Ol%C3%A1'),new Element('https://alocucao.com.br/locucao-off/#banco-de-vozes'),new Element('https://example.org/')];
const events={};const storage=new Map();
const context={URL,URLSearchParams,Element,location:{href:'https://alocucao.com.br/spot-comercial/?utm_source=bing&msclkid=abc',origin:'https://alocucao.com.br',search:'?utm_source=bing&msclkid=abc'},document:{body:{hasAttribute:()=>true},querySelectorAll:()=>links,addEventListener:(name,callback)=>events[name]=callback},sessionStorage:{getItem:key=>storage.get(key),setItem:(key,value)=>storage.set(key,value)}};
vm.runInNewContext(code,context);
for(const link of links.slice(0,2))assert.equal(new URL(link.href).searchParams.get('msclkid'),'abc');
assert.equal(new URL(links[0].href).searchParams.get('text'),'Olá');
assert.equal(new URL(links[1].href).hash,'#banco-de-vozes');
assert.equal(links[2].href,'https://example.org/');
assert.equal(links[0].dataset.voiceKind,'nao_informado');
const dynamic=new Element('https://wa.me/5527996529832?text=Voz','ia');events.click({target:dynamic});
assert.equal(new URL(dynamic.href).searchParams.get('utm_source'),'bing');assert.equal(dynamic.dataset.voiceKind,'ia');
context.location.search='';vm.runInNewContext(code,context);assert.equal(new URL(links[0].href).searchParams.get('msclkid'),'abc');
context.sessionStorage={getItem:()=>{throw Error('blocked')},setItem:()=>{throw Error('blocked')}};vm.runInNewContext(code,context);
console.log('PASS: attribution survives internal navigation, anchors, dynamic voice cards and blocked storage; external links and explicit voice types preserved.');
