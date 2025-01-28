/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Anubis. All rights reserved.
 *--------------------------------------------------------------------------------------------*/

const CACHE_NAME = 'anubis-cache-v1';
const PRECACHE_URLS = [
    '/',
    '/index.html',
    '/workbench.js',
    '/workbench.css'
];

self.addEventListener('install', (event: any) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(PRECACHE_URLS))
            .then(() => (self as any).skipWaiting())
    );
});

self.addEventListener('activate', (event: any) => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(cacheName => {
                    return cacheName.startsWith('anubis-cache-') && cacheName !== CACHE_NAME;
                }).map(cacheName => {
                    return caches.delete(cacheName);
                })
            );
        })
    );
});

self.addEventListener('fetch', (event: any) => {
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request)
            .then(response => {
                if (response) {
                    return response;
                }

                return fetch(event.request).then(response => {
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME)
                        .then(cache => {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                });
            })
    );
});