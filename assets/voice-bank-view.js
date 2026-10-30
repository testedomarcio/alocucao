/* Set the presentation before paint. The catalog, order and audio nodes are shared. */
(() => {
  'use strict';
  const key = 'alocucao.voiceBank.view';
  const viewport = matchMedia('(min-width: 1100px)');
  let preference;
  try { preference = localStorage.getItem(key); } catch (_) { /* Storage may be disabled. */ }
  if (!['list', 'cards'].includes(preference)) preference = null;
  function apply(view) {
    document.documentElement.dataset.voiceView = view;
    document.querySelectorAll('.bank-view-switch button').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.voiceView === view));
    });
  }
  apply(preference || (viewport.matches ? 'list' : 'cards'));
  document.addEventListener('DOMContentLoaded', () => {
    const control = document.querySelector('.bank-view-switch');
    if (!control) return;
    control.querySelectorAll('button').forEach(button => button.addEventListener('click', () => {
      preference = button.dataset.voiceView;
      apply(preference);
      try { localStorage.setItem(key, preference); } catch (_) { /* Keep the session choice. */ }
    }));
    apply(preference || (viewport.matches ? 'list' : 'cards'));
    control.hidden = false;
    viewport.addEventListener('change', () => {
      if (!preference) apply(viewport.matches ? 'list' : 'cards');
    });
  });
})();
