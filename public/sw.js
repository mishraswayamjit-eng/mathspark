// MathSpark Service Worker — v2
// Handles offline caching for static assets and lesson API

const CACHE_NAME = 'mathspark-v2';
const STATIC_ASSETS = ['/manifest.json', '/icon'];

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

// Fetch strategy
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  // Network-first + cache fallback for lesson API (5-min stale)
  if (event.request.url.includes('/api/questions/lesson')) {
    event.respondWith(
      fetch(event.request)
        .then((res) => {
          const clone = res.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return res;
        })
        .catch(() => caches.match(event.request).then((r) => r ?? Response.error())),
    );
    return;
  }

  // Network-first for everything else
  event.respondWith(
    fetch(event.request).catch(() =>
      caches.match(event.request).then((r) => r ?? Response.error()),
    ),
  );
});

// Push notification handler
self.addEventListener('push', (event) => {
  if (!event.data) return;
  const { title, body, icon } = event.data.json();
  event.waitUntil(
    self.registration.showNotification(title, {
      body,
      icon: icon ?? '/icon',
      badge: '/icon',
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
