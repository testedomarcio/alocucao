const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('assets/voice-bank-view.js','utf8');
function setup(width,saved,blocked=false){
 const events={},buttons=['list','cards'].map(view=>({dataset:{voiceView:view},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f}}));
 const control={hidden:true,querySelectorAll:()=>buttons};const root={dataset:{}};
 const media={matches:width>=1100,addEventListener(k,f){this.change=f}};const savedWrites=[];
 const document={documentElement:root,querySelectorAll:()=>buttons,querySelector:s=>s==='.bank-view-switch'?control:null,addEventListener(k,f){events[k]=f}};
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
// Verify the single-panel lifecycle against the actual event handlers.
{
 const events={},form={events:{},addEventListener(k,f){this.events[k]=f}};
 const viewButtons=['list','cards'].map(view=>({dataset:{voiceView:view},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f}}));
 const control={hidden:true,querySelectorAll:()=>viewButtons};
 const grid={events:{},classList:{add(){}},addEventListener(k,f){this.events[k]=f},querySelectorAll:()=>records.map(r=>r.button)};
 const records=['a-off','a-producao','b-off'].map(id=>{
  const card={hidden:false,contains:()=>true},classes=new Set();
  const audio={paused:true,currentTime:12,plays:0,pause(){this.paused=true},play(){this.paused=false;this.plays++;grid.events.play({target:this});return Promise.resolve()}};
  const button={attrs:{'aria-controls':id},events:{},setAttribute(k,v){this.attrs[k]=v},getAttribute(k){return this.attrs[k]},addEventListener(k,f){this.events[k]=f},closest:()=>card,focus(){this.focused=true}};
  const closeButton={events:{},addEventListener(k,f){this.events[k]=f}};
  const panel={classList:{add:c=>classes.add(c),remove:c=>classes.delete(c)},querySelector:s=>s==='audio'?audio:closeButton};
  return {id,card,audio,button,panel,classes,closeButton};
 });
 const document={documentElement:{dataset:{}},querySelectorAll:()=>viewButtons,querySelector:s=>s==='.bank-view-switch'?control:s==='#voice-results'?grid:s==='.filters'?form:null,getElementById:id=>records.find(r=>r.id===id).panel,addEventListener(k,f){events[k]=f}};
 vm.runInNewContext(source,{document,matchMedia:()=>({matches:true,addEventListener(){}}),localStorage:{getItem(){},setItem(){}}});events.DOMContentLoaded();
 const [off,produced,other]=records;
 assert.equal(records.reduce((n,r)=>n+r.audio.plays,0),0,'No unsolicited playback');
 off.button.events.click();assert.equal(off.button.attrs['aria-expanded'],'true');assert.equal(off.audio.paused,false);
 produced.button.events.click();assert.equal(off.button.attrs['aria-expanded'],'false');assert.equal(off.audio.paused,true);assert.equal(produced.classes.has('is-open'),true);
 other.button.events.click();assert.equal(produced.audio.paused,true);assert.equal(records.filter(r=>r.classes.has('is-open')).length,1);
 other.button.events.click();assert.equal(records.filter(r=>r.classes.has('is-open')).length,0);assert.equal(other.audio.currentTime,12,'Collapsing preserves playback position');grid.events.play({target:other.audio});assert.equal(records.filter(r=>r.classes.has('is-open')).length,0,'A late play event from a collapsed audio must not reopen its panel');
 off.button.events.click();off.closeButton.events.click();assert.equal(off.audio.paused,true);assert.equal(off.button.focused,true);
 produced.button.events.click();grid.events.keydown({key:'Escape',target:produced.audio,preventDefault(){}});assert.equal(produced.button.attrs['aria-expanded'],'false');
 off.button.events.click();viewButtons[1].events.click();assert.equal(off.audio.paused,false,'Switching view preserves playback');viewButtons[0].events.click();assert.equal(off.classes.has('is-open'),true);
 off.card.hidden=true;form.events.input();assert.equal(off.audio.paused,true);assert.equal(off.classes.has('is-open'),false);
 console.log('PASS: demand-only playback, Off/Produced switching, one panel, pause/collapse, retained time, close focus, Escape, view continuity and filtering a playing voice.');
}
