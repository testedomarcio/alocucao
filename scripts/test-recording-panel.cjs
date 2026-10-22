const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const listeners={},frame={contentWindow:{},style:{minHeight:'640px'}},other={contentWindow:{},style:{minHeight:'640px'}};
const window={addEventListener:(key,callback)=>{assert(!listeners[key]);listeners[key]=callback;}};
const context={window,document:{querySelectorAll:()=>[frame,other]},Math,Number,Array};
const code=fs.readFileSync('assets/recording-panel.js','utf8');vm.runInNewContext(code,context);vm.runInNewContext(code,context);
function send(origin,data,source=frame.contentWindow){listeners.message({origin,data,source});}
const origin='https://vozes.alocucao.com.br';
for(const data of [null,[],{}, {vitrineVozes:true,altura:'1000'},{vitrineVozes:1,altura:1000}, {vitrineVozes:true,altura:Infinity},{vitrineVozes:true,altura:NaN},{vitrineVozes:true,altura:239},{vitrineVozes:true,altura:60001}])send(origin,data);
assert.equal(frame.style.height,undefined);
send('https://vozes.alocucao.com.br.evil.example',{vitrineVozes:true,altura:1000});
send(origin,{vitrineVozes:true,altura:1000},{});assert.equal(frame.style.height,undefined);
send(origin,{vitrineVozes:true,altura:1886.2});assert.equal(frame.style.height,'1887px');assert.equal(frame.style.minHeight,'0');assert.equal(other.style.height,undefined);
send(origin,{vitrineVozes:true,altura:700},other.contentWindow);assert.equal(other.style.height,'700px');assert.equal(frame.style.height,'1887px');
console.log('PASS: strict origin, sender window, typed payload and safe height range; repeated initializer and independent frames.');
