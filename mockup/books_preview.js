// mockup/books_preview.js — assemble the catalog mockup. `node mockup/books_preview.js` -> preview/books.html
// `node mockup/books_preview.js --install` -> also writes src/pages/books.html (source) + site/books.html (rendered)
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src', 'pages'), SITE = path.join(ROOT, 'site'), PRE = path.join(ROOT, 'preview'), PART = path.join(ROOT, 'build', 'partials');
const p = n => fs.readFileSync(path.join(PART, n + '.html'), 'utf8');
const NAV = p('nav'), FOOTER = p('footer'), ML = p('mailerlite'), SCRIPTS = p('scripts');
const NAV_ITEMS = { home: ['/', 'Home'], books: ['/books', 'Books'], about: ['/about', 'About'], blog: ['/blog', 'Blog'], labs: ['/labs', 'Labs'] };
const navFor = a => { if (!a || !NAV_ITEMS[a]) return NAV; const [h, l] = NAV_ITEMS[a]; return NAV.replace(`<a href="${h}">${l}</a>`, `<a href="${h}" class="active">${l}</a>`); };
const render = h => h.replace(/<!--#include nav(?: active="([a-z]+)")?-->/g, (_, a) => navFor(a))
  .split('<!--#include footer-->').join(FOOTER).split('<!--#include mailerlite-->').join(ML).split('<!--#include scripts-->').join(SCRIPTS);

const cur = fs.readFileSync(path.join(SRC, 'books.html'), 'utf8');
const cut = cur.indexOf('<main id="main-content">');
if (cut < 0) throw new Error('no <main>');
const source = cur.slice(0, cut) + fs.readFileSync(path.join(__dirname, 'books-main.html'), 'utf8');
fs.mkdirSync(PRE, { recursive: true });
fs.writeFileSync(path.join(PRE, 'books.html'), render(source));
console.log('preview/books.html written');
if (process.argv.includes('--install')) {
  const ARCH = path.join(ROOT, '_archive', 'pre-redesign-2026-09-15');
  fs.mkdirSync(ARCH, { recursive: true });
  fs.copyFileSync(path.join(SRC, 'books.html'), path.join(ARCH, 'src-books.html'));
  fs.copyFileSync(path.join(SITE, 'books.html'), path.join(ARCH, 'site-books.html'));
  fs.writeFileSync(path.join(SRC, 'books.html'), source);
  fs.writeFileSync(path.join(SITE, 'books.html'), render(source));
  console.log('installed src/pages/books.html + site/books.html');
}
