// MathSpark Service Worker — v1
// Handles future push notifications and offline caching

const CACHE_NAME = 'mathspark-v1';
const STATIC_ASSETS = ['/manifest.json'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS)),
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)),
      ),
    ),
  );
  self.clients.claim();
});

// Network-first fetch strategy
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request).catch(() =>
      caches.match(event.request).then((r) => r ?? Response.error()),
    ),
  );
});

// Future: push notification handler
self.addEventListener('push', (event) => {
  if (!event.data) return;
  const { title, body, icon } = event.data.json();
  event.waitUntil(
    self.registration.showNotification(title, {
      body,
      icon: icon ?? '/icons/icon-192x192.png',
      badge: '/icons/icon-72x72.png',
    }),
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then((windowClients) => {
      if (windowClients.length > 0) {
        return windowClients[0].focus();
      }
      return clients.openWindow('/chapters');
    }),
  );
});
