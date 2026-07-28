// build/refactor.js — ONE-TIME: extract shared partials from index.html and
// rewrite the main pages in src/pages/ to use <!--#include ...--> directives.
// Safe: only replaces blocks that match verbatim; anything else is left inline.
// Usage: node build/refactor.js
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');
const SRC = path.join(ROOT, 'src', 'pages');
const PARTIALS = path.join(__dirname, 'partials');

const rd = (p) => fs.readFileSync(p, 'utf8');
const wr = (p, c) => { fs.mkdirSync(path.dirname(p), { recursive: true }); fs.writeFileSync(p, c); };

const navRe    = /<!--[^\n]*Navigation[^\n]*-->\r?\n<nav[\s\S]*?<\/nav>/;
const footerRe = /<!--[^\n]*Footer[^\n]*-->\r?\n<footer[\s\S]*?<\/footer>/;
const mlRe     = /<!-- MailerLite Universal -->[\s\S]*?<!-- End MailerLite Universal -->/;
const scrRe    = /<script>\r?\n\/\/ Scroll-triggered fade-in[\s\S]*?<\/script>/;

// 1) Extract canonical partials from index.html (nav stored WITHOUT active state)
const idx = rd(path.join(SITE, 'index.html'));
const navPlain = idx.match(navRe)[0].replace(/ class="active"/g, '');
wr(path.join(PARTIALS, 'nav.html'), navPlain);
wr(path.join(PARTIALS, 'footer.html'), idx.match(footerRe)[0]);
wr(path.join(PARTIALS, 'mailerlite.html'), idx.match(mlRe)[0]);
wr(path.join(PARTIALS, 'scripts.html'), idx.match(scrRe)[0]);
console.log('Partials written: nav, footer, mailerlite, scripts');

// 2) Convert the main pages
const PAGES = ['index.html', 'books.html', 'about.html', 'blog.html', 'labs.html', '404.html'];
const NAV_HREFS = { '/': 'home', '/books': 'books', '/about': 'about', '/blog': 'blog', '/labs': 'labs' };

for (const rel of PAGES) {
  const p = path.join(SITE, rel);
  if (!fs.existsSync(p)) { console.log('  skip (missing):', rel); continue; }
  let html = rd(p);
  const hits = [];
  const nm = html.match(navRe);
  if (nm) {
    const am = nm[0].match(/<a href="([^"]+)" class="active">/);
    const active = am ? NAV_HREFS[am[1]] : '';
    html = html.replace(navRe, active ? `<!--#include nav active="${active}"-->` : '<!--#include nav-->');
    hits.push('nav' + (active ? `(${active})` : ''));
  }
  if (footerRe.test(html)) { html = html.replace(footerRe, '<!--#include footer-->'); hits.push('footer'); }
  if (mlRe.test(html))     { html = html.replace(mlRe, '<!--#include mailerlite-->'); hits.push('mailerlite'); }
  if (scrRe.test(html))    { html = html.replace(scrRe, '<!--#include scripts-->'); hits.push('scripts'); }
  wr(path.join(SRC, rel), html);
  console.log('  ' + rel + ' -> ' + (hits.join(', ') || 'NO MATCHES (left inline)'));
}
console.log('Refactor complete. Now run: node build/build.js');
