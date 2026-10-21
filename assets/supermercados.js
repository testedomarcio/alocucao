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
})();
