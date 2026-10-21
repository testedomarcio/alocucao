(() => {
  'use strict';
  const root = document.querySelector('[data-catalog="vozes-ia"]');
  if (!root) return;
  const filters = root.querySelector('.ia-filters');
  filters.hidden = false;
  const search = root.querySelector('#ia-search');
  const gender = root.querySelector('#ia-gender');
  const style = root.querySelector('#ia-style');
  const cards = [...root.querySelectorAll('.ia-voice')];
  // Shuffle the existing cards once per visit; keep each voice and its player together.
  function shuffleCatalog() {
    const shuffled = [...cards];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    root.querySelector('.ia-grid').append(...shuffled);
  }
  shuffleCatalog();
  window.addEventListener('pageshow', event => {
    if (event.persisted) shuffleCatalog();
  });
  const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const track = (event, params = {}) => window.alocucaoTrackEvent?.(event, {page_path:'/vozes-ia/', service_name:'vozes_ia', ...params});
  function filter() {
    const query = normalize(search.value.trim());
    let count = 0;
    cards.forEach(card => {
      const match = (!query || normalize(card.textContent).includes(query)) && (!gender.value || card.dataset.gender === gender.value) && (!style.value || card.dataset.styles.split('|').includes(style.value));
      card.hidden = !match;
      if (match) count++;
      else card.querySelector('audio')?.pause();
    });
    root.querySelector('#ia-count').textContent = `${count} ${count === 1 ? 'voz encontrada' : 'vozes encontradas'}`;
    root.querySelector('#ia-empty').hidden = count !== 0;
  }
  search.addEventListener('input',filter);
  [gender,style].forEach(el => el.addEventListener('change', () => { filter();track('ia_filter_select',{filter_type:el.id,filter_value:el.value || 'todos'}); }));
  root.querySelector('#ia-reset').addEventListener('click', () => {search.value='';gender.value='';style.value='';filter();search.focus();});
  const audios = [...root.querySelectorAll('.ia-voice audio')];
  audios.forEach(audio => {
    audio.addEventListener('play', () => {audios.forEach(other => {if(other !== audio) other.pause();});track('ia_demo_play',{voice_name:audio.dataset.voice});});
    audio.addEventListener('error', () => {audio.hidden=true;audio.nextElementSibling.hidden=false;});
  });
  root.addEventListener('click',event => {
    const link=event.target.closest('a[data-ia-voice]');
    if(link?.dataset.iaVoice) track('ia_voice_select',{voice_name:link.dataset.iaVoice,cta_id:link.dataset.cta});
  });
  // Match the actual sticky header even when its mobile height changes.
  const header = document.querySelector('.al-header');
  function offset(){document.documentElement.style.scrollPaddingTop=((header?.getBoundingClientRect().height || 76)+24)+'px';}
  if (header && window.ResizeObserver) new ResizeObserver(offset).observe(header);
  offset();
})();
