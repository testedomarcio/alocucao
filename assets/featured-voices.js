(() => {
  'use strict';
  const widgets = [...document.querySelectorAll('[data-featured-voices]')];
  if (!widgets.length) return;
  const cards = widgets.flatMap(widget => [...widget.querySelectorAll('[data-featured-id]')]);
  const maxAge = 3 * 60 * 60 * 1000;
  let catalog = null, loading = false;
  const safeAudio = value => {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.hostname !== 'hd.paineldegravacao.com.br' || url.username || url.password) throw Error('Invalid audio');
    return url.href;
  };
  function validate(data) {
    if (data.schemaVersion !== 1 || !Number.isFinite(Date.parse(data.fetchedAt)) || !Array.isArray(data.voices) || data.voices.length !== 4 || data.count !== 4) throw Error('Invalid selection');
    const ids = new Set();
    for (const voice of data.voices) {
      if (typeof voice.id !== 'string' || ids.has(voice.id) || typeof voice.status !== 'string' || typeof voice.statusLabel !== 'string') throw Error('Invalid voice');
      safeAudio(voice.audio); ids.add(voice.id);
    }
    if (cards.some(card => !ids.has(card.dataset.featuredId))) throw Error('Missing selected voice');
    return data;
  }
  function update(failed = false) {
    const age = catalog ? Date.now() - Date.parse(catalog.fetchedAt) : Infinity;
    const fresh = age >= 0 && age < maxAge;
    const byId = new Map((catalog?.voices || []).map(voice => [voice.id, voice]));
    cards.forEach(card => {
      const voice = byId.get(card.dataset.featuredId), status = card.querySelector('[data-featured-status]');
      const label = fresh && voice ? voice.statusLabel : 'Disponibilidade sob consulta';
      if (status.textContent !== label) status.textContent = label;
      status.classList.toggle('is-recording', Boolean(fresh && voice?.status.startsWith('recording_')));
      const audio = card.querySelector('audio');
      // Do not interrupt playback or invalidate the MP3 cache on every status refresh.
      if (voice && audio.paused && !audio.currentTime) {
        const source = safeAudio(voice.audio);
        if (audio.getAttribute('src') !== source) audio.src = source;
        card.querySelector('[data-featured-fallback]').href = source;
      }
    });
    let note = 'Status sob consulta. Confirme disponibilidade e prazo pelo WhatsApp.';
    if (fresh) {
      const stamp = new Intl.DateTimeFormat('pt-BR', {timeZone:'America/Sao_Paulo',day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}).format(new Date(catalog.fetchedAt));
      note = `Última consulta: ${stamp} (Brasília). Confirme disponibilidade e prazo pelo WhatsApp.`;
      if (failed) note += ' Atualização temporariamente indisponível.';
    }
    widgets.forEach(widget => {
      const node = widget.querySelector('[data-featured-sync]');
      if (node.textContent !== note) node.textContent = note;
    });
  }
  async function refresh() {
    if (loading) return;
    loading = true;
    try {
      const response = await fetch('/assets/featured-voices.json?v=' + Math.floor(Date.now()/600000), {cache:'no-cache',signal:AbortSignal.timeout(15000)});
      if (!response.ok) throw Error('Catalog unavailable');
      catalog = validate(await response.json()); update();
    } catch (_) { update(true); }
    finally { loading = false; }
  }
  cards.forEach(card => {
    const audio = card.querySelector('audio'), error = card.querySelector('.featured-error');
    audio.addEventListener('error', () => { error.hidden = false; });
    audio.addEventListener('playing', () => { error.hidden = true; });
    audio.addEventListener('play', () => {
      document.querySelectorAll('audio').forEach(other => { if (other !== audio && !other.paused) other.pause(); });
    });
  });
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
  setInterval(() => { if (!document.hidden) refresh(); }, 15 * 60 * 1000);
  refresh();
})();
