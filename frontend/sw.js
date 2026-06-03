const CACHE_NAME = 'terrava-cache-v8';
const DYNAMIC_CACHE_NAME = 'terrava-dynamic-v8';

// Static assets to cache immediately on SW install
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './terrava-logo.png',
  './drone_satellite_farm_view.png',
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
      // Safe addAll to prevent one missing file from blocking the entire service worker installation
      return Promise.allSettled(
        STATIC_ASSETS.map((asset) => {
          return cache.add(asset)
            .then(() => console.log(`[TERRAVA-SW] Cached successfully: ${asset}`))
            .catch((err) => console.warn(`[TERRAVA-SW] Failed to pre-cache asset: ${asset}. Proceeding anyway.`, err));
        })
      );
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

// Helper to match request, checking for directory index fallbacks (e.g. /path/ -> /path/index.html)
function matchCacheRequest(request) {
  const url = new URL(request.url);
  let pathsToTry = [request.url];

  // If path ends with / or is a directory route (no file extension), try appending index.html
  if (url.pathname.endsWith('/')) {
    pathsToTry.push(url.origin + url.pathname + 'index.html');
  } else if (!url.pathname.split('/').pop().includes('.')) {
    pathsToTry.push(url.origin + url.pathname + '/index.html');
    pathsToTry.push(url.origin + url.pathname + 'index.html');
  }

  // Try matching paths sequentially
  const tryNext = (index) => {
    if (index >= pathsToTry.length) {
      return Promise.resolve(null);
    }
    return caches.match(pathsToTry[index]).then((response) => {
      if (response) return response;
      return tryNext(index + 1);
    });
  };

  return tryNext(0);
}

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
          return matchCacheRequest(event.request).then((cachedResponse) => {
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

  // Strategy A.2: Network-First with Cache Fallback for HTML navigation requests
  // This avoids serving stale pages when navigating between tabs/sections of the platform.
  if (event.request.mode === 'navigate' || (event.request.headers.get('Accept') && event.request.headers.get('Accept').includes('text/html'))) {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              // Cache under the original request object so offline lookup still succeeds
              cache.put(event.request, responseClone);
            });
          }
          return response;
        })
        .catch(() => {
          return matchCacheRequest(event.request).then((cachedResponse) => {
            if (cachedResponse) return cachedResponse;
            // General fallback
            return caches.match('./index.html').then((indexResponse) => {
              if (indexResponse) return indexResponse;
              return caches.match('../index.html');
            });
          });
        })
    );
    return;
  }

  // Strategy B: Cache-First for local static assets and images
  event.respondWith(
    matchCacheRequest(event.request).then((cachedResponse) => {
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
