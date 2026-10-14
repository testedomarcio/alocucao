(() => {
  'use strict';
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'msclkid'];
  const incoming = new URLSearchParams(location.search);
  let attribution = {};
  try { attribution = JSON.parse(sessionStorage.getItem('alocucao_supermercados_attribution') || '{}'); } catch (_) {}
  if (!attribution || typeof attribution !== 'object' || Array.isArray(attribution)) attribution = {};
  if (keys.some(key => incoming.has(key))) attribution = {};
  keys.forEach(key => { if (incoming.has(key)) attribution[key] = incoming.get(key).slice(0, 200); });
  try { sessionStorage.setItem('alocucao_supermercados_attribution', JSON.stringify(attribution)); } catch (_) {}
  document.querySelectorAll('a[data-cta]').forEach(link => {
    const url = new URL(link.href, location.href);
    if (url.hostname !== 'wa.me') return;
    const source = String(attribution.utm_source || (attribution.msclkid ? 'Bing Ads' : '')).slice(0, 80);
    const campaign = String(attribution.utm_campaign || '').slice(0, 80);
    const origin = [source, campaign].filter(Boolean).join(' / ');
    if (origin) url.searchParams.set('text', url.searchParams.get('text') + '\nOrigem: ' + origin);
    keys.forEach(key => { if (attribution[key]) url.searchParams.set(key, String(attribution[key])); });
    link.href = url.href;
  });
  // Supplementary GA4 event. Shared tracking sends the single existing UET
  // whatsapp_click action. Neither event represents a conversation or a sale.
  document.addEventListener('click', event => {
    const link = event.target instanceof Element ? event.target.closest('a[data-cta]') : null;
    if (!link || new URL(link.href, location.href).hostname !== 'wa.me') return;
    window.alocucaoTrackEvent?.('whatsapp_click_supermercados', {
      event_category: 'contact', contact_method: 'whatsapp',
      service_name: 'producao_supermercados', page_path: location.pathname,
      cta_id: link.dataset.cta, traffic_source: attribution.utm_source || (attribution.msclkid ? 'bing' : 'direct'),
      traffic_medium: attribution.utm_medium || (attribution.msclkid ? 'cpc' : 'none'),
      campaign_name: attribution.utm_campaign || 'not_set'
    });
  });
  const cards = [...document.querySelectorAll('[data-featured-id]')];
  const stamp = document.querySelector('[data-market-sync]');
  function unavailable(message) {
    cards.forEach(card => {
      const status = card.querySelector('[data-market-status]');
      status.textContent = 'Disponibilidade sob consulta no WhatsApp';
      status.classList.remove('is-recording');
    });
    if (stamp) stamp.textContent = message;
  }
  cards.forEach(card => {
    const audio = card.querySelector('audio'), error = card.querySelector('.featured-error');
    audio.addEventListener('error', () => { error.hidden = false; });
    audio.addEventListener('playing', () => { error.hidden = true; });
    const photo = card.querySelector('img');
    photo.addEventListener('error', () => { photo.hidden = true; });
  });
  let loading = false, expiresAt = 0;
  async function refresh() {
    if (loading) return;
    loading = true;
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 12000);
    try {
      const response = await fetch('/assets/voices-catalog.json', { cache: 'no-store', signal: controller.signal });
      if (!response.ok) throw new Error('Catalog unavailable');
      const data = await response.json(), updated = Date.parse(data.fetchedAt);
      if (data.schemaVersion !== 1 || !Array.isArray(data.voices) || !Number.isFinite(updated)) throw new Error('Invalid catalog');
      const date = new Intl.DateTimeFormat('pt-BR', { timeZone: 'America/Sao_Paulo', dateStyle: 'short', timeStyle: 'short' }).format(new Date(updated));
      expiresAt = updated + 45 * 60000;
      if (Date.now() > expiresAt || updated > Date.now() + 5 * 60000) {
        unavailable('Última atualização: ' + date + ' (Brasília). Status sob consulta; confirme disponibilidade e prazo com a equipe.');
        return;
      }
      cards.forEach(card => {
        const voice = data.voices.find(v => v.id === card.dataset.featuredId);
        const status = card.querySelector('[data-market-status]');
        const recording = voice?.status === 'recording_online';
        status.textContent = voice ? (recording ? 'Gravando em: ' : 'Status: ') + String(voice.statusLabel || 'Sob consulta').replace(/^Online \((.*)\)$/i, '$1') : 'Disponibilidade sob consulta no WhatsApp';
        status.classList.toggle('is-recording', recording);
      });
      if (stamp) stamp.textContent = 'Status atualizado em ' + date + ' (Brasília). Confirme disponibilidade e prazo no pedido.';
    } catch (_) {
      unavailable('Não foi possível atualizar os status. As demonstrações continuam disponíveis; consulte nossa equipe no WhatsApp.');
    } finally { clearTimeout(timer); loading = false; }
  }
  refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, 15 * 60000);
  setInterval(() => { if (expiresAt && Date.now() > expiresAt) unavailable('Status sob consulta. Confirme disponibilidade e prazo com nossa equipe.'); }, 60000);
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refresh(); });
})();
