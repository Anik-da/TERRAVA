const CACHE_NAME = 'terrava-cache-v1';
const DYNAMIC_CACHE_NAME = 'terrava-dynamic-v1';

// Static assets to cache immediately on SW install
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './terrava-logo.png',
  './terrava-config.js',
  './terrava_ag_os_dashboard/index.html',
  './terrava_ai_farm_doctor/index.html',
  './terrava_emergency_sos_rural_support_center_3/index.html',
  './terrava_livestock_guardian/index.html',
  './terrava_profile_settings_center/index.html',
  './terrava_crop_intelligence_center/index.html',
  './terrava_digital_farm_twin/index.html',
  './terrava_ag_os_command_center/index.html',
  './terrava_market_intelligence_center/index.html',
  './terrava_government_benefits_center/index.html'
];

// Install Event — pre-cache core offline shells
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[TERRAVA-SW] Pre-caching Core Offline Assets...');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event — cleanup old cache versions
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME && key !== DYNAMIC_CACHE_NAME) {
            console.log('[TERRAVA-SW] Cleaning up stale cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Interceptor — Dual-Strategy Router
self.addEventListener('fetch', (event) => {
  const requestUrl = new URL(event.request.url);

  // Skip non-GET requests (POST, PUT, DELETE should be handled by sync engines)
  if (event.request.method !== 'GET') {
    return;
  }

  // Strategy A: Network-First with Cache Fallback for API calls (/api/v1)
  if (requestUrl.pathname.includes('/api/v1')) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          // If successful network call, duplicate response into dynamic cache
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(DYNAMIC_CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Off-grid fallback: match request from dynamic cache
          console.warn('[TERRAVA-SW] Off-grid. Accessing dynamic cache fallback for:', requestUrl.pathname);
          return caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) return cachedResponse;
            
            // Construct a fallback JSON response if not cached
            return new Response(JSON.stringify({
              offline: true,
              error: "Network unavailable. Serving off-grid offline data.",
              timestamp: Date.now()
            }), {
              headers: { 'Content-Type': 'application/json' }
            });
          });
        })
    );
    return;
  }

  // Strategy B: Cache-First for local static assets and images
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        // Return from cache immediately, then fetch and update cache in background (Stale-While-Revalidate)
        fetch(event.request).then((networkResponse) => {
          if (networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, networkResponse);
            });
          }
        }).catch(() => {/* Ignore background sync failures */});
        return cachedResponse;
      }

      // If not in cache, fetch from network
      return fetch(event.request)
        .then((response) => {
          if (response.status === 200 || response.status === 0) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          // Fallback to home/index if page completely missing off-grid
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
    })
  );
});
