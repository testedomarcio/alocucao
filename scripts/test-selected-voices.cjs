const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
class Control {constructor(){this.value='';this.events={};this.hidden=false;this.textContent='';}addEventListener(k,f){this.events[k]=f;}focus(){this.focused=true;}}
const search=new Control(),gender=new Control(),style=new Control(),clear=new Control(),more=new Control(),count=new Control(),empty=new Control();
const controls={'.sv-search':search,'.sv-gender':gender,'.sv-style':style,'.sv-clear':clear,'.sv-more':more,'.sv-count':count,'.sv-empty':empty};
function card(name,g,s){const audio=new Control();audio.paused=true;audio.dataset={voice:name};audio.pause=()=>audio.paused=true;const error=new Control();error.hidden=true;return{hidden:false,dataset:{svName:name,svGender:g,svStyles:s},querySelector:q=>q==='audio'?audio:error};}
const cards=[card('Mário','Masculina','Padrão|Varejo'),card('Aida','Feminina','Animada'),...Array.from({length:6},(_,i)=>card('Voz '+i,i%2?'Feminina':'Masculina','Padrão'))];
const displayOrder=[];controls['.sv-grid']={appendChild:card=>displayOrder.push(card)};
const widget={querySelector:q=>controls[q],querySelectorAll:()=>cards};
const events={},tracked=[];
vm.runInNewContext(fs.readFileSync('assets/selected-voices.js','utf8'),{document:{querySelectorAll:q=>q==='[data-selected-voices]'?[widget]:[],addEventListener:(name,f)=>events[name]=f},window:{alocucaoTrackEvent:(...x)=>tracked.push(x)},location:{pathname:'/teste/',href:'https://alocucao.com.br/teste/'},Math:Object.assign(Object.create(Math),{random:()=>0}),URL,Element:class {},HTMLAudioElement:class {}});
assert.equal(displayOrder.length,cards.length);assert.equal(new Set(displayOrder).size,cards.length);assert.notDeepEqual(displayOrder,cards);
const initialOrder=[...displayOrder];
assert.equal(cards.filter(c=>!c.hidden).length,6);assert.equal(more.hidden,false);
more.events.click();assert.equal(cards.filter(c=>!c.hidden).length,8);assert.equal(more.hidden,true);
search.value='Mario';search.events.input();assert.equal(cards.filter(c=>!c.hidden).length,1);assert.equal(cards[0].hidden,false);
search.value='inexistente';search.events.input();assert.equal(empty.hidden,false);assert.equal(cards.filter(c=>!c.hidden).length,0);
clear.events.click();assert.equal(empty.hidden,true);assert.equal(cards.filter(c=>!c.hidden).length,6);
gender.value='Feminina';gender.events.change();assert.equal(cards.filter(c=>!c.hidden).length,4);
style.value='Animada';style.events.change();assert.equal(cards.filter(c=>!c.hidden).length,1);assert.equal(cards[1].hidden,false);
clear.events.click();cards[0].querySelector('audio').paused=false;search.value='Aida';search.events.input();assert.equal(cards[0].querySelector('audio').paused,true);
cards[1].querySelector('audio').events.play();assert.equal(tracked.length,1);assert.equal(tracked[0][0],'audio_play');
assert.deepEqual(displayOrder,initialOrder);
console.log('PASS: randomized initial order remains stable during filtering, accent-insensitive search, combined filters, empty results, pagination, reset, audio pause and non-conversion playback.');
