// mockup/build_preview.js — assemble the redesign mockup into preview/ (NOT site/).
// Homepage: current head+CSS from src/pages/index.html, new <main> from mockup/home-main.html.
// Labs: src/pages/labs.html with the team callout + newsletter replaced.
// Then copy every asset the pages need so preview/ can be served standalone.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SRC = path.join(ROOT, 'src', 'pages');
const OUT = path.join(ROOT, 'preview');
const PART = path.join(ROOT, 'build', 'partials');
const p = n => fs.readFileSync(path.join(PART, n + '.html'), 'utf8');
const NAV = p('nav'), FOOTER = p('footer'), ML = p('mailerlite'), SCRIPTS = p('scripts');
const NAV_ITEMS = { home: ['/', 'Home'], books: ['/books', 'Books'], about: ['/about', 'About'], blog: ['/blog', 'Blog'], labs: ['/labs', 'Labs'] };
const navFor = a => { if (!a || !NAV_ITEMS[a]) return NAV; const [h, l] = NAV_ITEMS[a]; return NAV.replace(`<a href="${h}">${l}</a>`, `<a href="${h}" class="active">${l}</a>`); };
const render = h => h.replace(/<!--#include nav(?: active="([a-z]+)")?-->/g, (_, a) => navFor(a))
  .split('<!--#include footer-->').join(FOOTER).split('<!--#include mailerlite-->').join(ML).split('<!--#include scripts-->').join(SCRIPTS);

fs.mkdirSync(OUT, { recursive: true });

// Homepage
const idx = fs.readFileSync(path.join(SRC, 'index.html'), 'utf8');
const cut = idx.indexOf('<main id="main-content">');
if (cut < 0) throw new Error('no <main> in index.html');
const home = idx.slice(0, cut) + fs.readFileSync(path.join(__dirname, 'home-main.html'), 'utf8');
fs.writeFileSync(path.join(OUT, 'index.html'), render(home));

// Labs
let labs = fs.readFileSync(path.join(SRC, 'labs.html'), 'utf8');
const a = labs.indexOf('<!-- ─── Team callout ─── -->');
const b = labs.indexOf('</main>');
if (a < 0 || b < 0) throw new Error('labs markers missing');
const engineer = fs.readFileSync(path.join(__dirname, 'labs-engineer.html'), 'utf8');
const newsletter = `

<!-- ─── Newsletter ─── -->
<section class="newsletter section-pad">
  <div class="container">
    <div class="newsletter-inner fade-in">
      <h2>Stay in The Loop</h2>
      <p>Get notified when we launch &mdash; plus the free <em>Creating with Claude</em> toolkit.</p>
      <div class="ml-embedded" data-form="By4UIw"></div>
    </div>
  </div>
</section>
`;
labs = labs.slice(0, a) + engineer + newsletter + labs.slice(b);
fs.writeFileSync(path.join(OUT, 'labs.html'), render(labs));

// Assets: css folder, root images, favicons, plus the new photo
const SITE = path.join(ROOT, 'site');
fs.cpSync(path.join(SITE, 'css'), path.join(OUT, 'css'), { recursive: true });
for (const f of fs.readdirSync(SITE)) if (/\.(png|jpg|jpeg|svg|ico|webp)$/i.test(f)) fs.copyFileSync(path.join(SITE, f), path.join(OUT, f));
fs.copyFileSync(path.join(__dirname, 'jayden.jpg'), path.join(OUT, 'jayden.jpg'));
// simple redirect stubs so nav links resolve on the local server
for (const [f, t] of [['books.html', '/books'], ['about.html', '/about'], ['blog.html', '/blog']]) {
  fs.writeFileSync(path.join(OUT, f), `<!doctype html><meta http-equiv="refresh" content="0;url=https://www.marquepublishing.com${t}"><a href="https://www.marquepublishing.com${t}">${t} (live site)</a>`);
}
console.log('preview built:', OUT);
