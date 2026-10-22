/* Official showcase messages are accepted only from the iframe we embedded. */
(() => {
  if (!document.body.hasAttribute('data-single-offer')) return;
  window.addEventListener('message', event => {
    const frame = document.getElementById('vitrine-vozes');
    if (!frame || event.origin !== 'https://vozes.alocucao.com.br' || event.source !== frame.contentWindow || !event.data || !event.data.vitrineVozes) return;
    const height = Number(event.data.altura);
    if (!Number.isFinite(height) || height <= 0) return;
    frame.style.minHeight = '0';
    frame.style.height = height + 'px';
  });
})();
