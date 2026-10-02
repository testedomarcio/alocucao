(() => {
  'use strict';
  const header = document.querySelector('.al-header');
  if (!header) return;
  const button = header.querySelector('.al-menu-toggle'), menu = header.querySelector('.al-menu');
  if (!button || !menu) return;
  header.dataset.enhanced = 'true';
  const setOpen = open => {
    menu.classList.toggle('is-open', open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  };
  button.addEventListener('click', () => setOpen(button.getAttribute('aria-expanded') !== 'true'));
  menu.addEventListener('click', event => { if (event.target.closest('a')) setOpen(false); });
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      setOpen(false); button.focus();
    }
  });
  document.addEventListener('click', event => { if (!header.contains(event.target)) setOpen(false); });
  window.matchMedia('(max-width:1100px)').addEventListener('change', () => setOpen(false));
  const path = location.pathname;
  const active = path.startsWith('/perfil-locutor-') ? '/vozes/' : path.startsWith('/blog/') ? '/blog/' : path;
  menu.querySelectorAll('a[href]').forEach(link => {
    if (link.getAttribute('href') === active) link.setAttribute('aria-current', 'page');
  });
  const year = document.querySelector('.al-footer #year');
  if (year) year.textContent = String(new Date().getFullYear());
})();
