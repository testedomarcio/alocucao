const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('calculadora/index.html','utf8');
const code=[...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(x=>x.includes("const $ = id"));
const elements=new Map();
function el(id){if(!elements.has(id))elements.set(id,{value:'',textContent:'',style:{},dataset:{},classList:{add(){},remove(){}},addEventListener(n,f){this[n]=f},setAttribute(){},focus(){},scrollIntoView(){},hidden:false});return elements.get(id)}
const document={getElementById:el,querySelectorAll:()=>[],addEventListener(){}};
const window={addEventListener(){},alocucaoTrackEvent:()=>false};
vm.runInNewContext(code,{document,window,URL,URLSearchParams,Date,setTimeout:()=>1,clearTimeout(){},setInterval(){},navigator:{},console});
el('voice-speed').value='120';el('service').value='off';
for(const [n,seconds,credits] of [[20,10,1],[80,40,1],[81,41,2],[180,90,3]]){el('script-text').value=Array(n).fill('palavra').join(' ');el('calculate').click();assert.equal(el('blocks').textContent,credits);assert.equal(el('duration').textContent,`${Math.floor(seconds/60)}:${String(seconds%60).padStart(2,'0')}`)}
el('clear').click();assert.equal(el('script-text').value,'');
const panel=[...html.matchAll(/<a[^>]+id="panel-link"[^>]+>/g)];assert.equal(panel.length,1);assert.match(panel[0][0],/https:\/\/vozes.alocucao.com.br\/painel\/cadastro/);
console.log('PASS: calculator initializes, computes 1/2/3 credits and 40-second boundary, clears input, preserves one online CTA.');
