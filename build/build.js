// build/build.js — Marque Publishing static site build
// Reconstitutes pages from src/pages/ + build/partials/ into site/.
// Shared nav / footer / tracking / fade-in script live in ONE place each.
// Usage: node build/build.js
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src', 'pages');
const OUT = path.join(ROOT, 'site');
const PARTIALS = path.join(__dirname, 'partials');

const partial = (n) => fs.readFileSync(path.join(PARTIALS, n + '.html'), 'utf8');
const NAV = partial('nav');
const FOOTER = partial('footer');
const MAILERLITE = partial('mailerlite');
const SCRIPTS = partial('scripts');

const NAV_ITEMS = {
  home:  ['/', 'Home'],
  books: ['/books', 'Books'],
  about: ['/about', 'About'],
  blog:  ['/blog', 'Blog'],
  labs:  ['/labs', 'Labs'],
};

function navFor(active) {
  if (!active || !NAV_ITEMS[active]) return NAV;
  const [href, label] = NAV_ITEMS[active];
  return NAV.replace(`<a href="${href}">${label}</a>`,
                     `<a href="${href}" class="active">${label}</a>`);
}

function render(html) {
  html = html.replace(/<!--#include nav(?: active="([a-z]+)")?-->/g, (_, a) => navFor(a));
  html = html.split('<!--#include footer-->').join(FOOTER);
  html = html.split('<!--#include mailerlite-->').join(MAILERLITE);
  html = html.split('<!--#include scripts-->').join(SCRIPTS);
  return html;
}

function walk(dir, rel = '') {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const abs = path.join(dir, e.name), r = path.join(rel, e.name);
    if (e.isDirectory()) walk(abs, r);
    else if (e.name.endsWith('.html')) {
      const out = path.join(OUT, r);
      fs.mkdirSync(path.dirname(out), { recursive: true });
      fs.writeFileSync(out, render(fs.readFileSync(abs, 'utf8')));
      console.log('  built', r);
    }
  }
}

if (!fs.existsSync(SRC)) { console.error('No src/pages/ found — run refactor first.'); process.exit(1); }
console.log('Building site/ from src/pages/ ...');
walk(SRC);
console.log('Done.');
