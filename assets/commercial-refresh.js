/* Attribution only: the existing tracking.js owns WhatsApp conversions. */
(() => {
  'use strict';
  // Every public page can be an entry point or an intermediate step to the panel.
  const keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'msclkid', 'gclid'];
  const incoming = new URLSearchParams(location.search);
  let attribution = {};
  try { attribution = JSON.parse(sessionStorage.getItem('alocucao_commercial_attribution') || '{}'); } catch (_) {}
  if (!attribution || typeof attribution !== 'object' || Array.isArray(attribution)) attribution = {};
  if (keys.some(key => incoming.has(key))) attribution = {};
  keys.forEach(key => { if (incoming.has(key)) attribution[key] = incoming.get(key).slice(0, 500); });
  try { sessionStorage.setItem('alocucao_commercial_attribution', JSON.stringify(attribution)); } catch (_) {}
  function decorate(link) {
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (!['http:', 'https:'].includes(url.protocol)) return;
    if (url.hostname === 'wa.me' && !link.dataset.voiceKind) link.dataset.voiceKind = 'nao_informado';
    const internal = url.origin === location.origin;
    if (!internal && !['wa.me', 'vozes.alocucao.com.br'].includes(url.hostname)) return;
    keys.forEach(key => { if (attribution[key] && !url.searchParams.has(key)) url.searchParams.set(key, attribution[key]); });
    link.href = url.href;
  }
  document.querySelectorAll('a[href]').forEach(decorate);
  // Pass the campaign to the provider's entry point. The provider remains
  // responsible for retaining it on its own links and completed orders.
  document.querySelectorAll('iframe[data-voice-showcase]').forEach(frame => {
    const url = new URL(frame.src, location.href);
    if (url.origin !== 'https://vozes.alocucao.com.br' || url.pathname !== '/embed.php') return;
    keys.forEach(key => { if (attribution[key] && !url.searchParams.has(key)) url.searchParams.set(key, attribution[key]); });
    if (frame.src !== url.href) frame.src = url.href;
  });
  // Capture also covers voice cards refreshed after page load and middle clicks.
  const handle = event => decorate(event.target instanceof Element ? event.target.closest('a[href]') : null);
  document.addEventListener('click', handle, true);
  document.addEventListener('auxclick', handle, true);
})();
