(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const normalize = text => String(text || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const grid = $('voice-grid'), player = $('voice-player'), dock = $('player-dock');
  const fields = {search:$('voice-search'),type:$('voice-type'),style:$('voice-style'),language:$('voice-language'),region:$('voice-region')};
  let catalog, shown = 24, favoriteView = false, compareView = false, playingId = null, loading = false;
  const selected = new Set();
  // A new random order per page opening, stable while filtering.
  const randomOrder = new Map();
  function registerRandomOrder(voices) {
    voices.forEach(voice => {
      if (!randomOrder.has(voice.id)) randomOrder.set(voice.id, Math.random());
    });
  }
  function compareVoices(a, b) {
    if ($('voice-sort').value === 'random') {
      return randomOrder.get(a.id) - randomOrder.get(b.id) || a.name.localeCompare(b.name, 'pt-BR');
    }
    return a.name.localeCompare(b.name, 'pt-BR');
  }
  let layout = 'list';
  try { if(localStorage.getItem('alocucao_voice_layout') === 'grid') layout = 'grid'; } catch (_) {}
  function updateLayout() {
    grid.classList.toggle('list-view', layout === 'list');
    $('view-list').setAttribute('aria-pressed', String(layout === 'list'));
    $('view-grid').setAttribute('aria-pressed', String(layout === 'grid'));
  }
  let favorites = new Set();
  try { const saved = JSON.parse(localStorage.getItem('alocucao_voice_favorites') || '[]'); if (Array.isArray(saved)) favorites = new Set(saved.filter(x => typeof x === 'string').slice(0,500)); } catch (_) {}
  function element(tag, className, text) { const node = document.createElement(tag); if(className) node.className = className; if(text !== undefined) node.textContent = text; return node; }
  function announce(text) { $('voice-announcement').textContent = text; }
  function updateTotals() {
    $('favorites-count').textContent = favorites.size;
    $('compare-count').textContent = selected.size;
    $('favorites-toggle').setAttribute('aria-pressed', String(favoriteView));
    $('compare-toggle').setAttribute('aria-pressed', String(compareView));
    document.querySelectorAll('[data-style]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.style === fields.style.value)));
  }
  function saveFavorite(id, button) {
    favorites.has(id) ? favorites.delete(id) : favorites.add(id);
    try { localStorage.setItem('alocucao_voice_favorites', JSON.stringify([...favorites])); } catch (_) {}
    button.setAttribute('aria-pressed', String(favorites.has(id))); button.textContent = favorites.has(id) ? '♥' : '♡';
    announce(favorites.has(id) ? 'Voz salva nos favoritos.' : 'Voz removida dos favoritos.');
    updateTotals(); if(favoriteView) render();
  }
  function play(voice) {
    if(playingId === voice.id && !player.paused) { player.pause(); return; }
    if(playingId !== voice.id) { player.pause(); const media = new URL(voice.audio); player.src = media.href; playingId = voice.id; }
    player.dataset.voice = voice.name;
    $('player-name').textContent = voice.name;
    $('player-detail').textContent = [voice.type ? 'Voz '+voice.type.toLowerCase() : 'Voz humana', ...voice.styles.slice(0,2)].join(' · ');
    $('player-error').hidden = true; dock.classList.add('open');
    player.play().catch(error => { if(error.name !== 'AbortError') { $('player-error').hidden = false; announce('A demo não pôde ser reproduzida.'); } });
    updatePlaying();
  }
  function updatePlaying() {
    grid.querySelectorAll('.voice').forEach(card => {
      const current = card.dataset.id === playingId && !player.paused;
      card.classList.toggle('is-playing', current);
      const button = card.querySelector('.listen'); button.textContent = current ? 'Ⅱ Pausar' : '▶ Ouvir demo'; button.setAttribute('aria-pressed', String(current));
    });
  }
  function card(voice) {
    const article = element('article','voice'); article.dataset.id = voice.id;
    const top = element('div','voice-top');
    const initials = voice.name.split(/\s+/).filter(Boolean).slice(0,2).map(x=>x[0]).join('');
    const avatar = element('span','avatar',initials); avatar.setAttribute('aria-hidden','true');
    if(voice.photo) { const photo = element('img'); photo.src = voice.photo; photo.alt = ''; photo.width = 160; photo.height = 160; photo.loading = 'lazy'; photo.decoding = 'async'; photo.addEventListener('error',()=>photo.remove(),{once:true}); avatar.append(photo); }
    const identity = element('div','voice-identity'); identity.append(element('h3','',voice.name),element('p','voice-type',voice.type ? 'Voz '+voice.type.toLowerCase() : 'Voz humana'));
    const favorite = element('button','favorite-button',favorites.has(voice.id)?'♥':'♡'); favorite.type='button'; favorite.setAttribute('aria-label','Salvar '+voice.name+' nos favoritos'); favorite.setAttribute('aria-pressed',String(favorites.has(voice.id))); favorite.addEventListener('click',()=>saveFavorite(voice.id,favorite));
    top.append(avatar,identity,favorite);
    const tags = element('div','tags'); voice.styles.forEach(style=>tags.append(element('span','tag',style)));
    const meta = element('div','voice-meta'); meta.append(element('span','',voice.region || 'Região não informada'),element('span','',voice.languages.join(' · ')));
    const actions = element('div','voice-actions');
    const listen = element('button','listen','▶ Ouvir demo'); listen.type='button'; listen.setAttribute('aria-label','Ouvir demonstração de '+voice.name); listen.setAttribute('aria-pressed','false'); listen.addEventListener('click',()=>play(voice));
    const choose = element('a','choose','Quero essa voz'); choose.href='https://wa.me/5527996529832?text='+encodeURIComponent('Olá! Quero uma gravação com '+voice.name+'. Pode confirmar a disponibilidade e o prazo?');  choose.dataset.cta='escolher_'+voice.id;
    actions.append(listen,choose);
    const compareLabel = element('label','compare-check'); const check = element('input'); check.type='checkbox'; check.checked=selected.has(voice.id); check.setAttribute('aria-label','Comparar '+voice.name);
    check.addEventListener('change',()=>{
      if(check.checked && selected.size >= 3){check.checked=false;announce('Você pode comparar até três vozes. Desmarque uma para escolher outra.');return;}
      check.checked?selected.add(voice.id):selected.delete(voice.id);updateTotals();announce(selected.size+' vozes selecionadas para comparar.');if(compareView)render();
    });
    compareLabel.append(check,document.createTextNode('Adicionar à comparação'));
    article.append(top,tags,meta,actions,compareLabel);
    return article;
  }
  function filtered() {
    const terms = normalize(fields.search.value.trim()).split(/\s+/).filter(Boolean);
    return catalog.voices.filter(v=> (!favoriteView || favorites.has(v.id)) && (!compareView || selected.has(v.id)) && (!fields.type.value || v.type===fields.type.value) && (!fields.style.value || v.styles.includes(fields.style.value)) && (!fields.language.value || v.languages.includes(fields.language.value)) && (!fields.region.value || v.region===fields.region.value) && terms.every(t=>normalize([v.name,v.region,...v.styles,...v.languages].join(' ')).includes(t))).sort(compareVoices);
  }
  function render() {
    if(!catalog)return;
    const list = filtered(); const visible = list.slice(0,shown); const fragment = document.createDocumentFragment();visible.forEach(v=>fragment.append(card(v)));grid.replaceChildren(fragment);
    $('result-count').textContent = `${list.length} ${list.length===1?'voz encontrada':'vozes encontradas'}`+(compareView?' · comparação':'');
    $('shown-count').textContent = list.length ? `Mostrando ${visible.length} de ${list.length}` : '';
    $('empty-state').hidden = list.length > 0; $('load-more').hidden = shown >= list.length;
    updateTotals();updatePlaying();updateLayout();
  }
  function reset() {
    Object.values(fields).forEach(f=>f.value='');favoriteView=false;compareView=false;shown=24;render();
  }
  function options(field, values) {
    const previous = field.value; while(field.options.length>1)field.remove(1);
    [...new Set(values.filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR')).forEach(v=>field.add(new Option(v,v)));
    field.value=[...field.options].some(o=>o.value===previous)?previous:'';
  }
  function validate(data) {
    if(data.schemaVersion!==1 || !Number.isFinite(Date.parse(data.fetchedAt)) || !Array.isArray(data.voices) || !data.voices.length || data.count!==data.voices.length || data.voices.length>1500)throw Error('Invalid catalog');
    const ids=new Set();
    for(const v of data.voices){
      if(typeof v.id!=='string'||ids.has(v.id)||typeof v.name!=='string'||!Array.isArray(v.styles)||!v.styles.every(x=>typeof x==='string')||!Array.isArray(v.languages)||!v.languages.every(x=>typeof x==='string'))throw Error('Invalid voice');
      if(v.localProfile && !/^\/perfil-locutor-[a-z0-9][a-z0-9-]*\/$/.test(v.localProfile))throw Error('Invalid local profile');
      if(v.profilePublished !== undefined && typeof v.profilePublished !== 'boolean')throw Error('Invalid profile flag');
      if(v.schedule !== undefined && (!Array.isArray(v.schedule)||v.schedule.length>7||!v.schedule.every(d=>['Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo'].includes(d.day)&&Array.isArray(d.intervals)&&d.intervals.length>0&&d.intervals.length<=8&&d.intervals.every(i=>/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(i.start)&&/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(i.end)))))throw Error('Invalid schedule');
      if(v.photo) { const photo=new URL(v.photo,location.origin); if(photo.protocol!=='https:'||photo.hostname!=='vozlocutor.com.br'||photo.pathname!=='/perfil-img.php'||photo.username||photo.password)throw Error('Invalid photo'); }
      const media=new URL(v.audio);if(media.protocol!=='https:'||media.hostname!=='vozlocutor.com.br'||media.username||media.password)throw Error('Invalid media');ids.add(v.id);
    }
    return data;
  }
  async function load() {
    if(loading)return;loading=true;
    try {
      const response=await fetch('/assets/voices-catalog.json?v=20261007-static',{signal:AbortSignal.timeout(15000)}); if(!response.ok)throw Error('Catalog unavailable');
      catalog=validate(await response.json());
      registerRandomOrder(catalog.voices);
      // Preserve favorites only for explicit catalog matches and the confirmed Celso alias.
      favorites = new Set([...favorites].map(id=>catalog.idAliases?.[id] || id));
      try { localStorage.setItem('alocucao_voice_favorites', JSON.stringify([...favorites])); } catch (_) {}
      const existing=new Set(catalog.voices.map(v=>v.id));for(const id of selected)if(!existing.has(id))selected.delete(id);for(const id of favorites)if(!existing.has(id))favorites.delete(id);
      options(fields.type,catalog.voices.map(v=>v.type));
      options(fields.style,catalog.voices.flatMap(v=>v.styles));options(fields.region,catalog.voices.map(v=>v.region));options(fields.language,catalog.voices.flatMap(v=>v.languages));
      $('sync-info').textContent = catalog.count + ' vozes para ouvir e comparar';render();
    } catch (_) {
      if(catalog){$('sync-info').textContent='Catálogo disponível para ouvir';render();}
      else{$('result-count').textContent='Catálogo temporariamente indisponível';$('sync-info').textContent='Peça uma indicação no atendimento.';$('empty-state').hidden=false;$('empty-state').querySelector('h3').textContent='Vamos ajudar você a encontrar uma voz.';$('empty-state').querySelector('p').textContent='O catálogo não carregou. Use o botão de orientação ou tente novamente.';$('empty-reset').textContent='Tentar carregar novamente';}
    } finally {loading=false;}
  }
  let debounce;
  Object.values(fields).forEach(field=>field.addEventListener(field===fields.search?'input':'change',()=>{clearTimeout(debounce);debounce=setTimeout(()=>{shown=24;render()},field===fields.search?120:0)}));
  document.querySelectorAll('[data-style]').forEach(b=>b.addEventListener('click',()=>{fields.style.value=b.dataset.style;shown=24;render()}));
  $('voice-sort').addEventListener('change',render);
  for(const mode of ['list','grid']) $('view-'+mode).addEventListener('click',()=>{layout=mode;try{localStorage.setItem('alocucao_voice_layout',mode)}catch(_){}updateLayout()});
  updateLayout();
  $('favorites-toggle').addEventListener('click',()=>{favoriteView=!favoriteView;compareView=false;shown=24;render()});
  $('compare-toggle').addEventListener('click',()=>{compareView=!compareView;favoriteView=false;if(compareView)Object.values(fields).forEach(f=>f.value='');shown=24;render()});
  $('clear-filters').addEventListener('click',reset);$('empty-reset').addEventListener('click',()=>catalog?reset():load());
  $('load-more').addEventListener('click',()=>{const index=shown;shown+=24;render();const next=grid.children[index]?.querySelector('.listen');next?.focus({preventScroll:true})});
  $('player-close').addEventListener('click',()=>{player.pause();dock.classList.remove('open');grid.querySelector(`[data-id="${CSS.escape(playingId||'')}"] .listen`)?.focus({preventScroll:true})});
  ['play','pause','ended'].forEach(event=>player.addEventListener(event,updatePlaying));
  player.addEventListener('error',()=>{if(player.getAttribute('src')){$('player-error').hidden=false;updatePlaying()}});
  load();
})();
