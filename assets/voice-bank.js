(() => {
  'use strict';
  const grid = document.getElementById('voice-grid');
  if (!grid) return;
  const search = document.getElementById('voice-search'), type = document.getElementById('voice-type'), style = document.getElementById('voice-style');
  const count = document.getElementById('result-count'), stamp = document.getElementById('sync-info');
  const more = document.getElementById('load-more'), empty = document.getElementById('empty-state');
  let voices = [], shown = 24, fetchedAt, loading = false;
  const order = new Map();
  const normalize = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const node = (tag, cls, text) => { const el = document.createElement(tag); el.className = cls || ''; if (text !== undefined) el.textContent = text; return el; };
  const stale = () => !fetchedAt || Date.now() - Date.parse(fetchedAt) > 45 * 60000;
  function render() {
    const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
    const matches = voices.filter(v => (!type.value || v.type === type.value) && (!style.value || v.styles.includes(style.value)) && terms.every(t => normalize([v.name, ...v.styles].join(' ')).includes(t))).sort((a,b) => order.get(a.id)-order.get(b.id));
    const fragment = document.createDocumentFragment();
    matches.slice(0,shown).forEach(v => {
      const card = node('article','voice'), top = node('div','voice-top');
      const avatar = node('span','avatar',v.name[0]);
      if (v.photo) { const image = node('img'); image.src = v.photo; image.alt = ''; image.width = image.height = 64; image.loading = 'lazy'; image.addEventListener('error',()=>image.remove(),{once:true}); avatar.append(image); }
      const identity = node('div','voice-identity'); identity.append(node('h3','',v.name)); top.append(avatar,identity);
      const status = node('p','status-badge');
      status.textContent = stale() ? 'Status sob consulta no WhatsApp' : (v.status === 'recording_online' ? 'Gravando em: ' : 'Status: ') + v.statusLabel;
      if (!stale() && v.status === 'recording_online') status.classList.add('is-recording');
      const tags = node('p','voice-styles',v.styles.join(' · '));
      const audio = node('audio'); audio.controls = true; audio.preload = 'none'; audio.src = v.audio; audio.dataset.voice = v.name; audio.setAttribute('aria-label','Ouvir demonstração de '+v.name);
      const error = node('p','voice-audio-error','Não foi possível carregar a demo. Peça mais demonstrações pelo WhatsApp.'); error.hidden = true;
      audio.addEventListener('error',()=>error.hidden=false); audio.addEventListener('playing',()=>error.hidden=true);
      audio.addEventListener('play',()=>document.querySelectorAll('audio').forEach(other=>{if(other!==audio)other.pause()}));
      const choose = node('a','choose','Peça no WhatsApp'); choose.href = 'https://wa.me/5527996529832?text='+encodeURIComponent('Olá! Ouvi a voz de '+v.name+' na A Locução. Quero mais demonstrações e uma proposta para meu áudio.'); choose.dataset.cta = 'voz_catalogo_'+v.id;
      card.append(top,status,tags,audio,error,choose); fragment.append(card);
    });
    // Keep an in-progress demo playing during background status refresh.
    grid.replaceChildren(fragment);
    count.textContent = matches.length+' vozes encontradas · mostrando '+Math.min(shown,matches.length);
    more.hidden = shown >= matches.length; empty.hidden = matches.length > 0;
    stamp.textContent = 'Status atualizado em '+new Intl.DateTimeFormat('pt-BR',{timeZone:'America/Sao_Paulo',dateStyle:'short',timeStyle:'short'}).format(new Date(fetchedAt))+' (Brasília). '+(stale()?'Confirme a disponibilidade no WhatsApp.':'Confirme o prazo ao fazer seu pedido.');
  }
  function validate(data) {
    if(data.schemaVersion!==1 || !Array.isArray(data.voices) || !data.voices.length || data.count!==data.voices.length || !Number.isFinite(Date.parse(data.fetchedAt))) throw Error('Invalid catalog');
    const ids = new Set();
    for (const v of data.voices) {
      if(typeof v.id!=='string' || ids.has(v.id) || typeof v.name!=='string' || !Array.isArray(v.styles) || !v.styles.every(x=>typeof x==='string')) throw Error('Invalid voice');
      for (const value of [v.audio, v.photo].filter(Boolean)) { const url = new URL(value); if(url.protocol!=='https:' || url.hostname!=='vozes.alocucao.com.br' || url.username || url.password || !['/midia.php','/download-audio.php'].includes(url.pathname)) throw Error('Invalid media'); }
      ids.add(v.id);
    }
    return data;
  }
  async function load() {
    if(loading) return; loading = true;
    try {
      const response = await fetch('/assets/voices-catalog.json?v=20261014',{cache:'no-store',signal:AbortSignal.timeout(15000)});
      if(!response.ok) throw Error('Unavailable');
      const data = validate(await response.json());
      if (voices.length && [...grid.querySelectorAll('audio')].some(audio=>!audio.paused)) return;
      voices = data.voices; fetchedAt = data.fetchedAt;
      voices.forEach(v=>{if(!order.has(v.id))order.set(v.id,Math.random())});
      const selectedStyle = style.value; style.replaceChildren(new Option('Todos os estilos',''));
      [...new Set(voices.flatMap(v=>v.styles))].sort().forEach(s=>style.add(new Option(s,s))); style.value = selectedStyle;
      render();
    } catch (_) {
      if(voices.length) {  grid.querySelectorAll('.status-badge').forEach(el=>el.textContent='Status sob consulta no WhatsApp'); stamp.textContent='Não foi possível atualizar o status. Confirme pelo WhatsApp.'; }
      else { count.textContent='Catálogo temporariamente indisponível'; empty.hidden=false; stamp.textContent='Nossa equipe pode enviar as demonstrações pelo WhatsApp.'; }
    } finally { loading=false; }
  }
  [search,type,style].forEach(el=>el.addEventListener(el===search?'input':'change',()=>{shown=24;render()}));
  document.getElementById('clear-filters').addEventListener('click',()=>{search.value=type.value=style.value='';shown=24;voices.length?render():load()});
  more.addEventListener('click',()=>{shown+=24;render()});
  load();
  setInterval(()=>{if(!document.hidden)load()},5*60000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)load()});
})();
