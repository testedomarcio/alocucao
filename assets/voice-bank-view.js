/* Shared catalog/audio nodes. Only the list presentation is progressively enhanced. */
(() => {
  'use strict';
  const key = 'alocucao.voiceBank.view';
  const viewport = matchMedia('(min-width: 1100px)');
  let preference, syncView = () => {};
  try { preference = localStorage.getItem(key); } catch (_) { /* Storage may be disabled. */ }
  if (!['list', 'cards'].includes(preference)) preference = null;
  function apply(view) {
    document.documentElement.dataset.voiceView = view;
    document.querySelectorAll('.bank-view-switch button').forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.voiceView === view));
    });
    syncView(view);
  }
  apply(preference || (viewport.matches ? 'list' : 'cards'));
  document.addEventListener('DOMContentLoaded', () => {
    const control = document.querySelector('.bank-view-switch');
    if (!control) return;
    const grid = document.querySelector('#voice-results');
    if (grid) syncView = enhanceDemos(grid);
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

  function enhanceDemos(grid) {
    const triggers = [...grid.querySelectorAll('[data-bank-demo]')];
    let active = null;
    const records = triggers.map(button => {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      const audio = panel.querySelector('audio');
      return {button, panel, audio, card: button.closest('.voice-card')};
    });
    function close(record, pause = true) {
      if (!record) return;
      if (pause) record.audio.pause();
      record.button.setAttribute('aria-expanded', 'false');
      record.panel.classList.remove('is-open');
      if (active === record) active = null;
    }
    function reveal(record) {
      if (active !== record) close(active);
      active = record;
      record.panel.classList.add('is-open');
      record.button.setAttribute('aria-expanded', 'true');
    }
    records.forEach(record => {
      record.button.addEventListener('click', () => {
        if (active === record) { close(record); return; }
        reveal(record);
        // Playback is requested only after the visitor explicitly chooses a demo.
        record.audio.play().catch(() => { /* Native controls/error message stay available. */ });
      });
      record.panel.querySelector('.bank-demo-close').addEventListener('click', () => {
        close(record);
        record.button.focus({preventScroll: true});
      });

    });
    grid.addEventListener('keydown', event => {
      if (event.key !== 'Escape' || !active || !active.card.contains(event.target)) return;
      const record = active;
      event.preventDefault(); close(record); record.button.focus({preventScroll: true});
    }, true);
    grid.addEventListener('play', event => {
      const record = records.find(r => r.audio === event.target);
      if (record && !record.audio.paused && !record.card.hidden) reveal(record);
    }, true);
    const form = document.querySelector('.filters');
    const checkFiltered = () => { if (active?.card.hidden) close(active); };
    form?.addEventListener('input', checkFiltered);
    form?.addEventListener('change', checkFiltered);
    grid.classList.add('bank-demos-ready');
    return view => {
      if (view !== 'list') return;
      const playing = records.find(r => !r.audio.paused && !r.card.hidden);
      if (playing) reveal(playing);
      checkFiltered();
    };
  }
})();
