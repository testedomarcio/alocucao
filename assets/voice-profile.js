(() => {
 'use strict';
 const id=document.body.dataset.voiceId,audio=document.getElementById('profile-audio'),status=document.getElementById('profile-status'),stamp=document.getElementById('profile-sync'),schedule=document.getElementById('profile-schedule');
 const days=['Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo'];
 const format=new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'});
 const el=(tag,text)=>{const node=document.createElement(tag);node.textContent=text;return node;};
 function personalizePanel(){
  const choose=document.querySelector('[data-cta="perfil_escolher"]');if(!choose)return;
  const bar=document.querySelector('.wa-mobile-conversion-bar a');
  if(bar){bar.href=choose.href;bar.textContent=choose.textContent.replace(' ↗','');bar.dataset.cta='perfil_barra_mobile';}
 }
 personalizePanel();
 if(document.readyState!=='complete')document.addEventListener('DOMContentLoaded',personalizePanel,{once:true});
 let loading=false;
 async function refresh(){
  if(loading)return;loading=true;
  try{
   const response=await fetch('/assets/voices-catalog.json?v='+Math.floor(Date.now()/600000),{cache:'no-cache',signal:AbortSignal.timeout(15000)});if(!response.ok)throw Error('Catalog unavailable');
   const data=await response.json();if(data.schemaVersion!==1||!Array.isArray(data.voices)||!Number.isFinite(Date.parse(data.fetchedAt)))throw Error('Invalid catalog');
   const voice=data.voices.find(v=>v.id===id);
   if(!voice){status.textContent='Esta voz não está no catálogo atual. Consulte outras opções no banco de vozes.';stamp.textContent='';return;}
   const age=Date.now()-Date.parse(data.fetchedAt),fresh=age>=0&&age<3*60*60*1000;
   status.textContent=fresh&&typeof voice.statusLabel==='string'?voice.statusLabel:'Disponibilidade sob consulta';
   stamp.textContent='Consulta do catálogo: '+format.format(new Date(data.fetchedAt))+' (Brasília)';
   const source=new URL(voice.audio);if(source.protocol!=='https:'||source.hostname!=='hd.paineldegravacao.com.br'||source.username||source.password)throw Error('Invalid audio');
   if(audio.paused&&!audio.currentTime){if(audio.getAttribute('src')!==source.href)audio.src=source.href;}
   if(Array.isArray(voice.schedule)&&voice.schedule.length<=7){
    const valid=voice.schedule.every(d=>days.includes(d.day)&&Array.isArray(d.intervals)&&d.intervals.length<=8&&d.intervals.every(i=>/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(i.start)&&/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(i.end)));
    if(valid){
     if(voice.schedule.length){const list=document.createElement('ul');list.className='profile-hours';voice.schedule.forEach(d=>{const row=document.createElement('li');row.append(el('strong',d.day),el('span',d.intervals.map(i=>i.start+'–'+i.end).join(' · ')));list.append(row)});schedule.replaceChildren(list);}
     else schedule.replaceChildren(el('p','O perfil de origem não informou uma agenda de gravação válida. Confira os horários no painel.'));
    }
   }
  }catch(_){status.textContent='Disponibilidade sob consulta';stamp.textContent='Atualização temporariamente indisponível';}
  finally{loading=false;}
 }
 audio.addEventListener('error',()=>{document.getElementById('profile-audio-error').hidden=false});
 audio.addEventListener('playing',()=>{document.getElementById('profile-audio-error').hidden=true});
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh()});
 setInterval(()=>{if(!document.hidden)refresh()},15*60*1000);refresh();
})();
