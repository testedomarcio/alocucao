(() => {
  'use strict';
  if (document.body.dataset.orderChannels !== 'dual') return;
  const campaignKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'msclkid', 'gclid'];
  const query = new URLSearchParams(location.search);
  const attribution = {};
  campaignKeys.forEach(key => { if (query.has(key)) attribution[key] = query.get(key); });
  // Carry campaign identifiers into the external panel; never send them as WhatsApp message text.
  document.querySelectorAll('a[href]').forEach(link => {
    const url = new URL(link.href, location.href);
    if (url.hostname !== 'vozes.alocucao.com.br' || !url.pathname.startsWith('/painel/')) return;
    Object.entries(attribution).forEach(([key, value]) => url.searchParams.set(key, value));
    link.href = url.href;
  });
  const common = link => ({
    page_path: location.pathname,
    service_name: 'pacotes_off_producao',
    traffic_source: attribution.utm_source || (attribution.msclkid ? 'bing' : 'not_set'),
    campaign_name: attribution.utm_campaign || 'not_set',
    cta_id: link?.dataset.cta || 'not_set',
    cta_location: link?.closest('section')?.id || (link?.closest('header') ? 'header' : link?.closest('.mobile-order') ? 'mobile_bar' : 'other')
  });
  document.addEventListener('click', event => {
    const link = event.target instanceof Element ? event.target.closest('a[href]') : null;
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.hostname === 'vozes.alocucao.com.br' && url.pathname.startsWith('/painel/')) {
      window.alocucaoTrackEvent?.('panel_click', { ...common(link), panel_action: url.pathname.includes('/cadastro') ? 'register' : 'login' });
    }
    if (link.dataset.cta === 'all_voices') window.alocucaoTrackEvent?.('voice_bank_click', common(link));
    // Existing tracking.js owns whatsapp_click; packages-landing.js owns package_interest.
  });
  let priceSeen = false;
  const prices = document.getElementById('pacotes');
  if (prices && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (!entries.some(entry => entry.isIntersecting) || priceSeen) return;
      priceSeen = window.alocucaoTrackEvent?.('pricing_view', { ...common(), cta_location: 'pacotes' }) === true;
      if (priceSeen) observer.disconnect();
    }, { threshold: 0.1 });
    observer.observe(prices);
    window.addEventListener('alocucao:consent', event => {
      if (event.detail?.value === 'accepted' && !priceSeen) {
        observer.unobserve(prices);
        observer.observe(prices);
      }
    });
  }
})();
