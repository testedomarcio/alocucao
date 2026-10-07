(() => {
  const players = [...document.querySelectorAll('audio')];
  players.forEach(audio => {
    const error = audio.closest('.audio-card').querySelector('.audio-error');
    audio.addEventListener('error', () => { error.hidden = false; });
    audio.addEventListener('playing', () => { error.hidden = true; });
    audio.addEventListener('play', () => {
      players.forEach(other => { if (other !== audio) other.pause(); });
      window.alocucaoTrackEvent?.('audio_play', { audio_name: audio.dataset.voice, page_path: location.pathname });
    });
  });
})();
