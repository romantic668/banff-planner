const CACHE = "banff-v1";
const ASSETS = ["/", "/static/styles.css", "/static/manifest.webmanifest"];

self.addEventListener("install", e => {
    e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
    self.skipWaiting();
});
self.addEventListener("activate", e => {
    e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
    self.clients.claim();
});
self.addEventListener("fetch", e => {
    const url = new URL(e.request.url);
    if (url.pathname.startsWith("/api/")) {
        e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
        return;
    }
    e.respondWith(caches.match(e.request).then(c => c || fetch(e.request).then(r => {
        const copy = r.clone(); caches.open(CACHE).then(cache => cache.put(e.request, copy)); return r;
    })));
});
