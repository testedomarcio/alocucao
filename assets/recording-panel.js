/* The embedded provider owns catalog controls; this page owns its frame size only. */
(() => {
  'use strict';
  if (window.alocucaoShowcaseReady) return;
  window.alocucaoShowcaseReady = true;
  const origin = 'https://vozes.alocucao.com.br';
  window.addEventListener('message', event => {
    if (event.origin !== origin || !event.data || typeof event.data !== 'object' || Array.isArray(event.data)) return;
    const { vitrineVozes, altura } = event.data;
    if (vitrineVozes !== true || typeof altura !== 'number' || !Number.isFinite(altura) || altura < 240 || altura > 60000) return;
    const frame = [...document.querySelectorAll('iframe[data-voice-showcase]')].find(el => el.contentWindow === event.source);
    if (!frame) return;
    frame.style.minHeight = '0';
    frame.style.height = Math.ceil(altura) + 'px';
  });
})();
