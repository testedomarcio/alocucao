(() => {
  'use strict';
  document.querySelectorAll('[data-featured-voices]').forEach(widget => {
    const list = widget.querySelector('.featured-list');
    if (!list) return;
    const cards = [...list.children];
    for (let i = cards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [cards[i], cards[j]] = [cards[j], cards[i]];
    }
    list.append(...cards);
    cards.forEach(card => {
      const audio = card.querySelector('audio'), error = card.querySelector('.featured-error');
      audio.addEventListener('error', () => { if (error) error.hidden = false; });
      audio.addEventListener('playing', () => { if (error) error.hidden = true; });
      audio.addEventListener('play', () => {
        document.querySelectorAll('audio').forEach(other => { if (other !== audio) other.pause(); });
      });
    });
  });
})();
