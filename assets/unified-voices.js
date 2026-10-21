(() => {
 'use strict';
 const normalize=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 const track=(name,params)=>window.alocucaoTrackEvent?.(name,{page_path:location.pathname,service_name:'banco_unificado',...params});
 document.addEventListener('play',event=>{if(event.target instanceof HTMLMediaElement)document.querySelectorAll('audio').forEach(other=>{if(other!==event.target)other.pause()})},true);
 const node=(tag,cls,text)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e};
 document.querySelectorAll('.uv-catalog').forEach(root=>{
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
  });
  const tabs=[...root.querySelectorAll('[data-tab]')];
  function activate(kind,focus=false){root.dataset.active=kind;if(root.dataset.layout==='tabs')root.querySelectorAll('.uv-panel').forEach(panel=>{const active=panel.dataset.kind===kind;panel.hidden=!active;panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',panel.id+'-tab')});tabs.forEach(tab=>{const active=tab.dataset.tab===kind;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;if(active&&focus)tab.focus()});root.querySelectorAll('.uv-panel').forEach(panel=>{if(panel.dataset.kind!==kind&&(root.dataset.layout==='tabs'||matchMedia('(max-width:800px)').matches))panel.querySelectorAll('audio').forEach(a=>a.pause())})}
  if(root.dataset.layout==='tabs'){tabs.forEach(tab=>tab.id=tab.getAttribute('aria-controls')+'-tab');activate(root.dataset.active)}
  tabs.forEach((tab,index)=>{tab.addEventListener('click',()=>activate(tab.dataset.tab));tab.addEventListener('keydown',event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();const next=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;activate(tabs[next].dataset.tab,true)})});
  root.addEventListener('click',async event=>{const link=event.target.closest('.uv-choose');const button=event.target.closest('.uv-play');if(button){const row=button.closest('.uv-row'),audio=row.querySelector('audio'),error=row.querySelector('.uv-error');if(!audio.src){audio.src=audio.dataset.src;audio.hidden=false}if(!audio.paused){audio.pause();return}error.hidden=true;button.disabled=true;button.textContent='Carregando…';try{await audio.play()}catch(_){error.hidden=false;button.textContent='▶ Tentar novamente'}finally{button.disabled=false}}
   if(link)track('voice_select',{voice_name:link.dataset.voiceName,voice_kind:link.dataset.voiceKind,cta_id:link.dataset.cta});
  });
  root.addEventListener('play',event=>{const audio=event.target;if(!(audio instanceof HTMLMediaElement))return;document.querySelectorAll('audio').forEach(other=>{if(other!==audio)other.pause()});const row=audio.closest('.uv-row');row.querySelector('.uv-play').textContent='❚❚ Pausar';row.querySelector('.uv-error').hidden=true;track('voice_demo_play',{voice_name:audio.dataset.voice,voice_kind:row.closest('.uv-panel').dataset.kind})},true);
  root.addEventListener('change',event=>{if(!event.target.matches('.uv-demo-select'))return;const row=event.target.closest('.uv-row'),audio=row.querySelector('audio');audio.pause();audio.removeAttribute('src');audio.load();audio.hidden=true;audio.dataset.src=event.target.value;row.querySelector('.uv-play').textContent='▶ Ouvir';row.querySelector('.uv-error').hidden=true;});
  for(const name of ['pause','ended'])root.addEventListener(name,event=>{const button=event.target.closest('.uv-row')?.querySelector('.uv-play');if(button)button.textContent='▶ Ouvir'},true);
  root.addEventListener('error',event=>{if(event.target.matches?.('.uv-avatar img')){const avatar=event.target.parentElement;avatar.replaceChildren(node('span','',avatar.closest('.uv-row')?.dataset.name.trim().charAt(0)||'?'));return;}if(!(event.target instanceof HTMLMediaElement))return;const row=event.target.closest?.('.uv-row');if(row){row.querySelector('.uv-error').hidden=false;row.querySelector('.uv-play').textContent='▶ Tentar novamente'}},true);
  root.querySelectorAll('.uv-avatar img').forEach(img=>{if(img.complete&&img.naturalWidth===0)img.parentElement.replaceChildren(node('span','',img.closest('.uv-row').dataset.name.trim().charAt(0)));});
 });
})();
