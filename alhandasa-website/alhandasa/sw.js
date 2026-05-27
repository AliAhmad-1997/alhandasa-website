const CACHE = "alhandasa-v1";
const FILES = [
  "./",
  "./index.html",
  "./packages.html",
  "./contact.html",
  "./shop.html",
  "./sections.html",
  "./css/styles.css",
  "./css/custom.css",
  "./js/theme.js",
  "./logo.svg",
  "./manifest.json"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(FILES))
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request))
  );
});
