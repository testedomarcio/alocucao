const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('assets/voice-bank-view.js','utf8');
function setup(width,saved,blocked=false){
 const events={},buttons=['list','cards'].map(view=>({dataset:{voiceView:view},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f}}));
 const control={hidden:true,querySelectorAll:()=>buttons};const root={dataset:{}};
 const media={matches:width>=1100,addEventListener(k,f){this.change=f}};const savedWrites=[];
 const document={documentElement:root,querySelectorAll:()=>buttons,querySelector:()=>control,addEventListener(k,f){events[k]=f}};
 vm.runInNewContext(source,{document,matchMedia:()=>media,localStorage:{getItem(){if(blocked)throw Error();return saved},setItem(k,v){if(blocked)throw Error();savedWrites.push(v)}}});
 events.DOMContentLoaded();return {root,media,buttons,control,savedWrites};
}
for(const width of [320,360,600,820,1024,1100,1440]){
 const t=setup(width);assert.equal(t.root.dataset.voiceView,width>=1100?'list':'cards');assert.equal(t.control.hidden,false);
 for(const view of ['list','cards']){const b=t.buttons.find(b=>b.dataset.voiceView===view);b.events.click();assert.equal(t.root.dataset.voiceView,view);assert.equal(b.attrs['aria-pressed'],'true');t.media.matches=!t.media.matches;t.media.change();assert.equal(t.root.dataset.voiceView,view)}
 for(const saved of ['list','cards'])assert.equal(setup(width,saved).root.dataset.voiceView,saved);
 assert.equal(setup(width,'invalid').root.dataset.voiceView,width>=1100?'list':'cards');
 const blocked=setup(width,null,true);blocked.buttons[0].events.click();assert.equal(blocked.root.dataset.voiceView,'list');
}
console.log('PASS: responsive defaults, both choices, persistence, invalid/blocked storage, resize respects explicit choice, accessible pressed state.');
