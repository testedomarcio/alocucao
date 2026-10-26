(() => {
  const nav = document.querySelector('.nav');
  document.querySelector('.menu-toggle')?.addEventListener('click', event => {
    const open = nav.classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });
  nav?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    nav.classList.remove('open');
    document.querySelector('.menu-toggle')?.setAttribute('aria-expanded', 'false');
  }));
  document.addEventListener('play', event => {
    if (event.target.tagName === 'AUDIO') document.querySelectorAll('audio').forEach(audio => {if(audio !== event.target) audio.pause();});
  }, true);
  document.querySelectorAll('audio').forEach(audio => audio.addEventListener('error', () => {
    const message = audio.parentElement.querySelector('.audio-error');
    if (message) message.hidden = false;
  }));
  const normalize = text => text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const form = document.querySelector('.filters');
  if (form) {
    const cards = [...document.querySelectorAll('.voice-card')];
    const search = form.querySelector('input'), gender = form.querySelector('#gender'), style = form.querySelector('#style');
    function filter() {
      let count = 0;
      cards.forEach(card => {
        const show = normalize(card.dataset.search).includes(normalize(search.value.trim())) && (!gender.value || card.dataset.gender === gender.value) && (!style.value || card.dataset.tags.split('|').includes(style.value));
        card.hidden = !show; if (show) count++;
      });
      document.querySelector('#voice-count').textContent = count + (count === 1 ? ' voz encontrada' : ' vozes encontradas');
      document.querySelector('#empty-voices').hidden = count > 0;
    }
    form.addEventListener('submit', e => e.preventDefault());
    form.addEventListener('input', filter);
    form.addEventListener('change', filter);
    form.querySelector('button').addEventListener('click', () => { form.reset(); filter(); search.focus(); });
    form.hidden = false;
  }
  const text = document.querySelector('#calc-text');
  if (text) text.addEventListener('input', () => {
    const words = text.value.trim() ? text.value.trim().split(/\s+/).length : 0;
    const seconds = Math.ceil(words / 2.5), blocks = Math.ceil(seconds/40);
    document.querySelector('#calc-result').textContent = `${words} palavras · aproximadamente ${seconds} segundos. Estimativa: Locução Off R$ ${(blocks*12).toFixed(2).replace('.',',')} · Produção Completa R$ ${(blocks*25).toFixed(2).replace('.',',')}. Interpretação, pausas e projetos especiais dependem de avaliação. Valor final confirmado pelo WhatsApp.`;
  });
  // Remove any cached legacy service worker so the current public pages are fetched.
  if ('serviceWorker' in navigator) navigator.serviceWorker.getRegistrations().then(registrations => registrations.forEach(registration => registration.unregister())).catch(() => {});
})();
