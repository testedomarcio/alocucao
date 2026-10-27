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
  // Shuffle on every fresh visit; also refresh the order after back/forward cache restores.
  function shuffleVoices() {
    document.querySelectorAll('.voice-grid').forEach(grid => {
      const cards = [...grid.children];
      for (let i=cards.length-1;i>0;i--) {
        const j=Math.floor(Math.random()*(i+1));
        [cards[i],cards[j]]=[cards[j],cards[i]];
      }
      cards.forEach(card => grid.appendChild(card));
    });
  }
  // Initial ordering happens inline beside each grid, before the first paint.
  window.addEventListener('pageshow', event => { if(event.persisted) shuffleVoices(); });
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
  const service = document.querySelector('#calc-service');
  function updateCalculator() {
    const characters = Array.from(text.value).length;
    const words = text.value.trim() ? text.value.trim().split(/\s+/u).length : 0;
    const seconds = Math.ceil(words / 2.5), blocks = Math.ceil(seconds / 40);
    const production = service?.value === 'producao';
    const name = production ? 'Produção Completa' : 'Locução Off';
    const money = value => value.toFixed(2).replace('.', ',');
    const result = document.querySelector('#calc-result');
    const link = document.querySelector('#calc-whatsapp');
    if (!words) {
      result.textContent = 'Digite um texto para estimar a duração e o valor.';
      if (link) link.href = 'https://wa.me/5527996529832?text=' + encodeURIComponent('Olá! Preciso de ajuda para orçar uma peça comercial.');
      return;
    }
    result.textContent = `${words} palavras · aproximadamente ${seconds} segundos · ${blocks} faixa(s) de até 40 segundos. ${characters} caracteres. Estimativa: Locução Off R$ ${money(blocks*12)} · Produção Completa R$ ${money(blocks*25)}. Selecionado: ${name}. Interpretação e pausas alteram a duração. Valor final confirmado antes do pagamento.`;
    if (link) link.dataset && (link.dataset.service = name);
    if (link) link.href = 'https://wa.me/5527996529832?text=' + encodeURIComponent(`Olá! Fiz uma estimativa no site da A Locução e gostaria de conferir o orçamento. Serviço: ${name}. Roteiro: ${words} palavras, ${characters} caracteres. Duração estimada: ${seconds} segundos (${blocks} faixa(s) de até 40 segundos). Valor estimado: R$ ${money(blocks*(production?25:12))}. Entendo que a duração e o valor final precisam ser confirmados pela equipe.`);
  }
  if (text) {
    text.addEventListener('input', updateCalculator);
    service?.addEventListener('change', updateCalculator);
  }
  // Remove any cached legacy service worker so the current public pages are fetched.
  if ('serviceWorker' in navigator) navigator.serviceWorker.getRegistrations().then(registrations => registrations.forEach(registration => registration.unregister())).catch(() => {});
})();
