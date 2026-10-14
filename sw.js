// Retire the old panel launcher cache so returning visitors see the current journey.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('alocucao-painel-')).map(key => caches.delete(key)))).then(() => self.registration.unregister()));
});
