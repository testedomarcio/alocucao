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
    const search = form.querySelector('input'), gender = form.querySelector('#gender'), style = form.querySelector('#style'), language = form.querySelector('#language');
    function filter() {
      let count = 0;
      cards.forEach(card => {
        const show = normalize(card.dataset.search).includes(normalize(search.value.trim())) && (!gender.value || card.dataset.gender === gender.value) && (!style.value || card.dataset.tags.split('|').includes(style.value)) && (!language?.value || (card.dataset.language || 'pt-BR') === language.value);
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
    const words = text.value.trim() ? text.value.trim().split(/\s+/u).length : 0;
    const seconds = Math.ceil(words / 2.5), blocks = Math.ceil(seconds / 40);
    const production = service?.value === 'producao';
    const name = production ? 'Produção Completa' : 'Locução Off';
    const money = value => value.toFixed(2).replace('.', ',');
    const result = document.querySelector('#calc-result');
    const link = document.querySelector('#calc-whatsapp');
    if (!words) {
      if (link?.dataset) delete link.dataset.service;
      result.textContent = 'Digite um texto para estimar a duração e o valor.';
      if (link) link.href = 'https://wa.me/5527996529832?text=' + encodeURIComponent('Olá! Preciso de ajuda para orçar uma peça comercial.');
      return;
    }
    const minutes = Math.floor(seconds / 60), remaining = seconds % 60;
    const duration = seconds < 60 ? `${seconds} ${seconds === 1 ? 'segundo' : 'segundos'}` : `${minutes} ${minutes === 1 ? 'minuto' : 'minutos'}${remaining ? ` e ${remaining} ${remaining === 1 ? 'segundo' : 'segundos'}` : ''}`;
    const credits = `${blocks} ${blocks === 1 ? 'crédito' : 'créditos'}`;
    const total = `R$ ${money(blocks * (production ? 25 : 12))}`;
    // Only calculated values and fixed service names enter the result markup.
    result.innerHTML = `<p class="calc-service-name">${name}</p><dl class="calc-details"><div><dt>Duração estimada</dt><dd>${duration}</dd></div><div><dt>Créditos necessários</dt><dd>${credits}</dd></div></dl><div class="calc-total"><span>Valor estimado</span><strong>${total}</strong></div>`;
    if (link) {
      if (link.dataset) link.dataset.service = name;
      link.href = 'https://wa.me/5527996529832?text=' + encodeURIComponent(`Olá! Fiz uma estimativa no site da A Locução e gostaria de solicitar um orçamento.\n\nServiço: ${name}\nDuração estimada: ${duration}\nCréditos necessários: ${credits}\nValor estimado: ${total}\n\nRoteiro:\n${text.value}\n\nValor sujeito à confirmação após análise do roteiro.`);
    }
  }
  if (text) {
    text.addEventListener('input', updateCalculator);
    service?.addEventListener('change', updateCalculator);
    service?.addEventListener('input', updateCalculator);
    updateCalculator();
  }
  // Remove any cached legacy service worker so the current public pages are fetched.
  if ('serviceWorker' in navigator) navigator.serviceWorker.getRegistrations().then(registrations => registrations.forEach(registration => registration.unregister())).catch(() => {});
})();
