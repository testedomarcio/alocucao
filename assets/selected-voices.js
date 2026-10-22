(() => {
  'use strict';
  const normalize = text => String(text || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  document.querySelectorAll('[data-selected-voices]').forEach(widget => {
    const search=widget.querySelector('.sv-search'),gender=widget.querySelector('.sv-gender'),style=widget.querySelector('.sv-style'),clear=widget.querySelector('.sv-clear'),more=widget.querySelector('.sv-more'),count=widget.querySelector('.sv-count'),empty=widget.querySelector('.sv-empty');
    const cards=[...widget.querySelectorAll('.sv-card')];let limit=6;
    const filter = () => {
      const term=normalize(search.value);
      const found=cards.filter(card => normalize(card.dataset.svName).includes(term)&&(!gender.value||card.dataset.svGender===gender.value)&&(!style.value||card.dataset.svStyles.split('|').includes(style.value)));
      const shown=new Set(found.slice(0,limit));
      cards.forEach(card=>{card.hidden=!shown.has(card);if(card.hidden){const audio=card.querySelector('audio');if(!audio.paused)audio.pause();}});
      count.textContent=`${Math.min(limit,found.length)} de ${found.length} vozes${found.length!==cards.length?' encontradas':' na seleção'}`;
      empty.hidden=found.length>0;more.hidden=found.length<=limit;
      more.textContent=`Mostrar mais vozes (${Math.max(0,found.length-limit)})`;
    };
    [search,gender,style].forEach(control=>control.addEventListener(control===search?'input':'change',()=>{limit=6;filter();}));
    clear.addEventListener('click',()=>{search.value='';gender.value='';style.value='';limit=6;filter();search.focus();});
    more.addEventListener('click',()=>{limit+=6;filter();});
    cards.forEach(card=>{
      const audio=card.querySelector('audio'),error=card.querySelector('.sv-audio-error');
      audio.addEventListener('error',()=>{error.hidden=false;});
      audio.addEventListener('playing',()=>{error.hidden=true;});
      audio.addEventListener('play',()=>{window.alocucaoTrackEvent?.('audio_play',{audio_name:audio.dataset.voice,page_path:location.pathname});});
    });
    filter();
  });
  document.addEventListener('play',event=>{if(event.target instanceof HTMLAudioElement)document.querySelectorAll('audio').forEach(other=>{if(other!==event.target&&!other.paused)other.pause();});},true);
  // Templates and legacy widgets may insert order links after load. Keep every order exit on WhatsApp.
  function fixOrderLink(link) {
    const href=link.getAttribute('href');if(!href)return;
    let url;try{url=new URL(href,location.href);}catch{return;}
    if(!['http:','https:'].includes(url.protocol))return;
    const isPanel=/\/(painel|cadastro|central-de-gravacao|central-de-producao)(\/|$)/i.test(url.pathname);
    if(!isPanel)return;
    const voice=link.dataset.voiceName;
    link.href='https://wa.me/5527996529832?text='+encodeURIComponent(voice?`Olá! Gostei da voz ${voice} e quero um orçamento.`:'Olá! Quero solicitar um orçamento.');
    if(!link.querySelector('img'))link.textContent='Solicitar orçamento pelo WhatsApp';
    link.dataset.cta='whatsapp_order';
  }
  document.querySelectorAll('a[href]').forEach(fixOrderLink);
  document.addEventListener('click',event=>{const link=event.target instanceof Element?event.target.closest('a[href]'):null;if(link)fixOrderLink(link);},true);
})();
