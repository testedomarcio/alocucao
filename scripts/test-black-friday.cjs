const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const html=fs.readFileSync('spot-black-friday/index.html','utf8');
const code=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).find(s=>s.includes('const ended'));
for(const [now,expired] of [['2026-10-21T12:00:00-03:00',false],['2026-11-10T23:59:59-03:00',false],['2026-11-11T00:00:00-03:00',true]]){
 const nodes=new Map([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],{hidden:true,textContent:''}]));const normal=[{dataset:{normal:'R$ 11,90'},textContent:'R$ 8,90'},{dataset:{normal:'R$ 29,90'},textContent:'R$ 16,90'}];const old=[{hidden:false}];
 vm.runInNewContext(code,{Date:{now:()=>Date.parse(now),parse:Date.parse},document:{getElementById:id=>{assert(nodes.has(id),'Missing element '+id);return nodes.get(id)},querySelectorAll:s=>s==='[data-normal]'?normal:old}});
 assert.equal(!nodes.get('expired').hidden,expired);assert.equal(normal[0].textContent,expired?'R$ 11,90':'R$ 8,90');assert.equal(normal[1].textContent,expired?'R$ 29,90':'R$ 16,90');
}
console.log('PASS: Black Friday active, final second in Brasília and expiry return regular prices without errors.');
