(() => {
 'use strict';
 const normalize=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const track=(name,params)=>window.alocucaoTrackEvent?.(name,{page_path:location.pathname,service_name:'banco_unificado',...params});
 document.addEventListener('play',event=>{if(event.target instanceof HTMLMediaElement)document.querySelectorAll('audio').forEach(other=>{if(other!==event.target)other.pause()})},true);
 const source='/assets/voices-catalog.json';
 let catalogPromise;
 const fetchCatalog=()=>catalogPromise ||= fetch(source,{cache:'no-store',signal:AbortSignal.timeout(15000)}).then(r=>{if(!r.ok)throw Error('Catálogo indisponível');return r.json()}).then(data=>{
  if(data.schemaVersion!==1||!Array.isArray(data.voices)||data.count!==data.voices.length||!Number.isFinite(Date.parse(data.fetchedAt)))throw Error('Catálogo inválido');
  const ids=new Set();
  for(const v of data.voices){
   if(typeof v.id!=='string'||ids.has(v.id)||!v.name||!Array.isArray(v.styles)||!v.styles.every(s=>typeof s==='string'))throw Error('Perfil inválido');ids.add(v.id);
   for(const value of [v.audio,v.photo].filter(Boolean)){const u=new URL(value);if(u.protocol!=='https:'||u.hostname!=='vozes.alocucao.com.br'||u.username||u.password||!['/midia.php','/download-audio.php'].includes(u.pathname))throw Error('Mídia inválida');}
  }return data;
 });
 const node=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e};
 function humanRow(v,origin){
  const row=node('article','uv-row');Object.assign(row.dataset,{id:v.id,name:v.name,gender:v.type||'',styles:v.styles.join('|')});
  const avatar=node('div','uv-avatar');
  if(v.photo){const img=node('img');Object.assign(img,{src:v.photo,alt:'Perfil do locutor '+v.name,width:56,height:56,loading:'lazy',decoding:'async'});avatar.append(img)}
  else avatar.textContent=v.name.trim().charAt(0);
  const identity=node('div','uv-identity');identity.append(node('h3','',v.name),node('p','uv-meta',[v.type,...v.styles].filter(Boolean).join(' · ')),node('p','uv-description',v.styles.length?'Interpretações disponíveis: '+v.styles.join(', ')+'.':'Ouça a demonstração para conhecer o estilo desta voz.'),node('span','uv-status','Disponibilidade sob consulta'));
  const controls=node('div','uv-controls'),button=node('button','uv-play','▶ Ouvir');button.type='button';button.setAttribute('aria-label','Ouvir '+v.name);
  const audio=node('audio','uv-audio');audio.controls=true;audio.preload='none';audio.hidden=true;audio.dataset.src=v.audio;audio.dataset.voice=v.name;audio.setAttribute('aria-label','Demonstração de '+v.name);
  const choose=node('a','uv-choose','Escolher esta voz');choose.href='https://wa.me/5527996529832?text='+encodeURIComponent('Olá! Gostei da voz humana '+v.name+' no site A Locução e gostaria de solicitar uma gravação. Origem: https://alocucao.com.br'+origin+'. Podem me orientar?');choose.target='_blank';choose.rel='noopener noreferrer';Object.assign(choose.dataset,{cta:'unified_human_'+v.id,voiceName:v.name,voiceKind:'human'});
  const error=node('p','uv-error','Não foi possível carregar a demonstração. Solicite o áudio pelo WhatsApp.');error.hidden=true;error.setAttribute('role','status');controls.append(button,audio,choose);row.append(avatar,identity,controls,error);return row;
 }
 document.querySelectorAll('.uv-catalog').forEach(root=>{
  const panels=[];let lastStatusCheck='0',liveAt=0,statusLoading=false,liveFailed=false;const liveStates=new Map();
  function applyLiveStatuses(){
   if(liveFailed){const panel=root.querySelector('.uv-panel[data-kind="human"]');if(panel){panel.querySelectorAll('.uv-status').forEach(status=>{status.textContent='Disponibilidade sob consulta';status.classList.remove('uv-online')});panel.querySelector('.uv-sync').textContent='Consulta direta temporariamente indisponível. Confirme o status pelo WhatsApp.';}return;}
   if(!liveAt||Date.now()-liveAt>90000)return;
   root.querySelectorAll('.uv-panel[data-kind="human"] .uv-row').forEach(row=>{const state=liveStates.get(row.dataset.id);if(!state)return;const status=row.querySelector('.uv-status');status.textContent=state.label;status.classList.toggle('uv-online',state.online)});
   const sync=root.querySelector('.uv-panel[data-kind="human"] .uv-sync');
   if(sync)sync.textContent='Disponibilidade consultada diretamente na fonte oficial. Confirme o prazo ao pedir.';
  }
  async function refreshLiveStatuses(){
   const panel=root.querySelector('.uv-panel[data-kind="human"]');if(!panel||statusLoading||document.hidden)return;statusLoading=true;
   try{
    const response=await fetch('https://vozes.alocucao.com.br/check_status.php?loja=382&last_check='+encodeURIComponent(lastStatusCheck),{cache:'no-store',credentials:'omit',signal:AbortSignal.timeout(10000)});
    if(!response.ok)throw Error('Status indisponível');const data=await response.json();
    if(data.success!==true||!Array.isArray(data.data)||typeof data.current_timestamp!=='string'||!/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(data.current_timestamp))throw Error('Status inválido');
    for(const item of data.data){if(!/^\d+$/.test(String(item.id))||typeof item.status_display!=='string'||item.status_display.length>200||!Number.isInteger(Number(item.status_id)))throw Error('Perfil de status inválido');}
    for(const item of data.data)liveStates.set('vl-'+item.id,{label:item.status_display,online:Number(item.status_id)>=0&&Number(item.status_id)<=7});
    lastStatusCheck=data.current_timestamp;liveAt=Date.now();liveFailed=false;applyLiveStatuses();
   }catch(_){liveAt=0;liveFailed=true;lastStatusCheck='0';liveStates.clear();panel.querySelectorAll('.uv-status').forEach(status=>{status.textContent='Disponibilidade sob consulta';status.classList.remove('uv-online')});panel.querySelector('.uv-sync').textContent='Consulta direta temporariamente indisponível. Confirme o status pelo WhatsApp.';
   }finally{statusLoading=false;}
  }
  root.querySelectorAll('.uv-panel').forEach(panel=>{
   const list=panel.querySelector('.uv-list'),search=panel.querySelector('.uv-search'),gender=panel.querySelector('.uv-gender'),style=panel.querySelector('.uv-style'),count=panel.querySelector('.uv-count'),more=panel.querySelector('.uv-more');
   let rows=[...list.querySelectorAll('.uv-row')],shown=12;const order=new Map();
   const rank=row=>{if(!order.has(row.dataset.id))order.set(row.dataset.id,Math.random());return order.get(row.dataset.id)};
   function sort(){rows.forEach(rank);rows.sort((a,b)=>rank(a)-rank(b));list.append(...rows)}
   function filter(){const terms=normalize(search.value).trim().split(/\s+/).filter(Boolean);const matches=rows.filter(row=>(!gender.value||row.dataset.gender===gender.value)&&(!style.value||row.dataset.styles.split('|').includes(style.value))&&terms.every(term=>normalize(row.dataset.name+' '+row.dataset.styles+' '+row.querySelector('.uv-description').textContent).includes(term)));const visible=new Set(matches.slice(0,shown));rows.forEach(row=>{row.hidden=!visible.has(row);if(row.hidden)row.querySelector('audio')?.pause()});count.textContent=matches.length+' vozes encontradas · mostrando '+Math.min(shown,matches.length);more.hidden=shown>=matches.length;panel.querySelector('.uv-empty').hidden=!!matches.length;}
   panel.querySelector('.uv-filters').hidden=false;
   [search,gender,style].forEach(el=>el.addEventListener(el===search?'input':'change',()=>{shown=12;filter();if(el!==search)track('voice_filter_select',{voice_kind:panel.dataset.kind,filter_value:el.value||'todos'})}));
   panel.querySelector('.uv-clear').addEventListener('click',()=>{search.value=gender.value=style.value='';shown=12;filter();search.focus()});more.addEventListener('click',()=>{shown+=12;filter()});
   sort();filter();
   async function refresh(){if(panel.dataset.kind!=='human')return;const sync=panel.querySelector('.uv-sync');
    try{const data=await fetchCatalog();if([...root.querySelectorAll('audio')].some(a=>!a.paused))return;
     const fragment=document.createDocumentFragment();rows=data.voices.map(v=>humanRow(v,root.dataset.origin));rows.forEach(row=>fragment.append(row));list.replaceChildren(fragment);
     const selected=style.value;style.replaceChildren(new Option('Todos os estilos',''));[...new Set(data.voices.flatMap(v=>v.styles))].sort().forEach(s=>style.add(new Option(s,s)));style.value=selected;
     const stale=Date.now()-Date.parse(data.fetchedAt)>45*60000;const byId=new Map(data.voices.map(v=>[v.id,v]));rows.forEach(row=>{const v=byId.get(row.dataset.id),status=row.querySelector('.uv-status');status.textContent=stale?'Disponibilidade sob consulta':v.statusLabel||'Sob consulta';status.classList.toggle('uv-online',!stale&&v.status==='recording_online')});
     sync.textContent='Atualização automática: '+new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',dateStyle:'short',timeStyle:'short'}).format(new Date(data.fetchedAt))+'. '+(stale?'Status sob consulta; confirme pelo WhatsApp.':'Condições da fonte oficial; confirme o prazo ao pedir.');sort();filter();applyLiveStatuses();
    }catch(_){rows.forEach(row=>{const status=row.querySelector('.uv-status');status.textContent='Disponibilidade sob consulta';status.classList.remove('uv-online')});sync.textContent='Não foi possível atualizar agora. Ouça as demonstrações disponíveis e confirme a disponibilidade pelo WhatsApp.';}}
   panels.push({panel,refresh});refresh();
  });
  const tabs=[...root.querySelectorAll('[data-tab]')];
  function activate(kind,focus=false){root.dataset.active=kind;tabs.forEach(tab=>{const active=tab.dataset.tab===kind;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;if(active&&focus)tab.focus()});root.querySelectorAll('.uv-panel').forEach(panel=>{if(panel.dataset.kind!==kind&&matchMedia('(max-width:800px)').matches)panel.querySelectorAll('audio').forEach(a=>a.pause())})}
  tabs.forEach((tab,index)=>{tab.addEventListener('click',()=>activate(tab.dataset.tab));tab.addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;activate(tabs[next].dataset.tab,true)})});
  root.addEventListener('click',async event=>{const link=event.target.closest('.uv-choose');const button=event.target.closest('.uv-play');if(button){const row=button.closest('.uv-row'),audio=row.querySelector('audio'),error=row.querySelector('.uv-error');if(!audio.src){audio.src=audio.dataset.src;audio.hidden=false}if(!audio.paused){audio.pause();return}error.hidden=true;button.disabled=true;button.textContent='Carregando…';try{await audio.play()}catch(_){error.hidden=false;button.textContent='▶ Tentar novamente'}finally{button.disabled=false}}
   if(link)track('voice_select',{voice_name:link.dataset.voiceName,voice_kind:link.dataset.voiceKind,cta_id:link.dataset.cta});
  });
  root.addEventListener('play',event=>{const audio=event.target;if(!(audio instanceof HTMLMediaElement))return;document.querySelectorAll('audio').forEach(other=>{if(other!==audio)other.pause()});const row=audio.closest('.uv-row');row.querySelector('.uv-play').textContent='❚❚ Pausar';row.querySelector('.uv-error').hidden=true;track('voice_demo_play',{voice_name:audio.dataset.voice,voice_kind:row.closest('.uv-panel').dataset.kind})},true);
  root.addEventListener('change',event=>{if(!event.target.matches('.uv-demo-select'))return;const row=event.target.closest('.uv-row'),audio=row.querySelector('audio');audio.pause();audio.removeAttribute('src');audio.load();audio.hidden=true;audio.dataset.src=event.target.value;row.querySelector('.uv-play').textContent='▶ Ouvir';row.querySelector('.uv-error').hidden=true;});
  for(const name of ['pause','ended'])root.addEventListener(name,event=>{const button=event.target.closest('.uv-row')?.querySelector('.uv-play');if(button)button.textContent='▶ Ouvir'},true);
  root.addEventListener('error',event=>{if(event.target.matches?.('.uv-avatar img')){const avatar=event.target.parentElement;avatar.textContent=avatar.closest('.uv-row')?.dataset.name.trim().charAt(0)||'?';return;}if(!(event.target instanceof HTMLMediaElement))return;const row=event.target.closest?.('.uv-row');if(row){row.querySelector('.uv-error').hidden=false;row.querySelector('.uv-play').textContent='▶ Tentar novamente'}},true);
  const refresh=()=>{catalogPromise=undefined;panels.forEach(p=>p.refresh());refreshLiveStatuses()};setInterval(()=>{if(!document.hidden)refresh()},5*60000);document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh()});
  if(panels.some(p=>p.panel.dataset.kind==='human')){refreshLiveStatuses();setInterval(refreshLiveStatuses,30000);}
  root.querySelectorAll('.uv-avatar img').forEach(img=>{if(img.complete&&img.naturalWidth===0)img.parentElement.textContent=img.closest('.uv-row').dataset.name.trim().charAt(0);});
 });
})();
